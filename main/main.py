"""Code for the final project"""
import pprint
import display_data
from unemployment_calc_risk import probability_industry_and_demographics

"""Calculates risk for unemployment based on industry and person's age and gender"""


# Appropriate inputs (Type without quotation marks):
# industry in ['Accommodation and food services', 'Agriculture',
#                'Business and building and other support services', 'Construction', 'Educational services',
#                'Finance and insurance and real estate and rental and leasing', 'Goods-producing sector',
#                'Health care and social assistance', 'Information and culture and recreation', 'Manufacturing',
#                'Natural resources', 'Other services (except public administration)',
#                'Professional and scientific and technical services', 'Public administration',
#                'Services-producing sector', 'Transportation and warehousing', 'Utilities',
#                'Wholesale and retail trade']
#
# age_and_gender in ['youth Females', 'youth Males', 'young_adult Females', 'young_adult Males',
#                      'mid_adults Females', 'mid_adults Males']
#
# education in ['highschool', 'bachelor', 'above_ba']


industry = input('Enter an industry: ')
age_and_gender = input('Enter an age and gender: ')
education = input('Enter an education level: ')
pprint.pprint(probability_industry_and_demographics(industry, age_and_gender, education))


# Calls the display_data file to create bar graphs for data
display_data.display_industry()
display_data.display_age()
display_data.display_increase()
display_data.display_ed()

