import unittest
from src.lexer import Lexer
from src.parser import Parser
from src.ast.nodes import (
    Program,
    VariableDecl,
    IfStmt,
    WhileStmt,
    ForStmt,
    BreakStmt,
    ContinueStmt,
    FunctionDecl,
    ReturnStmt,
    ClassDecl,
    BinaryOp,
    UnaryOp,
    UpdateExpr,
    CallExpr,
    ArrayLiteral,
    IndexExpr,
    MemberExpr,
    Identifier,
    Literal,
)


class TestParser(unittest.TestCase):
    def _parse(self, source: str) -> Program:
        tokens = Lexer(source).tokenize()
        return Parser(tokens, source_code=source).parse()

    def test_variable_and_const_declarations(self):
        source = """
        e의2승 x = 10;
        고래 pi = 3.14;
        서울말 msg = "안녕하세요";
        아진짜ㅏ요 ok = 짘자;
        울산고래탑 s;
        당당해지세요. e의2승 MAX = 100;
        """
        prog = self._parse(source)
        self.assertEqual(len(prog.statements), 6)

        # e의2승 x = 10;
        s0 = prog.statements[0]
        self.assertIsInstance(s0, VariableDecl)
        self.assertEqual(s0.type_name, "e의2승")
        self.assertEqual(s0.name, "x")
        self.assertIsInstance(s0.init, Literal)
        self.assertEqual(s0.init.value, 10)
        self.assertFalse(s0.is_const)

        # 울산고래탑 s;
        s4 = prog.statements[4]
        self.assertIsInstance(s4, VariableDecl)
        self.assertEqual(s4.name, "s")
        self.assertIsNone(s4.init)

        # 당당해지세요. e의2승 MAX = 100;
        s5 = prog.statements[5]
        self.assertIsInstance(s5, VariableDecl)
        self.assertTrue(s5.is_const)
        self.assertEqual(s5.name, "MAX")

    def test_operator_precedence(self):
        # 1 + 2 * 3 => 1 + (2 * 3)
        prog = self._parse("e의2승 res = 1 + 2 * 3;")
        decl = prog.statements[0]
        self.assertIsInstance(decl.init, BinaryOp)
        self.assertEqual(decl.init.op, "+")
        self.assertIsInstance(decl.init.right, BinaryOp)
        self.assertEqual(decl.init.right.op, "*")

        # (1 + 2) * 3 => (1 + 2) * 3
        prog2 = self._parse("e의2승 res = (1 + 2) * 3;")
        decl2 = prog2.statements[0]
        self.assertIsInstance(decl2.init, BinaryOp)
        self.assertEqual(decl2.init.op, "*")
        self.assertIsInstance(decl2.init.left, BinaryOp)
        self.assertEqual(decl2.init.left.op, "+")

        # 2 ** 3 ** 2 => 2 ** (3 ** 2)
        prog3 = self._parse("e의2승 res = 2 ** 3 ** 2;")
        decl3 = prog3.statements[0]
        self.assertEqual(decl3.init.op, "**")
        self.assertEqual(decl3.init.right.op, "**")

    def test_if_else_ladder(self):
        source = """
        왜요ㅗ (x > 10) {
            오쫄티비("A");
        } 실어요 왜요ㅗ (x > 5) {
            오쫄티비("B");
        } 실어요 {
            오쫄티비("C");
        }
        """
        prog = self._parse(source)
        s0 = prog.statements[0]
        self.assertIsInstance(s0, IfStmt)
        self.assertIsInstance(s0.else_branch, IfStmt)
        self.assertIsNotNone(s0.else_branch.else_branch)

    def test_while_and_for_loops(self):
        source = """
        whale (x < 10) {
            x++;
            말걸지마세요;
            꺼져ㅗ;
        }

        너므많아ㅡㅡㅅ (e의2승 i = 0; i < 10; i++) {
            오쫄티비(i);
        }
        """
        prog = self._parse(source)
        while_stmt = prog.statements[0]
        self.assertIsInstance(while_stmt, WhileStmt)
        self.assertEqual(len(while_stmt.body.statements), 3)
        self.assertIsInstance(while_stmt.body.statements[1], BreakStmt)
        self.assertIsInstance(while_stmt.body.statements[2], ContinueStmt)

        for_stmt = prog.statements[1]
        self.assertIsInstance(for_stmt, ForStmt)
        self.assertIsInstance(for_stmt.init, VariableDecl)
        self.assertIsInstance(for_stmt.condition, BinaryOp)
        self.assertIsInstance(for_stmt.update, UpdateExpr)

    def test_hanoi_function_parsing(self):
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
        prog = self._parse(source)
        self.assertEqual(len(prog.statements), 2)
        fn = prog.statements[0]
        self.assertIsInstance(fn, FunctionDecl)
        self.assertEqual(fn.name, "하노이")
        self.assertEqual(len(fn.params), 4)
        self.assertEqual(fn.params[0].name, "n")
        self.assertEqual(fn.params[1].name, "시작")

    def test_collections_and_member_access(self):
        source = """
        사투링고 board = [
            [1, 2],
            [3, 4]
        ];
        오쫄티비(board[1][0]);

        블루베리스무디레시피 nums = [1, 2, 3];
        nums.push(4);
        """
        prog = self._parse(source)
        self.assertEqual(len(prog.statements), 4)

        # board[1][0]
        print_stmt = prog.statements[1]
        call = print_stmt.expr
        self.assertIsInstance(call, CallExpr)
        arg = call.args[0]
        self.assertIsInstance(arg, IndexExpr)
        self.assertIsInstance(arg.target, IndexExpr)

        # nums.push(4)
        method_stmt = prog.statements[3]
        self.assertIsInstance(method_stmt.expr, CallExpr)
        self.assertIsInstance(method_stmt.expr.callee, MemberExpr)
        self.assertEqual(method_stmt.expr.callee.member, "push")

    def test_class_declaration(self):
        source = """
        1학년2반 Person {
            서울말 name;
            e의2승 age;

            이걸진짜만들었어요? greet() {
                오쫄티비(name);
            }
        }
        """
        prog = self._parse(source)
        c = prog.statements[0]
        self.assertIsInstance(c, ClassDecl)
        self.assertEqual(c.name, "Person")
        self.assertEqual(len(c.fields), 2)
        self.assertEqual(len(c.methods), 1)


if __name__ == "__main__":
    unittest.main()
