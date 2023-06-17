import pathlib
import logging
from problem_classes import Lesson, TimeTable
from data_generator import generate_problem, generate_problem_with_initial_solution
from constraints import define_constraints
import optapy.config
from optapy.types import Duration
from optapy import solver_manager_create
from optapy import solver_factory_create, solver_config_create_from_xml_file
from time import time
# solver_config = optapy.config.solver.SolverConfig() \
#     .withEntityClasses(Lesson) \
#     .withSolutionClass(TimeTable) \
#     .withConstraintProviderClass(define_constraints) \
#     .withTerminationSpentLimit(Duration.ofSeconds(90))

# logging.getLogger('optapy').setLevel(logging.DEBUG)

start_time = time()

def f(solution):
    solution.write_to_db()
    score = solution.score.toString()
    hard, soft = score.split('/')
    hard = hard[:-4]
    soft = soft[:-4]
    print(solution.score.toString())
    # with open('scores.txt', 'a') as file:
    #     print(f'{hard},{soft},{time() - start_time}', file=file)

print('0: Построить решение с нуля')
print('1: Использовать уже существующее')
flag = int(input())
time = 3000
if flag:
    solver_config = solver_config_create_from_xml_file(pathlib.Path('solverConfigWith_Initial_solution.xml')) \
        .withConstraintProviderClass(define_constraints) \
        .withTerminationSpentLimit(Duration.ofSeconds(time))

    solution = generate_problem_with_initial_solution()

else:
    solver_config = solver_config_create_from_xml_file(pathlib.Path('solverConfig.xml')) \
                    .withConstraintProviderClass(define_constraints) \
                    .withTerminationSpentLimit(Duration.ofSeconds(time))

    solution = generate_problem()


solver_manager = solver_manager_create(solver_config)
solver_manager.solveAndListen(0, lambda the_id: solution, f)