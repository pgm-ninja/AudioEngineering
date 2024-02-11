import pipeclient
from constants import *
import subprocess
import time
import requests
import urllib.request


file_path = '/home/qburst/Learn/AudioEngineering/'


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
client.write(f'Import2:Filename="{file_path + "test.wav"}"')

# Ensure that entire file is selected.
client.write('SelectAll:')
client.write('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1" StereoIndependent="0"')
client.write('Compressor:AttackTime="1.79" NoiseFloor="-40" Normalize="1" Ratio="2.5" ReleaseTime="11.1" Threshold="-18" UsePeak="0"')
# client.write('FilterCurve:f0="4000" f1="5000" FilterLength="8191" InterpolateLin="0" InterpolationMethod="B-spline" v0="0" v1="9"')
# client.write('FilterCurve:f0="100" f1="500" FilterLength="8191" InterpolateLin="0" InterpolationMethod="B-spline" v0="9" v1="0"')
# client.write('Normalize:ApplyGain="1" PeakLevel="-1" RemoveDcOffset="1" StereoIndependent="0"')
# # Export
client.write(f'Export2:Filename={file_path}"audacity_cleaned.wav" NumChannels={CHANNEL}')

end_time = time.time()

time_diff = (end_time - start_time) + 3

time.sleep(time_diff)

process.terminate()


