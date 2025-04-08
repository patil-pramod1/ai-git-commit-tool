def binary_search(arr, target):
    """
    Performs binary search on a sorted list.

    :param arr: A sorted list of elements.
    :param target: The element to search for.
    :return: The index of target if found, otherwise -1.
    """
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

if __name__ == "__main__":
    # Example usage:
    sorted_list = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]
    target = 14
    index = binary_search(sorted_list, target)
    if index != -1:
        print(f"Target {target} found at index {index}.")
    else:
        print(f"Target {target} not found in the list.")