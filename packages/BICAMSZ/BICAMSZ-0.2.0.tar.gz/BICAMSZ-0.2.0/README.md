# BICAMSZ: a package for z-transformation of BICAMS

## Table of contents
1. [About the creators](#aims---vub)
2. [Project explanation](#the-project)
3. [Considerations](#important-considerations)
4. [Deliverables](#deliverables)
5. [Required Data](#required-data)
5. [Code explanation](#code-explanation)

## Introduction

### AIMS - VUB

First of all, thank you very much for your interest in using our project on behalf of the Artificial Intelligence and Modelling in clinical Sciences (AIMS) lab, part of the Vrije Universiteit Brussel (VUB). We aim to contribute maximally to optimal clinical care in neurodegenerative disorders, with a special focus on Multiple Sclerosis, by performing relevant and advanced modelling on neurophysiological and brain imaging data. Moreover, in light of the prosper of the field and general understanding of our research, we do efforts to contribute to open, reproducible and transparant science by sharing code and actively practicing science communication on our [AIMS website](https://aims.research.vub.be).

### The project
This project is based on [Costers et al. 2017](https://www.msard-journal.com/article/S2211-0348(17)30202-X/fulltext). \
To understand the transformation, please visit our [streamlit application](https://share.streamlit.io/sdniss/bicams_web_application/BICAMS_application.py)!

In short, transforming test scores to z-scores by correcting for age, sex and education allows comparison of cognitive scores between subjects. The following phases can be distinguished:
1. Scaling of the raw scores
2. Predicting which score should normally be obtained by the subject according to their age, sex and education level. 
3. Obtain z-score: subtract the predicted score (2) from the scaled score (1), and divide by the residual error of the regression model

### Important considerations

Both the conversion table per test, used for the scaling of raw scores, and the fitting of the regression-line to yield the weights for the features within the regression model (age, age^2, sex, education level) rely on data from a sample of 97 Belgian, Dutch-speaking healthy controls. The demographics of this population (especially age and education, 43.52 ± 12.69 and 14.69 ± 1.61 (mean ± std) respectively) should be taken into account when converting a z-score for a subject. We highlight to be especially careful when calculating z-scores when a participant's characteristics have extreme values (either very low or very high) on either age or education level. 

Furthermore, testing conditions for this paper were very strict. E.g. for the SDMT, patients were not allowed to keep track of their progression on the test paper by using their fingers to indicate the symbol that needed to be converted into a digit. Please make sure that every subtest of BICAMS was administered with careful attention for correct execution. Moreover, only the Dutch version of CVLT-II is eligible for the z-normalization within this project.

## Deliverables

With this code, you can easily transform cognitive scores on BICAMS to z-scores.

## Required data
The following data is an absolute requirement:
- age: years (integer)
- sex: 
    - 1 = Male
    - 2 = Female
- education (years of education): 
    - 6 = Primary school
    - 12 = High school 
    - 13 = Professional education 
    - 15 = Bachelor 
    - 17 = Master 
    - 21 = Doctorate

Furthermore, data on at least 1 of the 3 scores below is required:
- sdmt: raw sdmt score
- bvmt: raw bvmt score
- cvlt: raw cvlt score

## Code explanation
All code is present in `functions.py`
- `data_check`: performs a check on your data for impossible values, including NaNs. If problems are still present, the code will automatically throw warnings and return NaNs.
- `normalization_pipeline`: entire pipeline. Uses the following internal functions:
    - `_check_impossible_values_or_nans`
    - `_get_conversion_table`: more info below
    - `_get_expected_score`
    - `_raw_to_scaled`
    - `_to_z_score`
    - `_impaired_or_not`
- `pipeline_for_pandas`: this allows the pipeline to be applied to a pandas dataframe with the `.apply()` function. Please use the following code snippets: 
    1. `new_columns = ['z_test', 'imp_test']`: replace 'test' with the test you are converting
    2. `input_columns = ['column_name_age', 'column_name_sex', 'column_name_edu', 'column_name_test']`: Adapt the names according to your columnnames.
    3. `df[new_columns] = df[input_columns].apply(pipeline_for_pandas, args = (test, z_cutoff), axis = 1)`: replace `test` with the string 'sdmt', 'bvmt' or 'cvlt'. Also choose the cut-off.
     
To load the three main functions: `from BICAMSZ import normalization_pipeline, data_check, pipeline_for_pandas` \
For info on these functions: please use `help(...function...)` to see the docstrings.

Additional note on conversion tables, used by `_get_conversion_table`: \
Every conversion table consists of the following columns:
- scaled_score: Categorical variable, the scaled score that accords with a raw score within the following interval between lower and upper bound:
- lower bound: lower bound of the raw score to yield a certain scaled score
- upper bound: upper bound of the raw score to yield a certain scaled score

Thus: scaled_score accords with lower_bound <= raw_score <= upper_bound \
Note: Also 'equal to' belongs to the interval between the lower and upper bounds!
