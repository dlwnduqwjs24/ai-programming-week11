# 성적 CSV 읽기 (load_scores)

## ① 무엇을 하나요 (What)

성적 CSV를 읽어 0~100 정수 점수만 골라 내고, 건너뛴 줄은 줄 번호와 이유를 함께 남긴다.

## ② 왜 만들었나요 (Why)

실제 성적 파일에는 빈 점수 칸, 105·-5 같은 범위 밖 점수, "결석" 같은 글자, 이름 안의 쉼표, 같은 이름이 두 번 나오는 줄이 섞여 있어서 그냥 읽으면 프로그램이 죽거나 틀린 점수가 조용히 섞인다.
그래서 잘못된 줄은 멈추지 않고 건너뛰되 어디서 왜 건너뛰었는지 남기는 함수가 필요했다.
10주차에는 결과가 맞는지 매번 눈으로 확인했는데, 고칠 때마다 다시 보기 힘들어서 명령 한 줄로 전부 다시 확인되는 테스트를 같이 만들었다.

## ③ 어떻게 쓰나요 (How)

파이썬 3.8 이상. Mac은 `python` 대신 `python3`, `pip` 대신 `pip3`.

```bash
# 설치
git clone https://github.com/dlwnduqwjs24/ai-programming-week11.git
cd ai-programming-week11
pip install pytest pytest-cov

# 실행 (파일 이름을 안 주면 scores.csv 를 읽음)
python load_scores.py scores.csv
```

실행하면 이렇게 나온다.

```
읽은 줄 : 5개
  김하나 88
  최,네번 77
  김하나 91
  윤보람 64
  서한별 95
건너뛴 줄 : 5개
  3행  이두리,105   ← 점수가 0~100 밖
  4행  박세찬,   ← 점수가 비어 있음
  7행  정오름,-5   ← 점수가 0~100 밖
  8행  한겨울,결석   ← 점수가 정수가 아님
  9행  장미르,72,비고없음   ← 열 개수가 2가 아님
```

다른 파일에서 쓸 때

```python
from load_scores import load_scores

kept, skipped = load_scores("scores.csv")
# kept    : [(이름, 점수), ...]
# skipped : [(줄번호, 원본줄, 이유), ...]
```

## ④ 어떻게 테스트하나요

이 폴더(`ai-programming-week11`) 안에서 실행해야 한다. 테스트가 같은 폴더의 CSV 파일을 읽기 때문.
`pytest` 명령을 못 찾는다고 나오면 `python -m pytest` 로 실행.

```bash
pytest
# 안 지나간 줄까지 보려면
pytest --cov=load_scores --cov-report=term-missing
```

```
collected 13 items

test_load_scores.py .............                                        [100%]

============================== 13 passed in 0.05s ==============================
```

커버리지는 80%. 남은 77-86행은 `python load_scores.py` 로 직접 실행할 때만 도는 화면 출력 부분이라 숫자에는 안 잡히고, `test_직접_실행하면_요약이_나온다` 가 실제로 실행해서 확인한다.

## ⑤ 파일 구성

| 파일 | 하는 일 |
| --- | --- |
| `load_scores.py` | 성적 CSV를 읽어 `(kept, skipped)` 를 돌려주는 함수. 직접 실행하면 결과를 화면에 출력 |
| `test_load_scores.py` | pytest 테스트 — 정상 3 · 예외 2 · 경계값 6(-1·0·1·99·100·101) · 커버리지 보충 2 |
| `scores.csv` | 평범한 성적 파일 — 빈 줄, 쉼표 이름, 같은 이름, 잘못된 점수가 섞여 있음 |
| `empty.csv` | 헤더만 있는 파일 |
| `weird.csv` | 이름 빈칸 · 소수 · 1000점 등 이상한 값만 모은 파일 |
| `.gitignore` | 캐시, 커버리지 결과, 테스트 중 생기는 `임시.csv` 를 올리지 않음 |
| `LICENSE` | MIT License |

## ⑥ 만든 사람 · AI를 어디에 썼는지

- 만든 사람 : 이주엽 · 2026100374
- AI를 쓴 곳 : Claude (claude-opus-5.5) — `load_scores.py` 초안(10주차 프롬프트 실험에서 받은 코드를 수업에서 정리한 것), 설계표 케이스를 pytest 코드로 옮기는 작업, README 문장 다듬기. 커밋마다 `Assisted-by: Claude:claude-opus-5.5` 를 적었다
- 내가 직접 판단한 것 : 코드를 보기 전에 명세서 6칸만 보고 여덟 케이스와 기대 결과를 정한 것, 경계를 -1·0·1·99·100·101로 잡은 것, 같은 이름은 지우지 않고 둘 다 남긴다는 규칙, 커버리지에서 안 지나간 두 곳(이름 빈칸, 직접 실행 부분)을 어떤 입력으로 채울지

## 라이선스

MIT License (LICENSE 파일 참고)
