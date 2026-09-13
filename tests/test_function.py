import unittest
import io
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


class TestFunction(unittest.TestCase):
    def _run_with_output(self, source: str) -> str:
        stdout = io.StringIO()
        tokens = Lexer(source).tokenize()
        program = Parser(tokens, source_code=source).parse()
        interp = Interpreter(source_code=source, stdout=stdout)
        interp.interpret(program)
        return stdout.getvalue()

    def test_simple_function_and_return(self):
        source = """
        이걸진짜만들었어요? add(e의2승 a, e의2승 b) {
            울산행KTX a + b;
        }

        e의2승 result = add(3, 5);
        오쫄티비(result);
        """
        output = self._run_with_output(source).strip()
        self.assertEqual(output, "8")

    def test_recursive_factorial(self):
        source = """
        이걸진짜만들었어요? factorial(e의2승 n) {
            왜요ㅗ (n <= 1) {
                울산행KTX 1;
            }
            울산행KTX n * factorial(n - 1);
        }

        오쫄티비(factorial(5));
        """
        output = self._run_with_output(source).strip()
        self.assertEqual(output, "120")

    def test_recursive_fibonacci(self):
        source = """
        이걸진짜만들었어요? fib(e의2승 n) {
            왜요ㅗ (n <= 0) {
                울산행KTX 0;
            }
            왜요ㅗ (n == 1) {
                울산행KTX 1;
            }
            울산행KTX fib(n - 1) + fib(n - 2);
        }

        오쫄티비(fib(10));
        """
        output = self._run_with_output(source).strip()
        self.assertEqual(output, "55")

    def test_hanoi_exact_output(self):
        """요구 명세 9번의 하노이탑 코드 및 예상 출력 완전 일치 검증"""
        source = """
        이걸진짜만들었어요? 하노이(e의2승 n, e의2승 시작, e의2승 중간, e의2승 끝) {
            왜요ㅗ (n == 1) {
                오쫄티비(시작, 끝);
                울산행KTX 남친;
            }

            하노이(n - 1, 시작, 끝, 중간);

            오쫄티비(시작, 끝);

            하노이(n - 1, 중간, 시작, 끝);
        }

        하노이(3, 1, 2, 3);
        """
        output = self._run_with_output(source).strip()
        expected = """1 3
1 2
3 2
1 3
2 1
2 3
1 3"""
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
