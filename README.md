# Gaffe
Simple structured exceptions for python. 

Gaffe relies on metaclass-based approach to be highly extensible and pluggable into any existing project, promoting better error handling and improved code readability.


# Features

- Simple and concise syntax for defining custom errors with optional subtypes
- Clean integration through metaclass-based approach
- Supports inheritance and composition of custom errors
- Automatic generation of error classes with custom attributes
- Easy comparison of errors using the __eq__ method, supporting both class and instance comparisons.

# Installation

With pip:
`pip install gaffe`

or poetry:

`poetry add gaffe`

# Usage

To use this custom error system, simply import the Error class and define your custom errors by inheriting from it:

```python
from gaffe import Error

class NotFoundError(Exception):
    ...

class MyError(Error):
    not_found: NotFoundError
    invalid_input: ...
    authentication_error = "authentication_error"
```

This creates three custom errors under the MyError class:
- `MyError.not_found` which extends also `NotFoundError`
- `MyError.invalid_input` the simplest definition of an error without additional subtype
- `MyError.authentication_error` an error with a custom value assigned to it

These custom errors can be used just like any other Python exceptions:

```python
from gaffe import Error

class NotFoundError(Exception):
    ...

class NetworkError(Error):
    timeout = "Request timed out"
    connection_error: ...

class HTTPError(NetworkError):
    bad_request: ...
    not_found: NotFoundError
```

This creates a hierarchy of custom errors with NetworkError as the base class and HTTPError as a subclass with additional HTTP-specific errors.

You can handle `HTTPError.timeout` as follows:

```python
try:
    raise HTTPError.timeout
except NetworkError as e:
    print(e)

try:
    raise HTTPError.timeout
except HTTPError as e:
    print(e)

try:
    raise HTTPError.timeout
except HTTPError.timeout as e:
    print(e)
```

You can handle `HTTPError.not_found` as follows:

```python
try:
    raise HTTPError.not_found
except HTTPError as e:
    print(e)

try:
    raise HTTPError.not_found
except HTTPError as e:
    print(e)

try:
    raise HTTPError.not_found
except NotFoundError as e:
    print(e)
```

# Integration with mypy

To fix mypy complains about the code you can use `gaffe.mypy:plugin` in your config file, like below:

```toml
[tool.mypy]
plugins = "gaffe.mypy:plugin"
```

That's all folks!

For more examples please [check the test scenarios](./tests/test_error.py).
