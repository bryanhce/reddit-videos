# from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from decouple import config
import requests

# HUGGING_FACE_TOKEN = config('HUGGING_FACE_TOKEN')
CORTEXT_API_KEY = config('CORTEXT_API_KEY')

# takes too long, does ritika know how to do it?
"""
def generate_caption(tup):
    '''
    Create caption using google's gemma model.

    Parameters:
    tup: tuple of (title, content)

    Returns:
    String containing the caption
    '''
    tokenizer = AutoTokenizer.from_pretrained("google/gemma-7b", token=HUGGING_FACE_TOKEN)
    model = AutoModelForCausalLM.from_pretrained("google/gemma-7b", token=HUGGING_FACE_TOKEN)

    # TODO: fine tune the prompt for better results
    input_text = f"Create short captions with hashtags for a tiktok \
                video that I can creating. Here is some information \
                about the video. Keep the captions and hashtags strictly \
                less than 40 words. Here is information about my video.\n \
                Title: {tup[0]} \n \
                Content : {tup[1]}"
    input_ids = tokenizer(input_text, return_tensors="pt")

    max_length = len(input_ids.input_ids[0]) + 50  # Adjust the additional tokens as needed

    # Generate caption
    outputs = model.generate(input_ids.input_ids, max_length=max_length, num_return_sequences=1)

    # outputs = model.generate(**input_ids)
    caption = tokenizer.decode(outputs[0])
    print(caption)
    return caption
"""

def generate_caption_cortex(tup):
    '''
    Create caption using text cortext api.
    Do not spam calls to this api as we have limited number of free calls everyday.

    Parameters:
    tup: tuple of (title, content)

    Returns:
    String containing the caption

    Documentation:
    https://docs.textcortex.com/api/paths/texts-social-media-posts/post
    '''
    url = 'https://api.textcortex.com/v1/texts/social-media-posts'

    headers = {
        "Authorization": f"Bearer {CORTEXT_API_KEY}",
        "Content-Type": "application/json"
    }

    context = f"Create short captions with hashtags for a tiktok \
                video that I can creating. Here is some information \
                about the video. Keep the captions and hashtags strictly \
                less than 40 words. Here is information about my video.\n \
                Title: {tup[0]} \n \
                Content : {tup[1]}"

    data = {
        "context": context,
        "formality": "less",
        # "keywords": [
        #     ""
        # ],
        "max_tokens": 2048,
        "mode": "twitter",
        "model": "chat-sophos-1",
        "n": 1,
        "source_lang": "en",
        "target_lang": "en",
        "temperature": 0.65
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        caption = response.json()['data']['outputs'][0]['text']
        # print(caption)
        print("POST request to cortext api is successful")
        return caption
    else:
        print("POST request to cortext api failed with status code:", response.status_code)




def summarise(article):
    '''
    Summarise article to have word count betweem 30 to 100.

    Parameters:
    article: string to be summarised

    Returns:
    String containing summary
    '''
    summariser = pipeline("summarization", model="facebook/bart-large-cnn")

    summary_arr = summariser(article, max_length=100, min_length=50, do_sample=False)
    summary_text = summary_arr[0]['summary_text']
    return summary_text

tup = ('Would you say majority Singaporean guys are decent and wholesome?', 'I heard there are less playboy behaviour from Singapore guys compared to Western guys hence why I ask, foreigner here posting. I’m curious to see what others think of Singaporean guys as a whole, not sure if those positive sentiments are shared by the locals however.')
# generate_caption_cortex(tup)
# summ = """
#     guys idk if u noticed it anot, but i realised many girls in their teens years they tend to want to have birthday parties with their friends at their homes. like literally everyone will come dressed in nice fancy dresses and their parents rlly prepare nice fancy cake and nice fancy decos for the birthday party especially the 'age balloons' thing (e.g. '19' for 19 year old girl) and the streamers and all. like i dont understand whether their family is super rich or smth or their parents are super rich or smth that they're so willing to spend alot of their money so that their daughters can have a nice quality time with their friends for their birthday party whereby they invite 10+ friends over to have fun and then u see the instagram stories on it. if u are a girl kindly enlighten this guy as to why yall do this and why your parents are so willing to do this, cos the tradition in my family is birthday just have a nice fancy meal outside to celebrate with the family, cake is optional and don't need to make the occasion so fancy. i thought having birthday parties was a stage that you'll grow out of after primary school, and even in kindergarten and all my family didnt even have birthday parties for me and my brother. our only 'birthday party' whereby we invited other ppl to come was during our one year old birthday LOL, then birthdays is kinda a low profile thing in my family. POV: im a guy which explains why i dont understand this haha. our birthdays we tend to celebrate in a quite simple fashion and we're quite chill about birthdays.
# """
# print(summarise(summ))
