#!/usr/bin/env python3
import sys
import os


def print_usage():
    print("사용법:")
    print("  python3 main.py <file.syl>")
    print("  python3 main.py run <file.syl>")
    print("  ./seoyun run <file.syl>")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print_usage()
        sys.exit(0)

    command = args[0]
    filepath = None

    if command == "run":
        if len(args) < 2:
            print("에러: 실행할 .syl 파일을 지정해주세요.", file=sys.stderr)
            sys.exit(1)
        filepath = args[1]
    else:
        filepath = args[0]

    if not os.path.exists(filepath):
        print(f"에러: 파일 '{filepath}'을(를) 찾을 수 없습니다.", file=sys.stderr)
        sys.exit(1)

    with open(filepath, "r", encoding="utf-8") as f:
        source_code = f.read()

    # 인터프리터 연동 (구현 후 호출)
    try:
        from src.lexer.lexer import Lexer
        from src.parser.parser import Parser
        from src.interpreter.interpreter import Interpreter

        lexer = Lexer(source_code)
        tokens = lexer.tokenize()
        parser = Parser(tokens, source_code=source_code)
        program = parser.parse()
        interpreter = Interpreter(source_code=source_code)
        interpreter.interpret(program)
    except Exception as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
