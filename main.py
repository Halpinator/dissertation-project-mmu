from google.cloud import texttospeech
import pvleopard

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
response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
)

# The response's audio_content is binary.
with open("output.mp3", "wb") as out:
    # Write the response to the output file.
    out.write(response.audio_content)
    print('Audio content written to file "output.mp3"')




#Picovoice code
leopard = pvleopard.create(access_key='Dkio7ypK+LdtdNX6MR9ryh6CiM1tH5yCUTVwqS4J1sM5YHz0gebQPg==')
audioPath = "./testAudioClip.mp3"

transcript, words = leopard.process_file(audioPath)
print(transcript)
for word in words:
    print(
      "{word=\"%s\" start_sec=%.2f end_sec=%.2f confidence=%.2f}"
      % (word.word, word.start_sec, word.end_sec, word.confidence))


