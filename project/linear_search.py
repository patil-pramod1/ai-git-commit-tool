def linear_search(arr, target):
    for index, element in enumerate(arr):
        if element == target:
            return index
    return -1