import os
# gpu id setup
os.environ["CUDA_VISIBLE_DEVICES"] = "6"
import argparse
import json
import config
import random
import numpy as np
import torch
from generation_utils import *
from tqdm import tqdm

def set_seeds(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)

def get_prompt_templates():
    prompt_paths = ['scope_prompt.txt', 'special_prompt.txt', 'subject_prompt.txt', 'processor_prompt.txt', 'lawful_prompt.txt', 'principal_prompt.txt']
    prompts = {}
    for prompt_path in prompt_paths:
        with open(os.path.join('prompts', prompt_path), 'r') as f:
            prompts[prompt_path.split('.')[0]] = f.read()
    return prompts

def get_llm_response(dataset, args, domain):
    response_save_path = args.log_path.replace('.txt', f'_{args.api_model}_response.json')
    if os.path.exists(response_save_path):
        with open(response_save_path, 'r') as f:
            response_list = json.load(f)
        log(f"Response file {response_save_path} already exists, loading from it.", args.log_path)
        return response_list
    chatbot = args.chatbot
    

    def get_response(args,message):
        message_list = [
        {"role": "user", "content": message}
        ]
        decision = chatbot.compeletion(args.api_model, message_list, args.max_retry, temperature = args.temperature, max_tokens = args.max_new_tokens)
        return decision
    
    def get_response_hf(args,message):
        '''
        Get response from Hugging Face model
        '''
        response = args.chatbot.respond(message, max_new_tokens=args.max_new_tokens)
        return response

    get_response_fc = get_response if args.api_name != 'hf' else get_response_hf

    response_list = []
    prompt_templates = get_prompt_templates()
    for i, cur_case in enumerate(tqdm(dataset)):
        # if i > 5:
        #     break
        case_content = cur_case['case_content']
        norm_type = cur_case['norm_type']
        #label_list = label_transform(norm_type)
        log(str(f"=== domain: {domain} --- case: {i}\n"), args.log_path)
        case_dict = {}
        case_dict['norm_type'] = norm_type
        case_dict['case_id'] = i
        for k,v in prompt_templates.items():
            cur_dict = {}
            case_dict[k] = {}
            message = v.replace(args.context_placeholder, case_content)
            #message = message.replace('[LABEL_PLACEHOLDER]', ', '.join(label_list))
            log(str(f"---- {k} \n"), args.log_path)
            #log(message, args.log_path)
            for _ in range(args.generation_round):
                try:
                    response_dict = get_response_fc(args, message)
                    response = response_dict['response']
                    if args.api_name == 'deepseek' and '</think>' in response:
                        response = response.split('</think>')[1].strip()
                        cur_dict['rationale'] = response.split('</think>')[0].strip()
                    elif args.api_name == 'deepseek':
                        cur_dict['rationale'] = response_dict.get('rationale', '')
                    response_dict = parse_json_dict(response)
                    cur_dict['query'] = message
                    cur_dict['case_id'] = i
                    cur_dict['question_type'] = k
                    cur_dict['response'] = response
                    if not response_dict or 'analyze_response' in response_dict:
                        log(str(f"Failed to parse the response, response: {response}"), args.log_path)
                    cur_dict['response_dict'] = response_dict
                    log(cur_dict, args.log_path)
                    case_dict[k] = cur_dict

                    if response_dict and 'analyze_response' not in response_dict:
                        break
                except Exception as e:
                    log(str(e), args.log_path)
                    print(f"Error in processing case {i} for question type {k}: {e}")
                    continue
        response_list.append(case_dict)
        if i % 10 == 5:
            with open(response_save_path, 'w') as f:
                json.dump(response_list, f, indent=4)

    with open(response_save_path, 'w') as f:
        json.dump(response_list, f, indent=4)
    return response_list

def main(args):
    set_seeds(args)
    KBs = get_local_KB_dataset()
    result_save_path = args.log_path.replace('.txt', '_results.json')
    for domain in args.domains.split('+'):
        assert domain in ['GDPR', 'HIPAA', 'AI_ACT', 'ACLU'], 'Invalid domain name' 
        if domain == 'ACLU':
            KB_dataset = None # we haven't annotated the related clauses for cases in ACLU
        else:
            KB_dataset = KBs[domain]
        case_dataset = get_local_case_dataset(domain)
        eval_dataset = case_dataset['test']
        ## random sample 10 cases
        # dataset_len = len(eval_dataset)
        # if dataset_len > 10:
        #     selected_indices = random.sample(range(dataset_len), 10)
        #     eval_dataset = eval_dataset.select(selected_indices)
        # log(f"Domain: {domain}, selected samples: {selected_indices}", args.log_path)
        #eval_dataset = eval_dataset.select([0,1])
        reseponse_list = get_llm_response(eval_dataset, args, domain)
        parsed_list = parse_response_list(reseponse_list, args)
        result_list = analyze_result(parsed_list)
        with open(result_save_path, 'w') as f:
            json.dump(result_list, f, indent=2)


def analyze_result(parsed_list):
    '''
    Analyze the parsed response list and return the results
    '''

    def parse_result(input_dict, temp_dict):
        for k,v in input_dict.items():
            if v.lower() == 'no':
                temp_dict['prohibit_count'] += 1
                temp_dict['pred'] = 'prohibit'
                temp_dict['violated_article'].append(k)
            elif v.lower() == 'yes':
                temp_dict['permit_count'] += 1
                temp_dict['permitted_article'].append(k)
            elif v.lower() == 'not sure':
                temp_dict['unknown_context'].append(k)

    def parse_lawful_dict(input_dict, temp_dict):
        '''
        Parse the lawful prompt dictionary
        '''
        yes_count = 0
        for k,v in input_dict.items():
            if v.lower() == 'no':
                temp_dict['prohibit_count'] += 1
                temp_dict['pred'] = 'prohibit'
                temp_dict['violated_article'].append(k)
            elif v.lower() == 'yes':
                temp_dict['permit_count'] += 1
                temp_dict['permitted_article'].append(k)
                yes_count += 1
            elif v.lower() == 'not sure':
                temp_dict['unknown_context'].append(k)
        if yes_count:
            temp_dict['pred'] = 'permit'

    def locate_special_condition(input_dict, temp_dict):
        '''
        Locate the special condition in the input dictionary
        '''
        for k,v in input_dict.items():
            if v.lower() == 'yes':
                temp_dict['applicable_special_conditions'].append(k)
            elif v.lower() == 'not sure':
                temp_dict['unknown_context'].append(k)

    ret_list = []
    correct_count = 0
    for case_dict in parsed_list:
        #if case_dict['case_id'] == 15:
            #print("Skipping case 15 due to known issues.")
        temp_dict = {}
        temp_dict['violated_article'] = []
        temp_dict['permitted_article'] = []
        temp_dict['prohibit_count'] = 0
        temp_dict['permit_count'] = 0
        temp_dict['case_id'] = case_dict['case_id']
        temp_dict['norm_type'] = case_dict['norm_type']
        temp_dict['unknown_context'] = []
        temp_dict['pred'] = 'permit' # default prediction is 'permit'
        temp_dict['applicable_special_conditions'] = []
        norm_type = case_dict['norm_type']
        label_list = label_transform(norm_type)

        processor_dict = case_dict['processor_prompt']
        parse_result(processor_dict, temp_dict)
        ### subject_dict
        subject_dict = case_dict['subject_prompt']
        locate_special_condition(subject_dict, temp_dict)
        ### special_dict
        special_dict = case_dict['special_prompt']
        locate_special_condition(special_dict, temp_dict)

        ### lawful_dict
        lawful_dict = case_dict['lawful_prompt']
        parse_lawful_dict(lawful_dict, temp_dict)

        ### principal_dict
        principal_dict = case_dict['principal_prompt']
        parse_result(principal_dict, temp_dict)

        ### result

        result = temp_dict['pred'] in label_list
        temp_dict['result'] = int(result)
        correct_count += int(result)

        ret_list.append(temp_dict)

    statement = f"Correct count: {correct_count}, Total count: {len(parsed_list)}, Accuracy: {correct_count / len(parsed_list):.4f}"
    print(statement)
    log(statement, args.log_path)
    return ret_list



def process_scope(scope_dict):
    '''
    Process the scope response dictionary
    return emtpy string if the could not get the key
    '''
    scope = scope_dict.get('is_gdpr_applicable', '')
    if scope.lower() in ['yes', 'true', 'applicable']:
        return 'yes'
    elif scope.lower() in ['no', 'false', 'not applicable']:
        return 'no'
    else:
        return ''


def filter_irrelevant(cur_dict):
    '''
    Filter the irrelevant context from the response dictionary
    '''
    new_dict = {}
    for k,v in cur_dict.items():
        if 'no' in v.lower():
            continue
        new_dict[k] = v
    return new_dict
def parse_response_list(reseponse_list: list, args: argparse.Namespace) -> list:
    '''
    Parse the response list to a dictionary
    '''
    ret_list = []
    for case_dict in reseponse_list:
        result_dict = {}
        # if case_dict['case_id'] == 15:
        #     print("Skipping case 15 due to known issues.")
        try:    
            scope_dict = case_dict['scope_prompt']['response_dict']
            special_dict = case_dict['special_prompt']['response_dict']
            subject_dict = case_dict['subject_prompt']['response_dict']
            processor_dict = case_dict['processor_prompt']['response_dict']
            lawful_dict = case_dict['lawful_prompt']['response_dict']
            principal_dict = case_dict['principal_prompt']['response_dict']
            result_dict['case_id'] = case_dict['case_id']
            result_dict['norm_type'] = case_dict['norm_type']            
            ### process one by one
            scope = process_scope(scope_dict)
            if scope == 'no' or scope == '':
                result_dict['scope_prompt'] = 'not applicable'
            else:
                result_dict['scope_prompt'] = 'applicable'
            result_dict['special_prompt'] = filter_irrelevant(special_dict)
            result_dict['subject_prompt'] = filter_irrelevant(subject_dict)
            result_dict['processor_prompt'] = processor_dict
            result_dict['lawful_prompt'] = lawful_dict
            result_dict['principal_prompt'] = principal_dict
            ret_list.append(result_dict)

        except Exception as e:
            print(f"Error in processing case {case_dict['case_id']}: {e}")
            log(f"Error in processing case {case_dict['case_id']}: {e}", args.log_path)
            continue


    return ret_list



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--context_placeholder", type=str, default="[CONTEXT_PLACEHOLDER]")
    parser.add_argument("--model", type=str, default="")
    #parser.add_argument("--log_path", type=str, default=f"logs/log.txt")
    #parser.add_argument("--prompt_template", type=str, default="prompts/cot-answer-prompt-auto.txt")
    parser.add_argument("--max_new_tokens", type=int, default=512)

    parser.add_argument("--generation_round", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--api_name", type=str, default=config.API_NAME)
    ### newly appeneded
    parser.add_argument("--domains", type=str, default='GDPR')
    #parser.add_argument("--api_model", type=str, default=config.API_MODEL)
    parser.add_argument("--api_model", type=str, default='gpt-4o')
    parser.add_argument("--api_token", type=str, default=config.OPENAI_API_KEY)
    parser.add_argument("--max_retry", type=int, default=3)
    parser.add_argument("--temperature", type=float, default=0.2)
    args = parser.parse_args()


    #args.log_path = args.log_path.replace('.txt', f'_{args.api_model}.txt')
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
    args.log_path = f'logs/{args.api_model}/log.txt'
    main(args)
