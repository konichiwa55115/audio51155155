import requests
import json
import time
import base64
import os
import cv2
import copy
import numpy as np
import os.path
import shutil
import speech_recognition as sr 
from pydub import AudioSegment
from pydub.silence import split_on_silence
from gtts import gTTS
from websocket import create_connection



##############################################################################################################
# speech to text


r = sr.Recognizer()


r.recognize_google(audio, language='ar-AR')

def get_large_audio_transcription(path,message):

    id = message.id
    sound = AudioSegment.from_wav(path)  
    chunks = split_on_silence(sound,
        min_silence_len = 500,
        silence_thresh = sound.dBFS-14,
        keep_silence=500,
    )

    folder_name = f"audio-chunks-{id}"
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""

    tsize = os.path. getsize(path)
    # edi = app.send_message(message.chat.id,f"Total Size: {tsize}") # status
    psize = 0

    for i, audio_chunk in enumerate(chunks, start=1):
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        with sr.AudioFile(chunk_filename) as source:
            audio_listened = r.record(source)

            try:
                text = r.recognize_google(audio_listened)
            except sr.UnknownValueError as e:
                #print("Error:", str(e))
                whole_text += "\n(error)\n"
            else:
                text = f"{text.capitalize()}. "
                #print(chunk_filename, ":", text)
                whole_text += text
        size = os.path. getsize(chunk_filename)        
        psize = psize + size
        # app.edit_message_text(f"Processed {psize/1024/1024} MB out of {tsize/1024/1024} MB - {math.floor(psize*100/tsize)}%",message.chat.id,edi.message_id)

    return whole_text


def splitfn(file,message,output):
	
	converted = get_large_audio_transcription(file,message)
	
	with open(output,"w") as file:
		file.write(converted)
	
	shutil.rmtree(f"audio-chunks-{message.id}", ignore_errors=True)
	return output



########################################################################################################################################################	
