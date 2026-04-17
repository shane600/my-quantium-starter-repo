#!/bin/bash

# activate the virtual enviroment
source venv/Scripts/activate

# run the test suite
venv/Scripts/pytest.exe

# pass pytests exit code back, 0 for pass 1 for fail
exit $?
