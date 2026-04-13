#api_model="o3-mini"
#log_path="logs/o3-mini/log.log"


#api_model="gpt-4o"
api_name="hf"
model="Qwen/Qwen2.5-7B-Instruct"
python get_response.py \
    --api_name $api_name \
    --model $model \
    --temperature 0.0