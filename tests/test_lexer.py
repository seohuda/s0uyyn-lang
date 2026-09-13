import unittest
from src.lexer import Lexer, TokenType
from src.errors import LexerError


class TestLexer(unittest.TestCase):
    def test_special_punctuation_keywords(self):
        """특수 punctuation 포함 키워드가 단일 토큰으로 정상 인식되는지 검증"""
        source = "오? 왜요ㅗ 너므많아ㅡㅡㅅ 이걸진짜만들었어요? 당당해지세요. 1학년2반"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        expected_types = [
            TokenType.KW_CHAR,       # 오?
            TokenType.KW_IF,         # 왜요ㅗ
            TokenType.KW_FOR,        # 너므많아ㅡㅡㅅ
            TokenType.KW_FUNCTION,   # 이걸진짜만들었어요?
            TokenType.KW_CONST,      # 당당해지세요.
            TokenType.KW_CLASS,      # 1학년2반
            TokenType.EOF,
        ]
        self.assertEqual([t.type for t in tokens], expected_types)
        self.assertEqual(tokens[0].lexeme, "오?")
        self.assertEqual(tokens[1].lexeme, "왜요ㅗ")
        self.assertEqual(tokens[2].lexeme, "너므많아ㅡㅡㅅ")
        self.assertEqual(tokens[3].lexeme, "이걸진짜만들었어요?")
        self.assertEqual(tokens[4].lexeme, "당당해지세요.")
        self.assertEqual(tokens[5].lexeme, "1학년2반")

    def test_all_grammar_keywords(self):
        """서윤랭 23개 확정 키워드 전체 매핑 검증"""
        source = (
            "e의2승 울산큰고래 고래 오? 서울말 아진짜ㅏ요 짘자 안히 남친 "
            "사투링고 블루베리스무디레시피 울산고래탑 오쫄티비 게히야 "
            "왜요ㅗ 실어요 whale 너므많아ㅡㅡㅅ 말걸지마세요 꺼져ㅗ 울산행KTX "
            "이걸진짜만들었어요? 당당해지세요. 1학년2반"
        )
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        expected = [
            TokenType.KW_INT,
            TokenType.KW_LONG,
            TokenType.KW_FLOAT,
            TokenType.KW_CHAR,
            TokenType.KW_STRING,
            TokenType.KW_BOOL,
            TokenType.KW_TRUE,
            TokenType.KW_FALSE,
            TokenType.KW_NULL,
            TokenType.KW_ARRAY,
            TokenType.KW_LIST,
            TokenType.KW_STACK,
            TokenType.KW_PRINT,
            TokenType.KW_INPUT,
            TokenType.KW_IF,
            TokenType.KW_ELSE,
            TokenType.KW_WHILE,
            TokenType.KW_FOR,
            TokenType.KW_BREAK,
            TokenType.KW_CONTINUE,
            TokenType.KW_RETURN,
            TokenType.KW_FUNCTION,
            TokenType.KW_CONST,
            TokenType.KW_CLASS,
            TokenType.EOF,
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_identifiers_not_confused_with_keywords(self):
        """키워드 접두사를 가진 식별자가 키워드로 오인되지 않는지 검증"""
        source = "고래밥 고래고기 오빠 안히야 왜요"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        self.assertEqual(
            [t.type for t in tokens],
            [
                TokenType.IDENTIFIER,
                TokenType.IDENTIFIER,
                TokenType.IDENTIFIER,
                TokenType.IDENTIFIER,
                TokenType.IDENTIFIER,
                TokenType.EOF,
            ],
        )
        self.assertEqual(tokens[0].lexeme, "고래밥")
        self.assertEqual(tokens[1].lexeme, "고래고기")
        self.assertEqual(tokens[2].lexeme, "오빠")
        self.assertEqual(tokens[3].lexeme, "안히야")
        self.assertEqual(tokens[4].lexeme, "왜요")

    def test_keywords_inside_string_literal(self):
        """문자열 내부에 등장하는 서윤랭 키워드는 키워드 토큰으로 인식되지 않아야 함"""
        source = '서울말 s = "왜요ㅗ 고래 남친";'
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        self.assertEqual(
            [t.type for t in tokens],
            [
                TokenType.KW_STRING,
                TokenType.IDENTIFIER,
                TokenType.EQ,
                TokenType.STRING_LITERAL,
                TokenType.SEMICOLON,
                TokenType.EOF,
            ],
        )
        self.assertEqual(tokens[3].value, "왜요ㅗ 고래 남친")

    def test_comments(self):
        """단일행 및 다중행 주석 처리 검증"""
        source = """
        !울산말 이 부분은 단일행 주석 울산말!
        e의2승 x = 10;
        !울산말
        여기는
        다중행
        주석입니다
        울산말!
        오쫄티비(x);
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        expected = [
            TokenType.KW_INT,
            TokenType.IDENTIFIER,
            TokenType.EQ,
            TokenType.INT_LITERAL,
            TokenType.SEMICOLON,
            TokenType.KW_PRINT,
            TokenType.LPAREN,
            TokenType.IDENTIFIER,
            TokenType.RPAREN,
            TokenType.SEMICOLON,
            TokenType.EOF,
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_unclosed_comment_raises_lexer_error(self):
        """닫히지 않은 주석에 대한 에러 검증"""
        source = "!울산말 닫히지 않은 주석..."
        lexer = Lexer(source)
        with self.assertRaises(LexerError) as ctx:
            lexer.tokenize()
        self.assertIn("닫히지 않은 주석", str(ctx.exception))

    def test_numbers_and_characters(self):
        """정수, 부동소수점, 문자 리터럴 검증"""
        source = "10 1000000000000 3.14 'A' '\\n'"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        self.assertEqual(tokens[0].type, TokenType.INT_LITERAL)
        self.assertEqual(tokens[0].value, 10)
        self.assertEqual(tokens[1].type, TokenType.INT_LITERAL)
        self.assertEqual(tokens[1].value, 1000000000000)
        self.assertEqual(tokens[2].type, TokenType.FLOAT_LITERAL)
        self.assertEqual(tokens[2].value, 3.14)
        self.assertEqual(tokens[3].type, TokenType.CHAR_LITERAL)
        self.assertEqual(tokens[3].value, "A")
        self.assertEqual(tokens[4].type, TokenType.CHAR_LITERAL)
        self.assertEqual(tokens[4].value, "\n")

    def test_operators(self):
        """모든 단항/이항/비트/논리 연산자 검증"""
        source = "+ - * / % ** ++ -- == != < > <= >= && || ! & | ^ << >> = . ; , : ( ) { } [ ]"
        lexer = Lexer(source)
        tokens = lexer.tokenize()

        expected = [
            TokenType.PLUS,
            TokenType.MINUS,
            TokenType.STAR,
            TokenType.SLASH,
            TokenType.PERCENT,
            TokenType.POWER,
            TokenType.PLUS_PLUS,
            TokenType.MINUS_MINUS,
            TokenType.EQ_EQ,
            TokenType.BANG_EQ,
            TokenType.LESS,
            TokenType.GREATER,
            TokenType.LESS_EQ,
            TokenType.GREATER_EQ,
            TokenType.AND_AND,
            TokenType.OR_OR,
            TokenType.BANG,
            TokenType.AMP,
            TokenType.PIPE,
            TokenType.CARET,
            TokenType.LSHIFT,
            TokenType.RSHIFT,
            TokenType.EQ,
            TokenType.DOT,
            TokenType.SEMICOLON,
            TokenType.COMMA,
            TokenType.COLON,
            TokenType.LPAREN,
            TokenType.RPAREN,
            TokenType.LBRACE,
            TokenType.RBRACE,
            TokenType.LBRACKET,
            TokenType.RBRACKET,
            TokenType.EOF,
        ]
        self.assertEqual([t.type for t in tokens], expected)

    def test_sample_program_tokenization(self):
        """기본 서윤랭 프로그램 토큰화 검증"""
        source = """
        당당해지세요. e의2승 MAX = 100;
        이걸진짜만들었어요? 하노이(e의2승 n, e의2승 시작, e의2승 중간, e의2승 끝) {
            왜요ㅗ (n == 1) {
                오쫄티비(시작, 끝);
                울산행KTX 남친;
            }
        }
        """
        lexer = Lexer(source)
        tokens = lexer.tokenize()
        self.assertEqual(tokens[0].type, TokenType.KW_CONST)
        self.assertEqual(tokens[1].type, TokenType.KW_INT)
        self.assertEqual(tokens[2].type, TokenType.IDENTIFIER)
        self.assertEqual(tokens[2].lexeme, "MAX")


if __name__ == "__main__":
    unittest.main()
