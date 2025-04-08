### 📝 Description
In this PR, I added two new search algorithms, binary search and linear search, to improve our data retrieval capabilities. These implementations will allow our users to choose the most efficient search method based on their data characteristics. 

### 📁 Files Changed
- **`project/binary_search.py`**: This file contains the implementation of the binary search algorithm, which is efficient for sorted datasets.
- **`project/linear_search.py`**: This file includes the linear search algorithm, suitable for unsorted datasets or when performance is not a critical factor.

### 🛠️ Impact Areas
The addition of these search algorithms impacts the following functionalities:
- **Searching Mechanisms**: Users can now utilize both binary and linear search methods, enhancing the flexibility and effectiveness of our search functionalities.
- **Performance Optimization**: The binary search implementation is expected to significantly improve search performance on sorted data, making it a valuable addition for users dealing with large datasets.

### ✅ Summary of Changes
- **Added Binary Search**: Introduced an efficient binary search algorithm in `binary_search.py`, which operates in O(log n) time complexity for sorted lists.
- **Added Linear Search**: Implemented a straightforward linear search algorithm in `linear_search.py`, which operates in O(n) time complexity, providing a fallback option for unsorted data.
- **Enhanced Search Capabilities**: These additions provide users with more tools to optimize their data retrieval processes, improving overall application performance and usability.