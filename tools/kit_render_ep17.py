import asyncio, os
from playwright.async_api import async_playwright

S = '/home/claude/eps/17'
OUT = '/home/claude/eps/17/kitimg'
os.makedirs(OUT + '/insta', exist_ok=True)
os.makedirs(OUT + '/tiktok', exist_ok=True)

NAME = '마사지볼 전완근 풀기'
FONT = "'Noto Sans CJK KR','Noto Sans KR',sans-serif"
BASE = f"""
<html lang="ko"><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:{FONT};color:#1d2a23;-webkit-font-smoothing:antialiased}}
.badge{{display:inline-block;background:#2e7d5a;color:#fff;font-weight:900;border-radius:8px}}
.logo{{position:absolute;font-weight:900;letter-spacing:.02em}}
b.g{{color:#2e7d5a}}
</style></head><body>"""

def page(w, h, inner, bg='#fff'):
    return BASE + f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{bg}">{inner}</div></body></html>'

# ---------- 1. thumbnail 1080 ----------
thumb = page(540, 540, f"""
<img src="file://{S}/action.png" style="position:absolute;inset:0;width:540px;height:540px">
<div style="position:absolute;inset:0 0 auto;height:260px;background:linear-gradient(#141414 0%,rgba(20,20,20,.86) 45%,rgba(20,20,20,0))"></div>
<div style="position:absolute;left:24px;top:22px">
 <span class="badge" style="font-size:19px;padding:6px 13px">오늘의 1분 운동</span>
 <div style="color:#fff;font-weight:900;font-size:35px;line-height:1.2;margin-top:12px;letter-spacing:-.5px">{NAME}</div>
 <div style="color:#7ddc93;font-weight:700;font-size:20px;margin-top:14px">허벅지 앞 뭉침을 푸는 1분</div>
</div>
<div class="logo" style="right:13px;bottom:13px;background:rgba(40,40,40,.72);color:#fff;font-size:12px;padding:6px 12px;border-radius:6px">INVENUE STUDIO</div>
""")

# ---------- 2. muscle 1080 ----------
muscle = page(540, 540, f"""
<img src="file://{S}/muscle.png" style="position:absolute;inset:0;width:540px;height:540px">
<div style="position:absolute;inset:0 0 auto;height:230px;background:linear-gradient(#111 0%,rgba(17,17,17,.9) 52%,rgba(17,17,17,0))"></div>
<div style="position:absolute;left:24px;top:22px">
 <span class="badge" style="font-size:19px;padding:6px 13px">운동 부위</span>
 <div style="color:#fff;font-weight:900;font-size:54px;line-height:1.1;margin-top:8px">전완근</div>
 <div style="color:#7ddc93;font-weight:700;font-size:19px;margin-top:6px">팔꿈치에서 손목까지 아래팔을 감싸는 근육</div>
</div>
<div class="logo" style="right:16px;bottom:14px;color:#1d2a23;font-size:12px;background:rgba(255,255,255,.8);padding:5px 10px;border-radius:6px">INVENUE STUDIO</div>
""")

# ---------- 3. exercise card 1080x1500 ----------
steps = [
 '책상 앞 의자에 <b class="g">허리 펴고</b> 앉아요',
 '<b class="g">오른손</b> 손바닥이 위로 오게 손등을 책상에 올려요',
 '<b class="g">왼손</b>으로 마사지볼을 오른쪽 <b class="g">팔꿈치 아래 안쪽</b>에 대요',
 '지그시 누르며 <b class="g">손목 쪽</b>으로 천천히 굴려요',
 '뭉친 곳은 <b class="g">5초</b> 멈추고, <b class="g">30초</b> 후 왼팔도 해요',
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
<img src="file://{S}/{src}" style="width:100%;height:100%;object-fit:cover">{extra}
<div style="position:absolute;left:8px;top:8px;white-space:nowrap;background:{bg};color:#fff;font-weight:700;font-size:12px;padding:4px 9px;border-radius:6px">{label}</div></div>'''

def action_marks(w):
    cx, cy, rw, rh = w*0.318, w*0.722, w*0.17, w*0.06
    return f'''<div style="position:absolute;left:{cx-rw/2}px;top:{cy-rh/2}px;width:{rw}px;height:{rh}px;border:2.5px dashed #3d7a52;border-radius:50%;background:rgba(61,122,82,.18);transform:rotate(100deg)"></div>
<div style="position:absolute;right:8px;bottom:8px;background:#fff;border:2px solid #2e7d5a;color:#2e7d5a;font-weight:700;font-size:{w*0.053:.1f}px;line-height:1.35;padding:5px 8px;border-radius:7px">손목 쪽으로<br>꾹꾹 굴려요</div>'''

card = page(540, 750, f"""
<div style="position:absolute;inset:0;padding:22px 26px 0">
 <span class="badge" style="font-size:18px;padding:7px 13px;border-radius:9px">오늘의 1분 운동</span>
 <div style="font-weight:900;font-size:30px;margin-top:10px;letter-spacing:-.6px">{NAME}</div>
 <div style="font-size:15px;color:#4c5a52;margin-top:7px;line-height:1.5">스마트폰·마우스로 굳기 쉬운 아래팔 전완근을<br>마사지볼로 <b class="g">시원하게 풀어 주는</b> 운동이에요.</div>
 <div style="display:flex;align-items:center;justify-content:space-between;margin-top:14px">
  {photo_box('start.png','① 팔꿈치 아래에 볼',False)}
  <div style="color:#2e7d5a;font-weight:900;font-size:22px">➜</div>
  {photo_box('action.png','② 손목 쪽으로 굴리기',True,action_marks(212))}
 </div>
 <div style="background:#fff;border-radius:12px;padding:5px 14px;margin-top:12px">{step_rows(steps)}</div>
 <div style="display:flex;gap:9px;margin-top:11px">
  <div style="flex:1.2;border:1.5px solid #cfe2d6;background:#fff;border-radius:12px;padding:11px 13px">
   <div style="color:#2e7d5a;font-weight:700;font-size:12px">📅 운동량</div>
   <div style="color:#2e7d5a;font-weight:900;font-size:22px;line-height:1.25;margin-top:3px">좌우 30초씩<br>2~3번</div></div>
  <div style="flex:1;background:#e6f1ea;border-radius:12px;padding:12px 13px;font-size:12.5px;line-height:1.6;color:#33443b">💡 손목 뼈 위는 세게<br>누르지 말고, 저리면<br>바로 멈춰요.</div>
 </div>
 <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px">
  <span style="font-size:11px;color:#7a877f">숨은 참지 말고 편하게 쉬어요</span>
  <span style="font-weight:900;font-size:11px;letter-spacing:.03em">INVENUE STUDIO</span></div>
</div>""", bg='#f6f7f5')


C=[('📱','스마트폰을 오래 쥐고 보기','아래팔이 굳기 쉬워요'),('🖱️','마우스·키보드를 오래 쓰기','손목을 꺾은 채라 굳기 쉬워요'),('🧺','집안일·육아로 손을 많이 쓰기','많이 쓰여 뭉치기 쉬워요')]
rows=''.join(f'<div style="display:flex;gap:16px;align-items:center;background:#fff;border-radius:14px;padding:14px 18px;margin-top:11px"><div style="font-size:32px">{e}</div><div><div style="font-weight:900;font-size:19px">{a}</div><div style="font-size:15px;color:#4c5a52;margin-top:2px">{b}</div></div></div>' for e,a,b in C)
cause=f'''<html><head><meta charset="utf-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:{FONT};color:#1d2a23}}</style></head><body>
<div style="position:relative;width:540px;height:540px;background:#f4f6f3;padding:0 32px;display:flex;flex-direction:column;justify-content:center">
<div>
<span style="display:inline-block;align-self:flex-start;background:#2e7d5a;color:#fff;font-weight:900;border-radius:8px;font-size:17px;padding:5px 12px">주된 원인</span>
<div style="font-weight:900;font-size:29px;line-height:1.3;margin-top:10px">전완근이<br>이럴 때 굳기 쉬워요</div>{rows}
<div style="font-size:14px;color:#4c5a52;margin-top:14px">내 생활습관에 해당된다면 오늘의 1분 운동으로 풀어 주세요 👇</div></div>
<div style="position:absolute;right:16px;top:16px;font-weight:900;font-size:12px;opacity:.9">INVENUE STUDIO</div></div></body></html>'''

async def shot(pw_page, html, w, h, path):
    await pw_page.set_viewport_size({'width': w, 'height': h})
    fn = path + '.html'; open(fn,'w').write(html)
    await pw_page.goto('file://' + fn); await pw_page.wait_for_timeout(300)
    await pw_page.screenshot(path=path, type='jpeg', quality=93); os.remove(fn)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(device_scale_factor=2)
        await shot(pg, muscle, 540, 540, f'{OUT}/2.jpg')
        await shot(pg, card, 540, 750, f'{OUT}/4.jpg')
        await shot(pg, cause, 540, 540, f'{OUT}/3.jpg')
        await b.close()
asyncio.run(main()); print('done')
