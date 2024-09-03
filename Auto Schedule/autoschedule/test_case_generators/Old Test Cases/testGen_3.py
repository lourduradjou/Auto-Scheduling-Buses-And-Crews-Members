#All the test cases first , second and this third one, are works on some random timing, which is not adaptable in realtime
#situations for example the user gives preferences like morning and wishes work in the timing of 14 to 20 , the scheduler won't assign
# to avoid these edge cases , we would handle these situations in the frontend itself incase the employees changes their preferences
# and while seeding in the backend also the values will be handled for smoother and precise scheduling.

import random
import json

def generate_test_case(num_crews, num_buses):
    crews = []
    buses = []

    # Generate crew members with random start, end times, and maxWork hours
    for i in range(1, num_crews + 1):
        start_time = random.randint(0, 20)
        end_time = random.randint(start_time + 1, 24)  # Ensure end time is after start time
        max_work = 8 #random.randint(4, 8)  # Random max work hours between 4 to 8 hours
        crews.append({
            'id': i,
            'start': start_time,
            'end': end_time,
            'morning': random.randint(0, 1),
            'afternoon': random.randint(0, 1),
            'evening': random.randint(0, 1),
            'night': random.randint(0, 1),
            'maxWork': max_work,
            'assigned': False
        })

    # Generate buses with random shift times for each time slot
    for j in range(1, num_buses + 1):
        buses.append({
            'id': f'B{j}',
            'morning': {"shift_start": random.randint(6, 9), "shift_end": random.randint(10, 12), "crew": None},
            'afternoon': {"shift_start": random.randint(12, 15), "shift_end": random.randint(16, 18), "crew": None},
            'evening': {"shift_start": random.randint(18, 21), "shift_end": random.randint(22, 24), "crew": None},
            'night': {"shift_start": random.randint(0, 3), "shift_end": random.randint(4, 6), "crew": None}
        })

    return crews, buses

# def print_test_case(crews, buses):
#     print("Crew Members:")
#     for crew in crews:
#         print(crew)
#     print("\nBuses:")
#     for bus in buses:
#         print(bus)

def save_to_file(filename, crews, buses):
    with open(filename, 'w') as file:
        json.dump({'crews': crews, 'buses': buses}, file, indent=4)

# Generate and print the test case
crews, buses = generate_test_case(5, 5)
#print_test_case(crews, buses)

# Save test case to a file
save_to_file('test_case3.json', crews, buses)
