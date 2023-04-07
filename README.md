# Introducing Gaffe: Streamlined Exception Handling for Python

Are you tired of managing messy, unstructured exceptions in your Python projects? Gaffe is here to save the day! This elegant library offers a metaclass-based approach for highly extensible and easy-to-integrate custom exceptions, leading to better error handling and improved code readability.

## 🔥 Key Features

- 🎯 Simple, concise syntax for defining custom errors with optional subtypes
- 🧩 Clean integration through metaclass-based approach
- 🌳 Supports inheritance and composition of custom errors
- 🏗️ Automatic generation of error classes with custom attributes
- 🧮 Easy error comparison with the __eq__ method, supporting both class and instance comparisons
- 🕵️‍♂️ raises decorator to inspect and validate exceptions raised by functions or methods
- 🚀 Quick Installation

For pip enthusiasts:

```bash
pip install gaffe
```

For poetry aficionados:

```bash
poetry add gaffe
```

# 💡 Getting Started

To employ Gaffe's custom error system, import the Error class and create custom errors by inheriting from it:

```python
from gaffe import Error

class NotFoundError(Exception):
    ...

class MyError(Error):
    not_found: NotFoundError
    invalid_input: ...
    authentication_error = "authentication_error"
```
    
With this example, you'll get three custom errors under the MyError class, ready to be used just like any other Python exceptions.

## 🎩 Raises Decorator

Harness the power of the raises decorator to define and validate the types of exceptions a function or method can raise:

```python
from gaffe import raises

@raises(TypeError, ValueError)
def my_function(x: int, y: int) -> float:
    if x <= 0 or y <= 0:
        raise ValueError("x and y must be positive")
    return x / y
```

The raises decorator ensures that my_function can only raise TypeError and ValueError. If it tries to raise an unlisted exception, an AssertionError will be raised with a suitable error message.

## 🤖 Mypy Integration

To keep mypy happy, use the gaffe.mypy:plugin in your config file, and ensure that error properties are annotated with `Exception` type instead of `...`

```toml
[tool.mypy]
plugins = "gaffe.mypy:plugin"
```


Ready to revolutionize your Python exception handling? Get started with Gaffe today and check out the test scenarios for more examples!
