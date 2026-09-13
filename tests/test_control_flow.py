import unittest
import io
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


class TestControlFlow(unittest.TestCase):
    def _run_with_output(self, source: str) -> str:
        stdout = io.StringIO()
        tokens = Lexer(source).tokenize()
        program = Parser(tokens, source_code=source).parse()
        interp = Interpreter(source_code=source, stdout=stdout)
        interp.interpret(program)
        return stdout.getvalue()

    def test_if_else_ladder(self):
        source = """
        e의2승 x = 7;
        왜요ㅗ (x > 10) {
            오쫄티비("10초과");
        } 실어요 왜요ㅗ (x > 5) {
            오쫄티비("5초과");
        } 실어요 {
            오쫄티비("5이하");
        }
        """
        output = self._run_with_output(source).strip()
        self.assertEqual(output, "5초과")

    def test_while_loop_with_break_and_continue(self):
        source = """
        e의2승 i = 0;
        e의2승 sum = 0;
        whale (i < 10) {
            i++;
            왜요ㅗ (i == 3) {
                꺼져ㅗ;
            }
            왜요ㅗ (i == 7) {
                말걸지마세요;
            }
            sum = sum + i;
        }
        오쫄티비(sum);
        """
        # i goes 1, 2, (3 skipped), 4, 5, 6, (7 breaks)
        # sum = 1 + 2 + 4 + 5 + 6 = 18
        output = self._run_with_output(source).strip()
        self.assertEqual(output, "18")

    def test_for_loop(self):
        source = """
        e의2승 total = 0;
        너므많아ㅡㅡㅅ (e의2승 i = 1; i <= 5; i++) {
            total = total + i;
        }
        오쫄티비(total);
        """
        output = self._run_with_output(source).strip()
        self.assertEqual(output, "15")


if __name__ == "__main__":
    unittest.main()
