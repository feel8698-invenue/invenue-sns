import asyncio, os, json
from playwright.async_api import async_playwright

ROOT = 'C:/Users/feel8/AppData/Local/Temp/claude/C--Users-feel8-claude-work/3b0a8dbe-662e-43f9-a723-84fff2f1ef43/scratchpad'
S = ROOT + '/ep18'
OUT = S + '/kit'
os.makedirs(OUT, exist_ok=True)
T = json.load(open(S + '/target.json', encoding='utf-8-sig'))

NAME = '누워서 한 다리 뻗기 복횡근 강화'
FONT = "'Noto Sans KR','Malgun Gothic',sans-serif"
BASE = f"""
<html lang="ko"><head><meta charset="utf-8"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;900&display=block"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:{FONT};color:#1d2a23;-webkit-font-smoothing:antialiased}}
.badge{{display:inline-block;background:#2e7d5a;color:#fff;font-weight:900;border-radius:8px}}
.logo{{position:absolute;font-weight:900;letter-spacing:.02em}}
b.g{{color:#2e7d5a}}
</style></head><body>"""

def page(w, h, inner, bg='#fff'):
    return BASE + f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{bg}">{inner}</div></body></html>'

# ---------- 2. muscle 1080 ----------
muscle = page(540, 540, f"""
<img src="file:///{S}/muscle.png" style="position:absolute;inset:0;width:540px;height:540px">
<div style="position:absolute;inset:0 0 auto;height:200px;background:linear-gradient(#111 0%,rgba(17,17,17,.9) 52%,rgba(17,17,17,0))"></div>
<div style="position:absolute;left:24px;top:22px">
 <span class="badge" style="font-size:19px;padding:6px 13px">운동 부위</span>
 <div style="color:#fff;font-weight:900;font-size:54px;line-height:1.1;margin-top:8px">복횡근</div>
 <div style="color:#7ddc93;font-weight:700;font-size:19px;margin-top:6px">배 가장 깊은 곳에서 허리를 복대처럼 감싸는 속근육</div>
</div>
<div class="logo" style="right:16px;bottom:14px;color:#1d2a23;font-size:12px;background:rgba(255,255,255,.8);padding:5px 10px;border-radius:6px">INVENUE STUDIO</div>
<div style="position:absolute;right:16px;top:212px;background:rgba(20,28,24,.78);color:#fff;font-weight:700;font-size:13px;padding:4px 10px;border-radius:6px">가상인물</div>
""")

# ---------- 3. exercise card 1080x1500 ----------
steps = [
 '매트에 누워 <b class="g">무릎을 90도</b>로 들어 올려요',
 '두 팔은 <b class="g">머리 위쪽</b>으로 쭉 뻗어요',
 '배꼽을 살짝 당겨 <b class="g">허리를 매트에</b> 붙여요',
 '숨을 내쉬며 <b class="g">왼다리</b>를 천천히 쭉 뻗어요',
 '제자리로 돌아와 <b class="g">오른다리</b>도 번갈아 해요',
]
def step_rows(items, start=1, fs=15, gap=8):
    rows = ''
    for i, s in enumerate(items):
        n = start + i
        border = 'border-top:1px dashed #d5ddd8;' if i else ''
        rows += f'<div style="display:flex;align-items:center;gap:12px;padding:{gap}px 0;{border}"><span style="flex:none;width:22px;height:22px;border-radius:50%;background:#1d2a23;color:#fff;font-weight:700;font-size:12px;display:flex;align-items:center;justify-content:center">{n}</span><span style="font-size:{fs}px;font-weight:500">{s}</span></div>'
    return rows

def photo_box(src, label, green, extra='', w=212):
    bg = '#2e7d5a' if green else 'rgba(80,80,80,.85)'
    return f'''<div style="position:relative;width:{w}px;height:{w}px;border-radius:10px;overflow:hidden">
<img src="file:///{S}/{src}" style="width:100%;height:100%;object-fit:cover">{extra}
<div style="position:absolute;left:8px;top:8px;white-space:nowrap;background:{bg};color:#fff;font-weight:700;font-size:12px;padding:4px 9px;border-radius:6px">{label}</div>
<div style="position:absolute;left:8px;bottom:8px;background:rgba(20,28,24,.78);color:#fff;font-weight:700;font-size:10.5px;padding:3px 7px;border-radius:5px">가상인물</div></div>'''

def action_marks(w):
    cx, cy, rw, rh = w*T['fx'], w*T['fy'], w*T.get('rw',0.17), w*T.get('rh',0.10)
    return f'''<div style="position:absolute;left:{cx-rw/2}px;top:{cy-rh/2}px;width:{rw}px;height:{rh}px;border:2.5px dashed #3d7a52;border-radius:50%;background:rgba(61,122,82,.18);transform:rotate({T['rot']}deg)"></div>
<div style="position:absolute;right:8px;bottom:8px;background:#fff;border:2px solid #2e7d5a;color:#2e7d5a;font-weight:700;font-size:{w*0.053:.1f}px;line-height:1.35;padding:5px 8px;border-radius:7px">허리는 매트에<br>붙인 채로</div>'''

card = page(540, 750, f"""
<div style="position:absolute;inset:0;padding:22px 26px 0">
 <span class="badge" style="font-size:18px;padding:7px 13px;border-radius:9px">오늘의 1분 운동</span>
 <div style="font-weight:900;font-size:29px;margin-top:10px;letter-spacing:-.6px">{NAME}</div>
 <div style="font-size:15px;color:#4c5a52;margin-top:7px;line-height:1.5">오래 앉아 약해지기 쉬운 배 속 깊은 복횡근을<br>누워서 <b class="g">차근차근 깨워 주는</b> 운동이에요.</div>
 <div style="display:flex;align-items:center;justify-content:space-between;margin-top:14px">
  {photo_box('start.png','① 무릎 90도 들기',False)}
  <div style="color:#2e7d5a;font-weight:900;font-size:22px">➜</div>
  {photo_box('action.png','② 한 다리 뻗기',True,action_marks(212))}
 </div>
 <div style="background:#fff;border-radius:12px;padding:5px 14px;margin-top:12px">{step_rows(steps)}</div>
 <div style="display:flex;gap:9px;margin-top:11px">
  <div style="flex:1.2;border:1.5px solid #cfe2d6;background:#fff;border-radius:12px;padding:11px 13px">
   <div style="color:#2e7d5a;font-weight:700;font-size:12px">📅 운동량</div>
   <div style="color:#2e7d5a;font-weight:900;font-size:22px;line-height:1.25;margin-top:3px">좌우 번갈아<br>10번씩 2세트</div></div>
  <div style="flex:1;background:#e6f1ea;border-radius:12px;padding:12px 13px;font-size:12.5px;line-height:1.6;color:#33443b">💡 허리가 뜨면 다리를<br>조금 덜 뻗고, 불편하면<br>바로 멈춰요.</div>
 </div>
 <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px">
  <span style="font-size:11px;color:#7a877f">숨은 참지 말고 편하게 쉬어요</span>
  <span style="font-weight:900;font-size:11px;letter-spacing:.03em">INVENUE STUDIO</span></div>
</div>""", bg='#f6f7f5')

C=[('🪑','오래 앉아 있기','배에 힘을 쓰지 않아 약해지기 쉬워요'),('🧍','구부정하거나 배를 내밀고 서기','속근육이 잘 쓰이지 않아요'),('🛋️','운동할 시간이 적은 생활','쓰지 않아 약해지기 쉬워요')]
rows=''.join(f'<div style="display:flex;gap:16px;align-items:center;background:#fff;border-radius:14px;padding:14px 18px;margin-top:11px"><div style="font-size:32px">{e}</div><div><div style="font-weight:900;font-size:19px">{a}</div><div style="font-size:15px;color:#4c5a52;margin-top:2px">{b}</div></div></div>' for e,a,b in C)
cause=BASE + f'''
<div style="position:relative;width:540px;height:540px;background:#f4f6f3;padding:0 32px;display:flex;flex-direction:column;justify-content:center">
<div>
<span style="display:inline-block;background:#2e7d5a;color:#fff;font-weight:900;border-radius:8px;font-size:17px;padding:5px 12px">주된 원인</span>
<div style="font-weight:900;font-size:29px;line-height:1.3;margin-top:10px">복횡근이<br>이럴 때 약해지기 쉬워요</div>{rows}
<div style="font-size:14px;color:#4c5a52;margin-top:14px">내 생활습관에 해당된다면 오늘의 1분 운동으로 깨워 주세요 👇</div></div>
<div style="position:absolute;right:16px;top:16px;font-weight:900;font-size:12px;opacity:.9">INVENUE STUDIO</div></div></body></html>'''

async def shot(pw_page, html, w, h, path):
    await pw_page.set_viewport_size({'width': w, 'height': h})
    fn = path + '.html'; open(fn,'w',encoding='utf-8').write(html)
    await pw_page.goto('file:///' + fn); await pw_page.evaluate('document.fonts.ready'); await pw_page.wait_for_timeout(500)
    await pw_page.screenshot(path=path, type='jpeg', quality=93); os.remove(fn)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(channel='msedge'); pg = await b.new_page(device_scale_factor=2)
        await shot(pg, muscle, 540, 540, f'{OUT}/2.jpg')
        await shot(pg, cause, 540, 540, f'{OUT}/3.jpg')
        await shot(pg, card, 540, 750, f'{OUT}/4.jpg')
        await b.close()
asyncio.run(main()); print('done')
