# 인베뉴 오늘의 1분 운동 도구

- daily_render_ep12.py : 12편(전경골근) 때 쓴 렌더 코드. 썸네일(1) · 운동 부위(2) · 운동 카드(3) + 인스타 4:5 6장 + 틱톡 9:16 6장. 회차마다 문구·사진 경로·초록 원 위치를 바꿔서 사용.
- sns_batch.py : 회차 데이터(EP 딕셔너리)로 인스타/틱톡 6장을 한 번에 렌더 (1~10편 재게시 때 사용, 시작·동작 사진은 *_wide.jpg로 왼쪽 여백 확장).
- kit_template.html : 포스팅 키트 아티팩트(https://claude.ai/artifact/CUXUyn9tLSDtS95RKwB4sw) 12편 버전. T 객체 문구와 사진 1~3.jpg만 바꿔서 같은 URL에 다시 게시.
- 렌더: Playwright Chromium, device_scale_factor=2, 폰트 Noto Sans CJK KR. HTML은 파일로 저장 후 file:// 로 열어야 사진이 보임.
