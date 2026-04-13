#api_model="o3-mini"
#log_path="logs/o3-mini/log.log"


#api_model="gpt-4o"  deepseek-r1  gemini-2.5-flash-all  o3-mini 
api_name="deepseek"
api_model="deepseek-r1"
python get_response.py \
    --api_model $api_model \
    --api_name $api_name \
    --temperature 0.0