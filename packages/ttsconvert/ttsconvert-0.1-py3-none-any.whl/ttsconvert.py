import gtts
import pyttsx3

def tts_file(text, filename):
	tts = gTTS(text, lang="ru")
	tts = gTTS(text, lang="en")

	tts.save(filename)

def tts_speech(text):
	engine = pyttsx3.init()
	engine.say(text)
	engine.runAndWait()

def help():
	print("Help:")
	print("ttsconvert.tts_file - Saving file.")
	print("Example:")
	print("import ttsconvert")
	print("ttsconvert.tts_file('text', 'filename')")
	print("ttsconvert.tts_speech - Speech.")
	print("Example:")
	print("import ttsconvert")
	print("ttsconvert.tts_speech('text')")
	input()