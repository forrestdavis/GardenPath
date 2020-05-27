#############################################
#This script includes a loading function and 
#class structure for formatting data for 
#garden path experiments.
#############################################
import pandas as pd
import numpy as np

class Stim:

    def __init__(self, version):

        #Pairs of sentences
        self.SENTS = []
        #Target words for pairs
        self.TARGET_WORDS = []
        #Target indices for pairs
        self.TARGET_IDX = []
        
        #Extract target info
        if version == 'def':
            self.create_def_exp()
        elif version == 'ref':
            self.create_ref_exp()
        elif version == 'temp':
            self.create_temp_exp()

        self.SURPS = {}
        self.dataframe = None

    def save_excel(self, fname):

        fname = fname.split('.')[0]+'.xlsx'

        if self.dataframe is None:
            self.create_df()

        self.dataframe.to_excel(fname, index=False)

    def save_csv(self, fname):
        fname = fname.split('.')[0]+'.csv'

        if self.dataframe is None:
            self.create_df()

        self.dataframe.to_csv(fname, index=False)

    def create_df(self):
        pass

    def load_IT(self, model_name, target_idx, values, multisent_flag=True):
        
        target_words = self.TARGET_WORDS[target_idx]
        target_idxs = self.TARGET_IDX[target_idx]

        #print(target_words)

        #split values into seperate sentences
        if multisent_flag:
            vs = []
            values = values[0]
            value = []
            for v in values:
                value.append(v)
                if v[0] == '.':
                    vs.append(value)
                    value = []
            values = vs

        #print(values)

        target = values[-1]
        print(target)
        print(target_words)
        print(target_idxs)
        surps = []
        for x in range(len(target_words)):
            t_word = target_words[x]
            t_idx = target_idxs[x]

            assert t_word == target[t_idx][0]

            surps.append(target[t_idx][1])

        print(surps)
        assert len(surps) != 0

        if model_name not in self.SURPS:
            self.SURPS[model_name] = []

        self.SURPS[model_name].append(surps)

    #Create definite experiment test sentences
    #save them in SENTS and save targets
    def create_def_exp(self):

        data_path = 'stimuli/Definite/'

        New_data = open(data_path+'New', 'r')
        Old_data = open(data_path+'Old', 'r')
        DefAmbi_data = open(data_path+'DefAmbi', 'r')
        DefUnambi_data = open(data_path+'DefUnambi', 'r')
        IndefAmbi_data = open(data_path+'IndefAmbi', 'r')
        IndefUnambi_data = open(data_path+'IndefUnambi', 'r')
        Regions_data = open(data_path+'Regions', 'r')

        #Load in data
        data = {}
        data['New'] = []
        for line in New_data:
            line = line.strip()
            data['New'].append(line)
        New_data.close()

        data['Old'] = []
        for line in Old_data:
            line = line.strip()
            data['Old'].append(line)
        Old_data.close()

        data['DefAmbi'] = []
        for line in DefAmbi_data:
            line = line.strip()
            data['DefAmbi'].append(line)
        DefAmbi_data.close()

        data['IndefAmbi'] = []
        for line in IndefAmbi_data:
            line = line.strip()
            data['IndefAmbi'].append(line)
        IndefAmbi_data.close()

        data['DefUnambi'] = []
        for line in DefUnambi_data:
            line = line.strip()
            data['DefUnambi'].append(line)
        DefUnambi_data.close()

        data['IndefUnambi'] = []
        for line in IndefUnambi_data:
            line = line.strip()
            data['IndefUnambi'].append(line)
        IndefUnambi_data.close()

        data['Regions'] = []
        for line in Regions_data:
            line = line.strip()
            data['Regions'].append(line)
        Regions_data.close()

        target_words = []
        sents = []
        target_idxs = []
        for i in range(len(data['New'])):
            num = str(i+1)
            region = data['Regions'][i]
            new = data['New'][i]
            old = data['Old'][i]
            IndefAmbi = data['IndefAmbi'][i]
            DefAmbi = data['DefAmbi'][i]
            IndefUnambi = data['IndefUnambi'][i]
            DefUnambi = data['DefUnambi'][i]

            t_words = region.split(' ')

            #New+IndefAmbi
            t_idxs = self.find_def_target(t_words, IndefAmbi)
            sent = [new, IndefAmbi]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #Old+DefAmbi
            t_idxs = self.find_def_target(t_words, DefAmbi)
            sent = [old, DefAmbi]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #New+DefAmbi
            t_idxs = self.find_def_target(t_words, DefAmbi)
            sent = [new, DefAmbi]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #New+IndefUnambi
            t_idxs = self.find_def_target(t_words, IndefUnambi)
            sent = [new, IndefUnambi]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #Old+DefUnambi
            t_idxs = self.find_def_target(t_words, DefUnambi)
            sent = [old, DefUnambi]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #New+DefUnambi
            t_idxs = self.find_def_target(t_words, DefUnambi)
            sent = [new, DefUnambi]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

        self.SENTS = sents
        self.TARGET_WORDS = target_words
        self.TARGET_IDX = target_idxs

    def find_def_target(self, t_words, sent):

        sent = sent.split(' ')
        count = 0
        t_idxs = []
        for x in range(len(sent)):
            word = sent[x]
            if count > len(t_words)-1:
                break
            if word == t_words[count]:
                count += 1
                t_idxs.append(x)

        return t_idxs

    #Create referential experiment test sentences, and 
    #set targets
    def create_ref_exp(self):

        data_path = 'stimuli/Referential/'

        one_NP_data = open(data_path+'1NP', 'r')
        two_NP_data = open(data_path+'2NP', 'r')
        Reduced_data = open(data_path+'Reduced', 'r')
        Unreduced_data = open(data_path+'Unreduced', 'r')

        #Load in data
        data = {}
        data['1NP'] = []
        for line in one_NP_data:
            line = line.strip()
            data['1NP'].append(line)
        one_NP_data.close()

        data['2NP'] = []
        for line in two_NP_data:
            line = line.strip()
            data['2NP'].append(line)
        two_NP_data.close()

        data['Reduced'] = []
        for line in Reduced_data:
            line = line.strip()
            data['Reduced'].append(line)
        Reduced_data.close()

        data['Unreduced'] = []
        for line in Unreduced_data:
            line = line.strip()
            data['Unreduced'].append(line)
        Unreduced_data.close()

        sents = []
        target_words = []
        target_idxs = []
        for i in range(len(data['1NP'])):
            one = data['1NP'][i]
            two = data['2NP'][i]
            reduced = data['Reduced'][i]
            unreduced = data['Unreduced'][i]

            #1NP + Reduced
            sent = [one, reduced]
            t_words = reduced.split(' ')[2:8]
            t_idxs = list(range(2, 8))
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #2NP + Reduced
            sent = [two, reduced]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #1NP + Unreduced
            sent = [one, unreduced]
            t_words = unreduced.split(' ')[4:10]
            t_idxs = list(range(4, 10))
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #2NP + Unreduced
            sent = [two, unreduced]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

        self.SENTS = sents
        self.TARGET_WORDS = target_words
        self.TARGET_IDX = target_idxs

    #Create temporal experiment test sentences
    #and get targets
    def create_temp_exp(self):

        data_path = 'stimuli/Temporal/'

        Future_data = open(data_path+'Future', 'r')
        Past_data = open(data_path+'Past', 'r')
        Reduced_data = open(data_path+'Reduced', 'r')
        Unreduced_data = open(data_path+'Unreduced', 'r')

        #Load in data
        data = {}
        data['Future'] = []
        for line in Future_data:
            line = line.strip()
            data['Future'].append(line)
        Future_data.close()

        data['Past'] = []
        for line in Past_data:
            line = line.strip()
            data['Past'].append(line)
        Past_data.close()

        data['Reduced'] = []
        for line in Reduced_data:
            line = line.strip()
            data['Reduced'].append(line)
        Reduced_data.close()

        data['Unreduced'] = []
        for line in Unreduced_data:
            line = line.strip()
            data['Unreduced'].append(line)
        Unreduced_data.close()

        sents = []
        target_words = []
        target_idxs = []
        for i in range(len(data['Past'])):
            past = data['Past'][i]
            future = data['Future'][i]
            reduced = data['Reduced'][i]
            unreduced = data['Unreduced'][i]

            #Past + Reduced
            sent = [past, reduced]
            t_words = reduced.split(' ')[2:8]
            t_idxs = list(range(2, 8))
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #Future + Reduced
            sent = [future, reduced]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #Past + Unreduced
            sent = [past, unreduced]
            t_words = unreduced.split(' ')[4:10]
            t_idxs = list(range(4, 10))
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

            #Future + Unreduced
            sent = [future, unreduced]
            sents.append(sent)
            target_words.append(t_words)
            target_idxs.append(t_idxs)

        self.SENTS = sents
        self.TARGET_WORDS = target_words
        self.TARGET_IDX = target_idxs

if __name__ == "__main__":

    #stimf = 'stimuli/The_boy_will_bounce_the_ball.xlsx'
    EXP = Stim('temp')
