# Changelog

## [0.13.2] - 2021-11-04
### Fixed
- Made compatibile with setuptools 58 by removing use_2to3

## [0.13.1] - 2021-11-04
### Added
- `_excl_classes_from_todict`, which can be used to list classes to be excluded from the `dict` representation

### Fixed
- A bug that caused double-backslashes

## [0.13.0] - 2021-02-22
### Added
- block style YAML representation support for lists
- recursive value expansion in `PathExAttMap`

## [0.12.11] - 2019-11-01
### Added
- distribute license with the package

## [0.12.10] - 2019-10-31
### Added
- license file

## [0.12.9] - 2019-07-30
### Added
- New feature to allow not printing the object type on reprs.

## [0.12.8] - 2019-07-30
### Fixed
- Bug with setting values via attribute-style setters.

## [0.12.7] - 2019-06-25
### Added
- Hook for calling value finalization in signature for `OrdAttMap`'s `__setitem__` implementation

## [0.12.6] - 2019-06-24
### Added
- Hook in value storage finalization for use of the key, not just the value

## [0.12.5] - 2019-06-06
### Changed
- By default, represent empty `Mapping` value as `null` in YAML rendition.
### Fixed
- Expand paths (in `PathExAttMap`) for text values stored and fetched with attribute` syntax or `.get`.

## [0.12.4] - 2019-05-30
### Fixed
- Avoid infinite recursion when an `EchoAttMap` subtype calls up to the superclass constructor: [Issue 55](https://github.com/pepkit/attmap/issues/55).

## [0.12.3] - 2019-05-18
### Changed
- `PathExAttMap` now decleares itself as lower type bound.

## [0.12.2] - 2019-05-18
### Fixed
- Tweaked map type conversion upon value insertion

## [0.12.1] - 2019-05-17
### Added
- `EchoAttMap` as alias for `AttMapEcho`; see [Issue 38](https://github.com/pepkit/attmap/issues/38)
### Fixed
- In any `OrdAttMap, for membership (`__contains__`) consider items added via attribute syntax.
- Prevent duplicate key/attr iteration in any `OrdAttMap`.
- Allow item and attribute syntax to equivalently mutate a map; see [Issue 50](https://github.com/pepkit/attmap/issues/50)
- Type conversion and merger of inserted mappings

## [0.12] - 2019-05-16
### Added
- Export base `AttMapLike`.
### Changed
- By default, add trailing newline to YAML rendition of an attmap instance; [Issue 48](https://github.com/pepkit/attmap/issues/48)
- Better API docs
### Fixed
- Do not replace double slash in URL with single slash. See [Issue 46](https://github.com/pepkit/attmap/issues/46)

## [0.11] - 2019-05-16
### Added
- `get_yaml_lines` to get collection of YAML-ready lines from any attmap
- `to_dict` to convert any attmap (and nested maps) to base `dict`
- `to_yaml` to represent any attmap as raw YAML text
### Changed
- `PathExAttMap` defers expansion behavior to retrieval time.

## [0.10] - 2019-05-15
### Fixed
- `OrdAttMap` and descendants now have data updated via `__setattr__` syntax.

## [0.9] - 2019-05-14
### Changed
- `OrdPathAttExAttMap` is now `PathExAttMap`.

## [0.8] - 2019-05-13
### Added
- `OrdAttMap` to create maps that preserve insertion order and otherwise behave like ordinary `AttMap`
- `get_data_lines` utility, supporting nice instance `repr`
- `is_custom_map` utility
### Changed
- Better `repr` and `str` for all `attmap`-like types, rendering like YAML
- `__getitem__` syntax on `AttMapEcho` no longer exhibits echo behavior (only dot notation does.)
- Instance comparison is now much stricter, requiring exact type match. This reflects some of the type-specific value conversion and representation behavior.
- `PathExAttMap` is now `OrdPathExAttMap`, preserving item insertion order
- `AttMapEcho` preserves item insertion order

## [0.7] - 2019-04-24
### Changed
- Removed `pandas` dependency
- Made hooks for omission of specific keys instance methods

## [0.6] - 2019-04-11
### Added
- Hook for omission of key(s) from instance comparison
- Documentation

## [0.5] - 2019-03-27
### Added
- Add `to_map` method to convert `Mapping` values to basic type

## [0.4] - 2019-03-19
### Changed
- What was `PepAttMap` is now `PathExAttMap`.

## [0.3] - 2019-03-19
### Added
- `PepAttMap` attempts expansion of text value as a path, using available environment variables
### Changed
- `AttMap` now derives from `PepAttMap` rather than ordinary `AttMap`

## [0.2] - 2019-03-04
### Changed
- `AttMapEcho` now converts an inserted `Mapping` to `AttMapEcho` -- no more specific type than that.
- Handle equivalence comparison when values are array-likes from `numpy` or `pandas`

## [0.1.8] - 2019-02-06
### Fixed
- Installation working for dependent packages

## [0.1.7] - 2019-02-05
### Changed
- Make `__version__` available on the main package object

##  [0.1.6] - 2019-02-05
### Changed
- Bound on most specific type to which a stored `Mapping` should be converted can be controlled in a subclass via overriding.

## [0.1.5] - 2019-02-05
### Changed
- `add_entries` method on an `AttMapLike` now returns the instance.
- Improve test coverage

## [0.1.4] - 2019-02-05
### Changed
- Removed support for Python 3.4

## [0.1.3] - 2019-02-05
### Fixed
- Pass unit tests on Python 3.4

## [0.1.2] - 2019-02-04
### Fixed
- Correct PyPI landing page rendering

## [0.1.1] - 2019-02-04
### Fixed
- Correct PyPI landing page rendering

## [0.1] - 2019-02-04
### New
- Initial release
