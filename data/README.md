# 📂 data folder

this folder contains **sample datasets** for testing and demos in **RiskLab**

currently, it includes:

---

## `sample_portfolio.csv`

a realistic, **tech-heavy equity portfolio** with light diversification into banking and energy

designed to produce **meaningful risk insights** (volatility, correlations, stress tests) out of the box

```csv
Ticker,Allocation
AAPL,0.20
MSFT,0.20
TSLA,0.15
AMZN,0.15
GOOG,0.10
NVDA,0.10
JPM,0.05
XOM,0.05
```

## breakdown

- 80% tech --> apple, microsoft, teska, amazon, google, nvidia

- 20% diversification --> JPmorgan (banking), exxonmobil (energy)

this mix ensures:

   - volatility & correlation effects

   - scenario relevance (banking or oil shocks impact part of the portfolio)

   - non-trivial outputs from risk metrics and heatmaps


---

## portfolio schema

any custom portfolio you provide should follow the schema below:

| Column       | Type   | Description                                                                 | Example |
| ------------ | ------ | --------------------------------------------------------------------------- | ------- |
| `Ticker`     | string | Stock ticker symbol (compatible with Yahoo Finance)                         | `AAPL`  |
| `Allocation` | float  | Fraction of capital allocated (between 0 and 1). Must sum to **1.0** total  | `0.20`  |
| `AssetType`  | string | Category of asset (equity/bond/commodity)                                   | `equity`|

---

## rules

1. header row required ( Ticker , Aloocation, AssetType)

2. ticker format: must be recognized by yahoo finance (TSLA, GOOG, MSFT)

3. allocation values:
  
  - floats between 0 and 1

  - sum of all allocations must be equal to 1.0

4. keep portfolio size reasonable (5-50 assets recommanded for clarity)


---

## exemple output

Portfolio Summary:
------------------
Total Assets: 8
Top Holding: AAPL (20%)
Diversification: Moderate (Tech heavy)
Asset Type: Equity


---

## notes 

- keep datasets lightweight so they load quickly

- do NOT include sensitive or propritary data

- users are encouraged to replace sample_portfolio.csv with their own portfolios, following the schema above