# dan.io package repository

## package rules

1. Packages must have a 'version' option.
2. Packages must handle the version option dynamically, ie.:
    - use property for url resolution
    - resolve actual version in `__initialize__` method
3. Packages must have at least one test, with no version restriction (the latest release will be tested in gh workflow).
