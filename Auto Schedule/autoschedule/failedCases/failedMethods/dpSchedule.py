import time


def dynamicProgrammingScheduling(crews, buses):
    # Sort crews and buses by their start times
    crews.sort(key=lambda x: x['start'])
    buses.sort(key=lambda x: x['shift_start'])
    
    n = len(buses)
    dp = [None] * (n + 1)
    dp[0] = []

    for i in range(1, n + 1):
        best_assignment = None
        for j in range(i):
            valid_crews = [
                crew for crew in crews
                if crew['start'] <= buses[i - 1]['shift_start'] and crew['end'] >= buses[i - 1]['shift_end']
            ]
            if valid_crews:
                for crew in valid_crews:
                    assignment = dp[j] + [{'bus': buses[i - 1]['id'], 'crew': crew['id']}]
                    if best_assignment is None or len(assignment) > len(best_assignment):
                        best_assignment = assignment
        dp[i] = best_assignment
    
    return dp[n] if dp[n] else [{'bus': bus['id'], 'crew': None} for bus in buses]

# Input data (same as previous examples)
crews = [
    {'id': 101, 'start': 8, 'end': 16},
    {'id': 102, 'start': 9, 'end': 18},
    {'id': 103, 'start': 14, 'end': 22},
    {'id': 104, 'start': 7, 'end': 15},
    {'id': 105, 'start': 10, 'end': 14},
    {'id': 106, 'start': 6, 'end': 10},
    {'id': 107, 'start': 8, 'end': 12},
    {'id': 108, 'start': 5, 'end': 9}
]

buses = [
    {'id': 'B1', 'shift_start': 8, 'shift_end': 12},
    {'id': 'B2', 'shift_start': 10, 'shift_end': 15},
    {'id': 'B3', 'shift_start': 12, 'shift_end': 18},
    {'id': 'B4', 'shift_start': 14, 'shift_end': 20},
    {'id': 'B5', 'shift_start': 6, 'shift_end': 10},
    {'id': 'B6', 'shift_start': 5, 'shift_end': 9},
    {'id': 'B7', 'shift_start': 9, 'shift_end': 14}
]

start_time = time.time()


print(dynamicProgrammingScheduling(crews, buses))

end_time = time.time()

print("Execution Time:", end_time - start_time, "seconds")
