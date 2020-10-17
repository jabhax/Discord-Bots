import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFilter, ImageSequence
from io import BytesIO

from settings import PREFIX, BATTLE_BG_PATH, TRANSPARENT
from pokemon.model import Pokedex


names = ['img{:02d}.gif'.format(i) for i in range(20)]


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
        pk1, pk2 = self.dex.get_pokemon(pk1name), self.dex.get_pokemon(pk2name)
        pk1_f, pk1_b = pk1.sprites['battle_front'], pk1.sprites['battle_back']
        pk2_f, pk2_b = pk2.sprites['battle_front'], pk2.sprites['battle_back']
        bg_im_orig, im1, im2 = BytesIO(), BytesIO(), BytesIO()
        bg_im_orig, im1, im2 = Image.open(BATTLE_BG_PATH), Image.open(pk1_f), Image.open(pk2_b)
        transparent_fg =  Image.open(TRANSPARENT)
        background = BytesIO()

        pk1_frames = []
        for frame in ImageSequence.Iterator(im1):
            frame = frame.copy()
            frame.paste(transparent_fg, mask=transparent_fg)
            frame.seek(0)
            pk1_frames.append(frame)

        pk1_frames[0].save('pk1_battle.gif', 'GIF', save_all=True, append_images=pk1_frames[1:])
        pk2_frames = []
        for frame in ImageSequence.Iterator(im1):
            frame = frame.copy()
            frame.paste(transparent_fg, mask=transparent_fg)
            pk2_frames.append(frame)
        pk2_frames[0].save('pk2_battle.gif', save_all=True, append_images=pk2_frames[1:])

        all_frames = pk1_frames[1:]+pk2_frames[1:]
        bg_img = bg_im_orig.copy()
        bg_img.paste(im1, (600, 100))
        bg_img.paste(im2, (100, 300))
        bg_img.save(background, 'GIF', save_all=True, append_images=all_frames, duration=100, loop=0)
        background.seek(0)
        background.name = 'swag.gif'
        await ctx.send(file=discord.File(background))

def setup(bot):
    bot.add_cog(ImageManipulation(bot))
