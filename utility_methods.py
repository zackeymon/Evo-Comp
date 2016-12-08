import numpy as np


def get_taste_average(taste_list):
    """Get average taste of a list of tastes (%360) using polar co-ordinates."""
    x = []
    y = []
    for taste in taste_list:
        taste_rad = np.radians(taste)
        x.append(np.cos(taste_rad))
        y.append(np.sin(taste_rad))

    x_average = np.sum(x) / len(x)
    y_average = np.sum(y) / len(y)

    average = np.arctan2(y_average, x_average) * 180 / np.pi
    if average < 0:
        average += 360

    return average


def sum_list_energy(organism_list):
    energy = 0

    for organism in organism_list:
        energy += organism.energy

    return energy


def average_lifetime(organism_list):
    """organism_list[turn][organism_index]"""
    total_number = sum([len(i) for i in organism_list])
    if total_number == 0:
        return 0

    total_lifetime = sum([sum([i.lifetime for i in turn]) for turn in organism_list])

    return total_lifetime / total_number


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

