# from transformers import AutoTokenizer, AutoModelForCausalLM, 
from transformers import pipeline
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
                less than 20 words. Here is information about my video.\n \
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

def llm_summarise(article):
    '''
    Summarise article to have word count betweem 150 to 170.

    Parameters:
    article: string to be summarised

    Returns:
    String containing summary
    '''
    summariser = pipeline("summarization", model="facebook/bart-large-cnn")

    summary_arr = summariser(article, max_length=170, min_length=150, do_sample=False)
    summary_text = summary_arr[0]['summary_text']
    return summary_text

# Code to test the functions above so that function developement can be
# done in this file, before integrating with other code
 
# tup = (
#       'Would you say majority Singaporean guys are decent and wholesome?', 
#       'I heard there are less playboy behaviour from Singapore guys compared to Western guys hence why I ask, foreigner here posting. I’m curious to see what others think of Singaporean guys as a whole, not sure if those positive sentiments are shared by the locals however.'
#       )
# generate_caption_cortex(tup)

# summ = """
# I, a female, was about 8 years old at the time and had a new pet for 2 weeks. A goldfish named Ben in a small round aquarium. I loved him so much. My parents liked to party at our house with their friends on weekends. My uncle was always there too and he always overdid it with the alcohol. One Saturday evening I was already asleep in my bed. Suddenly I heard the door open and someone came in. I pretended to be sleeping. I thought the person would walk out again at any moment. I heard strange noises like someone was undoing their belt and taking off their pants. When I heard farting noises, loud moans and someone singing “what shall we do with the drunken sailor”, I couldn’t understand anything. The farts were getting louder and louder and I was starting to get scared. It started to smell disgusting. The person left my room again and I fell asleep at some point. The next morning I heard my mother screaming. I woke up and saw my aquarium full to the brim with shit. My goldfish Ben survived, thank God. To this day I still wonder how. It smelled like hell. We only found out it was my uncle when he did the exact same thing to my cousin's spider. I still hate him to this day and whenever I hear the song “What shall we do with the drunken sailor” I get goosebumps. """
# print(llm_summarise(summ))
