import json

def dictionary_to_json(json_file, data_dictionary):
    with open(json_file, 'r') as f:
        json_data = json.load(f)
    
    json_data.update(data_dictionary)

    with open(json_file, 'w') as f:
        json.dump(json_data, f)

has_run = False

models_downloaded = []

default_extensions = [
    "-b 22.12.10 https://github.com/NUROISEA/stable-diffusion-webui-images-browser",
    "-b 23.01.14 https://github.com/NUROISEA/a1111-sd-webui-tagcomplete",
]

default_embeddings = [
    "https://huggingface.co/nick-x-hacker/bad-artist/resolve/main/bad-artist.pt",
    "https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt",
]

default_configs = [
    "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/ui-config.json",
    "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/config.json",
    "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/styles.csv",
]

xformers_link = "https://github.com/camenduru/stable-diffusion-webui-colab/releases/download/0.0.15/xformers-0.0.15.dev0+189828c.d20221207-cp38-cp38-linux_x86_64.whl"

webui_branch = "23.02.01"
