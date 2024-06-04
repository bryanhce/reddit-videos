import json
# special module to store global variables
# reference: https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules

def get_parameter(param):
    with open('/code/parameters.json') as f:
        parameters = json.load(f)

    return parameters.get(param)

# speed to increase video playback
SPEED_MULTIPLIER = get_parameter('SPEED_MULTIPLIER')

# boolean to toggle source of generated voice
IS_11LABS_VOICE = get_parameter('IS_11LABS_VOICE')

#voice id to get from eleven labs voice library
VOICE_ID = get_parameter('VOICE_ID')

SUMMARISER_TEMPLATE = '''
    Summarise the text WITHOUT CHANGING THE MEANING OF THE TEXT IN ANY WAY.
    The new summary should be at least 140 words long, NO LESS THAN 140 WORDS.
    Here is the text : {input}
    '''

CENSOR_TEMPLATE = '''
    If the input contains profanities, racial slurs
    or any sexual language, you are to REPLACE EACH TOXIC WORD with a benign
    word OF SAME MEANING AND NUANCE. In addition, these are some word mappings
    that you can use to replace some words when applicable.

    "cigarette": "puff",
    "fuck": "fk",
    "gun": "pew pew",
    "pussy": "kitty",
    "cunt": "cant",
    "sex": "segg",
    "thicc": "large",
    "thick": "large",
    "lesbian": "less",
    "gay": "happy",
    "queer": "confused",
    "shit": "crap",
    "disabled": "not abled",
    "threesome": "3sum",
    "dead": "un alive",
    "kill": "un alive",
    "die": "pass away",
    "dying": "passing away",
    "asshole": "bumhole",
    "kill myself": "un alive myself",

    You CANNOT CHANGE THE SENTENCE IN
    ANYOTHER WAY EXCEPT REPLACING THE TOXIC WORD.

    Here is the input text : {summarised_text}
    '''