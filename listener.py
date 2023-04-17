#Listens for wake word and records 5 seconds of audio after it is heard
import pvporcupine
from pvrecorder import PvRecorder

keywords = ['alexa']

porcupine = pvporcupine.create(
    access_key='Dkio7ypK+LdtdNX6MR9ryh6CiM1tH5yCUTVwqS4J1sM5YHz0gebQPg==',
    keywords=keywords
)

recorder = PvRecorder(device_index=-1, frame_length=porcupine.frame_length)


try:
    recorder.start()

    # start listening
    while True:

        #Check if incoming audio contains wake word
        keyword_index = porcupine.process(recorder.read())
        if keyword_index >= 0:
            print(f"Detected {keywords[keyword_index]}")


except KeyboardInterrupt:
    recorder.stop()
finally:
    porcupine.delete()
    recorder.delete()
