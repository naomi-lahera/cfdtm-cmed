import torch
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from sklearn.model_selection import train_test_split
import time
import random
from tqdm import tqdm
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from topmost import evaluations, models, trainers, optimizers

# Funciones auxiliares
def fix_seed(seed):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

def evaluate_model(trainer, dataset, device):
    trainer.model.eval()
    results = {}

    # get theta (doc-topic distributions)
    train_theta, test_theta = trainer.export_theta()
    
    top_words = trainer.get_top_words(20)
    train_times = dataset.train_times.cpu().numpy()

    # compute topic coherence
    dynamic_TC = evaluations.dynamic_TC(dataset.train_texts, train_times, dataset.vocab, top_words)
    results["dynamic_TC"] = dynamic_TC

    # compute topic diversity
    dynamic_TD = evaluations.dynamic_TD(top_words, dataset.train_bow.cpu().numpy(), train_times, dataset.vocab)
    results["dynamic_TD"] = dynamic_TD
    
    # evaluate clustering
    results["clustering"] = evaluations.evaluate_clustering(test_theta, dataset.test_labels)

    # evaluate classification
    results["classification"] = evaluations.evaluate_classification(train_theta, test_theta, dataset.train_labels, dataset.test_labels)
        
    return results

# 1. Cargar y Preparar Datos
def load_and_prepare_data(data_path, seed=42, test_size=0.2, batch_size=32):
    """
    Esta función simula la carga de los datos. 
    Debes remplazar esto con tu propia logica de carga de datos y preprocesado.
    """
    fix_seed(seed)
    
    # Genera datos dummy
    vocab_size = 200
    num_times = 10
    num_docs = 500
    
    all_times = torch.randint(0, num_times, (num_docs,))
    all_bows = torch.randint(0, 10, (num_docs, vocab_size)).float()
    train_time_wordfreq = torch.rand(num_times, vocab_size)
    pretrained_WE = torch.rand(vocab_size, 300)
    train_size = num_docs

    # Divide en train y validation
    train_bows, val_bows, train_times, val_times = train_test_split(all_bows, all_times, test_size=test_size, random_state=seed)
    
    # Crear objetos Dataset para el conjunto de entrenamiento y validación
    train_dataset = {
        "train_bow": train_bows,
        "train_times": train_times,
        "train_texts": [["texto"] * 10] * train_size,  # Debes remplazar esto con tus textos de entrenamiento
        "train_labels": torch.randint(0, 5, (train_size,)),  # Debes remplazar esto con tus etiquetas de entrenamiento
        "vocab": list(range(vocab_size)),  # Debes remplazar esto con tu vocabulario
        "test_labels": torch.randint(0, 5, (num_docs - train_size,)),  # Debes remplazar esto con tus etiquetas de prueba
        "vocab_size": vocab_size,
        "num_times": num_times,
        "train_time_wordfreq": train_time_wordfreq,
        "pretrained_WE": pretrained_WE,
    }

    val_dataset = {
        "train_bow": val_bows,
        "train_times": val_times,
        "train_texts": [["texto"] * 10] * (num_docs - train_size),  # Debes remplazar esto con tus textos de validacion
        "train_labels": torch.randint(0, 5, (num_docs - train_size,)),  # Debes remplazar esto con tus etiquetas de validacion
        "vocab": list(range(vocab_size)),  # Debes remplazar esto con tu vocabulario
        "test_labels": torch.randint(0, 5, (num_docs - train_size,)),  # Debes remplazar esto con tus etiquetas de prueba
        "vocab_size": vocab_size,
        "num_times": num_times,
        "train_time_wordfreq": train_time_wordfreq,
        "pretrained_WE": pretrained_WE,
    }

    train_data = TensorDataset(train_bows, train_times)
    train_loader = DataLoader(train_data, batch_size=batch_size, shuffle=True)

    val_data = TensorDataset(val_bows, val_times)
    val_loader = DataLoader(val_data, batch_size=batch_size, shuffle=False)

    return train_loader, val_loader, train_dataset, val_dataset

# 2. Definir el Espacio de Hiperparámetros
def get_hyperparameter_space():
    return {
        'num_topics': [20, 50, 100],
        'rho_size': [100, 200, 300],
        'en_units': [400, 800, 1200],
        'eta_hidden_size': [100, 200, 300],
        'enc_drop': [0.0, 0.2, 0.3, 0.5],
        'eta_nlayers': [1, 2, 3],
        'eta_dropout': [0.0, 0.2, 0.3, 0.5],
        'delta': [0.001, 0.005, 0.01, 0.05],
        'theta_act': ['relu', 'tanh', 'softplus', 'leakyrelu']
    }

# 3. Entrenamiento y Evaluación
def train_and_evaluate_model(params, train_dataset, val_dataset, device, epochs=10, patience=5, seed=42):

    fix_seed(seed)
    model = models.CFDTM(
        vocab_size=train_dataset["vocab_size"],
        num_times=train_dataset["num_times"],
        pretrained_WE=train_dataset["pretrained_WE"],
        train_time_wordfreq=train_dataset["train_time_wordfreq"],
        **params
    )
    model = model.to(device)
    trainer = trainers.DynamicTrainer(model, train_dataset, val_dataset=val_dataset, test_dataset=val_dataset, optimizer=optimizers.AdamW(lr=0.01), epochs=epochs, early_stop=True, patience=patience)

    top_words, train_theta = trainer.train()

    metrics = evaluate_model(trainer, train_dataset, device)

    return trainer, metrics

# Función Principal
def main():
    
    # Set device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Set Data Path
    data_path = "./dummy_data" # Aqui debes colocar la ruta de tus datos, si los cargas desde un archivo

    # Load and prepare data
    train_loader, val_loader, train_dataset, val_dataset = load_and_prepare_data(data_path)

    # Get hyperparameter space
    param_dist = get_hyperparameter_space()

    # Setup RandomizedSearchCV
    n_iter = 20  # Number of parameter settings that are sampled
    
    results_list = []
    
    for i in tqdm(range(n_iter), desc="Search Progress"):
      
      random_params = {k: random.choice(v) for k, v in param_dist.items()}

      trainer, metrics = train_and_evaluate_model(random_params, train_dataset, val_dataset, device)

      results_list.append({
          "params": random_params,
          "metrics": metrics
      })
    
    print("Search completed!")

    # Save the results
    results_dir = "search_results"
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    results_filename = f"detm_search_results_{timestamp}.json"
    results_filepath = os.path.join(results_dir, results_filename)
    with open(results_filepath, "w") as f:
        json.dump(results_list, f, indent=4)

    print(f"Results saved to: {results_filepath}")

    # Analyze and visualize results
    analyze_and_visualize_results(results_filepath)

def analyze_and_visualize_results(results_filepath):
    # Load results from file
    with open(results_filepath, "r") as f:
        results_list = json.load(f)

    # Convert the results to a Pandas DataFrame for easier analysis and plotting
    df = pd.json_normalize(results_list)

    # Separate the metrics and parameters
    metric_columns = [col for col in df.columns if 'metrics' in col]
    param_columns = [col for col in df.columns if 'params' in col]

    # Rename columns for better readability
    df = df.rename(columns={
        'metrics.dynamic_TC': 'Dynamic TC',
        'metrics.dynamic_TD': 'Dynamic TD',
        'metrics.clustering.AMI': 'Clustering AMI',
        'metrics.clustering.NMI': 'Clustering NMI',
        'metrics.clustering.homogeneity': 'Clustering Homogeneity',
        'metrics.clustering.completeness': 'Clustering Completeness',
        'metrics.clustering.v_measure': 'Clustering V-measure',
        'metrics.classification.micro_f1': 'Classification Micro F1',
        'metrics.classification.macro_f1': 'Classification Macro F1'
    })
    
    metrics_to_plot = ['Dynamic TC', 'Dynamic TD', 'Clustering AMI', 'Clustering NMI', 
                   'Clustering Homogeneity', 'Clustering Completeness', 'Clustering V-measure', 
                   'Classification Micro F1', 'Classification Macro F1']
    
    # Sort DataFrame by a metric of interest for better visualization (e.g., 'Avg NLL')
    df = df.sort_values(by='Dynamic TC', ascending=False)

    # Create box plots for each metric
    for metric in metrics_to_plot:
        plt.figure(figsize=(12, 6))
        sns.boxplot(x=metric, data=df)
        plt.title(f'Distribution of {metric}')
        plt.xlabel(metric)
        plt.tight_layout()
        plt.show()

    # Create scatter plots comparing two metrics
    for i, metric1 in enumerate(metrics_to_plot):
        for metric2 in metrics_to_plot[i+1:]:
            plt.figure(figsize=(8, 6))
            sns.scatterplot(x=metric1, y=metric2, data=df)
            plt.title(f'{metric1} vs {metric2}')
            plt.xlabel(metric1)
            plt.ylabel(metric2)
            plt.tight_layout()
            plt.show()

    # Create a heatmap to visualize the correlation between all metrics
    plt.figure(figsize=(10, 8))
    sns.heatmap(df[metrics_to_plot].corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Metrics')
    plt.tight_layout()
    plt.show()

    # Print the best parameters
    best_params_index = df['Dynamic TC'].idxmax()
    best_params = df.loc[best_params_index, 'params']
    print("Best Parameters based on Dynamic TC:")
    for param, value in best_params.items():
        print(f"{param}: {value}")

if __name__ == "__main__":
    main()