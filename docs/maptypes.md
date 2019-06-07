# Attmap class inheritance hierarchy

Attmap is organized into a series of related objects with slightly different behavior. This document shows the class relationships. Classes underneath others in this tree indicate parent-child relationships of the classes.

- [`AttMapLike`](autodoc_build/attmap.md#AttMapLike) (abstract)
    - [`AttMap`](autodoc_build/attmap.md#AttMap)
        - [`OrdAttMap`](autodoc_build/attmap.md#OrdAttMap)
            - [`PathExAttMap`](autodoc_build/attmap.md#PathExAttMap)
                - [`EchoAttMap`](autodoc_build/attmap.md#EchoAttMap)
