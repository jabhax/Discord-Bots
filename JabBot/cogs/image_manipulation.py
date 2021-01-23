import discord
import time
import multiprocessing
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageSequence
from io import BytesIO

from settings import PREFIX, BATTLE_BG_PATH, TRANSPARENT
from pokemon.model import Pokedex


names = ['img{:02d}.gif'.format(i) for i in range(20)]

def build_frames(pk1_f, pk2_b, frameIndex, bg, return_dict):
    st = time.time()
    background, im1, im2 = Image.open(bg), Image.open(pk1_f), Image.open(pk2_b)
    im1.seek(frameIndex), im2.seek(frameIndex)
    pkmn1, pkmn2 = im1.convert("RGBA"), im2.convert("RGBA")
    imageInMemory = BytesIO()
    new_img = Image.new('RGBA', (800,400), (0, 0, 0, 0))
    new_img.paste(background, (0,0))
    new_img.paste(pkmn1, (600, 100), mask=pkmn1)
    new_img.paste(pkmn2, (100, 300), mask=pkmn2)
    new_img.save(f'/Applications/Discord-Bots/JabBot/data/{imageInMemory}', 'png')
    imageInMemory.name = "/Applications/Discord-Bots/JabBot/data/gifInMemory_" + str(frameIndex) + ".png"
    return_dict['images'].append(Image.open(imageInMemory))
    print(f'Frame {frameIndex} took {time.time()-st}s')
    return return_dict

class ImageManipulation(commands.Cog):
    def __init__(self, bot):
        self._bot = bot
        self.dex = Pokedex(self._bot)

    @commands.command()
    async def gifmeup(self, ctx, *args):
       background = "green"
       color = "red"
       if len(args) > 0: background = args[0]
       if len(args) > 1: color = args[1]

       baseImage = Image.new("RGB", (200, 200), background)
       images, pos = [], 0
       for n in names:
          imageInMemory = BytesIO()
          frame = baseImage.copy()
          draw = ImageDraw.Draw(frame)
          draw.ellipse((pos, pos, 50+pos, 50+pos), color)
          frame.save(imageInMemory, 'png')
          imageInMemory.name = n
          imageInMemory.seek(0)
          images.append(Image.open(imageInMemory))
          pos += 10

       gifInMemory = BytesIO()
       images[0].save(gifInMemory, 'gif', save_all=True,
                      append_images=images[1:], duration=100, loop=0)
       gifInMemory.seek(0)
       gifInMemory.name = 'swag.gif'
       await ctx.send(file=discord.File(gifInMemory))

    @commands.command()
    async def battle(self, ctx, pk1name: str='charizard', pk2name: str='blastoise'):
        st = time.time()
        pk1, pk2 = self.dex.get_pokemon(pk1name), self.dex.get_pokemon(pk2name)
        pk1_f = pk1.sprites['battle_front']
        pk2_b = pk2.sprites['battle_back']
        print(f'Getting pokemon took {time.time()-st}s')

        st = time.time()
        background, im1, im2 = Image.open(BATTLE_BG_PATH), Image.open(pk1_f), Image.open(pk2_b)
        print(f'Initial Image.open() for pokemon took {time.time()-st}s')
        st = time.time()
        procs, images, length = [], [], min(im1.n_frames, im2.n_frames)
        self.return_dict = {'images': []}
        for frameIndex in range(0, length):
            p = multiprocessing.Process(
                target=build_frames,
                args=(pk1_f, pk2_b, frameIndex, BATTLE_BG_PATH, self.return_dict))
            procs.append(p)
            p.start()
        for p in procs: p.join()
        images = self.return_dict['images']
        for v in self.return_dict.values(): print(f'v: {v}')

        # for frameIndex in range(0, length):
        #     fst = time.time()
        #     im1.seek(frameIndex), im2.seek(frameIndex)
        #     pkmn1, pkmn2 = im1.convert("RGBA"), im2.convert("RGBA")
        #     imageInMemory = BytesIO()
        #     new_img = Image.new('RGBA', (800,400), (0, 0, 0, 0))
        #     new_img.paste(background, (0,0))
        #     new_img.paste(pkmn1, (600, 100), mask=pkmn1)
        #     new_img.paste(pkmn2, (100, 300), mask=pkmn2)
        #     new_img.save(imageInMemory, 'png')
        #     imageInMemory.name = "gifInMemory_" + str(frameIndex) + ".png"
        #     images.append(Image.open(imageInMemory))
        #     print(f'Frame {frameIndex} took {time.time()-fst}s')
        print(f'Proccessing {length} frames took {time.time()-st}s')

        st = time.time()
        gifInMemory = BytesIO()
        images[0].save(gifInMemory, "gif", save_all=True, optimize=True,
                       loop=0, duration=20, append_images=images[1:])
        gifInMemory.name = "battle.gif"
        gifInMemory.seek(0)
        print(f'Saving took {time.time()-st}s')

        st = time.time()
        await ctx.send(file=discord.File(gifInMemory))
        print(f'sending took {time.time()-st}s')


def setup(bot):
    bot.add_cog(ImageManipulation(bot))
