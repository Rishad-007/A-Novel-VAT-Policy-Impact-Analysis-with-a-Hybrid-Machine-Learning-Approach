# Hybrid Economic Policy Analysis

A comprehensive framework combining LSTM neural networks, Double Machine Learning, and Causal Forest methodologies for robust economic policy impact assessment.

## 📖 Overview

This project implements a novel hybrid approach to economic policy analysis by integrating three state-of-the-art machine learning methodologies:

- **LSTM Neural Networks** for macroeconomic time series forecasting
- **Double Machine Learning (DML)** for causal effect estimation
- **Causal Forest** for heterogeneous treatment effect analysis
- **Hybrid Ensemble** for integrated policy recommendations

The framework uses **real US economic data** from authoritative sources (FRED API, BLS, Business Dynamics Statistics) to analyze the causal impact of tax policy changes on firm survival rates.

## 🎯 Key Features

### ✅ **Data Integrity**
- **100% Real Data**: No synthetic or artificial data used anywhere
- **Verified Sources**: FRED API, Bureau of Labor Statistics, Business Dynamics Statistics
- **Reproducible**: All random seeds set to 42 for full reproducibility

### 🔬 **Advanced Methodology**
- **Multi-Model Integration**: Combines forecasting, causal inference, and heterogeneity analysis
- **Robust Causal Inference**: Uses Double ML with cross-fitting to eliminate confounding bias
- **Heterogeneous Effects**: Discovers how policy impacts vary across economic conditions
- **Ensemble Weighting**: Data-driven combination of model predictions

### 📊 **Publication-Ready Outputs**
- **5 Summary Tables**: Descriptive statistics, model performance, policy impacts
- **3 High-Quality Figures**: Model architecture, data overview, results visualization
- **Executive Summary**: Comprehensive analysis summary in JSON and text formats
- **Academic Standards**: All outputs formatted for thesis publication

## 🏗️ Project Structure

```
primary-thesis/
├── HybridEconomicPolicyAnalysis.ipynb    # Main analysis notebook
├── README.md                             # This file
├── database/                             # Raw economic data files
│   ├── bds2022.csv                      # Business Dynamics Statistics
│   ├── CPIAUCSL.csv                     # Consumer Price Index
│   ├── GDPC1.csv                        # Real GDP data
│   └── UNRATE.csv                       # Unemployment rate data
├── data/                                # Processed datasets
├── figures/                             # Generated visualizations
├── models/                              # Trained model artifacts
├── results/                             # Analysis results
└── exports/                             # Publication-ready outputs
    ├── table1_descriptive_statistics.csv
    ├── table2_model_performance.csv
    ├── table3_policy_impact_summary.csv
    ├── table4_economic_forecasts.csv
    ├── table5_detailed_model_comparison.csv
    ├── figure1_model_architecture.png
    ├── figure2_economic_data_overview.png
    ├── figure3_hybrid_model_results.png
    ├── executive_summary.txt
    ├── executive_summary.json
    └── results_package_manifest.json
```

## 🚀 Getting Started

### Prerequisites

```bash
# Core dependencies
pip install pandas numpy matplotlib seaborn
pip install tensorflow keras scikit-learn
pip install econml  # For causal inference
pip install fredapi  # For FRED data access
pip install requests beautifulsoup4  # For web scraping

# Jupyter environment
pip install jupyter ipykernel
```

### Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd primary-thesis
   ```

2. **Set up environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the analysis**
   ```bash
   jupyter notebook HybridEconomicPolicyAnalysis.ipynb
   ```

4. **Execute all cells** in order to reproduce the complete analysis

## 📋 Methodology Details

### 1. **Data Pipeline**
- **FRED API Integration**: Automatic download of macroeconomic indicators
- **BLS Data Processing**: Unemployment and labor statistics
- **Business Dynamics**: Firm-level survival and creation rates
- **Feature Engineering**: Economic regimes, volatility measures, policy indicators

### 2. **LSTM Forecasting**
- **Architecture**: Multi-layer LSTM with dropout regularization
- **Features**: GDP growth, unemployment, inflation, interest rates
- **Validation**: Time series cross-validation with walk-forward analysis
- **Output**: 5-year economic forecasts with uncertainty quantification

### 3. **Double Machine Learning**
- **Estimator**: LinearDML with cross-fitting
- **Treatment**: Tax policy changes (cuts vs. increases)
- **Outcome**: Firm survival rates
- **Confounders**: Macroeconomic controls
- **Result**: Unbiased average treatment effect estimation

### 4. **Causal Forest**
- **Model**: CausalForestDML for heterogeneous effects
- **Features**: Economic conditions, firm characteristics, policy timing
- **Analysis**: Individual treatment effect estimation
- **Insights**: Policy effectiveness varies by economic regime

### 5. **Hybrid Ensemble**
- **Weighting**: Performance-based ensemble weights
- **Integration**: Weighted combination of LSTM, DML, and Causal Forest
- **Scenarios**: Multiple policy simulation frameworks
- **Uncertainty**: Multi-source uncertainty quantification

## 📊 Key Results

### Model Performance
- **LSTM**: Captures temporal dependencies in economic data
- **Double ML**: Estimates average treatment effect with confidence intervals
- **Causal Forest**: Discovers heterogeneous policy impacts (98.5% ensemble weight)
- **Hybrid**: Robust policy recommendations with uncertainty quantification

### Policy Insights
- **Tax Cuts**: Generally positive impact on firm survival
- **Economic Regime**: Policy effectiveness varies by economic conditions
- **Heterogeneity**: Effects differ across firm sizes and economic stress levels
- **Forecasting**: 5-year projections with scenario analysis

## 🔬 Academic Contributions

### Methodological Innovation
1. **Multi-Model Integration**: Novel combination of forecasting and causal inference
2. **Real Data Validation**: Comprehensive analysis using only verified economic data
3. **Ensemble Methodology**: Data-driven weighting scheme for robust predictions
4. **Publication Standards**: Academic-quality outputs and reproducible research

### Policy Relevance
1. **Evidence-Based**: Quantitative assessment of tax policy effectiveness
2. **Heterogeneity**: Recognition that policy impacts vary across contexts
3. **Uncertainty**: Honest reporting of prediction confidence intervals
4. **Practical**: Actionable recommendations for policymakers

## 📈 Usage Examples

### Running Individual Components

```python
# Initialize data pipeline
data_pipeline = EconomicDataPipeline()
master_data = data_pipeline.create_master_dataset()

# Train LSTM forecaster
lstm_forecaster = LSTMForecaster()
lstm_model = lstm_forecaster.train_lstm_model(master_data)

# Run causal analysis
dml_analyzer = DoubleMachineLearning()
causal_effects = dml_analyzer.estimate_treatment_effects(master_data)

# Generate hybrid forecasts
hybrid_analyzer = HybridEconomicAnalyzer(lstm_forecaster, dml_analyzer, causal_forest_analyzer)
policy_scenarios = hybrid_analyzer.simulate_policy_scenarios(master_data)
```

### Export Results

```python
# Create publication package
pub_exporter = PublicationExporter(data_pipeline, lstm_forecaster, dml_analyzer, causal_forest_analyzer, hybrid_analyzer)
results_package = pub_exporter.export_all_results()
```

## 📝 Data Sources & Verification

### Primary Data Sources
- **Federal Reserve Economic Data (FRED)**: GDP, CPI, unemployment, interest rates
- **Bureau of Labor Statistics (BLS)**: Employment and labor force statistics  
- **Business Dynamics Statistics (BDS)**: Firm creation, destruction, and survival rates

### Data Verification
✅ **All data sources verified as real economic data**  
❌ **No synthetic or artificial data used anywhere in analysis**  
✅ **All data collection methods documented and reproducible**  
✅ **API keys and data access properly managed**

## 🔄 Reproducibility

### Complete Reproducibility
- **Random Seeds**: All set to 42 across all models
- **Version Control**: Complete Git history available
- **Environment**: Dependency versions locked
- **Documentation**: Comprehensive code comments and markdown

### Validation
- **Cross-Validation**: Time series appropriate validation methods
- **Robustness**: Multiple model specifications tested
- **Sensitivity**: Parameter sensitivity analysis conducted
- **Peer Review**: Code available for academic review

## 📚 References & Citations

### Methodological Papers
- Chernozhukov, V., et al. (2018). "Double/debiased machine learning for treatment and structural parameters"
- Wager, S., & Athey, S. (2018). "Estimation and inference of heterogeneous treatment effects using random forests"
- Hochreiter, S., & Schmidhuber, J. (1997). "Long short-term memory"

### Data Sources
- Federal Reserve Bank of St. Louis. Federal Reserve Economic Data (FRED)
- U.S. Bureau of Labor Statistics. Labor Force Statistics
- U.S. Census Bureau. Business Dynamics Statistics

## 👥 Contributing

This is an academic research project. For questions or collaboration inquiries, please contact the research team.

### Development Guidelines
1. **Data Integrity**: Maintain exclusive use of real economic data
2. **Reproducibility**: Ensure all changes maintain reproducibility
3. **Documentation**: Update documentation for any methodology changes
4. **Testing**: Validate changes against known results

## 📄 License

This project is developed for academic research purposes. Please cite appropriately if using this methodology in your research.

## 🔗 Contact

For questions about this research or potential collaborations, please reach out through the repository's issue tracker.

---

**Note**: This project represents cutting-edge research in economic policy analysis. All findings should be interpreted within the context of the methodological assumptions and data limitations discussed in the full academic paper.