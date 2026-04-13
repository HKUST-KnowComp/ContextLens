#model="Qwen/Qwen2.5-7B-Instruct"
api_name="openai"
api_model="gpt-4o-mini"
model=$api_model

# python case_analyze.py \
#     --api_model $api_model \
#     --api_name $api_name \
#     --temperature 0.0


python case_parser.py \
    --model $model 