import random


STAT_NAME = {
    'hp': 'HP',
    'attack': 'ATK',
    'defense': 'DEF',
    'special-attack': 'SPA',
    'special-defense': 'SPD',
    'speed': 'SPE'
}


class PKGenders:
    def __init__(self, male=None, female=None):
        self.male = male
        self.female = female
        self.genderless = None

    def __repr__(self):
        if self.male and self.female:
            return f'male: {self.male}, female: {self.female}'
        elif self.male:
            return f'male: {self.male}, female: 0'
        elif self.female:
            return f'male: 0, female: {self.female}'
        return 'genderless'


class PKEggGroups:
    def __init__(self, group1=None, group2=None):
        self.group1 = group1
        self.group2 = group2

    def __repr__(self):
        if self.group1 and self.group2:
            return f'group1: {self.group1}, group2: {self.group2}'
        elif self.group1:
            return f'group1: {self.group1}'
        elif self.group2:
            return f'group2: {self.group2}'
        else:
            return f'group1: {self.group1}, group2: {self.group2}'


class PKTypes:
    def __init__(self, type1=None, type2=None):
        self.type1 = type1
        self.type2 = type2

    def __repr__(self):
        if self.type1 and self.type2:
            return f'type1 {self.type1}, type2: {self.type2}'
        elif self.type1:
            return f'type1 {self.type1}'
        elif self.type2:
            return f'type2: {self.type2}'
        else:
            return 'type1: None, type2: None'

class Stat:
    ''' Pokemon Stat Interface '''
    name, value, iv, ev = None, None, None, None
    def convert(self): pass
    def __repr__(self): return f'{self.name}: {self.value}'

class BaseStat:
    def __init__(self, name=None, value=None):
        self.name = name
        self.value = value
    def __repr__(self): return f'Base{self.name}: {self.value}'


class IV:
    ''' Pokemon IV Object '''
    name, value = None, None
    def __init__(self, name, value):
        self.name = name
        self.value = value

class EV:
    ''' Pokemon EV Object '''
    name, value = None, None
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Hp(Stat):
    ''' Pokemon HP Stat Object '''
    def __init__(self, name='hp', base=None, value=None):
        self.name = name
        self.base = BaseStat(name=STAT_NAME[name], value=base)
        self.value = value if value else base
        self.iv = IV(name=name, value=random.randint(1, 31))
    def convert(self): return 'HP'


class Attack(Stat):
    ''' Pokemon Attack Stat Object '''
    def __init__(self, name='attack', base=None, value=None):
        self.name = name
        self.base = BaseStat(name=STAT_NAME[name], value=base)
        self.value = value if value else base
        self.iv = IV(name=name, value=random.randint(1, 31))
    def convert(self): return 'ATK'

class Defense(Stat):
    ''' Pokemon Defense Stat Object '''
    def __init__(self, name='defense', base=None, value=None):
        self.name = name
        self.base = BaseStat(name=STAT_NAME[name], value=base)
        self.value = value if value else base
        self.iv = IV(name=name, value=random.randint(1, 31))
        self.ev = EV(name=name, value=0)
    def convert(self): return 'DEF'

class SpecialAttack(Stat):
    ''' Pokemon Special Attack Stat Object '''
    def __init__(self, name='special-attack', base=None, value=None):
        self.name = name
        self.base = BaseStat(name=STAT_NAME[name], value=base)
        self.value = value if value else base
        self.iv = IV(name=name, value=random.randint(1, 31))
        self.ev = EV(name=name, value=0)
    def convert(self): return 'SPA'

class SpecialDefense(Stat):
    ''' Pokemon Special Defense Stat Object '''
    def __init__(self, name='special-defense', base=None, value=None):
        self.name = name
        self.base = BaseStat(name=STAT_NAME[name], value=base)
        self.value = value if value else base
        self.iv = IV(name=name, value=random.randint(1, 31))
        self.ev = EV(name=name, value=0)
    def convert(self): return 'SPD'

class Speed(Stat):
    ''' Pokemon Speed Stat Object '''
    def __init__(self, name='speed', base=None, value=None):
        self.name = name
        self.base = BaseStat(name=STAT_NAME[name], value=base)
        self.value = value if value else base
        self.iv = IV(name=name, value=random.randint(1, 31))
        self.ev = EV(name=name, value=0)
    def convert(self, n): return 'SPE'

class PKStats:
    ''' Pokemon Stat Object '''
    def __init__(self, hp=None, attack=None, defense=None,
                 sp_attack=None, sp_defense=None, speed=None):
        self.hp = Hp(base=hp)
        self.attack = Attack(base=attack)
        self.defense = Defense(base=defense)
        self.sp_attack = SpecialAttack(base=sp_attack)
        self.sp_defense = SpecialDefense(base=sp_defense)
        self.speed = Speed(base=speed)
        self.base_total = sum([hp, attack, defense, sp_attack, speed])
        self.total = None
        self.STATS = [self.hp, self.attack, self.defense, self.sp_attack,
                      self.sp_defense, self.speed]
        self.BASE_STATS = [s.base for s in self.STATS]
        self.IVS = [self.hp.iv, self.attack.iv, self.defense.iv,
                    self.sp_attack.iv, self.sp_defense.iv, self.speed.iv]
        self.EVS = [self.hp.ev, self.attack.ev, self.defense.ev,
                    self.sp_attack.ev, self.sp_defense.ev, self.speed.ev]
        name_spacing, value_spacing, padding = 3, 4, 8
        stat_names = (f'{"":<{padding}}'.join([f'{s.name.rjust(name_spacing, " ")}'
                      for s in self.BASE_STATS]))
        stat_values = (f'{"":<{padding}}'.join([f'{str(s.value).rjust(value_spacing, " ")}'
                       for s in self.BASE_STATS]))
        self.base_stats_str = f'⇦{stat_names} ⇨\n     {stat_values}'

    def __str__(self):
        ss = ', '.join([f'{s.name}: {s.value}' for s in self.STATS])
        return f'Stats Total: ({self.get_total()})\n{ss}'

    def get_total(self):
        return sum([s.value for s in self.STATS])

    def __repr__(self):
        return self


class PKAbility:
    def __init__(self, name=None, hidden=False):
        self.name = name
        self.hidden = hidden
    def __repr__(self):
        return f'name: {self.name}, hidden: {self.hidden}'

class DexPk:
    def __init__(self, id, name):
        self.id = id
        self.name = name

class Pokemon:
    def __init__(self, pkj):
        try:
            self.id = int(pkj['id'])
        except:
            key = next(iter(pkj.keys()))
            pkj = pkj[key]
            print(f'pkj: {pkj}')
            self.id = int(pkj['id'])
        self.name = pkj['name']
        self.height = pkj['height']
        self.weight = pkj['weight']
        self.base_exp = pkj['base_exp']
        self.exp_growth = pkj['exp_growth']
        self.capture_rate = pkj['capture_rate']
        self.base_happiness = pkj['base_happiness']
        self.abilities_list = pkj['abilities']
        self.abilities = []
        if len(pkj['abilities']) < 2:
            self.abilities.append(PKAbility(pkj['abilities'][0]))
        else:
            self.abilities.append(PKAbility(pkj['abilities'][0]))
            self.abilities.append(PKAbility(pkj['abilities'][1], True))
        self.genders_list = pkj['genders']
        male, female = pkj['genders']
        self.genders = PKGenders(male=male, female=female)
        self.genders_list = pkj['genders']
        self.egg_groups = pkj['egg_groups']
        self.classification = pkj['classification']
        self.dex_entry = pkj['entry_text']
        hp, atk, defe, spatk, spdef, spe = [s for s in pkj['base_stats']]
        self.stats = PKStats(hp=hp, attack=atk, defense=defe, sp_attack=spatk,
                             sp_defense=spdef, speed=spe)
        self.types = pkj['types']
        self.evs_earned = pkj['evs_earned']
        self.evo_line = pkj['evo_line']
        self.sprites = pkj['sprites']
        prev, next = pkj['prev_dex_pk'], pkj['next_dex_pk']
        self.prv = DexPk(prev[0], prev[1])
        self.nxt = DexPk(next[0], next[1])

    def __str__(self):
        evo_str = "\n".join(f'id: {e[0]}, name: {e[1]}' for e in self.evo_line)
        return (f'id: {self.id}\nname: {self.name}\nheight: {self.height}\n'
                f'weight: {self.weight}\nbase_exp: {self.base_exp}\n'
                f'exp_growth: {self.exp_growth}\ncapture_rate: {self.capture_rate}\n'
                f'base_happiness: {self.base_happiness}\nabilities: {self.abilities}\n'
                f'genders: {self.genders}\negg_groups: {self.egg_groups}\n'
                f'classification: {self.classification}\ndex_entry: {self.dex_entry}\n'
                f'stats: {self.stats}\ntypes: {self.types}\nevs_earned: {self.evs_earned}')
                # f'evo_line: {evo_str}')

    def __repr__(self):
        evo_str = "\n".join(f'id: {e[0]}, name: {e[1]}' for e in self.evo_line)
        return (f'id: {self.id}\nname: {self.name}\nheight: {self.height}\n'
                f'weight: {self.weight}\nbase_exp: {self.base_exp}\n'
                f'exp_growth: {self.exp_growth}\ncapture_rate: {self.capture_rate}\n'
                f'base_happiness: {self.base_happiness}\nabilities: {self.abilities}\n'
                f'genders: {self.genders}\negg_groups: {self.egg_groups}\n'
                f'classification: {self.classification}\ndex_entry: {self.dex_entry}\n'
                f'stats: {self.stats}\ntypes: {self.types}\nevs_earned: {self.evs_earned}\n',
                f'evo_line: {evo_str}')
