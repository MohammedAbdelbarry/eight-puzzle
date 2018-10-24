from typing import List


def is_sorted(l: List[int]) -> bool:
    """
    Checks if a list is sorted or not
    :param l: The list to be checked
    :return: a bool indicating whether the list is sorted or not
    """
    return all(a <= b for a, b in zip(l, l[1:]))
