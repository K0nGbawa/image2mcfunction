import json

import tqdm
from PIL import Image
from tkinter.filedialog import askopenfilename, asksaveasfilename

with open('color.json', 'r') as f:
    colors = json.load(f)
    keys = tuple(colors.keys())
    values = tuple(colors.values())

def calc(r, g, b):
    return [(r - i[0])**2 + (g - i[1])**2 + (b - i[2])**2 for i in values]

def get_block(r, g, b):
    var = calc(r, g, b)
    return keys[var.index(min(var))]

def img2mcfunction(image: Image.Image, pos: tuple[int, int, int]):
    commands = []
    if image.height > 512:
        image = image.resize((512, int(image.height*512/image.width)))
    if image.mode != 'RGB':
        temp = Image.new('RGB', image.size, (0, 0, 0))
        temp.paste(image)
        image = temp
    for i in tqdm.tqdm(range(image.width)):
        for j in range(image.height):
            color = image.getpixel((i, j))
            block = get_block(*color)
            commands.append(f'setblock {pos[0]+i} {pos[1]} {pos[2]+j} {block}')
    return commands


if __name__ == '__main__':
    path = askopenfilename()
    img = Image.open(path)
    with open('img.txt', 'w') as f:
        f.write('\n'.join(img2mcfunction(img, tuple([int(i) for i in input().split(' ')]))))