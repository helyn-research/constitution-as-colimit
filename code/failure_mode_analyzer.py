"""
Failure Mode Analyzer — Generic Network Robustness Tool
========================================================

Domain-agnostic tool for analyzing failure mode signatures in any network.
Implements the betweenness-based robustness protocol and classifies the
resulting topological signature as fragmentation, condensation, or neutral.

Supports three removal strategies:
  1. Targeted hub removal (highest betweenness first, recalculated each step)
  2. Random removal (averaged over multiple trials)
  3. Domain-specific removal (user-supplied node list)

Input: any NetworkX graph, or an edge list / GraphML / JSON file.
Output: metrics, classification, and diagnostic plots.

Requirements:
    python >= 3.9
    networkx >= 2.6
    numpy >= 1.20
    matplotlib >= 3.4

Usage:
    from failure_mode_analyzer import FailureModeAnalyzer

    analyzer = FailureModeAnalyzer(G, name="My Network")
    results = analyzer.run(n_removals=30, domain_targets=my_target_list)
    analyzer.plot(results, output_path="my_analysis.png")
    analyzer.print_summary(results)
"""

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from dataclasses import dataclass, field


# ── Metrics ────────────────────────────────────────────────────────────

def gini_coefficient(values):
    """Gini coefficient: 0 = uniform, 1 = maximally concentrated."""
    v = np.sort(np.array(values, dtype=float))
    n = len(v)
    if n == 0 or v.sum() == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * v) - (n + 1) * np.sum(v)) / (n * np.sum(v))


def concentration_ratio(bc_values, top_k=5):
    """Fraction of total betweenness held by top-k nodes."""
    total = bc_values.sum()
    if total == 0:
        return 0.0
    return bc_values[:min(top_k, len(bc_values))].sum() / total


def network_stats(G):
    """Basic network statistics."""
    if len(G) == 0:
        return {'nodes': 0, 'edges': 0, 'components': 0,
                'largest_cc': 0, 'density': 0.0}
    if G.is_directed():
        undirected = G.to_undirected()
    else:
        undirected = G
    components = list(nx.connected_components(undirected))
    largest = max(len(c) for c in components) if components else 0
    return {
        'nodes': len(G),
        'edges': G.number_of_edges(),
        'components': len(components),
        'largest_cc': largest,
        'density': nx.density(G),
    }


def lcc_gini(G):
    """Gini within largest connected component only."""
    if len(G) == 0:
        return 0.0
    if G.is_directed():
        undirected = G.to_undirected()
    else:
        undirected = G
    largest_cc_nodes = max(nx.connected_components(undirected), key=len)
    subgraph = G.subgraph(largest_cc_nodes)
    bc = nx.betweenness_centrality(subgraph)
    return gini_coefficient(list(bc.values()))


def _snapshot(G, bc_vals, step, removed=None):
    """Capture network state at one removal step."""
    return {
        'step': step,
        'removed': removed,
        'stats': network_stats(G),
        'gini': gini_coefficient(bc_vals),
        'gini_lcc': lcc_gini(G),
        'concentration_top5': concentration_ratio(bc_vals),
    }


# ── Removal strategies ────────────────────────────────────────────────

def targeted_removal(G, n_removals):
    """Remove highest-betweenness nodes, recomputing after each."""
    H = G.copy()
    bc = nx.betweenness_centrality(H)
    bc_vals = np.array(sorted(bc.values(), reverse=True))
    history = [_snapshot(H, bc_vals, 0)]

    for i in range(n_removals):
        if len(H) == 0:
            break
        bc = nx.betweenness_centrality(H)
        # Deterministic tie-breaking: highest betweenness, then highest node ID
        target = max(bc, key=lambda n: (bc[n], n))
        H.remove_node(target)
        bc_post = nx.betweenness_centrality(H)
        bc_vals = np.array(sorted(bc_post.values(), reverse=True))
        history.append(_snapshot(H, bc_vals, i + 1, removed=target))
    return history


def ordered_removal(G, removal_order, n_removals):
    """Remove nodes in a specified order."""
    H = G.copy()
    bc = nx.betweenness_centrality(H)
    bc_vals = np.array(sorted(bc.values(), reverse=True))
    history = [_snapshot(H, bc_vals, 0)]

    for i in range(min(n_removals, len(removal_order))):
        node = removal_order[i]
        if node not in H:
            continue
        H.remove_node(node)
        if len(H) == 0:
            break
        bc = nx.betweenness_centrality(H)
        bc_vals = np.array(sorted(bc.values(), reverse=True))
        history.append(_snapshot(H, bc_vals, i + 1, removed=node))
    return history


def random_removal(G, n_removals, n_trials=20):
    """Remove random nodes, averaged over trials with standard errors."""
    bc_base = np.array(sorted(nx.betweenness_centrality(G).values(), reverse=True))
    stats_base = network_stats(G)
    step0 = {
        'gini': gini_coefficient(bc_base),
        'gini_lcc': lcc_gini(G),
        'concentration_top5': concentration_ratio(bc_base),
        'largest_cc': stats_base['largest_cc'],
        'components': stats_base['components'],
    }

    all_trials = []
    for trial in range(n_trials):
        H = G.copy()
        nodes = list(H.nodes())
        rng = np.random.default_rng(seed=42 + trial)
        rng.shuffle(nodes)
        trial_hist = [step0]
        for i in range(n_removals):
            if i >= len(nodes) or len(H) == 0:
                break
            H.remove_node(nodes[i])
            bc = nx.betweenness_centrality(H)
            bc_vals = np.array(sorted(bc.values(), reverse=True))
            stats = network_stats(H)
            trial_hist.append({
                'gini': gini_coefficient(bc_vals),
                'gini_lcc': lcc_gini(H),
                'concentration_top5': concentration_ratio(bc_vals),
                'largest_cc': stats['largest_cc'],
                'components': stats['components'],
            })
        all_trials.append(trial_hist)

    min_len = min(len(t) for t in all_trials)
    avg = []
    for step in range(min_len):
        g = [t[step]['gini'] for t in all_trials]
        gl = [t[step]['gini_lcc'] for t in all_trials]
        avg.append({
            'step': step,
            'gini': np.mean(g), 'gini_se': np.std(g, ddof=1) / np.sqrt(len(g)),
            'gini_lcc': np.mean(gl), 'gini_lcc_se': np.std(gl, ddof=1) / np.sqrt(len(gl)),
            'largest_cc': np.mean([t[step]['largest_cc'] for t in all_trials]),
            'components': np.mean([t[step]['components'] for t in all_trials]),
        })
    return avg


# ── Classification ─────────────────────────────────────────────────────

def classify_signature(history, threshold=0.02):
    """Classify a removal trajectory as fragmentation, condensation, or neutral."""
    if len(history) < 2:
        return 'neutral', 0.0
    # Use step at ~30% of trajectory for robust classification
    check_step = min(max(len(history) // 3, 1), len(history) - 1)
    delta = history[check_step]['gini'] - history[0]['gini']
    if delta < -threshold:
        return 'fragmentation', delta
    elif delta > threshold:
        return 'condensation', delta
    else:
        return 'neutral', delta


# ── Analyzer class ─────────────────────────────────────────────────────

@dataclass
class AnalysisResults:
    """Container for failure mode analysis results."""
    name: str
    n_nodes: int
    n_edges: int
    baseline_gini: float
    targeted: list = field(default_factory=list)
    random: list = field(default_factory=list)
    domain: list = field(default_factory=list)
    domain_label: str = ''
    targeted_signature: str = ''
    domain_signature: str = ''


class FailureModeAnalyzer:
    """Generic failure mode analyzer for any network."""

    def __init__(self, G, name="Network"):
        self.G = G
        self.name = name

    def run(self, n_removals=30, n_random_trials=20, domain_targets=None,
            domain_label="Domain-specific"):
        """Run the full analysis.

        Args:
            n_removals: number of nodes to remove in each strategy
            n_random_trials: number of random removal trials
            domain_targets: optional list of node IDs for domain-specific removal
            domain_label: label for the domain-specific removal strategy
        """
        bc = nx.betweenness_centrality(self.G)
        bc_vals = np.array(sorted(bc.values(), reverse=True))

        results = AnalysisResults(
            name=self.name,
            n_nodes=len(self.G),
            n_edges=self.G.number_of_edges(),
            baseline_gini=gini_coefficient(bc_vals),
        )

        print(f'  Targeted hub removal ({n_removals} steps)...')
        results.targeted = targeted_removal(self.G, n_removals)
        sig, delta = classify_signature(results.targeted)
        results.targeted_signature = sig

        print(f'  Random removal ({n_removals} steps, {n_random_trials} trials)...')
        results.random = random_removal(self.G, n_removals, n_random_trials)

        if domain_targets:
            # Sort by betweenness (highest first)
            domain_in_network = [n for n in domain_targets if n in self.G]
            domain_order = sorted(domain_in_network, key=lambda n: bc.get(n, 0),
                                  reverse=True)
            print(f'  {domain_label} removal ({len(domain_order)} nodes)...')
            results.domain = ordered_removal(self.G, domain_order, n_removals)
            results.domain_label = domain_label
            sig_d, _ = classify_signature(results.domain)
            results.domain_signature = sig_d

        return results

    def plot(self, results, output_path=None):
        """Generate diagnostic plots."""
        has_domain = len(results.domain) > 0
        fig, axes = plt.subplots(2, 3, figsize=(18, 11))
        fig.suptitle(f'Failure Mode Analysis — {results.name}\n'
                     f'({results.n_nodes} nodes, {results.n_edges} edges)',
                     fontsize=14, fontweight='bold')

        n_orig = results.n_nodes

        # Panel A: Gini (full network)
        ax = axes[0, 0]
        t_steps = [h['step'] for h in results.targeted]
        t_gini = [h['gini'] for h in results.targeted]
        r_steps = [h['step'] for h in results.random]
        r_gini = [h['gini'] for h in results.random]
        r_se = [h['gini_se'] for h in results.random]
        ax.plot(t_steps, t_gini, 'r-o', ms=3, lw=1.5, label='Targeted (hub)')
        ax.errorbar(r_steps, r_gini, yerr=r_se, fmt='b--s', ms=3, lw=1.5,
                    label='Random (avg±SE)', capsize=2)
        if has_domain:
            d_steps = [h['step'] for h in results.domain]
            d_gini = [h['gini'] for h in results.domain]
            ax.plot(d_steps, d_gini, 'g-^', ms=4, lw=1.5,
                    label=results.domain_label)
        ax.axhline(y=t_gini[0], color='gray', ls=':', alpha=0.5)
        ax.set_xlabel('Nodes Removed')
        ax.set_ylabel('Gini Coefficient')
        ax.set_title('A. Betweenness Concentration (Gini)')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Panel B: Gini (LCC only)
        ax = axes[0, 1]
        t_glcc = [h['gini_lcc'] for h in results.targeted]
        r_glcc = [h['gini_lcc'] for h in results.random]
        r_glcc_se = [h['gini_lcc_se'] for h in results.random]
        ax.plot(t_steps, t_glcc, 'r-o', ms=3, lw=1.5, label='Targeted')
        ax.errorbar(r_steps, r_glcc, yerr=r_glcc_se, fmt='b--s', ms=3, lw=1.5,
                    label='Random', capsize=2)
        if has_domain:
            d_glcc = [h['gini_lcc'] for h in results.domain]
            ax.plot(d_steps, d_glcc, 'g-^', ms=4, lw=1.5,
                    label=results.domain_label)
        ax.axhline(y=t_glcc[0], color='gray', ls=':', alpha=0.5)
        ax.set_xlabel('Nodes Removed')
        ax.set_ylabel('Gini (LCC only)')
        ax.set_title('B. Gini Within Largest Component')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Panel C: Top-5 concentration
        ax = axes[0, 2]
        t_c5 = [h['concentration_top5'] for h in results.targeted]
        ax.plot(t_steps, t_c5, 'r-o', ms=3, lw=1.5, label='Targeted')
        if has_domain:
            d_c5 = [h['concentration_top5'] for h in results.domain]
            ax.plot(d_steps, d_c5, 'g-^', ms=4, lw=1.5,
                    label=results.domain_label)
        ax.set_xlabel('Nodes Removed')
        ax.set_ylabel('Top-5 Share')
        ax.set_title('C. Top-5 Concentration')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Panel D: Largest CC
        ax = axes[1, 0]
        t_lcc = [h['stats']['largest_cc'] / n_orig for h in results.targeted]
        r_lcc = [h['largest_cc'] / n_orig for h in results.random]
        ax.plot(t_steps, t_lcc, 'r-o', ms=3, lw=1.5, label='Targeted')
        ax.plot(r_steps, r_lcc, 'b--s', ms=3, lw=1.5, label='Random')
        if has_domain:
            d_lcc = [h['stats']['largest_cc'] / n_orig for h in results.domain]
            ax.plot(d_steps, d_lcc, 'g-^', ms=4, lw=1.5,
                    label=results.domain_label)
        ax.set_xlabel('Nodes Removed')
        ax.set_ylabel('Fraction of Original')
        ax.set_title('D. Largest Connected Component')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Panel E: Components
        ax = axes[1, 1]
        t_comp = [h['stats']['components'] for h in results.targeted]
        r_comp = [h['components'] for h in results.random]
        ax.plot(t_steps, t_comp, 'r-o', ms=3, lw=1.5, label='Targeted')
        ax.plot(r_steps, r_comp, 'b--s', ms=3, lw=1.5, label='Random')
        if has_domain:
            d_comp = [h['stats']['components'] for h in results.domain]
            ax.plot(d_steps, d_comp, 'g-^', ms=4, lw=1.5,
                    label=results.domain_label)
        ax.set_xlabel('Nodes Removed')
        ax.set_ylabel('Components')
        ax.set_title('E. Network Fragmentation')
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # Panel F: Cross-domain summary
        ax = axes[1, 2]
        ax.axis('off')
        summary = (
            f"FAILURE MODE CLASSIFICATION\n\n"
            f"Targeted hub removal:\n"
            f"  → {results.targeted_signature.upper()}\n\n"
        )
        if has_domain:
            summary += (
                f"{results.domain_label}:\n"
                f"  → {results.domain_signature.upper()}\n\n"
            )
        summary += (
            f"Baseline Gini: {results.baseline_gini:.4f}\n"
            f"Nodes: {results.n_nodes}\n"
            f"Edges: {results.n_edges}"
        )
        ax.text(0.1, 0.9, summary, transform=ax.transAxes, fontsize=12,
                verticalalignment='top', fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

        plt.tight_layout()
        if output_path:
            plt.savefig(output_path, dpi=150, bbox_inches='tight')
            print(f'  Plot saved to {output_path}')
        plt.close()

    def print_summary(self, results):
        """Print summary to console."""
        print(f'\n{"="*60}')
        print(f'{results.name} — FAILURE MODE ANALYSIS')
        print(f'{"="*60}')
        print(f'Nodes: {results.n_nodes}, Edges: {results.n_edges}')
        print(f'Baseline Gini: {results.baseline_gini:.4f}')

        step = min(10, len(results.targeted) - 1)
        t0 = results.targeted[0]
        t = results.targeted[step]
        delta_t = t['gini'] - t0['gini']
        print(f'\nTargeted ({step} steps): Gini {t0["gini"]:.4f} -> {t["gini"]:.4f} '
              f'(delta={delta_t:+.4f}) -> {results.targeted_signature.upper()}')

        if results.domain:
            d_step = min(10, len(results.domain) - 1)
            d = results.domain[d_step]
            delta_d = d['gini'] - t0['gini']
            print(f'{results.domain_label} ({d_step} steps): '
                  f'Gini {t0["gini"]:.4f} -> {d["gini"]:.4f} '
                  f'(delta={delta_d:+.4f}) -> {results.domain_signature.upper()}')

        r = results.random[min(10, len(results.random) - 1)]
        delta_r = r['gini'] - results.random[0]['gini']
        print(f'Random (10 steps avg): Gini delta={delta_r:+.4f} -> NEUTRAL')


# ── Domain-specific constants ──────────────────────────────────────────

# 30 Tier 1 cancer driver genes (COSMIC Cancer Gene Census)
CANCER_DRIVERS = [
    'TP53', 'PIK3CA', 'KRAS', 'PTEN', 'APC', 'BRAF', 'EGFR', 'BRCA1', 'BRCA2',
    'RB1', 'MYC', 'CDKN2A', 'NRAS', 'IDH1', 'CTNNB1', 'JAK2', 'ALK', 'ERBB2',
    'SMAD4', 'VHL', 'KIT', 'FGFR3', 'ABL1', 'RET', 'MET', 'CDH1', 'NOTCH1',
    'FBXW7', 'NPM1', 'DNMT3A',
]


# ── Convenience loaders ────────────────────────────────────────────────

def load_edgelist(path, directed=False, delimiter=None, comment='%',
                  node_type=int):
    """Load a network from an edge list file.

    Args:
        node_type: callable to convert node IDs (default: int).
            Use str for non-numeric node labels.
    """
    G = nx.DiGraph() if directed else nx.Graph()
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(comment):
                continue
            parts = line.split(delimiter)
            if len(parts) >= 2:
                try:
                    G.add_edge(node_type(parts[0].strip()),
                               node_type(parts[1].strip()))
                except (ValueError, TypeError):
                    G.add_edge(parts[0].strip(), parts[1].strip())
    return G


def load_string_json(path):
    """Load a STRING database JSON export."""
    import json
    with open(path, encoding='utf-8') as f:
        data = json.load(f)
    G = nx.Graph()
    for d in data:
        a = d['preferredName_A']
        b = d['preferredName_B']
        if a != b:
            G.add_edge(a, b, weight=d.get('score', 1.0))
    return G
