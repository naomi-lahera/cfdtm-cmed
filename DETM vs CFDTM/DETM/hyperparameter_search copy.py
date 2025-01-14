import topmost
from topmost.data import download_dataset
import itertools
import json

def search(dataset, hyperparameter_space):
    num_topics_values = hyperparameter_space["num_topics"]
    # rho_size_values = hyperparameter_space["rho_size"]
    en_units_values = hyperparameter_space["en_units"]
    eta_hidden_size_values = hyperparameter_space["eta_hidden_size"]
    # enc_drop_values = hyperparameter_space["enc_drop"]
    eta_nlayers_values = hyperparameter_space["eta_nlayers"]
    eta_dropout_values = hyperparameter_space["eta_dropout"]
    delta_values = hyperparameter_space["delta"]
    theta_act_values = hyperparameter_space["theta_act"]
    
    hyperparameters = list(itertools.product(num_topics_values, en_units_values, eta_hidden_size_values, eta_nlayers_values, eta_dropout_values, delta_values, theta_act_values))
    for num_topics, en_units, eta_hidden_size, eta_nlayers, eta_dropout, delta, theta_act in hyperparameters:
        # create a model
        model = topmost.models.DETM(
            vocab_size=dataset.vocab_size,
            num_times=dataset.num_times,
            train_size=dataset.train_size,
            train_time_wordfreq=dataset.train_time_wordfreq,
            num_topics=num_topics, 
            train_WE=False, 
            pretrained_WE=dataset.pretrained_WE 
            en_units=en_units, 
            eta_hidden_size=eta_hidden_size, 
            # rho_size=300, 
            # enc_drop=0.0, 
            eta_nlayers=eta_nlayers, 
            eta_dropout=eta_dropout, 
            delta=delta, 
            theta_act=theta_act,
            device=device,
        )
        model = model.to(device)
        trainer = topmost.trainers.DynamicTrainer(model, epochs=400)
        top_words, train_theta = trainer.train()
        
def get_hyperparameter_space():
    with open("hyperparameter_space.json", 'r') as f:
        return json.load(f)

if __name__ == '__main__':
    device = "cuda"  # or "cpu"
    dataset_dir = "./datasets/Ciencias-Médicas/CMed"
    dataset = topmost.data.DynamicDataset(dataset_dir, batch_size=200, read_labels=True, device=device)
    
    hyperparameter_space = get_hyperparameter_space()
    
    search(dataset, hyperparameter_space)