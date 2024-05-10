from utils import has_tuples
from llm import llm_summarise


def transform_text(body):
    """
    'main' method for text transformation.
    Replace banned words and summarises content
    if necessary.

    Parameters:
    body: dictionary of thumbnail and content
    where content is an array of string

    Returns:
    nothing, edits dict in place
    """
    body["thumbnail"] = replace_banned_words_with_dict(body["thumbnail"])
    body["content"] = [replace_banned_words_with_dict(body["content"][0])]
    summarise(body)


def replace_banned_words_with_dict(text):
    banned_word_dict = {
        "cigarette": "puff",
        "fuck": "fk",
        "gun": "pew pew",
        "penis": "pp",
        "dick": "pp",
        "bbc": "big black pp",
        "vagina": "kitty",
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
        "die" : "pass away",
        "dying": "passing away",
        "ass": "bum",
        "asshole": "bumhole",
        "til": "today I learnt",
        "fyi": "for your information",
        "mil": "mother in law",
        "fil": "father in law",
        "lmao": "laughing my butt off",
        "wtf": "what the heck",
        "kill myself": "un alive myself",
    }

    for banned_word, replacement_word in banned_word_dict.items():
        text = text.replace(banned_word, replacement_word)
    return text


def summarise(body):
    """
    'main' method for the summary.

    Parameters:
    body: dictionary of thumbnail and content
    where content is an array of string
    """
    if is_video_longer_than_one_min(body):
        text = llm_summarise(body["content"])
        body["content"] = [text]
        print("Summarisation complete!")


def is_video_longer_than_one_min(body):
    """
    Estimate that 1100 characters is the upper limit of 1 min

    Parameters:
    Body: dictionary of thumbnail and content
    thumbnail is a string while content is an array
    Content take on 2 forms
    1. [("s1", "s2"), ("s3", "s4")]
    2. ["s1", "s2", "s3", "s4"]

    Returns:
    boolean if video is longer than one minute
    """
    length = len(body["thumbnail"])
    if has_tuples(body["content"]):
        for tup in body["content"]:
            for text in tup:
                length += len(text)
    else:
        for text in body["content"]:
            length += len(text)

    return length > 1100


# bod = {"thumbnail": "lesbian mom", "content": ["fucking"]}
# transform_text(bod)
# print(bod)
