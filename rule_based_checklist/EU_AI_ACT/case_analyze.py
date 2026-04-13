import sys
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "6"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# print(os.path.abspath(__file__))
# print(os.path.dirname(os.path.abspath(__file__)))
from datasets import load_from_disk
import openai
import json
import re
from openai import OpenAI
import argparse

### parent folder
import config
from generation_utils import *




def get_reponse(args,message):
    message_list = [
    {"role": "user", "content": message}
    ]
    chatbot = args.chatbot
    decision = chatbot.compeletion(args.api_model, message_list, args.max_retry, temperature = args.temperature, max_tokens = args.max_new_tokens)
    return decision

def get_response_hf(args,message):
    '''
    Get response from Hugging Face model
    '''
    response = args.chatbot.respond(message, max_new_tokens=args.max_new_tokens)
    return response

def message_to_llm(user_prompt: str, args: argparse.Namespace,
                   system_prompt: str = "", max_retry: int = 3, max_tokens: int = 2048):

    cur_retry = 0
    while cur_retry < max_retry:
        try:
            if system_prompt:
                messages=[
                    #{"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            else:
                messages=[{"role": "user", "content": user_prompt}]
            
            # response = client.chat.completions.create(
            #     model=model_id,
            #     messages=messages,
            #     max_tokens=max_tokens,
            #     temperature=0.0
            # )
            get_response_fc = get_reponse if args.api_name != 'hf' else get_response_hf

            response = get_response_fc(args, user_prompt)

            if args.api_name != 'hf':
                rationale = response.choices[0].message.reasoning_content if hasattr(response.choices[0].message, 'reasoning_content') else ''
                return {'prompt': messages, 'rationale': rationale, 'response': response.choices[0].message.content}
            else:
                return {'prompt': messages, 'rationale': '', 'response': response}

        except Exception as e:
            cur_retry += 1
            print(f"Error: {e}")
            print(f"Retrying... ({cur_retry}/{max_retry})")
    return None

def read_json_file(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def case_analyze(case_content, args):
    
    system_prompt = """You are a context analyzer to identify AI systems and their fair usage based on the EU AI Act regulation."""

    user_prompt = """
As an expert context analyzer, your task is to analyze the given case and identify if there is any AI system involved. If there is AI system involved, please identify the name, type, usage and actions of the AI system.

**Definition of AI system**:
An AI system is defined as: A machine-based system designed to operate with varying levels of autonomy and that may exhibit adaptiveness after deployment and that, for explicit or implicit objectives, infers, from the input it receives, how to generate outputs such as predictions, content, recommendations, or decisions that can influence physical or virtual environments.

Please follow these steps:
1. Analyze the case and identify if there is any AI system involved. If there is AI system involved, please identify the name of the AI system, the type of the AI system, and the usage of the AI system.
2. If there is AI system involved, please identify atomic actions that are performed by the AI system and the target of the action. If there are more than one action, please identify all of them. 
3. For each action, please identify the target of the action and the purpose of the action.

    
**Case**: 
{case_content}

**Output format**:
Output format should be in JSON format:
    {{
        "AI_system_involved": True/False,
        "AI_system_name": "name of the AI system",
        "AI_system_type": "type of AI system",
        "AI_system_usage": "usage of the AI system",
        "atomic_actions": [
            {{
                "action": "atomic action",
                "target": "target of the action",
                "purpose": "purpose of the action"
            }},
            ...
        ]
    }}
""".format(case_content=case_content)
    #user_prompt = user_prompt.format(case_content=case_content)
    response = message_to_llm(user_prompt, args, system_prompt)
    return response

def question_prompt(question_list: list, case_content: str, case_context: str) -> str:
    user_prompt = """
You task is to play the role of the AI system inside the case. Please answer the following questions based on the case content and the case context. For each question, there may be more than 1 applicable option, you should provide a list of options.

**Case content**:
{case_content}

**Case context**:
{case_context}

**List of questions**:
{question_list}

**Output format**:

Output format should be in JSON format and your answer should contain only the numerical index of the option without any text in the options. You should select at least one option for each question.
{{
    "question_1": [option_1, option_2, ...],
    "question_2": [option_1, option_2, ...],
    ...
}} 
"""
    question_string = ""
    for i,question in enumerate(question_list):
        question_string += f"**Question {i+1}**: {question}\n"
    user_prompt = user_prompt.format(case_content=case_content, case_context=case_context, question_list=question_string)
    return user_prompt


def question_index_to_question(question_dict: dict) -> dict:
    ret = {}
    for i,question in enumerate(question_dict.keys()):
        ret[f'question_{str(i+1)}'] = question
    return ret

def question_generator(question_dict: dict) -> list:
    question_list = [] ## a list of questions (string)
    question_template = '''
**Question {q_index}**:
{question}

**Options**:
{option_string}

**background**:
{background}
'''
    for i,question in enumerate(question_dict.keys()):
        cur_dict=  question_dict[question]
        theme = cur_dict["theme"]
        options = cur_dict["options"]
        outcome = cur_dict["outcome"]
        source = cur_dict["source"]
        background = cur_dict["background"]
        option_string = convert_options_to_string(options)
        question_string = question_template.format(q_index=i+1, question=question, option_string=option_string, background=background)
        question_list.append(question_string)

    return question_list
def convert_options_to_string(options: list) -> str:
    '''
    convert the options to a string, each option should be in a new line and start with a number
    '''
    option_string = ""
    for i,option in enumerate(options):
        option_string += f"{i+1}. {option}\n"
    return option_string



### DFS to solve it
def process_answer_dict(answer_dict: dict, 
                      index_to_question: dict,
                      question_dict: dict) -> dict:
    
    def go_to_next_question(cur_question_index: str, cur_answer_list: list, results = [], result_paths=[]) -> str:
        cur_question = index_to_question[cur_question_index]
        if cur_question not in question_dict:
            return results, result_paths
        if cur_answer_list == []:
            results.append('No Option Given')
            return results, result_paths
        for answer in cur_answer_list:
            option_string = question_dict[cur_question]["options"][answer]
            next_question = question_dict[cur_question]["outcome"][option_string]
            next_question_index = question_to_index[next_question]
            results.append(option_string)
            result_paths.append(next_question)
            results, result_paths = go_to_next_question(next_question_index, answer_dict[next_question_index], results, result_paths)
        return results, result_paths
    

    question_to_index = {v: k for k, v in index_to_question.items()}
    start_question = 'question_1'
    cur_question_index = start_question
    cur_answer_list = answer_dict[cur_question_index]
    results, result_paths = go_to_next_question(cur_question_index, cur_answer_list)
    
    # cur_index = start_question
    # cur_question = index_to_question[cur_index]
    # while cur_index in answer_dict:
    #     cur_answer_list = answer_dict[cur_index]
    #     cur_answer_list = [int(x)-1 for x in cur_answer_list]
    #     for answer in cur_answer_list:
    #         option_string = question_dict[cur_question]["options"][answer]
    #         next_question = question_dict[cur_question]["outcome"][option_string]


    return results, result_paths


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--start_index', type=int, default=-1)

        ### newly appeneded
    parser.add_argument("--model", type=str, default="Qwen/Qwen2.5-7B-Instruct")
    parser.add_argument("--log_path", type=str, default=f"logs/log.txt")
    parser.add_argument("--max_new_tokens", type=int, default=512)
    parser.add_argument("--generation_round", type=int, default=5)
    parser.add_argument("--seed", type=int, default=42)
    #parser.add_argument("--api_name", type=str, default=config.API_NAME)
    parser.add_argument("--api_name", type=str, default='hf')
    parser.add_argument("--domains", type=str, default='AI_ACT')
    parser.add_argument("--api_model", type=str, default='gpt-4o-mini')
    parser.add_argument("--api_token", type=str, default=config.OPENAI_API_KEY)
    parser.add_argument("--max_retry", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0)
    args = parser.parse_args()
    start_index = args.start_index
    domain = args.domains
    
    if args.api_name == 'hf':
        if args.model:
            args.chatbot = HuggingfaceChatbot((args.model))
            args.model = args.model.replace('/', '--')
            args.api_model = args.model
        else:
            raise ValueError("Please specify the model name for Hugging Face chatbot.")
    else:
        args.chatbot = OpenAI_model(
            api_key=args.api_token,
            api_name=args.api_name
        ) 
    #args.log_path = args.log_path.replace('logs/', f'logs/{args.api_model}/')
    args.log_path = f'logs/{args.api_model}/'
    if not os.path.exists(os.path.dirname(args.log_path)):
        os.makedirs(os.path.dirname(args.log_path))

    # main part
    case_dataset = get_local_case_dataset(domain)
    dataset = case_dataset['test']
    question_dict = read_json_file("question_dict.json")
    question_list = question_generator(question_dict)
    #print(question_list)
    case_analyze_response_list = []
    final_response_list = []
    index_to_question = question_index_to_question(question_dict)
    for i, cur_case in enumerate(dataset):
        if i <= start_index:
            continue
        # if i > 5:
        #     break
        case_content = cur_case['case_content']
        norm_type = cur_case['norm_type']
        case_analyze_response = case_analyze(case_content, args)
        case_analyze_response["case_id"] = i
        #case_analyze_response_text = case_analyze_response['response']
        parsed_context = parse_json_dict(case_analyze_response['response'])
        if parsed_context is None:
            continue
        AI_system_involved = parsed_context.get("AI_system_involved", False)
        parsed_context["case_id"] = i
        case_analyze_response_list.append(case_analyze_response)
        if not AI_system_involved:
            ##
            print(f"Case {i} does not involve AI system, the result should be not applicable")
            #final_response_list.append({"case_id": i, "applicable": "not applicable"})
            #continue
        context_str = json.dumps(parsed_context, indent=1)    
        final_prompt = question_prompt(question_list, case_content, context_str)
        final_response = message_to_llm(final_prompt, args)
        final_response["case_id"] = i
        final_response["applicable"] = "yes"
        final_response['original_case'] = cur_case
        #print(final_response)
        final_response_list.append(final_response)

        #answer_dict = process_answer_dict(final_response)

        if i % 10 == 0:
            with open(f"{args.log_path}case_analyze_response_{domain}_{args.api_model}.json", "w", encoding="utf-8") as f:
                json.dump(case_analyze_response_list, f, indent=4, ensure_ascii=False)

            with open(f"{args.log_path}final_response_{domain}_{args.api_model}.json", "w", encoding="utf-8") as f:
                json.dump(final_response_list, f, indent=4, ensure_ascii=False)

            
            
        #print(case_analyze_response)

    with open(f"{args.log_path}case_analyze_response_{domain}_{args.api_model}.json", "w", encoding="utf-8") as f:
        json.dump(case_analyze_response_list, f, indent=4, ensure_ascii=False)

    with open(f"{args.log_path}final_response_{domain}_{args.api_model}.json", "w", encoding="utf-8") as f:
        json.dump(final_response_list, f, indent=4, ensure_ascii=False)
    