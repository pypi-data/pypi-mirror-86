from pprint import pprint

import matplotlib.pyplot as plt

from hetrob.result import AlgorithmResult
from hetrob.problem import BasicProblem
from hetrob.visualization import ProblemPlotter, EvolutionPlotter, RoutePlotter, SchedulePlotter

from hetrob.genetic.phenotype import BasicPhenotype


def visualize_basic(algorithm_result: AlgorithmResult):
    """
    Visualizes the 
    :param algorithm_result:
    :return:
    """
    solution = algorithm_result.solution
    problem: BasicProblem = algorithm_result.problem
    logbook = algorithm_result.logbook
    phenotype: BasicPhenotype = solution.phenotype

    fig, ((ax_problem, ax_evolution), (ax_routes, ax_feasible)) = plt.subplots(2, 2, figsize=(14, 10))

    # PLOTTING THE PROBLEM
    problem_plotter = ProblemPlotter()
    ax_problem = problem_plotter.plot_coordinates(
        problem.node_coordinates,
        axes=ax_problem,
        get_node_kwargs=lambda coords, index: {'color': 'black', 'marker': 's' if not index else 'o'},
    )
    ax_problem.set_title('Coordinates of task locations')
    ax_problem.set_xlabel('x-coordinate')
    ax_problem.set_ylabel('y-coordinate')

    # PLOTTING THE EVOLUTION OF THE FITNESS
    evolution_plotter = EvolutionPlotter()
    min_fitnesses = [entry['min'] for entry in logbook.chapters['fitness']]
    ax_evolution = evolution_plotter.plot_fitness(
        min_fitnesses,
        axes=ax_evolution
    )
    ax_evolution.set_title('Best fitness over the generations')
    ax_evolution.set_xlabel('generation')
    ax_evolution.set_ylabel('fitness')

    # PLOTTING THE VEHICLE ROUTES
    route_plotter = RoutePlotter()
    ax_routes = route_plotter.plot_routes(
        phenotype.full_routes,
        problem.node_coordinates,
        axes=ax_routes
    )
    ax_routes.set_title('Vehicle routes in solution')
    ax_routes.set_xlabel('x-coordinate')
    ax_routes.set_ylabel('y-coordinate')

    # PLOTTING THE EVOLUTION OF FEASIBILITY
    amount_feasible = [entry['feasible'] for entry in logbook.chapters['general']]
    ax_feasible = evolution_plotter.plot_fitness(
        amount_feasible,
        axes=ax_feasible
    )
    ax_feasible.set_title('Feasibility over the generations')
    ax_feasible.set_xlabel('generation')
    ax_feasible.set_ylabel('amount feasible')

    plt.show()
