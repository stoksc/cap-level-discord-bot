from discord.ext.commands import Bot
import discord
import bs4 as bs
import urllib.request
import secrets
import data

caplevel_bot = Bot(command_prefix="!")


@caplevel_bot.event
async def on_read():
    print("Client logged in")


@caplevel_bot.command()
async def hello(*args):
    return await caplevel_bot.say("Hello world!")


@caplevel_bot.command()
async def echo(*args):
    print(args)
    try:
        return await caplevel_bot.say(args[0])
    except:
        return await caplevel_bot.say("Nothing to echo.")


@caplevel_bot.command()
async def guide(*args):
    try:
        # preparing the url from the input args
        url = "http://www.wowhead.com/search?q="
        for part in args:
            url += (str(part) + "+")
        url = url[:-1]

        # retrieving the page html
        sauce = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        result = soup.find("a", {"class": "withimg"}).get("href")
        result_url = "http://www.wowhead.com{}".format(result)

        # printing the url to the user
        return await caplevel_bot.say(result_url)

    except:
        return await caplevel_bot.say("Please enter an item.")


@caplevel_bot.command()
async def item(*args):
    try:
        # preparing the url from the input args
        url = "http://www.wowdb.com/search?search="
        url2 = "#t1:items"
        for part in args:
            url += (str(part) + "+")
        url = url[:-1]
        url += url2

        # retrieving the page html from wowdb.com
        # setting the color
        sauce = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q0 t").get(
                "href")
            qual = 0x9d9d9d
        except:
            pass
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q1 t").get(
                "href")
            qual = 0xFFFFFF
        except:
            pass
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q2 t").get(
                "href")
            qual = 0x1EFF00
        except:
            pass
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q3 t").get(
                "href")
            qual = 0x0080FF
        except:
            pass
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q4 t").get(
                "href")
            qual = 0xB048F8
        except:
            pass
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q5 t").get(
                "href")
            qual = 0xFF8000
        except:
            pass
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q6 t").get(
                "href")
            qual = 0xE6CC80
        except:
            pass
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q7 t").get(
                "href")
            qual = 0x00CCFF
        except:
            pass

        # em = discord.Embed(title=)

        # retrieving the item image from the second url
        sauce = urllib.request.urlopen(new_href)
        soup = bs.BeautifulSoup(sauce, 'lxml')

        # creating an array with the contents of the item description
        thumbnail = "http:" + soup.find("img", class_="icon-56").get("src")
        info = soup.find("dl", class_="db-summary").text.split("\n")
        new_info = []
        for item in info:
            temp_item = item.strip().strip("\r")
            if temp_item == '':
                pass
            else:
                new_info.append(temp_item)

        # creating a formatted string for the embed description kwarg
        formatted_string = ''
        title = new_info[0]
        i = 1
        while i < len(new_info) - 3:
            if new_info[i + 1] in data.primary_stats:
                formatted_string += (new_info[i] + " **" + new_info[i+1] + "**\n")
                i += 2
            elif new_info[i + 1] in data.secondary_stats:
                if new_info[i+2][0] == "(":
                    formatted_string += (new_info[i] + " **" + new_info[i+1] + "** " + new_info[i + 2] + "\n")
                    i += 3
                else:
                    formatted_string += (new_info[i] + " **" + new_info[i+1] + "**\n")
                    i += 2
            elif new_info[i] == 'Equip:' or new_info[i] == 'Chance on hit:':
                formatted_string += ("\n" + new_info[i] + " " + new_info[i+1] + "\n")
                i += 2
            elif (new_info[i][::-1][0:6] == 'egamaD'):
                temp_string = new_info[i] + ' '*40
                formatted_string += (temp_string[0:37] + new_info[i+1].rjust(30) + "\n")
                i += 2
            elif (new_info[i+1] in data.weapon_types):
                temp_string = new_info[i] + ' '*40
                formatted_string += (temp_string[0:40] + new_info[i+1].rjust(30) + "\n")
                i += 2
            elif (new_info[i][::-1][0:6] == 'tekcoS'):
                formatted_string += ':white_small_square: ' + new_info[i] + "\n"
                i += 1
            else:
                formatted_string += (new_info[i] + "\n")
                i += 1
        if new_info[len(new_info) - 3][0] == "\"":
            formatted_string += ("\n*" + new_info[len(new_info) - 3] + "*")
        else:
            pass
        em = discord.Embed(title='', description=formatted_string, colour=qual, url=new_href)
        em.set_author(name=title)
        em.set_thumbnail(url=thumbnail)
        # preparing the discord markdown text block
        return await caplevel_bot.say(embed=em)
    except:
        await caplevel_bot.say(url)
        return await caplevel_bot.say(":anger: Something went wrong :/")

caplevel_bot.run(secrets.BOT_TOKEN)
