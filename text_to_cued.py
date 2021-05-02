from nltk.corpus import cmudict
import nltk
import sys
from predict_pronun import predict
d = cmudict.dict()

class Tokenizer:
    def __init__(self, data, vocab_size):
        self.vocab_size = vocab_size
        self.vocab = self.build_vocab(data)
        
        self.stoi = { ch:i for i,ch in enumerate(self.vocab) }
        self.itos = { i:ch for i,ch in enumerate(self.vocab) }
    
    def sort_vocab(self, vocab):
        """
        Vocab should have the followind order: hashtag, numbers, characters sorted by length.
        Hashtags should go first, because they will be used as dividers on tokenization step.
        Numbers should go before characters, because token ids are numbers. Otherwise token ids will be considered as usual numbers and replaced twice.
        """
        sorted_vocab = sorted(vocab, key=lambda x: len(x), reverse=True)
        tag = [int(s) for s in sorted_vocab if s == '#']
        
        numeric = [int(s) for s in sorted_vocab if s.isnumeric()]
        numeric = [str(s) for s in sorted(numeric, reverse=True)]
        rest = [s for s in sorted_vocab if not s.isnumeric()]
        
        sorted_vocab = tag + numeric + rest
        
        return sorted_vocab
    
    def build_vocab(self, data):
        """
        Build vocabluary using BPE alghorithm.
        """
        vocab = set(data)
        if len(vocab) > self.vocab_size:
            raise ValueError('Vocab size should be greater than unique char count')

        # check all available characters
        char_set = {c for c in vocab if c.isalpha()}
        
        # candidates dictionary will contain a set of all available tokens to search
        candidate_dict = dict().fromkeys(char_set, 0)
        
        # occurrences will contain all matched tokens and the count, how many times the token has been found.
        token_occurrences = OrderedDict()
        while len(vocab) < self.vocab_size:
            for candidate in candidate_dict.keys():
                occurrences = data.count(candidate)
                candidate_dict[candidate] = occurrences

            candidate_dict = {candidate: count for candidate, count in candidate_dict.items() if count}
            vocab.update(set(candidate_dict.keys()))
            token_occurrences.update(candidate_dict)

            # build new candidates
            temp_candidate_set = set()
            for char in char_set:
                # don't test candidates with occurency <= 2. New candidates won't have occurency higher than 2
                temp_candidate_set.update({candidate + char for candidate in candidate_dict.keys() if token_occurrences[candidate] > 2})

            candidate_dict = dict().fromkeys(temp_candidate_set, 0)

        tokens_to_remove = len(vocab) - self.vocab_size
        token_occurrences = OrderedDict(sorted(token_occurrences.items(), key=lambda x: x[1], reverse=True))
        for _ in range(tokens_to_remove):
            token, _ = token_occurrences.popitem()
            vocab.remove(token)

        sorted_vocab = self.sort_vocab(vocab)
        
        # add a special token for unknown tokens
        sorted_vocab.append('<unk>')
        self.vocab_size += 1 # plus <unk> special token
        
        return sorted_vocab
    
    def tokenize(self, data, block_size):
        for token in self.vocab:
            data = data.replace(token, f'#{self.stoi[token]}#')

        # If everything went well, first and last characters won't have # pair. Need to trim them
        data = data[1:-1]
        # Split by ## pairs
        tokenized_text = data.split('##')
        # Filter empty strings
        tokenized_text = [x for x in tokenized_text if x]
        result = []
        for tokenized in tokenized_text:
            # In case other single # found, replace them with <unk> special token, marking the element as unknown
            if '#' in tokenized:
                for unknown_candidate in tokenized.split('#'):
                    if unknown_candidate.isnumeric():
                        result.append(self.itos[int(unknown_candidate)])
                    else:
                        result.append('<unk>')
            else:
                result.append(self.itos[int(tokenized)])

        # all texts should have equal size. We can make text length equal by filling text with spaces
        for _ in range(block_size - len(result)):
            result.append(' ')
            
        # in case the sentence is longer, than block_size, we trim the sentence
        return result[:block_size]
    
    def encode(self, data):
        return [self.stoi[s] for s in data]
    
    def decode(self, data):
        return ''.join([self.itos[int(i)] for i in data])


# from cmu dict
def pronounce(word):
  try:
	 syllables = [list(y[:-1].lower() if y[-1].isdigit() else y.lower() for y in x ) for x in d[word.lower()]] 
  except KeyError:
	 syllables = [x.lower() for x in predict(word)]

  return syllables
def get_pronounce(sentence):
  return [pronounce(x)[0] for x in list(sentence.split())]


def vovel_check(syllable):
  vovels = ['a', 'e', 'i', 'o', 'u']
  for i in syllable:
    if i in vovels:
      return True
  return False


def get_index(hand_shape,pos):
   return ((hand_shape -1) * 8) + pos


def find_hand_shape(handshapes,s):
  # Code to find the handshape of the syllable 
  for item in handshapes:
    if s in handshapes[item]:
      return int(item)
  raise ValueError(*s)


def find_pos(positions,s):
  # Code to find the position of the syllable 
  for item in positions:
    if s in positions[item]:
      return int(item)
  raise ValueError(*s)


def cued_speech(text):
  
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
  
  """
  output format:
  output = {
     'lenth': length,
     'word': {'0': idx1, '1': idx2, '2': idx3 ..... }
          }
  """

  syllable = get_pronounce(text)
  output = {}
  output['word'] = {}
  
  for word in syllable: 
    for i in range(len(word)):

      if i != (len(word)-1):
        # Rule 1: Consonent sound on its own no vovel after it
        if not vovel_check(word[i])  and not vovel_check(word[i+1]):
          # cued in the side position
          pos = 4
          hand_shape = find_hand_shape(handshapes,word[i])
          output['word'][f'{i}'] = get_index(hand_shape,pos)

        # Rule 3: consonent folowed by a vovel
        if not vovel_check(word[i]) and vovel_check(word[i+1]):
          hand_shape = find_hand_shape(handshapes,word[i])
          pos = find_pos(positions,word[i+1])
          output['word'][f'{i}'] = get_index(hand_shape,pos)
          output['word'][f'{i+1}'] = output['word'][f'{i}'] 

          continue
      else:
        if not vovel_check(word[i]):
          pos = 4
          hand_shape = find_hand_shape(handshapes,word[i])
          output['word'][f'{i}'] = get_index(hand_shape,pos)

      
      if i != 0:
        # Rule 2: vovel on its own without a consonent before it or at the start of the word
        if vovel_check(word[i]) and vovel_check(word[i-1]):
          hand_shape = 5
          pos = find_pos(positions,word[i])
          output['word'][f'{i}'] = get_index(hand_shape,pos)
      if i == 0 and vovel_check(word[i]):
        hand_shape = 5
        pos = find_pos(positions,word[i])
        output['word'][f'{i}'] = get_index(hand_shape,pos)


  return output
