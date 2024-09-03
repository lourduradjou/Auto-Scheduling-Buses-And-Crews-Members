import json
import time

class Crew:
    def __init__(self, crew_data):
        self.id = crew_data['id']
        self.start = crew_data['start']
        self.end = crew_data['end']
        self.maxWork = crew_data['maxWork']
        self.shifts = {
            "morning": crew_data.get("morning", 0),
            "afternoon": crew_data.get("afternoon", 0),
            "evening": crew_data.get("evening", 0),
            "night": crew_data.get("night", 0)
        }
        self.assigned = False

    def can_work(self, shift_start, shift_end, shift_duration):
        return (self.start <= shift_start and
                self.end >= shift_end and
                self.maxWork >= shift_duration)

    def assign(self, shift_end, shift_duration):
        self.assigned = True
        self.start = shift_end
        self.maxWork -= shift_duration

def dynamic_programming_scheduling(crews, buses):
    global notAssigned, notAssignedBuses, unassignedCrews, countShifts
    notAssigned = 0
    notAssignedBuses = []
    unassignedCrews = []

    bus_shifts = []
    for bus in buses:
        for shift in ["morning", "afternoon", "evening", "night"]:
            shift_details = bus.get(shift)
            if shift_details and shift_details["shift_start"] is not None and shift_details["shift_end"] is not None:
                bus_shifts.append({
                    "bus_id": bus["id"],
                    "shift_name": shift,
                    "shift_start": shift_details["shift_start"],
                    "shift_end": shift_details["shift_end"],
                    "crew": shift_details["crew"]
                })

    countShifts = len(bus_shifts)
    bus_shifts.sort(key=lambda x: x['shift_start'])

    assignments = []
    crew_objects = [Crew(crew) for crew in crews]

    # DP table to store best assignments up to each shift
    dp = [{} for _ in range(len(bus_shifts))]
    
    # Initialize DP table
    for i, shift in enumerate(bus_shifts):
        shift_duration = shift['shift_end'] - shift['shift_start']
        dp[i]['best_assignments'] = []
        dp[i]['assigned'] = False

        # Collect all possible crews that can work this shift
        possible_crews = [
            crew for crew in crew_objects
            if crew.can_work(shift['shift_start'], shift['shift_end'], shift_duration) and crew.shifts[shift['shift_name']] == 1
        ]

        if possible_crews:
            # Sort possible crews by their end time in ascending order
            possible_crews.sort(key=lambda x: x.end)

            # Pick the crew with the earliest end time
            best_crew = possible_crews[0]

            dp[i]['assigned'] = True
            assignments.append({'bus': shift['bus_id'], 'crew': best_crew.id, 'shift': shift['shift_name']})
            best_crew.assign(shift['shift_end'], shift_duration)

        if not dp[i]['assigned']:
            notAssigned += 1
            notAssignedBuses.append(shift['bus_id'] + " (" + shift['shift_name'] + ")")
            assignments.append({'bus': shift['bus_id'], 'crew': None, 'shift': shift['shift_name']})

    # Collect unassigned crews
    for crew in crew_objects:
        if not crew.assigned:
            unassignedCrews.append(crew.id)

    return assignments, notAssigned, notAssignedBuses, unassignedCrews

def load_test_case(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['crews'], data['buses']

# Load the test case from the JSON file
crews, buses = load_test_case('d:/Auto Schedule/autoschedule/greedy/test_case4.json')

# Measure the running time
start_time = time.time()

assignments, notAssigned, notAssignedBuses, unassignedCrews = dynamic_programming_scheduling(crews, buses)

# Print results
end_time = time.time()

print("Execution Time:", end_time - start_time, "seconds")

print("\nFinal Analysis:")
print(assignments)
bus_shifts_len = countShifts
print(f"Total number of bus shifts: {bus_shifts_len}")
print(f"Total number of crews: {len(crews)}")
print(f"No of bus shifts that didn't get assigned to any crew members: {notAssigned}")
print(f"Buses without assignments: {notAssignedBuses}")
print(f"Total number of unassigned crews: {len(unassignedCrews)}")
print(f"Crews without assignments: {unassignedCrews}")

assigned_crews = len(crews) - len(unassignedCrews)
print(f"Total number of assigned crews: {assigned_crews}")
print(f"Percentage of crews assigned: {assigned_crews / len(crews) * 100:.2f}%")
