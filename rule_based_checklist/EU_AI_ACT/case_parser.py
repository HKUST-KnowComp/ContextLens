import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from datasets import load_from_disk
import os
import openai
import json
import re
from openai import OpenAI
import argparse

### parent folder
import config
from generation_utils import *

# def parse_json_dict(analyze_response: dict) -> dict:
#     '''
#     parse the analyze response to a dictionary
#     '''
#     response = analyze_response['response']
#     response = response.strip()
#     try:
#         if response.startswith("```json"):
#             json_str = re.search(r'```json(.*)```', response, re.DOTALL).group(1).strip()
#             json_str = json_str.replace("False", "false").replace("True", "true").replace("None", "null")
#             json_dict = json.loads(json_str)
#         elif response.startswith("{") and response.endswith("}"):
#             json_str = response.replace("False", "false").replace("True", "true").replace("None", "null")
#             json_dict = json.loads(json_str)
#         # else:
#         #     raise Exception("Failed to parse the response, response: {response}")
#     except:
#         print("Failed to parse the response, response:")
#         print(response)
#         return None
#         raise Exception(f"Failed to parse the response, response: {response}")
#     return json_dict

### DFS to solve it
def process_answer_dict(answer_dict: dict, 
                      index_to_question: dict,
                      question_dict: dict) -> dict:
    all_results = []
    all_result_paths = []
    def go_to_next_question(cur_question_index: str, cur_answer_list: list, results = [], result_paths=[]) -> str:
        if cur_question_index == 'result_end':
            return results, result_paths

        cur_question = index_to_question[cur_question_index]
        if cur_question not in question_dict:
            return results, result_paths
        if cur_answer_list == []:
            results.append('No Option Given')
            return results, result_paths
        for answer in cur_answer_list:
            answer = int(answer) - 1
            option_string = question_dict[cur_question]["options"][answer]
            next_question = question_dict[cur_question]["outcome"][option_string]
            #next_question_index = question_to_index[next_question]
            next_question_index = question_to_index.get(next_question, 'result_end')
            results.append(option_string)
            result_paths.append(f'{option_string} --- {next_question}')
            if next_question_index == 'result_end':
                all_results.append(next_question)
                all_result_paths.append(result_paths)
                return results, result_paths
            results, result_paths = go_to_next_question(next_question_index, answer_dict[next_question_index], results, result_paths)
        return results, result_paths
    

    question_to_index = {v: k for k, v in index_to_question.items()}
    start_question = 'question_1'
    cur_question_index = start_question
    cur_answer_list = answer_dict[cur_question_index]
    results = [cur_question_index]
    result_paths = [f'{index_to_question[cur_question_index]}']
    results, result_paths = go_to_next_question(cur_question_index, cur_answer_list, results, result_paths)
    return all_results, all_result_paths
    
def question_index_to_question(question_dict: dict) -> dict:
    ret = {}
    for i,question in enumerate(question_dict.keys()):
        ret[f'question_{str(i+1)}'] = question
    return ret
def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)
    

def majority_vote(results: list) -> str:
    ret = {}
    for result in results:
        if result not in ret:
            ret[result] = 0
        ret[result] += 1
    return max(ret, key=ret.get)


def result_to_norm_type(result: str) -> str:
    result = result.lower()
    if result == 'Out of scope'.lower():
        return 'not applicable'
    elif result == 'Prohibited'.lower():
        return 'prohibit'
    else:
        return 'permit'


def log(log_path: str, content: str):
    with open(log_path, 'a+') as f:
        f.write(content + '\n')









if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-7B-Instruct")
    #parser.add_argument("--log_path", type=str, default=f"logs/log.txt")
    parser.add_argument("--max_new_tokens", type=int, default=512)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--domains", type=str, default='AI_ACT')
    args = parser.parse_args()
    #args.api_model = args.model
    #args.log_path = args.log_path.replace('logs/', f'logs/{args.api_model}/')
    args.api_model = args.model.replace('/', '--')
    args.log_path = f'logs/{args.api_model}/'

    question_dict = read_json_file("question_dict.json")
    index_to_question = question_index_to_question(question_dict)
    #temp_log_path = 'log_GDPR.txt'
    

    DOMAINS = args.domains.split('+')
    for domain in DOMAINS:
        #domain = 'AI_ACT'
        assert domain in ['GDPR', 'AI_ACT'], 'Invalid domain name.' 
        #dataset = load_from_disk(f'PATH_TO_CASES/cases/{domain}')
        dataset = get_local_case_dataset(domain)
        data = dataset['test']

        #response_path1 = f'logs_old/final_response_{domain}.json'
        

        # path to the response file
        response_path = f"{args.log_path}final_response_{domain}_{args.api_model}.json"
    
        temp_log_path = response_path.replace('.json', 'result.log')
        with open(response_path, 'r') as f:
            response_list = json.load(f)

        #for response in response_list:
        correct = 0
        for idx, cur_case in enumerate(data):
            # if idx > 5:
            #     break

            response = response_list[idx]
            case_content = cur_case['case_content']
            #prompt = 
            response_case = response['prompt'][0]['content']
            response_case_content = response_case.split('**Case content**:\n')[1].split('\n\n**Case context**')[0].strip()
            assert case_content == response_case_content
            try:
                response_dict = parse_json_dict(response['response'])
                results, result_paths = process_answer_dict(response_dict, index_to_question, question_dict)
                voted_result = majority_vote(results)
                voted_result_norm_type = result_to_norm_type(voted_result)
                if voted_result_norm_type == cur_case['norm_type']:
                    correct += 1
            except Exception as e:
                print(f"Error parsing response for case {idx}: {e}")
                print(f'idx: {idx}. ground truth:{cur_case['norm_type']}\nresponse: {response['response']}')
                continue

            log(temp_log_path, f"idx: {idx}")
            log(temp_log_path, f"results: {results}")
            log(temp_log_path, f"cur_case['norm_type']: {cur_case['norm_type']}, voted_result_norm_type: {voted_result_norm_type}")
            

        print(f'{domain} accuracy: {correct / len(data)}, correct count: {correct}, total count: {len(data)}')
