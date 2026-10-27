"""오늘의 1분 운동 표지(썸네일) — 전후 대비형 (2026-10-27 사용자 확정 스타일, 회차 번호 넣지 않음)
사용: python3 cover_render.py cfg.json
cfg 예: {"before":"/abs/before.png","after":"/abs/after.png","bgx":0.70,"bgy":0.66,"agx":0.52,"agy":0.70,
 "blabel":"뻣뻣한 목","alabel":"1분 후 가볍게","title":"목이 뻣뻣하다면?","title2":"1분만 따라 해 보세요!",
 "sub":"목 옆 사각근 스트레칭 · 의자에서 바로","out":"/abs/cover.jpg"}
before/after: 같은 단발 트레이너(MAHY6s2tyVQ) 상반신 3:4 사진을 캔바 정사각 페이지에 위쪽 맞춤(crop top 0)해 1264px로 내보낸 것.
bgx/bgy·agx/agy: 사진(0~1) 안에서 빨간 빛(전)·초록 빛(후)을 둘 근육 위치. 의료 표현(통증 등) 금지.
"""
import asyncio, json, sys
C=json.load(open(sys.argv[1]))  # 설정 파일(JSON)
from playwright.async_api import async_playwright
F="'Noto Sans CJK KR',sans-serif"; S=600
def panel(src, left, cx, glow, gx, gy):
    off = 135 - cx*S
    return f'''<div style="position:absolute;left:{left}px;top:0;width:270px;height:675px;overflow:hidden;background:#15241d">
<img src="file://{src}" style="position:absolute;left:{off}px;top:0;width:{S}px;height:{S}px;-webkit-mask-image:linear-gradient(#000 82%,transparent);mask-image:linear-gradient(#000 82%,transparent)">
<div style="position:absolute;inset:0;background:{'linear-gradient(180deg,rgba(220,60,50,.10),rgba(220,60,50,.18))' if glow=='r' else 'linear-gradient(180deg,rgba(61,160,110,.08),rgba(61,160,110,.16))'}"></div>
<div style="position:absolute;left:{off+gx*S-55}px;top:{gy*S-55}px;width:110px;height:110px;border-radius:50%;background:radial-gradient({'rgba(255,60,40,.75)' if glow=='r' else 'rgba(80,220,140,.65)'},rgba(0,0,0,0) 70%);mix-blend-mode:{'multiply' if glow=='r' else 'screen'}"></div>
</div>'''
html=f'''<html><head><meta charset="utf-8"><style>*{{margin:0;padding:0;box-sizing:border-box}}body{{font-family:{F}}}</style></head><body>
<div style="position:relative;width:540px;height:675px;overflow:hidden;background:#222">
{panel(C["before"],0,C.get("bcx",0.5),"r",C["bgx"],C["bgy"])}
{panel(C["after"],270,C.get("acx",0.5),"g",C["agx"],C["agy"])}
<div style="position:absolute;left:268px;top:0;width:4px;height:675px;background:#fff;box-shadow:0 0 12px rgba(255,255,255,.9)"></div>
<div style="position:absolute;left:14px;top:14px;background:#2e7d5a;color:#fff;font-weight:900;font-size:14px;padding:5px 10px;border-radius:8px">오늘의 1분 운동</div>
<div style="position:absolute;right:14px;top:16px;color:#1d2a23;font-weight:900;font-size:11px;background:rgba(255,255,255,.75);padding:4px 8px;border-radius:6px">INVENUE STUDIO</div>
<div style="position:absolute;left:20px;top:70px;background:rgba(200,50,40,.9);color:#fff;font-weight:700;font-size:13px;padding:4px 10px;border-radius:999px">{C["blabel"]}</div>
<div style="position:absolute;right:20px;top:70px;background:rgba(46,125,90,.95);color:#fff;font-weight:700;font-size:13px;padding:4px 10px;border-radius:999px">{C["alabel"]}</div>
<svg style="position:absolute;left:205px;top:100px" width="130" height="74" viewBox="0 0 160 90" preserveAspectRatio="xMidYMid meet"><path d="M10 70 C 50 10, 110 10, 140 45" stroke="#fff" stroke-width="16" fill="none" stroke-linecap="round" opacity=".9"/><path d="M10 70 C 50 10, 110 10, 140 45" stroke="#2e7d5a" stroke-width="10" fill="none" stroke-linecap="round"/><path d="M122 30 L152 52 L118 62 Z" fill="#2e7d5a" stroke="#fff" stroke-width="3" stroke-linejoin="round"/></svg>
<div style="position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(rgba(18,30,24,0),rgba(18,30,24,.9) 40%,rgba(18,30,24,.97))"></div>
<div style="position:absolute;left:0;right:0;bottom:44px;text-align:center;color:#fff">
<div style="font-weight:900;font-size:40px;line-height:1.2;letter-spacing:-1px;text-shadow:0 2px 8px rgba(0,0,0,.5)">{C["title"]}</div>
<div style="font-weight:900;font-size:30px;line-height:1.25;margin-top:6px;color:#7ddc93">{C.get("title2","1분만 따라 해 보세요!")}</div>
<div style="font-size:14px;margin-top:10px;color:#dfece4">{C["sub"]}</div>
</div>
<div style="position:absolute;right:18px;bottom:16px;color:#7ddc93;font-weight:900;font-size:22px;letter-spacing:-4px">›››</div>
</div></body></html>'''
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(device_scale_factor=2)
        await pg.set_viewport_size({'width':540,'height':675}); open(C['out']+'.html','w').write(html)
        await pg.goto('file://'+C['out']+'.html'); await pg.wait_for_timeout(400)
        await pg.screenshot(path=C['out'],type='jpeg',quality=93); await b.close()
asyncio.run(main())
