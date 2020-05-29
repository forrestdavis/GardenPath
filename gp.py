from main import *
import argparse

parser = argparse.ArgumentParser(description='Garden Path Alleviation Experiments for LSTM Language Model Probing')

parser.add_argument('--models', type=str, default='all',
                    help='model to run [a|b|c|d|e|all]')
parser.add_argument('--exp', type=str, default='all', 
                    help='Experiment to run [def|ref|temp|all]')

args = parser.parse_args()

#hard code data_dir
data_path = './'
#hardcode vocab file for now
#vocab_file = '/Users/forrestdavis/Data/models/vocab'


#set device to cpu for work on desktop :/
device = torch.device('cpu')

#set loss function to be cross entropy
criterion = nn.CrossEntropyLoss()

vocab_file = 'models/glove.num_unk.vocab'

shuffled_model_files = glob.glob('models/shuffled/*.pt')#[:1]
ordered_model_files = glob.glob('models/ordered/*.pt')#[:1]

#Get models
if args.models == 'all':
    model_files = shuffled_model_files+ordered_model_files
elif (args.models == 'a' or args.models == 'b' or args.models == 'c' or
        args.models == 'd' or args.models == 'e'):
    shuffled_model_files = list(filter(lambda x: '_'+args.models+'_' in x, shuffled_model_files))
    ordered_model_files = list(filter(lambda x: '_'+args.models+'_' in x, ordered_model_files))
    model_files = shuffled_model_files+ordered_model_files

#Get experiment
if args.exp == 'all':
    versions = ['temp', 'def', 'ref']
elif args.exp == 'temp' or args.exp == 'ref' or args.exp == 'def':
    versions = [args.exp]

#Run experiment
outfile = 'results/'+args.models+'_'
for version in versions:
    save_file = outfile+version

    EXP = run_experiment(version, vocab_file, model_files)
    EXP.save_csv(save_file)
    EXP.save_excel(save_file)
