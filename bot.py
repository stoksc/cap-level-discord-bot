'''
Author: Bradley Laney
Date: 11/01/2017

Description:
This program uses the Discord's python module to interact with a discord server and give information
to the user like:
    !guide
        This command posts to a discord server with a url to a guide matching the query
    !player
        This command posts information on the player on the designated server
    !spell
        This command posts information on the spell matching the query
'''

# standard library imports
import urllib.request
import os

# related third party imports
from discord.ext.commands import Bot
import discord
import bs4 as bs

# library specific imports
import secrets
import data
import cacher

# setup directories for caching query result embeds
for dir_name in ('spell', 'guide', 'player', 'item'):
    full_dir_name = '{}\\{}'.format(os.getcwd(), dir_name)
    try:
        os.mkdir(full_dir_name)
    except FileExistsError:
        os.rmdir(full_dir_name)
        os.mkdir(full_dir_name)

# set the prefix for the bot commands
caplevel_bot = Bot(command_prefix='!caplevel ')

@caplevel_bot.command()
async def guide(*args):
    '''
    Command:
        !caplevel guide <query>
    This command constructs a URL from the <query> and posts a URL to a guide from a search of wowhead.com
    '''

    # see if query already exists and uncache if so
    cached_query =  cacher.uncache_embed('guide',''.join(args))
    if cached_query is not None:
        return await caplevel_bot.say(cached_query)

    # preparing the url from the input args
    url = 'http://www.wowhead.com/search?q='
    for part in args:
        url += (str(part) + '+')
    url = url[:-1]

    # retrieving the page html
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    prelim_result = soup.find('a', {'class': 'withimg'})
    if prelim_result is None:
        return await caplevel_bot.say(":anger: 404 Guide not found.")
    result = prelim_result.get('href')
    result_url = 'http://www.wowhead.com{}'.format(result)

    # cache the result
    cacher.cache_embed(result_url,'guide',''.join(args))

    # printing the url to the user
    return await caplevel_bot.say(result_url)

@caplevel_bot.command()
async def spell(*args):
    '''
    Command:
        !caplevel spell <query> <arg1>
    This command constructs a URL from the query, searches wowdb.com and posts
    a discord.Embed of the <arg1>'th entry in the search return.
    '''

    # see if query already exists and uncache if so
    cached_query =  cacher.uncache_embed('spell',''.join(args))
    if cached_query is not None:
        return await caplevel_bot.say(embed=cached_query)

    # check if args were passed
    if args == ():
        return await caplevel_bot.say('I need something to search.')

    # preparing the specific spell url from the input args
    url = 'http://www.wowdb.com/search?search='
    url2 = '#t1:abilities'
    entry = None
    if str(args[-1:][0]).isnumeric():
        entry = args[len(args)-1]
        for part in args[:-1:]:
            url += (str(part) + '+')
    else:
        for part in args:
            url += (str(part) + '+')
    url = url[:-1]
    url += url2

    # retrieving the page html from wowdb.com
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')
    spell_table = soup.find('table', class_='listing listing-spells b-table b-table-a')
    if spell_table is not None:
        spell_table_entries = spell_table.find_all('a', class_='listing-icon ')
    else:
        return await caplevel_bot.say(":anger: 404 Spell not found.")

    # handle multiple options
    href_list = []
    clarifying_str = ''
    for spell_cell_entry in spell_table_entries:
        href_list.append(spell_cell_entry.get('href'))
    if (len(href_list) == 1):
        new_href = href_list[0]
    elif ((len(href_list) > 1) and (entry is None)) or ((int(entry) >= (len(href_list)))):
        if entry is not None:
            clarifying_str += 'You requested entry {}. '.format(entry)
        new_href = href_list[0]
        clarifying_str += 'There were {} different options for the query. '\
            '\nTo get the correct option enter !*spellname* *option#*'\
            .format(len(href_list))
        for i, spell_href in enumerate(href_list):
            clarifying_str += '\n\t {}. {}'.format(i, spell_href)
    else:
        new_href = href_list[int(entry)]

    # retrieving the soup from wowdb.com for the spell
    sauce = urllib.request.urlopen(new_href).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')

    # creating an array with the contents of the item description
    thumbnail = 'http:' + soup.find('img', class_='icon-56 ').get('src')
    new_info = soup.find('div', class_='db-description')
    tooltip_table = new_info.find('table', class_='tooltip-table').find_all('tr')
    formatted_string = ''

    # goes through the table to retrieve the relevant spell information
    first = True
    for tr in tooltip_table:
        temp_arr = []
        for td in tr.find_all('td'):
            if first:
                title = td.text
                first = False
                wow_class = tr.find_all('td')[1].text.split()[0]
                break
            temp_arr.append(td.text)
        try:
            temp_string = temp_arr[0] + ' ' * 80
            formatted_string += temp_string[0:80] + temp_arr[1].rjust(0) + '\n'
        except:
            try:
                formatted_string += temp_arr[0] + '\n'
            except:
                pass
    formatted_string += (new_info.find('dl', class_='db-details').text + '\n')
    formatted_string += ('*' + new_info.find('p', class_='yellow').text + '*\n')
    if wow_class in data.wow_class_colors:
        qual = data.wow_class_colors[wow_class]
    else:
        qual = 0x000000

    # formatting the embedded object and printing it to the user
    em = discord.Embed(title='', description=formatted_string + '\n' + clarifying_str, colour=qual, url=new_href)
    em.set_author(name=title)
    em.set_thumbnail(url=thumbnail)

    # cache the result
    cacher.cache_embed(em,'spell',''.join(args))
    return await caplevel_bot.say(embed=em)


@caplevel_bot.command()
async def item(*args):
    '''
    Command:
        !caplevel <item>
    Uses the <item> queried to access wowdb.com, gather information on the closest matching item
    and format and post a discord.Embed item.
    '''

    # see if query already exists and uncache if so
    cached_query =  cacher.uncache_embed('item',''.join(args))
    if cached_query is not None:
        return await caplevel_bot.say(embed=cached_query)

    # preparing the url from the input args
    url = 'http://www.wowdb.com/search?search='
    url2 = '#t1:items'
    for part in args:
        url += (str(part) + '+')
    url = url[:-1]
    url += url2

    # retrieving the page html from wowdb.com
    sauce = urllib.request.urlopen(url).read()
    soup = bs.BeautifulSoup(sauce, 'lxml')

    # set item quality and get item url
    try:
        for i, quality in enumerate(data.qualities):
            item_table = soup.find('table', class_='listing listing-items b-table b-table-a')
            item_table_entry = item_table.find('a', class_='q{} t'.format(i))
            if item_table_entry is not None:
                new_href = item_table_entry.get('href')
                qual = quality
                break
    except AttributeError:
        return_str = ':anger: 404 Item not found.'
        return await caplevel_bot.say(return_str)

    # return the soup for the page of the item that was selected by the prior try/catch statements
    sauce = urllib.request.urlopen(new_href)
    soup = bs.BeautifulSoup(sauce, 'lxml')


    # grabs the thumbnail of the item from the soup of the page is a sort of dangerous way
    thumbnail = 'http:' + soup.find('img', class_='icon-56').get('src')

    # goes through the summary of the item in the 'db-summary' tag and makes an array of the information
    info = soup.find('dl', class_='db-summary').text.split('\n')
    new_info = []
    for item in info:
        temp_item = item.strip().strip('\r')
        if temp_item == '':
            pass
        else:
            new_info.append(temp_item)

    # creating a formatted string for the embedded object
    formatted_string = ''
    title = new_info[0]
    i = 1
    while i < len(new_info) - 3:
        if new_info[i + 1] in data.primary_stats:
            formatted_string += (new_info[i] + ' **' + new_info[i+1] + '**\n')
            i += 2
        elif new_info[i + 1] in data.secondary_stats:
            if new_info[i+2][0] == '(':
                formatted_string += (new_info[i] + ' **' + new_info[i+1] + '** ' + new_info[i + 2] + '\n')
                i += 3
            else:
                formatted_string += (new_info[i] + ' **' + new_info[i+1] + '**\n')
                i += 2
        elif new_info[i] == 'Equip:' or new_info[i] == 'Chance on hit:' or new_info[i] == 'Use:':
            formatted_string += ('\n' + new_info[i] + ' ' + new_info[i+1] + '\n')
            i += 2
        elif new_info[i][::-1][0:6] == 'egamaD':
            temp_string = new_info[i] + ' '*40
            formatted_string += (temp_string[0:37] + new_info[i+1].rjust(30) + '\n')
            i += 2
        elif new_info[i+1] in data.weapon_types:
            temp_string = new_info[i] + ' '*40
            formatted_string += (temp_string[0:40] + new_info[i+1].rjust(30) + '\n')
            i += 2
        elif new_info[i][::-1][0:6] == 'tekcoS':
            formatted_string += ':white_small_square: ' + new_info[i] + '\n'
            i += 1
        elif new_info[i] in data.armor_pieces:
            temp_string = new_info[i] + ' '*40
            formatted_string += (temp_string[0:37] + new_info[i+1].rjust(30) + '\n')
            i += 2
        elif new_info[i][0] == '(':
            formatted_string += '*' + new_info[i][0:3] + ' Set: ' + new_info[i+2] + '*\n'
            i += 3
        else:
            formatted_string += (new_info[i] + '\n')
            i += 1

    # specifically checks the end of the info array for flavour text
    if new_info[len(new_info) - 3][0] == '\'':
        formatted_string += ('\n*' + new_info[len(new_info) - 3] + '*')

    # creates the embed object from all the information gathered in the prior steps
    em = discord.Embed(title='', description=formatted_string, colour=qual, url=new_href)
    em.set_author(name=title)
    em.set_thumbnail(url=thumbnail)

    # spits it out to the user

    # cache the result
    cacher.cache_embed(em,'item',''.join(args))
    return await caplevel_bot.say(embed=em)

# player stats pulled from wowprogress.com
@caplevel_bot.command()
async def player(*args):
    """
    Command:
        !caplevel <server> <player>
    This command takes a <server> and <player> and formats a wowprogress.com url to find the player
    on the specified server. It then uses the player information to create a discord.Embed object
    and posts it to the server.
    """

    # see if query already exists and uncache if so
    cached_query =  cacher.uncache_embed('player',''.join(args))
    if cached_query is not None:
        return await caplevel_bot.say(embed=cached_query)

    # create the url from the player to search
    url = "https://www.wowprogress.com/character/us/"
    for arg in args:
        url += arg + "/"

    # pull the url for the player from the query url
    sauce = urllib.request.urlopen(url)
    soup = bs.BeautifulSoup(sauce, 'lxml')

    # pull the data from the player url from the table on the page
    # while formatting it in an acceptable fashion
    formatted_string = ''
    table_arr = soup.find("div", id='tiers_details')
    if table_arr is None:
        return_str = '404 Player not found.'
        return await caplevel_bot.say(return_str)
    player_table = table_arr.find_all("table", class_="rating")
    for table in player_table:
        for tr in table.find_all("tr"):
            for index, td in enumerate(tr):
                cell_content = td.text
                cell_content_ed = ' '.join(str(string_part) for string_part in cell_content
                                           .split()[0:len(cell_content.split()) - 1])
                if cell_content in data.header:
                    pass
                elif cell_content in data.released_raids:
                    formatted_string += "\n```" + cell_content + "```"
                elif cell_content_ed in data.released_bosses:
                    formatted_string += "\t" + cell_content_ed + " *" + cell_content\
                                        .split()[len(cell_content.split()) - 1] + "*"
                else:
                    if len(cell_content.split()) >= 2:
                        if cell_content.split()[1] == "days" or "months" or "month" or "day" or "hour" or "hours":
                            formatted_string += "\t(" + cell_content + ")\n"

    # create the embed object (looks nicer)
    em = discord.Embed(title='', description=formatted_string, url=url, color=0xE6CC80)
    em.set_author(name=args[1] + " on " + args[0])

    # return the formatted string from the data to the user
    cacher.cache_embed(em, 'player',''.join(args))
    return await caplevel_bot.say(embed=em)

# run the bot
caplevel_bot.run(secrets.BOT_TOKEN)
