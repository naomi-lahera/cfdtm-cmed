def evolutionary_search(search_space, population_size=20, generations=10, mutation_rate=0.1):
    population = [random_configuration(search_space) for _ in range(population_size - 1)]
    population.append(get_default_config())

    print(population)

    samples = 0
    tested_configs = dict()
    
    for generation in range(generations):
        scores = []
        for config in population:  
            
            print('🛒')
            print(tested_configs)
            
            if config.values() in tested_configs.keys():
                score = tested_configs[config.values()]
            else:
                try:
                    score = evaluate_configuration(config, samples)
                except:
                    score = float('-inf')
                    samples += 1
                tested_configs[config.values()] = score
                    # tested_configs[config.values()] = score
                    
            scores.append((config, score))

        print(scores)
        # scores = [(config, evaluate_configuration(config, samples += 1)) for config in population]
        scores.sort(key=lambda x: x[1], reverse=True)  
        print(f"🧬 Generación {generation + 1}, mejor pérdida: {scores[0][1]:.4f}")
        
        num_parents = population_size // 2
        parents = [config for config, _ in scores[:num_parents]]
        
        children = []
        while len(children) < population_size - num_parents:
            parent_1, parent_2 = random.sample(parents, 2)
            child = {key: random.choice([parent_1[key], parent_2[key]]) for key in search_space.keys()}
            
            if random.random() < mutation_rate:
                param_to_mutate = random.choice(list(search_space.keys()))
                child[param_to_mutate] = random.choice(search_space[param_to_mutate])
            
            children.append(child)
        
        population = parents + children
    
    best_config, best_score = max(scores, key=lambda x: x[1])
    return best_config, best_score