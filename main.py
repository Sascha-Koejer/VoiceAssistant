import os
import time
import playsound
import speech_recognition as sr
import pyttsx3
import subprocess
import datetime
import webbrowser                        

german_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_DE-DE_HEDDA_11.0"

engine = pyttsx3.init()
engine.setProperty('voice', german_voice)

wake = "friday"

def get_audio():
		r = sr.Recognizer()
		with sr.Microphone() as source:
			audio = r.listen(source)
			said = ""

			try:
				said = r.recognize_google(audio, language="de_DE")
				print(said)
			except Exception as e:
				print("Exception: " + str(e))

		return said.lower()

def say(text):
	engine.say(text)
	engine.runAndWait()

def note(text):
	date = datetime.datetime.now()
	file_name = str(date).replace(":", "-") + "-note.txt"
	with open(file_name, "w") as f:
		f.write(text)
	subprocess.Popen(["notepad.exe", file_name])


while True:
	print("Listening")
	text = get_audio()

	if text.count(wake) > 0:
		say("Was gibts?")
		text = get_audio()
	

		NOTE_STRS = ["schreib", "notiz"]
		for phrase in NOTE_STRS:
			if phrase in text:
				say("Was soll ich aufschreiben?")
				note_text = get_audio()
				note(note_text)
				say("Ich habe eine Notiz erstellt")
		
		if "discord" in text:
			subprocess.Popen(r"C:\Users\koeje\AppData\Local\Discord\app-0.0.306\Discord.exe")

		if "steam" in text:
			subprocess.Popen(r"D:\Programme\Steam\Steam.exe")

		if "youtube" in text:
			webbrowser.open("https://www.youtube.com/feed/subscriptions", new=2)

		if "e-mail" in text:
			webbrowser.open("https://mail.google.com/mail/u/0/#inbox", new=2)

		if "speedtest" or "speed" or "test" in text:
			os.system("start cmd /k speedtest-cli")
	