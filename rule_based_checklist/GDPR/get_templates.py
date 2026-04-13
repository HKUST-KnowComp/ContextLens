from prompts.prompt_prepare import PromptTemplate
import os




def format_template(template, context):
    """
    Formats the template with the provided context.
    """
    return template.format(context=context)



def save_prompts(prompt, filename):
    """
    prompt: a formatted prompt string.
    Saves the formatted prompts to a file.
    """
    save_path = os.path.join('prompts', filename)
    with open(save_path, 'w') as file:
        file.write(prompt)
        


if __name__ == "__main__":
    template = PromptTemplate()
    print('template loaded')
    context = '[CONTEXT_PLACEHOLDER]\n\n'

    ### Q1
    scope_prompt = format_template(template.scope_prompt, context)
    scope_pure_prompt = format_template(template.scope_pure_prompt, context)

    special_prompt = format_template(template.special_prompt, context)
    subject_prompt = format_template(template.subject_prompt, context)
    processor_prompt = format_template(template.processor_prompt, context)
    lawful_prompt = format_template(template.lawful_prompt, context)
    principal_prompt = format_template(template.principal_prompt, context)


    print('prompt loaded')
    save_prompts(scope_prompt, 'scope_prompt.txt')
    save_prompts(scope_pure_prompt, 'scope_pure_prompt.txt')
    save_prompts(special_prompt, 'special_prompt.txt')
    save_prompts(subject_prompt, 'subject_prompt.txt')
    save_prompts(processor_prompt, 'processor_prompt.txt')
    save_prompts(lawful_prompt, 'lawful_prompt.txt')
    save_prompts(principal_prompt, 'principal_prompt.txt')
    print('prompts saved')