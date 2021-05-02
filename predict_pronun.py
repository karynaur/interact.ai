import logging
from mingpt.utils import set_seed
import urllib
import re
import random
import numpy as np
import torch
import torch.nn as nn
from torch.nn import functional as F
from mingpt.model import GPT, GPTConfig
from collections import OrderedDict, Counter
import os
from mingpt.utils import sample

set_seed(42)

logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s -   %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        level=logging.INFO,

)
def predict(word):
  block_size = 200

  tok_data = torch.load('models/tok_data.pt',map_location = torch.device('cpu'))
  tok_tar = torch.load('models/tok_tar.pt', map_location = torch.device('cpu'))


  mconf = GPTConfig(tok_tar.vocab_size, block_size,
                    n_layer=2, n_head=4, n_embd=512)
  model = GPT(mconf)
  model.load_state_dict(torch.load('models/model (1).pt', map_location = torch.device('cpu')))
#  model = torch.load('models/pronunciation.pt', map_location = torch.device('cpu'))
  model.eval()
  x = torch.tensor(tok_data.encode(tok_data.tokenize(word, block_size)), dtype=torch.long)[None,...]
  y = sample(model, x, block_size, temperature=1.0, sample=True, top_k=10)[0]

  predicted = y[block_size:]
  return str(tok_tar.decode(predicted)).replace('\n','')

