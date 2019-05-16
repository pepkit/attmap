# Use cases and "how-to..."

## ...customize a subtype's text rendition
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
