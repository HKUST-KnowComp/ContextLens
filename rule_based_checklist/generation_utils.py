from openai import OpenAI
import time
import os
import config
from datasets import load_dataset, load_from_disk
import json
import re
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def log(message, path):

    ### directory check
    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    if not isinstance(message, str):
        try:
            # Use JSON for pretty and structured dict output
            message = json.dumps(message, ensure_ascii=False)
        except Exception as e:
            print(f"Error converting message to JSON: {e}")
            message = str(message)  # fallback to str()

    if not os.path.exists(path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(message+"\n")
    else:
        with open(path, "a", encoding="utf-8") as f:
            f.write(message+"\n")

def load_local_HF_dataset(path):
    '''
    Load a dataset from a local path
    '''
    dataset = load_from_disk(path)
    return dataset

def get_local_KB_dataset():
    KB_path = config.HF_KBs_path
    kb_data = load_local_HF_dataset(KB_path)
    return kb_data

def get_local_case_dataset(domain):
    case_path = config.HF_cases_path
    case_path = os.path.join(case_path, domain)
    case_data = load_local_HF_dataset(case_path)
    return case_data

def label_transform(label):
    ### convert a label to a list of labels
    ret = []
    if label.lower() in ['negative', 'prohibit', 'prohibited']:
        ret = ['negative', 'prohibit', 'prohibited']
    elif label.lower() in ['positive', 'permit', 'permitted']:
        ret = ['positive', 'permit', 'permitted']
    elif label.lower() in ['not applicable']:
        ret = ['not applicable']
    return ret


def parse_json_dict(analyze_response: str) -> dict:
    '''
    parse the analyze response to a dictionary
    '''
    response = analyze_response
    response = response.strip()
    try:
        if response.startswith("```json") and response.endswith("```"):
            json_str = re.search(r'```json(.*)```', response, re.DOTALL).group(1).strip()
            json_str = json_str.replace("False", "false").replace("True", "true").replace("None", "null")
            json_dict = json.loads(json_str)
        elif response.startswith("{") and response.endswith("}"):
            json_str = response.replace("False", "false").replace("True", "true").replace("None", "null")
            json_dict = json.loads(json_str)
        else:
            ### locate first json dict in the response
            json_pattern = r'\{.*?\}'
            match = re.search(json_pattern, response, re.DOTALL)
            if match:
                json_str = match.group(0)
                json_str = json_str.replace("False", "false").replace("True", "true").replace("None", "null")
                json_dict = json.loads(json_str)
        #     raise Exception("Failed to parse the response, response: {response}")
    except:
        print("Failed to parse the response, response:")
        print(response)
        return None
        raise Exception(f"Failed to parse the response, response: {response}")
    return json_dict








class OpenAI_model:
    def __init__(self, api_key: str, api_name: str):
        self.api_key = api_key
        self.api_name = api_name
        if(api_name == 'deepseek'):
            ### using deepseek r1 model from ARK API
            print('using API to respond via deepseek r1...')
            self.client = OpenAI(
                api_key = self.api_key,
                base_url = "INPUT_YOUR_API_BASE_URL",
            )
        else:
            self.client = OpenAI(
                api_key=self.api_key, 
                base_url="INPUT_YOUR_API_BASE_URL"
            )

    def compeletion(self, model: str, messages: list, max_retries: int, **kwargs):
        retries = 0
        while retries < max_retries:
            try:
                # set up your own endpoint
                # if(self.api_name == 'deepseek'):
                #     model = 'ep-20250208151949-2c29b'
                response = self.client.chat.completions.create(
                    model = model,
                    messages=messages,
                    **kwargs
                )
                #msg = response.choices[0].message.content
                #assert isinstance(msg, str), "The retruned response is not a string."
                return response  # Return the response if successful

            except Exception as e:
                # Catch all other exceptions
                print(f"Unexpected error: {e}. Retrying in 5 seconds...")
                retries += 1
                time.sleep(1)
        
        return ''  # Return an empty string if max_retries is exceeded
    


class HuggingfaceChatbot:
    def __init__(self, model, max_mem_per_gpu='80GiB'):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model = self.load_hugging_face_model(model, max_mem_per_gpu)
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        


    def load_hugging_face_model(self, model, max_mem_per_gpu='80GiB'):
        MAX_MEM_PER_GPU = max_mem_per_gpu
        map_list = {}
        for i in range(torch.cuda.device_count()):
            map_list[i] = MAX_MEM_PER_GPU
        model = AutoModelForCausalLM.from_pretrained(
            model,
            #device_map="auto",
            #max_memory=map_list,
            #torch_dtype="auto",
            #cache_dir = CACHE_DIR,
            torch_dtype=torch.bfloat16,
            #trust_remote_code=True
        ).to(self.device)
        return model

    def respond(self, message, max_new_tokens=128):
        messages = [
            #{"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": message}
        ]
        message = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        tokenized = self.tokenizer(message, return_tensors="pt")

        #input_ids = tokenized.input_ids
        input_ids = tokenized.input_ids.to(self.model.device)
        attention_mask = tokenized.attention_mask.to(self.model.device)
        generation_config = self.model.generation_config
        #generation_config.max_length = 8192
        generation_config.max_new_tokens = max_new_tokens
        output = self.model.generate(
            input_ids,
            attention_mask=attention_mask,
            generation_config=generation_config
        )
        response = self.tokenizer.batch_decode(output[:, input_ids.shape[1]:], skip_special_tokens=True)[0]
        response = response.strip()
        return response
