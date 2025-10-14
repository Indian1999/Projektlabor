from genetic import Genetic

if __name__ == "__main__":
    genetic = Genetic(n=15, population_size=60,  generations=None,
                       mutation_rate=0.01, accuracy=0, reach=None)
    genetic.run(fitness_mode=2)