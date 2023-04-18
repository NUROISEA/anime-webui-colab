import json
import os
import subprocess
from datetime import datetime,timezone

logged_keys = []
webui_branch = '23.03.14'

has_run = False
mounted_gdrive = False
installed_aria2 = False

pip_commands = [
  'pip install -q xformers==0.0.17',
  'pip install -q triton==2.0.0',
]
xformers_link = ' && '.join(pip_commands)

# copy pasted code, will update all notebooks later
web_ui_folder = '/content/stable-diffusion-webui'
models_folder = f'{web_ui_folder}/models/Stable-diffusion'
vae_folder = f'{web_ui_folder}/models/VAE'
embeddings_folder = f'{web_ui_folder}/embeddings'
extensions_folder = f'{web_ui_folder}/extensions'

models_downloaded = []

def dictionary_to_json(json_file, data_dictionary):
  with open(json_file, 'r') as f:
    json_data = json.load(f)
  
  json_data.update(data_dictionary)

  with open(json_file, 'w') as f:
    json.dump(json_data, f)

def log_usage(key):
  if key not in logged_keys:
    now_utc = datetime.now(timezone.utc)

    namespace = 'nuroisea-anime-webui-colab'
    count_url = f'https://api.countapi.xyz/hit/{namespace}/{key}'

    monthly_prefix = now_utc.strftime('m%y%m')
    weekly_prefix = now_utc.strftime('w%y%V')

    total_log = subprocess.check_output(['curl', count_url])
    monthly_log = subprocess.check_output(['curl', f'{count_url}-{monthly_prefix}'])
    weekly_log = subprocess.check_output(['curl', f'{count_url}-{weekly_prefix}'])

    logged_keys.append(key)

def install_webui(option):
  global webui_branch, web_ui_folder

  version_dictionary = {
    'stable':     f'-b {webui_branch} https://github.com/anime-webui-colab/stable-diffusion-webui',
    'latest':      'https://github.com/AUTOMATIC1111/stable-diffusion-webui',
    'ui-redesign': 'https://github.com/anapnoe/stable-diffusion-webui-ux'
  }

  log_usage(f'webui-version-{option}')

  if option == 'ui-redesign':
    print("✨ You are now using anapnoe's fork of the web UI! Layouts are different!")
  
  print('🌟 Installing stable-diffusion-webui...')
  git_clone_command = f"git clone -q {version_dictionary[option]} {web_ui_folder}"
  return git_clone_command

def extensions_list(option):
  global extensions_folder

  # folder, just f to not clutter the strings
  f = extensions_folder

  extensions = {
    'none': [],
    'lite': [
      f'-b 23.03.30 https://github.com/anime-webui-colab/ext-batchlinks {f}/batchlinks',
      f'-b 23.03.28 https://github.com/anime-webui-colab/ext-images-browser {f}/images-browser',
      f'-b 23.03.31 https://github.com/anime-webui-colab/ext-state {f}/state',
      f'-b 23.04.06 https://github.com/anime-webui-colab/ext-stealth-pnginfo {f}/stealth-pnginfo',
      f'-b 23.04.05 https://github.com/anime-webui-colab/ext-tagcomplete {f}/tagcomplete',
      f'-b 23.02.27 https://github.com/anime-webui-colab/ext-tunnels {f}/tunnels',
    ],
    'stable': [
      # now i just realized that i didnt need to rename the repos themselves.... i hate my self
      f'-b 23.03.31 https://github.com/anime-webui-colab/ext-aspect-ratio-preset {f}/aspect-ratio-preset',
      f'-b 23.03.30 https://github.com/anime-webui-colab/ext-batchlinks {f}/batchlinks',
      f'-b 23.03.23 https://github.com/anime-webui-colab/ext-controlnet {f}/controlnet',
      f'-b 23.03.22 https://github.com/anime-webui-colab/ext-cutoff {f}/cutoff',
      f'-b 23.03.09 https://github.com/anime-webui-colab/ext-fast-pnginfo {f}/fast-pnginfo',
      f'-b 23.03.28 https://github.com/anime-webui-colab/ext-images-browser {f}/images-browser',
      f'-b 23.02.19 https://github.com/anime-webui-colab/ext-latent-couple-two-shot {f}/latent-couple-two-shot',
      f'-b 23.03.19 https://github.com/anime-webui-colab/ext-session-organizer {f}/session-organizer',
      f'-b 23.03.31 https://github.com/anime-webui-colab/ext-state {f}/state',
      f'-b 23.04.06 https://github.com/anime-webui-colab/ext-stealth-pnginfo {f}/stealth-pnginfo',
      f'-b 23.04.05 https://github.com/anime-webui-colab/ext-tagcomplete {f}/tagcomplete',
      f'-b 23.02.27 https://github.com/anime-webui-colab/ext-tunnels {f}/tunnels',
    ],
    'latest': [
      # using my own fork again to not lose my presets
      f'-b 23.03.31 https://github.com/anime-webui-colab/ext-aspect-ratio-preset {f}/aspect-ratio-preset',
      f'https://github.com/etherealxx/batchlinks-webui {f}/batchlinks',
      f'https://github.com/Mikubill/sd-webui-controlnet {f}/controlnet',
      f'https://github.com/hnmr293/sd-webui-cutoff {f}/cutoff',
      f'https://github.com/NoCrypt/sd-fast-pnginfo {f}/fast-png-info',
      f'https://github.com/AlUlkesh/stable-diffusion-webui-images-browser {f}/images-browser',
      f'https://github.com/opparco/stable-diffusion-webui-two-shot {f}/latent-couple-two-shot',
      f'https://github.com/space-nuko/sd-webui-session-organizer {f}/session-organizer',
      f'https://github.com/ilian6806/stable-diffusion-webui-state {f}/state',
      f'https://github.com/ashen-sensored/sd_webui_stealth_pnginfo {f}/stealth-pnginfo',
      f'https://github.com/DominikDoom/a1111-sd-webui-tagcomplete {f}/tagcomplete',
      # wait why? because the upstream is optimized for their colab, this is the one i refuse to update
      f'-b 23.02.27 https://github.com/anime-webui-colab/ext-tunnels {f}/tunnels',
    ],
    'experimental': [
      # this will change a lot, dont expect anything permanent here
      f'https://github.com/deforum-art/deforum-for-automatic1111-webui {f}/exp-deforum',
      f'https://github.com/adieyal/sd-dynamic-prompts {f}/exp-dynamic-prompts',
      f'https://github.com/ashen-sensored/stable-diffusion-webui-two-shot {f}/exp-latent-couple-two-shot-regions',
      f'https://github.com/muerrilla/stable-diffusion-NPW {f}/exp-negative-prompt-weight',
      f'https://github.com/hako-mikan/sd-webui-regional-prompter {f}/exp-regional-prompter',
    ],
  }

  if option == 'experimental':
    print('😲 You are now installing some extensions I deem experimental for this colab!')
    print('😮 Experimental extensions are prefixed with "exp"')
    return extensions['latest'] + extensions['experimental']
  else:
    if option == 'none':
      print('😶 No extensions would be installed. Pure vanilla web UI')
    elif option == 'lite':
      print('🙂 No "advanced" extensions would be installed. Only installing the bare minimum.')

    return extensions[option]

def embeddings_list():
  print('🛏 Fetching embeddings...')
  return [
    'https://huggingface.co/nick-x-hacker/bad-artist/resolve/main/bad-artist.pt',
    'https://huggingface.co/nick-x-hacker/bad-artist/resolve/main/bad-artist-anime.pt',
    'https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt',
    'https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors',
  ]

def configs_list():
  print('🔧 Fetching configs...')
  return [
    'https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/config.json',
    'https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/ui-config.json',
    'https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/styles.csv',
  ]

def patch_list():
  import requests
  url = 'https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/patch_list.txt'
  response = requests.get(url)
  data = response.text
  print('🩹 Applying colab patches...')
  return data.splitlines()

def arguments(model='', vae='', tunnel='gradio', ng_token='', ng_region='auto', extra_args='', default_override=''):
  default_arguments = ' '.join([
    '--xformers',
    '--lowram',
    '--no-hashing',
    '--enable-insecure-extension-access',
    '--no-half-vae',
    '--disable-safe-unpickle',
    '--opt-channelslast',
    '--gradio-queue',
  ])
  
  args = [
    default_arguments if not default_override else default_override,
    f'--ckpt \"{model}\"' if model else '',
    f'--vae-path \"{vae}\"' if vae else '',
    extra_args if extra_args else '',
  ]

  if tunnel == 'gradio':
    args.append('--share')
  elif tunnel == 'ngrok':
    args.append(f'--ngrok {ng_token}')
    if ng_region != 'auto':
      args.append(f'--ngrok-region {ng_region}')
  else:
    args.append(f'--{tunnel}')

  log_usage(f'tunnel-{tunnel}')
  
  args_clean = list(filter(None, map(str.strip, args))) # thanks, chatgpt!
  return args_clean

def mount_drive(on_drive=False):
  global mounted_gdrive
  if not mounted_gdrive and on_drive:
    from google.colab import drive
    print('📂 Connecting to Google Drive...')
    drive.mount('/content/drive')
    mounted_gdrive = True

def output_to_gdrive(on_drive=False, drive_folder='AI/Generated'):
  drive_ouput_path = f'/content/drive/MyDrive/{drive_folder}/'
  
  config_path = '/content/stable-diffusion-webui/config.json'
  
  save_path = drive_ouput_path if on_drive else ''

  config_dictionary = {
    'outdir_txt2img_samples': f'{save_path}outputs/txt2img-images',
    'outdir_img2img_samples': f'{save_path}outputs/img2img-images',
    'outdir_extras_samples': f'{save_path}outputs/extras-images',
    'outdir_txt2img_grids': f'{save_path}outputs/txt2img-grids',
    'outdir_img2img_grids': f'{save_path}outputs/img2img-grids',
    'outdir_save': f'{save_path}outputs/saved',
  }

  dictionary_to_json(config_path, config_dictionary)

  if on_drive:
    log_usage('gdrive-output')
    print('💾 Generations will be saved to Google Drive.')
    print('😢 This will make the saving cell pointless (for now).')

def aria2_download(link, folder, file_name, force_redownload=False):
  global installed_aria2, models_downloaded

  if link in models_downloaded and not force_redownload:
    return f'echo "{file_name} already downloaded. Skipping..."'

  commands = []
  aria2_flags = '--quiet --console-log-level=error -c -x 16 -s 16 -k 1M'
  
  if not installed_aria2:
    print('🚀 Installing aria2...')
    commands += [
      'apt -y install -qq aria2 &> /dev/null', #because that wall of text is disgusting 
    ]
    installed_aria2 = True

  print(f'⏬ Downloading {file_name} to {folder}...')
  #print('⌚ Download status will be printed every 5 seconds.')
  commands += [
    f'aria2c {aria2_flags} "{link}" -d "{folder}" -o "{file_name}"'
  ]

  models_downloaded += [ link ]

  return ' && '.join(commands)

def download_model(link, yaml_link=''):
  # TODO: this function isn't elegant :/
  global models_folder, models_downloaded
  file_name = link.split('/')[-1]  
  commands = []

  if yaml_link not in models_downloaded and yaml_link != '':
    commands += [ f'wget -q "{yaml_link}" -P "{models_folder}/"' ]
    models_downloaded += [ yaml_link ]
  
  # i am cringing at this
  commands += [
    aria2_download(link, models_folder, file_name)
  ]

  return ' && '.join(commands)

def download_vae(link):
  if link == '':
    return 'echo "Continuing without VAE..."'

  global vae_folder
  file_name = link.split('/')[-1]
  return aria2_download(link, vae_folder, file_name)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print('👍 Utility script imported.')