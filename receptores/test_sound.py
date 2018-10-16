from kivy import platform
import os
print(platform)

if platform != "macosx":
    from kivy.core.audio import SoundLoader

    sound = SoundLoader.load('beep-06.wav')


    if sound:
        print("Sound found at %s" % sound.source)
        print("Sound is %.3f seconds" % sound.length)
        sound.play()
else:
    os.system("afplay beep-06.wav")
    os.system("afplay beep-06.wav")
    os.system("afplay beep-06.wav")
