from utils import *
from redefined import *
import random
import topmost
import os
from evaluation import eval

def evaluate_configuration(config):
    model = DETMFixed(
            num_topics=config['num_topics'], 
            vocab_size=dataset.vocab_size,
            num_times=dataset.num_times,
            train_size=dataset.train_size,
            train_time_wordfreq=dataset.train_time_wordfreq,
            train_WE=False, 
            pretrained_WE=dataset.pretrained_WE, 
            en_units=config['en_units'], 
            eta_hidden_size=config['eta_hidden_size'], 
            rho_size=config['rho_size'], 
            enc_drop=config['enc_drop'], 
            eta_nlayers=config['eta_nlayers'], 
            eta_dropout=config['eta_dropout'], 
            delta=config['delta'], 
            theta_act=config['theta_act'],
            device=device)

    model = model.to(device)
    trainer = topmost.DynamicTrainer(model, dataset, epochs=config['epochs'], learning_rate=config['learning_rate'], verbose=False)
    
    top_words, train_theta = trainer.train()
    dynamic_TC, dynamic_TD, clustering, classification = eval(dataset, trainer, top_words)
    
    return 0.4 * dynamic_TC + 0.4 * dynamic_TD + 0.1 * clustering + 0.1 * classification
    

def random_configuration(hyperparameter_space):
    return {
        'num_topics': random.choice(hyperparameter_space["num_topics"]),
        'rho_size': random.choice(hyperparameter_space["rho_size"]),
        'en_units': random.choice(hyperparameter_space["en_units"]),
        'eta_hidden_size': random.choice(hyperparameter_space["eta_hidden_size"]),
        'enc_drop': random.choice(hyperparameter_space["enc_drop"]),
        'eta_nlayers': random.choice(hyperparameter_space["eta_nlayers"]),
        'eta_dropout': random.choice(hyperparameter_space["eta_dropout"]),
        'delta_values': random.choice(hyperparameter_space["delta"]),
        'theta_act_values': random.choice(hyperparameter_space["theta_act"]),
        'learning_rate_values': random.choice(hyperparameter_space["learning_rate"]),
        'epochs_values': random.choice(hyperparameter_space["epochs"])}
    
def get_default_config():
    { 
        "num_topics" : 50,
        "rho_size": 300,
        "en_units" : 800,
        "eta_hidden_size" : 200,
        "enc_drop": 0.0,
        "eta_nlayers" : 3,
        "eta_dropou" : 0.0,
        "delta" : 0.005,
        "theta_act" : 'relu',
        "learning_rate": 0.005,
        "epochs": 100}

def evolutionary_search(search_space, population_size=20, generations=10, mutation_rate=0.1):
    population = [random_configuration(search_space) for _ in range(population_size)]
    
    for generation in range(generations):
        scores = [(config, evaluate_configuration(config)) for config in population]
        scores.sort(key=lambda x: x[1], reverse=True)  
        print(f"Generación {generation + 1}, mejor pérdida: {scores[0][1]:.4f}")
        
        num_parents = population_size // 2
        parents = [config for config, _ in scores[:num_parents]]
        
        children = []
        while len(children) < population_size - num_parents:
            parent1, parent2 = random.sample(parents, 2)
            child = {key: random.choice([parent1[key], parent2[key]]) for key in search_space.keys()}
            
            if random.random() < mutation_rate:
                param_to_mutate = random.choice(list(search_space.keys()))
                child[param_to_mutate] = random.choice(search_space[param_to_mutate])
            
            children.append(child)
        
        population = parents + children
    
    best_config, best_score = max(scores, key=lambda x: x[1])
    return best_config, best_score

if __name__ == '__main__':
    device = "cuda"  # or "cpu"
    dataset_dir = "/kaggle/input/revista-ciencias-mdicas-de-la-habana-cmed"
    output_dir = "./model_trainers"

    os.makedirs(output_dir, exist_ok=True)
    dataset = topmost.data.DynamicDataset(dataset_dir, batch_size=200, read_labels=True, device=device)
    
    search_space = get_hyperparameter_space()
    best_config, best_score = evolutionary_search(search_space, population_size=20, generations=10, mutation_rate=0.2)
    print("Mejor configuración encontrada:", best_config)
    print("Mejor pérdida:", best_score)
