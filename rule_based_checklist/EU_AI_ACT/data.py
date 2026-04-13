


result_dict = {
'handover_oblig': 'Handover obligations: If a deployer, distributer, or importer makes a \'substantial modification\' (see Article 3 point 23) to your system, they will be considered a \'provider\' of that system under Article 25. The original provider will not longer be considered a provider of that particular system. However, the original provider will have obligations to provide the new provider with: Technical documentation. Information about the capabilities of the AI system. Technical access. Assistance to help the new provider fulfil their obligations under the Act.',
'provider_oblig': 'Provider obligations: As a provider of a high-risk AI system, you must comply with the obligations listed under Article 16.',
'high_risk_oblig_green': 'High-risk obligations: Under Article 6, high-risk obligations apply to systems that are considered a \'safety component\' of the kind listed in Annex I Section A, and to systems that are considered a \'High-risk AI system\' under Annex III. You need to follow these obligations for high-risk systems: Establish and implement risk management processes according to Article 9. Use high-quality training, validation and testing data according to Article 10. Establish documentation and design logging features according to Article 11 and Article 12. Ensure an appropriate level of transparency and provide information to users according to Article 13. Ensure human oversight measures are built into the system and/or implemented by users according to Article 14. Ensure robustness, accuracy and cybersecurity according to Article 15. Set up a quality management system according to Article 17.',
'general_purpose_oblig': 'General Purpose AI model obligations: You need to follow these obligations for General Purpose AI models under Article 53. In summary, you must: Create and keep technical documentation for the AI model, and make it available to the AI Office upon request. Create and keep documentation for providers integrating AI models, balancing transparency and protection of IP. Put in place a policy to respect Union copyright law. Publish a publicly available summary of AI model training data according to a template provided by the AI Office. Also, consider whether the GPAI is used as, or a component of, an AI system. If so, obligations on high risk AI systems may apply directly or indirectly under Recital 85.',
'transparency_oblig_people': 'Transparency obligations: Natural persons You need to follow these transparency obligations under Article 50: The AI system, the provider or the user must inform any person exposed to the system in a timely, clear manner when interacting with an AI system, unless obvious from context. Where appropriate and relevant include information on which functions are AI enabled, if there is human oversight, who is responsible for decision-making, and what the rights to object and seek redress are.',
'excluded_research': 'Excluded: Research & development: AI systems and models with the sole purpose of scientific research and development are excluded. For all other systems, research & development activities are likely excluded until your AI system is placed on the market or put into service. Systems and activities that are excluded are not subject to any obligations. For more information see Article 2 points 5a and 5b. Definitions for these results Place on the market: the first making available of an AI system or a general purpose AI model on the Union market. Put into service: the supply of an AI system for first use directly to the deployer or for own use in the Union for its intended purpose.',
'transparency_oblig_content': 'Transparency obligations: Synthetic content You need to follow these transparency obligations under Article 50: Ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated. This does not apply to content authorised by law.',
'out_of_scope': 'Out of scope: Your system is likely outside of the scope of the EU AI Act. For more information about the scope of the Act, please see Article 2.',
'excluded_military_authurity': 'Excluded: Your system is likely excluded from the EU AI Act, which means you do not face any obligations. For more information see Article 2.',
'excluded_personal': 'Excluded: Personal, non-professional activity: Purely personal, non-professional uses of AI systems are likely excluded and are not subject to any obligations. For more information see Article 2 point 5c.',
'excluded_opensourse': 'Excluded: Open source systems: Until your AI system is placed on the market or put into service by a provider as part of an AI system that is high-risk, prohibited, general purpose, or has transparency obligations, your open source system is likely excluded from the EU AI Act, which means it is not subject to any obligations. For more information see Article 2 point 5g. Definitions for these results Place on the market: the first making available of an AI system or a general purpose AI model on the Union market. Put into service: the supply of an AI system for first use directly to the deployer or for own use in the Union for its intended purpose.',
'prohibited': 'Prohibited: Your system is likely prohibited under the EU AI Act. For more information see Article 5.',
'high_risk_oblig_yollow': 'High-risk exception: Your system likely falls under an Article 2 exception. This means that only Article 112 applies to your system, and you should: Comply with any existing regulations; Stay on the lookout for new developments from the EU and comply with any new regulations. Article 84 mostly describes obligations for the Commission to regularly review and update the EU AI Act, so the primary obligation for you is to keep an eye on these obligations and maintain compliance.',
'submit_to_PCA': 'Providers must submit notification to NCA If a provider considers their AI system to not pose a significant risk (see Article 6 point 2a) they must register their system in the EU database before that system is placed on the market or put into service (see Article 49 point 1a). They must also document their assessment and provide this documentation to the National Competent Authorities (NCA) upon request (see Article 6 point 2b). If a market surveillance authority finds that the AI system has been misclassified (see Article 80), your system would be subject to the \'high-risk\' obligations described in Chapter III Section 2 and you may be subject to fines under Article 99.',
'no_oblig': 'No obligations: The EU AI Act likely imposes no legal obligations on your AI system. The European Commission may publish a voluntary code of conduct in future that you may be asked to comply with on a voluntary basis. See Article 95 on Codes of Conduct.',

# for deployer: 
'deployer_oblig': 'Deployer obligations: As a deployer of a high-risk AI system, you must comply with Article 26 obligations. These include: Taking appropriate technical and organisational measures to ensure they use such systems in accordance with the instructions of use accompanying the systems. Monitoring the operation of the system on the basis of the instructions of use and when relevant, informing providers in accordance. Prior to installing or using the system within the workplace, consulting workers representatives with a view to reaching an agreement in accordance with Directive 2002/14/EC and informing the affected employees that they will be subject to the system. Cooperating with the relevant national competent authorities on any action those authorities take in relation with the high-risk system in order to implement the Regulation. To the extent that you exercise control over the system, you must: Implement human oversight, ensuring that the person or persons assigned to ensure this oversight are competent, properly qualified and trained, and have the necessary resources in order to ensure effective supervision. Ensure that relevant and appropriate robustness and cybersecurity measures are regularly monitored for effectiveness and are regularly adjusted or updated. Ensure that input data is relevant and sufficiently representative in view of the intended purpose of the high-risk AI system. Keep logs automatically generated by the system for at least six months. Where the system makes decisions or assists in decision-making related to people (such as in hiring or education), you must inform those people: That they are subject to the use of the high-risk AI system. Of the system\'s intended purpose and the type of decisions it makes. About their right to an explanation. If you believe that using the AI system according to its instructions might harm the health, safety, or rights of any person, you must: Without undue delay, inform the provider or distributor and relevant national supervisory authorities. Suspend the use of the system. If you have identified any serious incident or any malfunctioning, you must: Interrupt the use of the AI system. Immediately inform first the provider, and then the importer or distributor and relevant national supervisory authorities.',
'deployer_transparent_deepfake': 'Transparency obligations: Deep fakes You need to follow these transparency obligations under Article 50: Disclose that the content has been artificially generated or manipulated. Disclose, whenever possible, the name of the natural or legal person that generated or manipulated the content. Label the content as inauthentic. Information must be provided at first interaction or exposure and be accessible to vulnerable persons. This does not apply to content authorised by law or necessary for freedom of expression and arts and sciences.',
'deployer_transparent_bio': 'Transparency obligations: Emotion & biometric You need to follow these transparency obligations under Article 50: Obtain user consent before processing biometric and other personal data, unless authorised by law for criminal offences.',
'deployer_transparent_content': 'Transparency obligations: Synthetic content You need to follow these transparency obligations under Article 50: Ensure that the outputs of the AI system are marked in a machine-readable format and detectable as artificially generated or manipulated. This does not apply to content authorised by law.',

# for distributor:
'distributor_oblig': 'Distributor obligations: As a distributor, you must comply with Article 24 obligations. These include: Before distributing a high-risk AI system, verifying it has the required CE conformity marking, documentation, and instructions for use, and that the provider and importer have fulfilled their obligations. Not distributing non-compliant high-risk AI systems. If a system poses a risk, you must inform the provider, importer, and national competent authority of that. Ensuring storage and transport conditions do not jeopardise compliance of high-risk AI systems. If a distributed high-risk AI system is found to be non-compliant, to take corrective actions and report the non-compliant systems to the provider or importer, as well as national competent authorities. Providing the national competent authority with all necessary information and documentation to demonstrate a high-risk system\'s conformity, upon request. Cooperating with national competent authorities on actions to reduce and mitigate risks of high-risk AI systems.',

# for importor:
'importor_oblig': 'Importer obligations: As an importer, you must comply with Article 23 obligations. These include: Indicating your business name and address on the system or documentation. Ensuring proper storage and transport to maintain compliance. Providing authorities, upon a reasoned request, the necessary information and documentation to demonstrate conformity, including access to system logs. Cooperating with authorities on actions to reduce and mitigate system risks. If you are importing an AI system that is considered high-risk under Article 6, ensuring that the system conforms to the regulation by verifying that the provider conducted the proper conformity assessment, drew up the technical documentation, affixed the conformity marking, and included documentation and instructions. If you believe a system is non-conforming or counterfeit, you: Cannot place it on the market until it conforms. Must inform the provider and authorities of risks.',


# for authorized representatives:
'authorised_representatives_oblig': 'Authorised representative obligations: As an authorised representative appointed by an AI system provider via a written mandate, you must comply with Article 22 obligations. This includes: Being based in the EU. Performing mandated tasks. Providing a copy of the mandate to market surveillance authorities upon request. Being mandated to communicate with authorities on behalf of the provider on compliance issues. However, if you consider or have reason to consider that the provider is acting contrary to its obligations under the AI Act, you must immediately inform: The national supervisory authority of the Member State in which you are established. The relevant notified body, where applicable.',
}


status_index_dict = {
    'entity': range(6),
    'modification': range(4),
    'scope': range(5),
    'general_purpose': range(2),
    'excluded_system': range(5),
    'prohibit_system': range(9),
    'annex1_sectionB': range(8),
    'annex1_sectionA': range(13),
    'annex3': range(9),
    'transparent': range(3),
    'is_your_product': range(2),
    'is_significant': range(2),
}


question_dict = {
    'entity': 'Which kind of entity is your organisation?',
    'modification': 'Do you perform any of the following actions?',
    'scope': 'Do you meet any of the following criteria?',
    'general_purpose': 'Is your system a General Purpose AI model? General Purpose AI model: an AI model, including when trained with a large amount of data using self-supervision at scale, that displays significant generality and is capable to competently perform a wide range of distinct tasks regardless of the way the model is placed on the market and that can be integrated into a variety of downstream systems or applications.',
    'excluded_system': 'Does your system fall within any of the following categories?',
    'prohibit_system': 'Does your system perform any of these functions',
    'annex1_sectionB': 'Does your AI system (or the product for which your AI system is a \'safety component\') fall within any of the following high-risk categories? Safety component: A component of a product or of a system which fulfils a safety function for that product or system, or the failure or malfunctioning of which endangers the health and safety of persons or property. Select options from Annex 1, Section B',
    'annex1_sectionA': 'Select options from Annex 1, Section A',
    'annex3': 'Does your AI system fall within any of the following high-risk categories?',
    'transparent': 'Does your system perform any of these functions?',
    'is_your_product': 'Is your product (or the product for which your AI system is a \'safety component\') required to undergo a third-party conformity assessment under these existing EU laws?',
    'is_significant': 'Does your AI system pose a significant risk of harm to the health, safety or fundamental rights of any person?',
    'provider_modification': 'Has a downstream deployer, distributer, or importer made any of the following modifications to your system?',
    'product_manufaturer_condition': 'Does the AI system in your product meet any of these conditions?',
}


question_dict_statements = {
    'entity': 'Your organisation is which kind of entity:',
    'modification': 'You perform any of the following actions:',
    'scope': 'You meet any of the following criteria:',
    'general_purpose': 'Your system is a General Purpose AI model:',
    'excluded_system': 'Your system falls within any of the following categories:',
    'prohibit_system': 'Your system performs any of these functions:',
    'annex1_sectionB': 'Your AI system (or the product for which your AI system is a "safety component") falls within any of the following high-risk categories:',
    'annex1_sectionA': 'Select options from Annex 1, Section A:',
    'annex3': 'Your AI system falls within any of the following high-risk categories:',
    'transparent': 'Your system performs any of these functions:',
    'is_your_product': 'Your product (or the product for which your AI system is a "safety component") is required to undergo a third-party conformity assessment under these existing EU laws:',
    'is_significant': 'Your AI system poses a significant risk of harm to the health, safety or fundamental rights of any person:',
    'provider_modification': 'A downstream deployer, distributor, or importer has made any of the following modifications to your system:',
    'product_manufaturer_condition': 'The AI system in your product meets any of these conditions:'
}


option_dict = {
    'entity': ['Provider','Deployer', 'Distributor', 'Importer', 'Product Manufacturer', 'Authorised Representative'],
    'modification': [
        'Putting a different name/trademark on the system.', 
        'Modifying the intended purpose of a system already in operation.',
        'Performing a substantial modification (see Article 3 point 23) to the system',
        'None of the above'
    ],
    'scope': [
        'I am placing on the market or putting into service Al systems in the Union(regardless of whether you are established within the Union or in a thirdcountry).',
        'My AI system\'s output is used in the EU.', 
        'My AI system is located in a non-EU country where \'EU Member State lawapplies by virtue of public international law.',
        'My system is considered to be \'prohibited\' (see Article 5) and is used by adownstream deployer who is based in the EU.',
        'None of the above',
    ],
    'general_purpose': ['Yes', 'No'],
    'excluded_system': [
        'AI systems deveIoped and used exclusively for military purposes.', 
        'AI systems used by public authorities or international organisations in third countries for law enforcement and judicial cooperation.', 
        'AI research and development activity.', 
        'People using AI systems for purely personal, non-professional activity.', 
        'AI components provided under free and open-source licences.', 
        'None of the above.'
    ],
    'prohibit_system': [
        'Subliminal techniques, manipulation, and deception',
        'Exploiting vulnerabilities',
        'Biometric categorisation',
        'Social scoring',
        'Predictive policing',
        'Expanding facial recognition databases',
        'Emotion recognition',
        'Real-time remote biometrics',
        'None of the above',
    ],
    'annex1_sectionB': [
        'Civil aviation security',
        'Two-or three-wheel vehicles and quadricycles',
        'Agricultural and forestry vehicles',
        'Marine equipment',
        'Interoperability of the rail systems',
        'Motor vehicles and their trailers',
        'Civil aviation',
        'None of the above',
    ],
    'annex1_sectionA': [
        'Machinery',
        'Toys',
        'Recreational craft & personal watercraft',
        'Lifts and safety components of lifts',
        'Equipment and protective systems intended for use in potentially explosiveatmospheres',
        'Radio equipment',
        'Pressure equipment',
        'Cableway installations',
        'Personal protective equipment',
        'Appliances burning gaseous fuels',
        'Medical devices',
        'In vitro diagnostic medical devices', 
        'None of the above',
    ],
    'annex3': [
        'Biometrics',
        'Critical infrastructure',
        'Educational and vocational training',
        'Employment, workers management, and access to self-employment',
        'Access to and enjoyment of essential private services and public services and benefits',
        'Law enforcement',
        'Migration, asylum, and border control management',
        'Administration of justice and democratic processes',
        'None of the above',
    ],
    'transparent': [
        'Interacting with people',
        'Generating synthetic audio, image, video or text content',
        'None of the above',
    ],
    'is_your_product': ['Yes', 'No'],   
    'is_significant': ['Yes', 'No'],
}

deployer_transparency_options = [
    'Emotion recognition or biometric categorisation',
    'Generating synthetic audio, image, video or text content',
    'Generating or manipulating image, audio or video content constituting adeep fake',
    'None of the above',
]

distributor_scope_options = [
    'I am established or located in EU',
    'None of the above',
]

importor_scope_options = [
    'I am established or located in EU',
    'None of the above',
]

product_manufacturer_condition_options = [
    'The Al system was/ will be \'placed on the market\' together with myproduct under my manufacturer name or trademark',
    'The Al system was/ will be \'put into service\' under my manufacturername or trademark after my product has been placed on the market',
    'None of the above',
]

def verifier(
    entity = 'Product Manufacturer',
    modification = False,
    scope = False,
    general_purpose = True,
    excluded = ['research'], # military, authority, research, personal, open-sourse; if general_purpose is true, open-sourse can be choosen: 5 choises in total
    prohibited = False,
    annex1_sectionB = False,
    annex1_sectionA = True,
    annex3 = True,
    transparency_type = ['bio'],
    your_product = False,
    significant = True,
    ):  
    assert entity in ['Provider','Deployer', 'Distributor', 'Importer',  'Product Manufacturer', 'Authorised Representative',]
    def transparency_check(type_=[]):
        if entity == 'Deployer':
            output_trans_oblig = []
            if 'content' in type_:
                output_trans_oblig.append(result_dict['deployer_transparent_content']) #'transparent oblig: content'
            elif 'deepfake' in type_:
                output_trans_oblig.append(result_dict['deployer_transparent_deepfake']) #'transparent oblig: deep fake'
            elif 'bio' in type_:
                output_trans_oblig.append(result_dict['deployer_transparent_bio']) #'transparent oblig: bio'
            return output_trans_oblig
        else:
            output_trans_oblig = []
            if 'people' in type_:
                output_trans_oblig.append(result_dict['transparency_oblig_people']) #'transparent oblig: people'
            elif 'content' in type_:
                output_trans_oblig.append(result_dict['transparency_oblig_content']) #'transparent oblig: content'
            return output_trans_oblig
    
    question_flow = ['entity']
    output = []
    if entity == 'Authorised Representative':
        output.append(result_dict['authorised_representatives_oblig'])
        question_flow.append('scope')
        if not scope:
            output.append(result_dict['out_of_scope'])
            return question_flow, output
        question_flow.append('general_purpose')
        # if general_purpose:
        #     output.append(result_dict['general_purpose_oblig']) #'general oblig')

        # exclused and prohibited checking for authorised representatives
        question_flow.append('excluded_system')
        if 'military' in excluded or 'authority' in excluded:
            output.append(result_dict['excluded_military_authurity']) # 'excluded, no oblig'] # yellow sign, over write previous oblig
            return question_flow, output
        elif 'research' in excluded:
            output.append(result_dict['excluded_research']) #'research excluded')
        elif 'personal' in excluded:
            output.append(result_dict['excluded_personal']) #'personal excluded')
        elif 'open-sourse' in excluded:
            output.append(result_dict['excluded_opensourse']) # 'open-sourse excluded')
        question_flow.append('prohibit_system')
        if prohibited: # 'prohibited']
            output.append(result_dict['prohibited'])
        return question_flow, output 

    if entity == 'Importer':
        question_flow.append('modification')
        if not modification:
            output.append(result_dict['importor_oblig'])
        question_flow.append('scope')
        if not scope:
            return question_flow, [result_dict['out_of_scope']] # ['out of scope']
        if modification:
            question_flow.append('general_purpose')
        
        question_flow.append('excluded_system')
        if 'military' in excluded or 'authority' in excluded:
            return question_flow, [result_dict['excluded_military_authurity']] # 'excluded, no oblig'] # yellow sign, over write previous oblig
        elif 'research' in excluded:
            output.append(result_dict['excluded_research']) #'research excluded')
        elif 'personal' in excluded:
            output.append(result_dict['excluded_personal']) #'personal excluded')
        elif 'open-sourse' in excluded:
            output.append(result_dict['excluded_opensourse']) # 'open-sourse excluded')
        question_flow.append('prohibit_system')
        if prohibited:
            return question_flow, [result_dict['prohibited']] # 'prohibited']
        return question_flow, output
    
    if entity == 'Product Manufacturer':
        question_flow.append('annex1_sectionA')
        if not annex1_sectionA:
            return question_flow, [result_dict['out_of_scope']]
        question_flow.append('modification')
        if not modification: # we pretent use modification as the argument for the conditiion of the ai system for product manufacturer: true: go ahead; false: return outofscope 
            return question_flow, [result_dict['out_of_scope']]
        output.append(result_dict['high_risk_oblig_green'])
        question_flow.append('scope')
        if not scope:
            return question_flow, [result_dict['out_of_scope']] # ['out of scope']
        question_flow.append('general_purpose')
        if general_purpose:
            output.append(result_dict['general_purpose_oblig']) #'general oblig')
        question_flow.append('excluded_system')
        if 'military' in excluded or 'authority' in excluded:
            return question_flow, [result_dict['excluded_military_authurity']] # 'excluded, no oblig'] # yellow sign, over write previous oblig
        elif 'research' in excluded:
            output.append(result_dict['excluded_research']) #'research excluded')
        elif 'personal' in excluded:
            output.append(result_dict['excluded_personal']) #'personal excluded')
        elif 'open-sourse' in excluded:
            output.append(result_dict['excluded_opensourse']) # 'open-sourse excluded')
        question_flow.append('prohibit_system')
        if prohibited:
            return question_flow, [result_dict['prohibited']] # 'prohibited']
        question_flow.append('transparent')
        output += transparency_check(transparency_type)
        return question_flow, output

    question_flow.append('modification')
    if modification and entity =='Provider':
        output.append(result_dict['handover_oblig'])#'handover oblig')
    question_flow.append('scope')
    if not scope:
        return question_flow, [result_dict['out_of_scope']] # ['out of scope']
    if entity == 'Provider' or modification == True:
        question_flow.append('general_purpose')
        if general_purpose:
            output.append(result_dict['general_purpose_oblig']) #'general oblig')
    question_flow.append('excluded_system')
    if 'military' in excluded or 'authority' in excluded:
        return question_flow, [result_dict['excluded_military_authurity']] # 'excluded, no oblig'] # yellow sign, over write previous oblig
    elif 'research' in excluded:
        output.append(result_dict['excluded_research']) #'research excluded')
    elif 'personal' in excluded:
        output.append(result_dict['excluded_personal']) #'personal excluded')
    elif 'open-sourse' in excluded:
        output.append(result_dict['excluded_opensourse']) # 'open-sourse excluded')
    question_flow.append('prohibit_system')
    if prohibited:
        return question_flow, [result_dict['prohibited']] # 'prohibited']
    # high risk checking:
    question_flow.append('annex1_sectionB')
    if annex1_sectionB:
        return question_flow, [result_dict['high_risk_oblig_yollow']] #'high risk oblig (yellow)']
    question_flow.append('transparent')
    output += transparency_check(transparency_type)
    
    if entity == 'Provider': # obligation for different roles
        role_oblig_choise = 'provider_oblig'
    elif entity == 'Deployer':
        role_oblig_choise = 'deployer_oblig'
    elif entity == 'Distributor':
        role_oblig_choise = 'distributor_oblig'

    question_flow.append('annex1_sectionA')
    if annex1_sectionA:
        question_flow.append('is_your_product')
        if your_product:  
            output += [result_dict[role_oblig_choise], result_dict['high_risk_oblig_green']]# 'provider oblig', 'high risk oblig (green)']
            return question_flow, output
    question_flow.append('annex3')
    if annex3:
        question_flow.append('is_significant')
        if significant:
            output += [result_dict[role_oblig_choise], result_dict['high_risk_oblig_green']]
        else:
            output.append(result_dict['submit_to_PCA']) # 'submit to NCA')
    if output == []:
        return question_flow, [result_dict['no_oblig']] # 'no oblig']
    return question_flow, output


def question_option_replay(quesion_flow, sampled_status_index):
    '''
    sampled_status_index: index of status for all the options, stored in a dictionary. e.g. {'entity': [1,2], modification: [0,1]}
    '''
    question_option_buffer = ''
    for i, q in enumerate(quesion_flow):
        if sampled_status_index['entity'] == 4 and q == 'modification':
            
            question_option_buffer += f'Q{i}: conditions\n'
        else:
            question_option_buffer += f'Q{i}: {q}\n'
        
        if sampled_status_index['entity'] == 0 and q == 'modification':
            q_ = question_dict['provider_modification']
            question_option_buffer += f'\tQustion: {q_}\n'
        elif sampled_status_index['entity'] == 4 and q == 'modification':
            q_ = question_dict['product_manufaturer_condition']
            question_option_buffer += f'\tQustion: {q_}\n'
        else:
            question_option_buffer += f'\tQustion: {question_dict[q]}\n'
        question_option_buffer += f'\tOption:\n'

        # if q =='scope':
        #     print(q)
        #     print(sampled_status_index['scope'])

        if sampled_status_index['entity'][0] == 1 and q == 'transparent':
            for choise_index in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){deployer_transparency_options[choise_index]}\n'
        # elif sampled_status_index['entity'][0] == 5 and q == 'scope': # authorized representative
        #     for choise_index in sampled_status_index[q]:
        #         question_option_buffer += f'\t\t({choise_index+1}){authorised_representative_scope_options[choise_index]}\n'
        elif sampled_status_index['entity'][0] == 3 and sampled_status_index['modification'] == [3] and q == 'scope': # importer; modification selects the forth option; for the question scope
            for choise_index in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){importor_scope_options[choise_index]}\n'
        elif sampled_status_index['entity'][0] == 2 and sampled_status_index['modification'] == [3] and q == 'scope': # distributor; modification selects the forth option; for the question scope
            for choise_index in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){distributor_scope_options[choise_index]}\n'
        elif sampled_status_index['entity'][0] == 4 and q == 'modification': # manufacturer's condition options
            # if option_dict[q][choise_index] == 'None of the above':
            #     question_option_buffer += f'\t\t(3) None of the above'
            # else: 
            #     index_list_ = random.sample([0,1], random.choice([1,2]))
            for i in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){product_manufacturer_condition_options[i]}\n'
        else:
            for choise_index in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){option_dict[q][choise_index]}\n'
            
        question_option_buffer += '\n'
    return question_option_buffer


def question_option_replay_statements(quesion_flow, sampled_status_index):
    '''
    sampled_status_index: index of status for all the options, stored in a dictionary. e.g. {'entity': [1,2], modification: [0,1]}
    '''
    question_option_buffer = ''
    for i, q in enumerate(quesion_flow):
        
        question_option_buffer += f'{question_dict_statements[q]}\n'
        # question_option_buffer += f'\tOption:\n'

        # if q =='scope':
        #     print(q)
        #     print(sampled_status_index['scope'])

        if sampled_status_index['entity'][0] == 1 and q == 'transparent':
            for choise_index in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){deployer_transparency_options[choise_index]}\n'
        # elif sampled_status_index['entity'][0] == 5 and q == 'scope': # authorized representative
        #     for choise_index in sampled_status_index[q]:
        #         question_option_buffer += f'\t\t({choise_index+1}){authorised_representative_scope_options[choise_index]}\n'
        elif sampled_status_index['entity'][0] == 3 and sampled_status_index['modification'] == [3] and q == 'scope': # importer; modification selects the forth option; for the question scope
            for choise_index in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){importor_scope_options[choise_index]}\n'
        elif sampled_status_index['entity'][0] == 2 and sampled_status_index['modification'] == [3] and q == 'scope': # distributor; modification selects the forth option; for the question scope
            for choise_index in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){distributor_scope_options[choise_index]}\n'
        elif sampled_status_index['entity'][0] == 4 and q == 'modification': # manufacturer's condition options
            # if option_dict[q][choise_index] == 'None of the above':
            #     question_option_buffer += f'\t\t(3) None of the above'
            # else: 
            #     index_list_ = random.sample([0,1], random.choice([1,2]))
            for i in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){product_manufacturer_condition_options[i]}\n'
        else:
            for choise_index in sampled_status_index[q]:
                question_option_buffer += f'\t\t({choise_index+1}){option_dict[q][choise_index]}\n'
            
        question_option_buffer += '\n'
    return question_option_buffer
