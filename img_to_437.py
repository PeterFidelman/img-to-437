import sys
from PIL import Image

def bail(message):
    print(message, file=sys.stderr)
    exit()

try:
    img = Image.open(sys.argv[1])
except:
    bail("""
Convert a monochrome image to display in a codepage 437 terminal.
Black pixels become blanks, any other color becomes a mark.

python3 img_to_437.py [filename.png] > filename.txt

Output bytes are written to stdout, errors to stderr.
""")

codes437 = list()
(xdim, ydim) = img.size

if xdim > 80 or ydim > 50:
    bail("Error: Image size is too big for a standard screen")

if ydim & 1 == 1:
    bail("Error: Image height is not divisible by two")

for y in range(0, ydim, 2):
    for x in range(xdim):
        top_pixel = 0 if img.getpixel((x, y)) == (0, 0, 0) else 1
        bot_pixel = 0 if img.getpixel((x, y+1)) == (0, 0, 0) else 1
        selector = (top_pixel << 1) | bot_pixel
        codes437.append((32, 220, 223, 219)[selector])
    # lines that are exactly 80 columns wide will wrap automatically, but
    # shorter lines must be manually wrapped.
    if (xdim < 80):
        codes437.append(13)
        codes437.append(10)

sys.stdout.buffer.write(bytes(codes437))
