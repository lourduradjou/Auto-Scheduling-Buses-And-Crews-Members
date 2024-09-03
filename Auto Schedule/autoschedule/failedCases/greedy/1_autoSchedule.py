#Initially the algorithm was made just considering the prefered time of the employees , and how to schedule
#and with the existing buses as efficient and precise as possible , 
#deeper, realtime, complex cases will be considered next to adopt realtime situations.

import json
import time

notAssigned = 0
notAssignedBuses = []
unassignedCrews = []

def linkedScheduling(crews, buses):
    global notAssigned, notAssignedBuses, unassignedCrews
    
    # Sort crews and buses by their start times
    crews.sort(key=lambda x: x['start'])
    buses.sort(key=lambda x: x['shift_start'])

    assignments = []
    availableCrews = []
    crew_index = 0

    for bus in buses:
        # Remove crews that have completed their shifts
        while availableCrews and availableCrews[0]['end'] < bus['shift_start']:
            availableCrews.pop(0)

        # Add new available crews to the list
        while crew_index < len(crews) and crews[crew_index]['start'] <= bus['shift_start']:
            availableCrews.append(crews[crew_index])
            crew_index += 1

        # Sort available crews by their end times to prioritize the earliest available
        availableCrews.sort(key=lambda x: x['end'])

        # Assign the first available crew with priority rules
        assigned = False
        for crew in availableCrews:
            if crew['start'] <= bus['shift_start'] and crew['end'] >= bus['shift_end']:
                assignments.append({'bus': bus['id'], 'crew': crew['id']})
                crew['assigned'] = True  # Mark the crew as assigned
                crew['start'] = bus['shift_end']  # Update crew's availability for future assignments
                availableCrews.remove(crew)
                assigned = True
                break

        if not assigned:
            assignments.append({'bus': bus['id'], 'crew': None})  # No available crew for this bus
            notAssigned += 1
            notAssignedBuses.append(bus['id'])

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
assignments = linkedScheduling(crews, buses)

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


# Assignments: [{'bus': 'B3', 'crew': 5}, {'bus': 'B17', 'crew': 136}, {'bus': 'B65', 'crew': 157}, {'bus': 'B78', 'crew': 167}, {'bus': 'B83', 'crew': 467}, {'bus': 'B32', 'crew': 77}, {'bus': 'B30', 'crew': 216}, {'bus': 'B42', 'crew': 357}, {'bus': 'B62', 'crew': 64}, {'bus': 'B89', 'crew': 230}, {'bus': 'B27', 'crew': 269}, {'bus': 'B28', 'crew': 440}, {'bus': 'B47', 'crew': 474}, {'bus': 'B48', 'crew': 90}, {'bus': 'B80', 'crew': 441}, {'bus': 'B92', 'crew': 380}, {'bus': 'B96', 'crew': 197}, {'bus': 'B11', 'crew': 73}, {'bus': 'B13', 'crew': 184}, {'bus': 'B22', 'crew': 466}, {'bus': 'B31', 'crew': 54}, {'bus': 'B29', 'crew': 482}, {'bus': 'B38', 'crew': 350}, {'bus': 'B40', 'crew': 455}, {'bus': 'B77', 'crew': 121}, {'bus': 'B98', 'crew': 291}, {'bus': 'B5', 'crew': 471}, {'bus': 'B23', 'crew': 76}, {'bus': 'B41', 'crew': 245}, {'bus': 'B55', 'crew': 351}, {'bus': 'B63', 'crew': 360}, {'bus': 'B79', 'crew': 263}, {'bus': 'B9', 'crew': 83}, {'bus': 'B36', 'crew': 308}, {'bus': 'B67', 'crew': 153}, {'bus': 'B73', 'crew': 408}, {'bus': 'B12', 'crew': 222}, {'bus': 'B16', 'crew': 31}, {'bus': 'B18', 'crew': 15}, {'bus': 'B35', 'crew': 187}, {'bus': 'B57', 'crew': 155}, {'bus': 'B66', 'crew': 219}, {'bus': 'B74', 'crew': 35}, {'bus': 'B85', 'crew': 382}, {'bus': 'B10', 'crew': 253}, {'bus': 'B21', 'crew': 491}, {'bus': 'B70', 'crew': 38}, {'bus': 'B86', 'crew': 228}, {'bus': 'B8', 'crew': 325}, {'bus': 'B43', 'crew': 335}, {'bus': 'B46', 'crew': 299}, {'bus': 'B50', 'crew': 366}, {'bus': 'B52', 'crew': 132}, {'bus': 'B1', 'crew': 58}, {'bus': 'B4', 'crew': 49}, {'bus': 'B15', 'crew': 452}, {'bus': 'B19', 'crew': 75}, {'bus': 'B33', 'crew': 223}, {'bus': 'B71', 'crew': 27}, {'bus': 'B45', 'crew': 17}, {'bus': 'B49', 'crew': 414}, {'bus': 'B53', 'crew': 62}, {'bus': 'B72', 'crew': 176}, {'bus': 'B76', 'crew': 499}, {'bus': 'B82', 'crew': 158}, {'bus': 'B44', 'crew': 262}, {'bus': 'B56', 'crew': 122}, {'bus': 'B2', 'crew': 420}, {'bus': 'B34', 'crew': 239}, {'bus': 'B39', 'crew': 405}, {'bus': 'B54', 'crew': 316}, {'bus': 'B58', 'crew': 328}, {'bus': 'B88', 'crew': 71}, {'bus': 'B93', 'crew': 107}, {'bus': 'B95', 'crew': 256}, {'bus': 'B14', 'crew': 363}, {'bus': 'B20', 'crew': 186}, {'bus': 'B24', 'crew': 296}, {'bus': 'B59', 'crew': 67}, {'bus': 'B61', 'crew': 354}, {'bus': 'B68', 'crew': 342}, {'bus': 'B69', 'crew': 334}, {'bus': 'B75', 'crew': 284}, {'bus': 'B81', 'crew': 185}, {'bus': 'B97', 'crew': 144}, {'bus': 'B60', 'crew': 392}, {'bus': 'B84', 'crew': 172}, {'bus': 'B90', 'crew': 59}, {'bus': 'B91', 'crew': 128}, {'bus': 'B99', 'crew': 37}, {'bus': 'B7', 'crew': 23}, {'bus': 'B64', 'crew': 204}, {'bus': 'B94', 'crew': 260}, {'bus': 'B25', 'crew': 103}, {'bus': 'B26', 'crew': 224}, {'bus': 'B37', 'crew': 361}, {'bus': 'B51', 'crew': 254}, {'bus': 'B87', 'crew': 477}, {'bus': 'B6', 'crew': 318}, {'bus': 'B100', 'crew': 478}]
# Execution Time: 0.004233360290527344 seconds

# Final Analysis:
# Total number of buses: 100
# Total number of crews: 500
# No of buses that didn't get assigned to any crew members: 0
# Buses without assignments: []
# Total number of unassigned crews: 400
# Crews without assignments: [1, 97, 100, 150, 174, 210, 321, 329, 403, 141, 190, 255, 424, 29, 94, 200, 209, 212, 232, 233, 332, 397, 411, 415, 433, 21, 79, 138, 168, 207, 220, 270, 294, 298, 300, 323, 341, 368, 404, 431, 437, 16, 39, 51, 70, 72, 99, 289, 315, 347, 370, 4, 25, 127, 149, 194, 205, 278, 297, 313, 379, 386, 398, 416, 425, 447, 454, 475, 498, 11, 24, 26, 36, 47, 61, 66, 93, 98, 129, 192, 193, 213, 225, 229, 244, 257, 267, 276, 306, 338, 345, 385, 422, 453, 3, 68, 101, 105, 145, 152, 218, 243, 290, 303, 320, 339, 346, 479, 490, 9, 14, 28, 125, 133, 139, 143, 151, 177, 183, 195, 231, 248, 268, 272, 340, 367, 376, 390, 393, 395, 409, 435, 446, 472, 44, 48, 78, 85, 91, 175, 202, 215, 227, 252, 277, 293, 331, 364, 373, 402, 407, 410, 412, 492, 493, 20, 46, 74, 82, 95, 96, 110, 120, 137, 142, 201, 226, 237, 258, 261, 266, 307, 309, 365, 377, 383, 436, 450, 469, 494, 496, 8, 32, 33, 111, 154, 159, 161, 165, 178, 240, 271, 275, 288, 302, 324, 343, 374, 418, 438, 485, 12, 34, 40, 115, 135, 140, 191, 238, 242, 301, 389, 439, 483, 487, 497, 53, 81, 86, 92, 114, 166, 169, 182, 199, 206, 217, 251, 279, 295, 305, 319, 330, 337, 356, 359, 388, 419, 426, 427, 444, 457, 470, 476, 10, 13, 41, 56, 65, 124, 162, 171, 198, 214, 322, 353, 375, 434, 445, 458, 460, 463, 465, 18, 22, 55, 69, 89, 102, 104, 116, 117, 146, 148, 160, 163, 208, 236, 246, 247, 273, 344, 355, 371, 372, 391, 394, 448, 462, 464, 481, 84, 106, 112, 113, 134, 203, 211, 221, 264, 286, 287, 292, 304, 311, 348, 358, 362, 384, 399, 430, 449, 461, 473, 489, 6, 7, 42, 50, 57, 63, 87, 88, 119, 156, 170, 196, 249, 281, 283, 285, 327, 333, 349, 369, 381, 401, 406, 486, 488, 500, 2, 45, 60, 80, 179, 180, 274, 326, 336, 352, 387, 413, 421, 443, 456, 468, 495, 43, 52, 118, 123, 130, 164, 173, 234, 235, 250, 259, 265, 282, 310, 314, 378, 400, 417, 423, 432, 451, 459, 484, 19, 30, 108, 109, 126, 131, 147, 181, 188, 189, 241, 280, 312, 317, 396, 428, 429, 442, 480]
# Total number of assigned crews: 100
# Percentage of crews assigned: 20.00%