import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


### for mistral
HF_TOKEN = "INPUT_YOUR_HF_TOKEN"
HF_HOME = "INPUT_YOUR_HF_HOME"
api_model ='INPUT_YOUR_API_MODEL'
local_case_dir = 'INPUT_YOUR_LOCAL_CASE_DIR'

### paths for HF format datasets
# HF_cases_path = os.path.join(BASE_DIR, 'HF_cache', 'cases')
# HF_KBs_path = os.path.join(BASE_DIR, 'HF_cache', 'KBs')
# HF_MCQ_path = os.path.join(BASE_DIR, 'HF_cache', 'MCQ')