"""Code for the industry factor"""
import pandas as pd
import matplotlib.pyplot as plot
from dataclasses import dataclass
import csv


@dataclass
class Industry:
    """This class represents the attributes for the industry factor
    Attributes:
        - province: province in Canada
        - industry: the type of industry in Canada
        - july_2021: the floating number represents the unemployed in thousands
        - aug_2021: the floating number represents the unemployed in thousands
        - july_to_aug_2021: change in thousands from july to aug 2021
        - aug_2020_to_aug_2021: change in thousands from aug 2020 to aug 2021

    Representation Invariants:
      - self.province != ''
      - self.industry != ''
      - self.july_2021 >= 0
      - self.aug_2021 >= 0
    """

    province: str
    industry: str
    july_2021: float
    aug_2021: float
    july_to_aug_2021: float
    aug_2020_to_aug_2021: float


def load_data(filename: str) -> list[list[Industry]]:
    """Returns a nested list with the inner lists corresponding to Industry.
    There are 7 columns with 6 columns used.
    """
    data_so_far = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)

        for row in reader:
            data_so_far.append([Industry(row[0], row[1], float(row[2]), float(row[3]), float(row[5]), float(row[6]))])

    return data_so_far


def industry_computation(data: list[list[Industry]]) -> dict[str, list[float]]:
    """Takes in the nested list of Industry as input and returns the dictionary with the key
    as the industry (18 keys total) and the value comprised of a list of 4 elements corresponding to Jul 2021, Aug 2021,
    July to Aug 2021 and Aug 2020 to Aug 2021.
    """
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


def conversion(d: dict[str, list[float]]) -> dict[str, list[float]]:
    """Converts the dictionary of industries to a dictionary where the keys are
    July 2021, Aug 2021, Jul to Aug 2021 and Aug 2020 to Aug 2021. The values are
    a list corresponding to each industry.
    This format is needed to graph the industry results.
    """
    dict_so_far = {'Jul 2021 (thsnds)': [], 'Aug 2021 (thsnds)': [], 'Jul to Aug 2021 (change in thsnds)': [],
                   'Aug 2020 to Aug 2021 (change in thsnds)': []}
    for ind in d:
        dict_so_far['Jul 2021 (thsnds)'].append(d[ind][0])
        dict_so_far['Aug 2021 (thsnds)'].append(d[ind][1])
        dict_so_far['Jul to Aug 2021 (change in thsnds)'].append(d[ind][2])
        dict_so_far['Aug 2020 to Aug 2021 (change in thsnds)'].append(d[ind][3])
    return dict_so_far


if __name__ == '__main__':
    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
