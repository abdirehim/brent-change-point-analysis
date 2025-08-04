# Bayesian Change Point Analysis References

This document contains key references for Bayesian change point analysis, time series modeling, and related methodologies used in this project.

## Core Bayesian Change Point Analysis

### Foundational Papers
1. **Barry, D., & Hartigan, J. A. (1993).** A Bayesian analysis for change point problems. *Journal of the American Statistical Association*, 88(421), 309-319.
   - Classic paper on Bayesian change point detection
   - Introduces the product partition model

2. **Chib, S. (1998).** Estimation and comparison of multiple change-point models. *Journal of Econometrics*, 86(2), 221-241.
   - Multiple change point detection using MCMC
   - Model comparison and selection

3. **Fearnhead, P. (2006).** Exact and efficient Bayesian inference for multiple changepoint problems. *Statistics and Computing*, 16(2), 203-213.
   - Efficient algorithms for multiple change points
   - Forward-backward algorithm implementation

### Recent Developments
4. **Adams, R. P., & MacKay, D. J. (2007).** Bayesian online changepoint detection. *arXiv preprint arXiv:0710.3742*.
   - Online change point detection
   - Real-time applications

5. **Hinkley, D. V. (1970).** Inference about the change-point in a sequence of random variables. *Biometrika*, 57(1), 1-17.
   - Classical change point inference
   - Likelihood-based approaches

## PyMC3 and Probabilistic Programming

### PyMC3 Documentation and Tutorials
6. **Salvatier, J., Wiecki, T. V., & Fonnesbeck, C. (2016).** Probabilistic programming in Python using PyMC3. *PeerJ Computer Science*, 2, e55.
   - Comprehensive PyMC3 tutorial
   - Best practices and examples

7. **Kruschke, J. K. (2014).** *Doing Bayesian data analysis: A tutorial with R, JAGS, and Stan*. Academic Press.
   - Bayesian analysis fundamentals
   - Model comparison and diagnostics

### ArviZ and Model Diagnostics
8. **Kumar, R., Carroll, C., Hartikainen, A., & Martin, O. A. (2019).** ArviZ a unified library for exploratory analysis of Bayesian models in Python. *The Journal of Open Source Software*, 4(33), 1143.
   - Model diagnostics and visualization
   - Convergence assessment

## Time Series Analysis

### Structural Breaks and Regime Changes
9. **Bai, J., & Perron, P. (2003).** Computation and analysis of multiple structural change models. *Journal of Applied Econometrics*, 18(1), 1-22.
   - Multiple structural breaks
   - Econometric applications

10. **Hamilton, J. D. (1989).** A new approach to the economic analysis of nonstationary time series and the business cycle. *Econometrica*, 57(2), 357-384.
    - Markov regime-switching models
    - Business cycle applications

### Oil Price Modeling
11. **Kilian, L. (2009).** Not all oil price shocks are alike: Disentangling demand and supply shocks in the crude oil market. *American Economic Review*, 99(3), 1053-1069.
    - Oil price shock identification
    - Supply and demand dynamics

12. **Hamilton, J. D. (2003).** What is an oil shock? *Journal of Econometrics*, 113(2), 363-398.
    - Oil price shock definitions
    - Economic impact analysis

## Event Study Methodology

### Event Impact Analysis
13. **MacKinlay, A. C. (1997).** Event studies in economics and finance. *Journal of Economic Literature*, 35(1), 13-39.
    - Event study methodology
    - Statistical testing procedures

14. **Binder, J. J. (1998).** The event study methodology since 1969. *Review of Quantitative Finance and Accounting*, 11(2), 111-137.
    - Event study evolution
    - Methodological improvements

### Geopolitical Events and Oil Markets
15. **Kilian, L., & Park, C. (2009).** The impact of oil price shocks on the US stock market. *International Economic Review*, 50(4), 1267-1287.
    - Oil price and stock market relationship
    - Event-based analysis

16. **Driesprong, G., Jacobsen, B., & Maat, B. (2008).** Striking oil: Another puzzle? *Journal of Financial Economics*, 89(2), 307-327.
    - Oil price predictability
    - Market efficiency

## Model Comparison and Selection

### Information Criteria
17. **Watanabe, S. (2010).** Asymptotic equivalence of Bayes cross validation and widely applicable information criterion in singular learning theory. *Journal of Machine Learning Research*, 11, 3571-3594.
    - WAIC derivation and properties
    - Model selection theory

18. **Vehtari, A., Gelman, A., & Gabry, J. (2017).** Practical Bayesian model evaluation using leave-one-out cross-validation and WAIC. *Statistics and Computing*, 27(5), 1413-1432.
    - WAIC implementation
    - Cross-validation comparison

### Bayesian Model Averaging
19. **Hoeting, J. A., Madigan, D., Raftery, A. E., & Volinsky, C. T. (1999).** Bayesian model averaging: a tutorial. *Statistical Science*, 14(4), 382-401.
    - Model averaging methodology
    - Uncertainty quantification

## Software and Implementation

### Python Libraries
20. **McKinney, W. (2010).** Data structures for statistical computing in Python. *Proceedings of the 9th Python in Science Conference*, 51-56.
    - Pandas documentation
    - Data manipulation

21. **Harris, C. R., Millman, K. J., van der Walt, S. J., et al. (2020).** Array programming with NumPy. *Nature*, 585(7825), 357-362.
    - NumPy documentation
    - Numerical computing

### Visualization
22. **Hunter, J. D. (2007).** Matplotlib: A 2D graphics environment. *Computing in Science & Engineering*, 9(3), 90-95.
    - Matplotlib documentation
    - Scientific plotting

23. **Waskom, M. L. (2021).** Seaborn: statistical data visualization. *Journal of Open Source Software*, 6(60), 3021.
    - Seaborn documentation
    - Statistical visualization

## Applications to Energy Markets

### Energy Economics
24. **Kilian, L., & Murphy, D. P. (2014).** The role of inventories and speculative trading in the global market for crude oil. *Journal of Applied Econometrics*, 29(3), 454-478.
    - Oil market dynamics
    - Inventory effects

25. **Baumeister, C., & Kilian, L. (2016).** Understanding the decline in the price of oil since June 2014. *Journal of the Association of Environmental and Resource Economists*, 3(1), 131-158.
    - Recent oil price dynamics
    - Supply-demand analysis

### Financial Applications
26. **Engle, R. F. (1982).** Autoregressive conditional heteroscedasticity with estimates of the variance of United Kingdom inflation. *Econometrica*, 50(4), 987-1007.
    - GARCH models
    - Volatility modeling

27. **Bollerslev, T. (1986).** Generalized autoregressive conditional heteroskedasticity. *Journal of Econometrics*, 31(3), 307-327.
    - GARCH extensions
    - Time-varying volatility

## Additional Resources

### Online Courses and Tutorials
- **Statistical Rethinking** by Richard McElreath
- **Bayesian Methods for Hackers** by Cameron Davidson-Pilon
- **PyMC3 Tutorials** on the official website

### Books
- **Bayesian Data Analysis** by Gelman et al.
- **Time Series Analysis** by Hamilton
- **Applied Econometric Time Series** by Enders

### Journals
- *Journal of the American Statistical Association*
- *Journal of Econometrics*
- *Journal of Applied Econometrics*
- *Energy Economics*
- *Journal of Financial Economics*

## Citation Format

When citing these references in your work, use the standard academic citation format appropriate for your field. For example:

```bibtex
@article{barry1993bayesian,
  title={A Bayesian analysis for change point problems},
  author={Barry, Daniel and Hartigan, J. A.},
  journal={Journal of the American Statistical Association},
  volume={88},
  number={421},
  pages={309--319},
  year={1993},
  publisher={Taylor \& Francis}
}
```

## Notes

- Keep this document updated as new relevant literature is published
- Focus on high-impact journals and well-cited papers
- Include both theoretical and applied contributions
- Consider the specific context of oil price analysis 