import io
import random
import discord
import time
import pokebase as pb

from .pokemon import Pokemon
from settings import (PK_DATA_PATH, PK_JSON, DEX_ID_TO_NAME_JSON, NAME_TO_DEX_ID_JSON,
                      PKMN_BALLS_DIR, POKEBALLHD_PATH, PKMN_TYPES_DIR, PKMN_POKEMON_DIR,
                      PKMN_SPRITE_BATTLE_FRONT_NORMAL,
                      PKMN_SPRITE_BATTLE_FRONT_SHINY,
                      PKMN_SPRITE_BATTLE_BACK_NORMAL,
                      PKMN_SPRITE_BATTLE_BACK_SHINY,
                      PKMN_SPRITE_ARTWORK, PKMN_SPRITE_MENU,
                      ABILITY_NORMAL_PATH, ABILITY_HIDDEN_PATH, write_resource)
from utils.utils import embedded, create_field


EMPTY = discord.Embed.Empty
EMPTY_FV = '\u200b'
STAT_NAME = {
    'hp': 'HP',
    'attack': 'ATK',
    'defense': 'DEF',
    'special-attack': 'SP.ATK',
    'special-defense': 'SP.DEF',
    'speed': 'SPEED'
}
# Map of type names to type emoji file paths
TYPE_EMOJIS = {
    "water": f'{PKMN_TYPES_DIR}water.png',
	"fire": f'{PKMN_TYPES_DIR}fire.png',
	"grass": f'{PKMN_TYPES_DIR}grass.png',
	"rock": f'{PKMN_TYPES_DIR}rock.png',
	"electric": f'{PKMN_TYPES_DIR}electric.png',
	"ghost": f'{PKMN_TYPES_DIR}ghost.png',
	"ground": f'{PKMN_TYPES_DIR}ground.png',
	"fairy": f'{PKMN_TYPES_DIR}fairy.png',
	"bug": f'{PKMN_TYPES_DIR}bug.png',
	"poison": f'{PKMN_TYPES_DIR}poison.png',
	"wind": f'{PKMN_TYPES_DIR}wind.png',
	"fighting": f'{PKMN_TYPES_DIR}fighting.png',
	"normal": f'{PKMN_TYPES_DIR}normal.png',
	"ice": f'{PKMN_TYPES_DIR}ice.png',
	"dark": f'{PKMN_TYPES_DIR}dark.png',
	"steel": f'{PKMN_TYPES_DIR}steel.png',
	"psychic": f'{PKMN_TYPES_DIR}psychic.png',
	"flying": f'{PKMN_TYPES_DIR}flying.png',
	"dragon": f'{PKMN_TYPES_DIR}dragon.png'
}
# Path to small egg sprite displayed on Pokedex Egg-Groups field.
EGG_EMOJI_PATH = f'{PKMN_POKEMON_DIR}egg.png'

class Pokedex:
    dex = None
    GEN1 = (1, 151)
    GEN2 = (152, 251)
    GEN3 = (252, 386)
    GEN4 = (387, 493)
    GEN5 = (494, 649)
    GEN6 = (650, 721)
    GEN7 = (722, 809)
    GEN8 = (810, 893)

    def __init__(self,  max_gen=1):
        self.PK_CH = None
        self.max_gen = max_gen
        self.files = []
        self.attachments = []

    def meter_to_feet_inches(self, m):
        # Get  decimal portion (meters / .3048) by using % 1.
        # Then convert to inches by multiplying by 12.
        feet = m / .3048
        inches = (feet % 1) * 12
        return f'{int(feet)}\'{int(inches)}\"'

    def kg_to_lbs(self, kg):
        return f'{round(kg * 2.20462, 2)}lbs'

    def get_pokemon(self, name_or_id):
        ''' This is the main getter method for different Pokemon '''
        if name_or_id is None:
            raise ValueError('Found None Type for pk')
        is_in_json, nameid = self.check_in_json(name_or_id)
        if is_in_json:
            return Pokemon(PK_JSON[nameid])
        try:
            print('Not in JSON. Need to get Pokebase API ...')
            id = int(self.convert_name_to_id(name_or_id))
            pkmn = self.convert_pkbase_to_json(self.get_pokebase_pokemon(id))
            pkmn = Pokemon(pkmn)
        except:
            raise Exception(f'Failed to get {name_or_id} from Pokebase API.')
        print(f'pkmn from get_pokemon: {pkmn}')
        return pkmn

    def get_pokebase_pokemon(self, name_or_id):
        ''' Attempts to retrieve a pokemon from the Pokebase API Resource '''
        if name_or_id in DEX_ID_TO_NAME_JSON:
            id = int(self.convert_name_to_id(name_or_id))
            pkmn = pb.pokemon(id)
            msg = f'Pulled {pkmn.name} from PokebaseAPI (id in DEX_ID_TO_NAME_JSON)'
        elif str(name_or_id).isnumeric():
            id = int(name_or_id)
            pkmn = pb.pokemon(id)
            msg = f'Pulled {pkmn.name} from PokebaseAPI (is Numeric)'
        elif name_or_id in NAME_TO_DEX_ID_JSON:
            id = int(self.convert_name_to_id(name_or_id))
            pkmn = pb.pokemon(id)
            msg = f'Pulled {pkmn.name} from PokebaseAPI (name in NAME_TO_DEX_ID_JSON)'
        else:
            name = self.clean_name(name_or_id)
            id = int(self.convert_name_to_id(name))
            pkmn = pb.pokemon(id)
            msg = f'Pulled {pkmn.name} from PokebaseAPI.pokemon (convert clean name)'
        print(f'Msg: {msg} -- Type: {type(pkmn)}')
        return pkmn

    def check_in_json(self, name):
        name = str(name).lower()
        if name in PK_JSON:
            return True, name
        if name in NAME_TO_DEX_ID_JSON:
            if name in PK_JSON:
                return True, name
        if name in DEX_ID_TO_NAME_JSON:
            name = self.convert_id_to_name(name)
            if name in PK_JSON:
                return True, name
        if type(name) is discord.Emoji:
            in_json, name = self.check_in_json(name.name)
            return in_json, name
        return False, name

    def convert_pkbase_to_json(self, pkmn):
        print(f'converting pkmn of type ({type(pkmn)})\npkmn: {pkmn.id} to a JSON')
        evos = self.get_evolution_line(pkmn)
        # if len(evos) == 1: evo_line = [evos[0][0]]

        evo_line = [p[0] for p in evos]
        prev, next = self.get_prev_next_id_name(pkmn.id)
        pk_json = {
            'name': self.convert_id_to_name(pkmn.name),
            'id': pkmn.id,
            'sprites': {
                'artwork': f'{PKMN_SPRITE_ARTWORK}{pkmn.id}.png',
                'battle_front': f'{PKMN_SPRITE_BATTLE_FRONT_NORMAL}{pkmn.id}.gif',
                'battle_back': f'{PKMN_SPRITE_BATTLE_BACK_NORMAL}{pkmn.id}.gif',
                'battle_front_shiny': f'{PKMN_SPRITE_BATTLE_FRONT_SHINY}{pkmn.id}.gif',
                'battle_back_shiny': f'{PKMN_SPRITE_BATTLE_BACK_SHINY}{pkmn.id}.gif',
                'menu': f'{PKMN_SPRITE_MENU}{pkmn.id}.gif'
            },
            'prev_dex_pk': prev,
            'next_dex_pk': next,
            'height': pkmn.height,
            'weight': pkmn.weight,
            'base_exp': pkmn.base_experience,
            'exp_growth': pkmn.species.growth_rate.name.capitalize(),
            'capture_rate': pkmn.species.capture_rate,
            'base_happiness': pkmn.species.base_happiness,
            'base_stats': [int(s.base_stat) for s in pkmn.stats],
            'abilities': [str(a.ability.name) for a in pkmn.abilities],
            'genders': self.get_gender_rates(pkmn),
            'egg_groups': '\n'.join([g.name.capitalize() for g in pkmn.species.egg_groups]),
            'classification': self.get_classification_genera(pkmn),
            'entry_text': self.get_dex_entry_text(pkmn),
            'types': self.get_types(pkmn),
            'evs_earned': self.get_pokebase_evs_earned(pkmn),
            'evo_line': evos
        }
        self.update_pk_json(pk_json)
        return pk_json

    def update_pk_json(self, pkj):
        PK_JSON[pkj['name']] = pkj
        try:
            pk = Pokemon(PK_JSON[pkj['name']])
            write_resource(PK_DATA_PATH, PK_JSON, write_ops='w')
            print(f'***** UPDATED PK_JSON: {pk.name} *****')
        except:
            err = 'Update failed. Failed to convert PK JSON to Pokemon object.'
            raise Exception(err)

    def convert_pokemon_obj_to_json(self, pkmn):
        pk_json = {}
        pk_json['name'] = pkmn.name
        pk_json['id'] = pkmn.id
        pk_json['sprites'] = pkmn.sprites
        pk_json['height'] = pkmn.height
        pk_json['weight'] = pkmn.weight
        pk_json['base_exp'] = pkmn.base_exp
        pk_json['exp_growth'] = pkmn.exp_growth
        pk_json['capture_rate'] = pkmn.capture_rate
        pk_json['base_happiness'] = pkmn.base_happiness
        pk_json['base_stats'] = pkmn.base_stats_list
        pk_json['abilities'] = pkmn.abilities_list
        pk_json['genders'] = pkmn.genders_list
        pk_json['egg_groups'] = pkmn.egg_groups
        pk_json['classification'] = pkmn.classification
        pk_json['entry_text'] = pkmn.dex_entry
        pk_json['types'] = pkmn.types
        pk_json['evs_earned'] = pkmn.evs_earned
        pk_json['evo_line'] = pkmn.evo_line
        pk_json['prev_dex_pk'] = pkmn.prv
        pk_json['next_dex_pk'] = pkmn.nxt
        return pk_json

    def get_dex_entry_text(self, pkmn):
        '''
        Gets the dex entry description text of a pokemon from either a
        Pokebase API Resource or a Pokemon object.

        This is currently being randomly selected from the EN language pool of
        the pokemon's history of dex entries across all games, versions, and
        languages.
        '''
        try:
            return pkmn.dex_entry
        except:
            entries = []
            for entry in pkmn.species.flavor_text_entries:
                if entry.language.name == 'en': entries.append(entry)
            entry = random.choice(entries)
            text = entry.flavor_text.replace('\n', '')
            return f'{text}  ~ Pokemon {entry.version.name.upper()}'

    def get_classification_genera(self, pkmn):
        '''
        Gets the genus from the genera of a pokemon from Pokebase API.
        The genera of a pokemon is the classification of that pokemon.

        For example, Charizard is classififed as a Flame Pokemon, etc. It is not
        simply the elemental type or the species type of the pokemon, but
        some combination of both as an extra abstraction. It is also just
        details you would see in a pokedex entry rather than the wider gameplay.
        '''
        for g in pkmn.species.genera:
            if g.language.name == 'en': return g.genus
        return '*No Genera Found*'

    def get_gender_rates(self, pkmn):
        '''
        Gets the gender rates from the Pokebase API and converts them into
        proper ratios. Returns a list of size 2, where the left element
        represents the female ratio and the right element, the male ratio.
        '''
        if type(pkmn) is Pokemon:
            return Pokemon.genders
        female_rate = round(float(pkmn.species.gender_rate / 8), 3)
        male_rate = round(1-female_rate, 3)
        if female_rate < 0 and female_rate: return [None, None]
        return [male_rate, female_rate]  # [male, female]

    def get_types(self, pkmn):
        types = []
        for tslot in pkmn.types:
            types.append(tslot.type.name.title().lower())
        return types

    def get_evolution_line(self, pkmn):
        '''
        Gets the the evolutionary line of a pokemon from either a Pokebase API
        Resource or a Pokemon object.

        Returns a list containing the names in sorted order, with respect to the
        evolutionary line order.
        '''
        if type(pkmn) is Pokemon:
            print('is_POKEMON_not_PKBASE')
            pkmn_list = [name for name in pkmn.evo_line]
        else:
            try:
                pkmn_list, evo_chain = [], pkmn.species.evolution_chain.chain.evolves_to
                basic_name = pkmn.species.evolution_chain.chain.species.name.lower()
                pkmn_list.append(basic_name)
                if len(evo_chain) > 0:
                    stage2_name = evo_chain[0].species.name.lower()
                    pkmn_list.append(stage2_name)
                    if len(evo_chain[0].evolves_to) > 0:
                        stage3_name = evo_chain[0].evolves_to[0].species.name.lower()
                        pkmn_list.append(stage3_name)
            except:
                err = (f'Species not in {type(pkmn)}\n__dict__(pkmn):\n'
                       f'{pkmn.__dict__}\nstr(pkmn): {str(pkmn)}')
                raise Exception(err)
        result = []
        for pk in pkmn_list:
            if self.check_in_json(pk):
                result.append((self.convert_name_to_id(pk), pk.lower()))
            else:
                raise Exception(f'No key {pk} in NAME_TO_DEX_ID')
        return result

    def get_tiny_spr(self, id):
        '''
        Gets a pokemon's sprite emoji based on their Pokedex-IDs.
        Calls get_custom_emoji()
        '''
        id = self.convert_name_to_id(id)
        if id in NAME_TO_DEX_ID_JSON:
            id = self.convert_name_to_id(id)
        elif id in DEX_ID_TO_NAME_JSON:
            id = self.convert_name_to_id(DEX_ID_TO_NAME_JSON[id])
        else:
            raise ValueError(f'COULD NOT FIND TINY SPR {id}')
        return f'{PKMN_SPRITE_MENU}{id}.gif'
        # return f'../data/pokemon_data/pokemon/menu/{id}.gif'

    async def get_types_emoji(self, guild, types):
        '''
        Gets a pokemon-type emoji based on the type-name.
        Calls get_custom_emoji()
        '''
        type_emojis = []
        for t in types:
            if type(t) is discord.Emoji:
                type_emojis.append(t)
            else:
                if t in TYPE_EMOJIS:
                    e = await self.get_emoji(guild, t, TYPE_EMOJIS[t])
                    type_emojis.append(e)
                else:
                    err = f'INCOMPATIBLE POKEMON TYPE FOUND: {t} in {types}'
                    raise ValueError(err)
        return type_emojis

    async def get_evoltion_emojis(self, guild, evo_list):
        ''' Gets a pokemon-sprite emoji based on the evolution-line. '''
        evo_emojis = []
        for id, name in evo_list:
            if self.check_in_json(name):
                if id in DEX_ID_TO_NAME_JSON:
                    e = await self.get_emoji(guild, name, self.get_tiny_spr(id))
                    evo_emojis.append(e)
                elif name in NAME_TO_DEX_ID_JSON:
                    id = self.convert_name_to_id(name)
                    e = await self.get_emoji(guild, name, self.get_tiny_spr(id))
                    evo_emojis.append(e)
                else:
                    err = (f'INCOMPATIBLE POKEMON EVOLUTION FOUND: ({id}, {name}) '
                           f'in {evo_list}')
                    raise ValueError(err)
            elif name in NAME_TO_DEX_ID_JSON:
                id = self.convert_name_to_id(name)
                if id in DEX_ID_TO_NAME_JSON:
                    e = await self.get_emoji(guild, name, self.get_tiny_spr(id))
                    evo_emojis.append(e)
                else:
                    err = (f'INCOMPATIBLE POKEMON EVOLUTION FOUND: ({id}, {name}) '
                           f'in {evo_list}')
                    raise ValueError(err)
            elif id in DEX_ID_TO_NAME_JSON:
                e = await self.get_emoji(guild, name, self.get_tiny_spr(id))
                evo_emojis.append(e)
            else:
                err = (f'INCOMPATIBLE POKEMON EVOLUTION FOUND: ({id}, {name}) '
                       f'in {evo_list}')
                raise ValueError(err)
        return evo_emojis

    def get_prev_next_id_name(self, id):
        '''
        Gets the previous and next pokemon on the Pokedex of a given Dex-ID.
        This can be used to get the filename (e.i. <id>.gif or <id>.png) for the
        menu sprites of the previous and/or next pokemon.
            * If the id is out of bounds, it will return the id of the pokemon
              that was passed in as that placeholder value for either previous
              or next.
        '''
        id = self.convert_name_to_id(id)
        p, n = str(int(id)-1), str(int(id)+1)
        print(f'id: {id}')
        if p not in DEX_ID_TO_NAME_JSON:
            if int(p) <= 0: p = id
            else:
                for i in range(int(p), 0, -1):
                    if str(i) in DEX_ID_TO_NAME_JSON:
                        p = str(i)
                        break
                else: p = id
        if n not in DEX_ID_TO_NAME_JSON:
            if int(n) >= 10111: n = id
            else:
                for i in range(int(n), 10112):
                    if str(i) in DEX_ID_TO_NAME_JSON:
                        n = str(i)
                        break
                else: n = id
        prev = (p, self.convert_id_to_name(p))
        next = (n, self.convert_id_to_name(n))
        curr = (id, self.convert_id_to_name(id))
        print(f'prev: {prev[0]}, {prev[1]}\n'
              f'curr: {curr[0]}, {curr[1]}\n'
              f'next: {next[0]}, {next[1]}')
        if prev and next: return (prev[0], prev[1]), (next[0], next[1])
        elif prev: return (prev[0], prev[1]), (curr[0], curr[1])
        elif next: return (curr[0], curr[1]), (next[0], next[1])
        else: raise Exception('SOMETHING BAD HAPPENED....PREV_NEXT_PKMN')

    def get_pokebase_evs_earned(self, pkmn):
        '''
        Gets the EVS-Earned attribute of a pokemon from either a Pokebase API
        Resource or a Pokemon object.

        This is the EV value and amount that other pokemon would get upon
        defeating this current pokemon in a wild battle.
        '''
        evs_earned = ''
        for s in pkmn.stats:
            if int(s.effort) > 0:
                evs_earned += f'{s.effort} {STAT_NAME[s.stat.name]}\n'
        return evs_earned

    async def get_emoji(self, guild, emo_name, emo_path):
        '''
        Gets a custom emoji, primarily used to get sprite emojis:
        Pokemon Menu Sprite, Pokemon Front, Pokemon Front-Shiny, Pokemn Back,
        Pokemon Back-Shiny, Pokemon Artwork.
        '''
        # print(f'emo_name: {emo_name}, emo_path: {emo_path}')
        emo_name = self.clean_name(emo_name)
        animated, statics = [], []
        for e in guild.emojis:
            if emo_name.lower() == e.name.lower():
                print(f'emo_name: {emo_name}, emo_path: {emo_path}')
                return e
            animated.append(e) if e.animated else statics.append(e)
        else:
            print(f'Could not find {emo_name} emoji in guild emojis.')
        try:
            if len(animated) >= 50:
                await self.delete_emojis(guild, animated)
            if len(statics) >= 50:
                await self.delete_emojis(guild, statics)
            with open(emo_path, 'rb') as fd:
                print(f'emo_name: {emo_name}, emo_path: {emo_path}')
                b = bytearray(fd.read())
                # b = io.BytesIO(fd.read())
                # b.seek(0)
                emo = await guild.create_custom_emoji(name=emo_name, image=b)
                print(f'Created {emo.name} Emoji: {emo}')
                return emo
        except:
            err = f'Could not find emoji in {emo_name} with path {emo_path}'
            raise Exception(err)

    async def delete_emojis(self, guild, emoji_list):
        msg_list = []
        for e in emoji_list:
            for ch in guild.text_channels:
                if ch.name != 'admin':
                    msg_list += await ch.history(limit=200).flatten()
            await self.PK_CH.send(f'Clearing emoji {e} from all reactions...')
            for msg in msg_list:
                if len(msg.reactions) > 0:
                    reaction = discord.utils.get(msg.reactions, emoji=e.name)
                    await msg.clear_reaction(e)
            await self.PK_CH.send(f'Deleting {e}')
            await e.delete()

    async def embed_pokemon(self, guild, pk, detailed=True):
        pkmn = self.get_pokemon(pk)
        print(f'type: {type(pkmn)}, pkmn: {pkmn}')
        print(f'Await fields')
        print(f'Await emojis')
        fields = await self.create_pk_fields(guild, pkmn, detailed=detailed)
        artwork_sprite = f'{PKMN_SPRITE_ARTWORK}{pkmn.id}.png'
        battle_front_sprite =  f'{PKMN_SPRITE_BATTLE_FRONT_NORMAL}{pkmn.id}.gif'
        battle_back_sprite = f'{PKMN_SPRITE_BATTLE_BACK_NORMAL}{pkmn.id}.gif'
        battle_front_shiny_sprite = f'{PKMN_SPRITE_BATTLE_FRONT_SHINY}{pkmn.id}.gif'
        battle_back_shiny_sprite = f'{PKMN_SPRITE_BATTLE_BACK_SHINY}{pkmn.id}.gif'
        menu_sprite = f'{PKMN_SPRITE_MENU}{pkmn.id}.gif'
        pkball_emo = await self.get_emoji(guild, 'pokeballhd', POKEBALLHD_PATH)
        pkspr_emo = await self.get_emoji(guild,  pkmn.name, self.get_tiny_spr(pkmn.id))
        print(f'PKMN.ID: {pkmn.id}, {pkmn.name}')
        print(f'PKMN.PRV: {pkmn.prv.id}, {pkmn.prv.name}')
        print(f'PKMN.NXT: {pkmn.nxt.id}, {pkmn.nxt.name}')
        prv_emo = await self.get_emoji(guild, pkmn.prv.name, self.get_tiny_spr(pkmn.prv.id))
        nxt_emo = await self.get_emoji(guild, pkmn.nxt.name, self.get_tiny_spr(pkmn.nxt.id))
        print(f'Await files')
        title = f'{pkball_emo} {pkmn.name.capitalize():4} #{str(pkmn.id).zfill(3)} {pkspr_emo}'
        desc = EMPTY
        self.files, self.attachments = [], []
        self.files.append(discord.File(menu_sprite, filename=f'{pkmn.id}_menu.gif'))
        self.files.append(discord.File(battle_front_sprite, filename=f'{pkmn.id}_front.gif'))
        if detailed:
            desc = pkmn.dex_entry
            self.files.append(discord.File(artwork_sprite, filename=f'{pkmn.id}_artwork.gif'))
            for f in self.files: self.attachments.append(f'attachment://{f.filename}')
            image = self.attachments[2]
        else:
            for f in self.files: self.attachments.append(f'attachment://{f.filename}')
            image = EMPTY
        thumbnail = self.attachments[1]
        print(f'Await embed')
        footer_text = pkmn.stats.base_stats_str
        embed = embedded(
            title=title,
            desc=desc,
            color=0xDC143C,
            image=image,
            thumbnail=thumbnail,
            fields=fields,
            footer_text=footer_text,
            footer_icon=self.attachments[0])
        print(f'Await send')
        return embed, self.files, pkmn, prv_emo, nxt_emo

    async def create_pk_fields(self, guild, pkmn, detailed=True):
        types_emo = await self.get_types_emoji(guild, pkmn.types)
        egg_emo = await self.get_emoji(guild, 'egg', EGG_EMOJI_PATH)
        evo_line_emos = await self.get_evoltion_emojis(guild, pkmn.evo_line)
        genders = (f':male_sign::female_sign:' if pkmn.genders.female else
                   f':transgender_symbol:')
        fields = []
        fields.append(create_field(genders, EMPTY_FV, True))
        fields.append(create_field(' '.join([str(e) for e in types_emo]), EMPTY_FV, True))
        fields.append(create_field(f'EV-Earn ({pkmn.evs_earned})', EMPTY_FV, True))
        if detailed:
            fields.append(create_field(f'Species', pkmn.classification, True))
            lh, lw = len(str(pkmn.height)), len(str(pkmn.weight))
            height = float(f'{str(pkmn.height)[:lh-1]}.{str(pkmn.height)[lh-1:]}')
            weight = float(f'{str(pkmn.weight)[:lw-1]}.{str(pkmn.weight)[lw-1:]}')
            fields.append(create_field(f'📏 ({self.meter_to_feet_inches(height):4})', EMPTY_FV, True))
            fields.append(create_field(f'🏋 ({self.kg_to_lbs(weight):4})', EMPTY_FV, True))
            fields.append(create_field(f'Capture Rate ({pkmn.capture_rate})', EMPTY_FV, True))
            fields.append(create_field(f'XP-Growth ❖', pkmn.exp_growth, True))
            fields.append(create_field(f'💛 ({pkmn.base_happiness})', EMPTY_FV, True))
        abilities = '\n'.join([a for a in await self.convert_abilities(guild, pkmn)])
        fields.append(create_field('Abilities', abilities, True))
        fields.append(create_field(f':egg:Egg Groups', str(pkmn.egg_groups), True))
        print(f'evo_line from create_pkmn_fields: {pkmn.evo_line}')
        fields.append(create_field(f'Evolution Line: {self.convert_evo_line(evo_line_emos)}', EMPTY_FV))
        return fields

    def convert_evo_line(self, evo_line):
        print(f'converting evo line... {evo_line}')
        evo_str ='  ➠  '.join(str(e) for e in evo_line)
        return evo_str

    def convert_name_to_id(self, name):
        name = self.clean_name(name)
        if name in NAME_TO_DEX_ID_JSON: return NAME_TO_DEX_ID_JSON[name]
        elif name in DEX_ID_TO_NAME_JSON: return name
        elif name[0] in DEX_ID_TO_NAME_JSON: return NAME_TO_DEX_ID_JSON[self.clean_name(name[0])]
        elif name[1] in NAME_TO_DEX_ID_JSON: return self.clean_name(name[1])
        raise ValueError(f'No ID for NAME={name} in NAME-TO-DEX-ID TABLE')

    def convert_id_to_name(self, id):
        id = str(id).lower()
        if id in DEX_ID_TO_NAME_JSON: return DEX_ID_TO_NAME_JSON[id]
        elif id in NAME_TO_DEX_ID_JSON: return DEX_ID_TO_NAME_JSON[NAME_TO_DEX_ID_JSON[id]]
        raise ValueError(f'No NAME for ID={id} in DEX-ID-TO-NAME TABLE')

    async def convert_abilities(self, guild, pkmn):
        ability_normal = await self.get_emoji(guild, 'ability_normal', ABILITY_NORMAL_PATH)
        ability_hidden = await self.get_emoji(guild, 'ability_hidden', ABILITY_HIDDEN_PATH)
        abilities_str = []
        for ability in pkmn.abilities:
            if ability.hidden:
                abilities_str.append(f'{ability_hidden} - {ability.name.capitalize():4}')
            else:
                abilities_str.append(f'{ability_normal} - {ability.name.capitalize():4}')
        return abilities_str

    def clean_emoji_name(self, name):
        return (str(name).replace('-', '').replace('♀', '').replace('♂', '')
                .lower())

    def clean_name(self, name):
        # name = str(name)
        # if name.endswith('-f') or name.endswith('-m'):
        # if '-' in str(name):
        #     str(name).split('-')
        #     name = str(name).replace('-', '').lower()
        # if name.startswith(':') and name.endswith(':'):
            # name = name.replace(':', '')
        # return str(name).replace('♀', '').replace('♂', '').lower()
        return str(name).lower()
