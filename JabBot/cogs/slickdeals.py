import discord
from discord.ext import commands

from settings import PREFIX, SLICKDEALS_HOMEPAGE
from utils.utils import (get_soup, get_dealstate, set_dealstate, deal_format,
    parse_featured_deal)
from utils.roles import ADMIN_ROLE


class SlickDeals(commands.Cog):
    def __init__(self, bot):
        self._bot = bot

    @commands.command()
    @commands.has_role(ADMIN_ROLE)
    async def slick(self, ctx):
        '''
        Scrap slick deals Frontpage
        Description:
            Watches and scrapes the https://slickdeals.net frontpage.
        CRITICAL NOTE:
            This command is being worked on... Do not try run, it will
            spam the channel with uneccessary slickdeals.net frontpage
            items.
        Usage:
            [PREFIX]slick
        '''
        soup = get_soup(SLICKDEALS_HOMEPAGE)
        frontpage_grid = soup.find('ul', 'dealTiles gridDeals')
        frontpage_grid_item = frontpage_grid.find('li', 'frontpage')
        fp_item = frontpage_grid_item.find('div', 'fpItem')
        fp_item = fp_item.findChild()
        itemImageAndNames = fp_item.findChildren('div', 'itemImageAndName')
        featured_deals, logs = [], ''
        DEAL_STATE = get_dealstate()
        for item in itemImageAndNames:
            deal = parse_featured_deal(item)
            if deal['url'] in DEAL_STATE:
                DEAL_STATE[deal['url']]['status'] = 'OLD'
            else:
                DEAL_STATE[deal['url']] = deal
            logs += deal_format(deal)
        print(logs)
        async with ctx.channel.typing():
            i, new_i = 1, 1
            for deal_url in DEAL_STATE.keys():
                reply = (f'{SLICKDEALS_HOMEPAGE}{deal_url}'
                         if deal_url.startswith('/f') else deal_url)
                if DEAL_STATE[deal_url]['status'] == 'OLD':
                    reply = f'{i}.  {DEAL_STATE[deal["url"]]["status"]} DEAL: {reply}'
                    print(reply)
                elif DEAL_STATE[deal_url]['status'] == 'NEW':
                    await ctx.send(f'New Deal Item ({new_i}) ({i}).  {reply}')
                    new_i += 1
                i += 1
        set_dealstate(DEAL_STATE)

def setup(bot):
    bot.add_cog(SlickDeals(bot))
