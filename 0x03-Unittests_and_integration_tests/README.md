# Unit Testing with Python's `unittest`

This project demonstrates unit testing in Python using the `unittest` framework, focusing on testing the `access_nested_map` function from a utilities module.

## Overview

The project contains:

- `utils.py`: Module with utility functions including `access_nested_map`
- `test_utils.py`: Test file containing unit tests
- This `README.md`: Documentation

## Function Under Test

### `access_nested_map(nested_map: Mapping, path: Sequence) -> Any`

Accesses a value in a nested dictionary using a sequence of keys.

**Parameters:**

- `nested_map`: A nested dictionary structure
- `path`: Sequence of keys representing the path to the value

**Returns:**

- The value found at the specified path

**Example:**

```python
access_nested_map({"a": {"b": 1}}, ("a", "b"))  # Returns 1
```
