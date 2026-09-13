import unittest
import os
import subprocess
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestExamples(unittest.TestCase):
    def _run_example(self, filename: str) -> str:
        filepath = os.path.join(PROJECT_ROOT, "examples", filename)
        result = subprocess.run(
            [sys.executable, os.path.join(PROJECT_ROOT, "main.py"), "run", filepath],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, f"Error running {filename}: {result.stderr}")
        return result.stdout.strip()

    def test_hello(self):
        out = self._run_example("hello.syl")
        self.assertIn("안녕하세요, 서윤랭입니다!", out)

    def test_if_else(self):
        out = self._run_example("if_else.syl")
        self.assertEqual(out, "B 등급")

    def test_loop(self):
        out = self._run_example("loop.syl")
        self.assertIn("6에서 탈출", out)

    def test_factorial(self):
        out = self._run_example("factorial.syl")
        self.assertIn("5 120", out)
        self.assertIn("6 720", out)

    def test_fibonacci(self):
        out = self._run_example("fibonacci.syl")
        self.assertIn("10 55", out)

    def test_hanoi(self):
        out = self._run_example("hanoi.syl")
        expected = """1 3
1 2
3 2
1 3
2 1
2 3
1 3"""
        self.assertEqual(out, expected)

    def test_array(self):
        out = self._run_example("array.syl")
        self.assertIn("board[1][0] 수정 후: 777", out)

    def test_list(self):
        out = self._run_example("list.syl")
        self.assertIn("999 포함 여부: 짘자", out)

    def test_stack(self):
        out = self._run_example("stack.syl")
        self.assertIn("최종 비어있음 여부: 짘자", out)


if __name__ == "__main__":
    unittest.main()
