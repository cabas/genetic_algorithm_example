"""Genetic algorithm example"""
from random import randint, random
from functools import reduce
from operator import add
from colorama import Fore

TITLE_COLOR = Fore.CYAN
CONTENT_COLOR = Fore.WHITE

def generate_individual(length, minimum, maximum):
    """
    Generates a random individual of the population
    :length: number of values of the individual
    :param minimum: Minimum value for each position
    :param maximum: Maximun value for each position
    """
    return [randint(minimum, maximum) for i in range(length)]

def generate_population(count, length, minimum, maximum):
    """
    Generates a random population
    :param count: number of individuals
    :param length: number of values per individual
    :param minimum: minimum possible value for each position
    :param maximum: maximum possible value for each psition
    """
    return [generate_individual(length, minimum, maximum) for i in range(count)]

def fitness(individual, target):
    """
    Calculutes the fitness of an individual, lower is better
    :param individual: individual to calculate fitness
    :param target: the target value to achieve
    """
    result = reduce(add, individual, 0)
    return abs(target-result)

def best_fitness(population, target):
    """
    Obtains the best fitness of a generation with the corresponding
    :param population: population of the sample
    :param target: the target value to achieve
    """
    minimum = 1000
    result = None
    for individual in population:
        value = fitness(individual, target)
        if value < minimum:
            minimum = value
            result = individual
    return minimum, result

def average_fitness(population, target):
    """
    Calculates the average fitness for a population, lower is better
    :param population: population to calculate fitness
    :param target:
    """
    summed = reduce(add, (fitness(i, target) for i in population), 0)
    return summed / (len(population) * 1.0)

def tournament_selection(individual_1, individual_2, target):
    """
    Performs selection between two individuals
    :param individual_1: first individual of the tournament
    :param individual_2: second individual of the tournament
    :param target: target value for fitness
    """
    if fitness(individual_1, target) < fitness(individual_2, target):
        return individual_1
    return individual_2

def selection(population, target, selection_size):
    """
    Performs selection on half of the elements of the population using the tournament_selection
    :param population: entire population
    :param target: target value for fitness
    """
    result = []
    i = 0
    while i < selection_size:
        individual_1 = population[randint(0, len(population) - 1)]
        individual_2 = population[randint(0, len(population) - 1)]
        winner = tournament_selection(individual_1, individual_2, target)
        if winner not in result:
            result.append(winner)
            i += 1
    return result

def crossover(individual_1, individual_2, probability):
    """
    Performs crossover with the given probability between two individuals
    :param individual_1: first individual
    :param individual_1: second individual
    :param probability: crossover probability
    """
    if random() < probability:
        pivot = int(round(len(individual_1)/2, 0))
        child_1 = individual_1[:pivot] + individual_2[pivot:]
        child_2 = individual_2[:pivot] + individual_1[pivot:]
        return child_1, child_2
    return individual_1, individual_2

def mutation(individual, minimum, maximum, probability):
    """
    Performs mutation in an individual with the given probability, randomizes a a value in a random
    position using the minimum and maximum limits
    :param individual: individual to be mutated
    :param minimum: floor value for the random value
    :param maximum: ceil value for the random value
    :probability: chance of performing mutation
    """
    if random() < probability:
        individual[randint(0, len(individual)-1)] = randint(minimum, maximum)
    return individual

def evolve(count, length, minimum, maximum, crossover_probability, mutation_probability, target): # pylint: disable=R0913, R0914
    """
    Executes the genetic algorithm
    """
    # Initial population
    population = generate_population(count, length, minimum, maximum)
    history_average_fitness = []
    history_best_fitness = []

    # Cycle for generations to run
    i = 0
    while True:
        # Selection
        selection_size = int(round(0.9 * len(population)))
        population = selection(population, target, selection_size)
        while len(population) < count:
            population.append(generate_individual(length, minimum, maximum))
        # Crossover
        result = []
        j = 1
        while j < len(population):
            child1, child2 = crossover(population[j-1], population[j], crossover_probability)
            result.append(child1)
            result.append(child2)
            j += 2
        while len(population) < count:
            result.append(generate_individual(length, minimum, maximum))
        # Mutation
        for individual in result:
            individual = mutation(individual, minimum, maximum, mutation_probability)
        # Result evaluation
        best_value, best_individual = best_fitness(result, target)
        history_best_fitness.append(best_value)
        history_average_fitness.append(average_fitness(result, target))
        if best_value == 0:
            break
        i += 1
    return i, best_individual, history_average_fitness, history_best_fitness


def main():
    """Main function"""
    count = 100
    length = 6
    minimum = 0
    maximum = 300
    crossover_probability = 0.8
    mutation_probability = 0.10
    target = 250

    generations, best_individual, avg_fitness, best_value = evolve(count, length, minimum,
                                                                   maximum, crossover_probability,
                                                                   mutation_probability, target)
    print('\n'+TITLE_COLOR+'Generations to achieve optimal:'+CONTENT_COLOR, generations, '\n')
    print('\n'+TITLE_COLOR+'Best individual found:'+CONTENT_COLOR, best_individual, '\n')
    print('\n'+TITLE_COLOR+'Average fitness per generation:'+CONTENT_COLOR, avg_fitness, '\n')
    print('\n'+TITLE_COLOR+'Best fitness per generation'+CONTENT_COLOR, best_value, '\n')


if __name__ == "__main__":
    main()
