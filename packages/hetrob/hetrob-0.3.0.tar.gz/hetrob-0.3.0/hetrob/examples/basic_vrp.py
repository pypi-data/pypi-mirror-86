"""
This script contains a basic example of how the `hetrob` library basically works. The library was originally designed
to provide a framework for solving *vehicle routing problems* using *evolutionary algorithms*.

This example applies a very simple genetic algorithm to solving the basic vehicle routing problem (VRP). This base VRP
includes the following aspects:
- A certain amount of task locations have to be visited exactly once
- A limited amount vehicles is available to visit these locations
- The problem is entirely homogeneous. Each vehicle has the same speed, each location needs exactly the same
  visit duration.
"""
from pprint import pprint
from functools import partial

from deap import tools

from hetrob.problem import BasicProblem
from hetrob.util import MaxIterTermination
from hetrob.visualization import EvolutionPlotter, RoutePlotter

from hetrob.genetic.solution import generate_genetic_solution
from hetrob.genetic.genotype import RoutesGenotype
from hetrob.genetic.phenotype import BasicPhenotype
from hetrob.genetic.solve import solve_ga, GeneticOperators

from hetrob.examples._util import visualize_basic

if __name__ == '__main__':

    """
    1. CREATE ACTUAL PROBLEM INSTANCE
    =================================
    To actually execute an optimization algorithm such as the genetic algorithm, we first need an actual problem
    instance to execute the algorithm on.
    Problem instances are represented by `Problem` objects. The base class `Problem` is part of the module
    `hetrob.problem`. It presents an abstract base class from which all specific problem realizations have to inherit.
    One such child class realizes one specific variant of the vehicle routing problem. In this case the `BasicProblem`
    represents the simplest imaginable version of a vehicle routing problem, which only consist of some task locations
    available vehicles and otherwise totally homogeneous aspects such as a constant travel speed or visit duration.
    Creating one specific problem instance for this setting simply requires to pass the according parameters to the
    constructor of the class.
    """
    problem = BasicProblem(
        vehicle_count=2,
        coordinates=[
            (10, 10),
            (15, 16),
            (23, 89),
            (9, 0),
            (15, 34),
            (89, 72),
            (20, 77),
            (90, 10),
            (32, 9),
            (60, 54),
            (30, 60),
            (70, 25)
        ],
        duration=10
    )

    """
    2. DEFINE THE WAY A GENETIC SOLUTION LOOKS LIKE
    ===============================================
    The first step to solving this VRP instance using a genetic algorithm is to define a `Solution` class. Roughly
    speaking, a solution class defines the way a solution for a given Problem is being represented. For the specific
    case of evolutionary algorithms, this solution representation can be split into the *genotype* and
    *phenotype* classes. The genotype represents a solution as a simple composition of atomic data types such as
    strings, lists etc. It is also the genotype where the variation operators are defined. The phenotype on the
    other hand is the basis for the objective value evaluation and thus the selection process.

    In this case the function `generate_genetic_solution` takes a `Genotype` and a `Phenotype` class as parameters to
    then dynamically create a corresponding `GeneticSolution` *class*. This is a convenience function which is only
    used for the simplest cases. Usually the GeneticSolution class would be defined by hand. For a fully customized
    solution, one would write custom child classes of both Genotype and Phenotype classes as well. But for this simple
    example predefined versions already exist in the library. Roughly speaking the Genotype class implements the
    variation operators and the decoder function and the Phenotype class implements the evaluation process which is
    needed to calculate the objective function value.
    """
    GeneticSolution = generate_genetic_solution(RoutesGenotype, BasicPhenotype)

    """
    3. USE ALGORITHM TO SOLVE THE PROBLEM
    =====================================
    The `GeneticOperators` class wraps all necessary information about both the problem as well as the solution
    representation. In general, it contains all the information about the solution process. This is also the class
    where the selection operator could be changed for example. For this it requires two arguments: The first is the
    concrete `problem` object which is to be optimized and the second one is the GeneticSolution class.
    """
    genetic_operators = GeneticOperators(
        problem=problem,
        genetic_solution_class=GeneticSolution
    )

    """
    All of the above steps were required to setup the problem instance, how solutions are represented, which operators
    to use etc. This function `solve_ga` now actually executes the genetic algorithm. For this, it requires the
    GeneticOperators object, which contains all the information about *how* to execute the algorithm and
    *on which* actual problem.
    Another required argument is the termination condition. Termination conditions are represented by the abstract
    base class `Termination` from the module `hetrob.util`. There are some already implemented versions of this
    termination condition, but customized child classes can be defined. In this case `MaxIterTermination` ends after
    a fixed amount of generations have been executed by the genetic algorithm.
    The other parameters of the solve_ga function define the hyperparameters for the genetic algorithm, which are
    crossover and mutation chance, as well as population size.
    """
    algorithm_result = solve_ga(
        genetic_operators=genetic_operators,
        termination=MaxIterTermination(500),
        mutpb=0.8,
        cxpb=0.6,
        pop_size=50,
        verbose=True
    )

    """
    4. VIEW THE RESULTS
    ===================
    The function `solve_ga` returns an object of the type `AlgorithmResult`. This algorithm result object contains all
    the necessary information about the result and the execution process of the algorithm. It's most important
    attributes are the following:
    - feasible: The boolean value of whether or not the final result is feasible in regards to the problem constraints
    - fitness: The fitness value of the final solution
    - solution: An object of the type `Solution`, which represents the final solution of the algorithm
    - time: A float value for the number of seconds, which the algorithm required for execution.
    """
    print('\n'.join([
        '\n-| ALGORITHM RESULT |–',
        f'Is solution feasible?     {algorithm_result.feasible}',
        f'Final fitness value:      {round(algorithm_result.fitness, 3)}',
        f'Total execution time:     {round(algorithm_result.time, 3)} seconds',
    ]))

    """
    The hetrob library provides several pre-defined functionality of visualizing the results of an algorithm execution.
    The visualization is mainly done using `matplotlib` and all the related functionality is within the module
    `hetrob.visualization`. The details of how to use these will be mentioned in more advanced examples. For this
    example it is enough to know that the utility function visualize_basic will generate 4 plots, which contain the
    following information:
    - A two dimensional map with the locations of the tasks for the given problem instance
    - The same map, but which contains the routes of the final solution
    - A plot which shows the minimum fitness value for each generation
    - A plot for the amount of feasible solutions for each generation
    """
    visualize_basic(algorithm_result)

