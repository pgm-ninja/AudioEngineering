import soundfile as sf
import pyloudnorm as pyln
import numpy as np
from pydub import AudioSegment, effects
import requests
import os
import time

data, samplerate = sf.read('script/cleaned.wav')


n = len(data)
Fs = samplerate




def apply_normalizarion():
    data, samplerate = sf.read('script/cleaned.wav')
    ch1 = np.array([data[i][0] for i in range(n)])
    ch2 = np.array([data[i][1] for i in range(n)])

    print(f'Sample rate: {samplerate}')
    print(f'Channel 1 {ch1}')
    print(f'Channel 2 {ch2}')

    balanced_signal = data - np.mean(ch1)
    peak_normalized_audio = pyln.normalize.peak(balanced_signal, -1.0)
    sf.write('script/cleaned.wav', peak_normalized_audio, samplerate)


def apply_audio_compressor():
    pydub_audio = AudioSegment.from_file('script/cleaned.wav')
    compressed_audio = effects.compress_dynamic_range(
        pydub_audio,
        threshold=-18,
        ratio=2.5,
        attack=1.79,
        release=11.1
    )
    compressed_audio.set_channels(2)
    compressed_audio.export('script/cleaned.wav')
    return compressed_audio.get_array_of_samples()


def noise_reduction():
    url = 'https://auphonic.com/api/simple/productions.json'
    username = os.environ.get('WEB_USERNAME')
    print(f'username set: {username}')
    password = os.environ.get('WEB_PASSWORD')
    preset_uuid = os.environ.get('PRESET_UUID')
    title = 'Enhanced Audio'
    action = 'start'

    data = {
    'preset': preset_uuid,
    'title': title,
    'action': action
    }
    input_file_path = '/home/qburst/Learn/AudioEngineering/script/test.wav'
    files = {
    'input_file': open(input_file_path, 'rb')
    }
    response = requests.post(url, data=data, files=files, auth=(username, password))
    response_data = response.json()
    print(f'Response after uploading: {response_data}')
    production_uuid = response_data['data']['uuid']

    download_url = None

    tries = 0

    while download_url is None:
        production_response = requests.get(f'https://auphonic.com/api/production/{production_uuid}.json', auth=(username, password))
        production_data = production_response.json()
        print(f'Data received after production: {production_data}')
        output_files = production_data['data']['output_files']

        for file_ in output_files:
            if file_['format'] == 'wav-24bit':
                download_url = file_['download_url']
                print('download_url: ', download_url)
        time.sleep(2)
        tries += 1
        if tries >= 100:
            print('Maximum tries exceeded!')
            break
    print('download_url: ', download_url)
    get_file = requests.get(download_url, auth=(username, password))
    with open('script/cleaned.wav', 'wb') as f:
        f.write(get_file.content)


# noise_reduction()
apply_normalizarion()
apply_audio_compressor()
