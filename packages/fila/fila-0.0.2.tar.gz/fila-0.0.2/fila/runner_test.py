# -*- coding:utf-8 -*-

import unittest

from fila.runner import OK, run


class TestRunner(unittest.TestCase):

    def test_run(self):
        self.assertEqual(OK, run())


if __name__ == '__main__':
    unittest.main()
