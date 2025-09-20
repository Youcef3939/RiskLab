# examples

this folder contains hands-on demos for **RiskLab**, designed to show how the toolkit works step by step

---

## 📂 contents

- **`example_notebook.ipynb`** → interactive Jupyter notebook demonstrating:  

  1. loading a portfolio (`sample_portfolio.csv`)

  2. calculating core risk metrics (VaR, CVaR, volatility)

  3. generating a likelihood × impact **risk matrix**

  4. running simple stress tests

  5. visualizing results with plots  

- **`README.md`** → this guide  

---

## quick start

1. open the notebook in Jupyter or VS Code: 

```bash

jupyter notebook examples/example_notebook.ipynb
```

2. follow the cells step by step to explore RiskLab's features

3. swap in your own portfolio by changing the path in the first cell

---

## the workflow

portfolio --> risk metrics --> risk matrix --> visualization --> dashboard

this notebook serves as a full end to end demo so you can experiment with metrics, visualizations and risk scenarios without touching the core code


---

## example output

Portfolio Summary:
------------------
Total Assets: 8
Top Holding: AAPL (20%)
Diversification: Moderate (Tech heavy)

{'VaR_95': -0.032, 'CVaR_95': -0.045}