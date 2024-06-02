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

    # create prompt and chain objects
    summariser_prompt = ChatPromptTemplate.from_template(template=summariser_template)
    summariser_chain = LLMChain(llm=llm, prompt=summariser_prompt, output_key='summarised_text')

    censor_prompt = ChatPromptTemplate.from_template(censor_template)
    censor_chain = LLMChain(llm=llm, prompt=censor_prompt, output_key='final_text')

    overall_chain = SequentialChain(
        chains=[summariser_chain, censor_chain],
        input_variables=['input'],
        output_variables=['summarised_text', 'final_text'],
        verbose=True)
    
    res = overall_chain(body)['final_text']
    return res
