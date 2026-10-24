import asyncio, os
from playwright.async_api import async_playwright

S = '/home/claude/ep12/src'
OUT = '/home/claude/ep12/out'
os.makedirs(OUT + '/insta', exist_ok=True)
os.makedirs(OUT + '/tiktok', exist_ok=True)

NAME = '앉아서 전경골근 발끝 들기'
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
<img src="file://{S}/thumb_bg.jpg" style="position:absolute;inset:0;width:540px;height:540px">
<div style="position:absolute;inset:0 0 auto;height:260px;background:linear-gradient(#141414 0%,rgba(20,20,20,.86) 45%,rgba(20,20,20,0))"></div>
<div style="position:absolute;left:24px;top:22px">
 <span class="badge" style="font-size:19px;padding:6px 13px">오늘의 1분 운동</span>
 <div style="color:#fff;font-weight:900;font-size:35px;line-height:1.2;margin-top:12px;letter-spacing:-.5px">{NAME}</div>
 <div style="color:#7ddc93;font-weight:700;font-size:20px;margin-top:14px">정강이 앞 속근육을 깨우는 1분</div>
</div>
<div class="logo" style="right:13px;bottom:13px;background:rgba(40,40,40,.72);color:#fff;font-size:12px;padding:6px 12px;border-radius:6px">INVENUE STUDIO</div>
""")

# ---------- 2. muscle 1080 ----------
muscle = page(540, 540, f"""
<img src="file://{S}/muscle_bg.jpg" style="position:absolute;inset:0;width:540px;height:540px">
<div style="position:absolute;inset:0 0 auto;height:230px;background:linear-gradient(#111 0%,rgba(17,17,17,.9) 52%,rgba(17,17,17,0))"></div>
<div style="position:absolute;left:24px;top:22px">
 <span class="badge" style="font-size:19px;padding:6px 13px">운동 부위</span>
 <div style="color:#fff;font-weight:900;font-size:62px;line-height:1.1;margin-top:8px">전경골근</div>
 <div style="color:#7ddc93;font-weight:700;font-size:19px;margin-top:6px">정강이 앞, 발끝을 들어 주는 근육</div>
</div>
<div class="logo" style="right:16px;bottom:14px;color:#1d2a23;font-size:12px;background:rgba(255,255,255,.8);padding:5px 10px;border-radius:6px">INVENUE STUDIO</div>
""")

# ---------- 3. exercise card 1080x1500 ----------
steps = [
 '의자에 <b class="g">허리 펴고</b> 앉아요',
 '무릎 <b class="g">90도</b>, 두 발은 어깨너비로 놓아요',
 '<b class="g">뒤꿈치는</b> 바닥에 붙여 둬요',
 '발끝을 <b class="g">정강이 쪽으로</b> 끝까지 들어요',
 '<b class="g">2초</b> 멈췄다가 <b class="g">천천히</b> 내려요',
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
    # dashed circle on lower shin/ankle + bubble
    cx, cy, d = w*0.335, w*0.79, w*0.17
    return f'''<div style="position:absolute;left:{cx-d/2}px;top:{cy-d/2}px;width:{d}px;height:{d}px;border:2.5px dashed #34a56f;border-radius:50%;background:rgba(52,165,111,.22)"></div>
<div style="position:absolute;left:8px;top:32%;background:#fff;border:2px solid #2e7d5a;color:#2e7d5a;font-weight:700;font-size:{w*0.053:.1f}px;line-height:1.35;padding:5px 8px;border-radius:7px">정강이 앞이<br>단단해져요</div>'''

card = page(540, 750, f"""
<div style="position:absolute;inset:0;padding:22px 26px 0">
 <span class="badge" style="font-size:18px;padding:7px 13px;border-radius:9px">오늘의 1분 운동</span>
 <div style="font-weight:900;font-size:30px;margin-top:10px;letter-spacing:-.6px">{NAME}</div>
 <div style="font-size:15px;color:#4c5a52;margin-top:7px;line-height:1.5">정강이 앞에서 발끝을 들어 주는 전경골근을<br><b class="g">깨우고 강화하는</b> 운동이에요.</div>
 <div style="display:flex;align-items:center;justify-content:space-between;margin-top:14px">
  {photo_box('start.png','① 뒤꿈치 붙이고 앉기',False)}
  <div style="color:#2e7d5a;font-weight:900;font-size:22px">➜</div>
  {photo_box('action.png','② 발끝 끝까지 들기',True,action_marks(212))}
 </div>
 <div style="background:#fff;border-radius:12px;padding:5px 14px;margin-top:12px">{step_rows(steps)}</div>
 <div style="display:flex;gap:9px;margin-top:11px">
  <div style="flex:1.2;border:1.5px solid #cfe2d6;background:#fff;border-radius:12px;padding:11px 13px">
   <div style="color:#2e7d5a;font-weight:700;font-size:12px">📅 운동량</div>
   <div style="color:#2e7d5a;font-weight:900;font-size:22px;line-height:1.25;margin-top:3px">15번씩<br>2~3세트</div></div>
  <div style="flex:1;background:#e6f1ea;border-radius:12px;padding:12px 13px;font-size:12.5px;line-height:1.6;color:#33443b">💡 뒤꿈치가 뜨지 않게,<br>반동 없이 천천히<br>올려요.</div>
 </div>
 <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px">
  <span style="font-size:11px;color:#7a877f">숨은 참지 말고 편하게 쉬어요</span>
  <span style="font-weight:900;font-size:11px;letter-spacing:.03em">INVENUE STUDIO</span></div>
</div>""", bg='#f6f7f5')

# ---------- SNS slides ----------
def sns(w, h, top_h, top_html, photo=None, photo_extra='', bottom_html='', dark=False, full=None):
    if full:
        return page(w, h, full, bg='#f4f6f3')
    tbg = '#1d3a2c' if dark else '#f4f6f3'
    ph = f'<div style="position:absolute;left:0;top:{top_h}px;width:{w}px;height:{w}px"><img src="file://{S}/{photo}" style="width:100%;height:100%;object-fit:cover">{photo_extra}</div>'
    bot_top = top_h + w
    bot = f'<div style="position:absolute;left:0;top:{bot_top}px;width:{w}px;height:{h-bot_top}px;background:{tbg}">{bottom_html}</div>' if h - bot_top > 0 else ''
    return page(w, h, f'<div style="position:absolute;inset:0 0 auto;height:{top_h}px;background:{tbg}">{top_html}</div>{ph}{bot}')

def logo_chip(dark=False, size=11):
    c = '#fff' if dark else '#1d2a23'
    return f'<div class="logo" style="right:16px;top:14px;color:{c};font-size:{size}px;opacity:.9">INVENUE STUDIO</div>'

def slides(w, h, tk):
    top_h = 135 if not tk else 250
    k = 1.25 if tk else 1.0
    pad = 22 if not tk else 28
    out = []
    # 1 cover (question)
    t1 = f'''{logo_chip(True, 11*k)}<div style="padding:{pad}px {pad}px 0;{'padding-top:60px' if tk else ''}">
<span class="badge" style="font-size:{14*k}px;padding:4px 10px">오늘의 1분 운동</span>
<div style="color:#fff;font-weight:900;font-size:{26*k}px;line-height:1.3;margin-top:{8*k}px">계단에서 발끝이 툭,<br>걸린 적 있나요?</div></div>'''
    b1 = f'<div style="padding:{pad}px;padding-top:{26}px;color:#fff;font-weight:900;font-size:{24*k}px">{NAME} <span style="color:#7ddc93">→</span></div><div style="padding:0 {pad}px;color:#a9c9b6;font-size:{15*k}px;font-weight:500">옆으로 넘겨서 따라 해 보세요</div>' if tk else ''
    if not tk:
        t1 = t1.replace('line-height:1.3;', 'line-height:1.25;')
    ext1 = '' if tk else f'<div style="position:absolute;left:0;right:0;bottom:0;padding:40px {pad}px 16px;background:linear-gradient(rgba(29,58,44,0),rgba(29,58,44,.92));color:#fff;font-weight:900;font-size:22px">{NAME} <span style="color:#7ddc93">→</span></div>'
    out.append(sns(w, h, top_h, t1, 'action.png', ext1, b1, dark=True))
    # 2 muscle
    t2 = f'''{logo_chip(False, 11*k)}<div style="padding:{pad}px;{'padding-top:60px' if tk else ''}">
<span class="badge" style="font-size:{14*k}px;padding:4px 10px">운동 부위</span>
<div style="font-weight:900;font-size:{30*k}px;margin-top:{6*k}px">전경골근 <span style="font-size:{17*k}px;color:#4c5a52;font-weight:700">정강이 앞 근육</span></div>
<div style="font-size:{14*k}px;color:#4c5a52;margin-top:{4*k}px;line-height:1.5">걸을 때 발끝을 들어 올려<br>발이 끌리지 않게 도와줘요.</div></div>'''
    if not tk:
        t2 = t2.replace(f'<div style="font-size:{14*k}px;color:#4c5a52;margin-top:{4*k}px;line-height:1.5">걸을 때 발끝을 들어 올려<br>발이 끌리지 않게 도와줘요.</div>', f'<div style="font-size:14px;color:#4c5a52;margin-top:2px">걸을 때 발끝을 들어 발이 끌리지 않게 도와줘요.</div>')
    b2 = f'<div style="padding:{pad}px;font-size:{16*k}px;line-height:1.6;color:#33443b">오래 앉아 있거나 굽 높은 신발을 자주 신으면<br><b class="g">잘 쓰이지 않아 약해지기 쉬워요.</b></div>' if tk else ''
    out.append(sns(w, h, top_h, t2, 'muscle.png', '', b2))
    # 3 start (steps 1-2)
    def stephead(lbl, title):
        return f'''{logo_chip(False, 11*k)}<div style="padding:{pad}px;{'padding-top:60px' if tk else ''}"><span class="badge" style="font-size:{13*k}px;padding:4px 10px">{lbl}</span>
<div style="font-weight:900;font-size:{25*k}px;margin-top:{6*k}px">{title}</div></div>'''
    sbox = lambda items, st: f'<div style="padding:{pad-6}px {pad}px">{step_rows(items, st, fs=17*k, gap=8*k)}</div>'
    if tk:
        out.append(sns(w, h, top_h, stephead('STEP 1~2', '시작 자세'), 'start.png', '', sbox(steps[:2], 1)))
        out.append(sns(w, h, top_h, stephead('STEP 3~5', '발끝 들기'), 'action.png', action_marks(w), sbox(steps[2:], 3)))
    else:
        def ig_step(lbl, title, items, st, src, marks):
            top = f'''{logo_chip(False, 11)}<div style="padding:18px 22px 0"><span class="badge" style="font-size:13px;padding:4px 10px">{lbl}</span>
<span style="font-weight:900;font-size:23px;margin-left:8px;vertical-align:middle">{title}</span>
<div style="margin-top:6px">{step_rows(items, st, fs=16, gap=7)}</div></div>'''
            th = 70 + 39*len(items)
            ph_h = h - th
            return page(w, h, f'''<div style="position:absolute;inset:0 0 auto;height:{th}px;background:#f4f6f3">{top}</div>
<div style="position:absolute;left:0;top:{th}px;width:{w}px;height:{ph_h}px;overflow:hidden"><img src="file://{S}/{src}" style="position:absolute;right:0;top:0;height:{ph_h}px">{marks(ph_h)}</div>''')
        def wide_marks(ph):
            # photo occupies right ph x ph square inside the box
            off = w - ph
            cx, cy, d = off + ph*0.335, ph*0.79, ph*0.17
            return f'''<div style="position:absolute;left:{cx-d/2}px;top:{cy-d/2}px;width:{d}px;height:{d}px;border:2.5px dashed #34a56f;border-radius:50%;background:rgba(52,165,111,.22)"></div>
<div style="position:absolute;left:16px;top:30%;background:#fff;border:2px solid #2e7d5a;color:#2e7d5a;font-weight:700;font-size:15px;line-height:1.35;padding:6px 10px;border-radius:8px">정강이 앞이<br>단단해져요</div>'''
        out.append(ig_step('STEP 1~2', '시작 자세', steps[:2], 1, 'start_wide.jpg', lambda ph: ''))
        out.append(ig_step('STEP 3~5', '발끝 들기', steps[2:], 3, 'action_wide.jpg', wide_marks))
    # 5 amount + caution
    f5 = f'''{logo_chip(False, 11*k)}<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 {pad+8}px">
<span class="badge" style="align-self:flex-start;font-size:{14*k}px;padding:4px 10px">운동량</span>
<div style="font-weight:900;color:#2e7d5a;font-size:{50*k}px;line-height:1.15;margin-top:{10*k}px">15번씩<br>2~3세트</div>
<div style="font-size:{15*k}px;color:#4c5a52;margin-top:{8*k}px">틈날 때마다 하루 2번이면 충분해요</div>
<div style="background:#fff;border-radius:14px;padding:{14*k}px {16*k}px;margin-top:{24*k}px;font-size:{15*k}px;line-height:1.75">
<div style="font-weight:900;color:#c0582c;margin-bottom:4px">⚠️ 이것만 지켜 주세요</div>
· 뒤꿈치가 바닥에서 뜨지 않게<br>· 반동 없이 천천히 올리고 내리기<br>· 발목이 불편하면 바로 멈추기</div></div>'''
    out.append(sns(w, h, 0, '', full=f5))
    # 6 save + shop
    f6 = f'''<div style="position:absolute;inset:0;background:#1d3a2c;color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 {pad+8}px">
<div style="font-size:{40*k}px">📌</div>
<div style="font-weight:900;font-size:{27*k}px;line-height:1.3;margin-top:4px">저장해 두고<br>매일 1분만 해 보세요!</div>
<div style="height:1px;background:rgba(255,255,255,.2);margin:{20*k}px 0"></div>
<div style="font-weight:900;font-size:{19*k}px">인베뉴 스튜디오 <span style="font-weight:500;font-size:{14*k}px;color:#a9c9b6">울산 남구 · 1:1 전신케어</span></div>
<div style="font-size:{14.5*k}px;line-height:1.75;margin-top:{8*k}px;color:#dfece4">풀고 → 깨우고 → 강화하는 1:1 전신케어<br>당근 단골 <b style="color:#7ddc93">2,146명</b> · 평점 <b style="color:#7ddc93">4.9</b><br>첫 방문 모든 관리 <b style="color:#7ddc93">30% 할인</b></div>
<div style="align-self:flex-start;margin-top:{18*k}px;background:#7ddc93;color:#12271c;font-weight:900;font-size:{16*k}px;padding:{9*k}px {16*k}px;border-radius:10px">예약은 프로필 링크에서 👆</div>
<div class="logo" style="right:18px;bottom:16px;font-size:{11*k}px;opacity:.85">INVENUE STUDIO</div></div>'''
    out.append(sns(w, h, 0, '', full=f6))
    return out

async def shot(pw_page, html, w, h, path):
    await pw_page.set_viewport_size({'width': w, 'height': h})
    fn = path + '.html'
    open(fn,'w').write(html)
    await pw_page.goto('file://' + fn)
    await pw_page.wait_for_timeout(250)
    await pw_page.screenshot(path=path, type='jpeg', quality=93)

async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(device_scale_factor=2)
        await shot(pg, thumb, 540, 540, f'{OUT}/1.jpg')
        await shot(pg, muscle, 540, 540, f'{OUT}/2.jpg')
        await shot(pg, card, 540, 750, f'{OUT}/3.jpg')
        for i, html in enumerate(slides(540, 675, False), 1):
            await shot(pg, html, 540, 675, f'{OUT}/insta/{i}.jpg')
        for i, html in enumerate(slides(540, 960, True), 1):
            await shot(pg, html, 540, 960, f'{OUT}/tiktok/{i}.jpg')
        await b.close()
asyncio.run(main())
print('done')
