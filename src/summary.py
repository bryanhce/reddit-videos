from utils import has_tuples
from llm import llm_summarise

def summarise(body):
    '''
    'main' method for the summary.

    Parameters:
    body: dictionary of thumbnail and content
    where content is an array of string
    '''
    if is_video_longer_than_one_min(body):
        text = llm_summarise(body['content'])
        body['content'] = [text]
        print('Summarisation complete!')
    return body

def is_video_longer_than_one_min(body):
    '''
    Estimate that 1100 characters is the upper limit of 1 min

    Parameters:
    Body: dictionary of thumbnail and content
    thumbnail is a string while content is an array
    Content take on 2 forms
    1. [("s1", "s2"), ("s3", "s4")]
    2. ["s1", "s2", "s3", "s4"]

    Returns:
    boolean if video is longer than one minute
    '''
    length = len(body['thumbnail'])
    if has_tuples(body['content']):
        for tup in body['content']:
            for text in tup:
                length += len(text)
    else:
        for text in body['content']:
            length += len(text)

    return length > 1100 