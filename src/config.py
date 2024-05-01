import json
# special module to store global variables
# reference: https://docs.python.org/3/faq/programming.html#how-do-i-share-global-variables-across-modules

def get_parameter(param):
    with open('/code/parameters.json') as f:
        parameters = json.load(f)

    return parameters.get(param)

# speed to increase video playback
SPEED_MULTIPLIER = get_parameter('SPEED_MULTIPLIER')

# boolean to toggle gender of generated voice
IS_VOICE_FEMALE = get_parameter('IS_VOICE_FEMALE')