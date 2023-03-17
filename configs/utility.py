import json
import subprocess

def dictionary_to_json(json_file, data_dictionary):
  with open(json_file, 'r') as f:
    json_data = json.load(f)
  
  json_data.update(data_dictionary)

  with open(json_file, 'w') as f:
    json.dump(json_data, f)

def log_usage(key, ouput_info=False):
  if key not in logged_keys:
    namespace = "nuroisea-anime-webui-colab"
    output = subprocess.check_output(["curl", f"https://api.countapi.xyz/hit/{namespace}/{key}"])
    # result = json.loads(output)
    # value = result["value"]
    logged_keys.append(key)

logged_keys = []

has_run = False
mounted_gdrive = False
installed_aria2 = False

xformers_link = "pip install -q --pre xformers && pip install -q --pre triton"
webui_branch = "23.03.14"

# copy pasted code, will update all notebooks later
web_ui_folder = "/content/stable-diffusion-webui"
models_folder = f"{web_ui_folder}/models/Stable-diffusion"
vae_folder = f"{web_ui_folder}/models/VAE"
embeddings_folder = f"{web_ui_folder}/embeddings"
extensions_folder = f"{web_ui_folder}/extensions"

models_downloaded = []

default_extensions = [
  "-b 23.03.01 https://github.com/anime-webui-colab/a1111-sd-webui-tagcomplete",
  "-b 23.03.08 https://github.com/anime-webui-colab/batchlinks-webui",
  "-b 23.03.15 https://github.com/anime-webui-colab/deforum-for-automatic1111-webui",
  "-b 23.02.20 https://github.com/anime-webui-colab/sd-webui-ar",
  "-b 23.03.14 https://github.com/anime-webui-colab/sd-webui-controlnet",
  "-b 23.02.27 https://github.com/anime-webui-colab/sd-webui-tunnels",
  "-b 23.03.03 https://github.com/anime-webui-colab/stable-diffusion-webui-images-browser",
  "-b 23.02.19 https://github.com/anime-webui-colab/stable-diffusion-webui-two-shot",
]

default_embeddings = [
  "https://huggingface.co/nick-x-hacker/bad-artist/resolve/main/bad-artist.pt",
  "https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt",
  "https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors",
]

default_configs = [
  "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/config.json",
  "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/ui-config.json",
  "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/styles.csv",
]

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
    f"--ckpt \"{model}\"" if model else "",
    f"--vae-path \"{vae}\"" if vae else "",
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

  log_usage(f"tunnel-{tunnel}")
  
  args_clean = list(filter(None, map(str.strip, args))) # thanks, chatgpt!
  return args_clean

def _fetch_patch_list():
  import requests
  url = "https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/patch_list.txt"
  response = requests.get(url)
  data = response.text
  return data.splitlines()

patch_list = _fetch_patch_list()

def output_to_gdrive(on_drive=False, drive_folder="AI/Generated"):
  global mounted_gdrive

  if not mounted_gdrive and on_drive:
    from google.colab import drive
    print('🏇 Mounting to Google Drive...')
    print('👋 Please allow the notebook to connect 😁')
    drive.mount('/content/drive')
    mounted_gdrive = True
    log_usage("gdrive-output")

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

  print("\n💾 Generations will be saved to Google Drive. \n😢 This will make the saving cell pointless (for now).\n" if on_drive else "")

def aria2_download(link, folder, file_name, force_redownload=False):
  global installed_aria2, models_downloaded

  if link in models_downloaded and not force_redownload:
    return f'echo "{file_name} already downloaded. Skipping..."'

  commands = []
  aria2_flags = "--summary-interval=5 --console-log-level=error -c -x 16 -s 16 -k 1M"
  
  if not installed_aria2:
    print("🚀 Installing aria2...")
    commands += [
      'apt -y install -qq aria2 &> /dev/null', #because that wall of text is disgusting 
    ]
    installed_aria2 = True

  print(f"⏬ Downloading {file_name} to {folder}...")
  print("⌚ Download status will be printed every 5 seconds.")
  commands += [
    f'aria2c {aria2_flags} "{link}" -d "{folder}" -o "{file_name}"' 
  ]

  models_downloaded += [ link ]

  return " && ".join(commands)

# abstracting downloaders so the notebook code will be a lot cleaner
# just plonk the function and the link
# more will get added
def download_model(link, force_redownload=False):
  global models_folder
  file_name = link.split('/')[-1]
  return aria2_download(link, models_folder, file_name, force_redownload)

def download_vae(link, force_redownload=False):
  global vae_folder
  file_name = link.split('/')[-1]
  return aria2_download(link, vae_folder, file_name, force_redownload)