"""22편 세라밴드 후면삼각근 벌리기 — 19~21편 네이비·코랄 디자인, Linux판.
서 있는 전신 사진이라 4·5장은 사진을 줄여 머리~발이 다 보이게 넣음, 타겟 원 2개(양쪽).
usage: python3 tools/b22.py 2026-11-01_22"""
import asyncio, os, sys, json
from playwright.async_api import async_playwright

S = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else '2026-11-01_22')
PH = S + '/photos'
T = json.load(open(S + '/target.json', encoding='utf-8'))
FONT = "'Noto Sans CJK KR','Noto Sans KR',sans-serif"
NAVY, CORAL, CREAM, INK = '#1f2a44', '#ff7a59', '#fbf6f1', '#1f2a44'
W, H = 540, 675
NAME = '세라밴드 후면삼각근 벌리기'
MUSCLE = '후면삼각근'
MDESC = '어깨 뒤쪽을 감싸 팔을 뒤로 당겨 주는 근육'
Q1, Q2 = '책상 앞에 오래 앉아', '어깨가 앞으로 말렸다면?'
AMOUNT = '10번 × 2~3세트'
STEPS = ['발을 골반너비로 벌리고 <b class="c">바르게 서요</b>',
         '밴드를 어깨너비로 잡고 <b class="c">두 팔을 가슴 높이로</b> 앞으로 뻗어요',
         '어깨를 내리고 <b class="c">배에 살짝 힘</b>을 줘요',
         '숨을 내쉬며 <b class="c">두 팔을 양옆으로</b> 벌려 밴드를 가슴까지 당겨요',
         '<b class="c">2초 멈췄다</b> 천천히 앞으로 돌아와요']
CAUSES = [('💻', '팔을 앞으로 뻗고 컴퓨터 하기', '어깨 뒤쪽 근육이 약해지기 쉬워요'),
          ('📱', '고개 숙여 스마트폰 보기', '어깨가 앞으로 말리기 쉬워요'),
          ('🚗', '운전대를 오래 잡고 있기', '어깨 뒤쪽 힘을 쓸 일이 줄기 쉬워요')]
CAUTION = ['어깨가 귀 쪽으로 <b class="c">올라가지 않게</b> 해요',
           '허리를 젖히지 말고 <b class="c">배에 힘을 유지</b>해요',
           '저리거나 불편하면 <b class="c">바로 멈춰요</b>']

BASE = f"""<html lang="ko"><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:{FONT};color:{INK};-webkit-font-smoothing:antialiased}}
.badge{{display:inline-block;background:{CORAL};color:#fff;font-weight:900;border-radius:8px;font-size:14px;padding:4px 10px}}
b.c{{color:{CORAL}}}
.hdr{{position:absolute;right:14px;top:14px;display:flex;gap:6px;align-items:center;z-index:5}}
.pill{{font-weight:900;font-size:11px;letter-spacing:.02em;padding:4px 9px;border-radius:6px;line-height:1.2}}
</style></head><body>"""

def page(inner, bg='#fff', w=W, h=H):
    return BASE + f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{bg}">{inner}</div></body></html>'

def hdr(dark, person):
    logo_bg, logo_fg = ('rgba(255,255,255,.92)', NAVY) if dark else (NAVY, '#fff')
    vp = f'<span class="pill" style="background:{CORAL};color:#fff">가상인물</span>' if person else ''
    return f'<div class="hdr">{vp}<span class="pill" style="background:{logo_bg};color:{logo_fg}">INVENUE STUDIO</span></div>'

def rows(items, start, fs=15.5):
    out = ''
    for i, s in enumerate(items):
        bt = 'border-top:1px dashed #e3d9cf;' if i else ''
        out += f'<div style="display:flex;align-items:center;gap:10px;padding:6px 0;{bt}"><span style="flex:none;width:22px;height:22px;border-radius:50%;background:{NAVY};color:#fff;font-weight:700;font-size:12px;display:flex;align-items:center;justify-content:center">{start+i}</span><span style="font-size:{fs}px;font-weight:500">{s}</span></div>'
    return out

def ell(sz, ox, oy, fx, fy):
    cx, cy = ox + sz * fx, oy + sz * fy
    rw, rh = sz * T['rw'], sz * T['rh']
    return cx, cy, rw, rh, f'<div style="position:absolute;left:{cx-rw/2}px;top:{cy-rh/2}px;width:{rw}px;height:{rh}px;border:2.5px dashed {CORAL};border-radius:50%;background:rgba(255,122,89,.18);transform:rotate({T.get('rot',0)}deg)"></div>'

def marks(sz, ox, oy, w):
    cx, cy, rw, rh, e1 = ell(sz, ox, oy, T['fx'], T['fy'])
    e2 = ell(sz, ox, oy, T['ex'], T['ey'])[4]
    lx, ly = ox + sz * T['lab_x'], oy + sz * T['lab_y']
    return f'''{e1}{e2}
<svg style="position:absolute;left:0;top:0;width:{w}px;height:{w}px;overflow:visible"><line x1="{lx+20}" y1="{ly+26}" x2="{cx+rw*0.3}" y2="{cy-rh*0.4}" stroke="{CORAL}" stroke-width="2"/></svg>
<div style="position:absolute;left:{lx}px;top:{ly}px;background:{CORAL};color:#fff;font-weight:700;font-size:13px;padding:5px 11px;border-radius:999px;white-space:nowrap">{T['label']}</div>
<div style="position:absolute;left:{ox+sz*T['dir_x']}px;top:{oy+sz*T['dir_y']}px;background:rgba(31,42,68,.88);color:#fff;font-weight:700;font-size:12.5px;padding:5px 10px;border-radius:999px;white-space:nowrap">{T['dir']}</div>'''

def fitphoto(src, ph):
    sz = ph / 0.95; ox = (W - sz) / 2; oy = -0.02 * sz
    bg = f'<img src="file://{PH}/{src}" style="position:absolute;left:-20px;top:-20px;width:{W+40}px;height:{ph+40}px;object-fit:cover;filter:blur(14px)">'
    return sz, ox, oy, bg + f'<img src="file://{PH}/{src}" style="position:absolute;left:{ox}px;top:{oy}px;width:{sz}px;height:{sz}px">'

def cause_block(title_fs=26):
    cards = ''.join(f'<div style="display:flex;gap:14px;align-items:center;background:#fff;border-radius:14px;padding:14px 16px;margin-top:12px;box-shadow:0 1px 0 #eadfd3"><div style="font-size:30px">{e}</div><div><div style="font-weight:900;font-size:18px">{a}</div><div style="font-size:14.5px;color:#5b6475;margin-top:2px">{b}</div></div></div>' for e, a, b in CAUSES)
    return f''' <span class="badge" style="align-self:flex-start">주된 원인</span>
 <div style="font-weight:900;font-size:{title_fs}px;line-height:1.3;margin-top:8px">{MUSCLE}이<br>이럴 때 약해지기 쉬워요</div>{cards}
 <div style="font-size:13.5px;color:#5b6475;margin-top:16px;line-height:1.6">내 생활습관에 해당된다면<br>오늘의 1분 운동으로 깨워 주세요 👇</div>'''

def insta():
    out = []
    # 1 표지
    out.append(page(f'''{hdr(True, True)}
<img src="file://{PH}/cover.png" style="position:absolute;left:-50px;top:175px;width:640px;height:640px">
<div style="position:absolute;left:0;right:0;top:0;height:240px;background:linear-gradient({NAVY} 70%,rgba(31,42,68,0))"></div>
<div style="position:absolute;left:26px;top:24px;right:26px">
 <span class="badge">오늘의 1분 운동</span>
 <div style="color:#fff;font-weight:900;font-size:44px;line-height:1.16;margin-top:12px;letter-spacing:-1px">{Q1}<br><span style="color:{CORAL}">{Q2}</span></div>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;padding:44px 26px 20px;background:linear-gradient(rgba(31,42,68,0),rgba(31,42,68,.94) 45%)">
 <div style="color:#fff;font-weight:900;font-size:22px">{NAME} <span style="color:{CORAL}">→</span></div>
 <div style="color:#c9d1e3;font-size:13.5px;margin-top:4px">옆으로 넘겨서 1분만 따라 해 보세요</div>
</div>''', NAVY))
    # 2 부위
    out.append(page(f'''{hdr(False, True)}
<div style="position:absolute;left:0;right:0;top:0;height:150px;background:{CREAM};padding:22px 26px">
 <span class="badge">운동 부위</span>
 <div style="font-weight:900;font-size:32px;margin-top:6px">{MUSCLE}</div>
 <div style="font-size:14px;color:#5b6475;margin-top:2px">{MDESC}</div>
</div>
<img src="file://{PH}/muscle.png" style="position:absolute;left:0;top:150px;width:{W}px;height:{H-150}px;object-fit:cover;object-position:center 40%">''', CREAM))
    # 3 원인
    out.append(page(f'''{hdr(False, False)}
<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 32px">{cause_block()}</div>''', CREAM))
    # 4 시작 자세
    th = 150; ph = H - th
    sz, ox, oy, img = fitphoto('start.png', ph)
    out.append(page(f'''{hdr(False, True)}
<div style="position:absolute;left:0;right:0;top:0;height:{th}px;background:{CREAM};padding:20px 24px 0">
 <span class="badge">STEP 1~2</span><span style="font-weight:900;font-size:23px;margin-left:8px;vertical-align:middle">시작 자세</span>
 <div style="margin-top:6px">{rows(STEPS[:2], 1, 15)}</div>
</div>
<div style="position:absolute;left:0;top:{th}px;width:{W}px;height:{ph}px;overflow:hidden">{img}</div>''', CREAM))
    # 5 따라 하기
    th = 190; ph = H - th
    sz, ox, oy, img = fitphoto('action.png', ph)
    out.append(page(f'''{hdr(False, True)}
<div style="position:absolute;left:0;right:0;top:0;height:{th}px;background:{CREAM};padding:20px 24px 0">
 <span class="badge">STEP 3~5</span><span style="font-weight:900;font-size:23px;margin-left:8px;vertical-align:middle">따라 하기</span>
 <div style="margin-top:4px">{rows(STEPS[2:], 3, 14.5)}</div>
</div>
<div style="position:absolute;left:0;top:{th}px;width:{W}px;height:{ph}px;overflow:hidden">
 {img}{marks(sz, ox, oy, W)}
 <div style="position:absolute;right:16px;bottom:16px;background:{NAVY};color:#fff;font-weight:900;font-size:19px;padding:10px 20px;border-radius:12px;white-space:nowrap;box-shadow:0 4px 14px rgba(0,0,0,.25)">⏱ {AMOUNT}</div>
</div>''', CREAM))
    # 6 운동량·주의
    cau = ''.join(f'<div style="display:flex;gap:10px;align-items:flex-start;margin-top:12px"><span style="color:{CORAL};font-weight:900">✓</span><span style="color:#e4e8f1;font-size:16px;line-height:1.5">{c}</span></div>' for c in CAUTION)
    out.append(page(f'''{hdr(True, False)}
<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 32px;color:#fff">
 <span class="badge" style="align-self:flex-start">운동량</span>
 <div style="font-weight:900;font-size:40px;margin-top:10px;color:{CORAL}">{AMOUNT}</div>
 <div style="font-size:15px;color:#c9d1e3;margin-top:4px">천천히 벌리고 돌아오며 약 1분</div>
 <div style="height:1px;background:rgba(255,255,255,.2);margin:24px 0 10px"></div>
 <span class="badge" style="align-self:flex-start;background:#fff;color:{NAVY}">⚠️ 주의</span>
 {cau}
 <div style="margin-top:22px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.18);border-radius:12px;padding:12px 14px;font-size:14px;color:#c9d1e3;line-height:1.55">🎒 준비물: 세라밴드 1개<br>처음엔 가장 약한 강도부터 시작해요</div>
</div>''', NAVY))
    # 7 매장 소개
    out.append(page(f'''<div style="position:absolute;inset:0;background:{NAVY};color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 32px">
<div style="font-size:38px">📌</div>
<div style="font-weight:900;font-size:27px;line-height:1.3;margin-top:4px">저장해 두고<br>매일 1분만 해 보세요!</div>
<div style="height:1px;background:rgba(255,255,255,.2);margin:20px 0"></div>
<div style="font-weight:900;font-size:19px">인베뉴 스튜디오 <span style="font-weight:500;font-size:14px;color:#c9d1e3">울산 남구 · 1:1 전신케어</span></div>
<div style="font-size:14.5px;line-height:1.75;margin-top:8px;color:#e4e8f1">풀고 → 깨우고 → 강화하는 1:1 전신케어<br>당근 단골 <b style="color:{CORAL}">2,146명</b> · 평점 <b style="color:{CORAL}">4.9</b><br>첫 방문 모든 관리 <b style="color:{CORAL}">30% 할인</b></div>
<div style="align-self:flex-start;margin-top:18px;background:{CORAL};color:#fff;font-weight:900;font-size:16px;padding:9px 16px;border-radius:10px">예약은 프로필 링크에서 👆</div>
</div>{hdr(True, False)}''', NAVY))
    return out

def kit():
    K = 540
    out = []
    # 1 표지 정사각
    out.append(page(f'''{hdr(True, True)}
<img src="file://{PH}/cover.png" style="position:absolute;left:0px;top:150px;width:540px;height:540px">
<div style="position:absolute;left:0;right:0;top:0;height:200px;background:linear-gradient({NAVY} 72%,rgba(31,42,68,0))"></div>
<div style="position:absolute;left:24px;top:22px"><span class="badge">오늘의 1분 운동</span>
 <div style="color:#fff;font-weight:900;font-size:38px;line-height:1.16;margin-top:10px;letter-spacing:-1px">{Q1}<br><span style="color:{CORAL}">{Q2}</span></div></div>
<div style="position:absolute;left:0;right:0;bottom:0;padding:36px 24px 18px;background:linear-gradient(rgba(31,42,68,0),rgba(31,42,68,.94) 45%)">
 <div style="color:#fff;font-weight:900;font-size:22px">{NAME}</div>
 <div style="color:#c9d1e3;font-size:13px;margin-top:3px">1분만 따라 해 보세요</div></div>''', NAVY, K, K))
    # 2 운동 부위
    out.append(page(f'''<img src="file://{PH}/muscle.png" style="position:absolute;left:0;top:0;width:540px;height:540px">
<div style="position:absolute;left:24px;top:20px"><span class="badge">운동 부위</span>
 <div style="font-weight:900;font-size:34px;margin-top:6px">{MUSCLE}</div>
 <div style="font-size:14px;color:#5b6475;margin-top:4px;width:170px;line-height:1.5">{MDESC}</div></div>{hdr(False, True)}''', CREAM, K, K))
    # 3 원인
    out.append(page(f'''{hdr(False, False)}<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 32px">{cause_block(25)}</div>''', CREAM, K, K))
    # 4 운동 카드 540x750
    bw = 236
    def box(src, label, extra=''):
        return f'''<div style="position:relative;width:{bw}px;height:{bw}px;border-radius:10px;overflow:hidden">
<img src="file://{PH}/{src}" style="position:absolute;left:0;top:0;width:{bw}px;height:{bw}px">{extra}
<div style="position:absolute;left:8px;top:8px;background:{NAVY};color:#fff;font-weight:700;font-size:12px;padding:4px 9px;border-radius:6px">{label}</div>
<div style="position:absolute;right:8px;bottom:8px;background:{CORAL};color:#fff;font-weight:700;font-size:10.5px;padding:3px 7px;border-radius:5px">가상인물</div></div>'''
    am = ell(bw, 0, 0, T['fx'], T['fy'])[4] + ell(bw, 0, 0, T['ex'], T['ey'])[4] + f'<div style="position:absolute;left:6px;bottom:8px;background:{CORAL};color:#fff;font-weight:700;font-size:10.5px;padding:3px 7px;border-radius:999px;white-space:nowrap">타겟 · 양쪽 후면삼각근</div>'
    out.append(page(f'''<div style="position:absolute;inset:0;padding:22px 24px 0">
 <span class="badge" style="font-size:16px;padding:6px 12px">오늘의 1분 운동</span>
 <div style="font-weight:900;font-size:28px;margin-top:10px;letter-spacing:-.6px">{NAME}</div>
 <div style="font-size:14.5px;color:#5b6475;margin-top:6px;line-height:1.5">앞으로 말린 어깨 뒤쪽 근육을<br>밴드로 <b class="c">깨우고 강화하는</b> 운동이에요.</div>
 <div style="display:flex;align-items:center;justify-content:space-between;margin-top:14px">
  {box('start.png','① 밴드 앞으로')}<div style="color:{CORAL};font-weight:900;font-size:20px">➜</div>{box('action.png','② 양옆으로 벌리기', am)}
 </div>
 <div style="background:#fff;border-radius:12px;padding:4px 14px;margin-top:12px">{rows(STEPS, 1, 14)}</div>
 <div style="display:flex;gap:9px;margin-top:10px">
  <div style="flex:1;border:1.5px solid #f3d3c7;background:#fff;border-radius:12px;padding:10px 13px">
   <div style="color:{CORAL};font-weight:700;font-size:12px">📅 운동량</div>
   <div style="color:{NAVY};font-weight:900;font-size:21px;line-height:1.25;margin-top:3px">10번씩<br>2~3세트</div></div>
  <div style="flex:1.3;background:#fdeee8;border-radius:12px;padding:11px 13px;font-size:12.5px;line-height:1.6;color:#4a3a35">💡 어깨 으쓱 말고 등 뒤로!<br>허리는 젖히지 말고, 불편하면<br>바로 멈춰요.</div>
 </div>
 <div style="display:flex;justify-content:space-between;align-items:center;margin-top:9px">
  <span style="font-size:11px;color:#8a8f99">숨은 참지 말고 편하게 쉬어요</span>
  <span style="font-weight:900;font-size:11px;letter-spacing:.03em">INVENUE STUDIO</span></div>
</div>''', '#f7f3ee', K, 750))
    return out

async def main():
    os.makedirs(S + '/insta', exist_ok=True); os.makedirs(S + '/kit', exist_ok=True)
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(device_scale_factor=2)
        async def shot(html, w, h, path):
            await pg.set_viewport_size({'width': w, 'height': h})
            fn = path + '.html'; open(fn, 'w', encoding='utf-8').write(html)
            await pg.goto('file://' + fn); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(300)
            await pg.screenshot(path=path, type='jpeg', quality=93); os.remove(fn)
        for i, html in enumerate(insta(), 1):
            await shot(html, W, H, f'{S}/insta/{i}.jpg')
        sizes = [(540, 540)] * 3 + [(540, 750)]
        for i, (html, (w, h)) in enumerate(zip(kit(), sizes), 1):
            await shot(html, w, h, f'{S}/kit/{i}.jpg')
        await b.close()
    print('done')
asyncio.run(main())
