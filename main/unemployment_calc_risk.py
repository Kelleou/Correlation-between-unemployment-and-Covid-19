"""Calculates risk for unemployment based on industry and person's age and gender"""
import pprint
from organize_data import simplified_data, average_duplicates


def probability_industry_and_demographics(industry: str, age_and_gender: str, education: str) -> str:
    """Return string explaining probability that a person will become unemployed using the unemployment increase between
      age and gender during pandemic

      Preconditions:
        - industry in ['Accommodation and food services', 'Agriculture',
              'Business and building and other support services', 'Construction', 'Educational services',
              'Finance and insurance and real estate and rental and leasing', 'Goods-producing sector',
              'Health care and social assistance', 'Information and culture and recreation', 'Manufacturing',
              'Natural resources', 'Other services (except public administration)',
              'Professional and scientific and technical services', 'Public administration',
              'Services-producing sector', 'Transportation and warehousing', 'Utilities',
              'Wholesale and retail trade']

        - age_and_gender in ['youth Females', 'youth Males', 'young_adult Females', 'young_adult Males',
              'mid_adults Females', 'mid_adults Males']

        - education in ['highschool', 'bachelor', 'above_ba']


    >>> pprint.pprint(probability_industry_and_demographics('Utilities', 'youth Males', 'highschool'))
    ('The average increase in unemployment due to covid in the Utilities industry '
     'was 11.000000000000005%. Because you are in the group of youth Males with an '
     'education level of highschool, your risk increase would have been '
     'approximately 11.05490042571027% instead. In other words, you would be about '
     '0.1105490042571027 times more likely to be unemployed during covid compared '
     'to normal years')
    >>> pprint.pprint(probability_industry_and_demographics('Utilities', 'youth Females', 'highschool'))
    ('The average increase in unemployment due to covid in the Utilities industry '
     'was 11.000000000000005%. Because you are in the group of youth Females with '
     'an education level of highschool, your risk increase would have been '
     'approximately 12.271669988297393% instead. In other words, you would be '
     'about 0.12271669988297393 times more likely to be unemployed during covid '
     'compared to normal years')
    >>> pprint.pprint(probability_industry_and_demographics('Natural resources', 'mid_adults Males', 'above_ba'))
    ('The average increase in unemployment due to covid in the Natural resources '
     'industry was 227.99999999999997%. Because you are in the group of mid_adults '
     'Males with an education level of above_ba, your risk increase would have '
     'been approximately 203.33018299832605% instead. In other words, you would be '
     'about 2.0333018299832606 times more likely to be unemployed during covid '
     'compared to normal years')
    """

    dict = get_dict()
    starting_risk = dict[industry] * 100

    new_risk = starting_risk * (1 + (get_percent_increase_or_decrease(age_and_gender) / 100)) \
        * (1 + get_percent_increase_or_decrease(education) / 100)

    return "The average increase in unemployment due to covid in the " + industry + " industry was " \
           + str(starting_risk) + "%. Because you are in the group of " + age_and_gender \
           + " with an education level of " + education + \
           ", your risk increase would have been approximately " + str(new_risk) + \
           '% instead. In other words, you would be about ' + str(new_risk/100) + \
           ' times more likely to be unemployed during covid compared to normal years'


def get_dict() -> dict:
    """Get a dictionary mapping variables to their unemployment increase during pandemic"""
    lists = average_duplicates(simplified_data())

    variable_dict = {}
    for list in lists:
        variable_dict[list[0]] = list[1]
    return variable_dict


def get_percent_increase_or_decrease(age_and_gender_or_education) -> float:
    """Get percentage increase or decrease for unemployment risk using age and gender

    Preconditions:
        - age_and_gender_or_education in ['mid_adults Females', 'mid_adults Males', 'young_adult Females',
         'young_adult Males', 'youth Females', 'youth Males'] or ['highschool', 'bachelors', 'above_ba']

    >>> get_percent_increase_or_decrease('bachelor')
    4.716045689073855
    >>> get_percent_increase_or_decrease('above_ba')
    -6.100543094959356  # Meaning its less likely for people with above a bachelors to be unemployed
    >>> get_percent_increase_or_decrease('youth Males')
    -0.8733116495677226
    >>> get_percent_increase_or_decrease('youth Females')
    10.037174431731923
    """
    dict = get_dict()
    categories1 = ['mid_adults Females', 'mid_adults Males', 'young_adult Females', 'young_adult Males',
                   'youth Females', 'youth Males']
    categories2 = ['highschool', 'bachelor', 'above_ba']

    if age_and_gender_or_education in categories1:
        average_increase = sum(dict[x] for x in categories1) / len(categories1)

    else:
        average_increase = sum(dict[x] for x in categories2) / len(categories2)

    if dict[age_and_gender_or_education] > average_increase:
        percent_increase = ((dict[age_and_gender_or_education] - average_increase) / average_increase) * 100
    elif dict[age_and_gender_or_education] < average_increase:
        percent_increase = - ((average_increase - dict[age_and_gender_or_education]) / average_increase) * 100
    else:
        percent_increase = 0

    return percent_increase



