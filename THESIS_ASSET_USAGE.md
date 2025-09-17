# Thesis Asset & LaTeX Integration Guide

This document explains how to use the centralized assets (figures, tables, models) in your LaTeX thesis, how they are organized, and how to expand visualizations.

---

## 1. Asset Directory Structure

All curated assets live in the versioned repository under `thesis_images/`:

```
thesis_images/
├── figures/          # PNG/SVG/PDF images (versioned)
├── tables/           # CSV tables (versioned)
├── data_snapshots/   # Optional intermediate datasets
├── models/           # Serialized model artifacts (e.g., .h5)
├── summaries/        # Text or JSON summaries
├── manifests/        # asset_manifest.json / asset_manifest.csv
└── latex/            # Auto-generated LaTeX snippets
```

Naming pattern for every asset:

```
<section>__<short_descriptor>__v<major.minor>.<ext>
```

Example: `policy_analysis__policy_impact_quantification__v1.0.csv`

---

## 2. Manifest

Machine-readable inventory at:

- `thesis_images/manifests/asset_manifest.json`
- `thesis_images/manifests/asset_manifest.csv`

Quick load in Python:

```python
import json, pandas as pd
with open('thesis_images/manifests/asset_manifest.json') as f:
    manifest = pd.DataFrame(json.load(f))
manifest.head()
```

---

## 3. Using Tables (CSV) in LaTeX

You have three approaches.

### A. Use Auto-Generated LaTeX Snippets

When saving tables with `ThesisAssetManager.save_table`, a `.tex` snippet is added under `thesis_images/latex/`.

```
\input{thesis_images/latex/model_evaluation__table2_model_performance__v1.0.tex}
```

### B. Use `csvsimple` for Direct CSV Inclusion

Preamble:

```
\usepackage{csvsimple}
```

Usage:

```
\begin{table}[htbp]
  \centering
  \caption{Model Performance Summary}
  \label{tab:model_performance}
  \csvautotabular{thesis_images/tables/model_evaluation__table2_model_performance__v1.0.csv}
\end{table}
```

Custom formatting:

```
\csvreader[
  tabular=|l|c|c|c|,
  table head=\hline Model & RMSE & R\textsuperscript{2} & MAE \\ \hline,
  late after line=\\,
  late after last line=\\\hline
]{thesis_images/tables/model_evaluation__model_performance_comparison__v1.0.csv}{}%
{\csvcoli & \csvcolii & \csvcoliii & \csvcoliv}
```

### C. Use `pgfplotstable` (Alignment & Styling)

```
\usepackage{pgfplotstable}
\pgfplotstableset{col sep=comma}
\begin{table}[htbp]
  \centering
  \caption{Economic Forecasts}
  \label{tab:economic_forecasts}
  \pgfplotstabletypeset{thesis_images/tables/forecasting__table4_economic_forecasts__v1.0.csv}
\end{table}
```

### Regenerating a Table LaTeX Snippet

```
from thesis_asset_manager import ThesisAssetManager
assets = ThesisAssetManager()
assets.export_table_as_latex(section="model_evaluation", name="table2_model_performance", version="1.0")
```

---

## 4. Using Figures in LaTeX

Auto-generated figure snippets live in `thesis_images/latex/figure__...*.tex`.

Bulk include all figure snippets:

```
\input{thesis_images/latex/index_figures.tex}
```

Or single figure:

```
\input{thesis_images/latex/figure__policy_analysis__final_policy_impact_analysis__v1.0.tex}
```

Adjust width by editing the snippet line:

```
\includegraphics[width=0.65\textwidth]{...}
```

---

## 5. Recommended Thesis Placement (Mapping)

| Section          | Asset Type       | Suggested Label            | File Name                                                       |
| ---------------- | ---------------- | -------------------------- | --------------------------------------------------------------- |
| Methodology      | Figure 1         | fig:model_architecture     | general**figure1_model_architecture**v1.0.png                   |
| Methodology      | Figure 2         | fig:data_overview          | general**figure2_economic_data_overview**v1.0.png               |
| Methodology      | Table 1          | tab:descriptive_stats      | general**table1_descriptive_statistics**v1.0.csv                |
| Modeling         | Figure 3         | fig:lstm_training          | forecasting**lstm_training_history**v1.0.png                    |
| Modeling         | Table 2          | tab:model_performance      | model_evaluation**table2_model_performance**v1.0.csv            |
| Modeling         | Table 3          | tab:model_compare          | model_evaluation**model_performance_comparison**v1.0.csv        |
| Modeling         | Table 4          | tab:stability              | model_evaluation**stability_analysis**v1.0.csv                  |
| Modeling         | Table 5          | tab:cv_results             | model_evaluation**cross_validation_results**v1.0.csv            |
| Causal Inference | Figure 4         | fig:causal_forest_overview | causal_inference**causal_forest_results**v1.0.png               |
| Causal Inference | Table 6          | tab:cf_feature_importance  | causal_inference**causal_forest_feature_importance**v1.0.csv    |
| Causal Inference | Table 7          | tab:dml_feature_importance | causal_inference**dml_feature_importance**v1.0.csv              |
| Causal Inference | Table 8          | tab:cf_heterogeneous       | causal_inference**causal_forest_heterogeneous_effects**v1.0.csv |
| Causal Inference | Table 9          | tab:dml_heterogeneous      | causal_inference**dml_heterogeneous_effects**v1.0.csv           |
| Policy Analysis  | Figure 5         | fig:policy_impact_summary  | policy_analysis**final_policy_impact_analysis**v1.0.png         |
| Policy Analysis  | Figure 6         | fig:vat_interactive        | policy_analysis**interactive_vat_5.0percent_analysis**v1.0.png  |
| Policy Analysis  | Figure 7         | fig:hybrid_policy_panel    | policy_analysis**hybrid_policy_analysis_comprehensive**v1.0.png |
| Policy Analysis  | Table 10         | tab:policy_quant           | policy_analysis**policy_impact_quantification**v1.0.csv         |
| Policy Analysis  | Table 11         | tab:policy_metrics         | policy_analysis**policy_impact_metrics**v1.0.csv                |
| Policy Analysis  | Table 12         | tab:scenario_analysis      | policy_analysis**policy_scenario_analysis**v1.0.csv             |
| Policy Analysis  | Table 13         | tab:vat_scenarios          | policy_analysis**vat_increase_scenario_analysis**v1.0.csv       |
| Policy Analysis  | Table 14         | tab:vat_interactive_impact | policy_analysis**interactive_vat_5.0percent_impact**v1.0.csv    |
| Policy Analysis  | Table 15         | tab:policy_summary         | policy_analysis**table3_policy_impact_summary**v1.0.csv         |
| Policy Analysis  | Table 16         | tab:cf_recommendations     | policy_analysis**causal_forest_policy_recommendations**v1.0.csv |
| Forecast Results | Table (Optional) | tab:hybrid_forecasts       | forecasting**hybrid_economic_forecasts**v1.0.csv                |
| Forecast Results | Table (Optional) | tab:lstm_forecasts         | forecasting**lstm_forecasts**v1.0.csv                           |
| Appendix         | Table (Optional) | tab:detailed_model_compare | general**table5_detailed_model_comparison**v1.0.csv             |

---

## 6. Generating / Regenerating Snippets

When new assets are added:

```
python generate_latex_snippets.py
```

This refreshes figure snippets, indexes, and `master_assets_overview.tex`.

---

## 7. Adding New Visualizations

Suggested additions:

1. **Forecast vs Actual Curve** – Base vs Hybrid + confidence band.
2. **Residual Diagnostics** – Residual histogram + QQ/ACF (normality & autocorrelation).
3. **Treatment Effect Distribution** – Histogram/density of ITEs (Causal Forest).
4. **Feature Importance Comparison** – Side-by-side DML vs Causal Forest.
5. **Scenario Trajectories** – Multi-line plot for alternative tax or macro scenarios.
6. **Uncertainty Decomposition** – Contribution of model vs scenario vs causal adjustments.
7. **Heterogeneity Heatmap** – Effect intensity across regimes (e.g., growth × firm size).
8. **Ensemble Weights** – Donut chart or time-evolution if dynamic weights.
9. **Sensitivity (Tornado Plot)** – Effect magnitude under parameter perturbations.
10. **Rolling Policy Impact** – Moving window cumulative effect curve.

### Code Sketch Example (Forecast vs Actual)

```python
fig, ax = plt.subplots(figsize=(8,4))
ax.plot(actual.index, actual.values, label='Actual', color='black')
ax.plot(hybrid.index, hybrid.values, label='Hybrid Forecast', color='tab:blue')
ax.fill_between(hybrid.index, lower_ci, upper_ci, color='tab:blue', alpha=0.2, label='95% CI')
ax.set_title('Hybrid Forecast vs Actual')
ax.legend(frameon=False)
assets.save_figure(fig, section='forecasting', name='hybrid_forecast_vs_actual', description='Hybrid model forecast with confidence interval', tags=['forecast','hybrid'])
```

---

## 8. Consistent Styling

```python
import matplotlib.pyplot as plt
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'figure.dpi': 110,
    'axes.titlesize': 12,
    'axes.labelsize': 11,
    'legend.fontsize': 9,
    'savefig.dpi': 350,
})
```

For vector quality in LaTeX: `assets.save_figure(fig, ..., formats=['png','pdf'])`.

---

## 9. Referencing in LaTeX

Figures use labels like:

```
\label{fig:policy_analysis_final_policy_impact_analysis}
```

Tables use:

```
\label{tab:model_performance}
```

Then cite: `Figure~\ref{fig:policy_analysis_final_policy_impact_analysis}`.

---

## 10. Versioning Strategy

- Increment version on material change: `v1.0` → `v1.1`.
- Keep older versions for reproducibility until thesis freeze.
- If using Git tags, tag the commit of final accepted visuals.

---

## 11. Troubleshooting

| Issue                | Cause                                  | Fix                                                |
| -------------------- | -------------------------------------- | -------------------------------------------------- |
| Missing table `.tex` | Table saved before LaTeX feature added | Call `export_table_as_latex()`                     |
| Image too large      | Default width 0.85\textwidth           | Edit snippet or regenerate with smaller width      |
| Encoding problems    | Non-ASCII characters                   | Ensure UTF-8 and escape LaTeX specials             |
| Table too wide       | Many columns                           | Use `\resizebox{\textwidth}{!}{...}` or `tabularx` |

---

## 12. Future Enhancements (Optional)

- Automatic LaTeX list of figures/tables preamble generation
- Hash-based change detection & auto-version bump
- LaTeX glossary for variable descriptions
- Multi-panel figure composition utilities

---

## 13. Quick Command Summary

```
# Generate / refresh LaTeX snippets
default: python generate_latex_snippets.py

# Programmatically save a figure in notebook
assets.save_figure(fig, section='forecasting', name='ensemble_weight_evolution', description='Evolution of ensemble weights')

# Export an existing table to LaTeX (if missing)
assets.export_table_as_latex('model_evaluation','table2_model_performance','1.0')
```

---

**Use this file as a ready reference while composing the thesis document.**
