from genetic import Genetic

i = 11
while i < 40:
    print(i)
    genetic = Genetic(n=i, population_size=50, generations=100, mutation_rate=0.1, accuracy=0, reach=None)
    for msg in genetic.run(fitness_mode=2):
        print(msg)
    i += 1