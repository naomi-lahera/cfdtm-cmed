from redefined import *

eva.topic_coherence._coherence = _coherence_modified

########################### Evaluate ####################################
def eval(dataset, trainer, top_words):
    # get theta (doc-topic distributions)
    train_theta, test_theta = trainer.export_theta()

    train_times = dataset.train_times.cpu().numpy()
    # compute topic coherence
    dynamic_TC = eva.dynamic_coherence(dataset.train_texts, train_times, dataset.vocab, top_words, verbose=True)
    print("dynamic_TC: ", dynamic_TC)

    # compute topic diversity
    dynamic_TD = eva.dynamic_diversity(top_words, dataset.train_bow.cpu().numpy(), train_times, dataset.vocab)
    print("dynamic_TD: ", dynamic_TD)

    # evaluate clustering
    clustering = eva._clustering(test_theta, dataset.test_labels)
    print(clustering)

    # evaluate classification
    classification = eva._cls(train_theta, test_theta, dataset.train_labels, dataset.test_labels)
    print(classification)
    
    json = {
        "dynamic_TC": dynamic_TC,
        "dynamic_TD": dynamic_TD,
        "clustering": clustering,
        "classification": classification
    }
    
    return dynamic_TC, dynamic_TD, clustering, classification