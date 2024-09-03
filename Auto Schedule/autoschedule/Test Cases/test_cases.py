# Test Case: 1
crews = [
    {'id': 101, 'start': 8, 'end': 16},
    {'id': 102, 'start': 9, 'end': 18},
    {'id': 103, 'start': 14, 'end': 22},
    {'id': 104, 'start': 7, 'end': 15},
]

buses = [
    {'id': 'ABC', 'shift_start': 8, 'shift_end': 12},
    {'id': 'DEF', 'shift_start': 10, 'shift_end': 15},
    {'id': 'GHI', 'shift_start': 12, 'shift_end': 18},
    {'id': 'JKL', 'shift_start': 14, 'shift_end': 20},
]

#  Greedy: Perfectly Works
[{'bus': 'ABC', 'crew': 104}, {'bus': 'DEF', 'crew': 101}, {'bus': 'GHI', 'crew': 102}, {'bus': 'JKL', 'crew': 103}]
#  Backtracking also Works
[{'bus': 'ABC', 'crew': 104}, {'bus': 'DEF', 'crew': 101}, {'bus': 'GHI', 'crew': 102}, {'bus': 'JKL', 'crew': 103}]


# Test Case: 2
crews = [
    {'id': 101, 'start': 8, 'end': 16},
    {'id': 102, 'start': 9, 'end': 18},
    {'id': 103, 'start': 14, 'end': 22},
    {'id': 104, 'start': 7, 'end': 15},
    {'id': 105, 'start': 10, 'end': 14},
    {'id': 106, 'start': 6, 'end': 10},
    {'id': 107, 'start': 8, 'end': 12},  # Overlapping start time with different end times
    {'id': 108, 'start': 5, 'end': 9},   # Available before any bus starts
]

buses = [
    {'id': 'B1', 'shift_start': 8, 'shift_end': 12},
    {'id': 'B2', 'shift_start': 10, 'shift_end': 15},
    {'id': 'B3', 'shift_start': 12, 'shift_end': 18},
    {'id': 'B4', 'shift_start': 14, 'shift_end': 20},
    {'id': 'B5', 'shift_start': 6, 'shift_end': 10},
    {'id': 'B6', 'shift_start': 5, 'shift_end': 9},   # Starts before most crews
    {'id': 'B7', 'shift_start': 9, 'shift_end': 14},  # Overlaps with multiple shifts
]

#Greedy works fine:
[{'bus': 'B6', 'crew': 108}, {'bus': 'B5', 'crew': 106}, {'bus': 'B1', 'crew': 107}, {'bus': 'B7', 'crew': 104}, {'bus': 'B2', 'crew': 101}, {'bus': 'B3', 'crew': 102}, {'bus': 'B4', 'crew': 103}]
#Backtracking fails at one case, considering the case of assigning the best possible shift to the crew members
[{'bus': 'B6', 'crew': 108}, {'bus': 'B5', 'crew': 106}, {'bus': 'B1', 'crew': 104}, {'bus': 'B7', 'crew': 101}, {'bus': 'B2', 'crew': 102}, {'bus': 'B3', 'crew': None}, {'bus': 'B4', 'crew': 103}]
# -> failed case: {'bus': 'B3', 'crew': None}
# ILP : Works
[{'bus': 'B1', 'crew': 107}, {'bus': 'B2', 'crew': 104}, {'bus': 'B3', 'crew': 102}, {'bus': 'B4', 'crew': 103}, {'bus': 'B5', 'crew': 106}, {'bus': 'B6', 'crew': 108}, {'bus': 'B7', 'crew': 104}]

# So What we can do now? Which one to choose 


import random

def generate_test_case(num_crews, num_buses):
    crews = []
    buses = []

    # Generate crew members with random start and end times
    for i in range(1, num_crews + 1):
        start_time = random.randint(0, 20)
        end_time = random.randint(start_time + 1, 24)  # Ensure end time is after start time
        crews.append({'id': i, 'start': start_time, 'end': end_time, 'assigned': False})

    # Generate buses with random start and end times
    for j in range(1, num_buses + 1):
        start_time = random.randint(0, 20)
        end_time = random.randint(start_time + 1, 24)  # Ensure end time is after start time
        buses.append({'id': f'B{j}', 'shift_start': start_time, 'shift_end': end_time, 'crew': None})

    return crews, buses

def print_test_case(crews, buses):
    print("Crew Members:")
    for crew in crews:
        print(crew)
    print("\nBuses:")
    for bus in buses:
        print(bus)

# Generate test case with 500 crew members and 100 buses
crews, buses = generate_test_case(500, 100)

# Print the test case
print_test_case(crews, buses)

import json

def save_to_file(filename, crews, buses):
    with open(filename, 'w') as file:
        json.dump({'crews': crews, 'buses': buses}, file, indent=4)

# Save test case to a file
save_to_file('test_case.json', crews, buses)


#In conclusion we can't use 
# the dynamic programming approach or
#  the generic programming approach 
# the constraint programming approach also fails
# both of them aren't efficient for this problem and giving wrong answers

#On the algorithsm we used to solve the problem
# Optimized Greedy - 0.004233360290527344 seconds -  Percentage of crews utilized: 20.00%
# -> extremely constant and efficient , uses bit more employes but balanced one

# Backtracking Approach - 0.0020275115966796875 seconds - Percentage of crews utilized: 19.80%
# -> sometimes it fails for one members
# -> aligns to save the time of the employees and also explore all paths

# Integer Linear Programming - 2.1749467849731445 seconds -  Percentage of crews utilized: 14.20%
# -> Takes bit more time, but stringent use of employees to schedule, useful at the time where we have less employees
# -> takes more time than before 

# Simulation Annealing - 1.3020472526550293 seconds - Percentage of crews utilized: 17.80%
# -> balanced between the time and speed and efficient use of the employees
# -> can be used when we have to optimize the use of both the time and allot employees generously

