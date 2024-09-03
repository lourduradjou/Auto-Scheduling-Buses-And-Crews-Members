import random
import json

def generate_shift_times(shift_type):
    """Generate dynamic shift start and end times based on the shift type."""
    shift_ranges = {
        'morning': (6, 12),
        'afternoon': (12, 18),
        'evening': (18, 24),
        'night': (0, 6)
    }
    
    start, end = shift_ranges[shift_type]
    shift_start = random.randint(start, end - 1)
    shift_end = random.randint(shift_start + 1, end)  # Ensure end is after start
    
    return shift_start, shift_end

def generate_test_case(num_crews, num_buses):
    crews = []
    buses = []

    # Generate bus shift times for each bus
    for j in range(1, num_buses + 1):
        # Decide which shifts are needed for this bus
        shift_types = random.sample(['morning', 'afternoon', 'evening', 'night'], k=random.randint(1, 4))
        
        bus_shifts = {}
        for shift_type in shift_types:
            start_time, end_time = generate_shift_times(shift_type)
            bus_shifts[shift_type] = {"shift_start": start_time, "shift_end": end_time, "crew": None}
        
        # Add empty shifts for any shift types not included
        all_shifts = ['morning', 'afternoon', 'evening', 'night']
        for shift_type in all_shifts:
            if shift_type not in bus_shifts:
                bus_shifts[shift_type] = {"shift_start": None, "shift_end": None, "crew": None}
        
        buses.append({
            'id': f'B{j}',
            **bus_shifts
        })

    # Generate crew members with at least two shift preferences
    for i in range(1, num_crews + 1):
        # Randomly choose at least two shift preferences
        preferences = random.sample(['morning', 'afternoon', 'evening', 'night'], k=random.randint(2, 4))
        shift_start_end = {
            'morning': (6, 12),
            'afternoon': (12, 18),
            'evening': (18, 24),
            'night': (0, 6)
        }

        # Determine the start and end times based on preferences
        start_time = min(shift_start_end[pref][0] for pref in preferences)
        end_time = max(shift_start_end[pref][1] for pref in preferences)

        # Create a crew member with multiple preferences
        crew = {
            'id': i,
            'start': start_time,
            'end': end_time,
            'morning': 1 if 'morning' in preferences else 0,
            'afternoon': 1 if 'afternoon' in preferences else 0,
            'evening': 1 if 'evening' in preferences else 0,
            'night': 1 if 'night' in preferences else 0,
            'maxWork': 8,  # Static maxWork hours
            'assigned': False
        }

        crews.append(crew)

    return crews, buses

def save_to_file(filename, crews, buses):
    with open(filename, 'w') as file:
        json.dump({'crews': crews, 'buses': buses}, file, indent=4)

# Generate and save the test case
#crews, buses
crews, buses = generate_test_case(12000, 5000)
save_to_file('test_case4.json', crews, buses)


# import random
# import json

# def generate_shift_times(shift_type):
#     """Generate dynamic shift start and end times based on the shift type."""
#     shift_ranges = {
#         'morning': (6, 12),
#         'afternoon': (12, 18),
#         'evening': (18, 24),
#         'night': (0, 6)
#     }
    
#     start, end = shift_ranges[shift_type]
#     shift_start = random.randint(start, end - 1)
#     shift_end = random.randint(shift_start + 1, end)  # Ensure end is after start
    
#     return shift_start, shift_end

# def generate_test_case(num_crews, num_buses):
#     crews = []
#     buses = []

#     # Generate bus shift times for each bus
#     for j in range(1, num_buses + 1):
#         # Decide which shifts are needed for this bus
#         shift_types = random.sample(['morning', 'afternoon', 'evening', 'night'], k=random.randint(1, 4))
        
#         bus_shifts = {}
#         for shift_type in shift_types:
#             start_time, end_time = generate_shift_times(shift_type)
#             bus_shifts[shift_type] = {"shift_start": start_time, "shift_end": end_time, "crew": None}
        
#         # Add empty shifts for any shift types not included
#         all_shifts = ['morning', 'afternoon', 'evening', 'night']
#         for shift_type in all_shifts:
#             if shift_type not in bus_shifts:
#                 bus_shifts[shift_type] = {"shift_start": None, "shift_end": None, "crew": None}
        
#         buses.append({
#             'id': f'B{j}',
#             **bus_shifts
#         })

#     # Generate crew members with at least two shift preferences
#     for i in range(1, num_crews + 1):
#         # Randomly choose at least two shift preferences
#         preferences = random.sample(['morning', 'afternoon', 'evening', 'night'], k=random.randint(2, 4))
#         shift_start_end = {
#             'morning': (6, 12),
#             'afternoon': (12, 18),
#             'evening': (18, 24),
#             'night': (0, 6)
#         }

#         # Determine the start and end times based on preferences
#         start_time = 0
#         end_time = 24

#         # Create a crew member with multiple preferences
#         crew = {
#             'id': i,
#             'start': start_time,
#             'end': end_time,
#             'morning': 1 ,
#             'afternoon': 1,
#             'evening': 1,
#             'night': 1,
#             'maxWork': 8,  # Static maxWork hours
#             'assigned': False
#         }

#         crews.append(crew)

#     return crews, buses

# def save_to_file(filename, crews, buses):
#     with open(filename, 'w') as file:
#         json.dump({'crews': crews, 'buses': buses}, file, indent=4)

# # Generate and save the test case
# #crews, buses
# crews, buses = generate_test_case(12000, 5000)
# save_to_file('test_case4.json', crews, buses)
