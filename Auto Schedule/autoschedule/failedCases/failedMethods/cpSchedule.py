import time
import json

notAssigned = 0
notAssignedBuses = []
unassignedCrews = []

def dynamicProgrammingScheduling(crews, buses):
    """
    Dynamic Programming approach to solve the crew scheduling problem.

    Arguments:
    crews -- A list of dictionaries, each containing 'id', 'start', and 'end' times for the crew availability.
    buses -- A list of dictionaries, each containing 'id', 'shift_start', and 'shift_end' times for the bus shifts.

    Returns:
    A list of dictionaries mapping each bus to an assigned crew.
    If no valid crew is found for a bus, the crew field will be None.
    """
    
    # Sort crews and buses by their start times
    crews.sort(key=lambda x: x['start'])
    buses.sort(key=lambda x: x['shift_start'])
    
    n = len(buses)  # Number of buses
    dp = [None] * (n + 1)  # DP table to store the best assignments up to the i-th bus
    dp[0] = []  # Base case: No buses to assign, so no assignments

    # Iterate through each bus to find the optimal crew assignment
    for i in range(1, n + 1):
        best_assignment = None
        # Check all previous buses to find the best valid assignment
        for j in range(i):
            # Filter valid crews based on availability for the current bus shift
            valid_crews = [
                crew for crew in crews
                if crew['start'] <= buses[i - 1]['shift_start'] and crew['end'] >= buses[i - 1]['shift_end']
            ]
            # Assign the crew that maximizes the number of valid assignments
            if valid_crews:
                for crew in valid_crews:
                    assignment = dp[j] + [{'bus': buses[i - 1]['id'], 'crew': crew['id']}]
                    # Keep track of the best assignment found so far
                    if best_assignment is None or len(assignment) > len(best_assignment):
                        best_assignment = assignment
        dp[i] = best_assignment  # Store the best assignment found for the i-th bus
    
    # Prepare the final assignment and update global tracking variables
    assignments = dp[n] if dp[n] else [{'bus': bus['id'], 'crew': None} for bus in buses]

    for assignment in assignments:
        if assignment['crew'] is None:
            notAssignedBuses.append(assignment['bus'])
            global notAssigned
            notAssigned += 1
        else:
            assigned_crew = next(crew for crew in crews if crew['id'] == assignment['crew'])
            assigned_crew['assigned'] = True
    
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
crews, buses = load_test_case('d:/Bus_Scheduling_SIH_2024/autoschedule/test_case.json')
# ---------------------------------------------------------------------------------------


# Measure the running time
start_time = time.time()

# Run the scheduling algorithm
assignments = dynamicProgrammingScheduling(crews, buses)

# Print the results
print("Assignments:", assignments)

# Measure the end time and calculate the duration
end_time = time.time()
print("Execution Time:", end_time - start_time, "seconds")

# Analysis and Results
print("\nFinal Analysis:")
print(f"Total number of buses: {len(buses)}")
print(f"Total number of crews: {len(crews)}")
print(f"No of buses that didn't get assigned to any crew members: {notAssigned}")
print(f"Buses without assignments: {notAssignedBuses}")
print(f"Total number of unassigned crews: {len(unassignedCrews)}")
print(f"Crews without assignments: {unassignedCrews}")

assigned_crews = len(crews) - len(unassignedCrews)
print(f"Total number of assigned crews: {assigned_crews}")
print(f"Percentage of crews assigned: {assigned_crews / len(crews) * 100:.2f}%")


# Assignments: [{'bus': 'B3', 'crew': 5}, {'bus': 'B17', 'crew': 5}, {'bus': 'B65', 'crew': 157}, {'bus': 'B78', 'crew': 58}, {'bus': 'B83', 'crew': 58}, {'bus': 'B32', 'crew': 58}, {'bus': 'B30', 'crew': 5}, {'bus': 'B42', 'crew': 1}, {'bus': 'B62', 'crew': 157}, {'bus': 'B89', 'crew': 58}, {'bus': 'B27', 'crew': 157}, {'bus': 'B28', 'crew': 58}, {'bus': 'B47', 'crew': 58}, {'bus': 'B48', 'crew': 5}, {'bus': 'B80', 'crew': 157}, {'bus': 'B92', 'crew': 5}, {'bus': 'B96', 'crew': 58}, {'bus': 'B11', 'crew': 157}, {'bus': 'B13', 'crew': 157}, {'bus': 'B22', 'crew': 157}, {'bus': 'B31', 'crew': 157}, {'bus': 'B29', 'crew': 5}, {'bus': 'B38', 'crew': 58}, {'bus': 'B40', 'crew': 5}, {'bus': 'B77', 'crew': 5}, {'bus': 'B98', 'crew': 157}, {'bus': 'B5', 'crew': 157}, {'bus': 'B23', 'crew': 157}, {'bus': 'B41', 'crew': 157}, {'bus': 'B55', 'crew': 157}, {'bus': 'B63', 'crew': 58}, {'bus': 'B79', 'crew': 58}, {'bus': 'B9', 'crew': 157}, {'bus': 'B36', 'crew': 58}, {'bus': 'B67', 'crew': 157}, {'bus': 'B73', 'crew': 157}, {'bus': 'B12', 'crew': 58}, {'bus': 'B16', 'crew': 157}, {'bus': 'B18', 'crew': 58}, {'bus': 'B35', 'crew': 157}, {'bus': 'B57', 'crew': 157}, {'bus': 'B66', 'crew': 157}, {'bus': 'B74', 'crew': 157}, {'bus': 'B85', 'crew': 58}, {'bus': 'B10', 'crew': 58}, {'bus': 'B21', 'crew': 58}, {'bus': 'B70', 'crew': 58}, {'bus': 'B86', 'crew': 58}, {'bus': 'B8', 'crew': 58}, {'bus': 'B43', 'crew': 58}, {'bus': 'B46', 'crew': 157}, {'bus': 'B50', 'crew': 157}, {'bus': 'B52', 'crew': 157}, {'bus': 'B1', 'crew': 58}, {'bus': 'B4', 'crew': 58}, {'bus': 'B15', 'crew': 157}, {'bus': 'B19', 'crew': 58}, {'bus': 'B33', 'crew': 58}, {'bus': 'B71', 'crew': 157}, {'bus': 'B45', 'crew': 58}, {'bus': 'B49', 'crew': 157}, {'bus': 'B53', 'crew': 58}, {'bus': 'B72', 'crew': 58}, {'bus': 'B76', 'crew': 157}, {'bus': 'B82', 'crew': 157}, {'bus': 'B44', 'crew': 157}, {'bus': 'B56', 'crew': 58}, {'bus': 'B2', 'crew': 157}, {'bus': 'B34', 'crew': 58}, {'bus': 'B39', 'crew': 157}, {'bus': 'B54', 'crew': 157}, {'bus': 'B58', 'crew': 58}, {'bus': 'B88', 'crew': 157}, {'bus': 'B93', 'crew': 58}, {'bus': 'B95', 'crew': 157}, {'bus': 'B14', 'crew': 157}, {'bus': 'B20', 'crew': 157}, {'bus': 'B24', 'crew': 157}, {'bus': 'B59', 'crew': 58}, {'bus': 'B61', 'crew': 157}, {'bus': 'B68', 'crew': 58}, {'bus': 'B69', 'crew': 157}, {'bus': 'B75', 'crew': 58}, {'bus': 'B81', 'crew': 157}, {'bus': 'B97', 'crew': 157}, {'bus': 'B60', 'crew': 58}, {'bus': 'B84', 'crew': 157}, {'bus': 'B90', 'crew': 157}, {'bus': 'B91', 'crew': 157}, {'bus': 'B99', 'crew': 157}, {'bus': 'B7', 'crew': 157}, {'bus': 'B64', 'crew': 157}, {'bus': 'B94', 'crew': 157}, {'bus': 'B25', 'crew': 157}, {'bus': 'B26', 'crew': 157}, {'bus': 'B37', 'crew': 157}, {'bus': 'B51', 'crew': 157}, {'bus': 'B87', 'crew': 157}, {'bus': 'B6', 'crew': 157}, {'bus': 'B100', 'crew': 157}]
# Execution Time: 0.9689610004425049 seconds

# Final Analysis:
# Total number of buses: 100
# Total number of crews: 500
# No of buses that didn't get assigned to any crew members: 0
# Buses without assignments: []
# Total number of unassigned crews: 496
# Crews without assignments: [67, 97, 100, 136, 150, 167, 174, 197, 210, 308, 321, 329, 342, 357, 392, 403, 467, 15, 64, 77, 90, 141, 184, 190, 216, 228, 230, 255, 263, 269, 291, 299, 351, 380, 382, 424, 27, 29, 38, 49, 62, 73, 75, 94, 153, 155, 186, 200, 209, 212, 223, 232, 233, 325, 332, 335, 350, 360, 397, 411, 414, 415, 433, 441, 471, 482, 21, 54, 79, 121, 122, 138, 144, 168, 176, 207, 220, 239, 270, 294, 298, 300, 323, 328, 341, 368, 404, 408, 431, 437, 440, 455, 474, 16, 17, 31, 35, 39, 51, 70, 72, 76, 99, 107, 128, 204, 289, 315, 347, 363, 366, 370, 466, 499, 4, 25, 103, 127, 149, 187, 194, 205, 222, 245, 253, 256, 278, 284, 297, 313, 379, 386, 398, 416, 425, 447, 454, 475, 491, 498, 11, 24, 26, 36, 47, 59, 61, 66, 83, 93, 98, 129, 192, 193, 213, 219, 225, 229, 244, 254, 257, 260, 267, 276, 306, 338, 345, 385, 422, 453, 3, 68, 101, 105, 132, 145, 152, 218, 243, 290, 303, 320, 339, 346, 420, 479, 490, 9, 14, 28, 125, 133, 139, 143, 151, 177, 183, 195, 231, 248, 262, 268, 272, 340, 367, 376, 390, 393, 395, 405, 409, 435, 446, 452, 472, 44, 48, 78, 85, 91, 158, 175, 185, 202, 215, 224, 227, 252, 277, 293, 316, 331, 354, 361, 364, 373, 402, 407, 410, 412, 492, 493, 20, 46, 74, 82, 95, 96, 110, 120, 137, 142, 172, 201, 226, 237, 258, 261, 266, 307, 309, 365, 377, 383, 436, 450, 469, 494, 496, 8, 32, 33, 71, 111, 154, 159, 161, 165, 178, 240, 271, 275, 288, 296, 302, 324, 334, 343, 374, 418, 438, 485, 12, 34, 37, 40, 115, 135, 140, 191, 238, 242, 301, 318, 389, 439, 483, 487, 497, 53, 81, 86, 92, 114, 166, 169, 182, 199, 206, 217, 251, 279, 295, 305, 319, 330, 337, 356, 359, 388, 419, 426, 427, 444, 457, 470, 476, 10, 13, 23, 41, 56, 65, 124, 162, 171, 198, 214, 322, 353, 375, 434, 445, 458, 460, 463, 465, 477, 478, 18, 22, 55, 69, 89, 102, 104, 116, 117, 146, 148, 160, 163, 208, 236, 246, 247, 273, 344, 355, 371, 372, 391, 394, 448, 462, 464, 481, 84, 106, 112, 113, 134, 203, 211, 221, 264, 286, 287, 292, 304, 311, 348, 358, 362, 384, 399, 430, 449, 461, 473, 489, 6, 7, 42, 50, 57, 63, 87, 88, 119, 156, 170, 196, 249, 281, 283, 285, 327, 333, 349, 369, 381, 401, 406, 486, 488, 500, 2, 45, 60, 80, 179, 180, 274, 326, 336, 352, 387, 413, 421, 443, 456, 468, 495, 43, 52, 118, 123, 130, 164, 173, 234, 235, 250, 259, 265, 282, 310, 314, 378, 400, 417, 423, 432, 451, 459, 484, 19, 30, 108, 109, 126, 131, 147, 181, 188, 189, 241, 280, 312, 317, 396, 428, 429, 442, 480]
# Total number of assigned crews: 4
# Percentage of crews assigned: 0.80%