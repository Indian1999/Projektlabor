from genetic import Genetic

genetic = Genetic(n=17, population_size=60,  generations=150, mutation_rate=0.01, accuracy=0, reach=None)
genetic.run(fitness_mode=2)

