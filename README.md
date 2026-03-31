# 🏅 olympoly

**Predictive Modeling meets Olympic Prediction Markets.**

`olympoly` is an open-source data analysis tool designed to identify discrepancies between historical Olympic performance and real-time sentiment on decentralized prediction markets like **PolyMarket**.

---

## 📊 Project Overview

The core objective of `olympoly` is to determine if historical data can "out-predict" public sentiment. By leveraging over a century of Olympic datasets and modern machine learning baselines, the tool flags instances where the market's implied probability (the odds) deviates significantly from statistical reality.

### Key Features

- **Historical Baseline Engine:** Processes 120+ years of Olympic data to establish athlete and nation-state performance benchmarks.
- **PolyMarket Integration:** Interfaces with the PolyMarket API to fetch live odds and market volume for upcoming events.
- **Edge Detection:** Automatically calculates "Expected Value" (EV) by comparing model-generated probabilities against market prices.
- **Data Pipelines:** Streamlined cleaning and normalization for heterogeneous sports data (track, pool, and field).

---

## ⚙️ Installation

To set up the environment and explore the analysis, clone the repository and install the package:

```bash
git clone https://github.com/caleb-adhikari/olympics_are_cool
cd olympics_are_cool
pip install .
```