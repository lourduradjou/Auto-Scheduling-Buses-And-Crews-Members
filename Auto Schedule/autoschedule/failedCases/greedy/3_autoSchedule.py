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
                bus_shifts.append({
                    "bus_id": bus["id"],
                    "shift_name": shift,
                    "shift_start": shift_details["shift_start"],
                    "shift_end": shift_details["shift_end"],
                    "crew": None
                })

    # Sort bus shifts by their start times
    bus_shifts.sort(key=lambda x: x['shift_start'])

    assignments = []
    availableCrews = []
    crew_index = 0

    for bus_shift in bus_shifts:
        crew_index = 0
        shift_duration = bus_shift['shift_end'] - bus_shift['shift_start']

        # Remove crews that have completed their shifts or exceeded maxWork
        availableCrews = [crew for crew in availableCrews if crew['end'] >= bus_shift['shift_start'] and crew['maxWork'] >= shift_duration]

        # Add new available crews to the list
        for i in range(len(crews)):
            if crew_index < len(crews) and crews[crew_index]['start'] <= bus_shift['shift_start'] and crews[crew_index]['maxWork'] >= shift_duration:
                availableCrews.append(crews[crew_index])
            crew_index += 1

        # Sort available crews by their end times to prioritize the earliest available
        availableCrews.sort(key=lambda x: x['end'])

        # Assign the first available crew with matching shift preference and sufficient maxWork
        assigned = False
        for crew in availableCrews:
            if crew['start'] <= bus_shift['shift_start'] and crew['end'] >= bus_shift['shift_end'] and crew[bus_shift['shift_name']] == 1 and crew['maxWork'] >= shift_duration:
                assignments.append({'bus': bus_shift['bus_id'], 'crew': crew['id'], 'shift': bus_shift['shift_name']})
                crew['assigned'] = True  # Mark the crew as assigned
                crew['start'] = bus_shift['shift_end']  # Update crew's availability for future assignments
                crew['maxWork'] -= shift_duration  # Reduce the available work hours
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
crews, buses = load_test_case('d:/Auto Schedule/autoschedule/greedy/test_case4.json')
# ---------------------------------------------------------------------------------------
# Measure the running time
start_time = time.time()

# Run the scheduling algorithm
assignments = linkedScheduling(crews, buses)

# Print the results
# print("Assignments:", assignments)

# Measure the end time and calculate the duration
end_time = time.time()

print("Execution Time:", end_time - start_time, "seconds")

# Analysis and Results
print("\nFinal Analysis:")
bus_shifts_len = len(buses) * 4  # Assuming 4 shifts per bus
print(f"Total number of bus shifts: {bus_shifts_len}")
print(f"Total number of crews: {len(crews)}")
print(f"No of bus shifts that didn't get assigned to any crew members: {notAssigned}")
print(f"Buses without assignments: {notAssignedBuses}")
print(f"Total number of unassigned crews: {len(unassignedCrews)}")
print(f"Crews without assignments: {unassignedCrews}")

assigned_crews = len(crews) - len(unassignedCrews)
print(f"Total number of assigned crews: {assigned_crews}")
print(f"Percentage of crews assigned: {assigned_crews / len(crews) * 100:.2f}%")
