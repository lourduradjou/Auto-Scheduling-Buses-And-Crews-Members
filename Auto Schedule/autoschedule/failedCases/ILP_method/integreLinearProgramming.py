from pulp import LpProblem, LpVariable, LpInteger, LpMaximize, lpSum, value, PULP_CBC_CMD
import time
import json

notAssigned = 0
notAssignedBuses = []
unassignedCrews = []

def ilpScheduling(crews, buses):
    # Create a problem variable
    prob = LpProblem("Bus_Scheduling", LpMaximize)

    # Create variables
    x = LpVariable.dicts("assignment", (range(len(buses)), range(len(crews))), 0, 1, LpInteger)

    # Objective function (maximize the number of assigned buses)
    prob += lpSum(x[i][j] for i in range(len(buses)) for j in range(len(crews)))

    # Constraints
    for i, bus in enumerate(buses):
        prob += lpSum(x[i][j] for j in range(len(crews))) == 1  # Each bus is assigned to at most one crew

    for j, crew in enumerate(crews):
        for i, bus in enumerate(buses):
            if not (crew['start'] <= bus['shift_start'] and crew['end'] >= bus['shift_end']):
                prob += x[i][j] == 0  # Crew cannot be assigned if availability does not match

    # Solve the problem with a specific solver to suppress output
    prob.solve(PULP_CBC_CMD(msg=False))

    # Collect the results
    assignments = []
    assigned_crews = set()
    for i, bus in enumerate(buses):
        assigned = False
        for j, crew in enumerate(crews):
            if value(x[i][j]) == 1:
                assignments.append({'bus': bus['id'], 'crew': crew['id']})
                assigned_crews.add(crew['id'])
                assigned = True
                break
        if not assigned:
            assignments.append({'bus': bus['id'], 'crew': None})
            notAssignedBuses.append(bus['id'])
            global notAssigned
            notAssigned += 1
    
    # Find unassigned crews
    for crew in crews:
        if crew['id'] not in assigned_crews:
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

# Test the ILP scheduling
assignments = ilpScheduling(crews, buses)

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



# Assignments: [{'bus': 'B1', 'crew': 466}, {'bus': 'B2', 'crew': 426}, {'bus': 'B3', 'crew': 308}, {'bus': 'B4', 'crew': 33}, {'bus': 'B5', 'crew': 73}, {'bus': 'B6', 'crew': 224}, {'bus': 'B7', 'crew': 366}, {'bus': 'B8', 'crew': 71}, {'bus': 'B9', 'crew': 73}, {'bus': 'B10', 'crew': 95}, {'bus': 'B11', 'crew': 157}, {'bus': 'B12', 'crew': 299}, {'bus': 'B13', 'crew': 76}, {'bus': 'B14', 'crew': 27}, {'bus': 'B15', 'crew': 466}, {'bus': 'B16', 'crew': 245}, {'bus': 'B17', 'crew': 67}, {'bus': 'B18', 'crew': 493}, {'bus': 'B19', 'crew': 245}, {'bus': 'B20', 'crew': 296}, {'bus': 'B21', 'crew': 107}, {'bus': 'B22', 'crew': 73}, {'bus': 'B23', 'crew': 187}, {'bus': 'B24', 'crew': 408}, {'bus': 'B25', 'crew': 245}, {'bus': 'B26', 'crew': 413}, {'bus': 'B27', 'crew': 157}, {'bus': 'B28', 'crew': 382}, {'bus': 'B29', 'crew': 351}, {'bus': 'B30', 'crew': 209}, {'bus': 'B31', 'crew': 408}, {'bus': 'B32', 'crew': 15}, {'bus': 'B33', 'crew': 243}, {'bus': 'B34', 'crew': 291}, {'bus': 'B35', 'crew': 187}, {'bus': 'B36', 'crew': 39}, {'bus': 'B37', 'crew': 111}, {'bus': 'B38', 'crew': 360}, {'bus': 'B39', 'crew': 163}, {'bus': 'B40', 'crew': 103}, {'bus': 'B41', 'crew': 83}, {'bus': 'B42', 'crew': 233}, {'bus': 'B43', 'crew': 9}, {'bus': 'B44', 'crew': 295}, {'bus': 'B45', 'crew': 239}, {'bus': 'B46', 'crew': 245}, {'bus': 'B47', 'crew': 220}, {'bus': 'B48', 'crew': 73}, {'bus': 'B49', 'crew': 73}, {'bus': 'B50', 'crew': 441}, {'bus': 'B51', 'crew': 50}, {'bus': 'B52', 'crew': 73}, {'bus': 'B53', 'crew': 359}, {'bus': 'B54', 'crew': 426}, {'bus': 'B55', 'crew': 187}, {'bus': 'B56', 'crew': 405}, {'bus': 'B57', 'crew': 346}, {'bus': 'B58', 'crew': 284}, {'bus': 'B59', 'crew': 345}, {'bus': 'B60', 'crew': 159}, {'bus': 'B61', 'crew': 208}, {'bus': 'B62', 'crew': 157}, {'bus': 'B63', 'crew': 466}, {'bus': 'B64', 'crew': 178}, {'bus': 'B65', 'crew': 157}, {'bus': 'B66', 'crew': 219}, {'bus': 'B67', 'crew': 254}, {'bus': 'B68', 'crew': 59}, {'bus': 'B69', 'crew': 22}, {'bus': 'B70', 'crew': 232}, {'bus': 'B71', 'crew': 20}, {'bus': 'B72', 'crew': 224}, {'bus': 'B73', 'crew': 441}, {'bus': 'B74', 'crew': 185}, {'bus': 'B75', 'crew': 345}, {'bus': 'B76', 'crew': 120}, {'bus': 'B77', 'crew': 471}, {'bus': 'B78', 'crew': 67}, {'bus': 'B79', 'crew': 127}, {'bus': 'B80', 'crew': 73}, {'bus': 'B81', 'crew': 476}, {'bus': 'B82', 'crew': 224}, {'bus': 'B83', 'crew': 467}, {'bus': 'B84', 'crew': 119}, {'bus': 'B85', 'crew': 293}, {'bus': 'B86', 'crew': 366}, {'bus': 'B87', 'crew': 134}, {'bus': 'B88', 'crew': 23}, {'bus': 'B89', 'crew': 291}, {'bus': 'B90', 'crew': 157}, {'bus': 'B91', 'crew': 111}, {'bus': 'B92', 'crew': 467}, {'bus': 'B93', 'crew': 269}, {'bus': 'B94', 'crew': 175}, {'bus': 'B95', 'crew': 89}, {'bus': 'B96', 'crew': 471}, {'bus': 'B97', 'crew': 452}, {'bus': 'B98', 'crew': 414}, {'bus': 'B99', 'crew': 106}, {'bus': 'B100', 'crew': 108}]
# Execution Time: 2.1749467849731445 seconds

# Final Analysis:
# Total number of buses: 100
# Total number of crews: 500
# No of buses that didn't get assigned to any crew members: 0
# Buses without assignments: []
# Total number of unassigned crews: 429
# Crews without assignments: [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 19, 21, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61, 62, 63, 64, 65, 66, 68, 69, 70, 72, 74, 75, 77, 78, 79, 80, 81, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 96, 97, 98, 99, 100, 101, 102, 104, 105, 109, 110, 112, 113, 114, 115, 116, 117, 118, 121, 122, 123, 124, 125, 126, 128, 129, 130, 131, 132, 133, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 155, 156, 158, 160, 161, 162, 164, 165, 166, 167, 168, 169, 170, 171, 172, 173, 174, 176, 177, 179, 180, 181, 182, 183, 184, 186, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 210, 211, 212, 213, 214, 215, 216, 217, 218, 221, 222, 223, 225, 226, 227, 228, 229, 230, 231, 234, 235, 236, 237, 238, 240, 241, 242, 244, 246, 247, 248, 249, 250, 251, 252, 253, 255, 256, 257, 258, 259, 260, 261, 262, 263, 264, 265, 266, 267, 268, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 285, 286, 287, 288, 289, 290, 292, 294, 297, 298, 300, 301, 302, 303, 304, 305, 306, 307, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339, 340, 341, 342, 343, 344, 347, 348, 349, 350, 352, 353, 354, 355, 356, 357, 358, 361, 362, 363, 364, 365, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 379, 380, 381, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 406, 407, 409, 410, 411, 412, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 427, 428, 429, 430, 431, 432, 433, 434, 435, 436, 437, 438, 439, 440, 442, 443, 444, 445, 446, 447, 448, 449, 450, 451, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 468, 469, 470, 472, 473, 474, 475, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 494, 495, 496, 497, 498, 499, 500]
# Total number of assigned crews: 71
# Percentage of crews assigned: 14.20%