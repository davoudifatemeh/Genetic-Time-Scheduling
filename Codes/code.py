import random
import time

testFile1 = "test1.txt"
testFile2 = "test2.txt"

class Chromosome(object):
    def __init__(self, chromosome):
        self.chromosome = chromosome
        self.fitness = 0

class JobScheduler:
    def __init__(self, fileInfo):
        self.days = fileInfo[0]
        self.doctors = len(fileInfo[1])
        self.doctorsIds = fileInfo[1]
        self.maxCapacity = fileInfo[2]
        self.allShifts = fileInfo[3]
        self.popSize = 300
        self.chromosomes = self.generateInitialPopulation()
        self.elitismPercentage = 0.16
        self.crossOverPoint = 0
        self.pc = 0.65
        self.pm = 0.4
        
        
    def generateInitialPopulation(self):
        temp = list()
        population = list()
        
        for i in range(self.popSize):
            doctorInShift = list()
            for j in range(3*self.days):
                doctorNum = random.randint(0, self.doctors)
                Ids = random.sample(self.doctorsIds, doctorNum)
                doctorInShift.append(Ids)
            temp.append(doctorInShift)
        
        for i in range (self.popSize):
            chromosome = Chromosome(temp[i])
            population.append(chromosome)
            self.calculateFitness(chromosome)
        population = sorted(population, key = lambda x:x.fitness)
        
        return population
        
    
    def crossOver(self, parentChrom1, parentChrom2):
        randProb = random.random()
        chromosome1 = list()
        chromosome2 = list()
        if randProb < self.pc:
            self.crossOverPoint = random.randint(0, 3*self.days - 1)
            chromosome1 = parentChrom1[:self.crossOverPoint] + parentChrom2[self.crossOverPoint:]
            chromosome2 = parentChrom2[:self.crossOverPoint] + parentChrom1[self.crossOverPoint:]
        else:
            chromosome1 = parentChrom1
            chromosome2 = parentChrom2
        return Chromosome(chromosome1), Chromosome(chromosome2)
        
    def mutate(self, child):
        randProb = random.random()
        if randProb < self.pm:
            randomIndex = random.randint(0, 3*self.days - 1)
            randomNum = random.randint(0, self.doctors)
            Ids = random.sample(self.doctorsIds, randomNum)
            child.chromosome[randomIndex] = Ids
        return
        
        
    def calculateFitness(self, chrom):
        doctorsCap = [0]*self.doctors
        for i in range(3*self.days):
            for j in range(len(chrom.chromosome[i])):
                doctorsCap[chrom.chromosome[i][j]] += 1
                if (i % 3 == 2) and (i != 3*self.days - 1):
                    if chrom.chromosome[i][j] in chrom.chromosome[i + 1]:
                        chrom.fitness += 1
                    if chrom.chromosome[i][j] in chrom.chromosome[i + 2]:
                        chrom.fitness += 1
            
            if (i % 3 == 2) and (i != 3*self.days - 1) and (i != 3*self.days - 4):
                for doctor in self.doctorsIds:
                    if (doctor in chrom.chromosome[i]) and (doctor in chrom.chromosome[i + 3]) and (doctor in chrom.chromosome[i + 6]):
                        chrom.fitness += 1
            
            if (i % 3) == 0:
                if len(chrom.chromosome[i]) < self.allShifts[i//3][i%3][0]:
                    chrom.fitness += 1
                if len(chrom.chromosome[i]) > self.allShifts[i//3][i%3][1]:
                    chrom.fitness += 1
                if len(chrom.chromosome[i + 1]) < self.allShifts[(i + 1)//3][(i + 1)%3][0]:
                    chrom.fitness += 1
                if len(chrom.chromosome[i + 1]) > self.allShifts[(i + 1)//3][(i + 1)%3][1]:
                    chrom.fitness += 1
                if len(chrom.chromosome[i + 2]) < self.allShifts[(i + 2)//3][(i + 2)%3][0]:
                    chrom.fitness += 1
                if len(chrom.chromosome[i + 2]) > self.allShifts[(i + 2)//3][(i + 2)%3][1]:
                    chrom.fitness += 1
        
        for i in range(self.doctors):
            if doctorsCap[i] > self.maxCapacity:
                chrom.fitness += 1  
        return
    
    
    def generateNewPopulation(self):
        population = self.chromosomes
        newPopulation = list()
        index1 = int(self.elitismPercentage*self.popSize) + 1
        newPopulation = population[:index1]
        
        index2 = int((self.popSize - int(self.elitismPercentage*self.popSize))/2)
        for i in range(index2):
            parent1 = random.choice(population[:int(self.popSize/3)])
            parent2 = random.choice(population[:int(self.popSize/3)])
            child1, child2 = self.crossOver(parent1.chromosome, parent2.chromosome)
            self.mutate(child1)
            self.mutate(child2)
            self.calculateFitness(child1)
            self.calculateFitness(child2)
            newPopulation.append(child1)
            newPopulation.append(child2)

        newPopulation = sorted(newPopulation, key = lambda x:x.fitness)
        self.chromosomes = newPopulation
        return
    
    
    def schedule(self):
        goal_reached = False
        while goal_reached == False:
            self.generateNewPopulation()
            if self.chromosomes[0].fitness == 0:
                goal_reached = True
        return self.chromosomes[0]

def readInput(testFile) :
    file = open(testFile, 'r+')
    fileList = file.readlines()
    fileList = [s.replace('\n', '') for s in fileList]
    
    [days, doctors] = [int(i) for i in fileList[0].split()]
    maxCapacity = int(fileList[1])
    
    allShifts = []
    for i in range(2, days + 2):
        dayRequirements = fileList[i].split()
        morningReqs = [int(i) for i in dayRequirements[0].split(",")]
        eveningReqs = [int(i) for i in dayRequirements[1].split(",")]
        nightReqs = [int(i) for i in dayRequirements[2].split(",")]
        
        allShifts.append((morningReqs, eveningReqs, nightReqs))

    file.close()
    return [days, list(range(doctors)), maxCapacity, allShifts]

def printOutput(goal):
    for i in range(0, 3*js.days, 3):
        if (len(goal.chromosome[i]) == 0):
            print("empty", end=" ")
        for j in range(len(goal.chromosome[i])):
            if(j != len(goal.chromosome[i]) - 1):
                print(goal.chromosome[i][j], end=",")
            else:
                print(goal.chromosome[i][j], end=" ")
    
        if (len(goal.chromosome[i + 1]) == 0):
            print("empty", end=" ")
        for j in range(len(goal.chromosome[i + 1])):
            if(j != len(goal.chromosome[i + 1]) - 1):
                print(goal.chromosome[i + 1][j], end=",")
            else:
                print(goal.chromosome[i + 1][j], end=" ")
    
        if (len(goal.chromosome[i + 2]) == 0):
            print("empty")
        for j in range(len(goal.chromosome[i + 2])):
            if(j != len(goal.chromosome[i + 2]) - 1):
                print(goal.chromosome[i + 2][j], end=",")
            else:
                print(goal.chromosome[i + 2][j])

l = readInput(testFile1)
#l = readInput(testFile2)
js = JobScheduler(l)
chromosomes = js.chromosomes
tic = time.time()
goal = js.schedule()
toc = time.time()
#print("Time: ", toc - tic)
printOutput(goal)