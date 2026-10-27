"""1~10편 SNS 6장 렌더 (인스타 4:5, 틱톡 9:16).  usage: python3 batch.py N [N ...]"""
import asyncio, os, sys
import numpy as np
from PIL import Image, ImageFilter
from playwright.async_api import async_playwright

ROOT = '/home/claude/eps'
FONT = "'Noto Sans CJK KR','Noto Sans KR',sans-serif"

EP = {
1: dict(muscle='능형근', name='앉아서 능형근 날개뼈 모으기', q='등이 둥글게<br>말려 있지 않나요?',
   mdesc='양 날개뼈 사이, 날개뼈를 등 가운데로 모아 주는 근육', mlong='오래 숙이고 있으면 늘어난 채로 약해지기 쉬워요.',
   steps=['의자에 <b class="g">허리 펴고</b> 앉아요','팔꿈치를 <b class="g">90도</b>로 굽혀 옆구리에 붙여요','팔꿈치를 <b class="g">등 뒤로</b> 당겨 날개뼈를 모아요','<b class="g">5초</b> 버티고 천천히 풀어요','어깨가 <b class="g">귀 쪽으로</b> 올라가지 않게 해요'],
   amount='5초 × 10번', sub='하루 2~3번이면 충분해요', c1='어깨가 으쓱 올라가지 않게', type='강화'),
2: dict(muscle='견갑거근', name='앉아서 견갑거근 스트레칭', q='목 뒤가 늘<br>뻐근하고 무겁나요?',
   mdesc='목 옆에서 날개뼈 위쪽까지 이어진 근육', mlong='고개를 숙이고 화면을 오래 보면 쉽게 뭉쳐요.',
   steps=['의자에 <b class="g">허리 펴고</b> 앉아요','한 손으로 <b class="g">의자 끝</b>을 잡아요','반대 손은 머리 뒤에 <b class="g">얹기만</b> 해요','손 얹은 쪽 <b class="g">겨드랑이</b>를 보듯 고개를 숙여요','<b class="g">20초</b> 후 반대쪽도 해요'],
   amount='좌우 20초씩<br>2~3번', sub='틈날 때마다 해 주세요', c1='손으로 머리를 세게 당기지 않기', type='스트레칭'),
3: dict(muscle='회전근개', name='수건 끼고 회전근개 바깥 돌리기', q='팔 올릴 때<br>어깨가 뻑뻑한가요?',
   mdesc='어깨 관절을 감싸 잡아 주는 네 개의 속근육', mlong='팔을 쓸 때 어깨를 안정적으로 잡아 주는 근육이에요.',
   steps=['의자에 <b class="g">허리 펴고</b> 앉아요','겨드랑이에 <b class="g">수건</b>을 끼고 팔꿈치를 90도로 굽혀요','팔꿈치는 <b class="g">옆구리에</b> 붙여 둬요','<b class="g">문 열 듯</b> 손을 바깥으로 돌려요','<b class="g">3초</b> 멈췄다가 천천히 돌아와요'],
   amount='10번씩<br>하루 2~3번', sub='양쪽 모두 해 주세요', c1='수건이 빠지지 않게 팔꿈치 고정', type='강화'),
4: dict(muscle='승모근', name='승모근 으쓱 툭 풀기', q='어깨가 늘<br>귀 쪽으로 올라가 있나요?',
   mdesc='목 뒤에서 어깨와 등 위쪽까지 덮은 넓은 근육', mlong='긴장하면 어깨가 저절로 올라가며 뭉치기 쉬워요.',
   steps=['의자에 <b class="g">허리 펴고</b> 앉아요','팔은 <b class="g">편하게</b> 내려요','숨 마시며 어깨를 <b class="g">귀까지</b> 올려요','<b class="g">3초</b> 참아요','숨 내쉬며 어깨를 <b class="g">툭</b> 떨어뜨려요'],
   amount='5번씩<br>틈날 때마다', sub='업무 중간에 해 보세요', c1='목을 앞으로 빼지 않게', type='이완'),
5: dict(muscle='요방형근', name='앉아서 요방형근 옆구리 늘리기', q='오래 앉으면<br>허리 옆이 뻐근한가요?',
   mdesc='갈비뼈 아래에서 골반 위까지, 허리 양옆 깊은 근육', mlong='한쪽으로 기대 앉는 습관이 있으면 쉽게 굳어요.',
   steps=['의자에 <b class="g">허리 펴고</b> 앉아요','한 손은 <b class="g">의자 옆</b>을 짚어요','반대 팔을 <b class="g">머리 위로</b> 뻗어요','짚은 쪽으로 몸을 <b class="g">기울여요</b>','<b class="g">20초</b> 후 반대쪽도 해요'],
   amount='좌우 20초씩<br>2~3번', sub='틈날 때마다 해 주세요', c1='엉덩이가 의자에서 뜨지 않게', type='스트레칭'),
6: dict(muscle='비복근', name='벽 밀기 비복근 스트레칭', q='저녁만 되면<br>종아리가 무겁나요?',
   mdesc='종아리 뒤쪽의 볼록한 근육', mlong='오래 서 있거나 굽 있는 신발을 신으면 쉽게 굳어요.',
   steps=['벽 앞에 <b class="g">한 걸음</b> 떨어져 서요','두 손을 <b class="g">어깨 높이</b>로 벽에 짚어요','한 다리를 <b class="g">뒤로 크게</b> 빼요','뒤꿈치는 바닥에, 무릎은 <b class="g">쭉 펴요</b>','<b class="g">20초</b> 후 반대쪽도 해요'],
   amount='좌우 20초씩<br>2~3번', sub='자기 전에 해 보세요', c1='뒤꿈치가 바닥에서 뜨지 않게', type='스트레칭'),
7: dict(muscle='이상근', name='앉아서 이상근 스트레칭', q='오래 앉으면<br>엉덩이 속이 뻐근한가요?',
   mdesc='엉덩이 깊은 곳, 골반 뒤에서 허벅지 뼈로 이어진 근육', mlong='다리를 꼬고 오래 앉는 습관이 있으면 쉽게 굳어요.',
   steps=['의자 <b class="g">앞쪽에</b> 앉아요','한쪽 발목을 <b class="g">반대 무릎 위</b>에 올려요','허리를 펴고 <b class="g">가슴을 열어요</b>','허리 편 채 <b class="g">골반부터</b> 숙여요','<b class="g">20초</b> 후 반대쪽도 해요'],
   amount='좌우 20초씩<br>2~3번', sub='오래 앉은 날 꼭 해 주세요', c1='등을 둥글게 말지 않기', type='스트레칭'),
8: dict(muscle='대흉근', name='벽 짚고 대흉근 스트레칭', q='어깨가 앞으로<br>말려 있지 않나요?',
   mdesc='가슴 앞을 덮는 큰 근육', mlong='오래 숙여 있으면 짧아져 어깨를 앞으로 당겨요.',
   steps=['벽 <b class="g">옆에</b> 서요','팔을 어깨 높이에서 <b class="g">ㄱ자</b>로 벽에 대요','한 발을 <b class="g">반 걸음</b> 앞으로 내디뎌요','몸통을 <b class="g">벽 반대쪽</b>으로 돌려요','<b class="g">20초</b> 후 반대쪽도 해요'],
   amount='좌우 20초씩<br>2~3번', sub='틈날 때마다 해 주세요', c1='허리를 젖히지 말고 몸통만 돌리기', type='스트레칭'),
9: dict(muscle='장요근', name='무릎 꿇고 장요근 스트레칭', q='오래 앉았다 일어나면<br>허리가 안 펴지나요?',
   mdesc='허리뼈 앞에서 골반을 지나 허벅지 안쪽으로 이어진 깊은 근육', mlong='오래 앉아 있으면 짧아진 채로 굳기 쉬워요.',
   steps=['매트에 <b class="g">오른쪽 무릎</b>을 꿇어요','<b class="g">왼발</b>은 앞에 두고 무릎을 <b class="g">90도</b>로 세워요','허리를 펴고 손은 <b class="g">골반 위</b>에 얹어요','상체를 세운 채 <b class="g">골반을 앞으로</b> 밀어요','<b class="g">20초</b> 후 <b class="g">왼쪽 무릎</b>으로 바꿔 해요'],
   target=dict(fx=0.52, fy=0.675, rot=-30, label='타겟 · 오른쪽 장요근', dir='골반 앞으로 →'),
   amount='좌우 20초씩<br>2~3번', sub='무릎 아래에 매트를 깔아 주세요', c1='허리를 뒤로 젖히지 않게', type='스트레칭'),
10: dict(muscle='흉쇄유돌근', name='쇄골 누르고 흉쇄유돌근 스트레칭', q='스마트폰 볼 때<br>목이 앞으로 나와 있나요?',
   mdesc='귀 뒤에서 쇄골과 가슴뼈까지 비스듬히 이어진 목 앞 근육', mlong='고개를 앞으로 빼고 오래 있으면 쉽게 뭉쳐요.',
   steps=['의자에 <b class="g">허리 펴고</b> 앉아요','한 손으로 반대쪽 <b class="g">쇄골</b>을 살짝 눌러요','고개를 누른 쪽 <b class="g">반대로</b> 돌려요','턱을 <b class="g">천천히 위로</b> 들어요','<b class="g">20초</b> 후 반대쪽도 해요'],
   amount='좌우 20초씩<br>2~3번', sub='틈날 때마다 해 주세요', c1='쇄골은 세게 누르지 않기', type='스트레칭'),
13: dict(muscle='대퇴사두근', name='폼롤러 대퇴사두근 풀기', q='계단 오르고 나면<br>허벅지 앞이 뻐근한가요?',
   mdesc='골반에서 무릎뼈까지 허벅지 앞을 덮는 4갈래의 큰 근육', mlong='오래 앉아 있거나 많이 걸은 날 단단하게 굳기 쉬워요.',
   steps=['매트에 엎드려 폼롤러를 <b class="g">허벅지 앞 위쪽</b>에 놓아요','<b class="g">팔꿈치</b>를 어깨 아래에 대고 몸을 <b class="g">일자</b>로 버텨요','팔로 밀고 당기며 <b class="g">무릎 위</b>까지 천천히 굴려요','뭉친 곳에서 <b class="g">5초</b> 멈추고 숨을 내쉬어요','<b class="g">무릎 바로 위</b>에서 멈추고 다시 위로 굴려요'],
   causes=[('🪑','오래 앉아 있기','짧아진 채로 굳기 쉬워요'),('🥾','계단·등산·오래 서 있기','많이 쓰여 단단해지기 쉬워요'),('🏃','운동 후 풀어주지 않기','뭉친 채로 남기 쉬워요')],
   target=dict(fx=0.428, fy=0.598, rot=-12, label='타겟 · 양쪽 대퇴사두근', dir='← 무릎 쪽으로 굴리기'),
   amount='30초씩<br>2~3번', sub='운동 전후나 자기 전에 해 보세요', c1='무릎뼈·골반뼈 위는 굴리지 않기', c2='허리가 아래로 처지지 않게', type='폼롤러'),
14: dict(muscle='햄스트링', name='의자에 앉아 햄스트링 스트레칭', q='앉았다 일어날 때<br>허벅지 뒤가 당기나요?',
   mdesc='엉덩이 아래에서 무릎 뒤까지 허벅지 뒤를 지나는 3개의 근육', mlong='오래 앉아 있으면 짧아진 채로 굳기 쉬워요.',
   steps=['의자 앞쪽에 <b class="g">허리 펴고</b> 앉아요','<b class="g">오른쪽 다리</b>를 앞으로 쭉 뻗고 <b class="g">뒤꿈치</b>를 바닥에 대요','두 손은 <b class="g">왼쪽 무릎</b> 위에 얹어요','허리를 편 채 <b class="g">골반부터</b> 앞으로 숙여요','<b class="g">20초</b> 후 <b class="g">왼쪽 다리</b>로 바꿔 해요'],
   causes=[('🪑','오래 앉아 있기','짧아진 채로 굳기 쉬워요'),('🚗','운전·좌식 생활이 긴 날','무릎을 굽힌 채라 굳기 쉬워요'),('🏃','걷기·달리기 후 풀어주지 않기','뭉친 채로 남기 쉬워요')],
   target=dict(fx=0.47, fy=0.703, rot=29, label='타겟 · 오른쪽 햄스트링', dir='골반부터 앞으로 숙이기'),
   amount='좌우 20초씩<br>2~3번', sub='틈날 때마다 해 주세요', c1='등을 둥글게 말지 않기', c2='무릎 뒤가 저릴 만큼 숙이지 않기', type='스트레칭'),
15: dict(muscle='광배근', name='세라밴드 광배근 당겨 내리기', q='등이 구부정하고<br>어깨가 앞으로 말리나요?',
   mdesc='겨드랑이 아래에서 허리까지 등 옆을 넓게 덮는 큰 근육', mlong='구부정하게 오래 앉아 있으면 힘이 약해지기 쉬워요.',
   steps=['의자에 <b class="g">허리 펴고</b> 앉아요','세라밴드를 <b class="g">어깨너비보다 넓게</b> 잡고 머리 위로 뻗어요','숨을 내쉬며 <b class="g">팔꿈치를 옆구리 쪽</b>으로 당겨 내려요','밴드가 <b class="g">가슴 앞</b>에 오면 <b class="g">2초</b> 멈춰요','천천히 다시 <b class="g">머리 위로</b> 올려요'],
   causes=[('🪑','구부정하게 오래 앉아 있기','등 근육이 약해지기 쉬워요'),('📱','스마트폰·컴퓨터를 오래 보기','어깨가 앞으로 말리기 쉬워요'),('🙆','팔을 위로 쓸 일이 적은 생활','잘 쓰지 않아 약해지기 쉬워요')],
   target=dict(fx=0.415, fy=0.462, rot=92, rw=0.15, rh=0.075, extra=[dict(fx=0.578, fy=0.462, rot=88)], label='타겟 · 양쪽 광배근'),
   amount='10번씩<br>2~3세트', sub='밴드가 없으면 수건을 당겨도 좋아요', c1='어깨가 귀 쪽으로 올라가지 않게', c2='허리를 뒤로 젖히지 않기', cverb='약해지기', cend='깨워', type='세라밴드'),
16: dict(muscle='사각근', name='의자 잡고 사각근 스트레칭', q='목이 뻣뻣하다면?',
   mdesc='목 옆에서 쇄골 위 갈비뼈까지 이어진 목 옆 근육', mlong='고개를 숙이고 오래 있으면 굳기 쉬워요.',
   steps=['의자에 <b class="g">허리 펴고</b> 앉아요','<b class="g">오른손</b>으로 의자 옆을 잡아 <b class="g">오른쪽 어깨</b>를 내려요','고개를 <b class="g">왼쪽</b>으로 천천히 기울여요','턱을 <b class="g">살짝 들어</b> 오른쪽 목 옆을 늘려요','<b class="g">20초</b> 후 <b class="g">왼손</b>으로 잡고 반대쪽도 해요'],
   causes=[('📱','스마트폰을 오래 내려다보기','목 옆이 굳기 쉬워요'),('💻','컴퓨터 앞에서 어깨 올리고 일하기','긴장한 채로 굳기 쉬워요'),('😮‍💨','얕은 숨·가슴으로만 숨쉬기','목 근육을 많이 써 굳기 쉬워요')],
   target=dict(fx=0.467, fy=0.253, rot=119, rw=0.11, rh=0.06, label='타겟 · 오른쪽 사각근', ly=-0.12, dir='고개는 왼쪽 어깨 쪽으로'),
   amount='좌우 20초씩<br>2~3번', sub='틈날 때마다 해 주세요', c1='어깨가 따라 올라가지 않게', c2='목을 뒤로 젖히지 않기', type='스트레칭'),
17: dict(muscle='전완근', name='마사지볼 전완근 풀기', q='아래팔이 뻣뻣하다면?',
   mdesc='팔꿈치에서 손목까지 아래팔을 감싸는 근육들', mlong='손으로 쥐고 누르는 일을 오래 하면 굳기 쉬워요.',
   steps=['책상 앞 의자에 <b class="g">허리 펴고</b> 앉아요','<b class="g">오른손</b> 손바닥이 위로 오게 손등을 책상에 올려요','<b class="g">왼손</b>으로 마사지볼을 오른쪽 <b class="g">팔꿈치 아래 안쪽</b>에 대요','지그시 누르며 <b class="g">손목 쪽</b>으로 천천히 굴려요','뭉친 곳은 <b class="g">5초</b> 멈추고, <b class="g">30초</b> 후 왼팔도 해요'],
   causes=[('📱','스마트폰을 오래 쥐고 보기','아래팔이 굳기 쉬워요'),('🖱️','마우스·키보드를 오래 쓰기','손목을 꺾은 채라 굳기 쉬워요'),('🧺','집안일·육아로 손을 많이 쓰기','많이 쓰여 뭉치기 쉬워요')],
   target=dict(fx=0.318, fy=0.722, rot=100, rw=0.15, ex=0.295, ey=0.70, rh=0.05, label='타겟 · 오른쪽 전완근', ly=0.30, dir='볼을 손목 쪽으로 ↓', dfx=0.04, dfy=0.90),
   amount='좌우 30초씩<br>2~3번', sub='일하는 틈틈이 해 보세요', c1='손목 뼈 위는 세게 누르지 않기', c2='어깨에 힘 빼고 편하게', type='마사지볼'),
}

BASE = f"""<html lang="ko"><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:{FONT};color:#1d2a23;-webkit-font-smoothing:antialiased}}
.badge{{display:inline-block;background:#2e7d5a;color:#fff;font-weight:900;border-radius:8px}}
.logo{{position:absolute;font-weight:900;letter-spacing:.02em}}
b.g{{color:#2e7d5a}}
</style></head><body>"""
def page(w, h, inner, bg='#fff'):
    return BASE + f'<div style="position:relative;width:{w}px;height:{h}px;overflow:hidden;background:{bg}">{inner}</div></body></html>'

def step_rows(items, start, fs, gap):
    rows = ''
    for i, s in enumerate(items):
        border = 'border-top:1px dashed #d5ddd8;' if i else ''
        rows += f'<div style="display:flex;align-items:center;gap:12px;padding:{gap}px 0;{border}"><span style="flex:none;width:22px;height:22px;border-radius:50%;background:#1d2a23;color:#fff;font-weight:700;font-size:12px;display:flex;align-items:center;justify-content:center">{start+i}</span><span style="font-size:{fs}px;font-weight:500">{s}</span></div>'
    return rows

def logo(dark, size):
    return f'<div class="logo" style="right:16px;top:14px;color:{"#fff" if dark else "#1d2a23"};font-size:{size}px;opacity:.9">INVENUE STUDIO</div>'

def target_marks(t, ox, ph):
    """B안: 초록 점선 원 + 타겟 라벨 + 방향 라벨. ox=사진 왼쪽 시작, ph=사진 한 변(px, CSS)"""
    if not t: return ''
    cx, cy = ox + ph*t['fx'], ph*t['fy']
    rw, rh = ph*t.get('rw',0.17), ph*t.get('rh',0.10)
    lx, ly = max(14, cx - ph*0.62), max(12, cy - ph*t.get('ly',0.34))
    out = f'''<div style="position:absolute;left:{cx-rw/2}px;top:{cy-rh/2}px;width:{rw}px;height:{rh}px;border:2.5px dashed #3d7a52;border-radius:50%;background:rgba(61,122,82,.18);transform:rotate({t['rot']}deg)"></div>
<svg style="position:absolute;left:0;top:0;width:{ox+ph}px;height:{ph}px;overflow:visible"><line x1="{lx+70}" y1="{ly+26}" x2="{ox+ph*t['ex'] if 'ex' in t else cx-rw*0.35}" y2="{ph*t['ey'] if 'ey' in t else cy-rh*0.35}" stroke="#3d7a52" stroke-width="2"/></svg>
<div style="position:absolute;left:{lx}px;top:{ly}px;background:#3d7a52;color:#fff;font-weight:700;font-size:14px;padding:6px 12px;border-radius:999px;white-space:nowrap">{t['label']}</div>'''
    for ex in t.get('extra', []):
        ecx, ecy = ox + ph*ex['fx'], ph*ex['fy']
        out += f'''<div style="position:absolute;left:{ecx-rw/2}px;top:{ecy-rh/2}px;width:{rw}px;height:{rh}px;border:2.5px dashed #3d7a52;border-radius:50%;background:rgba(61,122,82,.18);transform:rotate({ex['rot']}deg)"></div>'''
    if t.get('dir'):
        dl, dt = (ox+ph*t['dfx'], ph*t['dfy']) if 'dfx' in t else (cx+rw*0.2, cy+rh*0.9)
        out += f'<div style="position:absolute;left:{dl}px;top:{dt}px;background:rgba(29,42,35,.85);color:#fff;font-weight:700;font-size:13px;padding:5px 11px;border-radius:999px;white-space:nowrap">{t["dir"]}</div>'
    return out

def wide(src, dst):
    im = Image.open(src).convert('RGB'); a = np.array(im); padl = 342
    p = np.pad(a, ((0,0),(padl,0),(0,0)), mode='edge'); big = Image.fromarray(p)
    blur = big.filter(ImageFilter.GaussianBlur(20))
    m = Image.new('L', big.size, 255); m.paste(0,(padl+30,0,big.size[0],big.size[1])); m = m.filter(ImageFilter.GaussianBlur(18))
    Image.composite(blur, big, m).save(dst, quality=95)

def slides(d, S, w, h, tk):
    k = 1.25 if tk else 1.0; pad = 28 if tk else 22
    pt = 'padding-top:60px;' if tk else ''
    top_h = 250 if tk else 135
    steps = d['steps']
    def photo(top, src, extra=''):
        return f'<div style="position:absolute;left:0;top:{top}px;width:{w}px;height:{w}px"><img src="file://{S}/{src}" style="width:100%;height:100%;object-fit:cover">{extra}</div>'
    def band(top, hh, bg, html):
        return f'<div style="position:absolute;left:0;top:{top}px;width:{w}px;height:{hh}px;background:{bg}">{html}</div>'
    out = []
    # 1 cover
    t1 = f'{logo(True,11*k)}<div style="padding:{pad}px {pad}px 0;{pt}"><span class="badge" style="font-size:{14*k}px;padding:4px 10px">오늘의 1분 운동</span><div style="color:#fff;font-weight:900;font-size:{26*k}px;line-height:1.25;margin-top:{8*k}px">{d["q"]}</div></div>'
    if tk:
        b1 = f'<div style="padding:{pad}px;padding-top:26px;color:#fff;font-weight:900;font-size:{24*k}px;line-height:1.3">{d["name"]} <span style="color:#7ddc93">→</span></div><div style="padding:0 {pad}px;color:#a9c9b6;font-size:{15*k}px">옆으로 넘겨서 따라 해 보세요</div>'
        out.append(page(w,h, band(0,top_h,'#1d3a2c',t1) + photo(top_h,'action.png') + band(top_h+w,h-top_h-w,'#1d3a2c',b1)))
    else:
        ov = f'<div style="position:absolute;left:0;right:0;bottom:0;padding:40px {pad}px 16px;background:linear-gradient(rgba(29,58,44,0),rgba(29,58,44,.92));color:#fff;font-weight:900;font-size:22px">{d["name"]} <span style="color:#7ddc93">→</span></div>'
        out.append(page(w,h, band(0,top_h,'#1d3a2c',t1) + photo(top_h,'action.png',ov)))
    # 2 muscle
    msz = 30 if len(d['muscle']) < 5 else 27
    t2 = f'{logo(False,11*k)}<div style="padding:{pad}px;{pt}"><span class="badge" style="font-size:{14*k}px;padding:4px 10px">운동 부위</span><div style="font-weight:900;font-size:{msz*k}px;margin-top:{6*k}px">{d["muscle"]}</div><div style="font-size:{14*k}px;color:#4c5a52;margin-top:2px;line-height:1.45">{d["mdesc"]}</div></div>'
    if tk:
        b2 = f'<div style="padding:{pad}px;font-size:{16*k}px;line-height:1.6;color:#33443b">{d["mlong"]}</div>'
        out.append(page(w,h, band(0,top_h,'#f4f6f3',t2) + photo(top_h,'muscle.png') + band(top_h+w,h-top_h-w,'#f4f6f3',b2)))
    else:
        out.append(page(w,h, band(0,top_h+20,'#f4f6f3',t2) + photo(top_h+20,'muscle.png')))
    # 3 causes
    if d.get('causes'):
        rows=''.join(f'<div style="display:flex;gap:{14*k}px;align-items:center;background:#fff;border-radius:14px;padding:{14*k}px {16*k}px;margin-top:{12*k}px"><div style="font-size:{30*k}px">{e}</div><div><div style="font-weight:900;font-size:{18*k}px">{a}</div><div style="font-size:{14.5*k}px;color:#4c5a52;margin-top:2px">{b}</div></div></div>' for e,a,b in d['causes'])
        f3 = f'''<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 {pad+8}px;background:#f4f6f3">
<span class="badge" style="align-self:flex-start;font-size:{14*k}px;padding:4px 10px">주된 원인</span>
<div style="font-weight:900;font-size:{25*k}px;line-height:1.3;margin-top:{8*k}px">{d["muscle"]}이<br>이럴 때 {d.get("cverb","굳기")} 쉬워요</div>{rows}
<div style="font-size:{13.5*k}px;color:#4c5a52;margin-top:{16*k}px;line-height:1.6">내 생활습관에 해당된다면<br>오늘의 1분 운동으로 {d.get("cend","풀어")} 주세요 👇</div></div>{logo(False,11*k)}'''
        out.append(page(w,h,f3,'#f4f6f3'))
    # 3,4 steps
    for lbl, title, items, st, src in [('STEP 1~2','시작 자세',steps[:2],1,'start'),('STEP 3~5','따라 하기',steps[2:],3,'action')]:
        if tk:
            th = f'{logo(False,11*k)}<div style="padding:{pad}px;{pt}"><span class="badge" style="font-size:{13*k}px;padding:4px 10px">{lbl}</span><div style="font-weight:900;font-size:{25*k}px;margin-top:{6*k}px">{title}</div></div>'
            bb = f'<div style="padding:{pad-6}px {pad}px">{step_rows(items, st, 17*k, 8*k)}</div>'
            out.append(page(w,h, band(0,top_h,'#f4f6f3',th) + photo(top_h,src+'.png') + band(top_h+w,h-top_h-w,'#f4f6f3',bb)))
        else:
            thh = 70 + 39*len(items); ph = h - thh
            th = f'{logo(False,11)}<div style="padding:18px 22px 0"><span class="badge" style="font-size:13px;padding:4px 10px">{lbl}</span><span style="font-weight:900;font-size:23px;margin-left:8px;vertical-align:middle">{title}</span><div style="margin-top:6px">{step_rows(items, st, 16, 7)}</div></div>'
            marks = target_marks(d.get('target'), w-ph, ph) if src=='action' else ''
            img = f'<div style="position:absolute;left:0;top:{thh}px;width:{w}px;height:{ph}px;overflow:hidden"><img src="file://{S}/{src}_wide.jpg" style="position:absolute;right:0;top:0;height:{ph}px">{marks}</div>'
            out.append(page(w,h, band(0,thh,'#f4f6f3',th) + img))
    # 5 amount
    f5 = f'''{logo(False,11*k)}<div style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:0 {pad+8}px;background:#f4f6f3">
<span class="badge" style="align-self:flex-start;font-size:{14*k}px;padding:4px 10px">운동량</span>
<div style="font-weight:900;color:#2e7d5a;font-size:{46*k}px;line-height:1.15;margin-top:{10*k}px">{d["amount"]}</div>
<div style="font-size:{15*k}px;color:#4c5a52;margin-top:{8*k}px">{d["sub"]}</div>
<div style="background:#fff;border-radius:14px;padding:{14*k}px {16*k}px;margin-top:{24*k}px;font-size:{15*k}px;line-height:1.75">
<div style="font-weight:900;color:#c0582c;margin-bottom:4px">⚠️ 이것만 지켜 주세요</div>
· {d["c1"]}<br>{("· "+d["c2"]+"<br>") if d.get("c2") else ""}· 반동 없이 천천히, 숨은 편하게<br>· 저리거나 불편하면 바로 멈추기</div></div>{logo(False,11*k)}'''
    out.append(page(w,h,f5,'#f4f6f3'))
    # 6 shop
    f6 = f'''<div style="position:absolute;inset:0;background:#1d3a2c;color:#fff;display:flex;flex-direction:column;justify-content:center;padding:0 {pad+8}px">
<div style="font-size:{40*k}px">📌</div>
<div style="font-weight:900;font-size:{27*k}px;line-height:1.3;margin-top:4px">저장해 두고<br>매일 1분만 해 보세요!</div>
<div style="height:1px;background:rgba(255,255,255,.2);margin:{20*k}px 0"></div>
<div style="font-weight:900;font-size:{19*k}px">인베뉴 스튜디오 <span style="font-weight:500;font-size:{14*k}px;color:#a9c9b6">울산 남구 · 1:1 전신케어</span></div>
<div style="font-size:{14.5*k}px;line-height:1.75;margin-top:{8*k}px;color:#dfece4">풀고 → 깨우고 → 강화하는 1:1 전신케어<br>당근 단골 <b style="color:#7ddc93">2,146명</b> · 평점 <b style="color:#7ddc93">4.9</b><br>첫 방문 모든 관리 <b style="color:#7ddc93">30% 할인</b></div>
<div style="align-self:flex-start;margin-top:{18*k}px;background:#7ddc93;color:#12271c;font-weight:900;font-size:{16*k}px;padding:{9*k}px {16*k}px;border-radius:10px">예약은 프로필 링크에서 👆</div>
<div class="logo" style="right:18px;bottom:16px;font-size:{11*k}px;opacity:.85">INVENUE STUDIO</div></div>'''
    out.append(page(w,h,f6))
    return out

async def main(nums):
    async with async_playwright() as p:
        b = await p.chromium.launch(); pg = await b.new_page(device_scale_factor=2)
        for n in nums:
            S = f'{ROOT}/{n}'; d = EP[n]
            for s in ['start','action']: wide(f'{S}/{s}.png', f'{S}/{s}_wide.jpg')
            for kind, (w,h,tk) in {'insta':(540,675,False),'tiktok':(540,960,True)}.items():
                os.makedirs(f'{S}/{kind}', exist_ok=True)
                for i, html in enumerate(slides(d,S,w,h,tk),1):
                    fn = f'{S}/{kind}/{i}.html'; open(fn,'w').write(html)
                    await pg.set_viewport_size({'width':w,'height':h}); await pg.goto('file://'+fn)
                    await pg.wait_for_timeout(200)
                    await pg.screenshot(path=f'{S}/{kind}/{i}.jpg', type='jpeg', quality=93); os.remove(fn)
            print('rendered', n)
        await b.close()
asyncio.run(main([int(x) for x in sys.argv[1:]]))
