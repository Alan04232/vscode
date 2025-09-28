import subprocess
mp3_file ="/home/alan/Downloads/Baby (PenduJatt.Com.Se).mp3"
wav_file = mp3_file.replace('.mp3','.wav').replace("'",'')
command = ['ffmpeg', '-i', mp3_file, wav_file]
subprocess.run(command)
print(f"Converted {mp3_file} to {wav_file}")