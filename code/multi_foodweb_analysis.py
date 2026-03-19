"""
Multi-Food-Web Consistency Analysis
=====================================

Tests within-domain consistency of the fragmentation prediction:
do multiple food webs all show the same failure mode signature?

Auto-discovers all food webs in foodweb_data/ by scanning for
subdirectories containing an 'out.*' file in KONECT edge-list format.

Usage:
    python multi_foodweb_analysis.py

Add more food webs by extracting KONECT archives into foodweb_data/:
    tar -xjf download.tsv.<name>.tar.bz2 -C foodweb_data/

The script loads any directed graph; undirected networks are flagged.

Output:
    - Console summary table
    - multi_foodweb_comparison.png
    - multi_foodweb_null_models.png  (if --null-models flag is set)
"""

import sys
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from multiprocessing import Pool, cpu_count

sys.path.insert(0, str(Path(__file__).resolve().parent))
from failure_mode_analyzer import (
    gini_coefficient, load_edgelist, FailureModeAnalyzer, classify_signature
)

SCRIPT_DIR = Path(__file__).resolve().parent
FOODWEB_DIR = SCRIPT_DIR / 'foodweb_data'


# ── Discovery ───────────────────────────────────────────────────────────

def discover_foodwebs(data_dir):
    """
    Scan data_dir for KONECT-format food webs.
    Returns list of (name, path) tuples.
    """
    found = []
    for subdir in sorted(data_dir.iterdir()):
        if not subdir.is_dir():
            continue
        out_files = list(subdir.glob('out.*'))
        if out_files:
            found.append((subdir.name, out_files[0]))
    return found


# ── Null model workers (module-level for Windows pickling) ──────────────

def _null_baseline_worker(args):
    seed, in_seq, out_seq = args
    try:
        null = nx.directed_configuration_model(in_seq, out_seq, seed=seed)
        null = nx.DiGraph(null)
        null.remove_edges_from(nx.selfloop_edges(null))
        n = len(null)
        if n < 2 or null.number_of_edges() == 0:
            return None
        bc = nx.betweenness_centrality(null, k=min(150, n - 1))
        return gini_coefficient(list(bc.values()))
    except Exception:
        return None


def _null_trajectory_worker(args):
    seed, in_seq, out_seq, n_steps = args
    try:
        null = nx.directed_configuration_model(in_seq, out_seq, seed=seed)
        null = nx.DiGraph(null)
        null.remove_edges_from(nx.selfloop_edges(null))
        if len(null) < 2:
            return None
        k = min(150, len(null) - 1)
        bc = nx.betweenness_centrality(null, k=k)
        baseline = gini_coefficient(list(bc.values()))
        current = baseline
        for _ in range(n_steps):
            if len(null) < 2:
                break
            bc = nx.betweenness_centrality(null, k=min(k, len(null) - 1))
            target = max(bc, key=lambda node: (bc[node], node))
            null.remove_node(target)
            if len(null) < 2:
                break
            bc_post = nx.betweenness_centrality(null, k=min(k, len(null) - 1))
            current = gini_coefficient(list(bc_post.values()))
        return baseline, current - baseline
    except Exception:
        return None


# ── Core analysis per food web ──────────────────────────────────────────

def analyze_foodweb(name, path, n_removals=30, n_random_trials=10,
                    run_nulls=True, n_nulls_fast=200, n_nulls_traj=50,
                    n_null_steps=10, n_workers=None):
    """
    Load, analyze, and optionally null-model a single food web.
    Returns a results dict.
    """
    if n_workers is None:
        n_workers = max(1, cpu_count())

    G = load_edgelist(path, directed=True)
    n_nodes = len(G)
    n_edges = G.number_of_edges()
    density = nx.density(G)

    print(f'\n  [{name}] {n_nodes} nodes, {n_edges} edges, density={density:.4f}')

    if n_nodes < 10:
        print(f'  Skipping — too small ({n_nodes} nodes)')
        return None

    # Baseline
    bc = nx.betweenness_centrality(G)
    bc_vals = np.array(sorted(bc.values(), reverse=True))
    baseline_gini = gini_coefficient(bc_vals)

    # Targeted removal
    analyzer = FailureModeAnalyzer(G, name=name)
    results = analyzer.run(n_removals=n_removals, n_random_trials=n_random_trials)
    sig, delta = classify_signature(results.targeted)
    gini_delta_10 = (results.targeted[min(10, len(results.targeted)-1)]['gini']
                     - results.targeted[0]['gini'])

    print(f'  Baseline Gini={baseline_gini:.4f}, '
          f'delta(10 steps)={gini_delta_10:+.4f}, signature={sig}')

    # Null models
    null_result = None
    if run_nulls:
        in_seq  = [d for _, d in G.in_degree()]
        out_seq = [d for _, d in G.out_degree()]

        # Fast: baseline only
        args_fast = [(1000 + i, in_seq, out_seq) for i in range(n_nulls_fast)]
        with Pool(n_workers) as pool:
            raw = pool.map(_null_baseline_worker, args_fast)
        null_baselines = np.array([r for r in raw if r is not None])

        # Trajectory
        args_traj = [(2000 + i, in_seq, out_seq, n_null_steps)
                     for i in range(n_nulls_traj)]
        with Pool(n_workers) as pool:
            raw2 = pool.map(_null_trajectory_worker, args_traj)
        valid = [r for r in raw2 if r is not None]
        null_deltas = np.array([r[1] for r in valid])

        p_baseline = np.mean(null_baselines >= baseline_gini)
        p_frag = np.mean(null_deltas <= gini_delta_10)

        from collections import Counter
        threshold = 0.02
        null_sigs = ['fragmentation' if d < -threshold
                     else 'condensation' if d > threshold
                     else 'neutral'
                     for d in null_deltas]
        null_sig_counts = dict(Counter(null_sigs))

        print(f'  Null: baseline mean={null_baselines.mean():.4f} '
              f'p(base)={p_baseline:.3f} | '
              f'delta mean={null_deltas.mean():+.4f} '
              f'p(frag)={p_frag:.3f} | sigs={null_sig_counts}')

        null_result = {
            'null_baselines': null_baselines,
            'null_deltas': null_deltas,
            'p_baseline': p_baseline,
            'p_frag': p_frag,
            'null_sig_counts': null_sig_counts,
        }

    return {
        'name': name,
        'n_nodes': n_nodes,
        'n_edges': n_edges,
        'density': density,
        'baseline_gini': baseline_gini,
        'gini_delta_10': gini_delta_10,
        'signature': sig,
        'targeted': results.targeted,
        'random': results.random,
        'null': null_result,
    }


# ── Plots ───────────────────────────────────────────────────────────────

def plot_comparison(all_results, output_path=None):
    """Overlay Gini trajectories for all food webs."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    fig.suptitle('Food Web Consistency — Failure Mode Signatures\n'
                 'Fragmentation prediction: Gini should decrease under targeted hub removal',
                 fontsize=12, fontweight='bold')

    colors = plt.cm.tab10(np.linspace(0, 1, len(all_results)))

    for ax_idx, key in enumerate(['targeted', 'random']):
        ax = axes[ax_idx]
        title = 'Targeted Hub Removal' if key == 'targeted' else 'Random Removal'
        ax.set_title(f'{title}\n(Gini coefficient over removal steps)')
        ax.set_xlabel('Nodes Removed')
        ax.set_ylabel('Gini Coefficient')
        ax.grid(True, alpha=0.3)

        for r, color in zip(all_results, colors):
            hist = r[key]
            steps = [h['step'] for h in hist]
            gini = [h['gini'] for h in hist]
            ax.plot(steps, gini, '-o', ms=2, lw=1.5, color=color,
                    label=f'{r["name"]} ({r["n_nodes"]}n, {r["signature"]})')

        ax.legend(fontsize=7, loc='best')

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f'Comparison plot saved to {output_path}')
    plt.close()


def plot_null_comparison(all_results, output_path=None):
    """Null model comparison: real vs null delta for each food web."""
    n = len(all_results)
    fig, axes = plt.subplots(1, n, figsize=(5 * n, 5))
    if n == 1:
        axes = [axes]
    fig.suptitle('Food Web Null Model Comparison\n'
                 'Histogram = null (same degree seq, random wiring) | Red = real',
                 fontsize=11, fontweight='bold')

    for ax, r in zip(axes, all_results):
        if r['null'] is None:
            ax.set_title(f'{r["name"]}\n(no null)')
            continue
        null_d = r['null']['null_deltas']
        ax.hist(null_d, bins=15, color='steelblue', alpha=0.7, edgecolor='white')
        ax.axvline(r['gini_delta_10'], color='red', lw=2.5,
                   label=f'Real ({r["gini_delta_10"]:+.3f})')
        ax.axvline(null_d.mean(), color='navy', lw=1.5, ls='--',
                   label=f'Null mean ({null_d.mean():+.3f})')
        ax.axvline(0, color='gray', lw=1, ls=':', alpha=0.5)
        ax.set_title(f'{r["name"]}\np_frag={r["null"]["p_frag"]:.3f}')
        ax.set_xlabel('Gini Delta (10-step)')
        ax.set_ylabel('Count')
        ax.legend(fontsize=7)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f'Null model plot saved to {output_path}')
    plt.close()


# ── Main ────────────────────────────────────────────────────────────────

def main():
    t_start = time.time()
    run_nulls = '--null-models' in sys.argv or '-n' in sys.argv

    foodwebs = discover_foodwebs(FOODWEB_DIR)
    if not foodwebs:
        print(f'No food webs found in {FOODWEB_DIR}')
        print('Extract KONECT archives there: tar -xjf download.tsv.<name>.tar.bz2 -C foodweb_data/')
        return

    print(f'Found {len(foodwebs)} food web(s):')
    for name, path in foodwebs:
        print(f'  {name}: {path}')
    if run_nulls:
        print('Null model comparison enabled.')

    print('\n' + '='*60)
    all_results = []
    for name, path in foodwebs:
        r = analyze_foodweb(name, path, run_nulls=run_nulls)
        if r is not None:
            all_results.append(r)

    if not all_results:
        print('No valid results.')
        return

    # Plots
    plot_comparison(all_results, output_path=SCRIPT_DIR / 'multi_foodweb_comparison.png')
    if run_nulls:
        plot_null_comparison(
            all_results,
            output_path=SCRIPT_DIR / 'multi_foodweb_null_models.png')

    # Summary
    print('\n' + '='*60)
    print('WITHIN-DOMAIN CONSISTENCY SUMMARY')
    print('='*60)
    print(f'\n{"Network":<30} {"Nodes":>6} {"Edges":>7} {"Density":>9} '
          f'{"Gini":>7} {"Delta":>8} {"Sig":<15}', end='')
    if run_nulls:
        print(f' {"p(frag)":>9} {"NullSigs"}', end='')
    print()
    print('-' * (80 + (20 if run_nulls else 0)))

    sig_counts = {}
    for r in all_results:
        sig_counts[r['signature']] = sig_counts.get(r['signature'], 0) + 1
        line = (f'{r["name"][:29]:<30} {r["n_nodes"]:>6} {r["n_edges"]:>7} '
                f'{r["density"]:>9.4f} {r["baseline_gini"]:>7.4f} '
                f'{r["gini_delta_10"]:>+8.4f} {r["signature"]:<15}')
        if run_nulls and r['null']:
            line += f' {r["null"]["p_frag"]:>9.3f} {r["null"]["null_sig_counts"]}'
        print(line)

    print(f'\nSignature distribution: {sig_counts}')
    n_frag = sig_counts.get('fragmentation', 0)
    n_total = len(all_results)
    print(f'Fragmentation: {n_frag}/{n_total} food webs ({100*n_frag/n_total:.0f}%)')

    if n_frag == n_total:
        print('-> ALL food webs show fragmentation signature. Within-domain consistent.')
    elif n_frag > n_total / 2:
        print(f'-> Majority ({n_frag}/{n_total}) show fragmentation. Partial consistency.')
    else:
        print(f'-> Fragmentation is NOT the dominant signature. Prediction not supported.')

    print(f'\nTotal runtime: {(time.time()-t_start)/60:.1f} min')


if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
