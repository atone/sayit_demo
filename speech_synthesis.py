import os
import azure.cognitiveservices.speech as speechsdk

def speak_text(text):
	speech_config = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
	audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
	speech_config.speech_synthesis_voice_name='zh-CN-XiaoxiaoMultilingualNeural'

	speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

	result = speech_synthesizer.speak_text_async(text).get()
	if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
		print("语音合成完成: [{}]".format(text))
	elif result.reason == speechsdk.ResultReason.Canceled:
		print("语音合成取消: {}".format(result.cancellation_details.reason))
