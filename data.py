import discord

primary_stats = ['Stamina','Agility','Intellect','Strength']
secondary_stats = ['Critical Strike','Haste','Mastery','Avoidance','Versatility','Leech','Speed','Fire Resistance', 'Nature Resistance',
                   'Agility/Intellect', 'Strength/Agility/Intellect', 'PvP Resilience']
weapon_types = ['Axe','Mace','Staff','Sword','Polearm','Dagger']
wow_class_colors = {
                       'Shaman': 0x0070DE,
                       'Warlock': 0x9482C9,
                       'Mage': 0x69CCF0,
                       'Rogue': 0xFFF569,
                       'Warrior': 0xC79C6E,
                       'Druid': 0xFF7D0A,
                       'Demon': 0xA330C9,
                       'Death': 0xC41F3B,
                       'Paladin': 0xF58CBA,
                       'Priest': 0xFFFFFF,
                       'Hunter': 0xABD473,
                       'Monk': 0x00FF96
}

armor_pieces = ['Head','Shoulders','Chest','Waist','Wrist','Hands','Legs','Waist','Feet']

released_raids = {"Tomb of Sargeras Bosses",
                  "The Emerald Nightmare Bosses",
                  "Trial of Valor Bosses",
                  "The Nighthold Bosses"}

released_bosses = {"Goroth",
                   "Demonic Inquisition",
                   "Harjatan",
                   "Sisters of the Moon",
                   "Mistress Sassz'ine",
                   "The Desolate Host",
                   "Maiden of Vigilance",
                   "Fallen Avatar",
                   "Kil'jaeden",
                   "Nythendra",
                   "Elerethe Renferal",
                   "Il'gynoth, Heart of Corruption",
                   "Ursoc",
                   "Dragons of Nightmare",
                   "Cenarius",
                   "Xavius",
                   "Odyn",
                   "Guarm",
                   "Helya",
                   "Skorpyron",
                   "Chronomatic Anomaly",
                   "Trilliax",
                   "Spellblade Aluriel",
                   "Tichondrius",
                   "Krosus",
                   "High Botanist Tel'arn",
                   "Star Augur Etraeus",
                   "Grand Magistrix Elisande",
                   "Gul'dan"}

header = {"First Seen Kill",
          "Score"}