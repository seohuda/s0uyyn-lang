# 서윤랭 (SeoyunLang)

서윤랭은 밈 형태의 키워드 체계를 가지면서도 재귀 함수, 반복문, 배열/리스트, 스택 등의 기본 자료구조를 지원하여 백준 브론즈~실버 수준의 알고리즘 문제를 실제로 풀 수 있도록 설계된 인터프리터 언어입니다.

구현 언어로 Python 3을 선택했습니다. 한글 및 유니코드 식별자와 기호 파싱을 안정적으로 처리할 수 있고, 별도의 빌드 단계 없이 크로스 플랫폼에서 즉시 실행 및 테스트가 가능하기 때문입니다.

## 파일 확장자

서윤랭 소스 파일은 `.syl` 확장자를 사용합니다.

```text
hello.syl
hanoi.syl
```

## 설치 및 요구사항

- Python 3.10 이상 (추가 외부 의존성 없음)

### pip을 통한 설치

```bash
# 로컬 소스 디렉터리에서 설치
pip install .

# 또는 GitHub 저장소에서 바로 설치
pip install git+https://github.com/seohuda/s0uyyn-lang.git
```

설치 후 시스템 어디서나 `seoyun` 명령어를 바로 사용할 수 있습니다:

```bash
seoyun run <file.syl>
```

### 소스 클론 방식

저장소를 클론하여 바로 실행할 수도 있습니다.

```bash
git clone https://github.com/seohuda/s0uyyn-lang.git
cd s0uyyn-lang
```

## 실행 방법

CLI 명령어를 통해 `.syl` 파일을 실행할 수 있습니다.

```bash
python3 main.py run examples/hello.syl
```

또는 루트 경로의 실행 스크립트를 사용합니다.

```bash
./seoyun run examples/hello.syl
```

테스트 실행:

```bash
python3 -m unittest discover -s tests
```

## 문법 매핑

서윤랭의 키워드 매핑은 다음과 같습니다.

| 일반 문법    | 서윤랭        | 설명 |
| -------- | ---------- | --- |
| int      | e의2승       | 정수형 |
| long     | 울산큰고래      | 64비트 정수형 |
| float    | 고래         | 부동소수점 실수형 |
| char     | 오?         | 단일 문자형 |
| string   | 서울말        | 문자열 |
| bool     | 아진짜ㅏ요      | 불리언 타입 |
| true     | 짘자         | 참 값 |
| false    | 안히         | 거짓 값 |
| null     | 남친         | 널 값 |
| Array    | 사투링고       | 배열 (인덱싱, 다차원 지원) |
| List     | 블루베리스무디레시피 | 동적 리스트 |
| Stack    | 울산고래탑      | 스택 자료구조 |
| print    | 오쫄티비       | 공백 구분 출력 및 개행 |
| input    | 게히야        | 표준 입력 한 줄 읽기 |
| if       | 왜요ㅗ        | 조건문 if |
| else     | 실어요        | 조건문 else |
| while    | whale      | while 반복문 |
| for      | 너므많아ㅡㅡㅅ    | for 반복문 |
| break    | 말걸지마세요     | 루프 탈출 |
| continue | 꺼져ㅗ        | 루프 다음 반복 진행 |
| return   | 울산행KTX     | 함수 값 반환 |
| function | 이걸진짜만들었어요? | 함수 정의 |
| const    | 당당해지세요.    | 상수 선언 (재할당 불가) |
| class    | 1학년2반      | 클래스 정의 |

### 주석

단일행 및 다중행 주석 모두 `!울산말 ... 울산말!` 구문을 사용합니다.

```text
!울산말 이 부분은 단일행 주석입니다 울산말!

!울산말
여러 줄에 걸친
주석 내용입니다
울산말!
```

## 언어 사용법

### Hello World

```text
서울말 msg = "안녕하세요, 서윤랭입니다!";
오쫄티비(msg);
```

### 변수와 타입

정적 타입 기반으로 변수를 선언합니다.

```text
e의2승 x = 10;
울산큰고래 big = 1000000000000;
고래 pi = 3.14;
오? c = 'A';
서울말 name = "서윤";
아진짜ㅏ요 yes = 짘자;

당당해지세요. e의2승 MAX = 100;
!울산말 MAX = 200; -> ConstAssignmentError 발생 울산말!
```

### 조건문

```text
e의2승 score = 85;

왜요ㅗ (score >= 90) {
    오쫄티비("A 등급");
} 실어요 왜요ㅗ (score >= 80) {
    오쫄티비("B 등급");
} 실어요 {
    오쫄티비("C 등급");
}
```

### 반복문

```text
!울산말 for 반복문 울산말!
너므많아ㅡㅡㅅ (e의2승 i = 0; i < 5; i++) {
    오쫄티비(i);
}

!울산말 while 반복문과 break, continue 울산말!
e의2승 count = 0;
whale (count < 10) {
    count++;
    왜요ㅗ (count == 3) {
        꺼져ㅗ;
    }
    왜요ㅗ (count == 6) {
        말걸지마세요;
    }
    오쫄티비(count);
}
```

### 함수 및 재귀

```text
이걸진짜만들었어요? add(e의2승 a, e의2승 b) {
    울산행KTX a + b;
}

e의2승 res = add(3, 5);
오쫄티비(res);
```

### Array (사투링고)

다차원 인덱스 접근과 수정을 지원합니다.

```text
사투링고 arr = [1, 2, 3, 4];
arr[1] = 10;
오쫄티비(arr[1]);

사투링고 board = [
    [1, 2],
    [3, 4]
];
오쫄티비(board[1][0]);
```

### List (블루베리스무디레시피)

동적 리스트로 `push`, `pop`, `size`, `clear`, `insert`, `remove`, `contains` 메서드를 제공합니다.

```text
블루베리스무디레시피 nums = [1, 2, 3];
nums.push(4);
오쫄티비(nums.size());
오쫄티비(nums.pop());
```

### Stack (울산고래탑)

스택 자료구조로 `push`, `pop`, `top`, `size`, `empty` 메서드를 제공합니다.

```text
울산고래탑 s;
s.push(1);
s.push(2);
s.push(3);

오쫄티비(s.pop());
오쫄티비(s.top());
오쫄티비(s.empty());
```

### 하노이탑 예제

실제 재귀 호출이 동작하는 하노이탑 구현입니다 (`examples/hanoi.syl`).

```text
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
```

실행 결과:

```text
1 3
1 2
3 2
1 3
2 1
2 3
1 3
```

## 현재 구현 상태

- [x] 어휘 분석기 (Lexer): 유니코드 한글 식별자 및 특수 기호 키워드(`오?`, `왜요ㅗ`, `너므많아ㅡㅡㅅ`, `이걸진짜만들었어요?`, `당당해지세요.`, `1학년2반`) 인식, `!울산말 ... 울산말!` 주석 파싱
- [x] 구문 분석기 (Parser): Pratt/우선순위 기반 표현식 및 구문 파싱
- [x] 런타임 값 및 스코프 환경: 정적 타입 바인딩, 블록 스코프, 섀도잉, 상수 재할당 방지
- [x] 제어 흐름: if/else, while, for, break, continue, return
- [x] 함수 및 재귀: 콜 프레임, 로컬 스코프 바인딩, 팩토리얼/피보나치/하노이탑 재귀 실행
- [x] 컬렉션: 사투링고(Array, 다차원 지원), 블루베리스무디레시피(List), 울산고래탑(Stack)
- [x] 입출력 및 알고리즘 내장 함수: `오쫄티비`, `게히야`, `min`, `max`, `abs`, `sort`, `reverse`, `len`, `split`, 타입 변환(`int`, `float`, `string`, `char`)
- [x] 클래스 기초: 1학년2반 선언, 필드, 메서드 바인딩 및 인스턴스 멤버 접근
- [x] 에러 리포팅: 줄/열 번호, 라인 스니펫, 캐럿(`^`) 위치 표시
- [x] CLI 러너: `python3 main.py run <file.syl>` 및 `./seoyun run <file.syl>`

## TODO (미구현 항목)

다음 항목들은 키워드가 미정이거나 후속 버전 로드맵에 해당합니다. 상세 내용은 [todo.md](todo.md)를 참고하세요.

- Queue, Deque, Set, Map, PriorityQueue, Heap 서윤랭 키워드 미정
- new 키워드 미정 (현재는 클래스명 직접 호출 `Person()` 방식으로 인스턴스화)
- import 및 모듈 시스템 키워드 미정
- try/catch 예외 처리 키워드 미정
- REPL 대화형 환경

## 기여 방법

1. 버그 제보나 제안은 이슈를 통해 등록합니다.
2. 풀 리퀘스트를 제출하기 전 `python3 -m unittest discover -s tests`를 실행하여 모든 단위 테스트가 통과하는지 확인합니다.
3. 확정된 서윤랭 키워드는 임의로 변경하거나 추가하지 않습니다.
