import unittest
import io
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


class TestClass(unittest.TestCase):
    def _run_with_output(self, source: str) -> str:
        stdout = io.StringIO()
        tokens = Lexer(source).tokenize()
        program = Parser(tokens, source_code=source).parse()
        interp = Interpreter(source_code=source, stdout=stdout)
        interp.interpret(program)
        return stdout.getvalue()

    def test_class_declaration_and_instantiation(self):
        source = """
        1학년2반 Person {
            서울말 name;
            e의2승 age;

            이걸진짜만들었어요? info() {
                오쫄티비(name, age);
            }
        }

        Person p = Person();
        p.name = "서윤";
        p.age = 17;
        p.info();
        """
        out = self._run_with_output(source).strip()
        self.assertEqual(out, "서윤 17")


if __name__ == "__main__":
    unittest.main()
