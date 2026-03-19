"""
Failure Mode Analysis — Little Rock Lake Food Web
==================================================

Tests the framework's prediction that system failure produces measurably
distinct topological signatures in betweenness centrality distributions:

  - Fragmentation: betweenness distribution flattens (no dominant hubs)
  - Condensation: betweenness concentrates (remaining nodes absorb all paths)

Method: compare targeted removal (highest-betweenness nodes first) vs.
random removal, tracking how the betweenness distribution changes.

Data: Little Rock Lake, Wisconsin food web (Martinez 1991).
183 taxa, 2494 directed feeding links. Edge convention: prey -> predator.
Source: KONECT / Koblenz Network Collection (maayan-foodweb).
Citation: Martinez, N. D. (1991). Artifacts or Attributes? Effects of
    Resolution on the Little Rock Lake Food Web. Ecological Monographs,
    61(4), 367-392. doi:10.2307/2937047

Requirements:
    python >= 3.9
    networkx >= 2.6
    numpy >= 1.20
    matplotlib >= 3.4

Usage:
    python foodweb_analysis.py

    The script resolves paths relative to its own location.
    Produces:
      - Console output with summary statistics
      - foodweb_failure_modes.png in the same directory

    Results are deterministic (fixed random seeds, explicit tie-breaking).
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from failure_mode_analyzer import (
    gini_coefficient, concentration_ratio, network_stats, lcc_gini,
    targeted_removal, random_removal, load_edgelist,
)

SCRIPT_DIR = Path(__file__).resolve().parent


# ── Visualization ──────────────────────────────────────────────────────

def plot_results(targeted_hist, random_hist, G_original, output_dir):
    """Generate analysis plots."""
    fig, axes = plt.subplots(2, 3, figsize=(18, 11))
    fig.suptitle(
        'Failure Mode Analysis — Little Rock Lake Food Web\n'
        '(Martinez 1991, 183 taxa, targeted hub removal vs. random)',
        fontsize=14, fontweight='bold')

    n_orig = targeted_hist[0]['stats']['nodes']

    # 1. Baseline betweenness distribution (log-log)
    ax = axes[0, 0]
    bc_baseline = np.array(sorted(
        nx.betweenness_centrality(G_original).values(), reverse=True))
    bc_nonzero = bc_baseline[bc_baseline > 0]
    rank = np.arange(1, len(bc_nonzero) + 1)
    ax.loglog(rank, bc_nonzero, 'ko-', markersize=3, linewidth=0.8)
    ax.set_xlabel('Rank')
    ax.set_ylabel('Betweenness Centrality')
    ax.set_title('A. Baseline Betweenness\n(rank-frequency, log-log)')
    ax.grid(True, alpha=0.3)

    # 2. Top-5 concentration over removal steps
    ax = axes[0, 1]
    t_c5 = [h['concentration_top5'] for h in targeted_hist]
    ax.plot(t_steps, t_c5, 'r-o', markersize=3, linewidth=1.5,
            label='Targeted (hub)')
    ax.axhline(y=t_c5[0], color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel('Nodes Removed')
    ax.set_ylabel('Top-5 Share')
    ax.set_title('B. Top-5 Betweenness Concentration')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # 3. Gini coefficient over removal steps (FULL NETWORK)
    ax = axes[0, 2]
    t_steps = [h['step'] for h in targeted_hist]
    t_gini = [h['gini'] for h in targeted_hist]
    r_steps = [h['step'] for h in random_hist]
    r_gini = [h['gini'] for h in random_hist]
    r_gini_se = [h['gini_se'] for h in random_hist]
    ax.plot(t_steps, t_gini, 'r-o', markersize=3, linewidth=1.5,
            label='Targeted (hub)')
    ax.errorbar(r_steps, r_gini, yerr=r_gini_se, fmt='b--s', markersize=3,
                linewidth=1.5, label='Random (avg±SE, 20 trials)', capsize=2)
    ax.axhline(y=t_gini[0], color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel('Nodes Removed')
    ax.set_ylabel('Gini Coefficient')
    ax.set_title('C. Betweenness Concentration (Gini)\n↑ = condensation, ↓ = fragmentation')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # 4. Gini coefficient within LARGEST CONNECTED COMPONENT only
    ax = axes[1, 0]
    t_gini_lcc = [h['gini_lcc'] for h in targeted_hist]
    r_gini_lcc = [h['gini_lcc'] for h in random_hist]
    r_gini_lcc_se = [h['gini_lcc_se'] for h in random_hist]
    ax.plot(t_steps, t_gini_lcc, 'r-o', markersize=3, linewidth=1.5,
            label='Targeted (hub)')
    ax.errorbar(r_steps, r_gini_lcc, yerr=r_gini_lcc_se, fmt='b--s',
                markersize=3, linewidth=1.5, label='Random (avg±SE)', capsize=2)
    ax.axhline(y=t_gini_lcc[0], color='gray', linestyle=':', alpha=0.5)
    ax.set_xlabel('Nodes Removed')
    ax.set_ylabel('Gini (LCC only)')
    ax.set_title('D. Gini Within Largest Component\n(controls for finite-size artifact)')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # 5. Largest connected component size
    ax = axes[1, 1]
    t_lcc = [h['stats']['largest_cc'] for h in targeted_hist]
    r_lcc = [h['largest_cc'] for h in random_hist]
    t_lcc_frac = [x / n_orig for x in t_lcc]
    r_lcc_frac = [x / n_orig for x in r_lcc]
    ax.plot(t_steps, t_lcc_frac, 'r-o', markersize=3, linewidth=1.5,
            label='Targeted')
    ax.plot(r_steps, r_lcc_frac, 'b--s', markersize=3, linewidth=1.5,
            label='Random')
    ax.set_xlabel('Nodes Removed')
    ax.set_ylabel('Fraction of Original Network')
    ax.set_title('E. Largest Connected Component\n(fragmentation = sharp drop)')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    # 6. Number of components
    ax = axes[1, 2]
    t_comp = [h['stats']['components'] for h in targeted_hist]
    r_comp = [h['components'] for h in random_hist]
    ax.plot(t_steps, t_comp, 'r-o', markersize=3, linewidth=1.5,
            label='Targeted')
    ax.plot(r_steps, r_comp, 'b--s', markersize=3, linewidth=1.5,
            label='Random')
    ax.set_xlabel('Nodes Removed')
    ax.set_ylabel('Number of Components')
    ax.set_title('F. Network Fragmentation\n(fragmentation = sharp rise)')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    output_path = output_dir / 'foodweb_failure_modes.png'
    plt.savefig(output_path, dpi=150, bbox_inches='tight')
    print(f'Saved plot to {output_path}')
    plt.close()
    return output_path


# ── Main ───────────────────────────────────────────────────────────────

def main():
    data_path = SCRIPT_DIR / 'foodweb_data' / 'maayan-foodweb' / 'out.maayan-foodweb'

    print('Loading Little Rock Lake food web...')
    G = load_edgelist(data_path, directed=True)
    stats = network_stats(G)
    print(f'  Nodes: {stats["nodes"]}')
    print(f'  Edges: {stats["edges"]}')
    print(f'  Self-loops: {nx.number_of_selfloops(G)}')
    print(f'  Components: {stats["components"]}')
    print(f'  Largest CC: {stats["largest_cc"]}')
    print(f'  Density: {stats["density"]:.4f}')
    print(f'  Edge convention: prey -> predator (KONECT standard)')

    # Baseline betweenness
    bc = nx.betweenness_centrality(G)
    bc_vals = np.array(sorted(bc.values(), reverse=True))
    print(f'\nBaseline betweenness:')
    print(f'  Gini coefficient: {gini_coefficient(bc_vals):.4f}')
    print(f'  Gini (LCC only): {lcc_gini(G):.4f}')
    print(f'  Top-5 concentration: {concentration_ratio(bc_vals):.4f}')
    print(f'  Max betweenness: {bc_vals[0]:.4f}')
    print(f'  Nodes with bc > 0: {np.sum(bc_vals > 0)} / {len(bc_vals)}')

    # Top-10 most central nodes with trophic interpretation
    top_nodes = sorted(bc.items(), key=lambda x: x[1], reverse=True)[:10]
    print(f'\n  Top-10 highest betweenness nodes:')
    print(f'  (Edge convention: prey->predator, so in-degree = prey count)')
    for node, centrality in top_nodes:
        in_deg = G.in_degree(node)   # number of prey (species this node eats)
        out_deg = G.out_degree(node) # number of predators (species that eat this node)
        print(f'    Node {node:3d}: bc={centrality:.4f}, '
              f'prey={in_deg}, predators={out_deg}')

    # Targeted removal
    n_remove = 30
    print(f'\nRunning targeted removal ({n_remove} steps)...')
    targeted_hist = targeted_removal(G, n_remove)

    print(f'Running random removal ({n_remove} steps, 20 trials)...')
    random_hist = random_removal(G, n_remove, n_trials=20)

    # Summary
    print(f'\n{"="*60}')
    print('RESULTS SUMMARY')
    print(f'{"="*60}')

    step_10 = min(10, len(targeted_hist) - 1)
    print(f'\nBaseline:')
    print(f'  Gini = {targeted_hist[0]["gini"]:.4f}')
    print(f'  Gini (LCC) = {targeted_hist[0]["gini_lcc"]:.4f}')
    print(f'  Top-5 concentration = {targeted_hist[0]["concentration_top5"]:.4f}')

    print(f'\nAfter {step_10} targeted removals:')
    t = targeted_hist[step_10]
    t0 = targeted_hist[0]
    print(f'  Gini = {t["gini"]:.4f} (delta = {t["gini"] - t0["gini"]:+.4f})')
    print(f'  Gini (LCC) = {t["gini_lcc"]:.4f} (delta = {t["gini_lcc"] - t0["gini_lcc"]:+.4f})')
    print(f'  Top-5 = {t["concentration_top5"]:.4f} (delta = {t["concentration_top5"] - t0["concentration_top5"]:+.4f})')
    print(f'  Largest CC = {t["stats"]["largest_cc"]} / {t0["stats"]["nodes"]}')
    print(f'  Components = {t["stats"]["components"]}')

    print(f'\nAfter {step_10} random removals (avg of 20 trials):')
    r = random_hist[step_10]
    r0 = random_hist[0]
    print(f'  Gini = {r["gini"]:.4f} (delta = {r["gini"] - r0["gini"]:+.4f})')
    print(f'  Gini (LCC) = {r["gini_lcc"]:.4f} (delta = {r["gini_lcc"] - r0["gini_lcc"]:+.4f})')
    print(f'  Largest CC = {r["largest_cc"]:.1f} / {t0["stats"]["nodes"]}')

    if t["gini"] < t0["gini"]:
        print(f'\n>>> TARGETED: Gini DECREASED -> fragmentation signature')
    else:
        print(f'\n>>> TARGETED: Gini INCREASED -> condensation signature')

    if t["gini_lcc"] < t0["gini_lcc"]:
        print(f'>>> TARGETED (LCC): Gini DECREASED -> fragmentation persists in LCC')
    else:
        print(f'>>> TARGETED (LCC): Gini INCREASED -> condensation in LCC')

    # Generate plots
    print('\nGenerating plots...')
    plot_path = plot_results(targeted_hist, random_hist, G, SCRIPT_DIR)
    print(f'\nDone. Plot saved to: {plot_path}')


if __name__ == '__main__':
    main()
