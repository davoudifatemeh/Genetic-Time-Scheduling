# Genetic Time Scheduling
In this project, I have found one of the most optimal possible time schedules for doctors' shifts according to the limitations and conditions.

This problem is implemented by genetic algorithm.

# Limitations and Coditions
The following conditions have been applied to the project:

1. Doctors in this hospital have three work shifts, morning, evening and night and for each day there is an estimate of the minimum and maximum number of doctors needed for each shift in the hospital and the number of doctors assigned to that shift must be within this range.

2. Due to the importance of doctors' health and also because doctors must focus enough on their work and treat patients with high efficiency, a doctor who works in the night shift cannot work in the morning and evening shifts the next day. A doctor cannot work three consecutive night shifts in a hospital.

3. Doctors cannot have more than a certain number of shifts and this number is the same for all doctors.

## Implementation Description

### Defining the Concept of Gene and Chromosome

Here, each chromosome has a length equal to three times the number of days and includes the ID of doctors who are in each shift. Each gene is also equivalent to one shift.

### Primary Population Production

To solve the problem, I have considered the number of the initial population equal to 300. The generation of the initial population is as follows: first, a random number is selected for each shift, which represents the number of doctors in that shift and then, according to this number, doctors' IDs are randomly selected.
This process continues until the production of 300 chromosomes in three times the number of days.

### Specifying the Fitness Function
Initially, the fitness for each chromosome has a value equal to zero. Then by checking the limits and if any limit is not established, the fitness value is added.

### Implementing Mutation and Cossover and Producing the Next Generation
In crossover implementation, the value of PC is assumed equal to 0.65 and every time this function is executed, a random number in the range of zero to one is generated. If its value is less than PC, two chromosomes are made, and the first chromosome is the combination of the first part of the first father. And the second part of the second father is created, and in the second chromosome, this structure is the opposite (the crossover point is also chosen randomly). If the random probability is greater than the PC number, the first chromosome will be equal to the first father's chromosome and the second chromosome will be equal to the second father's chromosome.

In the implementation of mutation, the value of pm is assumed equal to 0.4 and the operation is carried out in such a way that the index of a gene in a chromosome is randomly selected and then, like the generation of a gene in the population, first a gene is randomly generated and replaced The gene is selected.

To produce the new generation, I first sort the initial 300 chromosomes according to the fitness value, then I transfer 16% of its chromosomes exactly in the new generation, and I generate the rest by selecting two random fathers in each step and performing crossover and mutation operations, then the value I calculate the fitness for each chromosome in the new population and sort them twice based on this value.

### Genetic Algorithm
Finally, in the schedule function, I continue to generate a new population until I reach a chromosome with zero fitness (a program that complies with the mentioned restrictions).
