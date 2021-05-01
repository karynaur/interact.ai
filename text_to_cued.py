from nltk.corpus import cmudict
import nltk
import sys

d = cmudict.dict()

def pronounce(word):
  return [list(y[:-1].lower() if y[-1].isdigit() else y.lower() for y in x ) for x in d[word.lower()]] 

def get_pronounce(sentence):
  return [pronounce(x)[0] for x in list(sentence.split())]

def vovel_check(syllable):
  vovels = ['a', 'e', 'i', 'o', 'u']
  for i in syllable:
    if i in vovels:
      return True
  return False


def find_hand_shape(s):
  # Code to find the handshape of the syllable 
  for item in handshapes:
    if s in handshapes[item]:
      return item
  raise ValueError(*s)

def find_pos(s):
  # Code to find the position of the syllable 
  for item in positions:
    if s in positions[item]:
      return item
  raise ValueError(*s)
  
handshapes = {
    '1': ['d', 'p', 'zh'],
    '2': ['dh', 'k', 'v', 'z'],
    '3': ['s', 'h', 'r','hh'],
    '4': ['wh', 'b', 'n'],
    '5': ['m', 't', 'f', 'a', 'e', 'i', 'o', 'u'],
    '6': ['w', 'sh','l'],
    '7': ['th', 'j','g','jh'],
    '8': ['y','ng', 'ch']
  }

positions={
    '1': ['ee', 'er','ey'],
    '2': ['aw', 'ue', 'eh','ih','ow', 'uw'],
    '3': ['oo', 'i', 'a','ao','aa','ae'],
    '4': ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z','hh','sh','jh'],
    '5': ['oe', 'ah'],
    '6': ['uh'],
    '7': ['oi', 'ay','oy'],
    '8': ['ie', 'ou','iy']
  }


for word in get_pronounce(sys.argv[1]):
  for i in range(len(word)):

    if i != (len(word)-1):
      # Rule 1: Consonent sound on its own no vovel after it
      if not vovel_check(word[i])  and not vovel_check(word[i+1]):
        # cued in the side position
        pos = '4'
        hand_shape = find_hand_shape(word[i])
        print(word[i],pos,hand_shape)

      # Rule 3: consonent folowed by a vovel
      if not vovel_check(word[i]) and vovel_check(word[i+1]):
        hand_shape = find_hand_shape(word[i])
        pos = find_pos(word[i+1])
        print(word[i],word[i+1],pos,hand_shape)
        continue
    else:
      if not vovel_check(word[i]):
        pos = '4'
        hand_shape = find_hand_shape(word[i])
        print(word[i],pos,hand_shape)

    
    if i != 0:
      # Rule 2: vovel on its own without a consonent before it or at the start of the word
      if vovel_check(word[i]) and vovel_check(word[i-1]):
        hand_shape = '5'
        pos = find_pos(word[i])
        print(word[i],pos,hand_shape)
    if i == 0 and vovel_check(word[i]):
      hand_shape = '5'
      pos = find_pos(word[i])
      print(word[i],pos,hand_shape)


  print('============================')

