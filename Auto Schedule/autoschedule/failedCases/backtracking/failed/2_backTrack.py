# fails

import json
import time

notAssigned = 0
notAssignedBuses = []
unassignedCrews = []

def is_valid_assignment(bus, crew):
    """
    Check if a crew can be assigned to a bus based on the shift timings.
    """
    if bus.get('shift_start') is None or bus.get('shift_end') is None:
        return False  # Cannot assign if shift timings are not available
    
    is_valid = (crew['start'] <= bus['shift_start'] and
                crew['end'] >= bus['shift_end'] and
                crew['maxWork'] >= (bus['shift_end'] - bus['shift_start']))
    
    # Debug print
    print(f"Checking assignment: Bus {bus['id']} with Crew {crew['id']} - Valid: {is_valid}")
    
    return is_valid

def backtrack(assignments, buses, crews, index, used_crews):
    """
    Backtracking function to assign crews to buses.
    """
    if index == len(buses):
        return True  # All buses have been assigned

    bus = buses[index]
    assigned = False
    for i, crew in enumerate(crews):
        if not used_crews[i] and is_valid_assignment(bus, crew):
            used_crews[i] = True
            assignments.append({'bus': bus['id'], 'crew': crew['id']})
            crew['assigned'] = True  # Mark the crew as assigned
            
            if backtrack(assignments, buses, crews, index + 1, used_crews):
                return True
            
            # Backtrack
            used_crews[i] = False
            assignments.pop()
            assigned = True  # Mark that an assignment was attempted

    # If no valid assignment found
    if not assigned:
        assignments.append({'bus': bus['id'], 'crew': None})
        notAssignedBuses.append(bus['id'])
        global notAssigned
        notAssigned += 1
    
    return backtrack(assignments, buses, crews, index + 1, used_crews)

def linkedScheduling(crews, buses):
    global notAssignedBuses, unassignedCrews, notAssigned
    
    # Remove buses with None shift_start or shift_end
    buses = [bus for bus in buses if bus.get('shift_start') is not None and bus.get('shift_end') is not None]
    
    # Debug print
    print("Filtered Buses:", buses)

    # Sort crews and buses by their start times (after filtering)
    crews.sort(key=lambda x: x['start'])
    buses.sort(key=lambda x: x['shift_start'])

    # Debug print
    print("Sorted Crews:", crews)
    print("Sorted Buses:", buses)
    
    assignments = []
    used_crews = [False] * len(crews)
    
    # Start the backtracking process
    if not backtrack(assignments, buses, crews, 0, used_crews):
        print("No valid assignment found.")
        
    # Find unassigned crews
    for crew in crews:
        if not crew.get('assigned', False):
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

# Run the scheduling algorithm
assignments = linkedScheduling(crews, buses)

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
