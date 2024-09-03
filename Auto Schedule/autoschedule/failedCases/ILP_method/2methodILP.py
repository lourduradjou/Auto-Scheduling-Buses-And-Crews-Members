from pulp import LpProblem, LpVariable, LpInteger, LpMaximize, lpSum, value, PULP_CBC_CMD
import time
import json

notAssigned = 0
notAssignedBuses = []
unassignedCrews = []

def is_valid_assignment(bus, crew):
    # Check if shift start or end is None
    if bus.get('shift_start') is None or bus.get('shift_end') is None:
        return False
    if crew.get('start') is None or crew.get('end') is None:
        return False
    # Check if the crew can handle the bus shift
    return (crew['start'] <= bus['shift_start'] and
            crew['end'] >= bus['shift_end'] and
            crew.get('maxWork', 0) >= (bus['shift_end'] - bus['shift_start']))

def ilpScheduling(crews, buses):
    global notAssignedBuses, unassignedCrews, notAssigned

    # Create a problem variable
    prob = LpProblem("Bus_Scheduling", LpMaximize)

    # Create variables
    x = LpVariable.dicts("assignment", (range(len(buses)), range(len(crews))), 0, 1, LpInteger)

    # Objective function (maximize the number of assigned buses)
    prob += lpSum(x[i][j] for i in range(len(buses)) for j in range(len(crews)))

    # Constraints
    for i, bus in enumerate(buses):
        prob += lpSum(x[i][j] for j in range(len(crews))) == 1  # Each bus is assigned to at most one crew

    for j, crew in enumerate(crews):
        for i, bus in enumerate(buses):
            if not is_valid_assignment(bus, crew):
                prob += x[i][j] == 0  # Crew cannot be assigned if availability does not match

    # Solve the problem with a specific solver to suppress output
    prob.solve(PULP_CBC_CMD(msg=False))

    # Collect the results
    assignments = []
    assigned_crews = set()
    for i, bus in enumerate(buses):
        assigned = False
        for j, crew in enumerate(crews):
            if value(x[i][j]) == 1:
                assignments.append({'bus': bus['id'], 'crew': crew['id']})
                assigned_crews.add(crew['id'])
                assigned = True
                break
        if not assigned:
            assignments.append({'bus': bus['id'], 'crew': None})
            notAssignedBuses.append(bus['id'])
            notAssigned += 1
    
    # Find unassigned crews
    for crew in crews:
        if crew['id'] not in assigned_crews:
            unassignedCrews.append(crew['id'])

    return assignments

# Loading the test dataset -----------------------------------------
def load_test_case(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['crews'], data['buses']

# Load the test case from the JSON file
crews, buses = load_test_case('d:/Bus_Scheduling_SIH_2024/autoschedule/greedy/test_case4.json')

# Measure the running time
start_time = time.time()

# Test the ILP scheduling
assignments = ilpScheduling(crews, buses)

# Print the results
print("Assignments:", assignments)

# Measure the end time and calculate the duration
end_time = time.time()
print("Execution Time:", end_time - start_time, "seconds")

# Analysis and Results
print("\nFinal Analysis:")
print(f"Total number of buses: {len(buses)}")
print(f"Total number of crews: {len(crews)}")
print(f"No of buses that didn't get assigned to any crew members: {notAssigned}")
print(f"Buses without assignments: {notAssignedBuses}")
print(f"Total number of unassigned crews: {len(unassignedCrews)}")
print(f"Crews without assignments: {unassignedCrews}")

assigned_crews = len(crews) - len(unassignedCrews)
print(f"Total number of assigned crews: {assigned_crews}")
print(f"Percentage of crews assigned: {assigned_crews / len(crews) * 100:.2f}%")
