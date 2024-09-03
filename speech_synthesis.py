import os
import azure.cognitiveservices.speech as speechsdk
import threading

def speak_text_async(text):
	def synthesize_in_background():
		speech_config = speechsdk.SpeechConfig(subscription=os.getenv('AZURE_SPEECH_KEY'), region=os.getenv('AZURE_SPEECH_REGION'))
		audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
		speech_config.speech_synthesis_voice_name='zh-CN-XiaoxiaoMultilingualNeural'

		speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

		def on_synthesis_completed(evt):
			if evt.result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
				print("语音合成完成: [{}]".format(text))
			elif evt.result.reason == speechsdk.ResultReason.Canceled:
				print("语音合成取消: {}".format(evt.result.cancellation_details.reason))

		speech_synthesizer.synthesis_completed.connect(on_synthesis_completed)
		speech_synthesizer.speak_text_async(text)

	threading.Thread(target=synthesize_in_background).start()
	return "语音合成已开始"
