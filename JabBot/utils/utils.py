import discord
import os
import json
import random
from bs4 import BeautifulSoup
from selenium import webdriver

from settings import (DATA_DIR, PREFIX, VOWELS, JOKES, SLICKDEALS_HOMEPAGE,
    DEALSTATE_JSON, JABHAX_ICON, WORDS_DICTIONARY)


EMPTY = discord.Embed.Empty
async def notify_user(member, msg):
    if member:
        dm_ch = (member.dm_channel if member.dm_channel else
                 await member.create_dm())
        await dm_ch.send(msg)
    else:
        print('Could not notify user')

# Embed
def embedded(title=EMPTY, desc=EMPTY, author=EMPTY, fields=EMPTY,
             thumbnail=EMPTY, image=EMPTY, inline=None, color=0x00ff00, attachments=None,
             footer_text='JabBot Embedding', footer_icon=JABHAX_ICON):
    e = discord.Embed(color=color)
    if title: e.title = title
    if desc: e.description = desc
    if author: e.set_author(name=author)
    if fields:
        for f in fields:
            if inline:
                e.add_field(name=f['name'], value=f['value'], inline=inline)
            else:
                e.add_field(name=f['name'], value=f['value'], inline=f['inline'])
    if thumbnail: e.set_thumbnail(url=thumbnail)
    if image: e.set_image(url=image)
    if attachments:
        e.attach_files(attachments)
    e.set_footer(text=footer_text, icon_url=footer_icon)
    return e

def create_fields(names=[], values=[], inlines=[]):
    n, v, inl = len(names), len(values), len(inlines)
    if n != v:
        raise ValueError('Must have correct number of fields and values')
    fields = []
    for i in range(len(names)):
        fields.append(create_field(names[i], values[i], inlines[i]))
    return fields

def create_field(n='FieldName', v='FieldDesc', i=False):
    return {'name': n, 'value': v, 'inline': i}

def parse_embed_user_params(ctx, args):
    params = {
        'title': None, 'desc': None, 'fields': None, 'global_inline': None,
        'thumbnail': ctx.author.avatar_url,
    }
    print(f'thumbnail: {params["thumbnail"]}')
    if len(args) >= 1:
        params['title'] = args[0]
        if len(args) >= 2:
            params['desc'] = args[1]
        if len(args) > 2:
            names, values, inlines = [], [], []
            thumb, global_inline = 'thumbnail=', 'inline='
            for i in range(2, len(args)):
                if args[i].startswith(thumb):
                    params['thumbnail'] = args[i][len(thumb):]
                    print(f'thumbnail: {params["thumbnail"]}')
                elif args[i].startswith(global_inline):
                    params['global_inline'] = bool(args[i][len(global_inline):])
                    print(f'global_inline: {params["global_inline"]}')
                elif i % 2 == 0:
                    names.append(args[i])
                else:
                    values.append(args[i])
                inlines.append(False)
            params['fields'] = create_fields(names, values, inlines)
    return params

def get_words_dict():
    words_dict = {}
    with open(WORDS_DICTIONARY, 'r') as words_file:
        words_dict = json.load(words_file)
    return words_dict

# Slickdeals Functions
def get_dealstate():
    deals = {}
    with open(DEALSTATE_JSON, 'r') as deals_file:
        deals = json.load(deals_file)
    return deals

def set_dealstate(state):
    with open(DEALSTATE_JSON, 'w') as outfile:
        outfile.write(json.dumps(state))

def deal_format(deal):
    return (f'Item: {deal["url"]}\n'
            f'{"":4}- Title: {deal["title"]}\n'
            f'{"":4}- Store: {deal["store"]}\n'
            f'{"":4}- Price: {deal["price"]}\n'
            f'{"":4}- Image: {deal["image"]}\n'
            f'{"":4}- Status: {deal["status"]}\n\n')

def get_soup(url):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    browser.get(url)
    html = browser.page_source
    return BeautifulSoup(html, 'lxml')

def parse_featured_deal(item):
    deal = {
        'title': '', 'store': '', 'price': '', 'url': '', 'image': '',
        'status': ''
    }
    url = (item.parent.attrs['data-href']
           if 'data-href' in item.parent.attrs else item.parent.attrs)
    title = item.find('a', {'class': 'itemTitle'})
    store = item.find('span', 'blueprint')
    price = item.parent.find('div', {'class': 'itemPrice'})
    img_container = item.find('div', 'imageContainer', {"src": True})
    img_loading = item.find('img', {'class': 'loading'}, {"src": True})
    img = img_loading if img_loading else item.find('img', {"src": True})
    new = item.find('span', 'new')
    # build the deal item dict
    deal['title'] = title.text.strip() if title else 'No Title'
    deal['store'] = store.text.strip() if store else 'No Store'
    deal['price'] = price.text.strip() if price else 'No Price'
    deal['url'] = str(url) if url else 'No Url'
    deal['image'] = (f'{SLICKDEALS_HOMEPAGE}{img["src"]}'if img
                     else img_container)
    deal['status'] = new.text.strip() if new else 'OLD'
    # conver price and status array into string with space delimiter
    deal['price'] = " ".join(deal["price"].split())
    deal['status'] = "".join(deal["status"].split())
    return deal

# Yomamma Jokes
def get_random_joke():
    no_joke = 'I got no YoMama jokes right now. Please try again later.'
    with open(JOKES, 'r') as jokes_file:
        jokes = json.load(jokes_file)
        random_category = random.choice(list(jokes.keys()))
        joke = (no_joke if random_category not in jokes else
                no_joke if len(jokes[random_category]) < 1 else
                random.choice(list(jokes[random_category])))
        print(joke)
    return joke

# Creating a custom command
def create_cmd_ref(key, reply='', desc='', brief=''):
    return { 'key': key, 'reply': reply, 'desc': desc, 'brief': brief }

# Mention the message author and tag them
def mention(author):
    return '<@' + str(author.id) + '>'

# helper function for OWO text converter
def last_replace(s, old, new):
    li = s.rsplit(old, 1)
    return new.join(li)

def text_to_owo(text):
    """ Converts your text to OwO """
    smileys = [';;w;;', '^w^', '>w<', 'UwU', '(・`ω\´・)', '(´・ω・\`)']
    text = text.replace('L', 'W').replace('l', 'w')
    text = text.replace('R', 'W').replace('r', 'w')
    text = last_replace(text, '!', '! {}'.format(random.choice(smileys)))
    text = last_replace(text, '?', '? owo')
    text = last_replace(text, '.', '. {}'.format(random.choice(smileys)))
    for v in VOWELS:
        if 'n{}'.format(v) in text:
            text = text.replace('n{}'.format(v), 'ny{}'.format(v))
        if 'N{}'.format(v) in text:
            text = text.replace('N{}'.format(v), 'N{}{}'.format('Y' if v.isupper() else 'y', v))
    return text
