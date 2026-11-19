# test_load_scores.py
# 설계표(명세서 6칸만 보고 만든 여덟 케이스)를 그대로 옮긴 테스트
# 실행 : pytest   (이 파일과 scores.csv · empty.csv · weird.csv 가 있는 폴더에서)

import pytest
from load_scores import load_scores


def 쓰기(path, 점수):
    """헤더와 '테스트,점수' 한 줄만 있는 CSV를 만든다."""
    with open(path, "w", encoding="utf-8") as f:
        f.write("name,score\n")
        f.write(f"테스트,{점수}\n")


# ── 정상 ────────────────────────────────────────

def test_정상_파일을_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert len(kept) == 5
    assert len(skipped) == 5
    # 같은 이름은 지우지 않고 둘 다 남긴다 (동명이인)
    assert ("김하나", 88) in kept
    assert ("김하나", 91) in kept


def test_빈_줄은_건너뛴다():
    kept, skipped = load_scores("scores.csv")
    줄번호들 = [line_no for line_no, 원본, 이유 in skipped]
    assert 10 not in 줄번호들          # 10행은 빈 줄 — 기록하지 않는다
    assert ("윤보람", 64) in kept       # 빈 줄 다음 줄도 그대로 읽는다


def test_이름에_쉼표가_있어도_읽는다():
    kept, skipped = load_scores("scores.csv")
    assert ("최,네번", 77) in kept


# ── 예외 ────────────────────────────────────────

def test_없는_파일이면_오류가_난다():
    with pytest.raises(FileNotFoundError):
        load_scores("없는파일.csv")


def test_헤더만_있으면_빈_결과가_나온다():
    kept, skipped = load_scores("empty.csv")
    assert kept == []
    assert skipped == []


# ── 경계값 ───────────────────────────────────────

@pytest.mark.parametrize("점수, 유효한가", [
    (-1,  False),   # 경계 바로 아래
    (0,   True),    # ★ 아래쪽 경계
    (1,   True),
    (99,  True),
    (100, True),    # ★ 위쪽 경계
    (101, False),   # 경계 바로 위
])
def test_점수_경계값(점수, 유효한가):
    쓰기("임시.csv", 점수)
    kept, skipped = load_scores("임시.csv")
    assert (len(kept) == 1) == 유효한가


# ── 커버리지 측정 후 추가 (기록표 ②) ─────────────────

def test_이름이_비면_건너뛴다():
    # 55-56행을 지나가게 하는 입력 — weird.csv 2행 ",90"
    kept, skipped = load_scores("weird.csv")
    assert (2, ",90", "이름이 비어 있음") in skipped
    assert kept == [("한겨울", 77), ("윤보람", 88)]


def test_직접_실행하면_요약이_나온다():
    # 77-86행 — import 가 아니라 python load_scores.py 로 실행할 때만 도는 부분
    import subprocess
    import sys
    결과 = subprocess.run(
        [sys.executable, "load_scores.py", "scores.csv"],
        capture_output=True, text=True, encoding="utf-8",
    )
    assert 결과.returncode == 0
    assert "읽은 줄 : 5개" in 결과.stdout
    assert "건너뛴 줄 : 5개" in 결과.stdout
