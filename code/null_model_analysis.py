"""
Null Model Analysis — Configuration Model (Parallel)
=====================================================

Tests whether failure mode signatures in the three domain networks
are explained by degree sequence alone, using configuration model nulls.

For each network:
  1. FAST PHASE (N=500 nulls): compare baseline Gini only
     — Is the real network's initial betweenness concentration unusual?

  2. TRAJECTORY PHASE (N=100 nulls): run targeted removal to step 10
     — Does the real signature type persist vs. null expectations?

If real values fall outside null distribution (p < 0.05):
    The signature is not explained by degree sequence alone — structural.
If real values fall within null distribution (p >= 0.05):
    The signature may be a degree-sequence artifact.

Null graph generation and betweenness computation are parallelized across
CPU cores using multiprocessing.Pool.

Approximate betweenness (k=150) used for null graphs.
Exact betweenness used for real networks.

Estimated runtime: 2-4 minutes on a modern multi-core machine.
"""

import sys
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path
from multiprocessing import Pool, cpu_count
from collections import Counter

sys.path.insert(0, str(Path(__file__).resolve().parent))
from failure_mode_analyzer import gini_coefficient, load_edgelist, load_string_json

SCRIPT_DIR = Path(__file__).resolve().parent


# ── Worker functions (module-level: required for Windows pickling) ──────

def _baseline_worker(args):
    """Generate one null graph, return its baseline Gini. Used in Phase 1."""
    seed, in_seq, out_seq, directed = args
    try:
        if directed:
            null = nx.directed_configuration_model(in_seq, out_seq, seed=seed)
            null = nx.DiGraph(null)
        else:
            null = nx.configuration_model(in_seq, seed=seed)
            null = nx.Graph(null)
        null.remove_edges_from(nx.selfloop_edges(null))
        n = len(null)
        if n < 2 or null.number_of_edges() == 0:
            return None
        bc = nx.betweenness_centrality(null, k=min(150, n - 1))
        return gini_coefficient(list(bc.values()))
    except Exception:
        return None


def _trajectory_worker(args):
    """
    Generate one null graph, run n_steps targeted hub removal.
    Returns (baseline_gini, gini_delta). Used in Phase 2.
    """
    seed, in_seq, out_seq, directed, n_steps = args
    try:
        if directed:
            null = nx.directed_configuration_model(in_seq, out_seq, seed=seed)
            null = nx.DiGraph(null)
        else:
            null = nx.configuration_model(in_seq, seed=seed)
            null = nx.Graph(null)
        null.remove_edges_from(nx.selfloop_edges(null))
        if len(null) < 2:
            return None

        k = min(150, len(null) - 1)
        bc = nx.betweenness_centrality(null, k=k)
        baseline = gini_coefficient(list(bc.values()))
        current_gini = baseline

        for _ in range(n_steps):
            if len(null) < 2:
                break
            bc = nx.betweenness_centrality(null, k=min(k, len(null) - 1))
            target = max(bc, key=lambda node: (bc[node], node))
            null.remove_node(target)
            if len(null) < 2:
                break
            bc_post = nx.betweenness_centrality(null, k=min(k, len(null) - 1))
            current_gini = gini_coefficient(list(bc_post.values()))

        return baseline, current_gini - baseline
    except Exception:
        return None


# ── Real network (exact betweenness) ───────────────────────────────────

def real_network_stats(G, n_steps=10):
    """Exact baseline Gini and Gini delta under targeted removal."""
    H = G.copy()
    bc = nx.betweenness_centrality(H)
    baseline = gini_coefficient(list(bc.values()))
    current_gini = baseline

    for _ in range(n_steps):
        if len(H) < 2:
            break
        bc = nx.betweenness_centrality(H)
        target = max(bc, key=lambda node: (bc[node], node))
        H.remove_node(target)
        if len(H) < 2:
            break
        bc_post = nx.betweenness_centrality(H)
        current_gini = gini_coefficient(list(bc_post.values()))

    return baseline, current_gini - baseline


# ── Core analysis ───────────────────────────────────────────────────────

def run_null_analysis(G, directed, label,
                      n_fast=500, n_traj=100, n_steps=10, n_workers=None):
    """
    Run null model analysis for one network.

    Phase 1: n_fast nulls, baseline Gini only (fast).
    Phase 2: n_traj nulls, full n_steps targeted removal trajectory (slower).
    """
    if n_workers is None:
        n_workers = max(1, cpu_count())

    print(f'\n  [{label}] {len(G)} nodes, {G.number_of_edges()} edges  '
          f'| {n_workers} workers')

    # Degree sequences for workers (small, cheap to serialize)
    if directed:
        in_seq  = [d for _, d in G.in_degree()]
        out_seq = [d for _, d in G.out_degree()]
    else:
        in_seq  = [d for _, d in G.degree()]
        out_seq = in_seq  # unused for undirected

    # Real network (exact)
    t0 = time.time()
    real_baseline, real_delta = real_network_stats(G, n_steps)
    print(f'  Real: baseline Gini={real_baseline:.4f}, '
          f'delta({n_steps} steps)={real_delta:+.4f}  [{time.time()-t0:.1f}s]')

    # Phase 1: baseline Gini across n_fast nulls
    print(f'  Phase 1: {n_fast} nulls, baseline Gini...', flush=True)
    t0 = time.time()
    args_fast = [(1000 + i, in_seq, out_seq, directed) for i in range(n_fast)]
    with Pool(n_workers) as pool:
        raw = pool.map(_baseline_worker, args_fast)
    null_baselines = np.array([r for r in raw if r is not None])
    print(f'  Phase 1 done: {len(null_baselines)}/{n_fast} valid  '
          f'[{time.time()-t0:.1f}s]')
    print(f'  Null baseline: mean={null_baselines.mean():.4f} '
          f'± {null_baselines.std():.4f}  [real={real_baseline:.4f}]')

    p_baseline = np.mean(null_baselines >= real_baseline)
    print(f'  p(null_baseline >= real): {p_baseline:.3f}')

    # Phase 2: trajectory comparison
    print(f'  Phase 2: {n_traj} nulls, {n_steps}-step removal...', flush=True)
    t0 = time.time()
    args_traj = [(2000 + i, in_seq, out_seq, directed, n_steps)
                 for i in range(n_traj)]
    with Pool(n_workers) as pool:
        raw2 = pool.map(_trajectory_worker, args_traj)
    valid = [r for r in raw2 if r is not None]
    null_deltas = np.array([r[1] for r in valid])
    print(f'  Phase 2 done: {len(null_deltas)}/{n_traj} valid  '
          f'[{time.time()-t0:.1f}s]')
    print(f'  Null delta: mean={null_deltas.mean():+.4f} '
          f'± {null_deltas.std():.4f}  [real={real_delta:+.4f}]')

    p_frag = np.mean(null_deltas <= real_delta)
    p_cond = np.mean(null_deltas >= real_delta)
    print(f'  p(null_delta <= real) [fragmentation]: {p_frag:.3f}')
    print(f'  p(null_delta >= real) [condensation]:  {p_cond:.3f}')

    threshold = 0.02
    sig_types = []
    for d in null_deltas:
        if d < -threshold:
            sig_types.append('fragmentation')
        elif d > threshold:
            sig_types.append('condensation')
        else:
            sig_types.append('neutral')
    sig_counts = dict(Counter(sig_types))
    print(f'  Null signature types: {sig_counts}')

    return {
        'label': label,
        'real_baseline': real_baseline,
        'real_delta': real_delta,
        'null_baselines': null_baselines,
        'null_deltas': null_deltas,
        'p_baseline': p_baseline,
        'p_frag': p_frag,
        'p_cond': p_cond,
        'null_sig_counts': sig_counts,
    }


# ── Plot ────────────────────────────────────────────────────────────────

def plot_null_comparison(results_list, output_path=None):
    """2-row × N-col: baseline Gini (top) and Gini delta (bottom)."""
    n = len(results_list)
    fig, axes = plt.subplots(2, n, figsize=(6 * n, 10))
    fig.suptitle(
        'Null Model Comparison — Configuration Model\n'
        'Histogram = null distribution (same degree sequence, random wiring)  '
        '|  Red line = real network',
        fontsize=12, fontweight='bold'
    )

    for col, r in enumerate(results_list):
        label = r['label']

        # Row 0: baseline Gini
        ax = axes[0, col]
        ax.hist(r['null_baselines'], bins=30, color='steelblue',
                alpha=0.7, edgecolor='white')
        ax.axvline(r['real_baseline'], color='red', lw=2.5,
                   label=f'Real ({r["real_baseline"]:.3f})')
        mu = r['null_baselines'].mean()
        ax.axvline(mu, color='navy', lw=1.5, ls='--',
                   label=f'Null mean ({mu:.3f})')
        ax.set_title(f'{label}\nBaseline Gini  p={r["p_baseline"]:.3f}',
                     fontsize=10)
        ax.set_xlabel('Gini Coefficient')
        ax.set_ylabel('Count')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Row 1: Gini delta
        ax = axes[1, col]
        ax.hist(r['null_deltas'], bins=20, color='steelblue',
                alpha=0.7, edgecolor='white')
        ax.axvline(r['real_delta'], color='red', lw=2.5,
                   label=f'Real ({r["real_delta"]:+.3f})')
        mu_d = r['null_deltas'].mean()
        ax.axvline(mu_d, color='navy', lw=1.5, ls='--',
                   label=f'Null mean ({mu_d:+.3f})')
        ax.axvline(0, color='gray', lw=1, ls=':', alpha=0.6)

        p_shown = r['p_frag'] if r['real_delta'] < 0 else r['p_cond']
        p_label = 'p_frag' if r['real_delta'] < 0 else 'p_cond'
        ax.set_title(f'Gini Delta (10-step removal)  {p_label}={p_shown:.3f}',
                     fontsize=10)
        ax.set_xlabel('Gini Delta (after − before)')
        ax.set_ylabel('Count')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    if output_path:
        plt.savefig(output_path, dpi=150, bbox_inches='tight')
        print(f'\nPlot saved to {output_path}')
    plt.close()


# ── Main ────────────────────────────────────────────────────────────────

def main():
    t_start = time.time()
    all_results = []

    # 1. Food web (directed)
    print('\n' + '='*60)
    print('NULL MODEL 1: ECOLOGY — Little Rock Lake Food Web')
    print('='*60)
    G_food = load_edgelist(
        SCRIPT_DIR / 'foodweb_data' / 'maayan-foodweb' / 'out.maayan-foodweb',
        directed=True)
    all_results.append(
        run_null_analysis(G_food, directed=True, label='Food Web'))

    # 2. Cancer (undirected)
    print('\n' + '='*60)
    print('NULL MODEL 2: CANCER — Driver Gene Network')
    print('='*60)
    G_cancer = load_string_json(SCRIPT_DIR / 'cancer_network_raw.json')
    all_results.append(
        run_null_analysis(G_cancer, directed=False, label='Cancer'))

    # 3. C. elegans (undirected)
    print('\n' + '='*60)
    print('NULL MODEL 3: NEUROSCIENCE — C. elegans Connectome')
    print('='*60)
    G_neuro = load_edgelist(
        SCRIPT_DIR / 'neuro_data' / 'dimacs10-celegansneural' /
        'out.dimacs10-celegansneural',
        directed=False)
    all_results.append(
        run_null_analysis(G_neuro, directed=False, label='C. elegans'))

    # Plot
    plot_null_comparison(
        all_results,
        output_path=SCRIPT_DIR / 'null_model_comparison.png')

    # Summary
    print('\n' + '='*60)
    print('SUMMARY')
    print('='*60)
    print(f'\n{"Domain":<15} {"Real Gini":>10} {"Null Mean":>10} '
          f'{"p(base)":>9} {"Real Delta":>12} {"p(delta)":>10}  Null sig types')
    print('-' * 90)
    for r in all_results:
        p_d = r['p_frag'] if r['real_delta'] < 0 else r['p_cond']
        print(f'{r["label"]:<15} {r["real_baseline"]:>10.4f} '
              f'{r["null_baselines"].mean():>10.4f} '
              f'{r["p_baseline"]:>9.3f} '
              f'{r["real_delta"]:>+12.4f} '
              f'{p_d:>10.3f}  '
              f'{r["null_sig_counts"]}')

    print('\nInterpretation:')
    print('  p < 0.05 -> signature not explained by degree sequence (structural)')
    print('  p >= 0.05 -> signature consistent with degree-sequence artifact')
    print(f'\nTotal runtime: {(time.time()-t_start)/60:.1f} min')


if __name__ == '__main__':
    import multiprocessing
    multiprocessing.freeze_support()
    main()
