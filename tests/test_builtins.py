import unittest
import io
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


class TestBuiltins(unittest.TestCase):
    def _run_with_io(self, source: str, input_data: str = "") -> str:
        stdin = io.StringIO(input_data)
        stdout = io.StringIO()
        tokens = Lexer(source).tokenize()
        program = Parser(tokens, source_code=source).parse()
        interp = Interpreter(source_code=source, stdin=stdin, stdout=stdout)
        interp.interpret(program)
        return stdout.getvalue()

    def test_input_and_output(self):
        source = """
        e의2승 n = 게히야();
        서울말 s = 게히야();
        오쫄티비(n, s);
        """
        out = self._run_with_io(source, input_data="42\n서윤랭\n").strip()
        self.assertEqual(out, "42 서윤랭")

    def test_min_max_abs_len(self):
        source = """
        e의2승 a = -15;
        오쫄티비(abs(a));
        오쫄티비(min(10, 20), max(10, 20));

        사투링고 arr = [5, 2, 9, 1, 7];
        오쫄티비(min(arr), max(arr), len(arr));
        """
        lines = self._run_with_io(source).strip().splitlines()
        self.assertEqual(lines[0], "15")
        self.assertEqual(lines[1], "10 20")
        self.assertEqual(lines[2], "1 9 5")

    def test_sort_and_reverse(self):
        source = """
        사투링고 arr = [5, 1, 4, 2, 8];
        sort(arr);
        오쫄티비(arr[0], arr[1], arr[2], arr[3], arr[4]);
        reverse(arr);
        오쫄티비(arr[0], arr[1], arr[2], arr[3], arr[4]);
        """
        lines = self._run_with_io(source).strip().splitlines()
        self.assertEqual(lines[0], "1 2 4 5 8")
        self.assertEqual(lines[1], "8 5 4 2 1")

    def test_type_conversions(self):
        source = """
        e의2승 a = int("123");
        고래 b = float("3.14");
        서울말 c = string(456);
        오? d = char(65);
        오쫄티비(a, b, c, d);
        """
        out = self._run_with_io(source).strip()
        self.assertEqual(out, "123 3.14 456 A")

    def test_algorithm_split_and_sum(self):
        """백준 스타일: 공백으로 구분된 여러 정수 입력 받아 처리"""
        source = """
        서울말 line = 게히야();
        블루베리스무디레시피 tokens = split(line, " ");
        e의2승 sum = 0;
        너므많아ㅡㅡㅅ (e의2승 i = 0; i < len(tokens); i++) {
            sum = sum + int(tokens[i]);
        }
        오쫄티비(sum);
        """
        out = self._run_with_io(source, input_data="10 20 30 40\n").strip()
        self.assertEqual(out, "100")


if __name__ == "__main__":
    unittest.main()
