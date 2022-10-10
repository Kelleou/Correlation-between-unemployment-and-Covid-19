"""Display the data as bar graphs"""
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
import organize_data_age as od
import organize_data_education as oe

from organize_data_industry import load_data, industry_computation, conversion

youth = od.youth_data.loc[od.youth_data['Sex'] == 'Both sexes']
index = [i for i in youth['REF_DATE']]


def display_age() -> None:
    """Graph how age affects unemployment"""

    youth_unemployment = [i for i in youth['VALUE']]
    young_adults = od.young_adults_data.loc[od.young_adults_data['Sex'] == 'Both sexes']
    young_adults_unemployment = [i for i in young_adults['VALUE']]
    mid_adults = od.mid_adults_data.loc[od.mid_adults_data['Sex'] == 'Both sexes']
    mid_adults_unemployment = [i for i in mid_adults['VALUE']]
    age_data = pd.DataFrame({'15-24 y/o': youth_unemployment, '25-44 y/o': young_adults_unemployment,
                             '45-64 y/o': mid_adults_unemployment}, index=index)
    age_data.plot.bar(rot=0)
    plt.xticks(fontsize=6)
    plt.show()


def display_ed() -> None:
    """Graph how education affect unemployment"""
    hs_unemployment = [i for i in oe.highschool_data['VALUE']]
    ba_unemployment = [i for i in oe.bachelor_data['VALUE']]
    aba_unemployment = [i for i in oe.above_bachelor_data['VALUE']]
    education_data = pd.DataFrame({'highschool': hs_unemployment, 'bachelor': ba_unemployment,
                                   'above bachelor': aba_unemployment}, index=index)
    education_data.plot.bar(rot=0)
    plt.xticks(fontsize=6)
    plt.show()


def display_increase() -> None:
    """Graph the increase in unemployment for each factor"""
    hs_rate = oe.highschool.increase_factor
    ba_rate = oe.bachelor.increase_factor
    aba_rate = oe.above_ba.increase_factor
    youth_rate = od.youth.increase_factor['Both sexes']
    young_adult_rate = od.young_adults.increase_factor['Both sexes']
    mid_adult_rate = od.mid_adults.increase_factor['Both sexes']
    female_rate = od.female.increase_factor
    male_rate = od.male.increase_factor

    rates = pd.DataFrame({'rates': [hs_rate, ba_rate, aba_rate, youth_rate, young_adult_rate, mid_adult_rate,
                                    female_rate, male_rate]},
                         index=['highschool', 'bachelors', 'above bachelors', 'youth', 'young adult',
                                'midage adults', 'female', 'male']
                         )
    rates.plot.bar(rot=0)
    plt.xticks(fontsize=6)
    plt.show()


# Display graph for industry factor

def display_industry() -> None:

    # A python dictionary
    data = conversion(industry_computation(load_data('industry_edited.csv')))

    index = ['Goods sector', 'Agriculture', 'Natural resources', 'Utilities', 'Construction', 'Manufacturing',
             'Services sector', 'Wholesale & retail trade', 'Transportation & warehousing',
             'Finance & real estate ',
             'Professional & technical services', 'Business & building',
             'Educational services', 'Health care & social assistance', 'Information & recreation',
             'Accommodation and food services', 'Other services', 'Public administration']

    # Dictionary loaded into a DataFrame

    dataframe = pd.DataFrame(data=data, index=index)

    # Draw a vertical bar chart

    dataframe.plot.bar(rot=15, title='Unemployment vs. Industry in Canada', figsize=(15, 10))

    plt.show(block=True)
