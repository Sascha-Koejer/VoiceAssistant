import os
import sys
import time
import speech_recognition as sr
import pyttsx3
import subprocess
import datetime
import webbrowser
import pyautogui
from configparser import  ConfigParser

settings_folder = os.path.expandvars(R"C:\Users\$USERNAME\Documents\VoiceAssistant")
settings_path = os.path.expandvars(R"C:\Users\$USERNAME\Documents\VoiceAssistant\settings.ini")
config = ConfigParser()

if os.path.isfile(settings_path) != True:
    config["General"] = {
        "Folder_To_Sort" : "path",
		"Screenshot_Folder" : "path",
		"Spotify_Exe_Path" : "path"
    }
    config["Programs"] = {
        "name" : "Exe_Path"
    }
    config["SpotifyDevices"] = {
	    "name" : "device_id"
    }
    config["Spotify"] = {
        "username" : "",
		"client_id" : "",
		"client_secret" : ""
    }
    config["SortingFolders"] = {
	    "folder_name" : "file_extensions"
    }
	
    if os.path.exists(settings_folder) != True:
        os.mkdir(os.path.expandvars(settings_folder))
    with open(settings_path, "w") as configfile:
        config.write(configfile)

config.read(settings_path)

from modules import spotify
from modules import filesorting as fs

engine = pyttsx3.init()
sound = engine.getProperty('voices')
engine.setProperty('voice', sound[0].id)

wake = ["friday", "3D", "Scheide", "Kreide", "schade"]


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
	for key in config["Programs"]:
		if key in text:
			subprocess.Popen(str(config.get("Programs", key)))
			say(str(key) +  " wird gestartet")
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
	say("Ich habe die Suche gestartet")

while True:
	print("Listening")
	text = get_audio()

	for activation in wake:
		if activation.lower() in text:

			if text == activation.lower():
				say("Wie kann ich helfen?")
				text = get_audio()

			noteActivation = ["schreib", "notiz"]
			for word in noteActivation:
				if word in text:
					say("Was soll ich aufschreiben?")
					note_text = get_audio()
					note(note_text)
			
			if "neustart" in text:
				config.read(settings_path)
				say("Ich habe alle Einstellungen neu geladen")

			programActivation = ["starte", "öffne"]
			for word in programActivation:
				if word in text:
					startProgram(text)
			
			if "suche" in text:
				search(text)

			elif "spiele" and "von" in text:
				track = text.split("spiele")[1]
				track = track.split("von")[0]
				artist = text.split()
				artist = artist[-1]
				spotify.playSongFromArtist(track, artist)
				say("Ich spiele das Lied")

			elif "spiele" in text:
				spotify.playSong(text.split("spiele")[1])
				say("Ich spiele das Lied")

			elif "stop" in text:
				spotify.stopSong()
				say("Ich habe die Wiedergabe beendet")

			elif "vorheriges" in text:
				if spotify.previousSong() == True:
					say("Das vorherige Lied wird gespielt")
				elif spotify.previousSong() == False:
					say("Ich konnte kein vorheriges Lied finden")

			elif "wechsel" in text:
				spotify.changeDevice(text)
				say("Ich habe die Wiedergabe geändert")

			elif "lauter" in text:
				spotify.changeVolume("+")
				say("Lautstärke wurde erhöht")

			elif "leiser" in text:
				spotify.changeVolume("-")
				say("Lautstärke wurde gesenkt")

			elif "lautstärke" in text:
				volume = text.split("lautstärke")[1]
				volume = volume.split(" ")[1]
				spotify.setVolume(volume)
				say("Ich habe die Lautstärke angepasst")

			elif "screenshot" in text:
				myScreenshot = pyautogui.screenshot()
				myScreenshot.save(config.get("General", "screenshot_folder") + "\{}.png".format(dateNow()))
				say("Der Screenshot wurde gespeichert. Soll ich den Ordner öffnen?")
				text = get_audio()
				if text == "ja":
					os.startfile(config.get("General", "screenshot_folder"))

			elif "einstellungen" in text:
				os.startfile(settings_path)
				say("Hier sind meine Einstellungen")

			elif ("e-mail" in text) or ("email" in text):
				webbrowser.open("https://mail.google.com/mail/u/0/#inbox", new=2)
				say("E-Mails werden geöffnet")
			
			elif "räum auf" in text:
				fs.cleanUp()
				say("Ich habe den Ordner sortiert")

			elif "abschalten" in text:
				say("Bis bald")
				sys.exit()
				
			elif "speedtest" in text:
				say("Speedtest wird gestartet")
				os.system("start cmd /k speedtest-cli")

			