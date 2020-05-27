from main import *
import argparse

parser = argparse.ArgumentParser(description='Garden Path Alleviation Experiments for LSTM Language Model Probing')

#parser.add_argument('--models', type=str, default='a',
                    #help='model to run [a|b|c|d|e|all]')

args = parser.parse_args()

#hard code data_dir
data_path = './'
#hardcode vocab file for now
#vocab_file = '/Users/forrestdavis/Data/models/vocab'


#set device to cpu for work on desktop :/
device = torch.device('cpu')

#set loss function to be cross entropy
criterion = nn.CrossEntropyLoss()

versions = ['temp', 'def', 'ref']
vocab_file = 'models/glove.num_unk.vocab'

shuffled_model_files = glob.glob('models/shuffled/*.pt')#[:1]
ordered_model_files = glob.glob('models/ordered/*.pt')#[:1]

model_files = shuffled_model_files+ordered_model_files

for version in versions:
    EXP = run_experiment(version, vocab_file, model_files)
    EXP.save_csv('results/'+version)
    EXP.save_excel('results/'+version)
