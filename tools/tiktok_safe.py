"""인스타 4:5(1080x1350) 사진을 틱톡 9:16(1080x1920) 가운데에 놓고 위아래를 가장자리 색으로 채움.
틱톡 사진 게시물이 위아래를 잘라도 글자·사진이 잘리지 않게 하기 위함."""
import sys, os
from PIL import Image
def make(insta_dir, tiktok_dir):
    os.makedirs(tiktok_dir, exist_ok=True)
    import glob
    n = len(glob.glob(f'{insta_dir}/*.jpg'))
    for i in range(1, n+1):
        im = Image.open(f'{insta_dir}/{i}.jpg').convert('RGB')
        W, H = im.size
        top = im.getpixel((W//2, 2)); bot = im.getpixel((W//2, H-3))
        c = Image.new('RGB', (1080, 1920), bot if i == 1 else top)  # 1장(전후 대비 표지)은 아래 진녹색으로 채움
        pass  # 위아래 모두 위쪽 띠 색으로 통일
        c.paste(im, (0, (1920-H)//2))
        c.save(f'{tiktok_dir}/{i}.jpg', quality=93)
if __name__ == '__main__':
    for d in sys.argv[1:]:
        make(f'{d}/insta', f'{d}/tiktok'); print('tiktok safe', d)
