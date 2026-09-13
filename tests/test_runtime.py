import unittest
import io
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.errors import ConstAssignmentError, NameError, TypeError


class TestRuntime(unittest.TestCase):
    def _run(self, source: str) -> Interpreter:
        tokens = Lexer(source).tokenize()
        program = Parser(tokens, source_code=source).parse()
        interp = Interpreter(source_code=source)
        interp.interpret(program)
        return interp

    def test_variable_and_types(self):
        source = """
        e의2승 a = 42;
        울산큰고래 b = 10000000000;
        고래 c = 3.14;
        오? ch = 'Z';
        서울말 s = "서윤랭";
        아진짜ㅏ요 ok = 짘자;
        """
        interp = self._run(source)
        self.assertEqual(interp.global_env.get("a").val, 42)
        self.assertEqual(interp.global_env.get("b").val, 10000000000)
        self.assertEqual(interp.global_env.get("c").val, 3.14)
        self.assertEqual(interp.global_env.get("ch").val, "Z")
        self.assertEqual(interp.global_env.get("s").val, "서윤랭")
        self.assertEqual(interp.global_env.get("ok").val, True)

    def test_const_reassignment_raises_error(self):
        source = """
        당당해지세요. e의2승 MAX = 100;
        MAX = 200;
        """
        with self.assertRaises(ConstAssignmentError) as ctx:
            self._run(source)
        self.assertIn("상수 'MAX'에는 값을 재할당할 수 없습니다", str(ctx.exception))

    def test_block_scope_and_shadowing(self):
        source = """
        e의2승 x = 1;
        e의2승 shadowed = 10;
        {
            e의2승 y = 2;
            e의2승 shadowed = 20;
            x = 5;
        }
        """
        interp = self._run(source)
        self.assertEqual(interp.global_env.get("x").val, 5)
        self.assertEqual(interp.global_env.get("shadowed").val, 10)
        with self.assertRaises(NameError):
            interp.global_env.get("y")

    def test_type_mismatch_raises_error(self):
        source = """
        e의2승 x = 10;
        x = "문자열";
        """
        with self.assertRaises(TypeError):
            self._run(source)


if __name__ == "__main__":
    unittest.main()
