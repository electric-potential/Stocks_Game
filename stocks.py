from __future__ import unicode_literals
import discord
from discord.ext.commands import Bot
import asyncio
import sys
import os
import random
import time
import math
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

correct_path = os.getcwd()
os.chdir(correct_path+'/stocks saves')
prefix = '.'
description = 'stocks game'
my_bot = Bot(command_prefix = prefix, description = description)
my_bot.remove_command('help')
stocks = ['gold', 'silver', 'oil',
          'platinum', 'copper', 'corn', 'wheat',
          'cattle', 'cocoa', 'cotton', 'sugar',
          'coal', 'uranium']
time_bot_id = 321100519999537152
my_id = 297194292907343872

def new_trend_file():
    stocks = ['gold', 'silver', 'oil',
              'platinum', 'copper', 'corn', 'wheat',
              'cattle', 'cocoa', 'cotton', 'sugar',
              'coal', 'uranium']
    f = open('trend.dat', 'w')
    for x in stocks:
        f.write(x+': ')
        for y in range(0, 37):
            f.write('50: ')
        f.write('\n')
    f.close()

def comma_num(i):
    if type(i) == int:
        y = str(i)
        y = y[::-1]
        temp = ''
        count = 0
        for x in y:
            temp += x
            count += 1
            if count == 3:
                count = 0
                temp += ','
        temp = temp[::-1]
        if temp[0] == ',':
            temp = temp[1:]
        return temp

def prefix_num_to_num(i):
    if type(i) == str:
        lst = ['k', 'M', 'G', 'T', 'P', 'E']
        num = ''
        word = ''
        w = True
        for x in i[::-1]:
            if x in lst and w:
                word += x
            elif x not in lst and w:
                w = False
                num += x
            elif not w:
                num += x
        num = num[::-1]
        try:
            num = float(num)
        except Exception:
            return False
        for x in word:
            if x == 'k':
                num = num * 10**3
            elif x == 'M':
                num = num * 10**6
            elif x == 'G':
                num = num * 10**9
            elif x == 'T':
                num = num * 10**12
            elif x == 'P':
                num = num * 10**15
            elif x == 'E':
                num = num * 10**18
        if num.is_integer():
            return int(num)
        else:
            return False
    else:
        return False

def num_to_prefix_num(i):
    if type(i) == int or type(i) == float:
        if i >= 0 and i < 1000:
            return str(i)
        count = 0
        while True:
            if i/(10**count) >= 1 and i/(10**count) < 1000:
                break
            count += 3
        i = i*10
        i = math.floor(i/10**count)
        i = i/10
        count = count//3
        lst = ['', 'k', 'M', 'G', 'T', 'P', 'E']
        if count != 0 and count <= 6:
            return str(i)+lst[count]
        if count > 6:
            temp = str(i)+lst[6]
            count -= 6
            div = count//6
            rem = count%6
            for x in range(div):
                temp += lst[6]
            temp += lst[rem]
            return temp
        else:
            return str(int(i))

def initialize_game():
    stocks = ['gold', 'silver', 'oil',
              'platinum', 'copper', 'corn', 'wheat',
              'cattle', 'cocoa', 'cotton', 'sugar',
              'coal', 'uranium']
    f = open('probabilities.dat', 'w')
    for x in stocks:
        f.write(x+': '+str(random.randint(200,800))+'\n')
    f.close()
    f = open('costs.dat', 'w')
    for x in stocks:
        f.write(x+': '+str(random.randint(20,80))+'\n')
    f.close()

def get_lotto():
    f = open('lotto.dat', 'r')
    lst = f.readlines()
    f.close()
    values = {}
    for x in range(len(lst)):
        lst[x] = lst[x][0:len(lst[x])-1]
        values[lst[x].split(': ')[0]] = lst[x].split(': ')[1]
    values['pot'] = int(values['pot'])
    return values

def update_lotto(d):
    f = open('lotto.dat', 'w')
    for x in d:
        f.write(x+': '+str(d[x])+'\n')
    f.close()

def get_costs():
    f = open('costs.dat', 'r')
    lst = f.readlines()
    f.close()
    values = {}
    for x in range(len(lst)):
        lst[x] = lst[x][0:len(lst[x])-1]
        values[lst[x].split(': ')[0]] = int(lst[x].split(': ')[1])
    return values

def update_costs(d):
    f = open('costs.dat', 'w')
    for x in d:
        f.write(x+': '+str(d[x])+'\n')
    f.close()

def get_probabilities():
    f = open('probabilities.dat', 'r')
    lst = f.readlines()
    f.close()
    values = {}
    for x in range(len(lst)):
        lst[x] = lst[x][0:len(lst[x])-1]
        values[lst[x].split(': ')[0]] = int(lst[x].split(': ')[1])
    return values

def update_probabilities(d):
    f = open('probabilities.dat', 'w')
    for x in d:
        f.write(x+': '+str(d[x])+'\n')
    f.close()

def create_user(user_id, money=1000, referal=1):
    stocks = ['gold', 'silver', 'oil',
              'platinum', 'copper', 'corn', 'wheat',
              'cattle', 'cocoa', 'cotton', 'sugar',
              'coal', 'uranium']
    f = open(str(user_id)+'.txt', 'w')
    f.write('id: '+str(user_id)+'\n')
    f.write('money: '+str(money)+'\n')
    for x in stocks:
        f.write(x+': 0\n')
    f.write('lottos: 0\n')
    f.write('reset value: '+str(money)+'\n')
    f.write('used referal: '+str(referal)+'\n')
    f.close()
    
def get_info(user_id):
    try:
        f = open(str(user_id)+'.txt', 'r')
        lst = f.readlines()
        f.close()
        values = {}
        for x in range(len(lst)):
            lst[x] = lst[x][0:len(lst[x])-1]
            values[lst[x].split(': ')[0]] = int(lst[x].split(': ')[1])
        return values
    except Exception:
        return None

def update_player(d):
    f = open(str(d['id'])+'.txt', 'w')
    for x in d:
        f.write(x+': '+str(d[x])+'\n')
    f.close()

def add_save_file_element(index, value, user_id):
    d = get_info(user_id)
    d[index] = value
    update_player(d)
    
def buying(user_id, stock, quantity):
    user_info = get_info(user_id)
    if user_info == None:
        create_user(user_id)
        user_info = get_info(user_id)
    c = get_costs()
    p = get_probabilities()
    if user_info['money'] >= c[stock]*quantity:
        user_info[stock] += quantity
        user_info['money'] -= c[stock]*quantity
        p[stock] += 1
        if p[stock] > 800:
            p[stock] = 800
        update_probabilities(p)
    else:
        raise Exception
    update_player(user_info)

def selling(user_id, stock, quantity):
    user_info = get_info(user_id)
    if user_info == None:
        create_user(user_id)
    user_info = get_info(user_id)
    c = get_costs()
    p = get_probabilities()
    if user_info[stock] >= quantity:
        user_info[stock] -= quantity
        user_info['money'] += c[stock]*quantity
        p[stock] -= 1
        if p[stock] < 200:
            p[stock] = 200
        update_probabilities(p)
    else:
        raise Exception
    update_player(user_info)

@my_bot.event
async def on_ready():
    print('logged in')
    await my_bot.change_presence(game=discord.Game(name='| .commands',url=None,type=0))
    my_bot.server = discord.utils.get(my_bot.guilds, id=382737120768294913)
    my_bot.me = my_bot.server.owner
    my_bot.market_trend = discord.utils.get(my_bot.server.text_channels, name='market_trend')
    my_bot.member_log = discord.utils.get(my_bot.server.text_channels, name='member_log')
    my_bot.leaderboard = discord.utils.get(my_bot.server.text_channels, name='leaderboard')
    my_bot.lotto_winners = discord.utils.get(my_bot.server.text_channels, name='lotto_winners')
    while True:
        await asyncio.sleep(300)
        stocks = ['gold', 'silver', 'oil',
                  'platinum', 'copper', 'corn', 'wheat',
                  'cattle', 'cocoa', 'cotton', 'sugar',
                  'coal', 'uranium']
        mems_for_leaderboard = {}
        c = get_costs()
        p = get_probabilities()
        saved_roles = []
        for x in my_bot.server.roles:
            if x.name == 'announcements':
                saved_roles.append(x)
            elif x.name == 'stocks team':
                saved_roles.append(x)
            elif x.name == 'giveaways':
                saved_roles.append(x)
            elif x.name == 'user bot':
                saved_roles.append(x)
            elif x.name == 'contributor':
                saved_roles.append(x)
        for x in stocks:
            value = random.randint(1,20)
            rise = random.randint(0,1000)
            if p[x] > 550:
                p[x] -= (p[x]//100)*2
            if p[x] < 450:
                p[x] += (p[x]//100)*2
            update_probabilities(p)
            if rise <= p[x]:
                if value >= 1 and value <= 2:
                    pass
                elif value > 2 and value <= 14:
                    c[x] += 1
                elif value > 14 and value <= 17:
                    c[x] += 2
                elif value > 17:
                    c[x] += 3
                update_costs(c)
            else:
                if value >= 1 and value <= 2:
                    pass
                elif value > 2 and value <= 14:
                    c[x] -= 1
                elif value > 14 and value <= 17:
                    c[x] -= 2
                elif value > 17:
                    c[x] -= 3
                update_costs(c)
            if c[x] >= 100:
                c[x] = 50
                p[x] = random.randint(200, 800)
                update_costs(c)
                update_probabilities(p)
                for f in os.listdir():
                    if f.endswith('.txt'):
                        temp = get_info(int(f.split('.')[0]))
                        temp[x] = temp[x]*2
                        update_player(temp)
            if c[x] <= 0:
                c[x] = 50
                p[x] = random.randint(200,800)
                update_costs(c)
                update_probabilities(p)
                for f in os.listdir():
                    if f.endswith('.txt'):
                        temp = get_info(int(f.split('.')[0]))
                        temp[x] = 0
                        update_player(temp)
        #
        deleting = []
        async for x in my_bot.market_trend.history(limit=10):
            deleting.append(x)
        for x in deleting:
            await x.delete()
        f = open('trend.dat', 'r')
        lst = f.readlines()
        f.close()
        new = {}
        for x in lst:
            new[x.split(': ')[0]] = []
            for y in range(1, 38):
                new[x.split(': ')[0]].append(x.split(': ')[y])
        c = get_costs()
        for x in new:
            for y in range(0, 36):
                new[x][y] = new[x][y+1]
            new[x][36] = str(c[x])
        f = open('trend.dat', 'w')
        for x in new:
            f.write(x+': ')
            for y in range(0, 37):
                f.write(new[x][y]+': ')
            f.write('\n')
        f.close()
        #
        colors = ['#f9dd39', '#efedde', '#000000', '#9790db', '#b87333',
                  '#c0ce25', '#ff8800', '#0d18e0', '#5e360a', '#ff0000',
                  '#22c9c6', '#f707eb', '#4cff00']
        y = []
        for x in range(0, 101):
            y.append(x)
        x = []
        for y in range(36, -1, -1):
            x.append(y)
        plt.yticks(np.arange(0, 101, step=10))
        plt.subplots_adjust(right=0.8, top=0.95, bottom=0.09)
        plt.vlines(range(35, 0, -5), 0, 100, linestyles='dashed', linewidth=0.5)
        plt.hlines(range(10, 101, 10), 36, 0, linestyles='dashed', linewidth=0.5)
        d = {}
        for z in stocks:
            d[z] = []
            for w in new[z]:
                d[z].append(int(w))
        for z in range(len(stocks)):
            plt.plot(x, d[stocks[z]], colors[z], linewidth=2)
        plt.axis([36,0,0,100])
        plt.ylabel("Price Per Stock")
        plt.xlabel("Time")
        plt.title("Market Trend")
        plt.legend(stocks, bbox_to_anchor=(1.01, 1), borderaxespad=0.0)
        plt.savefig('trend.png')
        f = open('trend.png', 'rb')
        file = discord.File(f, filename='trend.png')
        await my_bot.market_trend.send(file=file)
        f.close()
        plt.gcf().clear()
        #
        msg = '```\nSTOCK TRENDS\n\n'
        for x in new:
            msg += x+': '+new[x][31]+' -> '+new[x][32]+' -> '+new[x][33]+' -> '+new[x][34]+' -> '+new[x][35]+' -> '+new[x][36]+'\n'
        msg += '```'
        await my_bot.market_trend.send(msg)
        #
        for x in my_bot.server.roles:
            if x.name == '1K': 
                role1 = x
            elif x.name == '10K':
                role2 = x
            elif x.name == '100K':
                role3 = x
            elif x.name == '1M':
                role4 = x
            elif x.name == '10M':
                role5 = x
            elif x.name == '100M':
                role6 = x
            elif x.name == '1G':
                role7 = x
            elif x.name == '10G':
                role8 = x
            elif x.name == '100G':
                role9 = x
            elif x.name == '1T':
                role10 = x
            elif x.name == '10T':
                role11 = x
            elif x.name == '100T':
                role12 = x
            elif x.name == '1P':
                role13 = x
            elif x.name == '10P':
                role14 = x
            elif x.name == '100P':
                role15 = x
            elif x.name == '1E':
                role16 = x
            elif x.name == '10E':
                role17 = x
            elif x.name == '100E':
                role18 = x
            elif x.name == 'stocks team':
                stocks_team_role = x
        mems_for_leaderboard = {}
        for x in my_bot.server.members:
            if x.id != 448372417430159360:
                c = get_costs()
                player = get_info(x.id)
                if player == None:
                    create_user(x.id)
                player = get_info(x.id)
                num = 0
                for y in stocks:
                    num += player[y]*c[y]
                num += player['money']
                player['lottos'] = 1
                update_player(player)
                if stocks_team_role not in x.roles:
                    mems_for_leaderboard.update({x: num})
                if num >= 10**20 and num < 10**21 and role18 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role18)
                    await x.edit(roles=adding_roles)
                elif num >= 10**19 and num < 10**20 and role17 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role17)
                    await x.edit(roles=adding_roles)
                elif num >= 10**18 and num < 10**19 and role16 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role16)
                    await x.edit(roles=adding_roles)
                elif num >= 10**17 and num < 10**18 and role15 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role15)
                    await x.edit(roles=adding_roles)
                elif num >= 10**16 and num < 10**17 and role14 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role14)
                    await x.edit(roles=adding_roles)
                elif num >= 10**15 and num < 10**16 and role13 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role13)
                    await x.edit(roles=adding_roles)
                elif num >= 10**14 and num < 10**15 and role12 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role12)
                    await x.edit(roles=adding_roles)
                elif num >= 10**13 and num < 10**14 and role11 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role11)
                    await x.edit(roles=adding_roles)
                elif num >= 10**12 and num < 10**13 and role10 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role10)
                    await x.edit(roles=adding_roles)
                elif num >= 10**11 and num < 10**12 and role9 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role9)
                    await x.edit(roles=adding_roles)
                elif num >= 10**10 and num < 10**11 and role8 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role8)
                    await x.edit(roles=adding_roles)
                elif num >= 10**9 and num < 10**10 and role7 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role7)
                    await x.edit(roles=adding_roles)
                elif num >= 10**8 and num < 10**9 and role6 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role6)
                    await x.edit(roles=adding_roles)
                elif num >= 10**7 and num < 10**8 and role5 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role5)
                    await x.edit(roles=adding_roles)
                elif num >= 10**6 and num < 10**7 and role4 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role4)
                    await x.edit(roles=adding_roles)
                elif num >= 10**5 and num < 10**6 and role3 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role3)
                    await x.edit(roles=adding_roles)
                elif num >= 10**4 and num < 10**5 and role2 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role2)
                    await x.edit(roles=adding_roles)
                elif num < 10**4 and role1 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role1)
                    await x.edit(roles=adding_roles)
        for x in saved_roles:
            if x.name == 'user bot':
                user_bot_role = x
        deleting = []
        async for x in my_bot.leaderboard.history(limit=10):
            deleting.append(x)
        for x in deleting:
            await x.delete()
        keys = []
        already_in = []
        for x in range(10):
            big = None
            for y in mems_for_leaderboard:
                if y.id not in already_in:
                    if (big == None or big[1] < mems_for_leaderboard[y]) and user_bot_role not in y.roles:
                        big = [y, mems_for_leaderboard[y]]
            already_in.append(big[0].id)
            keys.append(big)
        msg = '```\nLEADERBOARD\n\n'
        count = 1
        l = get_lotto()
        depreciation = 0.999656236
        for x in keys:
            msg += '['+str(count)+'] '+x[0].name+': '+num_to_prefix_num(x[1])+'\n'
            count += 1
            info = get_info(x[0].id)
            value = info['money']
            for x in stocks:
                value += info[x]*c[x]
            if value >= 1000000:
                temp_stocks = ['gold', 'silver', 'oil',
                               'platinum', 'copper', 'corn', 'wheat',
                               'cattle', 'cocoa', 'cotton', 'sugar',
                               'coal', 'uranium']
                new_value = int(round(value*depreciation))
                value_to_delete = value - new_value
                if info['money'] >= value_to_delete:
                    info['money'] -= value_to_delete
                    value_to_delete = 0
                else:
                    value_to_delete -= info['money']
                    info['money'] = 0
                    random.shuffle(temp_stocks)
                    for stock in temp_stocks:
                        if info[stock]*c[stock] > 0 and value_to_delete > 0:
                            if info[stock]*c[stock] >= value_to_delete:
                                temp = value_to_delete//c[stock]
                                if temp == 0:
                                    temp = 1
                                value_to_delete = 0
                                info[stock] -= temp
                            else:
                                value_to_delete -= info[stock]*c[stock]
                                info[stock] = 0
                update_player(info)
        l['pot'] += 1000
        update_lotto(l)
        msg += '```'
        await my_bot.leaderboard.send(msg)

@my_bot.event
async def on_member_join(member):
    for x in my_bot.server.roles:
        if x.name == 'announcements':
            role1 = x
        elif x.name == 'giveaways':
            role2 = x
    await member.add_roles(role1, role2)
    await my_bot.member_log.send('member count increased, now at: '+str(len(my_bot.server.members))+'\njoining member: '+member.name)
    await member.send('Welcome to Stocks Game! To get started, you can read the #how_to_play channel and if you have any questions about the game, feel free to ask the team in the #questions channel!\n\n '+
                      'https://www.gofundme.com/stocks-game-computer-upgrade')

@my_bot.event
async def on_member_remove(member):
    await my_bot.member_log.send('member count decreased, now at: '+str(len(my_bot.server.members))+'\nleaving member: '+member.name)

@my_bot.event
async def on_command_error(context, error):
    if type(error) == discord.ext.commands.CommandNotFound:
        await context.message.channel.send('```Command does not exist, for a list of all commands, type .commands.```')

@my_bot.command(pass_context=True)
async def add_element(context):
    if context.message.author.id == 297194292907343872:
        lst = context.message.content.split(' ')
        del lst[0]
        for f in os.listdir():
            if f.endswith('.txt'):
                x = f.split('.')
                x = int(x[0])
                add_save_file_element(lst[0], lst[1], x)

@my_bot.command(pass_context=True)
async def new_lotto(context):
    if context.message.author.id == 297194292907343872:
        stocks = ['gold', 'silver', 'oil',
                  'platinum', 'copper', 'corn', 'wheat',
                  'cattle', 'cocoa', 'cotton', 'sugar',
                  'coal', 'uranium']
        f = open('lotto.dat', 'w')
        f.write('stock: '+stocks[random.randint(0, len(stocks)-1)]+'\n')
        f.write('pot: 10000\n')
        f.close()

@my_bot.command(pass_context=True)
async def test_element(context):
    if context.message.author.id == 297194292907343872:
        lst = context.message.content.split('  ')
        del lst[0]
        for f in os.listdir():
            if f.endswith('.txt'):
                x = f.split('.')
                x = int(x[0])
                d = get_info(x)
                try:
                    test = d[lst[0]]
                except Exception:
                    print(x)
        print('done')

@my_bot.command(pass_context=True)
async def send_code(context):
    if context.message.author.id == 297194292907343872:
        os.chdir(correct_path)
        f = open('stocks.py', 'rb')
        file = discord.File(f, filename='stocks.py')
        await context.message.channel.send(file=file)
        f.close()
        os.chdir(correct_path+'/stocks saves')

@my_bot.command(pass_context=True)
async def help(context):
    await context.message.channel.send('```Use the command .commands instead.```')

@my_bot.command(pass_context=True)
async def referred_by(context):
    if context.message.content[0:13] == '.referred_by ' and len(context.message.mentions) == 1 and context.message.mentions[0].id != 448372417430159360 and context.message.mentions[0] in my_bot.server.members and type(context.message.channel) != discord.DMChannel and context.message.mentions[0] != context.message.author:
        using_command = get_info(context.message.author.id)
        if using_command == None:
            create_user(context.message.author.id)
            using_command = get_info(context.message.author.id)
        being_used_on = get_info(context.message.mentions[0].id)
        if being_used_on == None:
            create_user(context.message.mentions[0].id)
            being_used_on = get_info(context.message.mentions[0].id)
        if using_command['used referal'] >= 1:
            using_command['used referal'] -= 1
            being_used_on['reset value'] += 3000
            if being_used_on['reset value'] > 10000:
                being_used_on['reset value'] = 10000
            update_player(using_command)
            update_player(being_used_on)
            await context.message.channel.send('```player was successfully referred.```')
        else:
            await context.message.channel.send('```you already used your referal.```')
        
    else:
        await context.message.channel.send('```referal could not be made.```')  

@my_bot.command(pass_context=True)
async def buy(context):
    user_info = get_info(context.message.author.id)
    if user_info == None:
        create_user(context.message.author.id)
        user_info = get_info(context.message.author.id)
    try:
        c = get_costs()
        stock = context.message.content.split()[2]
        if context.message.content.split()[1] == 'max':
            q = user_info['money']//c[stock]
        elif context.message.content.split()[1] == 'half':
            q = (user_info['money']//c[stock])//2
        else:
            q = prefix_num_to_num(context.message.content.split()[1])
        if type(q) == bool:
            raise Exception
        buying(context.message.author.id, stock, q)
        if type(context.message.channel) == discord.DMChannel:
            await context.message.author.send('```purchase of '+num_to_prefix_num(q)+' '+stock+' successful at a price of '+str(c[stock])+' each for a total cost of '+num_to_prefix_num(q*c[stock])+'.```')
        else:
            await context.message.channel.send('```purchase of '+num_to_prefix_num(q)+' '+stock+' successful at a price of '+str(c[stock])+' each for a total cost of '+num_to_prefix_num(q*c[stock])+'.```')
    except Exception:
        if type(context.message.channel) == discord.DMChannel:
            await context.message.author.send('```purchase void```')
        else:
            await context.message.channel.send('```purchase void```')

@my_bot.command(pass_context=True)
async def sell(context):
    user_info = get_info(context.message.author.id)
    if user_info == None:
        create_user(context.message.author.id)
        user_info = get_info(context.message.author.id)
    try:
        c = get_costs()
        if context.message.content.split()[1] == 'all' and len(context.message.content.split()) == 2:
            stocks = ['gold', 'silver', 'oil',
                      'platinum', 'copper', 'corn', 'wheat',
                      'cattle', 'cocoa', 'cotton', 'sugar',
                      'coal', 'uranium']
            total = 0
            p = get_probabilities()
            for x in stocks:
                if user_info[x] > 0:
                    total += user_info[x]*c[x]
                    user_info['money'] += user_info[x]*c[x]
                    user_info[x] = 0
                    p[x] -= 1
                    if p[x] < 200:
                        p[x] = 200
            update_probabilities(p)
            update_player(user_info)
            if type(context.message.channel) == discord.DMChannel:
                await context.message.author.send('```sale of all stocks successful for a total return of '+num_to_prefix_num(total)+'.```')
            else:
                await context.message.channel.send('```sale of all stocks successful for a total return of '+num_to_prefix_num(total)+'.```')
        else:
            if context.message.content.split()[1] == 'max':
                stock = context.message.content.split()[2]
                q = user_info[stock]
                if q <= 0:
                    q = False
            elif context.message.content.split()[1] == 'half':
                stock = context.message.content.split()[2]
                q = user_info[stock]//2
                if q <= 0:
                    q = False
            else:
                q = prefix_num_to_num(context.message.content.split()[1])
                stock = context.message.content.split()[2]
            if type(q) == bool:
                raise Exception
            selling(context.message.author.id, stock, q)
            if type(context.message.channel) == discord.DMChannel:
                await context.message.author.send('```sale of '+num_to_prefix_num(q)+' '+stock+' successful at a price of '+str(c[stock])+' each for a total return of '+num_to_prefix_num(q*c[stock])+'.```')
            else:
                await context.message.channel.send('```sale of '+num_to_prefix_num(q)+' '+stock+' successful at a price of '+str(c[stock])+' each for a total return of '+num_to_prefix_num(q*c[stock])+'.```')
    except Exception:
        if type(context.message.channel) == discord.DMChannel:
            await context.message.author.send('```sale void```')
        else:
            await context.message.channel.send('```sale void```')

@my_bot.command(pass_context=True)
async def reset(context):
    if context.message.content == '.reset game values' and context.message.author == my_bot.me:
        initialize_game()
    else:
        try:
            d = get_info(context.message.author.id)
            money = d['reset value']
            referal = d['used referal']
            create_user(context.message.author.id, money, referal)
        except Exception:
            create_user(context.message.author.id)
        if type(context.message.channel) == discord.DMChannel:
            await context.message.author.send('```your account was reset.```')
        else:
            await context.message.channel.send('```your account was reset.```')

@my_bot.command(pass_context=True)
async def profile(context):
    stocks = ['gold', 'silver', 'oil',
          'platinum', 'copper', 'corn', 'wheat',
          'cattle', 'cocoa', 'cotton', 'sugar',
          'coal', 'uranium']
    if context.message.content == '.profile':
        player = get_info(context.message.author.id)
        if player == None:
            create_user(context.message.author.id)
        player = get_info(context.message.author.id)
        msg = '```\n'+context.message.author.name+' PROFILE\n\n'+'money: '+num_to_prefix_num(player['money'])+'\n'
        msg += 'reset value: '+num_to_prefix_num(player['reset value'])+'\n'
        msg += 'referrals left: '+str(player['used referal'])+'\n'
        msg += 'lottos left: '+str(player['lottos'])+'\n\n'
        for x in stocks:
            msg += x+': '+num_to_prefix_num(player[x])+'\n'
        msg += '```'
        if type(context.message.channel) == discord.DMChannel:
            await context.message.author.send(msg)
        else:
            await context.message.channel.send(msg)
    elif context.message.content[0:9] == '.profile ' and len(context.message.mentions) == 1 and context.message.mentions[0].id != 448372417430159360:
        player = get_info(context.message.mentions[0].id)
        if player == None:
            create_user(context.message.mentions[0].id)
        msg = '```\n'+context.message.mentions[0].name+' PROFILE\n\n'+'money: '+num_to_prefix_num(player['money'])+'\n'
        msg += 'reset value: '+num_to_prefix_num(player['reset value'])+'\n'
        msg += 'referrals left: '+str(player['used referal'])+'\n'
        msg += 'lottos left: '+str(player['lottos'])+'\n\n'
        for x in stocks:
            msg += x+': '+num_to_prefix_num(player[x])+'\n'
        msg += '```'
        if type(context.message.channel) == discord.DMChannel:
            await context.message.author.send(msg)
        else:
            await context.message.channel.send(msg)

@my_bot.command(pass_context=True)
async def exact_profile(context):
    stocks = ['gold', 'silver', 'oil',
              'platinum', 'copper', 'corn', 'wheat',
              'cattle', 'cocoa', 'cotton', 'sugar',
              'coal', 'uranium']
    for x in my_bot.server.roles:
        if x.name == 'contributor':
            role = x
    if type(context.message.channel) == discord.DMChannel:
        await context.message.channel.send('```This command can\'t be used in a DM channel.```')
        return
    if role not in context.message.author.roles:
        await context.message.channel.send('```Only members with the contributor role may use this command. In order to obtain the contributor role, a minimum donation of $5 is required here: ```\nhttps://www.gofundme.com/stocks-game-computer-upgrade')
        return
    if context.message.content == '.exact_profile':
        player = get_info(context.message.author.id)
        if player == None:
            create_user(context.message.author.id)
        player = get_info(context.message.author.id)
        msg = '```\n'+context.message.author.name+' EXACT PROFILE\n\n'+'money: '+comma_num(player['money'])+'\n'
        msg += 'reset value: '+comma_num(player['reset value'])+'\n'
        msg += 'referrals left: '+str(player['used referal'])+'\n'
        msg += 'lottos left: '+str(player['lottos'])+'\n\n'
        for x in stocks:
            msg += x+': '+comma_num(player[x])+'\n'
        msg += '```'
        await context.message.channel.send(msg)
    elif context.message.content[0:15] == '.exact_profile ' and len(context.message.mentions) == 1 and context.message.mentions[0].id != 448372417430159360:
        await context.message.channel.send('```This command can only be used on yourself.```')

@my_bot.command(pass_context=True)
async def stocks(context):
    c = get_costs()
    stocks = ['gold', 'silver', 'oil',
          'platinum', 'copper', 'corn', 'wheat',
          'cattle', 'cocoa', 'cotton', 'sugar',
          'coal', 'uranium']
    msg = '```\n'+'STOCKS\n\n'
    for x in stocks:
        msg += x+': '+str(c[x])+'\n'
    msg += '```'
    if type(context.message.channel) == discord.DMChannel:
        await context.message.author.send(msg)
    else:
        await context.message.channel.send(msg)

@my_bot.command(pass_context=True)
async def lotto_price(context):
    stocks = ['gold', 'silver', 'oil',
          'platinum', 'copper', 'corn', 'wheat',
          'cattle', 'cocoa', 'cotton', 'sugar',
          'coal', 'uranium']
    c = get_costs()
    if context.message.content == '.lotto_price':
        player = get_info(context.message.author.id)
        if player == None:
            create_user(context.message.author.id)
        player = get_info(context.message.author.id)
        value = 0
        for x in stocks:
            value += player[x]*c[x]
        value += player['money']
        num = value//100
        if num == 0:
            num = 1
        await context.message.channel.send('```The price you need to pay to play lottos is: '+num_to_prefix_num(num)+'```')
    elif context.message.content[0:13] == '.lotto_price ' and len(context.message.mentions) == 1 and context.message.mentions[0].id != 448372417430159360:
        player = get_info(context.message.mentions[0].id)
        if player == None:
            create_user(context.message.mentions[0].id)
        player = get_info(context.message.mentions[0].id)
        value = 0
        for x in stocks:
            value += player[x]*c[x]
        value += player['money']
        num = value//100
        if num == 0:
            num = 1
        await context.message.channel.send('```'+context.message.mentions[0].name+' needs to pay this much to play lotto: '+num_to_prefix_num(num)+'```')

@my_bot.command(pass_context=True)
async def lotto_pot(context):
    l = get_lotto()
    await context.message.channel.send('```The current pot for the lotto is: '+num_to_prefix_num(l['pot'])+'```')

@my_bot.command(pass_context=True)
async def lotto_stock(context):
    l = get_lotto()
    await context.message.channel.send('```The stock that you need three in a row for to win lotto is: '+l['stock']+'```')

@my_bot.command(pass_context=True)
async def lotto(context):
    if context.message.content == '.lotto':
        stocks = ['gold', 'silver', 'oil',
              'platinum', 'copper', 'corn', 'wheat',
              'cattle', 'cocoa', 'cotton', 'sugar',
              'coal', 'uranium']
        c = get_costs()
        l = get_lotto()
        value = 0
        player = get_info(context.message.author.id)
        if player == None:
            create_user(context.message.author.id)
        player = get_info(context.message.author.id)
        for x in stocks:
            value += player[x]*c[x]
        value += player['money']
        num = value//100
        if num == 0:
            num += 1
        msg = ''
        if player['lottos'] > 0 and player['money'] >= num:
            player['lottos'] -= 1
            player['money'] -= num
            l['pot'] += 1000
            s1 = stocks[random.randint(0, len(stocks)-1)]
            s2 = stocks[random.randint(0, len(stocks)-1)]
            s3 = stocks[random.randint(0, len(stocks)-1)]
            msg += '```You paid '+num_to_prefix_num(num)+' to play lotto! The stock you need is '+l['stock']+', and your lotto spin is:\n\n|'+s1+'|'+s2+'|'+s3+'|\n\n'
            if s1 == l['stock'] and s2 == l['stock'] and s3 == l['stock']:
                msg += 'You won! Your pot is: '+num_to_prefix_num(l['pot'])+', you will also be immortalized in #lotto_winners!```'
                await my_bot.lotto_winners.send(context.message.author.mention+' `won a pot of: '+num_to_prefix_num(l['pot'])+'`')
                player['money'] += l['pot']
                l['pot'] = 10000
                l['stock'] = stocks[random.randint(0, len(stocks)-1)]
            else:
                msg += 'You lost! try again next market update!```'
            update_lotto(l)
            update_player(player)
        else:
            msg += '```You either do not have enough money to play or have already used your lotto this market update.```'
        await context.message.channel.send(msg)

@my_bot.command(pass_context=True)
async def value(context):
    stocks = ['gold', 'silver', 'oil',
          'platinum', 'copper', 'corn', 'wheat',
          'cattle', 'cocoa', 'cotton', 'sugar',
          'coal', 'uranium']
    c = get_costs()
    if context.message.content == '.value':
        player = get_info(context.message.author.id)
        if player == None:
            create_user(context.message.author.id)
        player = get_info(context.message.author.id)
        num = 0
        for x in stocks:
            num += player[x]*c[x]
        num += player['money']
        msg = ('```'+context.message.author.name+' has a profile value of '+num_to_prefix_num(num)+'.```')
        if type(context.message.channel) == discord.DMChannel:
            await context.message.author.send(msg)
        else:
            await context.message.channel.send(msg)
    elif context.message.content[0:7] == '.value ' and len(context.message.mentions) == 1 and context.message.mentions[0].id != 448372417430159360:
        player = get_info(context.message.mentions[0].id)
        if player == None:
            await context.message.channel.send('```User has no profile yet.```')
            return
        num = 0
        for x in stocks:
            num += player[x]*c[x]
        num += player['money']
        msg = ('```'+context.message.mentions[0].name+' has a profile value of '+num_to_prefix_num(num)+'.```')
        if type(context.message.channel) == discord.DMChannel:
            await context.message.author.send(msg)
        else:
            await context.message.channel.send(msg)

@my_bot.command(pass_context=True)
async def announcements(context):
    if context.message.content == '.announcements':
        updated_roles = []
        if type(context.message.channel) != discord.DMChannel:
            for x in my_bot.server.roles:
                if x.name == 'announcements':
                    role = x
            for x in context.message.author.roles:
                updated_roles.append(x)
            if role in updated_roles:
                count = 0
                for x in updated_roles:
                    if x == role:
                        del updated_roles[count]
                    count += 1
            else:
                updated_roles.append(role)
            await context.message.author.edit(roles=updated_roles)
            await context.message.channel.send('```Roles updated.```')
        else:
            await context.message.channel.send('```This command can\'t be used in a DM channel.```')

@my_bot.command(pass_context=True)
async def giveaways(context):
    if context.message.content == '.giveaways':
        updated_roles = []
        if type(context.message.channel) != discord.DMChannel:
            for x in my_bot.server.roles:
                if x.name == 'giveaways':
                    role = x
            for x in context.message.author.roles:
                updated_roles.append(x)
            if role in updated_roles:
                count = 0
                for x in updated_roles:
                    if x == role:
                        del updated_roles[count]
                    count += 1
            else:
                updated_roles.append(role)
            await context.message.author.edit(roles=updated_roles)
            await context.message.channel.send('```Roles updated.```')
        else:
            await context.message.channel.send('```This command can\'t be used in a DM channel.```')

@my_bot.command(pass_context=True)
async def market_trend_erase(context):
    if context.message.author.id == 321100519999537152 or context.message.author.id == 297194292907343872:
        deleting = []
        async for x in my_bot.market_trend.history(limit=10):
            deleting.append(x)
        for x in deleting:
            await x.delete()

@my_bot.command(pass_context=True)
async def big_numbers(context):
    msg = ('```\n'+
           '1,000 = k = Thousand\n'+
           '1,000,000 = M = Million\n'+
           '1,000,000,000 = G = Billion\n'+
           '1,000,000,000,000 = T = Trillion\n'+
           '1,000,000,000,000,000 = P = Quadrillion\n'+
           '1,000,000,000,000,000,000 = E = Quintillion\n'+
           '```')
    await context.message.channel.send(msg)

@my_bot.command(pass_context=True)
async def update(context):
    if context.message.author.id == 321100519999537152 or context.message.author.id == 297194292907343872:
        stocks = ['gold', 'silver', 'oil',
                  'platinum', 'copper', 'corn', 'wheat',
                  'cattle', 'cocoa', 'cotton', 'sugar',
                  'coal', 'uranium']
        mems_for_leaderboard = {}
        c = get_costs()
        p = get_probabilities()
        saved_roles = []
        for x in my_bot.server.roles:
            if x.name == 'announcements':
                saved_roles.append(x)
            elif x.name == 'stocks team':
                saved_roles.append(x)
            elif x.name == 'giveaways':
                saved_roles.append(x)
            elif x.name == 'user bot':
                saved_roles.append(x)
            elif x.name == 'contributor':
                saved_roles.append(x)
        for x in stocks:
            value = random.randint(1,20)
            rise = random.randint(0,1000)
            if p[x] > 550:
                p[x] -= (p[x]//100)*2
            if p[x] < 450:
                p[x] += (p[x]//100)*2
            update_probabilities(p)
            if rise <= p[x]:
                if value >= 1 and value <= 2:
                    pass
                elif value > 2 and value <= 14:
                    c[x] += 1
                elif value > 14 and value <= 17:
                    c[x] += 2
                elif value > 17:
                    c[x] += 3
                update_costs(c)
            else:
                if value >= 1 and value <= 2:
                    pass
                elif value > 2 and value <= 14:
                    c[x] -= 1
                elif value > 14 and value <= 17:
                    c[x] -= 2
                elif value > 17:
                    c[x] -= 3
                update_costs(c)
            if c[x] >= 100:
                c[x] = 50
                p[x] = random.randint(200, 800)
                update_costs(c)
                update_probabilities(p)
                for f in os.listdir():
                    if f.endswith('.txt'):
                        temp = get_info(int(f.split('.')[0]))
                        temp[x] = temp[x]*2
                        update_player(temp)
            if c[x] <= 0:
                c[x] = 50
                p[x] = random.randint(200,800)
                update_costs(c)
                update_probabilities(p)
                for f in os.listdir():
                    if f.endswith('.txt'):
                        temp = get_info(int(f.split('.')[0]))
                        temp[x] = 0
                        update_player(temp)
        #
        deleting = []
        async for x in my_bot.market_trend.history(limit=10):
            deleting.append(x)
        for x in deleting:
            await x.delete()
        f = open('trend.dat', 'r')
        lst = f.readlines()
        f.close()
        new = {}
        for x in lst:
            new[x.split(': ')[0]] = []
            for y in range(1, 38):
                new[x.split(': ')[0]].append(x.split(': ')[y])
        c = get_costs()
        for x in new:
            for y in range(0, 36):
                new[x][y] = new[x][y+1]
            new[x][36] = str(c[x])
        f = open('trend.dat', 'w')
        for x in new:
            f.write(x+': ')
            for y in range(0, 37):
                f.write(new[x][y]+': ')
            f.write('\n')
        f.close()
        #
        colors = ['#f9dd39', '#efedde', '#000000', '#9790db', '#b87333',
                  '#c0ce25', '#ff8800', '#0d18e0', '#5e360a', '#ff0000',
                  '#22c9c6', '#f707eb', '#4cff00']
        y = []
        for x in range(0, 101):
            y.append(x)
        x = []
        for y in range(36, -1, -1):
            x.append(y)
        plt.yticks(np.arange(0, 101, step=10))
        plt.subplots_adjust(right=0.8, top=0.95, bottom=0.09)
        plt.vlines(range(35, 0, -5), 0, 100, linestyles='dashed', linewidth=0.5)
        plt.hlines(range(10, 101, 10), 36, 0, linestyles='dashed', linewidth=0.5)
        d = {}
        for z in stocks:
            d[z] = []
            for w in new[z]:
                d[z].append(int(w))
        for z in range(len(stocks)):
            plt.plot(x, d[stocks[z]], colors[z], linewidth=2)
        plt.axis([36,0,0,100])
        plt.ylabel("Price Per Stock")
        plt.xlabel("Time")
        plt.title("Market Trend")
        plt.legend(stocks, bbox_to_anchor=(1.01, 1), borderaxespad=0.0)
        plt.savefig('trend.png')
        f = open('trend.png', 'rb')
        file = discord.File(f, filename='trend.png')
        await my_bot.market_trend.send(file=file)
        f.close()
        plt.gcf().clear()
        #
        msg = '```\nSTOCK TRENDS\n\n'
        for x in new:
            msg += x+': '+new[x][31]+' -> '+new[x][32]+' -> '+new[x][33]+' -> '+new[x][34]+' -> '+new[x][35]+' -> '+new[x][36]+'\n'
        msg += '```'
        await my_bot.market_trend.send(msg)
        #
        for x in my_bot.server.roles:
            if x.name == '1K': 
                role1 = x
            elif x.name == '10K':
                role2 = x
            elif x.name == '100K':
                role3 = x
            elif x.name == '1M':
                role4 = x
            elif x.name == '10M':
                role5 = x
            elif x.name == '100M':
                role6 = x
            elif x.name == '1G':
                role7 = x
            elif x.name == '10G':
                role8 = x
            elif x.name == '100G':
                role9 = x
            elif x.name == '1T':
                role10 = x
            elif x.name == '10T':
                role11 = x
            elif x.name == '100T':
                role12 = x
            elif x.name == '1P':
                role13 = x
            elif x.name == '10P':
                role14 = x
            elif x.name == '100P':
                role15 = x
            elif x.name == '1E':
                role16 = x
            elif x.name == '10E':
                role17 = x
            elif x.name == '100E':
                role18 = x
            elif x.name == 'stocks team':
                stocks_team_role = x
        mems_for_leaderboard = {}
        for x in my_bot.server.members:
            if x.id != 448372417430159360:
                c = get_costs()
                player = get_info(x.id)
                if player == None:
                    create_user(x.id)
                player = get_info(x.id)
                num = 0
                for y in stocks:
                    num += player[y]*c[y]
                num += player['money']
                player['lottos'] = 1
                update_player(player)
                if stocks_team_role not in x.roles:
                    mems_for_leaderboard.update({x: num})
                if num >= 10**20 and num < 10**21 and role18 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role18)
                    await x.edit(roles=adding_roles)
                elif num >= 10**19 and num < 10**20 and role17 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role17)
                    await x.edit(roles=adding_roles)
                elif num >= 10**18 and num < 10**19 and role16 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role16)
                    await x.edit(roles=adding_roles)
                elif num >= 10**17 and num < 10**18 and role15 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role15)
                    await x.edit(roles=adding_roles)
                elif num >= 10**16 and num < 10**17 and role14 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role14)
                    await x.edit(roles=adding_roles)
                elif num >= 10**15 and num < 10**16 and role13 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role13)
                    await x.edit(roles=adding_roles)
                elif num >= 10**14 and num < 10**15 and role12 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role12)
                    await x.edit(roles=adding_roles)
                elif num >= 10**13 and num < 10**14 and role11 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role11)
                    await x.edit(roles=adding_roles)
                elif num >= 10**12 and num < 10**13 and role10 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role10)
                    await x.edit(roles=adding_roles)
                elif num >= 10**11 and num < 10**12 and role9 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role9)
                    await x.edit(roles=adding_roles)
                elif num >= 10**10 and num < 10**11 and role8 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role8)
                    await x.edit(roles=adding_roles)
                elif num >= 10**9 and num < 10**10 and role7 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role7)
                    await x.edit(roles=adding_roles)
                elif num >= 10**8 and num < 10**9 and role6 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role6)
                    await x.edit(roles=adding_roles)
                elif num >= 10**7 and num < 10**8 and role5 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role5)
                    await x.edit(roles=adding_roles)
                elif num >= 10**6 and num < 10**7 and role4 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role4)
                    await x.edit(roles=adding_roles)
                elif num >= 10**5 and num < 10**6 and role3 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role3)
                    await x.edit(roles=adding_roles)
                elif num >= 10**4 and num < 10**5 and role2 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role2)
                    await x.edit(roles=adding_roles)
                elif num < 10**4 and role1 not in x.roles:
                    adding_roles = []
                    for y in x.roles:
                        if y in saved_roles:
                            adding_roles.append(y)
                    adding_roles.append(role1)
                    await x.edit(roles=adding_roles)
        for x in saved_roles:
            if x.name == 'user bot':
                user_bot_role = x
        deleting = []
        async for x in my_bot.leaderboard.history(limit=10):
            deleting.append(x)
        for x in deleting:
            await x.delete()
        keys = []
        already_in = []
        for x in range(10):
            big = None
            for y in mems_for_leaderboard:
                if y.id not in already_in:
                    if (big == None or big[1] < mems_for_leaderboard[y]) and user_bot_role not in y.roles:
                        big = [y, mems_for_leaderboard[y]]
            already_in.append(big[0].id)
            keys.append(big)
        msg = '```\nLEADERBOARD\n\n'
        count = 1
        l = get_lotto()
        depreciation = 0.999656236
        for x in keys:
            msg += '['+str(count)+'] '+x[0].name+': '+num_to_prefix_num(x[1])+'\n'
            count += 1
            info = get_info(x[0].id)
            value = info['money']
            for x in stocks:
                value += info[x]*c[x]
            if value >= 1000000:
                temp_stocks = ['gold', 'silver', 'oil',
                               'platinum', 'copper', 'corn', 'wheat',
                               'cattle', 'cocoa', 'cotton', 'sugar',
                               'coal', 'uranium']
                new_value = int(round(value*depreciation))
                value_to_delete = value - new_value
                if info['money'] >= value_to_delete:
                    info['money'] -= value_to_delete
                    value_to_delete = 0
                else:
                    value_to_delete -= info['money']
                    info['money'] = 0
                    random.shuffle(temp_stocks)
                    for stock in temp_stocks:
                        if info[stock]*c[stock] > 0 and value_to_delete > 0:
                            if info[stock]*c[stock] >= value_to_delete:
                                temp = value_to_delete//c[stock]
                                if temp == 0:
                                    temp = 1
                                value_to_delete = 0
                                info[stock] -= temp
                            else:
                                value_to_delete -= info[stock]*c[stock]
                                info[stock] = 0
                update_player(info)
        l['pot'] += 1000
        update_lotto(l)
        msg += '```'
        await my_bot.leaderboard.send(msg)

@my_bot.command(pass_context=True)
async def commands(context):
    msg = ('```\n'+
           'COMMANDS\n\n'+
           '.reset: resets your game profile.\n\n'+
           '.stocks: shows the value of each stock.\n\n'+
           '.profile: shows you your inventory of stocks and money.\n\n'+
           '.exact_profile: only useable by members with the contributor role, shows your profile but with exact numbers (no approximations displayed).\n'
           '.buy <quantity> <stock>: lets you buy a certain quantity of one stock.\n\n'+
           '.sell <quantity> <stock>: lets you sell a certain quantity of one stock.\n\n'+
           '.value: shares your total profile value with you.\n\n'+
           '.big_numbers: posts the number symbols used to represent really large numbers.\n\n'+
           '.announcements: adds or removes the role announcements, which pings you if this server is updated or something changed.\n\n'+
           '.giveaways: adds or removes the role giveaways, which pings you if there is a giveaway being held.\n\n'+
           '.lotto: spins lotto, only 1 spin per market update.\n\n'+
           '.lotto_stock: posts what stock you need 3 of in lotto to win the pot.\n\n'+
           '.lotto_pot: posts how much money the winner of the current lotto will obtain.\n\n'+
           '.lotto_price: posts how much money it costs for you to play lotto.\n\n'+
           '.referred_by <mention>: if someone referred you to play stocks, mention them in this command to give them a bonus. 1 referal per player.\n\n'
           '```')
    if type(context.message.channel) == discord.DMChannel:
        await context.message.author.send(msg)
    else:
        await context.message.channel.send(msg)
                                    
@my_bot.command(pass_context=True)
async def link(context):
    if context.message.author.id == 297194292907343872:
        await context.message.author.send('https://discordapp.com/oauth2/authorize?&client_id=448372417430159360&scope=bot&permissions=0')

while True:
    try:
        my_bot.run('token')
    except Exception:
        my_bot.run('token')
