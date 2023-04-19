#Listens for wake word and records 5 seconds of audio after it is heard
import pvporcupine
from pvrecorder import PvRecorder
import pyaudio
import wave

# the file name output you want to record into
filename = "recievedMessage.wav"
# set the chunk size of 1024 samples
chunk = 1024
# sample format
FORMAT = pyaudio.paInt16
# mono, change to 2 if you want stereo
channels = 1
# 44100 samples per second
sample_rate = 44100
record_seconds = 4
# initialize PyAudio object
p = pyaudio.PyAudio()


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

            # Stop the recordeer
            recorder.stop()

            # open stream object as input & output
            stream = p.open(format=FORMAT,
                            channels=channels,
                            rate=sample_rate,
                            input=True,
                            output=True,
                            frames_per_buffer=chunk)
            frames = []
            print("Recording...")
            for i in range(int(sample_rate / chunk * record_seconds)):
                data = stream.read(chunk)
                # if you want to hear your voice while recording
                # stream.write(data)
                frames.append(data)
            print("Finished recording.")
            # stop and close stream
            stream.stop_stream()
            stream.close()
            # save audio file
            # open the file in 'write bytes' mode
            wf = wave.open(filename, "wb")
            # set the channels
            wf.setnchannels(channels)
            # set the sample format
            wf.setsampwidth(p.get_sample_size(FORMAT))
            # set the sample rate
            wf.setframerate(sample_rate)
            # write the frames as bytes
            wf.writeframes(b"".join(frames))
            # close the file
            wf.close()

            # Start the recorder again
            recorder.start()


except KeyboardInterrupt:
    recorder.stop()
    # terminate pyaudio object
    p.terminate()
finally:
    porcupine.delete()
    recorder.delete()
