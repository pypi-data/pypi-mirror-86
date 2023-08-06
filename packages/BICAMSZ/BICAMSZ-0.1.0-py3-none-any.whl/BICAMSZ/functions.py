import numpy as np
import pandas as pd


def data_check(array, key):
    """ Function that checks the value of an array for impossible values

    :param array: the array (column) you want to check
    :param key: str, the feature name of the array. Choose from ['age', 'sex', 'education', 'sdmt', 'bvmt', 'cvlt']
    :return: error if a problem is encountered, or prints a message when considered valid
    """
    error_dict = {'columns': 'Please be sure to use the correct column names and that they are lower case',
                  'age': 'Please use age values between 0 and 125 years, and only use integer values',
                  'sex': 'Please assure the following encoding: Male = 1, Female = 2',
                  'education': 'Please use education levels that are encoded as 6, 12, 13, 15, 17 or 21 years',
                  'sdmt': 'Please use sdmt values between 0 and 110',
                  'bvmt': 'Please use bvmt values between 0 and 36',
                  'cvlt': 'Please use cvlt values between 0 and 80'}

    allowed_range_dict = {'age': set(range(0, 126)),
                          'sex': {1, 2},
                          'education': {6, 12, 13, 15, 17, 21},
                          'sdmt': set(range(0, 111)),
                          'bvmt': set(range(0, 37)),
                          'cvlt': set(range(0, 81))}

    input_set = set(array)
    comparison_set = allowed_range_dict.get(key)

    # Check whether the values of input_set are within the allowed values (comparison_set)
    if not input_set.issubset(comparison_set):
        raise ValueError(error_dict.get(key))

    print('No errors. Ready for conversion! :)')


def normalization_pipeline(age, sex, edu, raw_score, test, z_cutoff):
    """ Entire normalization pipeline

    :param age: age in years
    :param sex: Male = 1, Female = 2
    :param edu: amount of years education (Choose from 6, 12, 13, 15, 17, 21)
    :param raw_score: int, raw score on the test of interest
    :param test: str, choose from 'sdmt', 'bvmt' or 'cvlt'
    :param z_cutoff: float, the value where you want to declare impairment on the cognitive domain
    :returns: z_score: z-score for the test of interest -- impaired_bool: 1 if impaired, 0 if preserved
    """

    # Additional required preparations
    age_2 = age**2
    data_vector = [age, age_2, sex, edu]
    conversion_table = _get_conversion_table(test)

    # The pipeline: from raw score to z-score and impairment boolean
    expected_score = _get_expected_score(data_vector, test)
    scaled_score = _raw_to_scaled(raw_score, conversion_table)
    z_score = _to_z_score(scaled_score, expected_score, test)
    impaired_bool = _impaired_or_not(z_score, z_cutoff)

    return z_score, impaired_bool


def _get_conversion_table(test):
    """ Get conversion table that corresponds with the test of interest

    :param test: str, choose from 'sdmt', 'bvmt' or 'cvlt'
    :return: dict, conversion table
    """
    # Read relevant files
    sdmt_ct = pd.read_csv('BICAMSZ/conversion_tables/sdmt_conversion_table.csv')
    bvmt_ct = pd.read_csv('BICAMSZ/conversion_tables/bvmt_conversion_table.csv')
    cvlt_ct = pd.read_csv('BICAMSZ/conversion_tables/cvlt_conversion_table.csv')

    # Dictionary with the tests and the according conversion tables
    conversion_dict = {'sdmt': sdmt_ct,
                       'bvmt': bvmt_ct,
                       'cvlt': cvlt_ct}

    # Get conversion table from test
    return conversion_dict.get(test)


def _get_expected_score(data_vector, test):
    """ Get the expected score on a subtest of the BICAMS

    :param data_vector: 1-D vector consisting in following order: [age, age^2, sex, education]
    :param test: str, choose from 'sdmt', 'bvmt' or 'cvlt'
    :return: the expected score on the respective test
    """
    weight_dict = {'sdmt': [10.648, -0.289, 0.002, -0.05, 0.479],
                   'cvlt': [9.052, -0.230, 0.002, 2.182, 0.323],
                   'bvmt': [16.902, -0.473, 0.005, -1.427, 0.341]}

    weight_vector = weight_dict.get(test)
    data_vector = [1] + list(data_vector)  # Add 1 to multiply with bias term in regression equation
    expected_score = np.dot(weight_vector, data_vector)

    return expected_score


def _raw_to_scaled(raw_score, conversion_table):
    """ Convert raw score to a categorical, scaled value

    :param raw_score: int, raw score on the test of interest
    :param conversion_table: pd dataframe, being the conversion table for the test of interest
    :return: categorical, scaled score
    """

    scaled_scores = conversion_table.iloc[:,0]
    lower_values = conversion_table.iloc[:,1]
    upper_values = conversion_table.iloc[:,2]

    for scaled_score, lower_value, upper_value in zip(scaled_scores, lower_values, upper_values):
        if lower_value <= raw_score <= upper_value:
            return scaled_score


def _to_z_score(scaled_score, expected_score, test):
    """ Turn scaled and expected score to a z score

    :param scaled_score: scaled score, result from raw_to_scaled function
    :param expected_score: expected score, result from get_expected_score function
    :param test: test of interest
    :return: z-score for the test of interest
    """
    denominator_dict = {'sdmt': 2.790,
                        'bvmt': 2.793,
                        'cvlt': 2.801}

    denominator = denominator_dict.get(test)

    z_score = (scaled_score - expected_score)/denominator

    return z_score


def _impaired_or_not(z_score, cutoff):
    """ Dichotimize z-score by applying a cutoff

    :param z_score: the z-score, i.e. performance relative to a reference population
    :param cutoff: the cut-off to decide impaired (<=) or preserved (>) on the cognitive domain
    :return: 1 if impaired, 0 if preserved
    """
    if z_score <= cutoff:
        return 1
    else:
        return 0
