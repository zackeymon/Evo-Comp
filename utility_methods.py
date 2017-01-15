import numpy as np


def get_taste_average(taste_list):
    """Get average taste of a list of tastes (%360) using polar co-ordinates."""
    rad_taste_list = np.radians(taste_list)
    x_average = np.average(np.cos(rad_taste_list))
    y_average = np.average(np.sin(rad_taste_list))

    average = np.arctan2(y_average, x_average) * 180 / np.pi

    return int(average % 360)


def get_taste_difference(taste1, taste2):
    return abs((taste1 - taste2 + 180) % 360 - 180)


def sum_list_energy(organism_list):
    return sum(organism.energy for organism in organism_list)


def average_lifetime(organism_list):
    """organism_list[turn][organism_index]"""
    total_number = sum([len(i) for i in organism_list])
    if total_number == 0:
        return 0

    total_lifetime = sum([sum([i.lifetime for i in turn]) for turn in organism_list])

    return total_lifetime / total_number


def average_rep_thresh(organism_list):
    """organism_list[turn][organism_index]"""
    total_number = sum([len(i) for i in organism_list])
    if total_number == 0:
        return 0

    total_rep_thresh = sum([sum([i.reproduction_threshold for i in turn]) for turn in organism_list])

    return total_rep_thresh / total_number


def split_list(data):
    """Split the overall list of data into separate days."""
    split_data = [[]]
    for item in data:
        if "'end_day'" in item:
            split_data.append([])
        else:
            split_data[-1].append(item)

    del split_data[-1]
    data = split_data

    return data
