# attmap

[![Run pytests](https://github.com/pepkit/attmap/actions/workflows/run-pytest.yml/badge.svg)](https://github.com/pepkit/attmap/actions/workflows/run-pytest.yml)

Key-value Mapping supporting nesting and attribute-style access.

**Note:** This package is no longer actively developed. Consider using plain dicts or dataclasses for new projects.

Originally designed for the [pepkit family projects](https://pepkit.github.io/).

## Install

```
pip install attmap
```

## Class hierarchy

- `AttMapLike` (abstract base)
    - `AttMap` — dict-backed mapping with dot notation access
        - `OrdAttMap` — insertion-ordered (extends `OrderedDict`)
            - `PathExAttMap` — expands environment variables in path-like string values
                - `EchoAttMap` — returns the key itself when a value is not set

## Customizing subclasses

### Excluding keys from text representation

Override `_excl_from_repr` in a subclass:

```python
def _excl_from_repr(self, k, cls):
    protected = ["reserved_metadata", "REZKEY"]
    return k in protected
```

### Excluding class name from repr

Override `__repr__` using the `exclude_class_list` argument to `_render`:

```python
def __repr__(self):
    return self._render(
        self._simplify_keyvalue(self._data_for_repr(), self._new_empty_basic_map),
        exclude_class_list="YacAttMap",
    )
```

### Excluding classes from `to_dict` conversion

Override `_excl_classes_from_todict`:

```python
def _excl_classes_from_todict(self):
    return (pandas.DataFrame, ClassToExclude)
```
