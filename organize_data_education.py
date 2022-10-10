"""Education data computations for the project"""
import pandas as pd
from dataclasses import dataclass

# data is a DataFrame object
data = pd.read_csv('education.csv')
# store all the factors we want to investigate in the table
factors = ["REF_DATE", "Educational attainment", "VALUE"]
# find the column of data that corresponds to the factor we want to look at
filtered_data = data[factors]
# filter data
highschool_data = filtered_data.loc[filtered_data['Educational attainment'] == 'High school graduate']
bachelor_data = filtered_data.loc[filtered_data['Educational attainment'] == 'Bachelor\'s degree']
above_bachelor_data = filtered_data.loc[filtered_data['Educational attainment'] == 'Above bachelor\'s degree']


@dataclass
class EducationGroup:
    """A class that stores the unemployment numbers and the factor unemployment increased by"""
    pre_covid: float
    covid: float
    increase_factor: float


# calculate the average unemployment before and during covid
def calculate_pre_covid(education: pd.DataFrame) -> float:
    """calculate the average unemployment rate the year before covid"""
    lst = [i for i in education['VALUE']]
    unemployment = 0
    for i in range(12):
        unemployment += lst[i]
    return unemployment / 12


def calculate_covid(education: pd.DataFrame) -> float:
    """calculate the average unemployment rate during covid"""
    lst = [i for i in education['VALUE']]
    unemployment = 0
    for i in range(12, 25):
        unemployment += lst[i]
    return unemployment / 12


# Calculate the factor in which unemployment numbers increased by
def calculate_increase_rate(pre_covid: float, covid: float) -> float:
    """return the rate of increase in unemployment"""
    return covid / pre_covid


# Create a class object to calculate and store the unemployment info for each age group
highschool = EducationGroup(calculate_pre_covid(highschool_data), calculate_covid(highschool_data),
                            calculate_increase_rate(calculate_pre_covid(highschool_data),
                                                    calculate_covid(highschool_data)))
bachelor = EducationGroup(calculate_pre_covid(bachelor_data), calculate_covid(bachelor_data),
                          calculate_increase_rate(calculate_pre_covid(bachelor_data),
                                                  calculate_covid(bachelor_data)))
above_ba = EducationGroup(calculate_pre_covid(above_bachelor_data), calculate_covid(above_bachelor_data),
                          calculate_increase_rate(calculate_pre_covid(above_bachelor_data),
                                                  calculate_covid(above_bachelor_data)))
