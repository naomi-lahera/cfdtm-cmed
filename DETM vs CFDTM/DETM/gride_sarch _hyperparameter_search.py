import topmost
from topmost.models.dynamic.DETM import DETM
import itertools
from tqdm import tqdm
import os

from utils import *
from redefined import *

DETM.get_theta = get_theta_redefined

########################### Seacrh ####################################
def search(dataset, hyperparameter_space, output_dir):
    num_topics_values = hyperparameter_space["num_topics"]
    rho_size_values = hyperparameter_space["rho_size"]
    en_units_values = hyperparameter_space["en_units"]
    eta_hidden_size_values = hyperparameter_space["eta_hidden_size"]
    enc_drop_values = hyperparameter_space["enc_drop"]
    eta_nlayers_values = hyperparameter_space["eta_nlayers"]
    eta_dropout_values = hyperparameter_space["eta_dropout"]
    delta_values = hyperparameter_space["delta"]
    theta_act_values = hyperparameter_space["theta_act"]
    learning_rate_values = hyperparameter_space["learning_rate"]
    epochs_values = hyperparameter_space["epochs"]
    
    hyperparameters = list(itertools.product(num_topics_values, rho_size_values, en_units_values, eta_hidden_size_values, enc_drop_values, eta_nlayers_values, eta_dropout_values, delta_values, theta_act_values, learning_rate_values, epochs_values))
    for i, [num_topics, rho_size, en_units, eta_hidden_size, enc_drop, eta_nlayers, eta_dropout, delta, theta_act, learning_rate, epochs] in enumerate(tqdm(hyperparameters)):
        # create a model
        print(get_desc(num_topics, rho_size, en_units, eta_hidden_size, enc_drop, eta_nlayers, eta_dropout, delta, theta_act, learning_rate, epochs))
        
        model = DETMFixed(
            num_topics=num_topics, 
            vocab_size=dataset.vocab_size,
            num_times=dataset.num_times,
            train_size=dataset.train_size,
            train_time_wordfreq=dataset.train_time_wordfreq,
            train_WE=False, 
            pretrained_WE=dataset.pretrained_WE, 
            en_units=en_units, 
            eta_hidden_size=eta_hidden_size, 
            rho_size=rho_size, 
            enc_drop=enc_drop, 
            eta_nlayers=eta_nlayers, 
            eta_dropout=eta_dropout, 
            delta=delta, 
            theta_act=theta_act,
            device=device)

        model = model.to(device)
        # trainer = topmost.DynamicTrainer(model, dataset, epochs=1, learning_rate=1e-3, lr_step_size=75, lr_scheduler=True, verbose=False)
        trainer = topmost.DynamicTrainer(model, dataset, epochs=epochs, learning_rate=learning_rate, verbose=False)
        
        top_words, train_theta = trainer.train()

        print(f'============= Model {i} ===================================')
        #eval(dataset, trainer, top_words)
        print(train_theta)
        print('\n')
        
        current_path = os.path.join(output_dir, f'./{i}')
        os.makedirs(current_path, exist_ok=True)
        
        save_json(get_hyperparameters_json(num_topics, rho_size, en_units, eta_hidden_size, enc_drop, eta_nlayers, eta_dropout, delta, theta_act, learning_rate, epochs), os.path.join(current_path, 'hyperparameters.json'))
        save_joblib(trainer, os.path.join(current_path, 'trainer.joblib'))
        save_top_words_txt(top_words)
        save_joblib(top_words, os.path.join(current_path, 'top_words.joblib'))
        
if __name__ == '__main__':
    device = "cuda"  # or "cpu"
    dataset_dir = "/kaggle/input/revista-ciencias-mdicas-de-la-habana-cmed"
    output_dir = "./model_trainers"

    os.makedirs(output_dir, exist_ok=True)
    dataset = topmost.data.DynamicDataset(dataset_dir, batch_size=200, read_labels=True, device=device)
    
    hyperparameter_space = get_hyperparameter_space()
    
    search(dataset, hyperparameter_space, output_dir)