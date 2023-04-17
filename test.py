import os
import sys
import time
import pyaudio
import pvporcupine

WAKEWORD_PATH = './Alexa_en_windows_v2_2_0.ppn'
AUDIO_DEVICE_INDEX = None
SAMPLE_RATE = 16000
NUM_CHANNELS = 1
FRAME_LENGTH = 512

def main():
    porcupine = None
    pa = None
    audio_stream = None
    pico_access_key ='Dkio7ypK+LdtdNX6MR9ryh6CiM1tH5yCUTVwqS4J1sM5YHz0gebQPg=='

    try:
        porcupine = pvporcupine.create(access_key=pico_access_key, keywords=["alexa"])
        pa = pyaudio.PyAudio()

        for keyword in pvporcupine.KEYWORDS:
            print(keyword)

        audio_stream = pa.open(
            rate=SAMPLE_RATE,
            channels=NUM_CHANNELS,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=FRAME_LENGTH,
            input_device_index=AUDIO_DEVICE_INDEX)

        print('Listening for the wake word...')

        while True:
            pcm = audio_stream.read(FRAME_LENGTH)
            pcm = [int(x) for x in pcm]
            result = porcupine.process(pcm)

            if result >= 0:
                print('Wake word detected! Recording for 5 seconds...')
                record_audio(pa, 5)
                print('Finished recording. Listening for the wake word...')

    except KeyboardInterrupt:
        print('Stopping...')
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        if porcupine is not None:
            porcupine.delete()

def record_audio(pa, duration):
    output_file = 'recorded_audio.wav'
    stream = pa.open(rate=SAMPLE_RATE,
                     channels=NUM_CHANNELS,
                     format=pyaudio.paInt16,
                     input=True,
                     frames_per_buffer=FRAME_LENGTH,
                     input_device_index=AUDIO_DEVICE_INDEX)

    frames = []

    for _ in range(0, int(SAMPLE_RATE / FRAME_LENGTH * duration)):
        data = stream.read(FRAME_LENGTH)
        frames.append(data)

    stream.stop_stream()
    stream.close()

    wf = wave.open(output_file, 'wb')
    wf.setnchannels(NUM_CHANNELS)
    wf.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
    wf.setframerate(SAMPLE_RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

if __name__ == '__main__':
    main()
