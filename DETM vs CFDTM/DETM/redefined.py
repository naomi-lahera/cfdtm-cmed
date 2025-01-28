from topmost.models.dynamic.DETM import DETM
import torch
from torch import nn
import torch.nn.functional as F

import numpy as np
from topmost import eva
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel
from topmost.data.file_utils import split_text_word

class DETMFixed(DETM):
    def __init__(self, vocab_size, num_times, train_size, train_time_wordfreq, num_topics=50, train_WE=True, pretrained_WE=None, en_units=800, eta_hidden_size=200, rho_size=300, enc_drop=0.0, eta_nlayers=3, eta_dropout=0.0, delta=0.005, theta_act='relu', device='cpu'):
        super().__init__(vocab_size, num_times, train_size, train_time_wordfreq, num_topics, True, pretrained_WE, en_units, eta_hidden_size, rho_size, enc_drop, eta_nlayers, eta_dropout, delta, theta_act, device)
        
        ## define the word embedding matrix \rho
        if not self.train_WE:
            rho = nn.Embedding(pretrained_WE.shape[1], pretrained_WE.shape[0])
            rho.weight.data = torch.from_numpy(pretrained_WE)
            self.rho = rho.weight.data.clone().float().to(self.device)
            
def get_theta_redefined(self, bows, times, eta=None): ## amortized inference
        """Returns the topic proportions.
        """
        # normalized_bows = bows / bows.sum(1, keepdims=True)
        # print("🍀 Before", normalized_bows)

        normalized_bows = bows / (bows.sum(1, keepdims=True) + 1e-12)
        # print("🍀 After", normalized_bows)
    
        if eta is None and self.training is False:
            eta, kl_eta = self.get_eta(self.rnn_inp)

        eta_td = eta[times]
        inp = torch.cat([normalized_bows, eta_td], dim=1)
        q_theta = self.q_theta(inp)
        if self.enc_drop > 0:
            q_theta = self.t_drop(q_theta)
        mu_theta = self.mu_q_theta(q_theta)
        logsigma_theta = self.logsigma_q_theta(q_theta)
        z = self.reparameterize(mu_theta, logsigma_theta)
        theta = F.softmax(z, dim=-1)
        kl_theta = self.get_kl(mu_theta, logsigma_theta, eta_td, torch.zeros(self.num_topics).to(self.device))

        if self.training:
            return theta, kl_theta
        else:
            return theta
        
def _coherence_modified(reference_corpus, vocab, top_words, cv_type='c_v'):
    print('🍀')
    
    split_top_words = split_text_word(top_words)
    num_top_words = len(split_top_words[0])
    for item in split_top_words:
        assert num_top_words == len(item)

    split_reference_corpus = split_text_word(reference_corpus)
    dictionary = Dictionary(split_text_word(vocab))

    #print(f"Corpus size: {len(split_reference_corpus)}")
    #print(f"Dictionary size: {len(dictionary)}")
    #print(f"Top words: {split_top_words}")

    #print(type(split_reference_corpus[0]))
    #print(type(reference_corpus[0]))

    cm = CoherenceModel(texts=split_reference_corpus, dictionary=dictionary, topics=split_top_words, topn=num_top_words, coherence=cv_type)
    cv_per_topic = cm.get_coherence_per_topic()
    # print(f"Coherence scores per topic: {cv_per_topic}")

    valid_scores = [score for score in cv_per_topic if not np.isnan(score)]
    if not valid_scores:
        raise ValueError("All coherence scores are NaN.")
    score = np.mean(valid_scores)

    return score