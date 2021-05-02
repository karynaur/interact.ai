#preprocessing
import os
import glob

def main(sentence): 
  if sentence == "favicon.ico":return 
  files = glob.glob('/var/www/html/audio/*')
  files.extend(glob.glob('/var/www/html/videos/*'))
  #files.append('/home/vish/output/html/output.html')
  if files is not None:
     for i in files:
        os.remove(i)


  words = []
  for i,word in enumerate(sentence.split()):
     words.append(cued_speech(word))
     tts = gTTS(word,lang = 'en', tld = 'ca')
     tts.save(f'/var/www/html/audio/{i}.wav')
     #tts.save(f'audio/{i}.wav')
     audio = AudioSegment.from_file(f'/var/www/html/audio/{i}.wav') #audio/{i}.wav')
     words[i]['length'] = audio.duration_seconds/len(words[i]['word'])


     args = argparse.Namespace(audio=f'/var/www/html/audio/{i}.wav', box=[-1, -1, -1, -1], \
     checkpoint_path='Wav2Lip/checkpoints/wav2lip_gan.pth', crop=[0, -1, 0, -1],\
     face='face.png', face_det_batch_size=16, fps=25.0, img_size=96, nosmooth=False,\
     outfile=f'/home/vish/output/html/videos/{i}.mp4', pads=[0, 10, 0, 0], resize_factor=1, rotate=False, \
     static=True, wav2lip_batch_size=128)

     inference.main(args)
     with open('/var/www/html/output.html', 'w+') as f:
         f.write(str(words))

  return json.dumps(str(words))
