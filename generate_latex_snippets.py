"""Generate LaTeX snippets for all registered thesis assets.

Outputs:
  thesis_images/latex/
    figures_<section>_<name>.tex   -> figure environments referencing image files
    table  .tex files already produced when saving tables (auto)
    index_figures.tex              -> consolidated include file
    index_tables.tex               -> consolidated include file
    master_assets_overview.tex     -> summary table of all assets

Run:
  python generate_latex_snippets.py
"""
from pathlib import Path
import json
from thesis_asset_manager import ThesisAssetManager

try:
    import pandas as pd
except Exception:
    pd = None

assets = ThesisAssetManager().ensure()
root = assets.root
latex_dir = root / 'latex'
latex_dir.mkdir(parents=True, exist_ok=True)

manifest = json.loads((root / 'manifests' / 'asset_manifest.json').read_text())

figure_snippet_paths = []

# Generate figure snippets
for rec in manifest:
    if rec['category'] != 'figure':
        continue
    img_path = root / rec['path']
    label = f"fig:{rec['section']}_{rec['name']}"
    caption = rec['description'] or f"{rec['name'].replace('_',' ').title()}"
    tex_filename = f"figure__{rec['section']}__{rec['name']}__{rec['version']}.tex"
    tex_path = latex_dir / tex_filename
    snippet = f"""% Auto-generated figure snippet
\\begin{{figure}}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{{{img_path.as_posix()}}}
  \caption{{{caption}}}
  \label{{{label}}}
\\end{{figure}}
"""
    tex_path.write_text(snippet)
    figure_snippet_paths.append(tex_path)

# Index for figures
index_fig = latex_dir / 'index_figures.tex'
index_fig.write_text("% Include this file to load all figure snippets (order can be adjusted)\n" + "\n".join([f"\\input{{{p.as_posix()}}}" for p in figure_snippet_paths]))

# Tables index (table .tex files created earlier if saved via manager)
tex_tables = sorted(latex_dir.glob('*.tex'))
tex_table_only = [p for p in tex_tables if p.name.startswith('model_') or p.name.startswith('policy_') or p.name.startswith('forecasting_') or p.name.startswith('general_') or p.name.startswith('causal_')]
index_tab = latex_dir / 'index_tables.tex'
index_tab.write_text("% Include this file to load all table snippets (curate order manually)\n" + "\n".join([f"\\input{{{p.as_posix()}}}" for p in tex_table_only]))

# Master overview (LaTeX tabular summarizing assets)
if pd is not None:
    import textwrap
    df = pd.DataFrame(manifest)
    overview_cols = ['category','section','name','version','filename','description']
    df_small = df[overview_cols].copy()
    df_small['description'] = df_small['description'].fillna("").str.slice(0,80)
    table_tex = df_small.to_latex(index=False, escape=True)
    overview_tex = f"""% Master asset overview
\\begin{{table}}[htbp]
  \centering
  \caption{{Master Asset Overview (truncated descriptions)}}
  \label{{tab:asset_overview}}
  {table_tex}
\\end{{table}}
"""
    (latex_dir / 'master_assets_overview.tex').write_text(overview_tex)

print("Generated LaTeX snippets:")
print(f"  Figures: {len(figure_snippet_paths)}")
print(f"  Index files: {index_fig.name}, {index_tab.name}")
