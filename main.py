from text_to_cued import cued_speech
from Wav2Lip import inference
from gtts import gTTS
import argparse
from pydub import AudioSegment
import json

#preprocessing
import os
import glob

def main(sentence): 
  files = glob.glob('audio/*')
  files.extend(glob.glob('videos/*'))
  if files is not None:
     for i in files:
https://www.youtube.com/watch?v=yNLtlZHmb6s        os.remove(i)


  words = []
  for i,word in enumerate(sentence.split()):
     words.append(cued_speech(word))
     tts = gTTS(word,lang = 'en', tld = 'ca')
     tts.save(f'audio/{i}.wav')
     audio = AudioSegment.from_file(f'audio/{i}.wav')
     words[i]['length'] = audio.duration_seconds/len(words[i]['word'])


     args = argparse.Namespace(audio=f'audio/{i}.wav', box=[-1, -1, -1, -1],\
     checkpoint_path='Wav2Lip/checkpoints/wav2lip_gan.pth', crop=[0, -1, 0, -1],\
     face='face.png', face_det_batch_size=16, fps=25.0, img_size=96, nosmooth=False,\
     outfile=f'videos/{i}.mp4', pads=[0, 10, 0, 0], resize_factor=1, rotate=False, \
     static=True, wav2lip_batch_size=128)
     
     inference.main(args)

  return json.dumps(str(words))
