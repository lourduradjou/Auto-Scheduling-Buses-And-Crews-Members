import json
import time

class Crew:
    def __init__(self, crew_data):
        self.id = crew_data['id']
        self.start = crew_data['start'] if crew_data['start'] is not None else 0  # Default to 0 if null
        self.end = crew_data['end'] if crew_data['end'] is not None else 24  # Default to 24 if null
        self.maxWork = crew_data['maxWork']  # Max hours crew can work
        self.role = crew_data['role']  # Conductor or Driver
        self.assigned = False  # Initially, no assignment
        self.resting = False  # Initially, not resting
        self.bus_id = None  # For linked duties

    def can_work(self, trip_start, trip_end, shift_duration, is_linked):
        if self.resting:
            return False  # If resting, can't work
        if is_linked and self.bus_id is not None:
            # Check if the crew is already linked to a bus and ensure they stay on it
            return (self.start <= trip_start and trip_end <= self.end and self.maxWork >= shift_duration)
        elif self.start > self.end:
            return ((self.start <= trip_start or trip_start < self.end) and
                    (self.start <= trip_end or trip_end < self.end) and self.maxWork >= shift_duration)
        else:
            return (self.start <= trip_start and trip_end <= self.end and self.maxWork >= shift_duration)

    def assign(self, bus_id, trip_end, shift_duration):
        """Assign crew to bus and trip, update work hours."""
        self.assigned = True
        self.bus_id = bus_id  # Store bus assignment for linked duty
        self.start = trip_end
        self.maxWork -= shift_duration

    def handover(self):
        """Handover the bus after a trip (for unlinked duty)."""
        self.bus_id = None  # Crew no longer assigned to this bus
        self.resting = True  # Set resting status after handover

    def finish_rest(self):
        """Mark crew as available after resting."""
        self.resting = False

def dynamic_programming_scheduling(crews, trips, buses, is_linked_duty):
    global notAssigned, notAssignedTrips, unassignedCrews
    notAssigned = 0
    notAssignedTrips = []
    unassignedCrews = []
    
    trips.sort(key=lambda x: x['start_time'])
    crew_objects = [Crew(crew) for crew in crews]  # Convert to crew objects

    full_allocated, half_allocated, no_allocated = [], [], []

    # Process each trip
    for trip in trips:
        trip_duration = trip['end_time'] - trip['start_time']
        assigned_conductor, assigned_driver = None, None

        # Try to find a bus and assign crews
        for bus in buses:
            bus_id = bus['id']
            for crew in crew_objects:
                if crew.can_work(trip['start_time'], trip['end_time'], trip_duration, is_linked_duty):
                    # Check role and assign based on linked or unlinked duty
                    if crew.role == 'conductor' and not assigned_conductor:
                        assigned_conductor = crew.id
                        crew.assign(bus_id, trip['end_time'], trip_duration)
                    elif crew.role == 'driver' and not assigned_driver:
                        assigned_driver = crew.id
                        crew.assign(bus_id, trip['end_time'], trip_duration)

                    # If unlinked duty, handle handover logic
                    if not is_linked_duty:
                        crew.handover()

                    # Stop assigning if both roles are filled
                    if assigned_conductor and assigned_driver:
                        break

            if assigned_conductor and assigned_driver:
                break

        # Log assignments
        if assigned_conductor and assigned_driver:
            full_allocated.append({
                'bus_id': bus_id,
                'conductor_id': assigned_conductor,
                'driver_id': assigned_driver,
                'route_id': trip['route_id'],
                'trip_id': trip['trip_id']
            })
        elif assigned_conductor or assigned_driver:
            half_allocated.append({
                'bus_id': bus_id,
                'conductor_id': assigned_conductor,
                'driver_id': assigned_driver,
                'route_id': trip['route_id'],
                'trip_id': trip['trip_id']
            })
        else:
            notAssigned += 1
            notAssignedTrips.append(f"Route {trip['route_id']}, Trip {trip['trip_id']}")
            no_allocated.append({
                'route_id': trip['route_id'],
                'trip_id': trip['trip_id']
            })

    # Mark crews who are not assigned
    for crew in crew_objects:
        if not crew.assigned:
            unassignedCrews.append(crew.id)

    return full_allocated, half_allocated, no_allocated, notAssigned, notAssignedTrips, unassignedCrews


def load_test_case(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['crews'], data['trips'], data['buses']


# Load the test case from the JSON file
crews, trips, buses = load_test_case('./test_cases.json')

# Measure the running time
start_time = time.time()

full_allocated, half_allocated, no_allocated, notAssigned, notAssignedTrips, unassignedCrews = dynamic_programming_scheduling(crews, trips, buses, True)

# Print results
end_time = time.time()

print("Execution Time:", end_time - start_time, "seconds")

# Print detailed allocations
print("\nFull Allocated:")
for assignment in full_allocated:
    print(assignment)

print(f"\nTotal Full Allocated: {len(full_allocated)}")
full_allocated_percentage = (len(full_allocated) / len(trips)) * 100 if trips else 0
print(f"Percentage of Full Allocated: {full_allocated_percentage:.2f}%")

print("\nHalf Allocated:")
for assignment in half_allocated:
    print(assignment)

print(f"\nTotal Half Allocated: {len(half_allocated)}")
half_allocated_percentage = (len(half_allocated) / len(trips)) * 100 if trips else 0
print(f"Percentage of Half Allocated: {half_allocated_percentage:.2f}%")

print("\nNot Allocated:")
for trip in no_allocated:
    print(trip)

print(f"\nTotal Not Allocated: {len(no_allocated)}")
not_allocated_percentage = (len(no_allocated) / len(trips)) * 100 if trips else 0
print(f"Percentage of Not Allocated: {not_allocated_percentage:.2f}%")

print(f"\nTotal number of crews: {len(crews)}")
print(f"Total number of unassigned crews: {len(unassignedCrews)}")
print(f"Unassigned crews: {unassignedCrews}")

assigned_crews = len(crews) - len(unassignedCrews)
print(f"Total number of assigned crews: {assigned_crews}")
print(f"Percentage of crews assigned: {assigned_crews / len(crews) * 100:.2f}%")


# Full Allocated:
# {'bus_id': 'B1', 'conductor_id': 1, 'driver_id': 3, 'route_id': 142, 'trip_id': '142_2'}
# {'bus_id': 'B1', 'conductor_id': 5, 'driver_id': 4, 'route_id': 142, 'trip_id': '142_1'}

# Total Full Allocated: 2
# Percentage of Full Allocated: 66.67%

# Half Allocated:
# {'bus_id': 'B3', 'conductor_id': None, 'driver_id': 6, 'route_id': 142, 'trip_id': '142_3'}

# Total Half Allocated: 1
# Percentage of Half Allocated: 33.33%

# Not Allocated:

# Total Not Allocated: 0
# Percentage of Not Allocated: 0.00%

# Total number of crews: 6
# Total number of unassigned crews: 1
# Unassigned crews: [2]
# Total number of assigned crews: 5
# Percentage of crews assigned: 83.33%
#--------------------------------------------------------------------------------------------------------------------

#Linked scheduling
# Full Allocated:
# {'bus_id': 'B1', 'conductor_id': 1, 'driver_id': 3, 'route_id': 142, 'trip_id': '142_2'}
# {'bus_id': 'B1', 'conductor_id': 2, 'driver_id': 4, 'route_id': 142, 'trip_id': '142_1'}
# {'bus_id': 'B1', 'conductor_id': 5, 'driver_id': 6, 'route_id': 142, 'trip_id': '142_3'}

# Total Full Allocated: 3
# Percentage of Full Allocated: 100.00%

# Half Allocated:

# Total Half Allocated: 0
# Percentage of Half Allocated: 0.00%

# Not Allocated:

# Total Not Allocated: 0
# Percentage of Not Allocated: 0.00%

# Total number of crews: 6
# Total number of unassigned crews: 0
# Unassigned crews: []
# Total number of assigned crews: 6
# Percentage of crews assigned: 100.00%