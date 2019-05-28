import numpy as np
from scipy.io import wavfile
from gtts import gTTS
from pydub import AudioSegment
import random

TEXT = 'Welcome to Aperture Science'
OUT_FILENAME = 'output'

tts = gTTS(text=TEXT, lang='en')
tts.save('gtts_%s.mp3' % OUT_FILENAME)

mp3 = AudioSegment.from_mp3('gtts_%s.mp3' % OUT_FILENAME)
mp3.export('%s.wav' % OUT_FILENAME, format='wav')

fs, data = wavfile.read('%s.wav' % OUT_FILENAME)

def shiftpitchup(segment, num):
  orig_fourtrans = np.fft.fft(segment)
  newft = np.int16([0]*num)
  newft = np.append(newft, orig_fourtrans[0:int(len(orig_fourtrans)/2-num)])
  newft = np.append(newft, orig_fourtrans[int(len(orig_fourtrans)/2+num):len(orig_fourtrans)])
  newft = np.append(newft, np.int16([0]*num))
  inv_fourier = np.fft.ifft(newft)
  return np.int16(inv_fourier.real)

def shiftpitchdown(segment, num):
  orig_fourtrans = np.fft.fft(segment)
  newft = orig_fourtrans[num:int(len(orig_fourtrans)/2)]
  newft = np.append(newft, np.int16([0]*num*2))
  newft = np.append(newft, orig_fourtrans[int(len(orig_fourtrans)/2):len(orig_fourtrans)-num])
  inv_fourier = np.fft.ifft(newft)
  return np.int16(inv_fourier.real)

def dictation(wavearray, freq): # freq 0.0-0.1
  fourt = np.fft.fft(wavearray)
  lenindex = len(fourt)
  for i in range(int(freq*lenindex*0.5)):
    fourt[i] /= 50
  for j in range(lenindex-int(freq*lenindex*0.5), lenindex):
    fourt[j] /= 50
  newarray = np.fft.ifft(fourt)
  return np.int16(newarray.real)

data_out = np.array([], np.int16)

step = 2400 # int(fs / 10)
for i in range(0, len(data), step):
  seg = data[i:i+step]
  prob = random.randint(0, 100)

  if prob < 20:
    seg_out = shiftpitchup(seg, num=20)
  elif 20 <= prob < 40:
    seg_out = shiftpitchdown(seg, num=20)
  else:
    seg_out = seg

  data_out = np.append(data_out, seg_out)

data_out = dictation(data_out, 0.02)

wavfile.write('%s.wav' % OUT_FILENAME, rate=fs, data=data_out)
