import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from constant_test_cases import PUBLIC_TEST_CASES


def test_app():
    for test_case in PUBLIC_TEST_CASES:
        test_input = test_case.get("test_input")
        expected = test_case.get("expected")
        assert app(test_input) == expected
        print('cool')
