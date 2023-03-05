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
  "-b 23.03.03 https://github.com/NUROISEA/stable-diffusion-webui-images-browser",
  "-b 23.03.01 https://github.com/NUROISEA/a1111-sd-webui-tagcomplete",
  "-b 23.02.20 https://github.com/NUROISEA/sd-webui-ar",
  "-b 23.02.19 https://github.com/NUROISEA/stable-diffusion-webui-two-shot",
  "-b v1.6-stable https://github.com/NUROISEA/sd-webui-tunnels",
  "-b ariasubnewcivit https://github.com/etherealxx/batchlinks-webui",
]

default_embeddings = [
  "https://huggingface.co/nick-x-hacker/bad-artist/resolve/main/bad-artist.pt",
  "https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt",
  "https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors",
]

default_configs = [
  "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/ui-config.json",
  "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/config.json",
  "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/styles.csv",
]

xformers_link = "https://github.com/camenduru/stable-diffusion-webui-colab/releases/download/0.0.16/xformers-0.0.16+814314d.d20230118-cp38-cp38-linux_x86_64.whl"

webui_branch = "23.02.04"

default_arguments = " ".join([
  "--xformers",
  "--lowram",
  "--no-hashing",
  "--enable-insecure-extension-access",
  "--no-half-vae",
  "--disable-safe-unpickle",
  "--opt-channelslast",
  "--gradio-queue",
])

def arguments(model="", vae="", tunnel="gradio", ng_token="", ng_region="auto", extra_args=""):
  args = [
    default_arguments,
    f"--ckpt {model}" if model else "",
    f"--vae-path {vae}" if vae else "",
    extra_args if extra_args else "",
  ]

  if tunnel == "gradio":
    args.append("--share")
  elif tunnel == "ngrok":
    args.append(f"--ngrok {ng_token}")
    if ng_region != "auto":
      args.append(f"--ngrok-region {ng_region}")
  else:
    args.append(f"--{tunnel}")
  
  args_clean = list(filter(None, map(str.strip, args))) # thanks, chatgpt!
  return args_clean

def _fetch_patch_list():
  import requests
  url = "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/patch_list.txt"
  response = requests.get(url)
  data = response.text
  return data.splitlines()

patch_list = _fetch_patch_list()

mounted_gdrive = False

def output_to_gdrive(on_drive=False, drive_folder="AI/Generated"):
  global mounted_gdrive

  if not mounted_gdrive and on_drive:
    from google.colab import drive
    drive.mount('/content/drive')
    mounted_gdrive = True

  drive_ouput_path = f"/content/drive/MyDrive/{drive_folder}/"
  
  config_path = "/content/stable-diffusion-webui/config.json"
  
  save_path = drive_ouput_path if on_drive else ""

  config_dictionary = {
    "outdir_txt2img_samples": f"{save_path}outputs/txt2img-images",
    "outdir_img2img_samples": f"{save_path}outputs/img2img-images",
    "outdir_extras_samples": f"{save_path}outputs/extras-images",
    "outdir_txt2img_grids": f"{save_path}outputs/txt2img-grids",
    "outdir_img2img_grids": f"{save_path}outputs/img2img-grids",
    "outdir_save": f"{save_path}outputs/saved",
  }

  dictionary_to_json(config_path, config_dictionary)

  print("\nGenerations will be saved to Google Drive.\nThis will make the saving cell pointless (for now).\n" if on_drive else "")

installed_aria2 = False

# copy pasted code, will update all notebooks later
web_ui_folder = "/content/stable-diffusion-webui"
models_folder = f"{web_ui_folder}/models/Stable-diffusion"
vae_folder = f"{web_ui_folder}/models/VAE"
embeddings_folder = f"{web_ui_folder}/embeddings"
extensions_folder = f"{web_ui_folder}/extensions"

def aria2_download(link, folder, file_name):
  global installed_aria2
  commands = []
  aria2_flags = "--summary-interval=10 --console-log-level=error -c -x 16 -s 16 -k 1M"
  
  if not installed_aria2:
    commands += [
      'echo "\nInstalling aria2...\n"',
      'apt -y install -qq aria2'
    ]
    installed_aria2 = True

  commands += [ f'aria2c {aria2_flags} {link} -d {folder} -o {file_name}' ]
  return " && ".join(commands)

# abstracting downloaders so the notebook code will be a lot cleaner
# just plonk the function and the link
# more will get added
def download_model(link):
  global models_folder
  file_name = link.split('/')[-1]
  print(f"Downloading {file_name}...")
  return aria2_download(link, models_folder, file_name)

def download_vae(link):
  global vae_folder
  file_name = link.split('/')[-1]
  print(f"Downloading {file_name}...")
  return aria2_download(link, vae_folder, file_name)