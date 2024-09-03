#This algorithm was made just considering the prefered time of the employees , and how to schedule
#and with the existing buses as efficient and precise as possible , 
#deeper, realtime, complex cases are considered and implement in this part
# Fails in what case: as in the problem statement it mentions we have to schedule in a way that employees won't exceed their alloted time , kinda avoid overworking
# this algo , allots a worker even if he/she worked their part, makes use of overworking, this could be used, if overworking is find (ha ha sadly it will happen)
# But in the next phase i will try to improvise this , to allot only if they have a remaining period to work.

import json
import time

notAssigned = 0
bus_shifts_len = 0
notAssignedBuses = []
unassignedCrews = []

def linkedScheduling(crews, buses):
    global notAssigned, notAssignedBuses, unassignedCrews
    
    # Flatten the buses structure to handle each shift separately
    bus_shifts = []
    for bus in buses:
        for shift in ["morning", "afternoon", "evening", "night"]:
            shift_details = bus.get(shift)
            if shift_details and shift_details["crew"] is None:  # If the shift is active
                bus_shifts.append({"bus_id": bus["id"], "shift_name": shift, "shift_start": shift_details["shift_start"], "shift_end": shift_details["shift_end"], "crew": None})


    # Sort bus shifts by their start times
    bus_shifts.sort(key=lambda x: x['shift_start'])

    assignments = []
    availableCrews = []
    crew_index = 0

    for bus_shift in bus_shifts:
        crew_index = 0
        # Remove crews that have completed their shifts
        while availableCrews and availableCrews[0]['end'] < bus_shift['shift_start']:
            print(availableCrews[0])
            availableCrews.pop(0)

        # Add new available crews to the list
        for i in range(len(crews)):
            if crew_index < len(crews) and crews[crew_index]['start'] <= bus_shift['shift_start']:
                availableCrews.append(crews[crew_index])
            crew_index += 1

        # Sort available crews by their end times to prioritize the earliest available
        availableCrews.sort(key=lambda x: x['end'])

        # Assign the first available crew with matching shift preference
        assigned = False
        for crew in availableCrews:
            if crew['start'] <= bus_shift['shift_start'] and crew['end'] >= bus_shift['shift_end'] and crew[bus_shift['shift_name']] == 1:
                assignments.append({'bus': bus_shift['bus_id'], 'crew': crew['id'], 'shift': bus_shift['shift_name']})
                crew['assigned'] = True  # Mark the crew as assigned
                crew['start'] = bus_shift['shift_end']  # Update crew's availability for future assignments
                availableCrews.remove(crew)
                assigned = True
                break

        if not assigned:
            assignments.append({'bus': bus_shift['bus_id'], 'crew': None, 'shift': bus_shift['shift_name']})  # No available crew for this bus shift
            notAssigned += 1
            notAssignedBuses.append(bus_shift['bus_id'] + " (" + bus_shift['shift_name'] + ")")

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
# crews, buses = load_test_case('d:/Bus_Scheduling_SIH_2024/autoschedule/test_case2.json')
# print(crews, buses)
# ---------------------------------------------------------------------------------------
crews = [
    {"id": 452, "start": 8, "end": 24, "morning": 1, "afternoon": 0, "evening": 1, "night": 0,"maxWork": 8, "assigned": False},
    {"id": 453, "start": 6, "end": 22, "morning": 1, "afternoon": 1, "evening": 0, "night": 1, "assigned": False},
    {"id": 454, "start": 12, "end": 20, "morning": 0, "afternoon": 1, "evening": 1, "night": 0, "assigned": False},
]

buses = [
    {"id": "B1", "morning": {"shift_start": 8, "shift_end": 12, "crew": None},
                 "afternoon": {"shift_start": 12, "shift_end": 16, "crew": None},
                 "evening": {"shift_start": 16, "shift_end": 20, "crew": None},
                 "night": {"shift_start": 20, "shift_end": 24, "crew": None}},
    {"id": "B2", "morning": {"shift_start": 6, "shift_end": 10, "crew": None},
                 "afternoon": {"shift_start": 10, "shift_end": 14, "crew": None},
                 "evening": {"shift_start": 14, "shift_end": 18, "crew": None},
                 "night": {"shift_start": 18, "shift_end": 22, "crew": None}},
]

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
print(bus_shifts_len)
print(f"Total number of bus shifts: {bus_shifts_len}")
print(f"Total number of crews: {len(crews)}")
print(f"No of bus shifts that didn't get assigned to any crew members: {notAssigned}")
print(f"Buses without assignments: {notAssignedBuses}")
print(f"Total number of unassigned crews: {len(unassignedCrews)}")
print(f"Crews without assignments: {unassignedCrews}")

assigned_crews = len(crews) - len(unassignedCrews)
print(f"Total number of assigned crews: {assigned_crews}")
print(f"Percentage of crews assigned: {assigned_crews / len(crews) * 100:.2f}%")
