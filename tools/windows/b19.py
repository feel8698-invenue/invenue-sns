"""19편 카드 7장 (인스타 4:5) — 큰 질문형 표지, 네이비·코랄 테마, '가상인물' 배지는 INVENUE STUDIO 옆 1회.
usage: python b19.py   (ep19 폴더의 cover/muscle/start/action.png, products.json 사용)"""
import asyncio, os, json
from playwright.async_api import async_playwright

ROOT = 'C:/Users/feel8/AppData/Local/Temp/claude/C--Users-feel8-claude-work/3b0a8dbe-662e-43f9-a723-84fff2f1ef43/scratchpad'
S = ROOT + '/ep19'
P = json.load(open(S + '/products.json', encoding='utf-8-sig'))
FONT = "'Noto Sans KR','Malgun Gothic',sans-serif"
NAVY, CORAL, CREAM, INK = '#1f2a44', '#ff7a59', '#fbf6f1', '#1f2a44'
W, H = 540, 675

BASE = f"""<html lang="ko"><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=block"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:{FONT};color:{INK};-webkit-font-smoothing:antialiased}}
.badge{{display:inline-block;background:{CORAL};color:#fff;font-weight:900;border-radius:8px;font-size:14px;padding:4px 10px}}
b.c{{color:{CORAL}}}
.hdr{{position:absolute;right:14px;top:14px;display:flex;gap:6px;align-items:center;z-index:5}}
.pill{{font-weight:900;font-size:11px;letter-spacing:.02em;padding:4px 9px;border-radius:6px;line-height:1.2}}
</style></head><body>"""

def page(inner, bg='#fff'):
    return BASE + f'<div style="position:relative;width:{W}px;height:{H}px;overflow:hidden;background:{bg}">{inner}</div></body></html>'

def hdr(dark, person):
    logo_bg, logo_fg = ('rgba(255,255,255,.92)', NAVY) if dark else (NAVY, '#fff')
    vp = f'<span class="pill" style="background:{CORAL};color:#fff">가상인물</span>' if person else ''
    return f'<div class="hdr">{vp}<span class="pill" style="background:{logo_bg};color:{logo_fg}">INVENUE STUDIO</span></div>'

def rows(items, start):
    out = ''
    for i, s in enumerate(items):
        bt = f'border-top:1px dashed #e3d9cf;' if i else ''
        out += f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0;{bt}"><span style="flex:none;width:22px;height:22px;border-radius:50%;background:{NAVY};color:#fff;font-weight:700;font-size:12px;display:flex;align-items:center;justify-content:center">{start+i}</span><span style="font-size:15.5px;font-weight:500">{s}</span></div>'
    return out

STEPS = ['매트에 누워 <b class="c">무릎을 세우고</b> 발은 바닥에 둬요',
         '땅콩볼을 <b class="c">뒤통수 아래 오목한 곳</b>에 대요',
         '턱을 살짝 당기고 <b class="c">어깨 힘</b>을 빼요',
         '숨을 내쉬며 고개를 천천히 <b class="c">왼쪽</b>으로 돌려요',
         '가운데로 돌아와 <b class="c">오른쪽</b>도 번갈아 해요']

def slides():
    out = []
    # 1 표지 — 큰 질문형
    out.append(page(f'''{hdr(True, True)}
<img src="file:///{S}/cover.png" style="position:absolute;left:-120px;top:-10px;width:780px;height:780px">
<div style="position:absolute;left:0;right:0;top:0;height:300px;background:linear-gradient({NAVY} 58%,rgba(31,42,68,0))"></div>
<div style="position:absolute;left:26px;top:24px;right:26px">
 <span class="badge">오늘의 1분 운동</span>
 <div style="color:#fff;font-weight:900;font-size:44px;line-height:1.16;margin-top:12px;letter-spacing:-1px">뒷목이 뻐근하고<br><span style="color:{CORAL}">머리가 무겁다면?</span></div>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;padding:44px 26px 20px;background:linear-gradient(rgba(31,42,68,0),rgba(31,42,68,.94) 45%)">
 <div style="color:#fff;font-weight:900;font-size:22px">누워서 땅콩볼 후두하근 풀기 <span style="color:{CORAL}">→</span></div>
 <div style="color:#c9d1e3;font-size:13.5px;margin-top:4px">옆으로 넘겨서 1분만 따라 해 보세요</div>
</div>''', NAVY))
    # 2 부위
    out.append(page(f'''{hdr(False, True)}
<div style="position:absolute;left:0;right:0;top:0;height:150px;background:{CREAM};padding:22px 26px">
 <span class="badge">운동 부위</span>
 <div style="font-weight:900;font-size:32px;margin-top:6px">후두하근</div>
 <div style="font-size:14px;color:#5b6475;margin-top:2px">뒤통수 바로 아래, 머리와 목을 잇는 작은 속근육</div>
</div>
<img src="file:///{S}/muscle.png" style="position:absolute;left:0;top:150px;width:{W}px;height:{H-150}px;object-fit:cover;object-position:center 20%">''', CREAM))
    # 3 원인 (인물 없음)
    C = [('📱','고개 숙이고 화면 오래 보기','뒷목이 굳기 쉬워요'),('💻','모니터를 내려다보며 일하기','고개가 앞으로 빠지기 쉬워요'),('😣','긴장해서 어깨·턱에 힘주기','목 뒤가 뭉치기 쉬워요')]
    cards = ''.join(f'<div style="display:flex;gap:14px;align-items:center;background:#fff;border-radius:14px;padding:14px 16px;margin-top:12px;box-shadow:0 1px 0 #eadfd3"><div style="font-size:30px">{e}</div><div><div style="font-weight:900;font-size:18px">{a}</div><div style="font-size:14.5px;color:#5b6475;margin-top:2px">{b}</div></div></div>' for e, a, b in C)
    out.append(page(f'''{hdr(False, False)}
<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 32px">
 <span class="badge" style="align-self:flex-start">주된 원인</span>
 <div style="font-weight:900;font-size:26px;line-height:1.3;margin-top:8px">후두하근이<br>이럴 때 굳기 쉬워요</div>{cards}
 <div style="font-size:13.5px;color:#5b6475;margin-top:16px;line-height:1.6">내 생활습관에 해당된다면<br>오늘의 1분 운동으로 풀어 주세요 👇</div>
</div>''', CREAM))
    # 4 시작 자세
    th = 150
    out.append(page(f'''{hdr(False, True)}
<div style="position:absolute;left:0;right:0;top:0;height:{th}px;background:{CREAM};padding:20px 24px 0">
 <span class="badge">STEP 1~2</span><span style="font-weight:900;font-size:23px;margin-left:8px;vertical-align:middle">시작 자세</span>
 <div style="margin-top:6px">{rows(STEPS[:2], 1)}</div>
</div>
<img src="file:///{S}/start.png" style="position:absolute;left:0;top:{th}px;width:{W}px;height:{H-th}px;object-fit:cover;object-position:center 45%">''', CREAM))
    # 5 동작 + 운동량
    th = 190; ph = H - th
    t = P['target']
    # 사진(정사각 1264)을 너비 540으로 놓고 세로로 가운데 맞춤 → 원본 좌표를 화면 좌표로
    scale = W; offy = (W - ph) * t.get('posy', 0.45)
    cx, cy = W * t['fx'], W * t['fy'] - offy
    rw, rh = W * t['rw'], W * t['rh']
    marks = f'''<div style="position:absolute;left:{cx-rw/2}px;top:{cy-rh/2}px;width:{rw}px;height:{rh}px;border:2.5px dashed {CORAL};border-radius:50%;background:rgba(255,122,89,.18)"></div>
<svg style="position:absolute;left:0;top:0;width:{W}px;height:{ph}px;overflow:visible"><line x1="150" y1="{cy+6}" x2="{cx-rw/2}" y2="{cy}" stroke="{CORAL}" stroke-width="2"/></svg>
<div style="position:absolute;left:14px;top:{cy-8}px;background:{CORAL};color:#fff;font-weight:700;font-size:13px;padding:5px 11px;border-radius:999px;white-space:nowrap">{t['label']}</div>
<div style="position:absolute;left:{cx+rw/2+8}px;top:{cy-34}px;background:rgba(31,42,68,.88);color:#fff;font-weight:700;font-size:12.5px;padding:5px 10px;border-radius:999px;white-space:nowrap">{t['dir']}</div>'''
    out.append(page(f'''{hdr(False, True)}
<div style="position:absolute;left:0;right:0;top:0;height:{th}px;background:{CREAM};padding:20px 24px 0">
 <span class="badge">STEP 3~5</span><span style="font-weight:900;font-size:23px;margin-left:8px;vertical-align:middle">따라 하기</span>
 <div style="margin-top:4px">{rows(STEPS[2:], 3)}</div>
</div>
<div style="position:absolute;left:0;top:{th}px;width:{W}px;height:{ph}px;overflow:hidden">
 <img src="file:///{S}/action.png" style="position:absolute;left:0;top:{-offy}px;width:{W}px;height:{W}px">{marks}
 <div style="position:absolute;left:50%;transform:translateX(-50%);bottom:16px;background:{NAVY};color:#fff;font-weight:900;font-size:19px;padding:10px 20px;border-radius:12px;white-space:nowrap;box-shadow:0 4px 14px rgba(0,0,0,.25)">⏱ 좌우 10번 × 2세트</div>
</div>''', CREAM))
    # 6 오늘의 준비물 (운동 사진 속 도구)
    def prod(label, name, n):
        return f'''<div style="background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:14px;padding:13px 16px;margin-top:12px">
<div style="color:#c9d1e3;font-size:12.5px;font-weight:700">{label}</div>
<div style="color:#fff;font-weight:900;font-size:18px;line-height:1.3;margin-top:3px">{name}</div>
<div style="color:{CORAL};font-weight:900;font-size:24px;margin-top:6px">프로필 링크 【{n}번】</div></div>'''
    out.append(page(f'''{hdr(True, True)}
<div style="position:absolute;left:26px;top:22px"><span class="badge">🎒 오늘의 준비물</span></div>
<div style="position:absolute;left:50%;top:70px;transform:translateX(-50%);width:230px;height:230px;border-radius:50%;overflow:hidden;border:4px solid {CORAL}">
 <img src="file:///{S}/start.png" style="position:absolute;width:1100px;height:1100px;left:{-1100*P['crop']['x']+115}px;top:{-1100*P['crop']['y']+115}px">
</div>
<div style="position:absolute;left:0;right:0;top:308px;text-align:center;color:#c9d1e3;font-size:13px">↑ 운동 사진 속 땅콩볼과 같은 종류</div>
<div style="position:absolute;left:26px;right:26px;top:332px">
 {prod('A · 오늘 운동 도구', P['A']['name'], P['A']['n'])}
 {prod('B · 화면 보는 습관에 도움이 되는 생활용품', P['B']['name'], P['B']['n'])}
</div>''', NAVY))
    # 7 매장 소개 (인물 없음)
    out.append(page(f'''<div style="position:absolute;inset:0;background:{NAVY};color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 32px">
<div style="font-size:38px">📌</div>
<div style="font-weight:900;font-size:27px;line-height:1.3;margin-top:4px">저장해 두고<br>매일 1분만 해 보세요!</div>
<div style="height:1px;background:rgba(255,255,255,.2);margin:20px 0"></div>
<div style="font-weight:900;font-size:19px">인베뉴 스튜디오 <span style="font-weight:500;font-size:14px;color:#c9d1e3">울산 남구 · 1:1 전신케어</span></div>
<div style="font-size:14.5px;line-height:1.75;margin-top:8px;color:#e4e8f1">풀고 → 깨우고 → 강화하는 1:1 전신케어<br>당근 단골 <b style="color:{CORAL}">2,146명</b> · 평점 <b style="color:{CORAL}">4.9</b><br>첫 방문 모든 관리 <b style="color:{CORAL}">30% 할인</b></div>
<div style="align-self:flex-start;margin-top:18px;background:{CORAL};color:#fff;font-weight:900;font-size:16px;padding:9px 16px;border-radius:10px">예약은 프로필 링크에서 👆</div>
</div>{hdr(True, False)}''', NAVY))
    return out

async def main():
    os.makedirs(S + '/insta', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='msedge'); pg = await b.new_page(device_scale_factor=2)
        await pg.set_viewport_size({'width': W, 'height': H})
        for i, html in enumerate(slides(), 1):
            fn = f'{S}/insta/{i}.html'; open(fn, 'w', encoding='utf-8').write(html)
            await pg.goto('file:///' + fn); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
            await pg.screenshot(path=f'{S}/insta/{i}.jpg', type='jpeg', quality=93); os.remove(fn)
        await b.close()
    print('done')
asyncio.run(main())
