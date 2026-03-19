"""
Failure Mode Analysis — Human Cancer Driver Gene Network
=========================================================

Cross-domain test using the generic failure_mode_analyzer library.
Adds cancer-specific analysis: comparison of targeted hub removal,
random removal, and cancer driver removal (known oncogenes).

Data: STRING v12, 30 COSMIC Tier 1 drivers + partners, confidence >= 900.
"""

import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from failure_mode_analyzer import (
    FailureModeAnalyzer, load_string_json, network_stats, CANCER_DRIVERS
)
import networkx as nx


def main():
    data_path = SCRIPT_DIR / 'cancer_network_raw.json'

    print('Loading cancer driver gene network...')
    G = load_string_json(data_path)
    stats = network_stats(G)
    print(f'  Nodes: {stats["nodes"]}')
    print(f'  Edges: {stats["edges"]}')
    print(f'  Density: {stats["density"]:.4f}')

    # Baseline betweenness — show cancer driver rankings
    bc = nx.betweenness_centrality(G)
    drivers_in_network = [g for g in CANCER_DRIVERS if g in G]
    sorted_all = sorted(bc.items(), key=lambda x: x[1], reverse=True)
    rank_map = {node: i+1 for i, (node, _) in enumerate(sorted_all)}

    print(f'\nCancer drivers ({len(drivers_in_network)} in network):')
    for gene in sorted(drivers_in_network, key=lambda g: bc.get(g, 0), reverse=True):
        print(f'  {gene:8s}: bc={bc[gene]:.4f}, rank={rank_map[gene]}/{len(G)}, '
              f'degree={G.degree(gene)}')

    top30 = {node for node, _ in sorted_all[:30]}
    drivers_in_top30 = set(CANCER_DRIVERS) & top30
    print(f'\n  Cancer drivers in top-30 betweenness: {len(drivers_in_top30)}/30')
    print(f'  NOTE: High ranking is partly a construction artifact of the')
    print(f'  query design (seed genes dominate hub-and-spoke queries).')

    # Run analysis using the generic library
    analyzer = FailureModeAnalyzer(G, name="Human Cancer Driver Gene Network (STRING/COSMIC)")
    results = analyzer.run(
        n_removals=30,
        domain_targets=CANCER_DRIVERS,
        domain_label="Cancer drivers")
    analyzer.plot(results, output_path=SCRIPT_DIR / 'cancer_failure_modes.png')
    analyzer.print_summary(results)


if __name__ == '__main__':
    main()
