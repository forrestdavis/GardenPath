import sys
import glob
import os

class Stimulus:

    def __init__(self, exp, data_type, model_num, stim_num):

        self.exp = exp 
        self.data_type = data_type
        self.context_types = []
        #1 Surp child per context type
        self.surps = []
        self.model_num = model_num
        self.stim_num = stim_num
        self.datafname = ''

class Surp: 

    def __init__(self):

        self.sent = ''
        self.words = []
        self.words_surps = []
        self.regions = []
        self.regions_surps = []


    def load_surp(self, data):

        last_word = []

        for x in range(len(data)):
            d = data[x]
            self.words.append(d[0])
            self.words_surps.append(float(d[4]))

            #Ignore final '.' and group in bigrams
            if x%2==1 and x!=len(data)-1:
                self.regions.append([last_word[0], d[0]])
                self.regions_surps.append([float(last_word[4]), float(d[4])])

            #There is one final region with only 1 member
            elif (len(data)-1)%2 == 1 and x==len(data)-1:
                self.regions.append([last_word[0]])
                self.regions_surps.append([float(last_word[4])])

            last_word = d

        self.sent = ' '.join(self.words)

        #For morpho
        region_one = [data[2][0], data[3][0], data[4][0]]
        region_two = [data[5][0], data[6][0], data[7][0]]
        self.regions[1] = region_one
        self.regions[2] = region_two
        region_one_surp = [float(data[2][4]), float(data[3][4]), float(data[4][4])]
        region_two_surp = [float(data[5][4]), float(data[6][4]), float(data[7][4])]
        self.regions_surps[1] = region_one_surp
        self.regions_surps[2] = region_two_surp

        return

def load_ref_exp():

    CONTEXTS = ['1NP+Reduced', '2NP+Reduced', '1NP+Unreduced', '2NP+Unreduced']
    stimuli = []

    #0-4 are models trained on ordered data
    #5-9 are models trained on shuffled data
    for modelNum in range(0,10):
        dataType = 'ordered'
        if modelNum > 4 and modelNum < 10:
            dataType = 'shuffled'

        path = 'measures/garden_path/ref/'+str(modelNum)+'/'

        files = glob.glob(path+'*')

        #Get number of stimuli
        num_stim = max(list(map(lambda x: int(x.split('_')[-2]), files)))

        #Generate results
        for i in range(num_stim):
            stimulus = Stimulus('ref', dataType, modelNum, i+1)
            #Save context labels to stimulus
            stimulus.context_types = CONTEXTS.copy()
            num = str(i+1)
            #Get files per stimulus
            result_files = list(filter(lambda x: x.split('_')[-2]==num, files))
            result_files.sort()
            #Read in suprisals
            for result_file in result_files:

                #Save filename
                stimulus.datafname = result_file[:-2]

                data = open(result_file, 'r')
                data.readline()
                sentence = []
                last_sentence = []
                for line in data:
                    line = line.strip().split()
                    sentence.append(line)
                    if line[0] == '.':
                        last_sentence = sentence.copy()
                        sentence = []
                #Only load surprisals for target sentence (last sentence)
                surp = Surp()
                surp.load_surp(last_sentence)
                stimulus.surps.append(surp)

            stimuli.append(stimulus)
    return stimuli

def load_exp(modelNum, exp_name, models_dir):

    CONTEXTS = ['1NP+Reduced', '2NP+Reduced', '1NP+Unreduced', '2NP+Unreduced']
    stimuli = []

    #0-4 are models trained on ordered data
    #5-9 are models trained on shuffled data
    #for modelNum in range(0,10):
    if modelNum == 'all':
        modelNums = range(len(glob.glob(models_dir+'*.pt')))
    else:
        modelNums = [modelNum]

    for modelNum in modelNums:
        dataType = 'ordered'
        #if modelNum > 4 and modelNum < 10:
        #    dataType = 'shuffled'

        path = 'measures/morpho/'+exp_name+'/'+str(modelNum)+'/'

        files = glob.glob(path+'*')

        #Get number of stimuli
        num_stim = max(list(map(lambda x: int(x.split('_')[-2]), files)))

        #Generate results
        for i in range(num_stim):
            stimulus = Stimulus(exp_name, dataType, modelNum, i+1)
            #Save context labels to stimulus
            stimulus.context_types = CONTEXTS.copy()
            num = str(i+1)
            #Get files per stimulus
            result_files = list(filter(lambda x: x.split('_')[-2]==num, files))
            result_files.sort()
            #Read in suprisals
            for result_file in result_files:

                #Save filename
                stimulus.datafname = result_file[:-2]

                data = open(result_file, 'r')
                data.readline()
                sentence = []
                last_sentence = []
                for line in data:
                    line = line.strip().split()
                    sentence.append(line)
                    if line[0] == '.':
                        last_sentence = sentence.copy()
                        sentence = []
                #Only load surprisals for target sentence (last sentence)
                surp = Surp()
                surp.load_surp(last_sentence)
                stimulus.surps.append(surp)

            stimuli.append(stimulus)
    return stimuli

def load_con_exp():

    CONTEXTS = ['1NP+Reduced', '2NP+Reduced', '1NP+Unreduced', '2NP+Unreduced']
    stimuli = []

    #0-4 are models trained on ordered data
    #5-9 are models trained on shuffled data
    #for modelNum in range(0,10):
    modelNums = [0,5]
    for modelNum in modelNums:
        dataType = 'ordered'
        if modelNum > 4 and modelNum < 10:
            dataType = 'shuffled'

        path = 'measures/garden_path/con/'+str(modelNum)+'/'

        files = glob.glob(path+'*')

        #Get number of stimuli
        num_stim = max(list(map(lambda x: int(x.split('_')[-2]), files)))

        #Generate results
        for i in range(num_stim):
            stimulus = Stimulus('con', dataType, modelNum, i+1)
            #Save context labels to stimulus
            stimulus.context_types = CONTEXTS.copy()
            num = str(i+1)
            #Get files per stimulus
            result_files = list(filter(lambda x: x.split('_')[-2]==num, files))
            result_files.sort()
            #Read in suprisals
            for result_file in result_files:

                #Save filename
                stimulus.datafname = result_file[:-2]

                data = open(result_file, 'r')
                data.readline()
                sentence = []
                last_sentence = []
                for line in data:
                    line = line.strip().split()
                    sentence.append(line)
                    if line[0] == '.':
                        last_sentence = sentence.copy()
                        sentence = []
                #Only load surprisals for target sentence (last sentence)
                surp = Surp()
                surp.load_surp(last_sentence)
                stimulus.surps.append(surp)

            stimuli.append(stimulus)
    return stimuli

def load_temp_exp():

    CONTEXTS = ['Past+Reduced', 'Future+Reduced', 'Past+Unreduced', 'Future+Unreduced']
    stimuli = []

    for modelNum in range(5):
    #modelNum = 10
    #for modelNum in range(5, 10):
        path = 'stimuli/out_files/temp/'+str(modelNum)+'/'

        files = glob.glob(path+'*')

        #Get number of stimuli
        num_stim = max(list(map(lambda x: int(x.split('_')[-2]), files)))
        #Get number of sentences per frame
        num_sents = max(list(map(lambda x: int(x.split('_')[-1]), files)))+1

        #Generate results
        for i in range(num_stim):
            stimulus = Stimulus('temp')
            stimulus.context_types = CONTEXTS.copy()
            num = str(i+1)
            result_files = list(filter(lambda x: x.split('_')[-2]==num, files))
            for result_file in result_files:

                data = open(result_file, 'r')
                data.readline()
                sentence = []
                last_sentence = []
                for line in data:
                    line = line.strip().split()
                    sentence.append(line)
                    if line[0] == '.':
                        last_sentence = sentence.copy()
                        sentence = []
                surp = Surp()
                surp.load_surp(last_sentence)
                stimulus.surps.append(surp)

            stimuli.append(stimulus)
    return stimuli

def load_def_exp():

    CONTEXTS = ['New+IndefAmbi', 'Old+DefAmbi', 'New+DefAmbi', 
                'New+IndefUnambi', 'Old+DefUnambi', 'New+DefUnambi']
    stimuli = []

    #for modelNum in range(5):
    #modelNum = 10
    for modelNum in range(5, 10):
        path = 'stimuli/out_files/def/'+str(modelNum)+'/'

        files = glob.glob(path+'*')

        #Get number of stimuli
        num_stim = max(list(map(lambda x: int(x.split('_')[-2]), files)))
        #Get number of sentences per frame
        num_sents = max(list(map(lambda x: int(x.split('_')[-1]), files)))+1

        #Generate results
        for i in range(num_stim):
            stimulus = Stimulus('def')
            stimulus.context_types = CONTEXTS.copy()
            num = str(i+1)
            result_files = list(filter(lambda x: x.split('_')[-2]==num, files))
            for result_file in result_files:

                data = open(result_file, 'r')
                data.readline()
                sentence = []
                last_sentence = []
                for line in data:
                    line = line.strip().split()
                    sentence.append(line)
                    if line[0] == '.':
                        last_sentence = sentence.copy()
                        sentence = []
                surp = Surp()
                surp.load_surp(last_sentence)
                stimulus.surps.append(surp)

            stimuli.append(stimulus)
    return stimuli

def get_temp_roi(stimuli_list):

    #Get each set of 4 test sentences

    regions = {}
    regions['contexts'] = {}
    regions['verb_by'] = []
    regions['NP'] = []
    regions['RR'] = []
    for stim in stimuli_list:
        verb_bys = []
        NPs = []
        RRs = []
        for i in range(len(stim.surps)):
            context = stim.context_types[i]
            if context not in regions['contexts']:
                regions['contexts'][context] = i
            surprisal = stim.surps[i]

            #Get verb+by region and NP region
            verb_by = surprisal.regions_surps[1]
            NP = surprisal.regions_surps[2]

            #If unreduced this is shifted over by one region
            if 'Unreduced' in context:
                verb_by = surprisal.regions_surps[2]
                NP = surprisal.regions_surps[3]

            verb_bys.append(sum(verb_by))
            NPs.append(sum(NP))
            RRs.append(sum(verb_by)+sum(NP))

        regions['verb_by'].append(verb_bys)
        regions['NP'].append(NPs)
        regions['RR'].append(RRs)

    return regions

def get_def_roi(stimuli_list):

    regions = {}
    regions['contexts'] = {}
    regions['critical'] = []

    #Get regions of interest file
    critical_regions = []
    critical_list = open('stimuli/Definite/Regions','r')
    for line in critical_list:
        line = line.strip()
        critical_regions.append(line)
    critical_list.close()

    #Go through stimuli list
    j = 0
    for stim in stimuli_list:
        critical_rois = []
        subset_words = critical_regions[j].split()
        j+=1
        #Reset if into next model
        if j == len(critical_regions):
            j = 0
        for i in range(len(stim.surps)):
            context = stim.context_types[i]
            if context not in regions['contexts']:
                regions['contexts'][context] = i
            surprisal = stim.surps[i]
            words = surprisal.words
            indices = get_word_subset_index(words, subset_words.copy())
            roi = [surprisal.words_surps[index] for index in indices]
            critical_rois.append(sum(roi))
        regions['critical'].append(critical_rois)
    return regions

def get_word_subset_index(words, subset_words):

    indices = []
    for i in range(len(words)):
        word = words[i] 
        if len(subset_words)==0:
            break
        if word == subset_words[0]:
            subset_words.pop(0)
            indices.append(i)

    #Found substring
    assert len(subset_words)==0

    return indices

def get_ref_csv(stimuli):

    path = 'results/ref/'
    HEADER = 'exp,model_type,condition,model_num,stim_num,datfname,region,context,surp'

    one_two_out_str = HEADER + '\n'
    reduced_unreduced_str = HEADER + '\n'
    for stim in stimuli:
        #reduced surprisals
        oneNPR = 0
        twoNPR = 0
        #unreduced surprisals
        oneNPU = 0 
        twoNPU = 0
        index = 0
        for context in stim.context_types:
            if '1NP' in context and 'Reduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[1])
                oneNPR = verb_by
            if '2NP' in context and 'Reduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[1])
                twoNPR = verb_by
            if '1NP' in context and 'Unreduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[2])
                oneNPU = verb_by
            if '2NP' in context and 'Unreduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[2])
                twoNPU = verb_by
            index += 1

        one_two_NPR = oneNPR-twoNPR
        one_two_NPU = oneNPU-twoNPU

        #Add one minus two for reduced
        one_two_out_str += 'ref,'+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        one_two_out_str += stim.datafname+',vp+by,one-twoNP,'+str(one_two_NPR) + '\n'
        #Add one minus two for unreduced
        one_two_out_str += 'ref,'+stim.data_type+',unreduced'+str(stim.model_num)+','+str(stim.stim_num)+','
        one_two_out_str += stim.datafname+',vp+by,one-twoNP,'+str(one_two_NPU) + '\n'

        #Add oneNP reduced
        reduced_unreduced_str += 'ref,'+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,oneNP,'+str(oneNPR)+'\n'
        #Add twoNP reduced
        reduced_unreduced_str += 'ref,'+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,twoNP,'+str(twoNPR)+'\n'
        #Add oneNP unreduced
        reduced_unreduced_str += 'ref,'+stim.data_type+',unreduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,oneNP,'+str(oneNPU)+'\n'
        #Add twoNP unreduced
        reduced_unreduced_str += 'ref,'+stim.data_type+',unreduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,twoNP,'+str(twoNPU)+'\n'

    out = open(path+'ordered_shuffled_one-two.csv', 'w')
    out.write(one_two_out_str)
    out.close()

    out = open(path+'ordered_shuffled_reduced_unreduced.csv', 'w')
    out.write(reduced_unreduced_str)
    out.close()

    return

def get_csv(stimuli, exp_name):

    path = 'results/morpho/'+exp_name+'/'
    if not os.path.isdir(path):
        os.mkdir(path)
    HEADER = 'exp,model_type,condition,model_num,stim_num,datfname,region,context,surp'

    one_two_out_str = HEADER + '\n'
    reduced_unreduced_str = HEADER + '\n'
    for stim in stimuli:
        #reduced surprisals
        oneNPR = 0
        twoNPR = 0
        #unreduced surprisals
        oneNPU = 0 
        twoNPU = 0
        index = 0
        for context in stim.context_types:
            if '1NP' in context and 'Reduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[1])
                oneNPR = verb_by
            if '2NP' in context and 'Reduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[1])
                twoNPR = verb_by
            if '1NP' in context and 'Unreduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[2])
                oneNPU = verb_by
            if '2NP' in context and 'Unreduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[2])
                twoNPU = verb_by
            index += 1

        one_two_NPR = oneNPR-twoNPR
        one_two_NPU = oneNPU-twoNPU

        #Add one minus two for reduced
        one_two_out_str += exp_name+','+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        one_two_out_str += stim.datafname+',vp+by,one-twoNP,'+str(one_two_NPR) + '\n'
        #Add one minus two for unreduced
        one_two_out_str += exp_name+','+stim.data_type+',unreduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        one_two_out_str += stim.datafname+',vp+by,one-twoNP,'+str(one_two_NPU) + '\n'

        #Add oneNP reduced
        reduced_unreduced_str += exp_name+','+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,oneNP,'+str(oneNPR)+'\n'
        #Add twoNP reduced
        reduced_unreduced_str += exp_name+','+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,twoNP,'+str(twoNPR)+'\n'
        #Add oneNP unreduced
        reduced_unreduced_str += exp_name+','+stim.data_type+',unreduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,oneNP,'+str(oneNPU)+'\n'
        #Add twoNP unreduced
        reduced_unreduced_str += exp_name+','+stim.data_type+',unreduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,twoNP,'+str(twoNPU)+'\n'

    out = open(path+'ordered_shuffled_one-two.csv', 'w')
    out.write(one_two_out_str)
    out.close()

    out = open(path+'ordered_shuffled_reduced_unreduced.csv', 'w')
    out.write(reduced_unreduced_str)
    out.close()

    return

def get_con_csv(stimuli):

    path = 'results/con/'
    HEADER = 'exp,model_type,condition,model_num,stim_num,datfname,region,context,surp'

    one_two_out_str = HEADER + '\n'
    reduced_unreduced_str = HEADER + '\n'
    for stim in stimuli:
        #reduced surprisals
        oneNPR = 0
        twoNPR = 0
        #unreduced surprisals
        oneNPU = 0 
        twoNPU = 0
        index = 0
        for context in stim.context_types:
            if '1NP' in context and 'Reduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[1])
                oneNPR = verb_by
            if '2NP' in context and 'Reduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[1])
                twoNPR = verb_by
            if '1NP' in context and 'Unreduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[2])
                oneNPU = verb_by
            if '2NP' in context and 'Unreduced' in context:
                surprisal = stim.surps[index]
                verb_by = sum(surprisal.regions_surps[2])
                twoNPU = verb_by
            index += 1

        one_two_NPR = oneNPR-twoNPR
        one_two_NPU = oneNPU-twoNPU

        #Add one minus two for reduced
        one_two_out_str += 'con,'+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        one_two_out_str += stim.datafname+',vp+by,one-twoNP,'+str(one_two_NPR) + '\n'
        #Add one minus two for unreduced
        one_two_out_str += 'con,'+stim.data_type+',unreduced'+str(stim.model_num)+','+str(stim.stim_num)+','
        one_two_out_str += stim.datafname+',vp+by,one-twoNP,'+str(one_two_NPU) + '\n'

        #Add oneNP reduced
        reduced_unreduced_str += 'con,'+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,oneNP,'+str(oneNPR)+'\n'
        #Add twoNP reduced
        reduced_unreduced_str += 'con,'+stim.data_type+',reduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,twoNP,'+str(twoNPR)+'\n'
        #Add oneNP unreduced
        reduced_unreduced_str += 'con,'+stim.data_type+',unreduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,oneNP,'+str(oneNPU)+'\n'
        #Add twoNP unreduced
        reduced_unreduced_str += 'con,'+stim.data_type+',unreduced,'+str(stim.model_num)+','+str(stim.stim_num)+','
        reduced_unreduced_str += stim.datafname+',vp_by,twoNP,'+str(twoNPU)+'\n'

    out = open(path+'ordered_shuffled_one-two.csv', 'w')
    out.write(one_two_out_str)
    out.close()

    out = open(path+'ordered_shuffled_reduced_unreduced.csv', 'w')
    out.write(reduced_unreduced_str)
    out.close()

    return


def get_shuff_rand_temp_csv(regions):

    ### Get by Region ###

    PastRs = []
    PastUs = []
    FutureRs = []
    FutureUs = []
    for verb_by in regions['verb_by']:
        PastR = 0
        PastU = 0
        FutureR = 0
        FutureU = 0
        for context in regions['contexts']:
            if 'Past' in context and 'Reduced' in context:
                PastR = verb_by[regions['contexts'][context]]
            if 'Past' in context and 'Unreduced' in context:
                PastU = verb_by[regions['contexts'][context]]
            if 'Future' in context and 'Reduced' in context:
                FutureR = verb_by[regions['contexts'][context]]
            if 'Future' in context and 'Unreduced' in context:
                FutureU = verb_by[regions['contexts'][context]]
        PastRs.append(PastR)
        PastUs.append(PastU)
        FutureRs.append(FutureR)
        FutureUs.append(FutureU)


    path = 'results/temp/SHUFF/'
    #path = 'results/temp/'
    HEADER = 'EXP,Region,Context,Stim,surp\n'

    #Write vp+by Context Merged
    total_out_str = ''
    total_out_str += HEADER
    for element in PastRs:
        total_out_str += 'temp,vp+by,Past,reduced,'+str(element)+'\n'
    for element in PastUs:
        total_out_str += 'temp,vp+by,Past,unreduced,'+str(element)+'\n'
    for element in FutureRs:
        total_out_str += 'temp,vp+by,Future,reduced,'+str(element)+'\n'
    for element in FutureUs:
        total_out_str += 'temp,vp+by,Future,unreduced,'+str(element)+'\n'

    total_out = open(path+'vpby_Past_Future.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    return

def get_shuff_rand_def_csv(regions):

    ### Get by Region ###

    IndefNewRs = []
    IndefNewUs = []
    DefNewRs = []
    DefNewUs = []
    DefOldRs = []
    DefOldUs = []
    for crit in regions['critical']:
        IndefNewR = 0
        IndefNewU = 0
        DefNewR = 0
        DefNewU = 0 
        DefOldR = 0
        DefOldU = 0
        for context in regions['contexts']:

            if 'New+IndefAmbi' in context:
                IndefNewR = crit[regions['contexts'][context]]
            if 'New+IndefUnambi' in context:
                IndefNewU = crit[regions['contexts'][context]]
            if 'New+DefAmbi' in context:
                DefNewR = crit[regions['contexts'][context]]
            if 'New+DefUnambi' in context:
                DefNewU = crit[regions['contexts'][context]]
            if 'Old+DefAmbi' in context:
                DefOldR = crit[regions['contexts'][context]]
            if 'Old+DefUnambi' in context:
                DefOldU = crit[regions['contexts'][context]]
        IndefNewRs.append(IndefNewR)
        IndefNewUs.append(IndefNewU)
        DefNewRs.append(DefNewR)
        DefNewUs.append(DefNewU)
        DefOldRs.append(DefOldR)
        DefOldUs.append(DefOldU)

    path = 'results/def/'
    HEADER = 'EXP,Region,Context,Stim,surp\n'

    #Write vp+by Context Merged
    total_out_str = ''
    total_out_str += HEADER

    for element in IndefNewRs:
        total_out_str += 'def,crit,New+Indef,reduced,'+str(element)+'\n'
    for element in IndefNewUs:
        total_out_str += 'def,crit,New+Indef,unreduced,'+str(element)+'\n'
    for element in DefNewRs:
        total_out_str += 'def,crit,New+Def,reduced,'+str(element)+'\n'
    for element in DefNewUs:
        total_out_str += 'def,crit,New+Def,unreduced,'+str(element)+'\n'
    for element in DefOldRs:
        total_out_str += 'def,crit,Old+Def,reduced,'+str(element)+'\n'
    for element in DefOldUs:
        total_out_str += 'def,crit,Old+Def,unreduced,'+str(element)+'\n'

    total_out = open(path+'ORDERED_crit_Reduced_Unreduced.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    return

def get_context_shuff_rand_con_csv(regions):

    ### Get by Region ###

    one_two_NPRs = []
    one_two_NPUs = []

    for verb_by in regions['verb_by']:
        one_NPR = 0
        one_NPU = 0
        two_NPR = 0
        two_NPU = 0
        for context in regions['contexts']:
            if '1NP' in context and 'Reduced' in context:
                one_NPR = verb_by[regions['contexts'][context]]
            if '1NP' in context and 'Unreduced' in context:
                one_NPU = verb_by[regions['contexts'][context]]
            if '2NP' in context and 'Reduced' in context:
                two_NPR = verb_by[regions['contexts'][context]]
            if '2NP' in context and 'Unreduced' in context:
                two_NPU = verb_by[regions['contexts'][context]]
        one_two_NPRs.append(one_NPR-two_NPR)
        one_two_NPUs.append(one_NPU-two_NPU)

    #path = 'results/ref/SHUFF/'
    path = 'results/con/'
    HEADER = 'EXP,Region,Context,Stim,surp\n'

    #Write vp+by Context Merged
    total_out_str = ''
    total_out_str += HEADER
    for element in one_two_NPRs:
        total_out_str += 'con,vp+by,oneNP-twoNP,reduced,'+str(element)+'\n'
    for element in one_two_NPUs:
        total_out_str += 'con,vp+by,oneNP-twoNP,unreduced,'+str(element)+'\n'

    total_out = open(path+'vpby_one_two_R_U.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    return

def get_context_shuff_rand_temp_csv(regions):

    ### Get by Region ###

    Past_FutureRs = []
    Past_FutureUs = []
    for verb_by in regions['verb_by']:
        PastR = 0
        PastU = 0
        FutureR = 0
        FutureU = 0
        for context in regions['contexts']:
            if 'Past' in context and 'Reduced' in context:
                PastR = verb_by[regions['contexts'][context]]
            if 'Past' in context and 'Unreduced' in context:
                PastU = verb_by[regions['contexts'][context]]
            if 'Future' in context and 'Reduced' in context:
                FutureR = verb_by[regions['contexts'][context]]
            if 'Future' in context and 'Unreduced' in context:
                FutureU = verb_by[regions['contexts'][context]]
        Past_FutureRs.append(PastR-FutureR)
        Past_FutureUs.append(PastU-FutureU)

    #path = 'results/temp/SHUFF/'
    path = 'results/temp/'
    HEADER = 'EXP,Region,Context,Stim,surp\n'

    #Write vp+by Context Merged
    total_out_str = ''
    total_out_str += HEADER
    for element in Past_FutureRs:
        total_out_str += 'temp,vp+by,Past-Future,reduced,'+str(element)+'\n'
    for element in Past_FutureUs:
        total_out_str += 'temp,vp+by,Past-Future,unreduced,'+str(element)+'\n'

    total_out = open(path+'vpby_Past_Future_R_U.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    return

def get_context_shuff_rand_def_csv(regions):

    ### Get by Region ###

    Indefs_Def_New = []
    for crit in regions['critical']:
        IndefNewR = 0
        DefNewR = 0
        DefOldR = 0
        for context in regions['contexts']:
            if 'New+IndefAmbi' in context:
                IndefNewR = crit[regions['contexts'][context]]
            if 'New+DefAmbi' in context:
                DefNewR = crit[regions['contexts'][context]]
            if 'Old+DefAmbi' in context:
                DefOldR = crit[regions['contexts'][context]]
        Indefs_Def_New.append(IndefNewR-DefNewR)

    path = 'results/def/'
    HEADER = 'EXP,Region,Context,Stim,surp\n'

    #Write vp+by Context Merged
    total_out_str = ''
    total_out_str += HEADER

    for element in Indefs_Def_New:
        total_out_str += 'def,crit,Indef-Def_New,reduced,'+str(element)+'\n'

    total_out = open(path+'SHUFF_crit_Indef_Def.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    return

def get_context_shuff_rand_def_info_csv(regions):

    ### Get by Region ###

    New_Old_Def = [] 
    for crit in regions['critical']:
        IndefNewR = 0
        DefNewR = 0
        DefOldR = 0
        for context in regions['contexts']:
            if 'New+IndefAmbi' in context:
                IndefNewR = crit[regions['contexts'][context]]
            if 'New+DefAmbi' in context:
                DefNewR = crit[regions['contexts'][context]]
            if 'Old+DefAmbi' in context:
                DefOldR = crit[regions['contexts'][context]]

        New_Old_Def.append(DefNewR-DefOldR)

    path = 'results/def/'
    HEADER = 'EXP,Region,Context,Stim,surp\n'

    #Write vp+by Context Merged
    total_out_str = ''
    total_out_str += HEADER

    for element in New_Old_Def:
        total_out_str += 'def,crit,New-Old_Def,reduced,'+str(element)+'\n'

    total_out = open(path+'SHUFF_crit_New_Old.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    return

def get_temp_csv(regions):

    ### Get by Region ###

    vp_by_Past = []
    vp_by_Future = []
    vp_by_Past_vs_Future_R = []
    vp_by_Past_vs_Future_U = []
    for verb_by in regions['verb_by']:
        PastR = 0
        PastU = 0
        FutureR = 0
        FutureU = 0
        for context in regions['contexts']:
            if 'Past' in context and 'Reduced' in context:
                PastR = verb_by[regions['contexts'][context]]
            if 'Past' in context and 'Unreduced' in context:
                PastU = verb_by[regions['contexts'][context]]
            if 'Future' in context and 'Reduced' in context:
                FutureR = verb_by[regions['contexts'][context]]
            if 'Future' in context and 'Unreduced' in context:
                FutureU = verb_by[regions['contexts'][context]]

        vp_by_Past.append(PastR - PastU)
        vp_by_Future.append(FutureR - FutureU)
        vp_by_Past_vs_Future_R.append(PastR - FutureR)
        vp_by_Past_vs_Future_U.append(PastU - FutureU)

    NP_Past = []
    NP_Future = []
    NP_Past_vs_Future_R = []
    NP_Past_vs_Future_U = []

    for NP in regions['NP']:
        PastR = 0
        PastU = 0
        FutureR = 0
        FutureU = 0
        for context in regions['contexts']:
            if 'Past' in context and 'Reduced' in context:
                PastR = NP[regions['contexts'][context]]
            if 'Past' in context and 'Unreduced' in context:
                PastU = NP[regions['contexts'][context]]
            if 'Future' in context and 'Reduced' in context:
                FutureR = NP[regions['contexts'][context]]
            if 'Future' in context and 'Unreduced' in context:
                FutureU = NP[regions['contexts'][context]]

        NP_Past.append(PastR - PastU)
        NP_Future.append(FutureR - FutureU)
        NP_Past_vs_Future_R.append(PastR - FutureR)
        NP_Past_vs_Future_U.append(PastU - FutureU)

    #path = 'results/temp/'
    path = 'results/temp/SHUFF/'
    HEADER = 'EXP,Region,Context,surp\n'

    #Write vp+by Context Merged
    total_out_str = ''
    total_out_str += HEADER
    Past_out_str = ''
    Past_out_str += HEADER
    for element in vp_by_Past:
        total_out_str += 'temp,vp+by,Past,'+str(element)+'\n'
        Past_out_str += 'temp,vp+by,Past,'+str(element)+'\n'

    Future_out_str = ''
    Future_out_str += HEADER
    for element in vp_by_Future:
        total_out_str += 'temp,vp+by,Future,'+str(element)+'\n'
        Future_out_str += 'temp,vp+by,Future,'+str(element)+'\n'

    total_out = open(path+'vpby_SHUFF_compiled_R-U.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    Past_out = open(path+'vpby_SHUFF_Past_R-U.csv', 'w')
    Past_out.write(Past_out_str)
    Past_out.close()

    Future_out = open(path+'vpby_SHUFF_Future_R-U.csv', 'w')
    Future_out.write(Future_out_str)
    Future_out.close()

    #Write vp+by Context Differ
    total_out_str = ''
    total_out_str += HEADER
    R_out_str = ''
    R_out_str += HEADER
    for element in vp_by_Past_vs_Future_R:
        total_out_str += 'temp,vp+by,Past-FutureR,'+str(element)+'\n'
        R_out_str += 'temp,vp+by,Past-FutureR,'+str(element)+'\n'

    U_out_str = ''
    U_out_str += HEADER
    for element in vp_by_Past_vs_Future_U:
        total_out_str += 'temp,vp+by,Past-FutureU,'+str(element)+'\n'
        U_out_str += 'temp,vp+by,Past-FutureU,'+str(element)+'\n'

    total_out = open(path+'vpby_SHUFF_compiled_Past-FutureR-U.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    Past_out = open(path+'vpby_SHUFF_Past-FutureR.csv', 'w')
    Past_out.write(R_out_str)
    Past_out.close()

    Future_out = open(path+'vpby_SHUFF_Past-FutureU.csv', 'w')
    Future_out.write(U_out_str)
    Future_out.close()

    #Write np Context Merged
    total_out_str = ''
    total_out_str += HEADER
    Past_out_str = ''
    Past_out_str += HEADER
    for element in NP_Past:
        total_out_str += 'temp,np,Past,'+str(element)+'\n'
        Past_out_str += 'temp,np,Past,'+str(element)+'\n'

    Future_out_str = ''
    Future_out_str += HEADER
    for element in NP_Future:
        total_out_str += 'temp,np,Future,'+str(element)+'\n'
        Future_out_str += 'temp,np,Future,'+str(element)+'\n'

    total_out = open(path+'np_SHUFF_compiled_R-U.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    Past_out = open(path+'np_SHUFF_Past_R-U.csv', 'w')
    Past_out.write(Past_out_str)
    Past_out.close()

    Future_out = open(path+'np_SHUFF_Future_R-U.csv', 'w')
    Future_out.write(Future_out_str)
    Future_out.close()

    #Write np Context Differ
    total_out_str = ''
    total_out_str += HEADER
    R_out_str = ''
    R_out_str += HEADER
    for element in NP_Past_vs_Future_R:
        total_out_str += 'temp,np,Past-FutureR,'+str(element)+'\n'
        R_out_str += 'temp,np,Past-FutureR,'+str(element)+'\n'

    U_out_str = ''
    U_out_str += HEADER
    for element in NP_Past_vs_Future_U:
        total_out_str += 'temp,np,Past-FutureU,'+str(element)+'\n'
        U_out_str += 'temp,np,Past-FutureU,'+str(element)+'\n'

    total_out = open(path+'np_SHUFF_compiled_Past-FutureR-U.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    Past_out = open(path+'np_SHUFF_Past-FutureR.csv', 'w')
    Past_out.write(R_out_str)
    Past_out.close()

    Future_out = open(path+'np_SHUFF_Past-FutureU.csv', 'w')
    Future_out.write(U_out_str)
    Future_out.close()
    
    ### Get Collapsed ###
    RR_Past = []
    RR_Future = []
    RR_Past_vs_Future_R = []
    RR_Past_vs_Future_U = []

    for RR in regions['RR']:
        PastR = 0
        PastU = 0
        FutureR = 0
        FutureU = 0
        for context in regions['contexts']:
            if 'Past' in context and 'Reduced' in context:
                PastR = RR[regions['contexts'][context]]
            if 'Past' in context and 'Unreduced' in context:
                PastU = RR[regions['contexts'][context]]
            if 'Future' in context and 'Reduced' in context:
                FutureR = RR[regions['contexts'][context]]
            if 'Future' in context and 'Unreduced' in context:
                FutureU = RR[regions['contexts'][context]]

        RR_Past.append(PastR - PastU)
        RR_Future.append(FutureR - FutureU)
        RR_Past_vs_Future_R.append(PastR - FutureR)
        RR_Past_vs_Future_U.append(PastU - FutureU)

    #Write RR Context Merged
    total_out_str = ''
    total_out_str += HEADER
    Past_out_str = ''
    Past_out_str += HEADER
    for element in RR_Past:
        total_out_str += 'temp,RR,Past,'+str(element)+'\n'
        Past_out_str += 'temp,RR,Past,'+str(element)+'\n'

    Future_out_str = ''
    Future_out_str += HEADER
    for element in RR_Future:
        total_out_str += 'temp,RR,Future,'+str(element)+'\n'
        Future_out_str += 'temp,RR,Future,'+str(element)+'\n'

    total_out = open(path+'RR_SHUFF_compiled_R-U.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    Past_out = open(path+'RR_SHUFF_Past_R-U.csv', 'w')
    Past_out.write(Past_out_str)
    Past_out.close()

    Future_out = open(path+'RR_SHUFF_Future_R-U.csv', 'w')
    Future_out.write(Future_out_str)
    Future_out.close()

    #Write np Context Differ
    total_out_str = ''
    total_out_str += HEADER
    R_out_str = ''
    R_out_str += HEADER
    for element in RR_Past_vs_Future_R:
        total_out_str += 'ref,RR,Past-FutureR,'+str(element)+'\n'
        R_out_str += 'ref,RR,Past-FutureR,'+str(element)+'\n'

    U_out_str = ''
    U_out_str += HEADER
    for element in RR_Past_vs_Future_U:
        total_out_str += 'ref,RR,Past-FutureU,'+str(element)+'\n'
        U_out_str += 'ref,RR,Past-FutureU,'+str(element)+'\n'

    total_out = open(path+'RR_SHUFF_compiled_Past-FutureR-U.csv', 'w')
    total_out.write(total_out_str)
    total_out.close()

    Past_out = open(path+'RR_SHUFF_Past-FutureR.csv', 'w')
    Past_out.write(R_out_str)
    Past_out.close()

    Future_out = open(path+'RR_SHUFF_Past-FutureU.csv', 'w')
    Future_out.write(U_out_str)
    Future_out.close()

    return

def get_def_csv(regions):

    ### Get Contexts ###
    IndefNewA = []
    IndefNewU = []
    DefNewA = []
    DefNewU = []
    DefOldA = []
    DefOldU = []

    #Example of context: New+DefUnambi
    for crit in regions['critical']:
        for context in regions['contexts']:
            if 'Indef' in context and 'Ambi' in context and 'New' in context:
                IndefNewA.append(crit[regions['contexts'][context]])
            if 'Indef' in context and 'Unambi' in context and 'New' in context:
                IndefNewU.append(crit[regions['contexts'][context]])
            if 'Def' in context and 'Ambi' in context and 'New' in context:
                DefNewA.append(crit[regions['contexts'][context]])
            if 'Def' in context and 'Unambi' in context and 'New' in context:
                DefNewU.append(crit[regions['contexts'][context]])
            if 'Def' in context and 'Ambi' in context and 'Old' in context:
                DefOldA.append(crit[regions['contexts'][context]])
            if 'Def' in context and 'Unambi' in context and 'Old' in context:
                DefOldU.append(crit[regions['contexts'][context]])

    path = 'results/def/'
    #path = 'results/def/SHUFF/'
    HEADER = 'EXP,Region,Context,surp\n'

    ### A - U ###
    out_str = ''
    out_str += HEADER
    for i in range(len(IndefNewA)):
        IndefNew = IndefNewA[i] - IndefNewU[i]
        DefNew = DefNewA[i] - DefNewU[i]
        DefOld = DefOldA[i] - DefOldU[i]

        out_str += 'def,crit,IndefNewA-U,'+str(IndefNew)+'\n'
        out_str += 'def,crit,DefNewA-U,'+str(DefNew)+'\n'
        out_str += 'def,crit,DefOldA-U,'+str(DefOld)+'\n'

    outFile = open(path+'crit_SHUFF_complied_A-U.csv', 'w')
    outFile.write(out_str)
    outFile.close()

    #### IndefNew - DefNew ###
    out_str = ''
    out_str += HEADER
    for i in range(len(IndefNewA)):
        IndefNewDefNewA = IndefNewA[i]-DefNewA[i]
        IndefNewDefNewU = IndefNewU[i]-DefNewU[i]

        out_str += 'def,crit,Indef-Def_New_A,'+str(IndefNewDefNewA)+'\n'
        out_str += 'def,crit,Indef-Def_New_U,'+str(IndefNewDefNewU)+'\n'

    outFile = open(path+'crit_SHUFF_complied_IndefNew-DefNew.csv', 'w')
    outFile.write(out_str)
    outFile.close()

    ### DefNew - DefOld ###
    out_str = ''
    out_str += HEADER
    for i in range(len(DefNewA)):
        DefNewOldA = DefNewA[i] - DefOldA[i]
        DefNewOldU = DefNewU[i] - DefOldU[i]

        out_str += 'def,crit,Def_New-Old_A,'+str(DefNewOldA)+'\n'
        out_str += 'def,crit,Def_New-Old_U,'+str(DefNewOldU)+'\n'

    outFile = open(path+'crit_SHUFF_complied_DefNew-DefOld.csv', 'w')
    outFile.write(out_str)
    outFile.close()
    return


if __name__ == "__main__":

    if len(sys.argv) != 2:
        sys.stderr.write('INCORRECT USAGE: \n\t python compile_test.py (ref|temp|def|all)\n')
        sys.exit()

    exp = sys.argv[1]

    #Load result files
    if exp == 'ref' or exp == 'all':
        ref_results = load_ref_exp()
        get_ref_csv(ref_results)

    if exp == 'temp' or exp == 'all':
        temp_results = load_temp_exp()
        temp_regions = get_temp_roi(temp_results)
        #get_temp_csv(temp_regions)
        #get_shuff_rand_temp_csv(temp_regions)
        get_context_shuff_rand_temp_csv(temp_regions)

    if exp == 'def' or exp == 'all':
        def_results = load_def_exp()
        def_regions = get_def_roi(def_results)
        #get_def_csv(def_regions)
        #get_shuff_rand_def_csv(def_regions)
        get_context_shuff_rand_def_csv(def_regions)
        get_context_shuff_rand_def_info_csv(def_regions)

    if exp == 'con':
        con_results = load_con_exp()
        get_con_csv(con_results)
