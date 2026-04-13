from utils import load_law_tree



GDPR_TREE = load_law_tree('GDPR')



class PromptTemplate:
    def __init__(self, law_tree=GDPR_TREE):
        self.law_tree = law_tree

        self.prepare_prompt_scope()
        self.prepare_prompt_special()
        self.prepare_prompt_subject()
        self.prepare_prompt_processor()
        self.prepare_prompt_lawful()
        self.prepare_prompt_principal()

    def prepare_prompt_scope(self):
        """
        Prepare the prompt based on the scope of GDPR .
        """
        instruction = """
You are an expert in the General Data Protection Regulation (GDPR). Your task is to analyze the provided context and answer the question to determine if it falls under the scope of GDPR. Your output should be in JSON format with the following key:
     - "is_gdpr_applicable": "yes" or "no"
        
**Context:**
{context}"""


        reference = """**GDPR Reference:**
1. This Regulation applies to the processing of personal data in the context of the activities of an establishment of a controller or a processor in the Union, regardless of whether the processing takes place in the Union or not.
2. This Regulation applies to the processing of personal data of data subjects who are in the Union by a controller or processor not established in the Union, where the processing activities are related to:
the offering of goods or services, irrespective of whether a payment of the data subject is required, to such data subjects in the Union; or the monitoring of their behaviour as far as their behaviour takes place within the Union.
3. This Regulation applies to the processing of personal data by a controller not established in the Union, but in a place where Member State law applies by virtue of public international law.
Suitable Recitals.

This Regulation does not apply to the processing of personal data:
- in the course of an activity which falls outside the scope of Union law;
- by the Member States when carrying out activities which fall within the scope of Chapter 2 of Title V of the TEU;
- by a natural person in the course of a purely personal or household activity;
- by competent authorities for the purposes of the prevention, investigation, detection or prosecution of criminal offences or the execution of criminal penalties, including the safeguarding against and the prevention of threats to public security."""


        question = "**Question:**" + "\n" + "Does the provided context fall under the scope of GDPR?"

        pure_question = instruction + '\n' + question
        question_with_reference = instruction + '\n' + reference + '\n' + question
        
        self.scope_prompt = question_with_reference
        self.scope_pure_prompt = pure_question


    def prepare_prompt_special(self):
        """
        Prepare the prompt based on the special conditions of GDPR.
        """
        instruction = """
You are an expert in the General Data Protection Regulation (GDPR). Your task is to analyze the provided context and answer the question to determine if it falls under the atricles of special conditions. If the context is not relevant or not applicable to the referred article, please answer "no". If the context is relevant and cannot be determined for the given special conditions, please answer with "not sure" for this article.

**Context:**
{context}"""

        reference = """**GDPR Articles for Special Conditions:**
- Article 8: Conditions applicable to child's consent
- Article 9: Processing of special categories of personal data about racial or ethnic origin, political opinions, religious or philosophical beliefs, or trade union membership, genetic data, biometric data, health data, sex life or sexual orientation.
- Article 10: Processing of personal data relating to criminal convictions and offences.
- Article 11: Processing of personal data do not or do no longer require the identification of a data subject.
- Article 44: Transfers of personal data to third countries or international organisations.
- Article 86: Processing and public access to official documents.
- Article 87: Processing of the national identification number.
- Article 88: Processing in the context of employment.
- Article 89: Safeguards and derogations relating to processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes
"""

        question = """
**Question:** 
Does the provided context fall under the special conditions of GDPR? If yes, please answer with the corresponding articile under the following output format.

**Output Format:**
Output format should be in JSON format:
{{
    "Article 8": "yes" or "no" or "not sure",
    "Article 9": "yes" or "no" or "not sure",
    "Article 10": "yes" or "no" or "not sure",
    "Article 11": "yes" or "no" or "not sure",
    "Article 44": "yes" or "no" or "not sure",
    "Article 86": "yes" or "no" or "not sure",
    "Article 87": "yes" or "no" or "not sure",
    "Article 88": "yes" or "no" or "not sure"
}} 
"""
        prompt = instruction + '\n' + reference + '\n' + question
        self.special_prompt = prompt

    def prepare_prompt_subject(self):
        """
        Prepare the prompt based on the subject rights of GDPR.
        """

        instruction = """You are an expert in the General Data Protection Regulation (GDPR). Your task is to analyze the provided context and answer the question to determine if it involves the subject rights of GDPR. If the subject right is not applicable or irrelevant, please answer with "no" for the given article. If the subject right is relevant but does not specify in the context, please answer with "not sure" for the given article.
**Context:**
{context}"""

        reference = """**GDPR Articles for Subject Rights:**
- Article 13: Information to be provided where personal data are collected from the data subject.
- Article 14: Information to be provided where personal data have not been obtained from the data subject.
- Article 15: Right of access by the data subject.
- Article 16: Right to rectification.
- Article 17: Right to erasure ('right to be forgotten').
- Article 18: Right to restriction of processing.
- Article 20: Right to data portability.
- Article 21: Right to object.
- Article 22: Automated individual decision-making, including profiling."""

        question = """
**Question:**
Does the provided context fall under the subject rights of GDPR? If yes, please answer with the corresponding article under the following output format.

**Output Format:**
Output format should be in JSON format:
{{
    "Article 13": "yes" or "no" or "not sure",
    "Article 14": "yes" or "no" or "not sure",
    "Article 15": "yes" or "no" or "not sure",
    "Article 16": "yes" or "no" or "not sure",
    "Article 17": "yes" or "no" or "not sure",
    "Article 18": "yes" or "no" or "not sure",
    "Article 20": "yes" or "no" or "not sure",
    "Article 21": "yes" or "no" or "not sure",
    "Article 22": "yes" or "no" or "not sure"
}} 
"""
        prompt = instruction + '\n' + reference + '\n' + question
        self.subject_prompt = prompt

    def prepare_prompt_processor(self):
        """
        Adherence to approved codes of conduct as referred to in Article 40 or approved certification mechanisms as referred to in Article 42 may be used as an element by which to demonstrate compliance with the obligations of the controller.
        """

        instruction = """You are an expert in the General Data Protection Regulation (GDPR). Your task is to analyze the provided context and answer the question to determine if the context satisfies the processor/controller obligations of GDPR. If the context does not mention any obligations, please answer with "not sure" for all articles.
**Context:**
{context}"""

        reference = """**GDPR Articles for Processor/Controller Obligations:**
- Article 40: Codes of conduct
- Article 42: Certification"""

        question = """
**Question:**
Does the provided context satisfy the processor/controller obligations of GDPR? Please answer with the corresponding article under the following output format.

**Output Format:**
Output format should be in JSON format:
{{
    "Article 40": "yes" or "no" or "not sure",
    "Article 42": "yes" or "no" or "not sure"
}} 
"""
        prompt = instruction + '\n' + reference + '\n' + question
        self.processor_prompt = prompt

    def prepare_prompt_lawful(self):        
        """
        Prepare the prompt based on the lawful basis of GDPR.
        """

        instruction = """You are an expert in the General Data Protection Regulation (GDPR). Your task is to analyze the provided context and answer the question to determine if it falls under the lawful basis of GDPR. If the lawful basis cannot be inferred from context, please answer with "not sure".
**Context:**
{context}"""

        reference = """**GDPR Articles for Lawful Basis:**
-  : Lawfulness of processing
- Article 6(1)(a): the data subject has given consent to the processing of his or her personal data for one or more specific purposes;
- Article 6(1)(b): processing is necessary for the performance of a contract to which the data subject is party or in order to take steps at the request of the data subject prior to entering into a contract;
- Article 6(1)(c): processing is necessary for compliance with a legal obligation to which the controller is subject;
- Article 6(1)(d): processing is necessary in order to protect the vital interests of the data subject or of another natural person;
- Article 6(1)(e): processing is necessary for the performance of a task carried out in the public interest or in the exercise of official authority vested in the controller;
- Article 6(1)(f): processing is necessary for the purposes of the legitimate interests pursued by the controller or by a third party, except where such interests are overridden by the interests or fundamental rights and freedoms of the data subject which require protection of personal data, in particular where the data subject is a child.
"""

        question = """
**Question:**
Does the provided context satisfy lawful basis of GDPR? If yes, please answer with the corresponding article under the following output format.

**Output Format:**
Output format should be in JSON format:
{{
    "Article 6(1)(a)": "yes" or "no" or "not sure",
    "Article 6(1)(b)": "yes" or "no" or "not sure",
    "Article 6(1)(c)": "yes" or "no" or "not sure",
    "Article 6(1)(d)": "yes" or "no" or "not sure",
    "Article 6(1)(e)": "yes" or "no" or "not sure",
    "Article 6(1)(f)": "yes" or "no" or "not sure"
}} 
"""
        prompt = instruction + '\n' + reference + '\n' + question
        self.lawful_prompt = prompt

    def prepare_prompt_principal(self):
        """
        Prepare the prompt based on the principal of GDPR.
        """

        instruction = """You are an expert in the General Data Protection Regulation (GDPR). Your task is to analyze the provided context and answer the question to determine if it follows the general principal of GDPR. If the principal cannot be inferred from context, please answer with "not sure". If the context is against the principal, please answer with "no" for the given article.
**Context:**
{context}"""
        reference = """**GDPR Articles for General Principal:**
- Article 5(1)(b): Personal data shall be collected for specified, explicit and legitimate purposes and not further processed in a manner that is incompatible with those purposes; further processing for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes shall, in accordance with Article 89(1), not be considered to be incompatible with the initial purposes.
- Article 5(1)(c): Personal data shall be adequate, relevant and limited to what is necessary in relation to the purposes for which they are processed;
- Article 5(1)(d): Personal data shall be accurate and, where necessary, kept up to date; every reasonable step must be taken to ensure that personal data that are inaccurate, having regard to the purposes for which they are processed, are erased or rectified without delay;
- Article 5(1)(e): kept in a form which permits identification of data subjects for no longer than is necessary for the purposes for which the personal data are processed; personal data may be stored for longer periods insofar as the personal data will be processed solely for archiving purposes in the public interest, scientific or historical research purposes or statistical purposes in accordance with Article 89(1) subject to implementation of the appropriate technical and organisational measures required by this Regulation in order to safeguard the rights and freedoms of the data subject;
- Article 5(1)(f): processed in a manner that ensures appropriate security of the personal data, including protection against unauthorised or unlawful processing and against accidental loss, destruction or damage, using appropriate technical or organisational measures.
"""

        question = """
**Question:**
Does the provided context follows the general principal of GDPR? Please answer with the corresponding article under the following output format.

**Output Format:**
Output format should be in JSON format:
{{
    "Article 5(1)(b)": "yes" or "no" or "not sure",
    "Article 5(1)(c)": "yes" or "no" or "not sure",
    "Article 5(1)(d)": "yes" or "no" or "not sure",
    "Article 5(1)(e)": "yes" or "no" or "not sure",
    "Article 5(1)(f)": "yes" or "no" or "not sure"
}} 
"""
        prompt = instruction + '\n\n' + reference + '\n\n' + question
        self.principal_prompt = prompt