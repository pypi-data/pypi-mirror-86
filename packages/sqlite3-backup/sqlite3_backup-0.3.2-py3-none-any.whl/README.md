# README

`sqlite3` from the standard library does not support the backup
functionality provided by the original `sqlite3` C implementation.

This package fixes this by providing a simple backup function.

Typical use case is to write an in-memory sqlite3-db to disk.

This package uses the `ctypes` module and does not require a
working c compiler setup.
