#############################################
#This script includes a number of functions 
#for measuring the behavior of a feed-forward 
#LSTM with two layers.
#############################################

import math
import glob
import sys
import warnings 
warnings.filterwarnings("ignore") #wild
import torch
import torch.nn as nn
import data_test
import data

#set device to cpu for work on desktop :/
device = torch.device('cpu')

#set loss function to be cross entropy
criterion = nn.CrossEntropyLoss()

#### Information theory stuff ###
def get_entropy(state):
    ''' Compute entropy of input vector '''
    # requirments: state should be a vector scoring possible classes
    # returns scalar

    #get probabilities of outputs
    probs = nn.functional.softmax(state, dim=0)
    #get log probs
    logprobs = nn.functional.log_softmax(state, dim=0)
    #entropy is sum over i, -prob(i)*logprob(i)
    prod = probs.data * logprobs.data
    #set nans to zero
    prod[prod != prod] = 0

    return torch.Tensor([-1 * torch.sum(prod)]).to(device)

def get_surps(state):
    ''' Compute surprisal for each element in vector '''
    #Get log prob of softmax layer, so this will be vector
    #of surprisals for given output
    logprobs = nn.functional.log_softmax(state, dim=0)
    return -1 * logprobs

#return word, surp, H for each word in state
def get_IT(state, obs, corpus):

    metrics = []
    #get entropies and put into shannons 
    Hs = torch.log2(torch.exp(torch.squeeze(apply(get_entropy, state))))
    #get surprisals and put into shannons 
    surps = torch.log2(torch.exp(apply(get_surps, state)))

    for corpuspos, targ in enumerate(obs):
        #get word 
        word = corpus.dictionary.idx2word[int(targ)]
        if word == "<eos>":
            #skip over EOS
            continue
        #Get surprisal of target at time step 
        surp = float(surps[corpuspos][int(targ)].data)
        #Get entropy at time step
        H = float(Hs[corpuspos])
        metrics.append((word, surp, H))
    return metrics

#other helpers
def test_get_batch(source):
    ''' Creates an input/target pair for evaluation '''
    seq_len = len(source) - 1
    #Get all words except last one
    data = source[:seq_len]
    #Get all targets
    target = source[1:1+seq_len].view(-1)
    return data, target

def repackage_hidden(in_state):
    if isinstance(in_state, torch.Tensor):
        return in_state.detach()
    else:
        return tuple(repackage_hidden(value) for value in in_state)

def apply(func, apply_dimension):
    output_list = [func(m) for m in torch.unbind(apply_dimension, dim=0)]
    return torch.stack(output_list, dim=0)

def test_IT(data_source, corpus, model):
    ''' Given a list of one hot encoded data, return information theoretic measures '''

    model.eval()

    total_loss = 0.

    #Get vocab size for beam
    ntokens = len(corpus.dictionary)

    #For each sent
    values = []
    for i in range(len(data_source)):
        sent_ids = data_source[i].to(device)
        hidden = model.init_hidden(1)

        data, targets = test_get_batch(sent_ids)

        data = data.unsqueeze(1)

        output, hidden = model(data, hidden)
        output_flat = output.view(-1, ntokens)
        metrics = get_IT(output_flat, targets, corpus)
        values.append(metrics)
    return values

def run_experiment(version, vocab_file, model_files,
        multisent_flag = True, verbose=True):
    ''' Given an experiment version (def|ref|temp), 
    model vocabulary file and model files
    return information theoretic measures'''

    #hard code data_dir
    data_path = './'

    #set loss function to be cross entropy
    criterion = nn.CrossEntropyLoss()

    #Load experimental stim
    EXP = data.Stim(version)

    #Loop through the models
    for model_file in model_files:
        if verbose:
            print('running experiment:', version, 'testing model:', model_file)

        #load the model
        with open(model_file, 'rb') as f:
            #run on local cpu for now
            model = torch.load(f, map_location='cpu')

            # make in continous chunk of memory for speed
            if isinstance(model, torch.nn.DataParallel):
                model = model.module
            model.rnn.flatten_parameters()

        #loop through experimental items for EXP
        for x in range(len(EXP.SENTS)):
            sentences = list(EXP.SENTS[x])

            #Create corpus wrapper (this is for one hoting data)
            corpus = data_test.TestSent(data_path, vocab_file, 
                    sentences, multisent_flag)
            #Get one hots
            sent_ids = corpus.get_data()

            values = test_IT(sent_ids, corpus, model)

            EXP.load_IT(model_file, x, values, multisent_flag)

    return EXP
