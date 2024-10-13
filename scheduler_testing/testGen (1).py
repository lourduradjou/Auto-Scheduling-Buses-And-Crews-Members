import random
import json

def generate_employee_shift_preferences(num_crews):
    """Generate crew members without predefined shift preferences and ensure flexible shift assignments."""
    crews = []
    
    for i in range(1, num_crews + 1):
        role = random.choice(['conductor', 'driver'])  # Randomly assign role

        # Create a crew member with role and no fixed shift preferences
        crew = {
            'id': i,
            'start': None,  # Start time to be assigned later based on the trip
            'end': None,    # End time will be dynamically assigned
            'role': role,   # Conductor or Driver
            'maxWork': 8,   # Max work hours per day
            'assigned': False  # Initially not assigned to any route/trip
        }

        crews.append(crew)
    
    return crews

def generate_buses(num_buses):
    """Generate a list of buses with no assignment initially."""
    buses = [{'id': f'B{j}', 'route_id': None, 'trip_id': None} for j in range(1, num_buses + 1)]
    return buses

def generate_trips(route_id, num_trips):
    """Generate trips for a given route_id, with start and end times, including return trip considerations."""
    trips = []
    
    for trip_num in range(1, num_trips + 1):
        trip_id = f"{route_id}_{trip_num}"  # Unique trip ID for this route
        
        # Trip scheduling - consider both trip and return trip time.
        trip_start = random.randint(0, 18)  # Start hour between 0 and 18 to allow for both trip and return trip
        duration = random.randint(1, 3)  # Random trip duration between 1 and 3 hours
        trip_end = trip_start + duration  # Ensure trip end is after start
        
        return_start = trip_end  # Return trip starts after the outbound trip ends
        return_duration = duration  # Assume return trip takes the same time
        return_end = return_start + return_duration  # Ensure return end time

        # Adjust to 24-hour format (wrap around if necessary)
        if return_end > 24:
            return_end = return_end % 24

        trip = {
            'route_id': route_id,
            'trip_id': trip_id,
            'start_time': trip_start,
            'end_time': trip_end,
            'return_start_time': return_start,
            'return_end_time': return_end
        }
        
        trips.append(trip)
    
    return trips

def save_to_file(filename, crews, buses, trips):
    """Save the generated test case data to a JSON file."""
    with open(filename, 'w') as file:
        json.dump({'crews': crews, 'buses': buses, 'trips': trips}, file, indent=4)

# Generate test cases with employees, buses, and trips
num_crews = 6
num_buses = 3
route_id = 142
num_trips = 3

crews = generate_employee_shift_preferences(num_crews)
buses = generate_buses(num_buses)
trips = generate_trips(route_id, num_trips)

# Save to file
save_to_file('test_cases.json', crews, buses, trips)
