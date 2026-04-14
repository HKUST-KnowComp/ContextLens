<div align="center">

<h1>ContextLens: Modeling Imperfect Privacy and Safety Context for Legal Compliance</h1>

<p>
  <a href="https://teapotliid.github.io/">Haoran Li</a><sup>1</sup>, 
  <a href="https://egbertjing.github.io/">Huihao Jing</a><sup>1</sup>, 
  <a href="https://whuak.github.io/">Wenbin Hu</a><sup>1</sup>, 
  Tsz Ho Li<sup>1</sup>, 
  Chanhou Lou<sup>1</sup>, 
  Hong Ting Tsang<sup>1</sup>, 
  Sirui Han<sup>1</sup>, 
  <a href="https://www.math.hkust.edu.hk/people/faculty/profile/yqsong/">Yangqiu Song<sup>1</sup>, 
</p>


<p>
<sup>1</sup>Hong Kong University of Science and Technology  
</p>

</div>


## Abstract

Individuals' concerns about data privacy and AI safety are highly contextualized and extend beyond sensitive patterns. Addressing these issues requires reasoning about the context to identify and mitigate potential risks. Though researchers have widely explored using large language models (LLMs) as evaluators for contextualized safety and privacy assessments, these efforts typically assume the availability of complete and clear context, whereas real-world contexts tend to be ambiguous and incomplete. In this paper, we propose ContextLens, a semi-rule-based framework that leverages LLMs to ground the input context in the legal domain and explicitly identify both known and unknown factors for legal compliance. Instead of directly assessing safety outcomes, our ContextLens instructs LLMs to answer a set of crafted questions that span over applicability, general principles and detailed provisions to assess compliance with pre-defined priorities and rules. We conduct extensive experiments on existing compliance benchmarks that cover the General Data Protection Regulation (GDPR) and the EU AI Act. The results suggest that our ContextLens can significantly improve LLMs' compliance assessment and surpass existing baselines without any training. Additionally, our ContextLens can further identify the ambiguous and missing factors.

<img width="1405" height="607" alt="ss 2026-04-14 135946" src="https://github.com/user-attachments/assets/3e1bb84b-fe78-4df2-9c36-f280d660fb06" />


## Quick Start: We provide the annotated chunking for the EU AI Act and GDPR.

```
cd rule_based_checklist/EU_AI_ACT/
./run_oai.sh
```

### EU AI ACT
Example scripts can be found at:
```
cd rule_based_checklist/EU_AI_ACT/
./run_oai.sh
```

### GDPR

Example scripts can be found at:
```
cd rule_based_checklist/GDPR/
./run_qwen.sh
```

## Citation
Please kindly cite the following paper if you found our method and resources helpful!

## Miscellaneous
Please send any questions about the code and/or the method to hlibt@connect.ust.hk.
<div align="center">
