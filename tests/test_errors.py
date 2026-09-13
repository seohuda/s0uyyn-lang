import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter
from src.errors import (
    LexerError,
    SyntaxError,
    TypeError,
    NameError,
    RuntimeError,
    IndexError,
    ConstAssignmentError,
)


class TestErrors(unittest.TestCase):
    def test_lexer_error_reporting(self):
        source = "e의2승 x = 10; @"
        with self.assertRaises(LexerError) as ctx:
            Lexer(source).tokenize()
        msg = ctx.exception.format_message()
        self.assertIn("서윤랭 LexerError", msg)
        self.assertIn("1번째 줄 14번째 문자", msg)
        self.assertIn("@", msg)

    def test_syntax_error_reporting(self):
        source = "왜요ㅗ (x > ) {\n    오쫄티비(x);\n}"
        with self.assertRaises(SyntaxError) as ctx:
            tokens = Lexer(source).tokenize()
            Parser(tokens, source_code=source).parse()
        msg = ctx.exception.format_message()
        self.assertIn("서윤랭 SyntaxError", msg)
        self.assertIn("왜요ㅗ (x > ) {", msg)
        self.assertIn("^", msg)

    def test_name_error_reporting(self):
        source = "오쫄티비(없는변수);"
        with self.assertRaises(NameError) as ctx:
            tokens = Lexer(source).tokenize()
            program = Parser(tokens, source_code=source).parse()
            Interpreter(source_code=source).interpret(program)
        msg = ctx.exception.format_message()
        self.assertIn("서윤랭 NameError", msg)
        self.assertIn("선언되지 않은 식별자입니다: '없는변수'", msg)

    def test_const_assignment_error_reporting(self):
        source = "당당해지세요. e의2승 MAX = 100;\nMAX = 200;"
        with self.assertRaises(ConstAssignmentError) as ctx:
            tokens = Lexer(source).tokenize()
            program = Parser(tokens, source_code=source).parse()
            Interpreter(source_code=source).interpret(program)
        msg = ctx.exception.format_message()
        self.assertIn("서윤랭 ConstAssignmentError", msg)
        self.assertIn("상수 'MAX'에는 값을 재할당할 수 없습니다", msg)

    def test_index_error_reporting(self):
        source = "사투링고 arr = [1, 2];\n오쫄티비(arr[5]);"
        with self.assertRaises(IndexError) as ctx:
            tokens = Lexer(source).tokenize()
            program = Parser(tokens, source_code=source).parse()
            Interpreter(source_code=source).interpret(program)
        msg = ctx.exception.format_message()
        self.assertIn("서윤랭 IndexError", msg)
        self.assertIn("인덱스 범위를 벗어났습니다: 5", msg)

    def test_divide_by_zero_runtime_error(self):
        source = "e의2승 x = 10 / 0;"
        with self.assertRaises(RuntimeError) as ctx:
            tokens = Lexer(source).tokenize()
            program = Parser(tokens, source_code=source).parse()
            Interpreter(source_code=source).interpret(program)
        msg = ctx.exception.format_message()
        self.assertIn("서윤랭 RuntimeError", msg)
        self.assertIn("0으로 나눌 수 없습니다", msg)


if __name__ == "__main__":
    unittest.main()
