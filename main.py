from google.cloud import texttospeech
import os
import pyaudio
import pvporcupine
import pvleopard

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = './text-to-speech-project-mmu-b433f405c098.json'

#Google Text to speech code
    
# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Set the text input to be synthesized
synthesis_input = texttospeech.SynthesisInput(text="David Halpin-Roberts test.")

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

# Perform the text-to-speech request on the text input with the selected
# voice parameters and audio file type
#response = client.synthesize_speech(
#    input=synthesis_input, voice=voice, audio_config=audio_config
#)

# The response's audio_content is binary.
#with open("output.mp3", "wb") as out:
    # Write the response to the output file.
#    out.write(response.audio_content)
#    print('Audio content written to file "output.mp3"')




#Picovoice code
picoKey = 'Dkio7ypK+LdtdNX6MR9ryh6CiM1tH5yCUTVwqS4J1sM5YHz0gebQPg=='
#leopard = pvleopard.create(access_key='Dkio7ypK+LdtdNX6MR9ryh6CiM1tH5yCUTVwqS4J1sM5YHz0gebQPg==')
#audioPath = "./testAudioClip.mp3"

def get_supported_sample_rates(device_index):
    supported_sample_rates = []
    for sample_rate in range(8000, 50000, 1000):
        try:
            test_stream = pa.open(
                rate=sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                input_device_index=device_index,
                frames_per_buffer=512,
            )
            supported_sample_rates.append(sample_rate)
            test_stream.close()
        except Exception as e:
            pass
    return supported_sample_rates

# Initialize Porcupine with a built-in keyword
porcupine = None
try:
    porcupine = pvporcupine.create(access_key=picoKey,keyword_paths=[pvporcupine.KEYWORD_PATHS["alexa"]])
except Exception as e:
    print(f"Failed to initialize Porcupine: {str(e)}")

# Set up PyAudio to record from the microphone
audio_stream = None
pa = pyaudio.PyAudio()

for i in range(pa.get_device_count()):
    device_info = pa.get_device_info_by_index(i)
    if device_info['maxInputChannels'] > 0:
        print(f"Input Device index {i} - {device_info['name']}")


try:
    input_device_index = 1
    supported_sample_rates = get_supported_sample_rates(input_device_index)
    print(f"Supported sample rates for device {input_device_index}: {supported_sample_rates}")

    audio_stream = pa.open(
        rate=porcupine.sample_rate,
        channels=1,
        format=pyaudio.paInt16,
        input=True,
        frames_per_buffer=porcupine.frame_length,
)
except Exception as e:
    print(f"Failed to open audio stream: {str(e)}")
    exit(1) 


# Main loop
if porcupine is None:
    print("Porcupine initialization failed. Exiting.")
    exit(1)

try:
    while True:
        # Read audio samples from the microphone
        pcm = []
        while len(pcm) < porcupine.frame_length:
            buffer = audio_stream.read(porcupine.frame_length - len(pcm), exception_on_overflow=False)
            pcm.extend(int(p) for p in buffer[:porcupine.frame_length - len(pcm)])

        # Process the audio samples with Porcupine
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            # Wake word detected, record 3 seconds of audio
            print("Wake word detected!")
            audio_data = []
            for _ in range(0, int(porcupine.sample_rate / porcupine.frame_length * 3)):
                audio_data += audio_stream.read(porcupine.frame_length)
            
            # Convert recorded audio to text
            audio_path = "recorded_audio.wav"
            with open(audio_path, "wb") as wf:
                wf.write(b"".join(audio_data))

            # Process recorded audio with Picovoice Leopard
            leopard = pvleopard.create(access_key='Dkio7ypK+LdtdNX6MR9ryh6CiM1tH5yCUTVwqS4J1sM5YHz0gebQPg==')
            transcript, words = leopard.process_file(audio_path)
            print(transcript)

            # Synthesize speech from the transcript
            #synthesize_speech(transcript)

finally:
    # Clean up resources
    if audio_stream is not None:
        audio_stream.close()

    if porcupine is not None:
        porcupine.delete()

    if pa is not None:
        pa.terminate()