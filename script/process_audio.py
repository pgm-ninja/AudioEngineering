import pipeclient
from constants import *
import subprocess
import time
import requests
import urllib.request


file_path = '/home/qburst/Learn/AudioEngineering/'


url = "https://auphonic.com/api/simple/productions.json"
username = "ammuvavamol111"
password = "albaedis321"
preset_uuid = "K8eZrEbNvTEK6L4d7fiy5c"
title = "Enhanced Audio"
input_file_path = file_path + '/test.wav'
action = "start"

data = {
    "preset": preset_uuid,
    "title": title,
    "action": action
}

files = {
    "input_file": open('/home/qburst/Learn/AudioEngineering/script/cleaned.wav', "rb")
}

response = requests.post(url, data=data, files=files, auth=(username, password))

time.sleep(20)

response_data = response.json()

production_uuid = response_data['data']['uuid']


production_response = requests.get(f'https://auphonic.com/api/production/{production_uuid}.json', auth=(username, password))

production_data = production_response.json()

print(production_data)

download_url = None

output_files = production_data['data']['output_files']

for file_ in output_files:
    if file_['format'] == 'mp3':
        download_url = file_['download_url']

get_file = requests.get(download_url, auth=(username, password))

with open('cleaned.mp3', 'wb') as f:
    f.write(get_file.content)



while True:
    try:
        process = subprocess.Popen(['/usr/bin/audacity'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        time.sleep(5)
        if process.poll() is None:
            print("Audacity opened successfully!")
            break
    except Exception as e:
        print(f"Error: {e}")


start_time = time.time()

client = pipeclient.PipeClient()

# Import file to process
client.write(f'Import2:Filename="{file_path + "cleaned.mp3"}"')

# Ensure that entire file is selected.
client.write('SelectAll:')
client.write('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1" StereoIndependent="0"')
client.write('Compressor:AttackTime="1.79" NoiseFloor="-40" Normalize="1" Ratio="2.5" ReleaseTime="11.1" Threshold="-18" UsePeak="0"')
client.write('FilterCurve:f0="4000" f1="5000" FilterLength="8191" InterpolateLin="0" InterpolationMethod="B-spline" v0="0" v1="9"')
client.write('FilterCurve:f0="100" f1="500" FilterLength="8191" InterpolateLin="0" InterpolationMethod="B-spline" v0="9" v1="0"')
client.write('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1" StereoIndependent="0"')
# Export
client.write(f'Export2:Filename={file_path}"enhanced.mp3" NumChannels={CHANNEL}')

end_time = time.time()

time_diff = (end_time - start_time) + 3

time.sleep(time_diff)

process.terminate()


