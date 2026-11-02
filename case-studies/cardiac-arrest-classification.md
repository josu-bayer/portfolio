# Telling two cardiac-arrest states apart from ECG and ballistocardiogram signals

Bachelor's thesis, Physics and Electronic Engineering double degree, UPV/EHU.

## Contents

- [Clinical problem](#clinical-problem)
- [Data](#data)
- [The validation problem](#the-validation-problem)
- [Results](#results)

## Clinical problem

During resuscitation, pulseless electrical activity (PEA) and perfusion with rhythm (PR) look the same on an ECG. A ballistocardiogram (BCG, a two-channel accelerometer) records the mechanical response of the heart and can separate them. The thesis compares machine-learning classifiers and validation strategies for this task.

## Data

- 157 signal segments from 6 patients, sampled at 250 Hz during CPR.
- 48 features from the ECG and both BCG channels, including spectral power, entropy measures and a cardiac component extracted from the BCG with an adaptive filter locked to the QRS rhythm.
- Classes are imbalanced, 77 percent PR against 23 percent PEA.
- The clinical recordings are not published. This page describes the method only.

## The validation problem

Every patient contributes segments of a single class. Leave-one-patient-out validation therefore leaves a test fold with one class only, and the area under the curve cannot be computed. The thesis replaces it with a patient-pair leave-out scheme, where each fold holds one PEA patient and one PR patient, so both classes are always present in the test set and the metrics are defined.

## Results

Across 11 model and imbalance-handling configurations under patient-pair leave-out, a class-balanced support vector machine generalised best:

- Recall for PEA 0.90 and AUC 0.805, with the smallest gap between training and test performance.
- BCG sample entropy was the strongest single feature (univariate AUROC 0.913).
- BCG features carried far more information than ECG features, and entropy measures more than morphology measures.

With six patients the confidence intervals are wide, and the thesis says so. External validation on more patients is the natural next step.

Stack: MATLAB for signal extraction, Python (scikit-learn) for modelling.
