# Windows(로컬 PC)용 렌더 코드 — 18편부터

- b18.py : batch.py의 Windows판. Edge(channel='msedge') + Noto Sans KR 웹폰트 + file:/// + utf-8 저장. 인물 사진에 '가상인물' 라벨 추가. `python b18.py 18`
- kit18.py : 블로그·당근용 운동 부위(2) · 주된 원인(3) · 운동 카드(4). 사진 상자마다 '가상인물' 라벨.
- cover18.py : cover_render.py의 Windows판, 전/후 양쪽에 '가상인물' 라벨. `python cover18.py cfg.json`
- 경로(ROOT)는 각 파일 맨 위에서 바꿔서 사용. target.json(타겟 원 위치)은 회차 폴더에 둠.
- 표지(cover.jpg)를 insta/1.jpg로 복사한 뒤 `python ../tiktok_safe.py 회차폴더`로 틱톡 9:16 생성.
