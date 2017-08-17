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

# basic command
@caplevel_bot.command()
async def hello(*args):
    return await caplevel_bot.say("Hello world!")

# testing an echo command
@caplevel_bot.command()
async def extra(*args):
    try:
        return await caplevel_bot.say(args[0])
    except:
        return await caplevel_bot.say("Nothing extra needed.")

# command that takes args and returns a guide link on wowhead.com
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

        # general catch returns that something went wrong
        return await caplevel_bot.say("Please enter an item.")

# command that takes *args and prints an embedded spell description to the user's discord channel
@caplevel_bot.command()
async def spell(*args):
    try:
        # preparing the specific spell url from the input args
        url = "http://www.wowdb.com/search?search="
        url2 = "#t1:abilities"
        entry = 0
        if str(args[-1:][0]).isnumeric():
            entry = args[len(args)-1]
            for part in args[:-1:]:
                url += (str(part) + "+")
        else:
            for part in args:
                url += (str(part) + "+")
        url = url[:-1]
        url += url2

        # retrieving the page html from wowdb.com
        # setting the color
        sauce = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        try:
            new_href = soup.find("table", class_="listing listing-spells b-table b-table-a").find_all("a", class_="listing-icon ")
            try:
                href_list = []
                for href in new_href:
                    href_list.append(href.get("href"))
                if len(href_list) > 1:
                    await caplevel_bot.say("There were {} different options for the query. To get a different option enter !(query) (option#)".format(len(href_list)))
                if entry == 0:
                    raise()
                else:
                    try:
                        new_href = href_list[int(entry)]
                    except:
                        new_href = href_list[0]
            except:
                new_href = soup.find("table", class_="listing listing-spells b-table b-table-a").find("a", class_="listing-icon ").get("href")
        except:
            pass

        # retrieving the soup from wowdb.com for the spell
        sauce = urllib.request.urlopen(new_href).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')

        # creating an array with the contents of the item description
        thumbnail = "http:" + soup.find("img", class_="icon-56 ").get("src")
        new_info = soup.find("div", class_="db-description")
        tooltip_table = new_info.find("table", class_="tooltip-table").find_all("tr")
        formatted_string = ""

        # goes through the table to retrieve the relevant spell information
        try:

            first = True
            for tr in tooltip_table:
                temp_arr=[]
                for td in tr.find_all("td"):
                    if first:
                        title = td.text
                        first = False
                        try:
                            wow_class = tr.find_all("td")[1].text.split()[0]
                        except:
                            pass
                        break
                    temp_arr.append(td.text)
                    # crazy formatting magic
                try:
                    temp_string = temp_arr[0] + " " * 80
                    formatted_string += temp_string[0:80] + temp_arr[1].rjust(0) + "\n"
                except:
                    try:
                        formatted_string += temp_arr[0] + "\n"
                    except:
                        pass
        except:
            # go back and add error messages to all except statements -_-
            pass

        # adds the in the information from the "db-details" block
        try:
            formatted_string += (new_info.find("dl", class_="db-details").text + "\n")
        except:
            pass

        # adds in the spell description from the class="yellow" block
        try:
            formatted_string += ("*" + new_info.find("p", class_="yellow").text + "*\n")
        except:
            pass

        try:
            qual = data.wow_class_colors[wow_class]
        except:
            qual = 0x000000


        # formatting the embedded object and printing it to the user
        em = discord.Embed(title='', description=formatted_string, colour=qual, url=new_href)
        em.set_author(name=title)
        em.set_thumbnail(url=thumbnail)
        return await caplevel_bot.say(embed=em)

    except:

        # super generalized error message catching anything that went from so that the entire bot doesn't
        # shutdown on an error
        await caplevel_bot.say(new_href)
        return await caplevel_bot.say(":anger: Something went wrong :/")


# takes an input in the for of !spell (spell query) and returns a formatted embedded
# object that displays the object in a 'pretty' way
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

        # retrieving the page html from wowdb.com. based on how the page it retrieved (on which class_=(quality_label) works)
        # sets the color (qual) to the correct item quality color e.g. orange, purple, ect.
        sauce = urllib.request.urlopen(url).read()
        soup = bs.BeautifulSoup(sauce, 'lxml')
        # try for the '0' quality
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q0 t").get(
                "href")
            qual = 0x9d9d9d
        except:
            pass
        # try for the '1' quality
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q1 t").get(
                "href")
            qual = 0xFFFFFF
        except:
            pass
        # try for the '2' quality
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q2 t").get(
                "href")
            qual = 0x1EFF00
        except:
            pass
        # try for the '3' quality
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q3 t").get(
                "href")
            qual = 0x0080FF
        except:
            pass
        # try for the '4' quality
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q4 t").get(
                "href")
            qual = 0xB048F8
        except:
            pass
        # try for the '5' quality
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q5 t").get(
                "href")
            qual = 0xFF8000
        except:
            pass
        # try for the '6' quality
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q6 t").get(
                "href")
            qual = 0xE6CC80
        except:
            pass
        # try for the '7' quality
        try:
            new_href = soup.find("table", class_="listing listing-items b-table b-table-a").find("a", class_="q7 t").get(
                "href")
            qual = 0x00CCFF
        except:
            pass

        # inherit in the way it works, it selects the highest
        # quality available from the search results
        # may be eventually useful to allow more particular selection of items (based on class, rarity, ect.)


        # return the soup for the page of the item that was selected by the prior try/catch statements
        sauce = urllib.request.urlopen(new_href)
        soup = bs.BeautifulSoup(sauce, 'lxml')


        # grabs the thumbnail of the item from the soup of the page is a sort of dangerous way
        thumbnail = "http:" + soup.find("img", class_="icon-56").get("src")

        # goes through the summary of the item in the 'db-summary' tag and makes an array of the information
        # carefully strips out spaces, returns and newlines
        info = soup.find("dl", class_="db-summary").text.split("\n")
        new_info = []
        for item in info:
            temp_item = item.strip().strip("\r")
            if temp_item == '':
                pass
            else:
                new_info.append(temp_item)

        # creating a formatted string for the embedded object --- this is the majority of the content.
        # does a lot of sloppy work to identify special parts expected in the description to format them
        # as i saw as most visually pleasing
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
            elif new_info[i] == 'Equip:' or new_info[i] == 'Chance on hit:' or new_info[i] == 'Use:':
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
            elif (new_info[i] in data.armor_pieces):
                temp_string = new_info[i] + ' '*40
                formatted_string += (temp_string[0:37] + new_info[i+1].rjust(30) + "\n")
                i += 2
            elif (new_info[i][0] == '('):
                formatted_string += "*" + new_info[i][0:3] + " Set: " + new_info[i+2] + "*\n"
                i += 3

            else:
                formatted_string += (new_info[i] + "\n")
                i += 1

        # specifically checks the end of the info array for flavour text
        if new_info[len(new_info) - 3][0] == "\"":
            formatted_string += ("\n*" + new_info[len(new_info) - 3] + "*")
        else:
            pass

        # creates the embed object from all the information gathered in the prior steps
        em = discord.Embed(title='', description=formatted_string, colour=qual, url=new_href)
        em.set_author(name=title)
        em.set_thumbnail(url=thumbnail)

        # spits it out to the user
        return await caplevel_bot.say(embed=em)
    except:

        # if something went wrong in any of the before mentioned steps it throws an error but returns what
        # it thinks is the url to the wowdb.com from the item
        await caplevel_bot.say(url)
        return await caplevel_bot.say(":anger: Something went wrong :/")

# player stats pulled from wowprogress.com
@caplevel_bot.command()
async def player(*args):
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
    table_arr = soup.find("div",id='tiers_details').find_all("table", class_="rating")
    for table in table_arr:
        for tr in table.find_all("tr"):
            for td in tr:
               # if td[::-1][0:6] ==
            print("\nnewtr\n")
            formatted_string += "\n"

    # return the formatted string from the data to the user
    return await caplevel_bot.say(formatted_string)

caplevel_bot.run(secrets.BOT_TOKEN)
