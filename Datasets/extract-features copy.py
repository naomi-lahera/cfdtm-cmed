if __name__ == '__main__':
    nltk.download('stopwords')
    stopwords_es = set(stopwords.words('spanish'))

    preprocessing = Preprocessing(min_term=5, stopwords=stopwords_es)
    logger = Logger("WARNING")
    
    train_items = file_utils.read_jsonlist(os.path.join(jsonlist_path, 'train.jsonlist'))
    test_items = file_utils.read_jsonlist(os.path.join(jsonlist_path, 'test.jsonlist'))
    
    logger.info(f"Found training documents {len(train_items)} testing documents {len(test_items)}")
    
    raw_train_texts = []
    train_labels = None
    raw_test_texts = []
    test_labels = None
    
    for item in train_items:
        raw_train_texts.append(item['text'])
    for item in test_items:
        raw_test_texts.append(item['text'])
        
    rst = preprocessing.preprocess(raw_train_texts, None, raw_test_texts, None)
    preprocessing.save(output_path, **rst)
