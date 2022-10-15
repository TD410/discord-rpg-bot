import json, os
from discord import Member, utils, User, Server
from discord.ext import commands
from datetime import datetime, timedelta


bot = commands.Bot(command_prefix="!", description="")

bot.remove_command("help")

LOCATION_ITEM = {}
USER_ITEM = {}
LOCATION_ROLE = {}
USER_MOVE = {}

EXCLUDE_ROLE = ["375683169678000129", "375684595133186049", "375684785793662997", "406744577844707338", "406347371149262860"]

EVERYONE_ROLE_ID = '375683169678000129'
PLAYER_ROLE_ID = '406347371149262860'
AUDIENCE_ROLE_ID = '406744577844707338'
GOD_ROLE_ID = '375684595133186049'

SECRET_CH_ID = '375686965569388545'

GOD_ROLE = None
PLAYER_ROLE = None
AUDIENCE_ROLE = None

SECRET_CH = None

DUNG_ID = '232522866346819604'
OANH_ID = '322714445740638210'
PA_ID = '309998113232519168'

OANH = None
DUNG = None
PA = None

SET_UP = False

JUDGEMENT = False

ONBREAK = False

CANPICK = True

MAP = ('```diff\n'
       '- NHỮNG VỊ TRÍ MÀU XANH (CÓ DẤU +) LÀ CÓ THỂ VÀO, MÀU XÁM LÀ ĐANG BỊ KHÓA -\n'
       '+============ Tầng 2 ============+\n'
       '+   |-- Hành lang\n'
       '    |-- 2-A\n'
       '    |-- 2-B\n'
       '    |-- 2-C\n'
       '    |-- 2-D\n'
       '+   |-- Phòng gym\n'
       '    |-- Y\n'
       '    |-- Z\n'
       '+============ Tầng 1 ============+\n'
       '+   |-- Hành lang\n'
       '+   |-- 1-A\n'
       '+   |-- 1-B\n'
       '+   |-- 1-C\n'
       '+   |-- 1-D\n'
       '+   |-- Phòng giải trí\n'
       '+   |-- Phòng y tế\n'
       '    |-- X\n'
       '=========== Khoang tàu ===========\n'
       '    |-- Boong tàu\n'
       '    |-- Hành lang\n'
       '    |-- Phòng thủy thủ đoàn\n'
       '    |-- Phòng lái\n'
       '    |-- Phòng dạ hội\n'             
       '    |-- Bếp\n'
       '    |-- Hồ bơi\n'
       '============ Tầng hầm ============\n'
       '    |-- Hành lang\n'
       '    |-- Phòng máy\n'
       '    |-- Kho thiết bị\n'
       '```')

HELP = ('```'
        '!help:\n'
            '- Trợ giúp, hướng dẫn cú pháp câu lệnh.\n'
        '!showmap:\n'
            '- Hiển thị danh sách các phòng và địa điểm.\n'
        '!look:\n'
            '- Nhìn xung quanh vị trí hiện tại.\n'
            '- Cho bạn biết có bao nhiên món đồ có thể nhặt tại nơi đang đứng.\n'
        '!bag hoặc !bag public:\n'
            '- Xem túi của chính mình.\n'
            '- Khi gõ !bag, thông tin túi sẽ được BOT inbox cho bạn, người khác không thể xem.\n'
            '- Khi gõ !bag public, thông tin túi sẽ được BOT in ra trên chat cho mọi người xem..\n'
            '- Túi chứa được tối đa 7 đồ vật.\n'
        '!pickup Tên đồ vật:\n'
            '- Lấy đồ vật bỏ vào túi.\n'
            '- Sử dụng !look để nhìn xung quanh, có thể bạn sẽ phát hiện ra món đồ gì thú vị.\n'
            '- Bạn có thể thử lấy nhiều đồ vật khác nhau cho đến khi lấy được.\n'
        '!drop Tên đồ vật:\n'
            '- Vứt bỏ đồ vật có trong túi.\n'
            '- Bạn hoặc người khác có thể nhặt lại đồ vật này khi nói !pickup Tên đồ vật ở nơi bạn đã vứt.\n'
        '!use Tên đồ vật:\n'
            '- Sử dụng đồ vật có trong túi.\n'
            '- GM sẽ được thông báo và xác nhận việc sử dụng đồ vật của bạn.\n'
        '!goto Tên tầng - Tên vị trí\n'
            '- Chuyển sang vị trí mới.\n'
            '- VD: !goto Tầng 1 - 1-A\n'
            '- Bạn có thể chuyển vị trí mỗi giờ.\n'
            '- Gõ !showmap để xem danh sách tên vị trí. Hãy nhớ gõ đúng tên vị trí.\n'
        '!judgement\n'
            '- Gọi GM để buộc tội một người nào đó.\n'
            '- Chỉ có thể buộc tội khi bạn đã nhìn thấy xác chết.\n'
        '```')


@bot.event
async def on_ready():
    bot.leave_server()
    global LOCATION_ITEM, USER_ITEM, LOCATION_ROLE, USER_MOVE

    print("AeBot started.")
    LOCATION_ITEM = json.load(open('location_item.json', 'r', encoding='utf8'))
    LOCATION_ROLE = json.load(open('location_role.json', 'r', encoding='utf8'))
    USER_ITEM = json.load(open('user_item.json', 'r', encoding='utf8'))
    USER_MOVE = json.load(open('user_move.json', 'r', encoding='utf8'))
    print("Read all Data.")


@bot.command(pass_context=True)
async def setup(ctx):
    global LOCATION_ITEM, USER_ITEM, LOCATION_ROLE, EXCLUDE_ROLE, USER_MOVE, \
        GOD_ROLE, PLAYER_ROLE, AUDIENCE_ROLE, OANH, DUNG, PA, SECRET_CH, SET_UP

    if SET_UP:
        print("Already set up.")
        return

    GOD_ROLE = utils.find(lambda x: x.id == GOD_ROLE_ID, ctx.message.server.roles)
    PLAYER_ROLE = utils.find(lambda x: x.id == PLAYER_ROLE_ID, ctx.message.server.roles)
    AUDIENCE_ROLE = utils.find(lambda x: x.id == AUDIENCE_ROLE_ID, ctx.message.server.roles)

    DUNG = utils.find(lambda x: x.id == DUNG_ID, ctx.message.server.members)
    OANH = utils.find(lambda x: x.id == OANH_ID, ctx.message.server.members)
    PA = utils.find(lambda x: x.id == PA_ID, ctx.message.server.members)

    SECRET_CH = ctx.message.server.get_channel(SECRET_CH_ID)

    SET_UP = True
    await bot.say("Done set up.")


@bot.command(pass_context=True)
async def clearchat(ctx):
    if not SET_UP:
        print('Bot is not set up!')
        return

    if GOD_ROLE not in ctx.message.author.roles:
        print('Unauthorized.')
        return
    else:
        mgs = []
        number = 100
        async for x in bot.logs_from(ctx.message.channel, limit=number):
            mgs.append(x)
        await bot.delete_messages(mgs)


@bot.command(pass_context=True)
async def cleargoto(ctx):
    if not SET_UP:
        print('Bot is not set up!')
        return

    if GOD_ROLE not in ctx.message.author.roles:
        print("Unauthorized.")
        return

    global USER_MOVE
    for key in USER_MOVE:
        name = USER_MOVE[key]['name']
        USER_MOVE[key] = {'name': name, 'time': ''}

    save_user_move()

    await bot.say("Cleared move record.")


@bot.command(pass_context=True)
async def togglepick(ctx):
    if not SET_UP:
        print('Bot is not set up!')
        return

    if GOD_ROLE not in ctx.message.author.roles:
        print("Unauthorized.")
        return

    global CANPICK
    CANPICK = not CANPICK
    await bot.say('CANPICK is ' + str(CANPICK))


@bot.command(pass_context=True)
async def beginjudgement(ctx):
    if not SET_UP:
        print('Bot is not set up!')
        return

    if GOD_ROLE not in ctx.message.author.roles:
        print("Unauthorized.")
        return

    global JUDGEMENT
    JUDGEMENT = True

    players = list(filter(lambda x: PLAYER_ROLE in x.roles, ctx.message.server.members))

    for player in players:
        await bot.replace_roles(player, PLAYER_ROLE)

    await bot.say('Begin Judgement.')


@bot.command(pass_context=True)
async def endjudgement(ctx):
    if not SET_UP:
        print('Bot is not set up!')
        return

    if GOD_ROLE not in ctx.message.author.roles:
        print("Unauthorized.")
        return

    global JUDGEMENT
    JUDGEMENT = False

    await bot.say('End Judgement.')


@bot.command()
async def help():
    global HELP
    await bot.say(HELP)


@bot.command(pass_context=True)
async def look(ctx):
    """Nhìn xung quanh vị trí hiện tại."""

    location_items = get_location_items(ctx.message.channel.id)
    item_string = ""
    if location_items is not None:
        if len(location_items) > 0:
            item_string = "\n\nCó vẻ như ở đây có [" + str(sum(map(lambda x: x.get('num', 0), location_items))) + "] món đồ mà bạn có thể lấy."
        else:
            item_string = "\n\nCó vẻ như ở đây không còn món đồ gì để lấy."
    await bot.say("```ini\n" + ctx.message.channel.topic + item_string + "```")


@bot.command(pass_context=True)
async def pickup(ctx, *, item=""):
    """Lấy đồ vật bỏ vào túi.
    Túi chứa được tối đa 7 đồ vật.
    Sử dụng !look để nhìn xung quanh, có thể bạn sẽ phát hiện ra món đồ gì thú vị.
    Bạn có thể thử lấy nhiều đồ vật khác nhau cho đến khi lấy được."""

    if not CANPICK:
        await bot.say('GM đã khóa lệnh nhặt đồ vật.')
        return

    if item=="":
        await bot.say("Bạn muốn lấy đồ vật gì? Gõ ``!pickup Tên đồ vật`` ví dụ ``!pickup ly nước`` để lấy đồ vật.")
    else:
        location_items = get_location_items(ctx.message.channel.id)
        if location_items is None:
            await bot.say('Unauthorized.')
            return

        location_name = LOCATION_ITEM[ctx.message.channel.id]['name']

        item = str.strip(item.lower())
        has_item = False
        item_name = ""
        item_desc = ""
        item_location = ""
        item_hidden = ""

        first_name = ""

        for location_item in location_items:
            names = location_item["name"].split(",")
            num = location_item.get("num", 0)
            if num <= 0:
                continue
            stripped_names = map(str.strip, map(str.lower, names))
            if item in stripped_names:
                has_item = True
                item_name = location_item["name"]
                item_desc = location_item.get("desc", "???")
                item_location = location_name
                item_hidden = location_item.get("hidden", 0)
                location_item["num"] -= 1
                first_name = names[0]
                break

        if has_item:
            added = add_user_item(ctx.message.author.id, item_name, item_desc, item_location, item_hidden)
            if added:
                await bot.say(ctx.message.author.nick + " vừa lấy **" + first_name + "** bỏ vào túi.")
            else:
                await bot.say('Túi của ' + ctx.message.author.nick + ' đã đầy. Bạn không thể lấy thêm đồ được nữa. Sử dụng ``!drop`` để vứt bớt đồ trong túi.')
        else:
            await bot.say("...")


@bot.command(pass_context=True)
async def drop(ctx, *, item=""):
    """Vứt bỏ đồ vật có trong túi.
    Bạn hoặc người khác có thể nhặt lại đồ vật này khi nói !pickup Tên đồ vật ở nơi bạn đã vứt."""

    if item=="":
        await bot.say("Bạn muốn vứt đồ vật nào? Gõ ``!drop Tên đồ vật`` ví dụ ``!drop ly nước`` để vứt bỏ đồ vật trong túi.")
    else:
        user_items = USER_ITEM[ctx.message.author.id]['items']
        has_item = False
        not_used = True
        item_name = ""
        item = str.strip(item.lower())

        for i in range(0, len(user_items)):
            user_item = user_items[i]
            names = user_item['name'].split(',')
            stripped_names = map(str.strip, map(str.lower, names))

            if item in stripped_names:
                has_item = True

                if True: #or user_item['status'] == 'Chưa sử dụng':
                    not_used = True

                    item_name = names[0]
                    item_desc = user_item.get('desc', '???')
                    item_hidden = user_item.get('hidden', 0)

                    added = add_location_item(ctx.message.channel.id, item_name, item_desc, item_hidden)

                    if added:
                        user_items.pop(i)
                        save_user_item()

                    else:
                        await bot.say('Không thể vứt bỏ đồ vật ở đây.')
                        return

                    break
                else:
                    item_name = names[0]
                    not_used = False

        if has_item:
            if not_used:
                await bot.say(
                    ctx.message.author.nick +
                    " vừa vứt bỏ **" + item_name + "**.")
            else:
                await bot.say("**" + item_name + "** đã được sử dụng và đang chờ GM xác nhận, bạn không thể vứt vật dụng này bây giờ.")

        else:
            await bot.say("Bạn không có **" + item + "** trong túi. Gõ ``!bag`` để kiểm tra và gõ đúng tên đồ vật.")


@bot.command(pass_context=True)
async def use(ctx, *, item=""):
    """Sử dụng đồ vật có trong túi.
    GM sẽ được thông báo và xác nhận việc sử dụng đồ vật của bạn."""

    if ONBREAK:
        await bot.say('Chỉ có thể sử dụng đồ vật từ 9h đến 12h đêm khi có mặt GM để kiểm chứng.')
        return

    if item=="":
        await bot.say("Bạn muốn sử dụng gì? Gõ ``!use Tên đồ vật`` ví dụ ``!use cái nĩa`` để sử dụng đồ vật.")
    else:
        user_items = get_user_items(ctx.message.author.id)
        if user_items is None:
            await bot.say('Unauthorized.')
            return

        has_item = False
        item = str.strip(item.lower())
        item_name = ""

        for user_item in user_items:

            names = user_item["name"].split(",")
            stripped_names = map(str.strip, map(str.lower, names))

            if item in stripped_names:
                has_item = True
                item_name = names[0]
                #user_item['status'] = 'Đã sử dụng, đang đợi GM xác nhận'
                save_user_item()
                break

        if has_item:
            await bot.say(
                ctx.message.author.nick +
                " đã sử dụng **" + item_name +
                "**. Hãy inbox <@" + OANH_ID + "> để xác nhận bạn muốn sử dụng đồ vật này như thế nào.")

        else:
            await bot.say("Bạn không có **" + item + "** trong túi. Gõ ``!bag`` để kiểm tra và gõ đúng tên đồ vật.")


@bot.command(pass_context=True)
async def bag(ctx, public=""):
    """Xem túi của mình."""

    items = get_user_items(ctx.message.author.id)

    if items is None:
        await bot.say("Unauthorized.")
        return

    item_string = "```markdown\n#========== Túi của " + ctx.message.author.nick + " ==========#\n\n"

    if len(items) <= 0:
        item_string = item_string + "Không có gì trong này.\n\nTúi của bạn còn chứa được 7 món đồ nữa.```"

    else:
        count = 0
        for item in items:
            count+=1
            first_name = item["name"].split(",")[0]
            name = str(count)+ ". " + first_name
            desc = "|--Mô tả: " + item.get('desc', '???')
            location = "|--Nhặt được ở: " + item.get('location', '???')
            #status = "|--Tình trạng: " + item.get('status', 'Chưa sử dụng')
            item_string += name + "\n" + desc + "\n" + location + "\n\n" #+ status + "\n\n"

        item_string = item_string + "Túi của bạn còn chứa được " + str(7- len(items)) + " món đồ nữa.```"

    if public == "public":
        await bot.say(item_string)
    else:
        await bot.send_message(ctx.message.author, content=item_string)
        await bot.say(ctx.message.author.nick + " vừa mở túi ra xem. Hãy kiểm tra inbox của bạn.")


@bot.command(pass_context=True)
async def goto(ctx, *, location):
    """Nói !goto Tên tầng - Tên vị trí  để chuyển sang vị trí mới.
     VD: !goto Tầng 1 - 1-A
     Bạn có thể chuyển vị trí mỗi giờ.
     Gõ !showmap để xem danh sách tên vị trí. Hãy nhớ gõ đúng tên vị trí."""

    if not SET_UP:
        print('Bot is not set up!')
        return

    if JUDGEMENT:
        await bot.say('...')
        return

    global LOCATION_ROLE, PLAYER_ROLE_ID, USER_MOVE

    author = ctx.message.author

    await bot.delete_message(ctx.message)

    user_move = USER_MOVE.get(author.id, "Not found")

    if user_move == "Not found":
        print('Unauthorized.')
        return

    last_move_string = user_move['time']

    if last_move_string:
        last_move_time = datetime.strptime(last_move_string,'%H:%M:%S %d/%m/%y')

        if last_move_time.hour == ctx.message.timestamp.hour and last_move_time.date() == ctx.message.timestamp.date():
            await bot.say('Chưa đến thời gian được chuyển phòng.')
            return

    location_stripped = location.lower().replace(" ","")
    loc = LOCATION_ROLE.get(location_stripped, None)

    if loc is None:
        await bot.say('Tên vị trí không chính xác.\n'
                      'Gõ ``!goto Tên tầng - Tên vị trí``.\n'
                      'Gõ ``!showmap`` để xem chính xác tên vị trí và thử lại.')
        return

    new_channel = ctx.message.server.get_channel(loc['locationid'])

    if new_channel == ctx.message.channel:
        await bot.say('Bạn hiện đang ở ' + location + '. Hãy di chuyển đến vị trí mới.')
        return

    if not loc['isopen']:
        await bot.say('Vị trí này hiện đang bị khóa.')
        return

    #current_role_in_author = list(filter(lambda x: x.id not in EXCLUDE_ROLE, author.roles))[0]
    #current_role = utils.find(lambda x: x.id == current_role_in_author.id, ctx.message.server.roles)
    new_role = utils.find(lambda x: x.id == loc['roleid'], ctx.message.server.roles)


    #await bot.add_roles(author, new_role)

    #if current_role is not None:
        #await bot.remove_roles(author, current_role)

    await bot.replace_roles(author, PLAYER_ROLE, new_role)

    USER_MOVE[author.id]['time'] = ctx.message.timestamp.strftime("%H:%M:%S %d/%m/%y")

    save_user_move()

    location_old = LOCATION_ITEM[ctx.message.channel.id]['name']

    await bot.say(author.nick + ' đã rời khỏi [' + location_old.title() + '].')
    await bot.send_message(new_channel, content=(author.nick + ' đã vào [' + location.title() + ']'))
    await bot.send_message(SECRET_CH, content=(author.nick + ' đi từ ['+ location_old.title() +'] đến [' + location.title() + ']'))


@bot.command()
async def showmap():
    """Hiển thị danh sách phòng."""
    global MAP
    await bot.say(MAP)


@bot.command()
async def judgement():
    if ONBREAK:
        await bot.say('Chỉ có thể mở phiên tòa từ 9h đến 12h đêm khi có mặt GM để kiểm chứng.')
        return

    await bot.say('Bạn muốn buộc tội ai? <@' + OANH_ID + '>')


def get_user_items(user_id):
    global USER_ITEM
    user = USER_ITEM.get(user_id, None)
    if user is not None:
        items = user.get('items', None)
        if items is not None:
            return items
        else:
            user['items'] = []
            save_user_item()
            return []

    return None

'''
def get_user_moves(user_id):
    global USER_MOVE
    user = USER_MOVE.get(user_id, None)
    if user is not None:
        moves = user.get('moves', None)
        if moves is not None:
            return moves
        else:
            user['moves'] = []
            save_user_move()
            return []

    return None
'''


def get_location_items(location_id):
    global LOCATION_ITEM
    location = LOCATION_ITEM.get(location_id, None)
    if location is not None:
        items = location.get('items', None)
        if items is not None:
            return items
        else:
            location['items'] = []
            save_location_item()
            return []

    return None


def add_user_item(user_id, name, desc, location, hidden):
    global USER_ITEM
    user = USER_ITEM.get(user_id, None)

    if user is None:
        return False

    items = user.get('items', None)
    if items is None:
        user['items'] = []

    items = user['items']

    if len(items) < 7:
        item = {"name": name, "desc": desc, "location": location, "hidden": hidden} #"status": "Chưa sử dụng",
        items.append(item)
        save_user_item()
        return True

    else:
        return False


def add_location_item(location_id, name, desc, hidden):
    global LOCATION_ITEM
    location = LOCATION_ITEM.get(location_id, None)

    if location is None:
        return False

    item = {"name": name, "desc": desc, "num": 1, "hidden": hidden}

    items = location.get('items', None)
    if items is None:
        location['items'] = []

    items = location['items']
    items.append(item)
    save_location_item()

    return True

'''
def move_user(user, current_role, new_role, location, timestamp):
    if current_role is not None:
        bot.remove_roles(user, [current_role])

    bot.add_roles(user, [new_role])

    user_moves = get_user_moves(user.id)
    move = {'location': location, 'time': timestamp.strftime("%Y/%m/%d %H:%M:%S")}
    user_moves.append(move)
    save_user_move()
'''


def save_user_item():
    global USER_ITEM
    json.dump(USER_ITEM, open('user_item.json', 'w+'))


def save_location_item():
    global LOCATION_ITEM
    json.dump(LOCATION_ITEM, open('location_item.json', 'w'))


def save_user_move():
    global USER_MOVE
    json.dump(USER_MOVE, open('user_move.json', 'w+'))


bot.run("NDA1NjAxMzY4Nzc1MTk2Njcy.DVDRaQ.7tPyU4aLfl7niB8cUFBGcIuupmQ")