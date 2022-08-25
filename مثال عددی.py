import random

class Scheduler:
    def __init__(self):
        self.done = False
        self.popSize = 500
        self.chromosomes = self.generateInitialPopulation()
        self.shelf_capacities =[2,4,4]
        self.S = [[0.36, 0.24, 0.15, 0.16, 0.13, 0.1, 0.1, 0.17, 0.11, 0.12],
                  [0, 0.47, 0.18, 0.18, 0.18, 0.13, 0.11, 0.22, 0.14, 0.14],
                  [0, 0, 0.46, 0.22, 0.2, 0.12, 0.14, 0.21, 0.17, 0.14],
                  [0, 0, 0, 0.45, 0.16, 0.14, 0.13, 0.24, 0.18, 0.12],
                  [0, 0, 0, 0, 0.36, 0.08, 0.09, 0.16, 0.14, 0.13],
                  [0, 0, 0, 0, 0, 0.36, 0.2, 0.19, 0.1, 0.1],
                  [0, 0, 0, 0, 0, 0, 0.31, 0.12, 0.07, 0.1],
                  [0, 0, 0, 0, 0, 0, 0, 0.49, 0.23, 0.16],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0.31, 0.09],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.9]]
        
        self.C = [[1, 0.67, 0.42, 0.44, 0.36, 0.28, 0.28, 0.47, 0.31, 0.33],
                  [0.51, 0.1, 0.38, 0.38, 0.38, 0.28, 0.23, 0.47, 0.3, 0.3],
                  [0.33, 0.39, 1, 0.48, 0.43, 0.26, 0.3, 0.46, 0.37, 0.3],
                  [0.36, 0.4, 0.49, 1, 0.36, 0.31, 0.29, 0.53, 0.4, 0.27],
                  [0.36, 0.5, 0.56, 0.44, 1, 0.22, 0.25, 0.44, 0.39, 0.36],
                  [0.28, 0.36, 0.33, 0.39, 0.22, 1, 0.56, 0.53, 0.28, 0.28],
                  [0.32, 0.35, 0.45, 0.42, 0.29, 0.65, 1, 0.39, 0.23, 0.32],
                  [0.35, 0.45, 0.43, 0.49, 0.33, 0.39, 0.24, 1, 0.47, 0.33],
                  [0.35, 0.45, 0.55, 0.58, 0.45, 0.32, 0.23, 0.74, 1, 0.29],
                  [0.4, 0.47, 0.47, 0.4, 0.43, 0.33, 0.33, 0.53, 0.3, 1]]

        self.V = [0.8, 0.5, 0.9, 0.6, 0.2, 0.5, 0.1, 0.5, 0.4, 0.9, 0.4, 0.1, 0.1, 0.5, 0.9, 0.1, 0.3, 0.7, 0.5, 0.5, 0.5, 0.1, 0.1, 0.7, 0.2, 0.3, 0.8, 0.1, 0.8, 0.1]
        self.B = [40, 15, 70, 20, 15, 25, 10, 10, 22, 5]
        self.num = 320
        self.s_min = 0.2
        self.elitismPercentage = 0.01
        self.crossOverPoints = 30
        self.pc = 0.4
        self.pm = 0.6
    def generateInitialPopulation(self):
        chromosomes = []
        for i in range(self.popSize):
            chromosome = []
            for _ in range(30):
                rand_num = random.uniform(0, 1)
                if rand_num < 0.5:
                    chromosome.append(0)
                else:
                    chromosome.append(1)

            chromosomes.append(chromosome)
                    
        return chromosomes
    
    def check_column_limits(self, chromosome):
        ok_cols = 0
        for i in range(10):
            col_sum = 0
            col_sum += chromosome[3*i + 0]
            col_sum += chromosome[3*i + 1]
            col_sum += chromosome[3*i + 2]
            
            if col_sum == 1:
              ok_cols += 1
        return ok_cols / 10  
        
    def check_shelf_limits(self, chromosome):
        sum_shelf1 = 0
        sum_shelf2 = 0
        sum_shelf3 = 0
        
        for i in range(len(chromosome)):
            if i % 3 == 0:
                sum_shelf1 += chromosome[i]
            if i % 3 == 1:
                sum_shelf2 += chromosome[i]
            if i % 3 == 2:
                sum_shelf3 += chromosome[i] 

        return ((sum_shelf1 <= self.shelf_capacities[0]) + \
                (sum_shelf2 <= self.shelf_capacities[1]) + \
                (sum_shelf3 <= self.shelf_capacities[2]) ) / 3   
        
    def check_support_constraint(self, chromosome):
        shelf_1 = []
        shelf_2 = []
        shelf_3 = []
        ok_supports = 0
        
        for i in range(len(chromosome)):
            if i % 3 == 0:
                shelf_1.append(chromosome[i])
            if i % 3 == 1:
                shelf_2.append(chromosome[i])
            if i % 3 == 2:
                shelf_3.append(chromosome[i])

        for i in range(len(shelf_1) - 1):
            if shelf_1[i] * shelf_1[i+1] * (self.S[i][i+1] - self.s_min) >= 0:
                ok_supports += 1
        for i in range(len(shelf_2) - 1):
            if shelf_2[i] * shelf_2[i+1] * (self.S[i][i+1] - self.s_min) >= 0:
                ok_supports += 1
        for i in range(len(shelf_3) - 1):
            if shelf_3[i] * shelf_3[i+1] * (self.S[i][i+1] - self.s_min) >= 0:
                ok_supports += 1    
        
        return ok_supports / 27
    
    def calculate_preference_function(self, chromosome):
        shelf_1 = []
        shelf_2 = []
        shelf_3 = []
        ans = 0
        
        for i in range(len(chromosome)):
            if i % 3 == 0:
                shelf_1.append(chromosome[i])
            if i % 3 == 1:
                shelf_2.append(chromosome[i])
            if i % 3 == 2:
                shelf_3.append(chromosome[i])

        for i in range(9):
            for l in range(i+1, 10):
                Cil = self.C[i][l]
                Cli = self.C[l][i]
                sh1 = self.B[i] * self.V[3*i] + self.B[l] * self.V[3*l] * shelf_1[i] * shelf_1[l]
                sh2 = self.B[i] * self.V[3*i + 1] + self.B[l] * self.V[3*l + 1] * shelf_2[i] * shelf_2[l]
                sh3 = self.B[i] * self.V[3*i + 2] + self.B[l] * self.V[3*l + 2] * shelf_3[i] * shelf_3[l]
                ans += (Cil + Cli * (sh1 + sh2 + sh3))
        
        return ans
    
    def caculateFitness(self, chromosome):
        column_limits = self.check_column_limits(chromosome)
        shelf_limits = self.check_shelf_limits(chromosome)
        support_constraint = self.check_support_constraint(chromosome)
        # ans = self.calculate_preference_function(chromosome)
        # print(ans)
        if column_limits == 1 and shelf_limits == 1 and support_constraint == 1:
            return self.calculate_preference_function(chromosome)
        return (column_limits + shelf_limits + support_constraint) / 3 * self.num
    
    
    def put_default_best_chromosomes(self):
        self.chromosomes.sort(key = lambda x:self.caculateFitness(x))
        num = self.elitismPercentage * self.popSize
        if num - int(num) > 0:
            index = int(num) + 1
        else:
            index = int(num)
        highest = self.chromosomes[-index:]
        return highest, index
    
    def crossOver(self, chromosome1, chromosome2):
        child1=[]
        child2=[]
        prev_index = 0
        chromo = 1
        for i in range(1,self.crossOverPoints):
            rand_num = random.random()
            if rand_num < self.pc:
                if(chromo == 1):
                    child1 += (chromosome1[prev_index:i])
                    child2 += (chromosome2[prev_index:i])
                    prev_index = i
                    chromo = 2
                else:
                    child1 += (chromosome2[prev_index:i])
                    child2 +=(chromosome1[prev_index:i])
                    prev_index = i
                    chromo = 1
        
        if(chromo == 1):
            child1 += (chromosome1[prev_index:])
            child2 += (chromosome2[prev_index:])
        else:
            child1 += (chromosome2[prev_index:])
            child2 +=(chromosome1[prev_index:])
            
        return child1,child2
    
    def mutate(self, chromosome):
        for i in range(self.crossOverPoints):
            rand_num = random.random()
            if rand_num < self.pm:
                if chromosome[i] == 1:
                    chromosome[i] = 0
                else:
                    chromosome[i] = 1
        return chromosome

    def generateNewPopulation(self, counter):
        new_chromosomes,index = self.put_default_best_chromosomes()

        maximum_fitness = self.caculateFitness(new_chromosomes[-1])
        if maximum_fitness == 300:
            self.done = True
            ans_chromosome = new_chromosomes[-1]
            ans = self.calculate_preference_function(ans_chromosome)
            print(ans)
            return ans_chromosome
        # print(new_chromosomes[-1])
        if counter > 95:
            print(maximum_fitness)
            print('....................................')
        
        for i in range(len(self.chromosomes)):
            chromosome1_index = random.randint(0,len(self.chromosomes)-1)
            chromosome2_index = random.randint(0,len(self.chromosomes)-1)
            while chromosome1_index == chromosome2_index:
                chromosome2_index = random.randint(0,len(self.chromosomes)-1)
                
            self.chromosomes[chromosome1_index], self.chromosomes[chromosome2_index] = \
                self.crossOver(self.chromosomes[chromosome1_index], self.chromosomes[chromosome2_index])
        
        for i in range(len(self.chromosomes)):
            chromosome1_index = random.randint(0,len(self.chromosomes)-1)
            self.chromosomes[chromosome1_index] = self.mutate(self.chromosomes[chromosome1_index])

        self.chromosomes.sort(key = lambda x:self.caculateFitness(x))
        # print(self.caculateFitness(self.chromosomes[5]))
        self.chromosomes[:index] = new_chromosomes
        
    def schedule(self): 
        counter = 0 
        while (not self.done and counter < 100):
            self.generateNewPopulation(counter)
            counter += 1
scheduler = Scheduler()
scheduler.schedule()