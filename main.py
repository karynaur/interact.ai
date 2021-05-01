from text_to_cued import cued_speech
from Wav2Lip import inference
from gtts import gTTS

sentence = "jack is a good boy"
words = []
for word in sentence.split():
   words.append(cued_speech(word))
   



