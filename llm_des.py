import openai
import sys 
sys.path.append('../')
import json
from tqdm import tqdm
import argparse
import os
import torch
import torch.nn as nn
from clip import clip

def dump_into_json(descriptions, json_file):
    f = open(json_file, 'w')
    json.dump(descriptions, f, indent=4)
    f.close()
    print(f'Write the format llm descriptions into {json_file}.')

def analyze_tags(tag, openai_client=None):
    # Generate LLM tag descriptions

    llm_prompts = [ f"Describe concisely what a(n) {tag} looks like:", \
                    f"How can you identify a(n) {tag} concisely?", \
                    f"What does a(n) {tag} look like concisely?",\
                    f"What are the identifying characteristics of a(n) {tag}:", \
                    f"Please provide a concise description of the visual characteristics of {tag}:"]

    results = {}
    result_lines = []

    result_lines.append(f"a photo of a {tag}.")

    for llm_prompt in tqdm(llm_prompts):

        # send message
        response = openai_client.chat.completions.create(
            messages=[{"role": "user", "content": llm_prompt,}],
                model="gpt-3.5-turbo",
                max_tokens=77,
                temperature=0.99,
                n=10,
                stop=None
        )
        # parse the response
        for item in response.choices:
            result_lines.append(item.message.content.strip())
    results[tag] = result_lines
    return results


if __name__ == "__main__":
    openai_api_key = 'sk-7UgTwwOP3IgAcN6YrUZA5i1gEFupUQfC0JgF55HblrlbN97p'
    # set OpenAI API key
    openai_client = openai.OpenAI(
        # This is the default and can be omitted
        api_key=openai_api_key,
        base_url="https://api.chatanywhere.tech/v1"
    )
    # get class names from file
    categories = ['unknown']
    llm_tag_des_file = '/mnt/irdc_rd/songfaxing/code/ram/custom_dataset/red_sea_crawler/llm-tag-descriptions/unknown_llm_descripions.json'
    tag_descriptions = []
    for tag in categories:
        result = analyze_tags(tag, openai_client)
        tag_descriptions.append(result)
    dump_into_json(tag_descriptions, llm_tag_des_file)
    

"""
Go into SenseCore Container to run this scripts.
OPENAI_KEY: sk-proj-CT9Ey8Z7pHtLr5UXXesIT3BlbkFJWmIAX0IPiD7TOLgEK9yh

# free api key from : https://github.com/chatanywhere/GPT_API_free?tab=readme-ov-file
# we should replace base url with base_url="https://api.chatanywhere.tech/v1"
# openai_key = 'sk-7UgTwwOP3IgAcN6YrUZA5i1gEFupUQfC0JgF55HblrlbN97p'
# sk-7UgTwwOP3IgAcN6YrUZA5i1gEFupUQfC0JgF55HblrlbN97p
python generate_info_for_custom_dataset.py \
    --openai_api_key sk-7UgTwwOP3IgAcN6YrUZA5i1gEFupUQfC0JgF55HblrlbN97p \
    --llm_tag_des /mnt/irdc_rd/songfaxing/code/ram/llm-tag-descriptions/custom/shark-species_llm_tag_descriptions.json \
    --class_names_file /mnt/irdc_rd/songfaxing/Data/RedSea/red_sea_json/shark-species.txt \
    --output_tensor_path ../../model/frozen_tag_embedding/shark-species-embedding_class_14_des_51.pth \
    --output_taglist_path ../datasets/custom/shark-species/shark-species_ram_taglist.txt
"""
