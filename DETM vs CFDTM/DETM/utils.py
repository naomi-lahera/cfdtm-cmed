import joblib
import json

def save_txt(obj, path):
    with open(path, 'w') as file:
        file.write(obj)

def save_top_words_txt(top_words):
    with open('./top_words.txt', 'w') as file:
        for i, time in enumerate(top_words):
            file.write(f'================= Time {i} ================= \n')
            for j, topic in enumerate(time):
                file.write(f'================= Topic {j} ================= \n')
                file.write(f'{topic}')
                file.write('\n')
            file.write('\n')

def save_json(obj, path):
    with open(path, 'w') as file:
        json.dump(obj, file)

def save_joblib(obj, path):
    joblib.dump(obj, path)

def get_desc(num_topics, rho_size, en_units, eta_hidden_size, enc_drop, eta_nlayers, eta_dropout, delta, theta_act, learning_rate, epochs):
    return f'Trainig model with hyperparameters: \n num_topics (K):  {num_topics} rho_size: {rho_size} \n en_units: {en_units} \n eta_hidden_size: {eta_hidden_size} \n enc_drop: {eta_dropout} \n eta_nlayers: {eta_nlayers} \n eta_dropou: {eta_dropout} \n delta: {delta} \n theta_act: {theta_act} \n learning_rate: {learning_rate} \n epochs: {epochs}'

def get_hyperparameters_json(num_topics, rho_size, en_units, eta_hidden_size, enc_drop, eta_nlayers, eta_dropout, delta, theta_act, learning_rate, epochs):
    return { 
        "num_topics" : num_topics,
        "rho_size": rho_size,
        "en_units" : en_units,
        "eta_hidden_size" : eta_hidden_size,
        "enc_drop": enc_drop,
        "eta_nlayers" : eta_nlayers,
        "eta_dropou" : eta_dropout,
        "delta" : delta,
        "theta_act" : theta_act,
        "learning_rate": learning_rate,
        "epochs": epochs}
    
def get_hyperparameter_space():
    with open('./hyperparameter_space.json', 'r') as f:
        return json.load(f)