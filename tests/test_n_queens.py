# Copyright 2020 D-Wave Systems Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import unittest
from subprocess import Popen, PIPE ,STDOUT

from dimod import ExactSolver
from neal import SimulatedAnnealingSampler

from n_queens import *

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# def run_integration_test():
#     """Only run integration tests on Linux and with Python 3.9."""
#     print(os.environ.get('DWAVE_LOG_LEVEL', "Nothing"))
#     if sys.version_info.major == 3 and sys.version_info.minor == 9 and sys.platform == 'linux':
#         return True
#     else:
#         return False

class TestNQueens(unittest.TestCase):
    @unittest.skipIf(os.getenv('SKIP_INT_TESTS'), "Only run integration tests w/ latest supported Python, on Linux.")
    def test_smoke(self):
        # check that nothing crashes
        print("inside test_smoke")

        demo_file = os.path.join(project_dir, 'n_queens.py')
        p = Popen([sys.executable, demo_file],
                  stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        p.stdin.write(b'4')

        output = p.communicate()[0]
        output = str(output).upper()

        # check that solution is valid
        with self.subTest(msg="Verify if output contains 'Solution is valid.' \n"):
            self.assertIn("Solution is valid.".upper(), output)

        # check that solution image was saved
        image_name = '4-queens-solution.png'
        self.assertTrue(os.path.isfile(image_name))
        os.remove(image_name)

    def test_4_queens(self):
        sampler = ExactSolver()

        n = 4
        solution = n_queens(n, sampler)
        self.assertTrue(is_valid_solution(n, solution))

    def test_10_queens(self):
        sampler = SimulatedAnnealingSampler()
        n = 10

        tries = 0
        valid = False

        while not valid and tries < 3:
            solution = n_queens(n, sampler)
            valid = is_valid_solution(n, solution)
            tries += 1

        self.assertTrue(valid)

if __name__ == '__main__':
    unittest.main()