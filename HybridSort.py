"""
Your Name:
Project 2 - Hybrid Sorting - Solution Code
CSE 331 Fall 2021
Professor Sebnem Onsay
"""
import random
from typing import TypeVar, List, Callable, Tuple, Dict
import copy

T = TypeVar("T")  # represents generic type


def merge_sort(data: List[T], threshold: int = 0,
               comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> int:
    """
    This function conducts a merge sort on a given list
    if a threshold is given, it is executed until that
    threshold  is met
    inputs:
    data: a list to sort
    threshold: a threshold value to meet
    comparator: user defined comparison function
    returns: the count of inversions
    """
    inv = 0
    length = len(data)
    if len(data) <= threshold:
        insertion_sort(data, comparator)
    elif len(data) > 1:
        mid = length // 2
        s_one = data[0:mid]
        s_two = data[mid:length]
        inv += merge_sort(s_one, threshold, comparator)
        inv += merge_sort(s_two, threshold, comparator)
        i = j = 0
        temp = 0
        while i < len(s_one) and j < len(s_two):
            if comparator(s_one[i], s_two[j]):
                data[temp] = s_one[i]
                i = i + 1
            else:
                data[temp] = s_two[j]
                inv += len(s_one) - i
                j = j + 1
            temp += 1
        while i < len(s_one):
            data[temp] = s_one[i]
            i += 1
            temp += 1
        while j < len(s_two):
            data[temp] = s_two[j]
            j += 1
            temp += 1
    return inv


def insertion_sort(data: List[T], comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> None:
    """
    This function sorts a given set of data using the
    insertion method
    inputs:
    data: a list to sort
    comparator: user defined comparison function
    returns: nothing
    """
    length = len(data)
    for i in range(length):
        j = i
        while j > 0 and comparator(data[j], data[j - 1]):
            data[j], data[j - 1] = data[j - 1], data[j]
            j -= 1


def hybrid_sort(data: List[T], threshold: int,
                comparator: Callable[[T, T], bool] = lambda x, y: x <= y) -> None:
    """
    A wrapper function for merge sort
    inputs:
    data: a list to sort
    comparator: user defined comparison function
    returns: nothing
    """
    merge_sort(data, threshold, comparator)


def inversions_count(data: List[T]) -> int:
    """
    counts the inversions of a copy of the data
    inputs:
    data: a list to count
    returns: inversion count
    """
    data_cpy = copy.deepcopy(data)
    inv = merge_sort(data_cpy)
    return inv


def reverse_sort(data: List[T], threshold: int) -> None:
    """
    INSERT DOCSTRING HERE
    """
    merge_sort(data, threshold, comparator=lambda x, y: x >= y)
    return


# forward reference
Ship = TypeVar('Ship')


# DO NOT MODIFY BELOW
class Ship:
    """
    A class representation of a ship
    """

    __slots__ = ['name', 'x', 'y']

    def __init__(self, name: str, x: int, y: int) -> None:
        """
        Constructs a ship object
        :param name: name of the ship
        :param x: x coordinate of the ship
        :param y: y coordinate of the ship
        """
        self.x, self.y = x, y
        self.name = name

    def __str__(self):
        """
        :return: string representation of the ship
        """
        return "Ship: " + self.name + " x=" + str(self.x) + " y=" + str(self.y)

    __repr__ = __str__

    def __eq__(self, other):
        """
        :return: bool if two ships are equivalent
        """
        return self.x == other.x and self.y == other.y and self.name == other.name

    def __hash__(self):
        """
        Allows Ship to be used as a key in a dictionary (pretty cool, right?)
        :return: hash of string representation of the ship
        """
        return hash(str(self))

    def euclidean_distance(self, other: Ship) -> float:
        """
        returns the euclidean distance between `self` and `other`
        :return: float
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** .5

    def taxicab_distance(self, other: Ship) -> float:
        """
        returns the taxicab distance between `self` and `other`
        :return: float
        """
        return abs(self.x - other.x) + abs(self.y - other.y)


# MODIFY BELOW
def navigation_test(ships: Dict[Ship, List[Ship]], euclidean: bool = True) -> List[Ship]:
    """
    This function sorts a list of ships by its given
    inversion count
    inputs:
    ships: a dictionary of ship and sonar results
    euclidean: a bool to indicate what distance formula to use
    returns:
    sorted list of ships by inversion count
    """
    res_list = []

    for key in ships:
        work_list = []
        if euclidean:
            for ship in ships[key]:
                work_list.append(key.euclidean_distance(ship))
        else:
            for ship in ships[key]:
                work_list.append(key.taxicab_distance(ship))
        inv = inversions_count(work_list)
        res_list.append((key, inv))

    hybrid_sort(res_list, threshold=0,
                comparator=lambda x, y: x[1] <= y[1] if x[1] != y[1] else x[0].name <= y[0].name)
    return [item[0] for item in res_list]