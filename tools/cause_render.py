import asyncio
from playwright.async_api import async_playwright
FONT="'Noto Sans CJK KR','Noto Sans KR',sans-serif"
C=[('🪑','오래 앉아 있기','짧아진 채로 굳기 쉬워요'),('🥾','계단·등산·오래 서 있기','많이 쓰여 단단해지기 쉬워요'),('🏃','운동 후 풀어주지 않기','뭉친 채로 남기 쉬워요')]
rows=''.join(f'<div style="display:flex;gap:16px;align-items:center;background:#fff;border-radius:14px;padding:14px 18px;margin-top:11px"><div style="font-size:32px">{e}</div><div><div style="font-weight:900;font-size:19px">{a}</div><div style="font-size:15px;color:#4c5a52;margin-top:2px">{b}</div></div></div>' for e,a,b in C)
html=f'''<html><head><meta charset="utf-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:{FONT};color:#1d2a23}}</style></head><body>
<div style="position:relative;width:540px;height:540px;background:#f4f6f3;padding:0 32px;display:flex;flex-direction:column;justify-content:center">
<div>
<span style="display:inline-block;align-self:flex-start;background:#2e7d5a;color:#fff;font-weight:900;border-radius:8px;font-size:17px;padding:5px 12px">주된 원인</span>
<div style="font-weight:900;font-size:29px;line-height:1.3;margin-top:10px">대퇴사두근이<br>이럴 때 굳기 쉬워요</div>{rows}
<div style="font-size:14px;color:#4c5a52;margin-top:14px">내 생활습관에 해당된다면 오늘의 1분 운동으로 풀어 주세요 👇</div></div>
<div style="position:absolute;right:16px;top:16px;font-weight:900;font-size:12px;opacity:.9">INVENUE STUDIO</div></div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(device_scale_factor=2)
        await pg.set_viewport_size({'width':540,'height':540}); open('/home/claude/ep13/c.html','w').write(html)
        await pg.goto('file:///home/claude/ep13/c.html'); await pg.wait_for_timeout(300)
        await pg.screenshot(path='/home/claude/ep13/out/cause.jpg',type='jpeg',quality=93); await b.close()
asyncio.run(main())
