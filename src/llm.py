# from transformers import pipeline
from langchain_cohere import ChatCohere
from langchain.chains import SequentialChain, LLMChain
from langchain.prompts.chat import ChatPromptTemplate
from decouple import config
from utils import get_prompt_templates

def run_summariser_censor(body):
    '''
    Summarises and censors toxic words within post body using Cohere LLM.

    Parameters:
    Post body to be summarised and censored.

    Returns:
    The summarised and cleaned text.
    '''
    llm = ChatCohere(cohere_api_key=config('COHERE_API_KEY'))
    summariser_template, censor_template = get_prompt_templates()

    summariser_prompt = ChatPromptTemplate.from_template(template=summariser_template)
    summariser_chain = LLMChain(llm=llm, prompt=summariser_prompt, output_key='summarised_text')

    censor_prompt = ChatPromptTemplate.from_template(censor_template)
    censor_chain = LLMChain(llm=llm, prompt=censor_prompt, output_key='final_text')

    overall_chain = SequentialChain(
        chains=[summariser_chain, censor_chain],
        input_variables=['input'],
        output_variables=['summarised_text', 'final_text'],
        verbose=True)

    print(overall_chain(body))
    res = overall_chain(body)['final_text']
    return res

# def llm_summarise(article):
#     """
#     Summarise article to have word count betweem 150 to 170.

#     Parameters:
#     article: string to be summarised

#     Returns:
#     String containing summary
#     """
#     summariser = pipeline("summarization", model="facebook/bart-large-cnn")

#     summary_arr = summariser(article, max_length=170, min_length=150, do_sample=False)
#     summary_text = summary_arr[0]["summary_text"]
#     return summary_text


# for testing
# summ = """
# I, a female, was about 8 years old at the time and had a new pet for 2 weeks. A goldfish named Ben in a small round aquarium. I loved him so much. My parents liked to party at our house with their friends on weekends. My uncle was always there too and he always overdid it with the alcohol. One Saturday evening I was already asleep in my bed. Suddenly I heard the door open and someone came in. I pretended to be sleeping. I thought the person would walk out again at any moment. I heard strange noises like someone was undoing their belt and taking off their pants. When I heard farting noises, loud moans and someone singing “what shall we do with the drunken sailor”, I couldn’t understand anything. The farts were getting louder and louder and I was starting to get scared. It started to smell disgusting. The person left my room again and I fell asleep at some point. The next morning I heard my mother screaming. I woke up and saw my aquarium full to the brim with shit. My goldfish Ben survived, thank God. To this day I still wonder how. It smelled like hell. We only found out it was my uncle when he did the exact same thing to my cousin's spider. I still hate him to this day and whenever I hear the song “What shall we do with the drunken sailor” I get goosebumps. """
# print(llm_summarise(summ))
