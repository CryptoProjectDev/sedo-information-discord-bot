# SEDO-discord-price-bot configuration file
#

CURRENCY = 'SEDO'
TOKEN_ETH_ADDRESS = "0x0F00f1696218EaeFa2D2330Df3D6D1f94813b38f"

UPDATE_RATE = 120  # how often to update all APIs (in seconds)
TOKEN_HOLDER_UPDATE_RATE_HOURS = 6  # how often to update the token holder chart (in hours)
COMMAND_CHARACTER = '!'  # what character should prepend all commands

DATA_FOLDER = './databases/'  # folder to store persistent data (all-time high prices, etc)

# URL for your Ethereum provider. Get one for free at infura.io
ETHEREUM_NODE_URL = "https://mainnet.infura.io/f12d6274997840158b99b418f0ed8ec1"

# Channels listed here will be ignored by the bot for all but 'global' commands
BLACKLISTED_CHANNEL_IDS = [
    # SEDO server
    '454156227446964226',  # announcements
    '417834372864147456',  # articles
    '413927301932253185',  # useful-links
    '412477591778492429',  # 0xbitcoin
    #'412483801265078273',  # trading (allowed)
    '429103257026297866',  # marketing
    '419929514316136473',  # miner-dev
    '414664710210846722',  # development
    '412483768541249536',  # support
    '438693168393748500',  # mining
    '435893447958986752',  # pools
    '439217061475123200',  # memes
    '421306695940046852',  # off-topic
    '418282243186753537',  # alts-trading
]

# List of users who should be allowed to run privileged commands (like !setath)
PRIVILEGED_USER_IDS = [
    '0',                   # testing user ID
    '513468214341140530',  # SEDO-DEV
]

# List of object prices. This is used by two classes of bot commands:
#  - Trading commands ie `!lambo` -> "1 lambo = 1,194,557 0xBTC ($400.0k)"
#  - Source data for convert ie `!convert 800 0xbtc to tesla`
EXPENSIVE_STUFF = [
    (400000,
     ['lambo']),
    (200000,
     ['used lambo']),
    (500000,
     ['private island', 'privare island', 'pirvate island', 'island']),
    (398.8*1000*1000,
     ['whitehouse', 'white house']),
    (1.225*1000*1000*1000,
     ['buckingham palace']),
    (3.9*1000*1000*1000,
     ['air force one']),
    (101500, 
     ['tesla', 'telsa']),
    (1700,
     ['used ford taurus', 'used taurus', 'old ford taurus', 'old taurus', 'used ford torus']),
    (17600,
     ['like new ford taurus', 'like new taurus']),
    (28400,
     ['new ford taurus', 'ford taurus', 'new taurus', 'taurus']),
    (12,
     ['avocado toast',
      'avocado on toast', 
      'avacado toast', 
      'avacado on toast', 
      'avocato toast', 
      'avocato on toast',
      'avovado toast',
      'avacodo toast',
      'avo toast']),
    (1,
     ['oneaire']),
    (10,
     ['tennaire', 'tenaire']),
    (100,
     ['hundredaire', 'hundradiere']),
    (1e3,
     ['thousandaire']),
    (1e6,
     ['millionaire']),
    (1e9,
     ['billionaire']),
    (1e12,
     ['trillionaire']),
    (650,
     ['magnum domperignon', 'domperignon', 'champagne', 'donperignon']),
    (200,
     ['microsoft windows license', 'microsoft windows', 'windows']),
]
