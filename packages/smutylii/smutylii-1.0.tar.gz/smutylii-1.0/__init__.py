# Modules
# Sound

import playsound

def StartSound(soundfile):
    try:
        playsound.playsound(soundfile)

    except:
        print(f"No file as '{soundfile}'")

StartSound('jdfs')

