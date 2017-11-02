# cap-level-discord-bot
simple, terribly written bot that does stuff for people who play WoW and use discord. Can respond to queries about players, spells, items and guides. Goes through a lot of trouble to webscrape the data from wowdb.com and wowhead.com; later versions would be made using Blizzard's API but this was more for an exercise in webscraping for me.

## Examples
![!caplevel spell *spellname* *entryno*](/examples/spell_ex.png)
![!caplevel item *itemname*](/examples/item_ex.png)
![!caplevel player *server* *playername*](/examples/player_ex.png)
![!caplevel guide *guidename*](/examples/guide_ex.png)

## Getting Started

#### If you want, for some odd reason, to run this on your machine, here's how:
1. Make sure you have a Python3 environment installed with lxml, BeautifulSoup4 and discord packages installed.
2. After this is done, go to discord.com and login. Scroll to the bottom of the home page and click developers.
3. Click Add Bot. Name your bot and generate a secret key and a token.
4. Fork this repo and activate the Python3 environment.
5. Open secrets.py and replace the secret key and token with yours.
6. Run bot.py, add the bot to your channel and enjoy? Or be frustrated.

## Built With

* [discord](https://github.com/Rapptz/discord.py) - An API wrapper for Discord written in Python.
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) - A Python package for webscraping and more.

## Authors

* **Bradley Laney** - *Initial work* - [Lieblos](https://github.com/stoksc)
## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to @meowki for the idea.
