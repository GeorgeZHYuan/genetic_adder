from random import randint
import random

CHROMOSOME_LENGTH = 140
MUTATION_RATE = 0.001
CROSSOVER_RATE = 0.7

POPULATION_SIZE = 100
TARGET = 71
MAX_GENERATIONS = 100

class Equation_Finder():
    chromosome = ""
    equation = ''
    result = 0.0
    fitness = 0.0

    def __init__(self, _chromosome=None):
        if _chromosome == None:
            for x in range(0, CHROMOSOME_LENGTH):
                self.chromosome += str(randint(0, 1))
        else:
            self.chromosome = _chromosome
        self.calculate()
        self.get_fitness()

    def decode(self, gene):
        return {
            "0000": 0.0,
            '0001': 1.0,
            '0010': 2.0,
            '0011': 3.0,
            '0100': 4.0,
            '0101': 5.0,
            '0110': 6.0,
            '0111': 7.0,
            '1000': 8.0,
            '1001': 9.0,
            '1010': '+',
            '1011': '-',
            '1100': '*',
            '1101': '/',
        }.get(gene, '')

    def create_equation(self):
        get_number = True
        for x in range (0, CHROMOSOME_LENGTH, 4):
            element = self.decode(self.chromosome[x:x+4])
            if get_number:
                if isinstance(element, float):
                    if not(self.equation[-1:] == '/' and element == 0.0):
                        self.equation += str(element)
                        get_number = False
            else:
                if not isinstance(element, float) and element != '':
                    self.equation += element
                    get_number = True
        if self.equation == "":
            self.equation = "0.0"
        else:
            try:
                int(self.equation[-1:])
            except:
                self.equation = self.equation[:-1]


    def calculate(self):
        self.create_equation()
        self.result = eval(self.equation)

    def get_fitness(self):
        dif = abs(TARGET-self.result)
        if dif == 0:
            self.fitness = float("inf")
        else:
            self.fitness = 1/dif

def cross_over(chromos):
    if random.uniform(0.00, 1.00) < CROSSOVER_RATE:
        x = randint(0, CHROMOSOME_LENGTH-1)
        temp = chromos[0]
        chromos[0] = (chromos[0])[:x] + (chromos[1])[x:]
        chromos[1] = (chromos[1])[:x] + temp[x:]
    return chromos

def mutate(chromo):
    if random.uniform(0.00, 1.00) < MUTATION_RATE:
        x = randint(0, CHROMOSOME_LENGTH-1)
        mutant = str(int(not(bool(int(chromo[x])))))
        chromo = chromo[:x] + mutant + chromo[x+1:]
    return chromo

def select_pair(sample):
    breeding_pair_chroms = []
    total_fitness = 0.0
    for specimen in sample:
        if specimen.fitness == float("inf"):
            return [-1, specimen]
        total_fitness += specimen.fitness
    for i in range(0, 2):
        position = random.uniform(0.0, total_fitness)
        spinner_location = 0.0
        for specimen in sample:
            spinner_location += specimen.fitness
            if position <= spinner_location:
                breeding_pair_chroms.append(specimen.chromosome)
                total_fitness -= specimen.fitness
                specimen.fitness = 0.0
                break
    return breeding_pair_chroms

def create_offspring(chromos):
    offspring = []
    cross_over(chromos)
    for chrom in chromos:
        mutate(chrom)
        offspring.append(Equation_Finder(chrom))
    return offspring

def find_equation():
    pop = []
    for i in range(0, POPULATION_SIZE):
        pop.append(Equation_Finder())
    for i in range(0, MAX_GENERATIONS):
        new_generation = []
        for j in range(0, POPULATION_SIZE):
            breeding_pair = select_pair(pop)
            if breeding_pair[0] == -1:
                return breeding_pair[1]
            offspring = create_offspring(breeding_pair)
            for specimen in offspring:
                new_generation.append(specimen)
        pop = new_generation

the_equation = find_equation()
print(the_equation.chromosome + "\n" + the_equation.equation + " = " + str(the_equation.result))