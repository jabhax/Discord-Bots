class Ranks:
    async def update_data(self, USERS, user):
        uid = str(user.id)
        if not uid in USERS:
            USERS[uid] = {}
            USERS[uid]['experience'] = 0
            USERS[uid]['level'] = 0

    async def add_xp(self, USERS, user, xp):
        uid = str(user.id)
        if uid in USERS: USERS[uid]['experience'] = USERS[uid]['experience'] + xp
        else: print(f'{uid} not in {USERS.keys()}')

    async def lvl_up(self, USERS, user, ch):
        uid = str(user.id)
        xp = USERS[uid]['experience']
        lvl_start = USERS[uid]['level']
        lvl_end = int(xp ** float(1.5/4))
        if lvl_start < lvl_end:
            await ch.send(f'{user.mention} has leveled up to {lvl_end}')
            USERS[uid]['level'] = lvl_end
        else:
            print(f'No level yet -sosad. {xp}')
