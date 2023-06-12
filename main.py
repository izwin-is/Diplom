import pathlib
import logging
from problem_classes import Lesson, TimeTable
from data_generator import generate_problem
from constraints import define_constraints
import optapy.config
from optapy.types import Duration
from optapy import solver_manager_create
from optapy import solver_factory_create, solver_config_create_from_xml_file

# solver_config = optapy.config.solver.SolverConfig() \
#     .withEntityClasses(Lesson) \
#     .withSolutionClass(TimeTable) \
#     .withConstraintProviderClass(define_constraints) \
#     .withTerminationSpentLimit(Duration.ofSeconds(90))

# logging.getLogger('optapy').setLevel(logging.DEBUG)

def f(solution):
    solution.write_to_db()
    print(solution.score)



solver_config = solver_config_create_from_xml_file(pathlib.Path('solverConfig.xml')) \
                .withConstraintProviderClass(define_constraints) \
                .withTerminationSpentLimit(Duration.ofSeconds(200))

solution = generate_problem()
solver_manager = solver_manager_create(solver_config)
solver_manager.solveAndListen(0, lambda the_id: solution, f)
# solution = solver_factory_create(solver_config) \
#     .buildSolver() \
#     .solve(generate_problem())
# solution = generate_problem()

# print(solution)