"""Draw the original A05 review fixture. Dev-only dependency: Pillow; no media service."""
from pathlib import Path
import argparse, random
from PIL import Image, ImageDraw

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output', required=True, type=Path, help='new PNG path inside an authorized test workspace')
args = parser.parse_args()
if args.output.exists():
    parser.error('output already exists; choose a new path')
args.output.parent.mkdir(parents=True, exist_ok=True)
rng = random.Random(230923)
im = Image.new('RGB', (960, 720), (102, 102, 102))
d = ImageDraw.Draw(im)
d.rectangle((0, 575, 959, 719), fill=(65,65,65))
d.line((0,575,959,575), fill=(38,38,38), width=4)
# Low seated subject, long bench and open wall are intentional.
d.rectangle((190,561,650,577),fill=(49,49,49))
d.rectangle((212,577,222,657),fill=(34,34,34))
d.rectangle((617,577,627,657),fill=(34,34,34))
d.ellipse((290,447,334,491),fill=(147,147,147))
d.polygon([(293,488),(332,488),(346,558),(288,562)],fill=(79,79,79))
d.line((309,558,350,579,366,642),fill=(82,82,82),width=17)
d.line((333,555,380,571,404,632),fill=(82,82,82),width=15)
d.line((367,645,397,645),fill=(40,40,40),width=10)
d.line((402,635,430,635),fill=(40,40,40),width=10)
# Isolated high-contrast sign at the upper-right competes with the subject.
d.rectangle((730,115,916,228),fill=(246,246,246))
for y in [138,166,194]:
    for x in range(750,896,24):
        d.rectangle((x,y,x+12,y+11),fill=(22,22,22))
pixels=im.load()
for y in range(im.height):
    for x in range(im.width):
        noise=rng.randint(-12,12)
        v=max(0,min(255,pixels[x,y][0]+noise))
        pixels[x,y]=(v,v,v)
im.save(args.output)
print(args.output)
