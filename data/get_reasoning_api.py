import os
import sys
import config
os.environ['HF_TOKEN'] = config.HF_TOKEN
os.environ['HF_HOME'] = config.HF_HOME

import argparse
import copy
import json
import pandas as pd
import sys

from tqdm import tqdm


from api_utils import *
import random
import numpy as np
import torch
import concurrent.futures

def set_seeds(args):
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)




def process_domain_data(case_dataset, batch_size, args, domain):
    ### convert to batchs
    all_outputs = []
    results = []

    for i in tqdm(range(0, len(case_dataset), batch_size)):
        batch = case_dataset[i:i+batch_size]
        batch_len = len(batch['sender'])
        ### a list of vars
        ids = [i+j for j in range(batch_len)]
        case_contents = case_dataset['case_content']
        norm_types = case_dataset['norm_type']

        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_index = {
                 executor.submit(process_single_case, idx, case_content, norm_type, args, domain): idx
            for case_content, norm_type, idx in zip(case_contents, norm_types, ids)
            }
            for future in concurrent.futures.as_completed(future_to_index):
                index = future_to_index[future]
                try:
                    result, decision, norm_type = future.result()
                    results.append(result)
                    case_output = {
                        'id': index,
                        'result': result,
                        'decision': decision,
                        'norm_type': norm_type
                    }
                    all_outputs.append(case_output)
                except Exception as exc:
                    print(f'generated an exception: {exc}')
                    case_output = {
                        'id': -1,
                        'result': 'NA',
                        'decision': 'NA',
                        'norm_type': 'NA'
                    }
                    all_outputs.append(case_output)
                    results.append(0)
        
        ### display the result for the last batch
        log(str(f"---batch starts on: {i}\n"), args.log_path)
        for case_output in all_outputs[i:i+batch_len]:
            idx = case_output['id']
            result = case_output['result']
            norm_type = case_output['norm_type']
            decision = case_output['decision']

            log(str(f"=== domain: {domain} --- case: {idx}\n"), args.log_path)
            log(str(f"sample_id: {idx} --- result:{result} --- answer: {norm_type}\n"), args.log_path)
            log(str(decision)+"\n", args.log_path)

    acc = (sum(results) / len(results))
    print(acc)
    log(str(f"domain: {domain} --- num_sample: {len(case_dataset)} --- accuracy:{acc}\n"), args.log_path)
    log(str(f"domain: {domain} --- num_sample: {len(case_dataset)} --- accuracy:{acc}\n"), args.result_save_path)

def main(args):
    set_seeds(args)
    log(str(args),args.log_path)
    KBs = get_KB_dataset()
    cases = get_local_case_dataset()

    ### batch_size
    batch_size = args.api_batch_size
    #if args.api_name:
    #    chatbot = ''


    result_save_path = args.log_path.replace('.txt', '_results.txt')
    args.result_save_path = result_save_path
    for domain in args.domains.split('+'):
        assert domain in ['GDPR', 'HIPAA', 'AI_ACT'], 'Invalid domain name' 
        KB_dataset = KBs[domain]
        case_dataset = cases[domain]['train']
        process_domain_data(case_dataset, batch_size, args, domain)



    # permit/prohibit/not applicable

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    #parser.add_argument("--model", type=str, default="meta-llama/Llama-3.1-8B-Instruct")
    parser.add_argument("--model", type=str, default="")
    parser.add_argument("--log_path", type=str, default="rl_log/deepseek_r1.txt")
    parser.add_argument("--max_new_tokens", type=int, default=1024)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--api_name", type=str, default='deepseek')
    ### newly appeneded
    parser.add_argument("--domains", type=str, default='GDPR+HIPAA+AI_ACT')
    parser.add_argument("--api_model", type=str, default='deepseek')
    parser.add_argument("--api_token", type=str, default='INPUT_YOUR_API_TOKEN')
    parser.add_argument("--max_retry", type=int, default=5)
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--num_sample_per_label", type=int, default=50)
    args = parser.parse_args()
    main(args)
