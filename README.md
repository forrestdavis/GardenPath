# ExperimentNorming
Project for probing pragmatic and discourse knowledge acquired by 
RNN language models using garden path alleviation experiments. There
are three classes of experiments. One experiment set targets
 alleviation of NP/Z garden path effects modeled off of 
[Besserman & Kaiser (2016)](https://cogsci.mindmodeling.org/2016/papers/0161/). 
The manipulation there is definiteness and information status (given vs. new). 
The other two target alleviation of MV/RR garden path effects, by manipulating 
the number of possible referents (as in 
[Spivey-Knowlton, Trueswell, & Tanenhaus (1993)](http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.384.8480))
and by manipulating temporal sequencing (as in 
[Trueswell & Tanenhaus (1991)](https://www.tandfonline.com/doi/abs/10.1080/01690969108406946)).

 
### Dependencies
Requires the following python packages (available through pip):
* [pytorch](https://pytorch.org/) v1.0.0
* [pandas](https://pandas.pydata.org) 
* [numpy](https://numpy.org)


### Quick Usage
To run norming on stimuli:

    python gp.py

### Information on Files

Python files:
* data.py is a wrapper for loading the experiment stimuli and formating it in a way that 
main expects
* data_test.py is a wrapper that generates one-hot encodings for input 
to the model 
* model.py generates the pytorch RNN model (default is LSTM)
* main.py generates the information-theoretic measures and runs the experimental stimuli 
through the model
* gp.py is the over-arching wrapper for the user that just allows different configurations for main.py

Directories:

* figures/ has the figures used in the paper
* stimuli/ has the stimuli used for the experiments in sub-directories and in files broken by type. 
For example, stimuli/Referential/1NP contains the one possible referent contexts for the MV/RR experiments.
* models/ has the models used in the paper and the vocab file
* perplexity/ contains the valid data broken into articles as specified in the paper. The perplexity values are 
saved in the file values. There are scripts that compile the perplexity values and that break up the valid 
data into articles. To save one the computational time, the by-word complexity measures are given by model 
in sub-directories. 
* r_code/ contains the r_code used to run statistical tests in the paper and to generate the figures.
* results/ contains the measures for the experiments and the differences by context type for each experiment.

Feel free to reach out to me via email, if you have further questions.

### Extra Details
To run gp.py with non-default settings:

    usage: gp.py [-h] [--models MODELS] [--exp EXP]

    Garden Path Alleviation Experiments for LSTM Language Model Probing

    optional arguments:
      -h, --help       show this help message and exit
      --models MODELS  model to run [a|b|c|d|e|all]
      --exp EXP        Experiment to run [def|ref|temp]
                    
        usage: norm.py [-h] [--models models] [--stim_file stim_file] [--has_header]
                       [--multi_sent] [--output_file output_file]
                       [--file_type file_type]

Example run:
        gp.py --models a --exp def

This will run the experiments for NP/Z using the first shuffled and ordered models. The 
results will be saved to results as a_def.csv (and a_def.xlsx).

One can prevent the saving to an excel file by commented out save_excel in gp.py.

### References
Forrest Davis and Marten van Schijndel. "Interaction with Context During Recurrent Neural Network 
Sentence Processing." In Proceedings of the 42nd Annual Meeting of the Cognitive Science Society (CogSci 2020). 2020.
