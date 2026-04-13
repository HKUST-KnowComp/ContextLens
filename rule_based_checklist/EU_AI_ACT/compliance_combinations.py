import random
from data import *

import numpy as np
from tqdm import tqdm

def generate_random_bool_list_with_probs(probabilities):
    return [np.random.rand() < prob for prob in probabilities]

# # Example usage
# length = 10  # Length of the list
# probabilities = [0.1, 0.5, 0.3, 0.8, 0.2, 0.7, 0.4, 0.6, 0.9, 0.05]  # Different probabilities for each element
# bool_list = generate_random_bool_list_with_probs(length, probabilities)
# print(bool_list)

def random_sample_choices(random_bool_list,entity_type):
    ''' 
    return a dict that contains choises for each question
    '''
    assert entity_type in ['Provider','Deployer', 'Distributor', 'Importer',  'Product Manufacturer', 'Authorised Representative',]
    sampled_status_index = {}
    # random_bool_list = [random.choice([True, False]) for _ in range(len(status_index_dict))] # the first bool value is non-sense
    #assert len(prob_list) == len(status_index_dict)
    #random_bool_list = generate_random_bool_list_with_probs(prob_list)
    for i, key in enumerate(status_index_dict.keys()):
        if key == 'entity':
            #sampled_status_index[key] = [random.choice(status_index_dict[key])]
            sampled_status_index[key] = entity_type
        elif key in ['general_purpose', 'is_significant', 'is_your_product', 'is_your_product']:
            ##sampled_status_index[key] = [int(not random_bool_list[i])]
            sampled_status_index[key] = [idx for idx in range(2)]
        else:
            if random_bool_list[i] == True:
                #sampled_status_index[key] = random.sample(status_index_dict[key][:-1], random.choice(status_index_dict[key][1:-1]))
                sampled_status_index[key] = [idx for idx in status_index_dict[key][:-1]]
                if key == 'excluded_system' and sampled_status_index['entity'][0] == 0 and random_bool_list[3] == True:
                    # for provider, if it is for a general purpose, then the number of choises becomes 4.
                    pass
                    # sampled_status_index[key] = random.sample(status_index_dict[key][:-1], random.choice(status_index_dict[key][1:-2]))
                if key == 'transparent' and sampled_status_index['entity'][0] == 1: # for deployer, transparent is different
                    #sampled_status_index[key] = random.sample(range(4), random.choice([1,2,3]))
                    sampled_status_index[key] = [idx for idx in range(3)]
                # if key == 'scope' and sampled_status_index['entity'][0] == 5: # for authorised representative, scope is different
                #     sampled_status_index[key] = [0]
                if key == 'scope' and sampled_status_index['entity'][0] == 3 and sampled_status_index['modification'] == [3]: # for importor, scope is different, yet same with authorised representative
                    sampled_status_index[key] = [0]
                if key == 'scope' and sampled_status_index['entity'][0] == 2 and sampled_status_index['modification'] == [3]: # for distributor, scope is different, yet same with authorised representative
                    sampled_status_index[key] = [0]
                if key == 'scope' and sampled_status_index['entity'][0] == 1 and sampled_status_index['modification'] == [3]: # for deployer, scope is different; scope range from 0 - 2
                    ##sampled_status_index[key] = random.sample([0,1,2], random.choice([1,2,3]))
                    sampled_status_index[key] = [idx for idx in range(3)]
                if key == 'modification' and sampled_status_index['entity'][0] == 4 : # for manufacturer, the modification is for conditions choices
                    ##sampled_status_index[key] = random.sample([0,1], random.choice([1,2]))
                    sampled_status_index[key] = [idx for idx in range(2)]
            else:
                sampled_status_index[key] = [len(status_index_dict[key])-1]
                if key == 'transparent' and sampled_status_index['entity'][0] == 1: # for deployer, transparent is different
                    sampled_status_index[key] = [3]
                # if key == 'scope' and sampled_status_index['entity'][0] == 5: # for authorised representative, scope is different
                #     sampled_status_index[key] = [1]
                if key == 'scope' and sampled_status_index['entity'][0] == 3 and sampled_status_index['modification'] == [3]:
                    sampled_status_index[key] = [1]
                if key == 'scope' and sampled_status_index['entity'][0] == 2 and sampled_status_index['modification'] == [3]:
                    sampled_status_index[key] = [1]
                if key == 'scope' and sampled_status_index['entity'][0] == 1 and sampled_status_index['modification'] == [3]:
                    sampled_status_index[key] = [len(status_index_dict[key])-1]
                if key == 'modification' and sampled_status_index['entity'][0] == 4:
                    sampled_status_index[key] = [2]
    return random_bool_list, sampled_status_index


excluded_system_type = ['military', 'authority', 'research', 'personal', 'open-sourse', None]
role_type_list = ['Provider','Deployer', 'Distributor', 'Importer',  'Product Manufacturer', 'Authorised Representative',]
entity_to_index = {entity: index for index, entity in enumerate(role_type_list)}

def verify_and_display(random_bool_list, sampled_status_index):
    def return_trans_type(role_type):
        if role_type == 'Deployer':
            transparency_type = ['bio', 'content', 'deepfake', None]
        else:
            transparency_type = ['people', 'content', None]
        return transparency_type
    entity_trial = role_type_list[sampled_status_index['entity'][0]]
    #entity_trial = sampled_status_index['entity']
    question_flow, result = verifier(
        entity=entity_trial,
        modification=random_bool_list[1],
        scope=random_bool_list[2],
        general_purpose=random_bool_list[3],
        excluded= [excluded_system_type[i] for i in sampled_status_index['excluded_system']],
        prohibited=random_bool_list[5],
        annex1_sectionB=random_bool_list[6],
        annex1_sectionA=random_bool_list[7],
        annex3=random_bool_list[8],
        transparency_type = [return_trans_type(entity_trial)[i] for i in sampled_status_index['transparent']],
        your_product=random_bool_list[10],
        significant=random_bool_list[11]
        )
    
    quesion_str = question_option_replay(question_flow, sampled_status_index)
    statement_str = question_option_replay_statements(question_flow, sampled_status_index)

    return quesion_str, result, statement_str


import itertools
from itertools import product

def span_options(sampled_status_index):
    '''
    Each ley should be one element in the list
    iterate through all the keys and values and create a list of status_index
    '''
    #keys = sampled_status_index.keys()
    #values = sampled_status_index.values()
    keys = [k for k, v in sampled_status_index.items() if isinstance(v, list)]
    values = [sampled_status_index[k] for k in keys]
    constant_items = {k: v for k, v in sampled_status_index.items() if not isinstance(v, list)}
    if 'entity' in constant_items.keys():
        constant_items['entity'] = [entity_to_index[constant_items['entity']]]
    #combinations = product(*values)
    #result = [dict(zip(keys, combo)) for combo in combinations]
    result = []
    for combo in product(*values):
        combo_dict = dict(zip(keys, combo))
        combo_dict.update(constant_items)  # merge in the constant keys
        result.append(combo_dict)
    return result


def case_generation(num_generation=10, prob_list=[0.5]*len(status_index_dict)):
    entity_type_list = ['Provider','Deployer', 'Distributor', 'Importer',  'Product Manufacturer', 'Authorised Representative']
    ### set q1, 
    #bool_list_all = list(itertools.product([True, False], repeat=len(status_index_dict)))
    bool_list_all = [True] * len(status_index_dict)
    bool_list_all = [bool_list_all]
    ### reduce repeated results, make the results always True for 'entity','general_purpose', 'is_significant', 'is_your_product', 
    # for i, bool_list in enumerate(bool_list_all):
    #     bool_list_all[i] = list(bool_list)
    #     bool_list_all[i][0] = True
    #     bool_list_all[i][3] = True
    #     bool_list_all[i][11] = True
    #     bool_list_all[i][10] = True
    # #bool_list_all = list(set(bool_list_all))
    # bool_list_all = list(set(tuple(bool_list) for bool_list in bool_list_all))
    all_results = []
    for entity_type in entity_type_list:
        element_count = 0
        temp_recorder = {}
        generated_question_result = []
        for bool_list in tqdm(bool_list_all):
            random_bool_list, sampled_status_index = random_sample_choices(random_bool_list=bool_list, entity_type=entity_type)
            span_status_index = span_options(sampled_status_index)

            bool_list_str = str(bool_list)
            temp_recorder[bool_list_str] = len(span_status_index)
            # with open(f'temp_recorder_{entity_type}.json', 'w') as f:
            #     json.dump(temp_recorder, f, indent=4)
            
            for sampled_status_index_element in span_status_index:
                for k in sampled_status_index_element.keys():
                    v = sampled_status_index_element[k]
                    if isinstance(v, int):
                        sampled_status_index_element[k] = [v]
                element_count += 1
                quesion_str, result, statement_str = verify_and_display(random_bool_list, sampled_status_index_element)
                generated_question_result.append(
                    {
                    'random_bool_list': random_bool_list, 
                    'sampled_status_index': sampled_status_index_element,
                    'question': quesion_str,
                    'statement': statement_str,
                    'result': result
                    }
                )
        all_results.extend(generated_question_result)

        print(f'Total number of unique results for {entity_type}: {len(generated_question_result)}')
        with open(f'all_results_{entity_type}.json', 'w') as f:
            json.dump(generated_question_result, f, indent=4)
        
    return all_results


import json

if __name__ == '__main__':
    all_results = case_generation()
    all_results = list(set(all_results))
    print(f'Total number of unique results: {len(all_results)}')
    ### save to json
    with open('all_results.json', 'w') as f:
        json.dump(all_results, f, indent=4)