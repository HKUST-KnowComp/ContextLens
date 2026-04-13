from openai import OpenAI
import os
import time
from datasets import DatasetDict, load_dataset,load_from_disk
import config


class OpenAI_model:
    def __init__(self, api_key: str, 
                 api_name: str,
                 get_reasoning_content: bool = False):
        self.api_key = api_key
        self.api_name = api_name
        self.get_reasoning_content = get_reasoning_content
        #if 
        if(api_name == 'deepseek'):
            ### using deepseek r1 model from ARK API
            print('using ARK API to respond via deepseek r1...')
            self.client = OpenAI(
                api_key = self.api_key,
                base_url = "https://ark.cn-beijing.volces.com/api/v3",
            )
        else:
            self.client = OpenAI(api_key=self.api_key, base_url="https://api.oneabc.org/v1")

    def compeletion(self, model: str, messages: list, max_retries: int, **kwargs):
        retries = 0
        ret = {
            'content': '',
            'reasoning': ''
        }
        while retries < max_retries:
            try:
                if(self.api_name == 'deepseek'):
                    model = 'ep-20250208151949-2c29b'
                response = self.client.chat.completions.create(
                    model = model,
                    messages=messages,
                    **kwargs
                )
                msg = response.choices[0].message.content
                assert isinstance(msg, str), "The retruned response is not a string."
                ret['content'] = msg
                if self.get_reasoning_content:
                    ret['reasoning'] = response.choices[0].message.reasoning
                return ret  # Return the response if successful

            except Exception as e:
                # Catch all other exceptions
                print(f"Unexpected error: {e}. Retrying in 5 seconds...")
                retries += 1
                time.sleep(1)
        
        return ''  # Return an empty string if max_retries is exceeded
    

def log(message, path):

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(message+"\n")
    else:
        with open(path, "a", encoding="utf-8") as f:
            f.write(message+"\n")


def get_MCQ_dataset():
    #MCQ_path = config.HF_MCQ_path
    mcq_data = load_dataset('teapotlid/PrivaCI-Bench_mcqs', cache_dir=config.HF_HOME)
    return mcq_data

def get_KB_dataset():
    #KB_path = config.HF_KBs_path
    kb_data = load_dataset('teapotlid/PrivaCI-Bench_KBs', cache_dir=config.HF_HOME)
    return kb_data

def get_local_case_dataset():
    case_dir = config.local_case_dir
    domains = ['AI_ACT','GDPR','HIPAA', 'ACLU']
    case_dataset = DatasetDict()
    for domain in domains:
        case_path = os.path.join(case_dir, domain)
        case_data = load_from_disk(case_path)
        case_dataset[domain] = case_data
    
    return case_dataset