import os
import time
import speech_recognition as sr
import pyttsx3
import subprocess
import datetime
import webbrowser
import pyautogui

engine = pyttsx3.init()
sound = engine.getProperty('voices')
engine.setProperty('voice', sound[0].id)


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

def dateNow():
	date = datetime.datetime.now()
	date = datetime.datetime.strptime(str(date), '%Y-%m-%d %H:%M:%S.%f').strftime('%d-%m-%Y %H-%M-%S')
	return str(date)

def note(text):
	filename = dateNow() + ".txt"
	path = os.path.join(r'C:\Users\koeje\Desktop', filename)
	with open(path, "w") as f:
		f.write(text)
	subprocess.Popen(["notepad.exe", path])
	say("Ich habe die Notiz gespeichert")

def startProgram(text):
	if "discord" in text:
		#os.path.expandvars(r"C:\Users\$USERNAME\Documents\YTDownloader")
		subprocess.Popen(os.path.expandvars(R"C:\Users\$USERNAME\AppData\Local\Discord\app-0.0.306\Discord.exe"))
		say("Discord wird gestartet")
		return

	elif "steam" in text:
		subprocess.Popen(r"D:\Programme\Steam\Steam.exe")
		say("Steam wird gestartet")
		return

	elif "youtube" in text:
		webbrowser.open("https://www.youtube.com/feed/subscriptions", new=2)
		say("YouTube wird geöfnet")
		return

	else:
		say("Ich konnte das Programm nicht finden")
		return

def search(text):
	if "suche" and "wikipedia" in text:
		webbrowser.open("https://de.wikipedia.org/w/index.php?cirrusUserTesting=control&search={}".format(text.split("nach")[1]), new=2)
	elif "suche" and "youtube" in text:
		webbrowser.open("https://www.youtube.com/results?search_query={}".format(text.split("nach")[1]), new=2)
	elif "suche" in text:
		webbrowser.open("https://www.google.com/search?q={}".format(text.split("nach")[1]), new=2)

while True:
	print("Listening")
	text = get_audio()

	if wake in text:

		if text == wake:
			say("Wie kann ich helfen?")
			text = get_audio()

		noteActivation = ["schreib", "notiz"]
		for word in noteActivation:
			if word in text:
				say("Was soll ich aufschreiben?")
				note_text = get_audio()
				note(note_text)
		
		programActivation = ["start", "öffne"]
		for word in programActivation:
			if word in text:
				startProgram(text)
		
		if "suche" in text:
			search(text)

		elif "screenshot" in text:
			myScreenshot = pyautogui.screenshot()
			myScreenshot.save(r'C:\Users\koeje\Pictures\Screenshots\{}.png'.format(dateNow()))
			say("Der Screenshot wurde gespeichert. Soll ich den Ordner öffnen?")
			text = get_audio()
			if text == "ja":
				os.startfile(r'C:\Users\koeje\Pictures\Screenshots')

		elif "e-mail" in text:
			webbrowser.open("https://mail.google.com/mail/u/0/#inbox", new=2)
			
		elif "speedtest" in text:
			os.system("start cmd /k speedtest-cli")

			