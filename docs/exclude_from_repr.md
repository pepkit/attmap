# Use cases and "how-to..."

## How to customize a subtype's text rendition
In a subclass, override `_excl_from_repr`, using key and/or type of value.

The most basic implementation is a no-op, excluding nothing:
```python
def _excl_from_repr(self, k, cls):
    return False
```

To exclude by key, though, you can do something like:
```python
def _excl_from_repr(self, k, cls):
    protected = ["reserved_metadata", "REZKEY"]
    return k in protected
```

To exclude by value type, you can use something like:
```python
def _excl_from_repr(self, k, cls):
    return issubclass(cls, BaseOmissionType)
```
where `BaseOmissionType` is a proxy for the name of some type of values that may
be stored in your mapping but that you prefer to not display in its text representation.

The two kinds of exclusion criteria may be combined as desired.
Note that it's often advisable to invoke the superclass version of the method,
but to achieve the intended effect this may be skipped.


## How to exclude the object type from a text rendition

Starting in `0.12.9`, you can override the `__repr__` with to use the new `_render` arg, `exclude_class_list`:

```python
def __repr__(self):
    # Here we want to render the data in a nice way; and we want to indicate
    # the class if it's NOT a YacAttMap. If it is a YacAttMap we just want
    # to give you the data without the class name.
    return self._render(self._simplify_keyvalue(
        self._data_for_repr(), self._new_empty_basic_map),
        exclude_class_list="YacAttMap")
```

## How to exclude classes from `to_dict` conversion

Starting in `0.13.1`, you can specify a collection of classes that will be skipped in the conversion of the object to `dict`.

```python
def _excl_classes_from_todict(self):
    return (pandas.DataFrame, ClassToExclude,)
```
