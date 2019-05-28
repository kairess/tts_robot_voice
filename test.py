import pyttsx3

engine = pyttsx3.init()

print(engine.getProperty('rate'))
# engine.setProperty('rate', 250)
voices = engine.getProperty('voices')
print(len(voices))

# nsss for mac osx
voices_list = [0, 7, 10, 11, 16, 17, 25, 26, 28, 32, 35, 36, 39, 40, 43]
voices_female_list = [16, 17, 25, 26, 28, 32, 35, 36, 39, 40]
voices_list = [25, 35, 39]

engine.setProperty('voice', voices[25].id)

engine.say('Welcome to Aperture Science')
engine.runAndWait()
engine.stop()
