# Daily temperature forecasting at Bilbao Airport

Bachelor's thesis, Physics and Electronic Engineering double degree, UPV/EHU.

## Contents

- [Question](#question)
- [Data and setup](#data-and-setup)
- [Results](#results)
- [What the comparison shows](#what-the-comparison-shows)

## Question

How much better than a persistence forecast (tomorrow equals today) can learning models predict the daily mean temperature at Bilbao Airport, and which model family is the most reliable across horizons of 1, 3, 5 and 7 days?

## Data and setup

- Daily AEMET observations for 2014 to 2023.
- Seven input features: maximum and minimum temperature, mean relative humidity, mean wind speed, maximum and minimum pressure, plus a cyclic calendar encoding (sine and cosine of the day of year), over a five-day look-back window.
- Models: LSTM, Transformer, XGBoost and Random Forest, against the persistence baseline.
- Evaluation: time-series-aware 3-fold cross-validation repeated three times, so each model has nine evaluations and no future data leaks into training.
- Feature choices were checked with permutation importance, forward selection and ablation.

## Results

Mean absolute error in degrees Celsius.

| Model | 1 day | 3 days | 5 days | 7 days |
|---|---|---|---|---|
| LSTM | 1.633 | 2.435 | 2.512 | 2.562 |
| XGBoost | 1.690 | 2.390 | 2.516 | 2.561 |
| Transformer | 1.693 | 2.356 | 2.457 | 2.513 |
| Random Forest | 1.749 | 2.532 | 2.607 | 2.647 |
| Persistence | 1.814 | 2.862 | 3.180 | 3.329 |

## What the comparison shows

- Every learning model beats persistence, with an error 6 to 10 percent lower at one day and a wider margin at longer horizons.
- The LSTM is best at one day. The Transformer gives the best trade-off between accuracy and stability from three days on.
- XGBoost is the most stable across folds (lowest spread, 0.028 degrees).
- The calendar encoding matters a great deal, and a five-day window works better than longer ones.

Stack: Python, PyTorch, scikit-learn, XGBoost, Matplotlib. An earlier exploratory phase used MATLAB (random forest sweeps, a neural network, clustering).
