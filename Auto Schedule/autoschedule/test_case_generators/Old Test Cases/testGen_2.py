import random

def generate_test_case(num_crews, num_buses):
    crews = []
    buses = []

    # Define the time ranges for each shift
    shifts = {
        'morning': (5, 12),
        'afternoon': (12, 18),
        'evening': (18, 24),
        'night': (0, 5)
    }

    # Generate crew members with random shift preferences
    for i in range(1, num_crews + 1):
        crew = {
            'id': i,
            'shifts': {
                'morning': random.choice([0, 1]),
                'afternoon': random.choice([0, 1]),
                'evening': random.choice([0, 1]),
                'night': random.choice([0, 1])
            },
            'assigned': False
        }
        crews.append(crew)

    # Generate buses with random start and end times within a shift
    for j in range(1, num_buses + 1):
        shift_name = random.choice(list(shifts.keys()))
        shift_start, shift_end = shifts[shift_name]

        # Randomize the bus's actual start and end times within the chosen shift
        bus_start_time = random.randint(shift_start, shift_end - 1)
        bus_end_time = random.randint(bus_start_time + 1, shift_end)

        bus = {
            'id': f'B{j}',
            'shift_name': shift_name,
            'shift_start': bus_start_time,
            'shift_end': bus_end_time,
            'crew': None
        }
        buses.append(bus)

    return crews, buses

def print_test_case(crews, buses):
    print("Crew Members:")
    for crew in crews:
        print(crew)
    print("\nBuses:")
    for bus in buses:
        print(bus)

# Generate test case with 500 crew members and 100 buses
crews, buses = generate_test_case(100, 100)

# Print the test case
print_test_case(crews, buses)

import json

def save_to_file(filename, crews, buses):
    with open(filename, 'w') as file:
        json.dump({'crews': crews, 'buses': buses}, file, indent=4)

# Save test case to a file
save_to_file('test_case2.json', crews, buses)
