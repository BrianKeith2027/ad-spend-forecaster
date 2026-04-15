# Ad Spend Monitor & Forecaster

An end-to-end advertising spend monitoring and forecasting platform that tracks historical campaign performance, forecasts spend and ROAS for the next 12 months, and recommends optimal budget allocation across channels using time series modeling and machine learning.

## Overview

Marketing teams need to justify every dollar of ad spend and forecast budgets accurately for financial planning. This project ingests historical advertising data across channels (Google Ads, Meta, LinkedIn, programmatic), builds time series forecast models, and delivers interactive dashboards showing spend trends, ROAS predictions, seasonal patterns, and optimal budget allocation recommendations.

**End Use:** Marketing analysts, media buyers, and finance teams use this platform to monitor current ad performance, forecast next-year budgets with confidence intervals, identify seasonal spend patterns, and optimize channel allocation through a Streamlit dashboard or programmatic API.

## Key Features

| Feature | Description |
|---------|-------------|
| **Multi-Channel Ingestion** | Unified data pipeline for Google Ads, Meta Ads, LinkedIn, and programmatic channels |
| **Spend Monitoring Dashboard** | Real-time KPI cards, trend lines, and anomaly alerts for ad spend |
| **Prophet Forecasting** | Facebook Prophet time series models with seasonality decomposition |
| **ARIMA Baseline** | Statistical ARIMA/SARIMA models for comparison and ensemble |
| **XGBoost Regression** | ML-based forecast using engineered features (lag, rolling, holiday) |
| **Model Comparison** | Automated backtesting with MAPE, RMSE, MAE across all models |
| **Budget Optimizer** | Constrained optimization recommending spend allocation by channel |
| **Anomaly Detection** | Flags unusual spend spikes/drops with configurable thresholds |
| **MLflow Tracking** | Full experiment tracking for all forecast models and parameters |

## Quick Start

```bash
pip install -r requirements.txt
python src/data/generate_ad_data.py
python src/models/train_forecasts.py
streamlit run src/app/dashboard.py
```

## Tech Stack

| Category | Technology |
|----------|-----------|
| Forecasting | Facebook Prophet, statsmodels (ARIMA/SARIMA), XGBoost |
| Optimization | SciPy (minimize with constraints) |
| Data Processing | Pandas, NumPy |
| Visualization | Plotly Express, Plotly Graph Objects |
| Dashboard | Streamlit |
| Experiment Tracking | MLflow |
| Anomaly Detection | SciPy (Z-score), IQR-based |
| Testing | pytest |
| Language | Python 3.10+ |

## End-Use Scenarios

| Scenario | Who Uses It | What They See |
|----------|-------------|---------------|
| Monthly Spend Review | Marketing Director | KPI dashboard with spend vs budget, ROAS trends |
| Annual Budget Planning | Finance Team | 12-month channel forecast with confidence intervals |
| Channel Optimization | Media Buyer | Budget reallocation recommendations by ROAS |
| Anomaly Investigation | Marketing Ops | Spend spike/drop alerts with root cause context |
| Executive Reporting | CMO / CFO | Exportable forecast summary for board presentations |

## Future Improvements

- Add real API connectors (Google Ads API, Meta Marketing API)
- - Implement Bayesian structural time series (CausalImpact)
  - - Add attribution modeling (multi-touch, Markov chain)
    - - Build automated weekly email reports
      - - Add Databricks/Spark support for large-scale historical data
       
        - ## Author
       
        - **Brian Stratton**
        - Senior Data Engineer | AI/ML Engineer | Doctoral Researcher
        - [LinkedIn](https://www.linkedin.com/in/briankstratton/) | [GitHub](https://github.com/BrianKeith2027)
       
        - ## License
       
        - This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
