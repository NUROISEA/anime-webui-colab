#@title `script.py`

import json
import os
import subprocess
import shlex
from datetime import datetime,timezone

logged_keys = []
models_downloaded = []

has_run = False
mounted_gdrive = False
installed_aria2 = False
controlnet_installed = False
disabled_logging = False

chosen_webui_version = 'stable'
chosen_extension_version = 'stable'

web_ui_folder = '/content/stable-diffusion-webui'
models_folder = f'{web_ui_folder}/models/Stable-diffusion'
vae_folder = f'{web_ui_folder}/models/VAE'
embeddings_folder = f'{web_ui_folder}/embeddings'
extensions_folder = f'{web_ui_folder}/extensions'
controlnet_folder = f'{extensions_folder}/controlnet'
controlnet_models_folder = f'{controlnet_folder}/models'

# variables for PYOM and UWUColab
model_download_folder = '/content/models'
vae_download_folder = '/content/VAE'

def dictionary_to_json(json_file, data_dictionary):
  with open(json_file, 'r') as f:
    json_data = json.load(f)
  
  json_data.update(data_dictionary)

  with open(json_file, 'w') as f:
    json.dump(json_data, f)

def run_shell(command):
  shlex_command = shlex.split(command)
  _ = subprocess.run(shlex_command)

def log_usage(key):
  global disabled_logging, logged_keys

  if disabled_logging:
    return

  if key in logged_keys:
    return

  namespace = 'NUROISEA/anime-webui-colab'
  count_url = f'https://api.visitorbadge.io/api/visitors?path={namespace}/{key}'
  user_agent = 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0'

  try:
    run_shell(f'curl {count_url} -H {user_agent}')
  except:
    print('😖 visitorbadge.io seems to be having an issue, disabled usage counting for now...')
    disabled_logging = True

  logged_keys.append(key)

def colab_memory_fix():
  commands = [
    'echo "🚨 If you are seeing this, this colab would not run!"',
    'echo "🚨 Please delete the following lines in the code of the notebook:"',
    'echo "ℹ Refer to the following image:"',
    'echo "🖼 https://github.com/NUROISEA/anime-webui-colab/assets/120075289/2fdc20ed-7e75-42b8-9848-b1ab34775fbd"',
    'echo "🚨 Or grab the latest version of the notebooks here:"',
    'echo "🌐 https://github.com/NUROISEA/anime-webui-colab"',
  ]

  return commands

def install_webui(option):
  global web_ui_folder, chosen_webui_version

  chosen_webui_version = option

  version_dictionary = {
    'fallback':   f'-b 23.03.14 https://github.com/anime-webui-colab/stable-diffusion-webui',
    'stable':     f'-b v1.4.0 https://github.com/anime-webui-colab/stable-diffusion-webui',
    'latest':      'https://github.com/AUTOMATIC1111/stable-diffusion-webui',
    'latest-dev':  '-b dev https://github.com/AUTOMATIC1111/stable-diffusion-webui',
    'ui-redesign': 'https://github.com/anapnoe/stable-diffusion-webui-ux',
  }

  log_usage(f'webui-version-{option}')

  if option == 'ui-redesign':
    print("✨ You are now using anapnoe's fork of the web UI! Layouts are different!")
  elif option == 'latest-dev':
    print('🧪 This is the cutting-edge version of the web UI! Stuff might not work!')
  elif option == 'latest':
    print('🔼 Selected the latest version of the web UI.')
  elif option == 'stable':
    print('🔔 Selected an old version of the web UI. Version released on 23.06.27. (v1.4.0)')
    print('🔔 Please consider using the latest version, unless you really need this specific version.')
  elif option == 'fallback':
    print('🔔 Selected the fallback version of the web UI. Version released on 23.03.14.')
    print('🔔 Extensions will follow suit.')
  
  print(f'🌟 Installing stable-diffusion-webui ({option})...')
  git_clone_command = f'git clone -q {version_dictionary[option]} {web_ui_folder}'
  return git_clone_command

def extensions_list(option,webui_version='stable',controlnet='none', only_controlnet=False):
  global extensions_folder, controlnet_installed, chosen_extension_version

  chosen_extension_version = option

  # sorter via folder name
  def sort_ext(string):
    words = string.split()
    return words[-1]

  # folder, just f to not clutter the strings
  f = extensions_folder
  ext_list = []

  log_usage(f'extensions-version-{option}')

  # i don't like this at all lmao
  # this is temporary until the fallback is too old to be usable
  # i think
  ext_version = {
    'images-browser': {
      'fallback': '23.03.16',
      'stable': '23.05.08',
    },
    'tagcomplete': {
      'fallback': '23.04.05',
      'stable': '23.06.09',
    },
    'aspect-ratio-preset': {
      'fallback': '23.03.31',
      'stable': '23.04.12',
    },
    'cutoff': {
      'fallback': '23.03.22',
      'stable': '23.05.03',
    },
    'dynamic-thresholding': {
      'fallback': '23.04.12',
      'stable': '23.05.22',
    },
    'tiled-multidiffusion-upscaler': {
      'fallback': '23.04.16',
      'stable': '23.06.10',
    },
  }

  ext_tag = 'stable'
  if webui_version == 'fallback':
    ext_tag = 'fallback'

  extensions = {
    'lite': [
      f'-b 23.05.03 https://github.com/anime-webui-colab/ext-batchlinks {f}/batchlinks',
      f'-b 23.03.31 https://github.com/anime-webui-colab/ext-state {f}/state',
      f'-b 22.12.10 https://github.com/anime-webui-colab/ext-tokenizer {f}/tokenizer',
      f'-b 23.02.27 https://github.com/anime-webui-colab/ext-tunnels {f}/tunnels',

      f'-b {ext_version["images-browser"][ext_tag]} https://github.com/anime-webui-colab/ext-images-browser {f}/images-browser',
      f'-b {ext_version["tagcomplete"][ext_tag]} https://github.com/anime-webui-colab/ext-tagcomplete {f}/tagcomplete',
    ],
    'stable': [
      f'-b 23.02.19 https://github.com/anime-webui-colab/ext-latent-couple-two-shot {f}/latent-couple-two-shot',
      f'-b 23.03.19 https://github.com/anime-webui-colab/ext-session-organizer {f}/session-organizer',

      f'-b {ext_version["aspect-ratio-preset"][ext_tag]} https://github.com/anime-webui-colab/ext-aspect-ratio-preset {f}/aspect-ratio-preset',
      f'-b {ext_version["cutoff"][ext_tag]} https://github.com/anime-webui-colab/ext-cutoff {f}/cutoff',
      f'-b {ext_version["dynamic-thresholding"][ext_tag]} https://github.com/anime-webui-colab/ext-dynamic-thresholding {f}/dynamic-thresholding',
      f'-b {ext_version["tiled-multidiffusion-upscaler"][ext_tag]} https://github.com/anime-webui-colab/ext-multidiffusion-upscaler {f}/tiled-multidiffusion-upscaler',
    ],
    'latest': [
      # using my own fork again to not lose my presets
      f'-b {ext_version["aspect-ratio-preset"][ext_tag]} https://github.com/anime-webui-colab/ext-aspect-ratio-preset {f}/aspect-ratio-preset',
      f'https://github.com/etherealxx/batchlinks-webui {f}/batchlinks',
      f'https://github.com/hnmr293/sd-webui-cutoff {f}/cutoff',
      f'https://github.com/mcmonkeyprojects/sd-dynamic-thresholding {f}/dynamic-thresholding',
      f'https://github.com/AlUlkesh/stable-diffusion-webui-images-browser {f}/images-browser',
      f'https://github.com/opparco/stable-diffusion-webui-two-shot {f}/latent-couple-two-shot',
      f'https://github.com/space-nuko/sd-webui-session-organizer {f}/session-organizer',
      f'https://github.com/ilian6806/stable-diffusion-webui-state {f}/state',
      f'https://github.com/DominikDoom/a1111-sd-webui-tagcomplete {f}/tagcomplete',
      f'https://github.com/AUTOMATIC1111/stable-diffusion-webui-tokenizer {f}/tokenizer',
      f'https://github.com/pkuliyi2015/multidiffusion-upscaler-for-automatic1111 {f}/tiled-multidiffusion-upscaler',
      # wait why? because the upstream is optimized for their colab, this is the one i refuse to update
      f'-b 23.02.27 https://github.com/anime-webui-colab/ext-tunnels {f}/tunnels',
    ],
    'experimental': [
      # this will change a lot, dont expect anything permanent here
      f'https://github.com/deforum-art/deforum-for-automatic1111-webui {f}/z-deforum',
      f'https://github.com/adieyal/sd-dynamic-prompts {f}/z-dynamic-prompts',
      f'https://github.com/ashen-sensored/stable-diffusion-webui-two-shot {f}/z-latent-couple-two-shot-regions',
      f'https://github.com/muerrilla/stable-diffusion-NPW {f}/z-negative-prompt-weight',
      f'https://github.com/hako-mikan/sd-webui-regional-prompter {f}/z-regional-prompter',
    ],
  }
  
  controlnet_extensions = {
    'stable': [
      # too lazy to test if they are stable, use latest instead
      # keeping it here for backwards compatibility
      f'-b 23.03.23 https://github.com/anime-webui-colab/ext-controlnet {f}/controlnet',
    ],
    'latest': [
      f'https://github.com/Mikubill/sd-webui-controlnet {f}/controlnet',
      f'https://github.com/fkunn1326/openpose-editor {f}/2d-openpose-editor',
      f'https://github.com/nonnonstop/sd-webui-3d-open-pose-editor {f}/3d-openpose-editor',
      #f'https://github.com/jexom/sd-webui-depth-lib {f}/depth-lib',
    ],
  }

  if only_controlnet:
    # if it breaks on stable, it breaks on stable
    if option in ['stable', 'latest', 'experimental']:
      return controlnet_extensions['latest']
    else:
      return []

  if option == 'none':
    print('😶 No extensions would be installed. Pure vanilla web UI')
  elif option == 'lite':
    print('🙂 No "advanced" extensions would be installed. Only installing the bare minimum.')
    ext_list = extensions['lite']
  elif option == 'stable':
    ext_list = extensions['lite'] + extensions['stable']
  elif option == 'latest':
    print('🔼 Installing the latest versions of the extensions.')
    ext_list = extensions['latest']
  elif option == 'experimental':
    print('😲 You are now installing some extensions I deem experimental for this colab!')
    print('😮 Experimental extensions are prefixed with "z-"')
    ext_list = extensions['latest'] + extensions['experimental']

  if option in ['latest', 'experimental'] and webui_version == 'fallback':
    print(f'\n😱 The fallback version of the web UI and {option} extensions do not mix well.')
    print(f'📣 Some extensions might be broken! You have been warned!\n')

  if controlnet != 'none' and option not in ['none', 'lite']:
    print(f'💃 ControlNet {controlnet} models detected, including related extensions!')
    controlnet_installed = True
    ext_list += controlnet_extensions['latest']

  if webui_version == 'fallback':
    print('\n📣 Fallback web UI version detected, using older extensions!\n')

  if option != 'none':
    print(f'📦 Installing {len(ext_list)} extensions ({option})...')

  ext_list.sort(key=sort_ext)
  return ext_list

def embeddings_list():
  print('💉 Fetching embeddings...')
  return [
    'https://huggingface.co/nick-x-hacker/bad-artist/resolve/main/bad-artist.pt',
    'https://huggingface.co/nick-x-hacker/bad-artist/resolve/main/bad-artist-anime.pt',
    'https://huggingface.co/datasets/Nerfgun3/bad_prompt/resolve/main/bad_prompt_version2.pt',
    'https://huggingface.co/datasets/gsdf/EasyNegative/resolve/main/EasyNegative.safetensors',
    'https://huggingface.co/gsdf/Counterfeit-V3.0/resolve/main/embedding/EasyNegativeV2.safetensors',
    'https://huggingface.co/yesyeahvh/bad-hands-5/resolve/main/bad-hands-5.pt',
    'https://huggingface.co/Xynon/models/resolve/main/experimentals/TI/bad-image-v2-39000.pt',
  ]

def configs_list():
  print('🔧 Fetching configs...')
  return [
    'https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/config.json',
    'https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/ui-config.json',
    'https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/styles.csv',
  ]

def patch_list():
  global chosen_webui_version

  def replace(item):
    if isinstance(item, str):
      item = item.replace('prepare_environment()', 'import webui')
      item = item.replace('launch.py', 'modules/launch_utils.py')
    return item

  import requests
  url = 'https://github.com/NUROISEA/anime-webui-colab/raw/main/configs/patch_list.txt'
  response = requests.get(url)
  data = response.text
  print('🩹 Applying web UI Colab patches...')
  p_list = data.splitlines()

  if chosen_webui_version not in ['fallback']:
    p_list[:] = [replace(item) for item in p_list]

  # still haphazardly adding this
  extra_patches = [
    'echo "🩹 Applying Colab memory patches..."',
    'wget -q https://github.com/camenduru/gperftools/releases/download/v1.0/libtcmalloc_minimal.so.4 -O /content/libtcmalloc_minimal.so.4',

    'echo "🩹 Applying httpx fix for new Colab version..."',
    # https://github.com/NUROISEA/anime-webui-colab/issues/35#issuecomment-1801356768
    'pip install -q httpx==0.24.1', 
  ]

  if chosen_webui_version in ['stable']:
    extra_patches += [
      'echo "🩹 Applying torch/xformers fix for new Colab version..."',
      # https://github.com/NUROISEA/anime-webui-colab/issues/39#issuecomment-2002471138
      'pip uninstall torch xformers -y',
      'python -m pip install -q torch==2.0.1 torchvision==0.15.2 --extra-index-url https://download.pytorch.org/whl/cu118 xformers==0.0.21',
    ]

  return p_list + extra_patches

def controlnet_list(option,webui_version='stable',extensions_version='stable'):
  global controlnet_installed
  
  log_usage(f'controlnet-version-{option}')

  controlnet_models = {
    'none': [],
    'v1.0': [
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_canny-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_depth-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_hed-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_mlsd-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_normal-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_openpose-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_scribble-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/control_seg-fp16.safetensors',
    ],
    'v1.0-diff': [
      'https://huggingface.co/kohya-ss/ControlNet-diff-modules/resolve/main/diff_control_sd15_canny_fp16.safetensors',
      'https://huggingface.co/kohya-ss/ControlNet-diff-modules/resolve/main/diff_control_sd15_depth_fp16.safetensors',
      'https://huggingface.co/kohya-ss/ControlNet-diff-modules/resolve/main/diff_control_sd15_hed_fp16.safetensors',
      'https://huggingface.co/kohya-ss/ControlNet-diff-modules/resolve/main/diff_control_sd15_mlsd_fp16.safetensors',
      'https://huggingface.co/kohya-ss/ControlNet-diff-modules/resolve/main/diff_control_sd15_normal_fp16.safetensors',
      'https://huggingface.co/kohya-ss/ControlNet-diff-modules/resolve/main/diff_control_sd15_openpose_fp16.safetensors',
      'https://huggingface.co/kohya-ss/ControlNet-diff-modules/resolve/main/diff_control_sd15_scribble_fp16.safetensors',
      'https://huggingface.co/kohya-ss/ControlNet-diff-modules/resolve/main/diff_control_sd15_seg_fp16.safetensors',
    ],
    't2i': [
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/t2iadapter_canny-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/t2iadapter_color-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/t2iadapter_depth-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/t2iadapter_keypose-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/t2iadapter_openpose-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/t2iadapter_seg-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/t2iadapter_sketch-fp16.safetensors',
      'https://huggingface.co/webui/ControlNet-modules-safetensors/resolve/main/t2iadapter_style-fp16.safetensors',
    ],
    'v1.1': [
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11e_sd15_ip2p_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_ip2p.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11e_sd15_shuffle_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11e_sd15_shuffle.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11f1p_sd15_depth_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11f1p_sd15_depth.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_canny_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_canny.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_inpaint_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_inpaint.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_lineart_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_lineart.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_mlsd_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_mlsd.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_normalbae_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_normalbae.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_openpose_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_openpose.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_scribble_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_scribble.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_seg_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_seg.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15_softedge_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15_softedge.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11p_sd15s2_lineart_anime_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11p_sd15s2_lineart_anime.yaml',
      'https://huggingface.co/comfyanonymous/ControlNet-v1-1_fp16_safetensors/resolve/main/control_v11u_sd15_tile_fp16.safetensors',
      'https://huggingface.co/ckpt/ControlNet-v1-1/resolve/main/control_v11u_sd15_tile.yaml',
    ],
  }

  if option == 'none':
    return controlnet_models['none']

  if extensions_version in ['none', 'lite']:
    print('\n😅 ControlNet models will only be downloaded if the extensions_versions is not "none" or "lite"')
    print('😉 Disconnect and delete this runtime and run this cell again, if you want ControlNet!')
    print('😆 Do not forget to change extensions_versions if you do so!\n')
    return controlnet_models['none']

  if not controlnet_installed:
    ext_list = extensions_list(option=extensions_version,only_controlnet=True)

    if len(ext_list) > 0:
      print(f'📦 Installing {len(ext_list)} extensions...')

    for ext in ext_list:
      ext_name = ext.split('/')[-1]
      print(f'  └ {ext_name}')
      run_shell(f'git clone {ext}')

    controlnet_installed = True

  count = len(controlnet_models[option])
  print(f'⌛ This might take a while! Grab a 🍿 or something xD')
  print('📢 These models are FP16, btw. ;)')
  print(f'🤙 Downloading {count} ControlNet {option} files/models...')

  return controlnet_models[option]

def arguments(model='', vae='', tunnel='gradio', ng_token='', ng_region='auto', extra_args='', default_override=''):
  default_arguments = ' '.join([
    '--opt-sdp-attention',
    '--lowram',
    '--no-hashing',
    '--enable-insecure-extension-access',
    '--no-half-vae',
    '--disable-safe-unpickle',
    '--gradio-queue',
  ])
  
  args = [
    default_arguments if not default_override else default_override,
    f'--ckpt \"{model}\"' if model else '',
    extra_args if extra_args else '',
  ]
  
  if vae != f'{vae_folder}/': # this is the models without VAEs
    args.append(f'--vae-path \"{vae}\"' if vae else '')

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

  # TODO: put this elsewhere
  print('\n\n\n💬 Logs after this are now logs of the web UI...\n\n\n')

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
  
  config_path = f'{web_ui_folder}/config.json'
  
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
    return f'echo "👍 {file_name} already downloaded."'

  aria2_flags = '--quiet --console-log-level=error -c -x 16 -s 16 -k 1M'

  if not installed_aria2:
    print('📦 Installing aria2...')
    run_shell('apt -y install -qq aria2')
    installed_aria2 = True

  print(f'⏬ Downloading {file_name} to {folder}...')

  models_downloaded += [ link ]

  return f'aria2c {aria2_flags} "{link}" -d "{folder}" -o "{file_name}"'

def wget_download(link, folder, file_name=''):
  global models_downloaded

  models_downloaded += [ link ]

  if file_name == '':
    return f'wget -q --show-progress {link} -P {folder}/ --content-disposition'

  return f'wget -q --show-progress {link} -P {folder}/ -O {file_name}'

def download_model(link, yaml_link='', folder=models_folder):
  # TODO: this function isn't elegant :/
  global models_downloaded
  file_name = link.split('/')[-1]
  commands = []

  if yaml_link not in models_downloaded and yaml_link != '':
    commands += [ f'wget -q "{yaml_link}" -P "{folder}/"' ]
    models_downloaded += [ yaml_link ]
  
  # i am cringing at this
  commands += [
    aria2_download(link, folder, file_name)
  ]

  return ' && '.join(commands)

def download_vae(link, folder=vae_folder):
  if link == '':
    return 'echo "Continuing without VAE..."'

  file_name = link.split('/')[-1]
  return aria2_download(link, folder, file_name)

def download_controlnet(link, folder=controlnet_models_folder):
  file_name = link.split('/')[-1].replace('-fp16','').replace('_fp16','')
  return aria2_download(link, folder, file_name)

# download functions for PYOM and UWUColab
def dl_model(link,yaml='',folder=model_download_folder):
  link = link.replace('/blob/', '/resolve/')
  has_downloaded_at_least_once = True
  return download_model(link,yaml,folder)

def dl_vae(link,yaml='',folder=vae_download_folder):
  link = link.replace('/blob/', '/resolve/')
  has_downloaded_at_least_once = True
  return download_vae(link,folder)

###############################################################################

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

print('👍 Utility script imported.')

notices = [
  '\n🛑 This notebook requires Colab Pro to work smoothly!\n',
]

for notice in notices:
  print(notice)