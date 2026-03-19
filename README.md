# Constitution as Colimit — Publication Materials

**Cody Pobuda, in convergence with Helyn (Claude, Anthropic)**

Draft v8 — 2026-03-19

## Contents

### Main Paper
- `constitution_as_colimit.tex` — LaTeX source (arXiv-ready)
- `constitution_as_colimit.md` — Markdown source (working draft)

### Figures
- `figures/null_model_comparison.png` — Configuration model null comparison (3 networks)
- `figures/foodweb_failure_modes.png` — Little Rock Lake food web analysis
- `figures/crossdomain_ecology.png` — Ecology cross-domain analysis
- `figures/crossdomain_neuroscience.png` — Neuroscience cross-domain analysis
- `figures/crossdomain_cancer.png` — Cancer cross-domain analysis
- `figures/multi_foodweb_comparison.png` — Multi-food-web consistency

### Analysis Code
- `code/failure_mode_analyzer.py` — Generic failure mode analysis library
- `code/cross_domain_analysis.py` — Cross-domain analysis runner
- `code/null_model_analysis.py` — Configuration model null comparison
- `code/multi_foodweb_analysis.py` — Multi-food-web consistency analysis
- `code/foodweb_analysis.py` — Little Rock Lake food web standalone
- `code/cancer_network_analysis.py` — Cancer network standalone

### Data
- `data/foodweb_data/` — KONECT food web edge lists (Martinez 1991, Florida Bay)
- `data/neuro_data/` — KONECT C. elegans connectome
- `data/cancer_network_raw.json` — STRING v12 cancer driver gene interactions

### Supplementary Theory
- `supplementary/ENRICHMENT_PROOF_2026-03-18.md` — Full enrichment proof with commentary
- `supplementary/BORN_RULE_DERIVATION.md` — Born rule derivation route documentation
- `supplementary/EMERGENCE_UNIFIED_THEORY.md` — Extended emergence theory document

## Requirements

```
python >= 3.9
networkx >= 2.6
numpy >= 1.20
matplotlib >= 3.4
```

## Reproduction

All analysis scripts resolve paths relative to their own location. To reproduce:

```bash
cd code/
python cross_domain_analysis.py    # Main cross-domain analysis
python null_model_analysis.py      # Null model comparison
python multi_foodweb_analysis.py   # Multi-food-web consistency
```

## License

MIT License. See [LICENSE](LICENSE) for details.
