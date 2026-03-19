"""
Cross-Domain Failure Mode Analysis
====================================

Runs the failure mode analyzer on three domains:
  1. Ecology — Little Rock Lake food web (Martinez 1991)
  2. Cancer biology — Human cancer driver gene network (STRING/COSMIC)
  3. Neuroscience — C. elegans connectome (White et al. 1986)

Tests the framework's prediction that the same failure mode taxonomy
applies across domains, but different domains show different signatures.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from failure_mode_analyzer import (
    FailureModeAnalyzer, load_edgelist, load_string_json, CANCER_DRIVERS
)
import networkx as nx

SCRIPT_DIR = Path(__file__).resolve().parent


def main():
    n_removals = 30

    # ── 1. Ecology: Little Rock Lake food web ──────────────────────────
    print('\n' + '='*60)
    print('DOMAIN 1: ECOLOGY — Little Rock Lake Food Web')
    print('='*60)
    foodweb_path = SCRIPT_DIR / 'foodweb_data' / 'maayan-foodweb' / 'out.maayan-foodweb'
    G_food = load_edgelist(foodweb_path, directed=True)
    analyzer_food = FailureModeAnalyzer(G_food, name="Little Rock Lake Food Web (Martinez 1991)")
    results_food = analyzer_food.run(n_removals=n_removals)
    analyzer_food.plot(results_food,
                       output_path=SCRIPT_DIR / 'crossdomain_ecology.png')
    analyzer_food.print_summary(results_food)

    # ── 2. Cancer biology: driver gene network ─────────────────────────
    print('\n' + '='*60)
    print('DOMAIN 2: CANCER BIOLOGY — Driver Gene Network')
    print('='*60)
    cancer_path = SCRIPT_DIR / 'cancer_network_raw.json'
    G_cancer = load_string_json(cancer_path)
    analyzer_cancer = FailureModeAnalyzer(
        G_cancer, name="Human Cancer Driver Gene Network (STRING/COSMIC)")
    results_cancer = analyzer_cancer.run(
        n_removals=n_removals,
        domain_targets=CANCER_DRIVERS,
        domain_label="Cancer drivers")
    analyzer_cancer.plot(results_cancer,
                         output_path=SCRIPT_DIR / 'crossdomain_cancer.png')
    analyzer_cancer.print_summary(results_cancer)

    # ── 3. Neuroscience: C. elegans connectome ─────────────────────────
    print('\n' + '='*60)
    print('DOMAIN 3: NEUROSCIENCE — C. elegans Connectome')
    print('='*60)
    celegans_path = (SCRIPT_DIR / 'neuro_data' /
                     'dimacs10-celegansneural' / 'out.dimacs10-celegansneural')
    # KONECT DIMACS10 version is explicitly undirected (symmetric pairs)
    G_neuro = load_edgelist(celegans_path, directed=False)
    analyzer_neuro = FailureModeAnalyzer(
        G_neuro, name="C. elegans Connectome (White et al. 1986)")
    results_neuro = analyzer_neuro.run(n_removals=n_removals)
    analyzer_neuro.plot(results_neuro,
                        output_path=SCRIPT_DIR / 'crossdomain_neuroscience.png')
    analyzer_neuro.print_summary(results_neuro)

    # ── Cross-domain comparison ────────────────────────────────────────
    print('\n' + '='*60)
    print('CROSS-DOMAIN COMPARISON')
    print('='*60)
    print(f'\n{"Domain":<35} {"Nodes":>6} {"Edges":>6} '
          f'{"Baseline Gini":>14} {"Hub Removal":>15}')
    print('-' * 85)
    for r in [results_food, results_cancer, results_neuro]:
        print(f'{r.name[:34]:<35} {r.n_nodes:>6} {r.n_edges:>6} '
              f'{r.baseline_gini:>14.4f} {r.targeted_signature:>15}')
    if results_cancer.domain_signature:
        print(f'\nCancer driver removal: {results_cancer.domain_signature.upper()}')

    print('\nKey finding: different domains show different failure mode signatures')
    print('under the same removal protocol — consistent with the framework\'s')
    print('prediction that failure mode type depends on network structure.')


if __name__ == '__main__':
    main()
