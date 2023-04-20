#!/usr/bin/env python3

from google.cloud import texttospeech
import os
import rospy
from std_msgs.msg import String

try:
    package_path = rospy.get_param('/turtlebot_voice_control_package_path')
except KeyError:
    package_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(package_path, 'config', 'text-to-speech-project-mmu-b433f405c098.json')

# Instantiates a client
client = texttospeech.TextToSpeechClient()

# Build the voice request, select the language code ("en-US") and the ssml
# voice gender ("neutral")
voice = texttospeech.VoiceSelectionParams(
    language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
)

# Select the type of audio file you want returned
audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3
)

def synthesize_text(text):
    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    with open(os.path.join(package_path, "output", "output.mp3"), "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file "output.mp3"')

def callback(msg):
    synthesize_text(msg.data)

if __name__ == '__main__':
    rospy.init_node('speaker_node')
    rospy.Subscriber('voice_commands', String, callback)
    rospy.spin()
