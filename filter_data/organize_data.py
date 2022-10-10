"""Data computations for the project"""
import pandas as pd
from dataclasses import dataclass
import csv
import pprint
from organize_data_age import youth, young_adults, mid_adults
from organize_data_education import highschool, bachelor, above_ba


@dataclass
class Industry:
    """This class represents the attributes for the industry factor"""

    province: str
    industry: str
    july_2021: float
    aug_2021: float
    july_to_aug_2021: float
    aug_2020_to_aug_2021: float


def load_data(filename: str) -> list[list[Industry]]:
    data_so_far = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        for row in reader:
            data_so_far.append([Industry(row[0], row[1], float(row[2]), float(row[3]), float(row[5]), float(row[6]))])

    return data_so_far


def industry_computation(data: list[list[Industry]]) -> dict[str, list[float]]:
    dict_so_far = {}
    l_so_far = [0.0] * 4
    for i in range(len(data)):
        if data[i][0].industry not in dict_so_far:
            l_so_far[0] = data[i][0].july_2021
            l_so_far[1] = data[i][0].aug_2021
            l_so_far[2] = data[i][0].july_to_aug_2021
            l_so_far[3] = data[i][0].aug_2020_to_aug_2021
            dict_so_far[data[i][0].industry] = l_so_far
            l_so_far = [0.0] * 4
        else:
            dict_so_far[data[i][0].industry][0] += data[i][0].july_2021
            dict_so_far[data[i][0].industry][1] += data[i][0].aug_2021
            dict_so_far[data[i][0].industry][2] += data[i][0].july_to_aug_2021
            dict_so_far[data[i][0].industry][3] += data[i][0].aug_2020_to_aug_2021
    return dict_so_far


def simplified_data() -> list[list]:
    """Returns a list of lists that pair variables to their increase in unemployment"""
    industry_data = [[x[0].industry, x[0].aug_2020_to_aug_2021]
                     for x in load_data('industry_edited.csv')]
    province_data = [[x[0].province, x[0].aug_2020_to_aug_2021]
                     for x in load_data('industry_edited.csv')]

    youth_data_f = [['youth Females', youth.increase_factor['Females']]]
    youth_data_m = [['youth Males', youth.increase_factor['Males']]]
    young_adult_f = [['young_adult Females', young_adults.increase_factor['Females']]]
    young_adult_m = [['young_adult Males', young_adults.increase_factor['Males']]]
    mid_adult_f = [['mid_adults Females', mid_adults.increase_factor['Females']]]
    mid_adult_m = [['mid_adults Males', mid_adults.increase_factor['Males']]]

    highschool_all = [['highschool', highschool.increase_factor]]
    bachelor_all = [['bachelor', bachelor.increase_factor]]
    above_ba_all = [['above_ba', above_ba.increase_factor]]

    return industry_data + province_data + youth_data_f + youth_data_m + young_adult_f + \
        young_adult_m + mid_adult_f + mid_adult_m + highschool_all + bachelor_all + above_ba_all


def average_duplicates(data: list[list]) -> list[list]:
    """Returns a list of lists that pair variables to the average increase in unemployment without duplicates"""
    new_list = []
    duplicates = []
    data_copy = data.copy()
    for list in data_copy:
        if list[0] not in [x[0] for x in new_list]:
            new_list.append(list)
        else:
            duplicates.append(list)

    sorted_duplicates = sorted(duplicates)
    for i in range(len(sorted_duplicates) - 1):
        if sorted_duplicates[i][0] != '':
            count = 1
            index = 1
            while i + index <= len(sorted_duplicates) - 1:
                if sorted_duplicates[i][0] == sorted_duplicates[i + index][0]:
                    sorted_duplicates[i][1] += sorted_duplicates[i + index][1]
                    sorted_duplicates[i + index][0] = ''
                    count += 1
                    index += 1
                else:
                    break

            for list in new_list:
                if list[0] == sorted_duplicates[i][0]:
                    list[1] = (list[1] + sorted_duplicates[i][1]) / (count + 1)

    return new_list

