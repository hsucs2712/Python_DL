#from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
import azure.cognitiveservices.speech as speech_sdk
from playsound import playsound

def main():
    try:
        global speech_config

        # Get Configuration Settings
        #load_dotenv()
        cog_key = 'f4ad5afcb99b4e769720ee7b16f098d3' #os.getenv('COG_SERVICE_KEY')
        cog_region = 'eastasia' #os.getenv('COG_SERVICE_REGION')

        # Configure speech service
        # https://docs.microsoft.com/en-us/javascript/api/microsoft-cognitiveservices-speech-sdk/speechconfig?view=azure-node-latest
        # https://docs.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechconfig?view=azure-python
        # https://www.techonthenet.com/js/language_tags.php
        speech_config = speech_sdk.SpeechConfig(cog_key, cog_region, speech_recognition_language='zh-TW')
        print('Ready to use speech service in:', speech_config.region) 

        # Get spoken input
        command = TranscribeCommand()
        if command.lower() in['what time is it?', '現在幾點？', '幾點？']:
            TellTime()

    except Exception as ex:
        print(ex)

def TranscribeCommand():
    command = ''

    # Configure speech recognition 一個自己講話 
    audio_config = speech_sdk.AudioConfig(use_default_microphone=True)
    speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)
    print('Speak now...')

    # Configure speech recognition 播放語音檔案
    #audioFile = 'time.wav'
    #playsound(audioFile)
    #audio_config = speech_sdk.AudioConfig(filename=audioFile)
    #speech_recognizer = speech_sdk.SpeechRecognizer(speech_config, audio_config)    

    # Process speech input
    # Process speech input
    speech = speech_recognizer.recognize_once_async().get()
    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print(command)
    else:
        print(speech.reason)
        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print(cancellation.reason)
            print(cancellation.error_details)

    # Return the command
    return command


def TellTime():
    now = datetime.now()
    response_text = '現在時間是 {}:{:02d}'.format(now.hour,now.minute)


    # Configure speech synthesis
    # https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support?tabs=speechtotext#text-to-speech
    speech_config.speech_synthesis_voice_name = "zh-TW-HsiaoChenNeural"
    speech_synthesizer = speech_sdk.SpeechSynthesizer(speech_config)    

    # Synthesize spoken output
    speak = speech_synthesizer.speak_text_async(response_text).get()
    if speak.reason != speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print(speak.reason)


    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()