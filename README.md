# 🏅 olympoly

**Predictive Modeling meets Olympic Prediction Markets.**

`olympoly` is an open-source data analysis tool designed to identify discrepancies between historical Olympic performance and real-time sentiment on decentralized prediction markets like **PolyMarket**.

---

## 📊 Project Overview

The core objective of `olympoly` is to determine if historical data can "out-predict" public sentiment. By leveraging over a century of Olympic datasets and modern machine learning baselines, the tool flags instances where the market's implied probability (the odds) deviates significantly from statistical reality.

### Key Features
- **Time Series Analysis:** Analyze trends and changes in Olympic participation and medal outcomes over time.
- **Machine Learning:** Train models to estimate probabilities of Olympic outcomes.
- **Aggregation:** Convert athlete-level predictions into event-level estimates (e.g., by country).
- **Market Comparison:** Identify discrepancies between model probabilities and market-implied odds.
- **Simulation:** Evaluate betting strategies based on detected differences.

---

## ⚙️ Installation

To set up the environment and explore the analysis, clone the repository and install the package:

```bash
git clone https://github.com/caleb-adhikari/olympoly.git
cd olympoly
python -m pip install -e ".[dev]"
```

Requirements 
[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/)
---
``olympoly`` requires:

* ``python``, >=3.13
* ``datasets``, >=4.8.4
* ``numpy``, >=2.0
* ``pandas``, >=2.2
* ``seaborn``, >=0.13
* ``scikit-learn``, >=1.8.0

Optional requirements:

* ``pytest``
* ``jupyter``
* ``matplotlib``
* ``ruff``

---

## ▶️ Run the Demo

Run the demonstration of olympoly’s capabilities:

```python
from olympoly.demo import run_demo

run_demo()
```

This executes the complete pipeline, including:
- Data loading and cleaning
- Performance and timeline analysis
- Visualization of trends
- Predictive modeling
- Strategy simulation

---

## 🧪 Testing

Run the test suite:

```bash
pytest
```

Tests cover:
- Model training and feature engineering  
- Market vs model comparisons  
- Simulation strategies  
- Data validation  
- Visualization functions  

---