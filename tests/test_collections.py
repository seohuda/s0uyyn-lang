import unittest
import io
from src.lexer import Lexer
from src.parser import Parser
from src.interpreter import Interpreter


class TestCollections(unittest.TestCase):
    def _run_with_output(self, source: str) -> str:
        stdout = io.StringIO()
        tokens = Lexer(source).tokenize()
        program = Parser(tokens, source_code=source).parse()
        interp = Interpreter(source_code=source, stdout=stdout)
        interp.interpret(program)
        return stdout.getvalue()

    def test_array_and_multidimensional(self):
        source = """
        사투링고 arr = [10, 20, 30];
        오쫄티비(arr[0], arr[1], arr[2]);
        arr[1] = 99;
        오쫄티비(arr[1]);

        사투링고 board = [
            [1, 2],
            [3, 4]
        ];
        오쫄티비(board[1][0]);
        board[1][0] = 77;
        오쫄티비(board[1][0]);
        """
        output = self._run_with_output(source).strip().splitlines()
        self.assertEqual(output[0], "10 20 30")
        self.assertEqual(output[1], "99")
        self.assertEqual(output[2], "3")
        self.assertEqual(output[3], "77")

    def test_list_operations(self):
        source = """
        블루베리스무디레시피 nums = [1, 2, 3];
        nums.push(4);
        오쫄티비(nums.size());
        오쫄티비(nums.pop());
        오쫄티비(nums.size());

        nums.insert(1, 99);
        오쫄티비(nums[1]);
        오쫄티비(nums.contains(99));

        nums.remove(1);
        오쫄티비(nums.contains(99));

        nums.clear();
        오쫄티비(nums.size());
        """
        output = self._run_with_output(source).strip().splitlines()
        self.assertEqual(output[0], "4")     # push(4) -> size is 4
        self.assertEqual(output[1], "4")     # pop() -> 4
        self.assertEqual(output[2], "3")     # size is 3
        self.assertEqual(output[3], "99")    # nums[1] is 99
        self.assertEqual(output[4], "짘자")  # contains(99) -> 짘자 (True)
        self.assertEqual(output[5], "안히")  # contains(99) after remove -> 안히 (False)
        self.assertEqual(output[6], "0")     # clear() -> size is 0

    def test_stack_operations(self):
        source = """
        울산고래탑 s;
        오쫄티비(s.empty());
        s.push(10);
        s.push(20);
        s.push(30);

        오쫄티비(s.size());
        오쫄티비(s.top());
        오쫄티비(s.pop());
        오쫄티비(s.pop());
        오쫄티비(s.size());
        오쫄티비(s.empty());
        """
        output = self._run_with_output(source).strip().splitlines()
        self.assertEqual(output[0], "짘자")  # empty() is true
        self.assertEqual(output[1], "3")     # size 3
        self.assertEqual(output[2], "30")    # top 30
        self.assertEqual(output[3], "30")    # pop 30
        self.assertEqual(output[4], "20")    # pop 20
        self.assertEqual(output[5], "1")     # size 1
        self.assertEqual(output[6], "안히")  # empty() is false

    def test_string_indexing_and_methods(self):
        source = """
        서울말 s = "hello";
        오쫄티비(s[0]);
        오쫄티비(s.length());
        오쫄티비(s.find("ll"));
        오쫄티비(s.substring(1, 4));

        서울말 korean = "서윤랭언어";
        오쫄티비(korean[0]);
        오쫄티비(korean.substring(0, 3));
        """
        output = self._run_with_output(source).strip().splitlines()
        self.assertEqual(output[0], "h")
        self.assertEqual(output[1], "5")
        self.assertEqual(output[2], "2")
        self.assertEqual(output[3], "ell")
        self.assertEqual(output[4], "서")
        self.assertEqual(output[5], "서윤랭")


if __name__ == "__main__":
    unittest.main()
