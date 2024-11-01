# Made in October 2024, inspired by Han Kang's Nobel Prize in Literature
import speech_recognition as sr

# Load the audio file for transcription
audio_file_path = "./nobel.mp3"
recognizer = sr.Recognizer()

# Convert the mp3 file to text
with sr.AudioFile(audio_file_path) as source:
    audio_data = recognizer.record(source)
    try:
        # Using Google's speech recognition
        text_output = recognizer.recognize_google(audio_data, language="en-US")
    except sr.UnknownValueError:
        text_output = "Sorry, the audio was not clear enough for transcription."
    except sr.RequestError:
        text_output = "Sorry, there was an issue with the transcription service."

print('successfully recognized')
print(text_output)
