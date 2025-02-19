import os
import numpy as np
from tqdm import tqdm
import scipy.sparse
from topmost.preprocessing import Preprocessing
import topmost.preprocessing.preprocessing as prepro
from topmost.utils.logger import Logger
import fasttext
import fasttext.util
import nltk
from nltk.corpus import stopwords
from utils import get_args_json, files

logger = Logger("DEBUG")
nltk.download('stopwords')
stopwords_es = set(stopwords.words('spanish'))
fasttext.util.download_model('es', if_exists='ignore')  # Español

def make_word_embeddings_es(vocab):
    # Cargar el modelo binario preentrenado
    fasttext_model = fasttext.load_model("cc.es.300.bin")

    # glove_vectors = gensim.downloader.load('glove-wiki-gigaword-200')
    word_embeddings = np.zeros((len(vocab), fasttext_model.get_dimension()))

    num_found = 0

    # try:
        # key_word_list = glove_vectors.index_to_key
    # except:
        # key_word_list = glove_vectors.index2word

    # for i, word in enumerate(tqdm(vocab, desc="loading word embeddings")):
        # if word in key_word_list:
            # word_embeddings[i] = fasttext_model.get_word_vector(word)
            # # word_embeddings[i] = glove_vectors[word]
            # num_found += 1

    for i, word in enumerate(tqdm(vocab, desc="loading word embeddings")):
        word_embeddings[i] = fasttext_model.get_word_vector(word)
        num_found += 1

    logger.info(f'number of found embeddings: {num_found}/{len(vocab)}')

    return scipy.sparse.csr_matrix(word_embeddings)

prepro.preprocessing.make_word_embeddings = make_word_embeddings_es

    

if __name__ == '__main__':
    args = get_args_json(files.build_dataset)
    
    jsonlist_path = args['jsonlist_path']
    output_path = args['output_path']
    
    os.makedirs(jsonlist_path, exist_ok=True)
    os.makedirs(output_path, exist_ok=True)

    preprocessing = Preprocessing(stopwords=stopwords_es)

    rst = preprocessing.preprocess_jsonlist(dataset_dir=jsonlist_path, label_name="label")

    preprocessing.save(output_path, **rst)    