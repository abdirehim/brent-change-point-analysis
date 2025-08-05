# Interim Report: Brent Oil Price Change Point Analysis

**Date:** 2025-08-05

**Author:** Gemini AI Agent

**Status:** Task 1 (Laying the Foundation for Analysis) Complete

---

## 1. Introduction

The primary objective of this analysis is to study how significant geopolitical and economic events affect Brent oil prices. By identifying statistically significant change points in the historical price data, we aim to associate these shifts with real-world events, providing clear, data-driven insights for investors, analysts, and policymakers.

This document outlines the completed foundational work and the planned steps for the subsequent modeling and analysis phases.

## 2. Data Analysis Workflow

The project will be executed in four distinct stages:

**Stage 1: Data Preparation and Exploration (Completed)**
- **Objective:** To load, clean, and understand the raw data.
- **Steps:**
  1. Loaded historical Brent oil price data from `data/raw/BrentOilPrices.csv`.
  2. Pre-processed the data by converting date formats, sorting chronologically, and handling missing values.
  3. Engineered key features for modeling: **log returns** to ensure stationarity and a **30-day rolling volatility** metric.
  4. Performed Exploratory Data Analysis (EDA), including visualizations and statistical tests (Augmented Dickey-Fuller), to confirm that the log-return series is stationary and suitable for modeling.
  5. Compiled and loaded a structured list of key historical events from `data/external/events.csv`.

**Stage 2: Bayesian Change Point Modeling (Next Steps)**
- **Objective:** To identify statistically significant structural breaks in the price data.
- **Steps:**
  1. **Model Specification:** Define a Bayesian change point model using the `PyMC3` library to detect multiple change points in the log-return series.
  2. **Model Fitting:** Employ Markov Chain Monte Carlo (MCMC) methods to fit the model to the data.
  3. **Model Diagnostics:** Use the `ArviZ` library to rigorously check for model convergence and ensure the reliability of the results.

**Stage 3: Analysis and Interpretation**
- **Objective:** To connect model outputs to real-world context.
- **Steps:**
  1. **Identify Change Points:** Analyze the model's output to determine the most probable dates of structural breaks.
  2. **Associate Changes with Events:** Compare the detected change points with the compiled list of historical events to formulate data-driven hypotheses about their potential causes.
  3. **Quantify Impact:** Measure the magnitude of the changes in price behavior (e.g., mean and volatility) around each identified change point.

**Stage 4: Communication of Results**
- **Objective:** To present the findings to stakeholders in an accessible format.
- **Steps:**
  1. **Interactive Dashboard:** The primary deliverable will be a web-based dashboard (Flask/React) that allows users to visualize the price series, change points, and associated events.
  2. **Final Report:** A comprehensive document will be created to summarize the project's methodology, key findings, and conclusions.

## 3. Assumptions and Limitations

- **Correlation vs. Causation:** It is critical to acknowledge that this analysis identifies **statistical correlations** in time. It does not and cannot prove that a specific event **caused** a price shift. The findings should be interpreted as strong, data-driven hypotheses.
- **Model Simplification:** The change point model is a simplification of the complex, multifaceted global oil market.
- **Event Selection:** The list of events, while curated, is not exhaustive. Other factors not included in the event list could have influenced the price.

---

## Appendix: Key Historical Events for Analysis

The following table contains the structured list of major geopolitical and economic events that will be used to provide context for the change points identified by the model.

| Date         | Event Description                           |
|--------------|---------------------------------------------|
| 1990-08-02   | Gulf War                                    |
| 1997-07-02   | Asian Financial Crisis                      |
| 2001-09-11   | 9/11 Attacks                                |
| 2002-12-02   | Venezuelan General Strike                   |
| 2003-03-20   | Invasion of Iraq                            |
| 2008-07-11   | Global Financial Crisis (Peak Oil Price)    |
| 2008-12-23   | Global Financial Crisis (Bottom Oil Price)  |
| 2011-01-14   | Arab Spring                                 |
| 2020-04-20   | COVID-19 Pandemic (Oil Price Crash)         |
| 2022-02-24   | Russian Invasion of Ukraine                 |
| 2023-10-07   | Israel-Hamas Conflict                       |

