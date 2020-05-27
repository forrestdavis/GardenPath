from main import *
import argparse

parser = argparse.ArgumentParser(description='Garden Path Alleviation Experiments for LSTM Language Model Probing')

parser.add_argument('--models', type=str, default='a',
                    help='model to run [a|b|c|d|e|all]')

args = parser.parse_args()

#hard code data_dir
data_path = './'
#hardcode vocab file for now
#vocab_file = '/Users/forrestdavis/Data/models/vocab'


#set device to cpu for work on desktop :/
device = torch.device('cpu')

#set loss function to be cross entropy
criterion = nn.CrossEntropyLoss()

