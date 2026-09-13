# SeoyunLang TODO

## Phase 0 - Project Setup
- [x] `src/` 디렉터리 및 패키지 구조 초기화
- [x] 테스트 러너 및 기본 단위 테스트 뼈대 구성 (`tests/`)
- [x] CLI 엔트리포인트 구성 (`main.py`)

## Phase 1 - Lexer
- [x] `src/lexer/token.py`에 Token, TokenType, Position 정의
- [x] `src/lexer/lexer.py`에 숫자 리터럴(정수, 부동소수점), 문자열 리터럴, 문자 리터럴 파싱 구현
- [x] 주석(`!울산말 ... 울산말!`) 단일행/다중행 스캐닝 구현
- [x] 서윤랭 특수 키워드(`오?`, `왜요ㅗ`, `너므많아ㅡㅡㅅ`, `이걸진짜만들었어요?`, `당당해지세요.`) 및 전체 키워드 테이블 매핑 구현
- [x] 연산자 및 기호 토큰(`++`, `--`, `==`, `!=`, `<=`, `>=`, `&&`, `||`, `**`, `<<`, `>>` 등) longest-match 구현
- [x] Lexer 단위 테스트 작성 (`tests/test_lexer.py`)
  - [x] 한글 및 Unicode 키워드 인식 테스트
  - [x] 특수 punctuation 포함 키워드(`오?`, `당당해지세요.` 등) 분리 방지 테스트
  - [x] 문자열 내부 키워드 무시 테스트
  - [x] 주석 처리 테스트

## Phase 2 - AST / Parser
- [x] `src/ast/nodes.py`에 AST 노드 정의 (Program, VariableDecl, ConstDecl, Assignment, BinaryOp, UnaryOp, Literal, Identifier, IfStmt, WhileStmt, ForStmt, BreakStmt, ContinueStmt, FunctionDecl, CallExpr, ReturnStmt, ArrayLiteral, IndexExpr, MemberExpr, BlockStmt, ClassDecl)
- [x] `src/parser/parser.py`에 연산자 우선순위(Pratt / Precedence Climbing) 파서 구현
- [x] 변수 선언 및 상수(`당당해지세요.`) 선언 파싱
- [x] 할당 및 복합 표현식 파싱
- [x] 제어문 파싱 (`왜요ㅗ`, `실어요`, `whale`, `너므많아ㅡㅡㅅ`, `말걸지마세요`, `꺼져ㅗ`)
- [x] 함수 선언(`이걸진짜만들었어요?`) 및 반환문(`울산행KTX`) 파싱
- [x] 컬렉션 리터럴(`[...]`) 및 인덱스 접근(`arr[i]`, `arr[i][j]`) 파싱
- [x] 메서드 및 멤버 접근(`obj.member(...)`) 파싱
- [x] 클래스 선언(`1학년2반`) 파싱
- [x] Parser 단위 테스트 작성 (`tests/test_parser.py`)

## Phase 3 - Runtime & Environment
- [x] `src/runtime/values.py`에 서윤랭 런타임 값 객체(Int, Long, Float, Char, String, Bool, Null) 정의
- [x] `src/runtime/environment.py`에 Scope Chain, 변수/상수 바인딩, Shadowing 규칙 구현
- [x] `src/interpreter/interpreter.py`에 리터럴, 산술/비교/논리 연산자 평가 구현
- [x] 변수 선언/할당 및 상수 재할당 금지(`ConstAssignmentError`) 검증
- [x] 블록 스코프 평가 테스트 (`tests/test_runtime.py`)

## Phase 4 - Control Flow
- [x] `src/interpreter/control_flow.py`에 BreakSignal, ContinueSignal, ReturnSignal 제어 흐름 구현
- [x] `왜요ㅗ` / `실어요` (if-else if-else) 실행 구현
- [x] `whale` (while) 반복문 실행 구현
- [x] `너므많아ㅡㅡㅅ` (for) 반복문 실행 구현
- [x] `말걸지마세요` (break) 및 `꺼져ㅗ` (continue) 최인접 루프 적용 구현
- [x] 제어문 단위 테스트 작성 (`tests/test_control_flow.py`)

## Phase 5 - Functions & Recursion
- [x] `src/runtime/function.py`에 함수 객체, Call Frame, 매개변수 로컬 스코프 바인딩 구현
- [x] `울산행KTX` 반환값 처리 및 `남친` (null) 반환 구현
- [x] 재귀 함수 호출 스택 및 실행 구현
- [x] 팩토리얼(Factorial) 및 피보나치(Fibonacci) 재귀 실행 테스트
- [x] 하노이탑(Hanoi) 재귀 실행 및 출력 결과 검증 테스트 (`tests/test_function.py`)

## Phase 6 - Collections
- [x] `사투링고` (Array) 런타임 및 다차원 인덱스 읽기/쓰기 구현
- [x] `블루베리스무디레시피` (List) 런타임 및 메서드(`size`, `push`, `pop`, `clear`, `insert`, `remove`, `contains`) 구현
- [x] `울산고래탑` (Stack) 런타임 및 메서드(`push`, `pop`, `top`, `size`, `empty`) 구현
- [x] 문자열(`서울말`) 인덱싱 및 Unicode 처리 구현
- [x] 컬렉션 단위 테스트 작성 (`tests/test_collections.py`)

## Phase 7 - Algorithm Compatibility & Builtins
- [x] `src/stdlib/builtins.py`에 입출력 구현 (`오쫄티비`, `게히야`)
- [x] 문자열 메서드 및 헬퍼 구현 (`split`, `substring`, `find`, `length`, `size`)
- [x] 기본 알고리즘 함수 구현 (`min`, `max`, `abs`, `sort`, `reverse`, `len`)
- [x] 기본 형변환 함수 구현 (`int`, `long`, `float`, `string`, `char`)
- [x] 알고리즘 내장 함수 테스트 작성 (`tests/test_builtins.py`)

## Phase 8 - Classes & Member Access
- [x] `src/runtime/klass.py`에 클래스 정의 및 인스턴스 런타임 구현
- [x] 멤버 필드 및 메서드 접근/호출 구현
- [x] 클래스 단위 테스트 작성 (`tests/test_class.py`)

## Phase 9 - Error Reporting & Diagnostics
- [x] `src/errors/errors.py`에 에러 계층 구조 정의 (`LexerError`, `SyntaxError`, `TypeError`, `NameError`, `RuntimeError`, `IndexError`, `ConstAssignmentError`)
- [x] 소스 위치(행, 열), 코드 라인 스니펫, 캐럿(`^`) 포맷팅 구현
- [x] 에러 리포팅 단위 테스트 작성 (`tests/test_errors.py`)

## Phase 10 - CLI, Examples, and Verification
- [x] `main.py` CLI 구현 (`seoyun run <file.syl>`)
- [x] `examples/` 예제 파일 작성 및 검증
  - [x] `examples/hello.syl`
  - [x] `examples/if_else.syl`
  - [x] `examples/loop.syl`
  - [x] `examples/fibonacci.syl`
  - [x] `examples/factorial.syl`
  - [x] `examples/hanoi.syl`
  - [x] `examples/array.syl`
  - [x] `examples/list.syl`
  - [x] `examples/stack.syl`
- [x] `hanoi.syl` 실제 출력 일치 검증
- [x] `README.md` 작성 (담백하고 정확한 기술 문서 스타일)

## Backlog
- [ ] Queue 키워드 결정 및 추가
- [ ] Deque 키워드 결정 및 추가
- [ ] Set 키워드 결정 및 추가
- [ ] Map 키워드 결정 및 추가
- [ ] PriorityQueue 키워드 결정 및 추가
- [ ] Heap 키워드 결정 및 추가
- [ ] import 키워드 결정 및 모듈 시스템
- [ ] new 키워드 결정
- [ ] try/catch 키워드 결정
- [ ] REPL (`seoyun repl`)
