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