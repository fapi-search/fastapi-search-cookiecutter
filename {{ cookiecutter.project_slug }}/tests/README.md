# Organization

This project's tests are organized into data and unit tests. Data
tests validate features that interact with live databases and those
tests may inspect the results placed in the database. Data tests can
be more complex, time consuming, and should validate resulting data
state in addition to response.

Unit tests should not access databases and may use
[mocks](https://docs.python.org/3/library/unittest.mock.html) to
accomplished isolated tests without invoking database calls.
