"""
This script contains a slightly more advanced example of how to use the hetrob library. In contrast to the previous
example, this one will mainly change the following parts:
- Load a problem instance from memory
- Show more details of the visualization process
- Change the selection operator for the genetic algorithm
- Define an objective function for a solution representation

The VRP variant, which is introduced in this script is the HSVRSP. This variant was the subject of the bachelor's
thesis called "Analysis of Existing Algorithms for the Coordination of Heterogeneous Robotic Teams", which was written
by the author of the hetrob library Jonas Teufel.
The PDF of this thesis can be found `on Github <https://github.com/the16thpythonist/hetrob/blob/master/thesis.pdf>`_.
This VRP variant can be briefly described like this:
- There is a set of spatially distributed tasks which have to be completed. These tasks have 2D coordinates and
  different durations. Each task has a certain skill requirement. They can only be completed by those vehicles which
  posses the necessary skill.
- The set of available vehicles is heterogeneous. This most importantly refers to the fact that they can have different
  skills to be able to complete different kinds of tasks. A vehicle may have more than one skill. Additionally, the
  vehicles may have different travel speeds.
- There are additional *synchronization* constraints. This refers to the fact that some tasks may be coupled to each
  other by one or more dynamic time window constraints. This means that if one task is started by some vehicle it
  automatically imposes a time window on some other task, which dictates a window of max and min time where this task
  has to be started. For this variant, only two special cases of these dynamic time window constraints are realized:
  Cooperation and Precedence. Cooperation is when multiple vehicles have to start a task at the same time.
  Precedence defines that some tasks have to be completed before others can start.
"""
from functools import partial

import matplotlib.pyplot as plt
from deap import tools

from hetrob.data import load_data
from hetrob.problem import OrderedHeterogeneousSkillTimeConstraintProblem
from hetrob.util import MaxTimeTermination, d2
from hetrob.visualization import SchedulePlotter, RoutePlotter

from hetrob.genetic.evaluate import WeightedSumObjective, AbsoluteEndTimeObjective, InfeasibilityPenalty
from hetrob.genetic.phenotype import OrderedHeterogeneousSkillTimeConstraintPhenotype
from hetrob.genetic.genotype import EntezariMahootchiGenotype
from hetrob.genetic.solution import generate_genetic_solution
from hetrob.genetic.solve import GeneticOperators, solve_ga_hybrid, MigrateElite
from hetrob.genetic.search import NoGeneticSearch


if __name__ == '__main__':

    """
    1. CREATING THE PROBLEM INSTANCE
    ================================
    The previous example created a problem instance using the constructor of the Problem class. However it is also
    possible to create problem instances once and then save them to a persistent JSON file. This persistent file can
    then be used to load the problem instance from.
    The hetrob library comes with some predefined problem instances especially for the HSVRSP variant. These instances
    are saved in the package `hetrob.data`. This package is also used to load these instances. Specifically the
    `load_data` function will be used. This function expects one argument, which is the unique identifying name for the
    corresponding problem instance. This name consists of two parts, which are separated by a slash.

    - problem set name. A "problem set" refers to a set of problem instances, which are grouped semantically. Usually,
      these instances are generated computationally, where the majority of generational parameters is kept constant for
      all instances, but a small subset of parameters is different for every instance. This way a problem set describes
      the variation of only one isolated problem aspect.
    - instance name. Each instance within such a problem set is furthermore identified by a name, which should contain
      the most important characteristics.

    The most important characteristics of the instance which is being loaded for this example are that there are 20
    task nodes, 2 available vehicles, a total of 3 different skills and 10% of tasks require cooperative execution and
    another 10% are bound by synchronization constraints of some sort.
    """
    problem_data = load_data('hsvrsp_variable_size/hsvrsp_n_20_m_2_rc_10_rp_10.json')

    """
    The "load_data" function itself only returns a python dictionary object, which represents the contents of the JSON
    file. This dict can then be used to create a new Problem class of the correct type by using the "from_dict" method.
    The class `OrderedHeterogeneousSkillTimeConstraintProblem` is the correct class for representing a problem of the
    HSVRSP variant.
    """
    problem = OrderedHeterogeneousSkillTimeConstraintProblem.from_dict(problem_data)

    """
    2. DEFINE THE WAY A GENETIC SOLUTION LOOKS LIKE
    ===============================================
    The creation of the genetic solution is basically the same for this example. For the HSVRSP, there are also already
    predefined classes that can be used for both the genotype and the phenotype representation.

    One thing, which is important to note on the topic of genotype and phenotype representations in general is the
    following: The chances are high that if one would want to implement a new VRP variant by creating a new subclass
    of the Problem base class, new custom Genotype and Phenotype sub classes would have to be developed as well.
    This is because both aspects are tightly coupled to which problem actually has to be solved.
    How these custom problems are defined will be explained in another example file.

    Another thing which could be noted here is the actual genotype class that is being used for the HSVRSP. It is
    called `EntezariMahootchiGenotype`. This is because it is closely based on a genotype representation which was
    developed in a publication of the authors Enterzari and Mahootchi titled "Developing a mathematical model for
    staff routing and scheduling in home health care industries: Genetic Algorithm based solution scheme" (2020).
    Further details about how and why this specific representation is used for the HSVRSP can also be found in the
    previously mentioned bachelor thesis.
    """
    GeneticSolution = generate_genetic_solution(
        EntezariMahootchiGenotype,
        OrderedHeterogeneousSkillTimeConstraintPhenotype
    )

    """
    Another thing which is introduced by this example is the ability to change the objective function for a problem.
    The objective function is modeled as a property of the Phenotype *class*. The "objective" class attribute of the
    Phenotype class has to be an object from a subclass of the abstract base class `SingleObjective` which is part of
    the module `hetrob.genetic.evaluate`.

    The actual objective function to be used can be changed dynamically during the runtime, as this example shows. A
    new SingleObjective object simply has to be created and assigned to the "objective" attribute of the phenotype
    class which is being used.
    In this case the main object is created from the `InfeasibilityPenalty` class. This class is a utility wrapper to
    create a modified objective function, which will assign a static penalty value to infeasible solutions. The
    constructor of this class accepts another SingleObjective object, which is then used for the feasible solutions.
    In this case, the objective function for feasible solutions will be the AbsoluteEndTimeObjective. This objective
    function simply returns the absolute end time of operations for the last task in general.

    One note for the objective functions: At this point the objective function classes like `AbsoluteEndTimeObjective`
    have to be made somewhat custom for each new phenotype. In the future it would be desirable to support arbitrary
    phenotypes using interfaces.
    """
    OrderedHeterogeneousSkillTimeConstraintPhenotype.objective = InfeasibilityPenalty(
        objective=AbsoluteEndTimeObjective(),
        penalty=5000
    )

    """
    With the GeneticOperators object it works basically the same. The arguments it needs are the actual problem object
    and the class GeneticSolution.

    In this example there is also the additional optional argument "select_func". This provides the opportunity to
    define a custom selection operator for the genetic algorithm. How to actually define such a custom selection
    operator will be the subject of a different example. For this example it is enough to introduce the *deap* library.
    *deap* is a python package and one of the dependencies of the hetrob package. It is an abbreviation for
    "distributed evolutionary algorithms in python". This library actually already provides a series of predefined
    selection operators, which can be used for the GeneticOperators as well. These selection functions are part of
    the module `deap.tools`.
    This example is using the "tournament selection operator" with a tournament size of 7.
    """
    genetic_operators = GeneticOperators(
        problem=problem,
        genetic_solution_class=GeneticSolution,
        select_func=partial(tools.selTournament, tournsize=7)
    )

    """
    3. USE ALGORITHM TO SOLVE THE PROBLEM
    =====================================
    The previous example used the function "solve_ga" to execute the genetic algorithm. But there are actually several
    slightly modified versions to this basic genetic algorithm procedure. For this example we are using the function
    "solve_ga_hybrid", which is making several modifcations:

    - Migration mechanism. This version of the GA implements an additional step called "migrate" into the evolutionary
      cycle. This step is applied after all other operators have been applied. It is executed on both the parent
      population of individuals and the offspring population. It offers the option to directly let some parent
      individuals live on by replacing some children. The argument "migrate" expects an object which is from a subclass
      of the abstract base class "Migration".
    - Chance functions. In contrast to the basic version, here the chance for the mutation parameter and the crossover
      parameter are no longer constant values, but rather functions of the generation. This provides the option to have
      the values change with the generation count.
    - Genetic search. This is yet another step within the evolutionary cycle, which provides the ability to additionally
      execute a local search heuristic on some of the individuals of the offspring population. This was implemented
      to essentially realize *memetic algorithms*. The argument "genetic_search" expects an object which is from a
      sublcass of the abstract base class "GeneticSearch".

    This example does not implement any additional local search schemes for the individuals (so no memetic algorithm).
    This can be done by using the `NoGeneticSearch` class. But this example does use the migration mechanism. In
    particular, the `MigrateElite` class. This class implements a mechanism, where for each iteration of the basic
    evolutionary loop, the worst *k* individuals of the offspring population are replaced by the elite *k* individuals
    from the parent generation.
    """
    algorithm_result = solve_ga_hybrid(
        genetic_operators=genetic_operators,
        migrate=MigrateElite(k=10),
        mutpb=lambda gen: 1.0,
        cxpb=lambda gen: 0.5,
        termination=MaxTimeTermination(20),
        genetic_search=NoGeneticSearch(),
        pop_size=50
    )

    """
    4. VIEW THE RESULTS
    ===================
    """
    print('\n'.join([
        '\n-| ALGORITHM RESULT |–',
        f'Is solution feasible?     {algorithm_result.feasible}',
        f'Final fitness value:      {round(algorithm_result.fitness, 3)}',
        f'Total execution time:     {round(algorithm_result.time, 3)} seconds',
    ]))

    """
    This example will go into a little bit more detail regarding the visualization of a solution. In general, the
    visualization related functions and classes are contained within the module `hetrob.visualization`. For this
    example, the result will be visualized by two plots, where one of them shows the vehicle's routes and the other
    the vehicle's schedules in the form of a Gantt chart.

    Plots are generally created by creating an object of the corresponding "Plotter" class and using one of these
    object's utility methods. These methods usually return matplotlib `Axes` objects, where the desired plotting
    information has been added to the canvas.
    Generally speaking, most of the information required for the plotting of a solution are attributes of the
    phenotype object, which is part of the solution object.
    """
    phenotype: OrderedHeterogeneousSkillTimeConstraintPhenotype = algorithm_result.solution.phenotype
    fig, (ax_routes, ax_schedules) = plt.subplots(1, 2, figsize=(15, 8))

    # PLOTTING THE ROUTES
    route_plotter = RoutePlotter()

    # The problem class we are using here in fact has an attribute called "coordinates", but this is a list of 3D (!)
    # coordinates, whereas the plotter method needs 2D coordinates. So here we are converting every entry to 2D using
    # the function "d2", which in this case removes the z-coordinate.
    coordinates = [d2(coords) for coords in problem.coordinates]
    ax_routes = route_plotter.plot_routes(phenotype.full_routes, coordinates, axes=ax_routes)
    ax_routes.set_title('Vehicle routes of solution')
    ax_routes.set_xlabel('x-coordinate')
    ax_routes.set_ylabel('y-coordinate')

    # PLOTTING THE SCHEDULES
    schedule_plotter = SchedulePlotter()

    ax_schedules = schedule_plotter.plot_schedules(
        time_table=phenotype.time_table,
        full_routes=phenotype.full_routes,
        axes=ax_schedules
    )
    ax_schedules.set_title('Vehicle schedules of solution')
    ax_schedules.set_xlabel('time')
    ax_schedules.set_ylabel('vehicle index')

    # To prompt matplotlib to actually open a new window, which contains the previously defined plots
    plt.show()
