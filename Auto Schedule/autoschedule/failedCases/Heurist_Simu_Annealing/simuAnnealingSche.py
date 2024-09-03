import random
import math
import time
import json

notAssigned = 0
notAssignedBuses = []
unassignedCrews = []

def simulatedAnnealingScheduling(crews, buses, initial_temp=1000, cooling_rate=0.99, iterations=1000):
    def fitness(assignment):
        score = 0
        for a in assignment:
            bus = next(b for b in buses if b['id'] == a['bus'])
            crew = next((c for c in crews if c['id'] == a['crew']), None)
            if crew and crew['start'] <= bus['shift_start'] and crew['end'] >= bus['shift_end']:
                score += 1
        return score

    def mutate(assignment):
        index = random.randint(0, len(assignment) - 1)
        new_assignment = assignment[:]
        new_assignment[index] = {'bus': assignment[index]['bus'], 'crew': random.choice(crews)['id']}
        return new_assignment

    current_solution = [{'bus': b['id'], 'crew': random.choice(crews)['id']} for b in buses]
    current_fitness = fitness(current_solution)
    temperature = initial_temp

    for _ in range(iterations):
        new_solution = mutate(current_solution)
        new_fitness = fitness(new_solution)
        if new_fitness > current_fitness or random.random() < math.exp((new_fitness - current_fitness) / temperature):
            current_solution = new_solution
            current_fitness = new_fitness
        temperature *= cooling_rate

    return current_solution

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

# Test the Simulated Annealing scheduling
assignments = simulatedAnnealingScheduling(crews, buses)

# Print the results
print("Assignments:", assignments)

# Measure the end time and calculate the duration
end_time = time.time()
print("Execution Time:", end_time - start_time, "seconds")

# Analysis and Results
print("\nFinal Analysis:")
assigned_crews = set()
for a in assignments:
    if a['crew'] is not None:
        assigned_crews.add(a['crew'])
    else:
        notAssignedBuses.append(a['bus'])

# Unassigned crews calculation
unassignedCrews = [crew['id'] for crew in crews if crew['id'] not in assigned_crews]

print(f"Total number of buses: {len(buses)}")
print(f"Total number of crews: {len(crews)}")
print(f"No of buses that didn't get assigned to any crew members: {len(notAssignedBuses)}")
print(f"Buses without assignments: {notAssignedBuses}")
print(f"Total number of unassigned crews: {len(unassignedCrews)}")
print(f"Crews without assignments: {unassignedCrews}")

assigned_crews_count = len(crews) - len(unassignedCrews)
print(f"Total number of assigned crews: {assigned_crews_count}")
print(f"Percentage of crews assigned: {assigned_crews_count / len(crews) * 100:.2f}%")


# Assignments: [{'bus': 'B1', 'crew': 301}, {'bus': 'B2', 'crew': 364}, {'bus': 'B3', 'crew': 473}, {'bus': 'B4', 'crew': 498}, {'bus': 'B5', 'crew': 469}, {'bus': 'B6', 'crew': 346}, {'bus': 'B7', 'crew': 222}, {'bus': 'B8', 'crew': 494}, {'bus': 'B9', 'crew': 224}, {'bus': 'B10', 'crew': 286}, {'bus': 'B11', 'crew': 439}, {'bus': 'B12', 'crew': 151}, {'bus': 'B13', 'crew': 60}, {'bus': 'B14', 'crew': 300}, {'bus': 'B15', 'crew': 57}, {'bus': 'B16', 'crew': 189}, {'bus': 'B17', 'crew': 261}, {'bus': 'B18', 'crew': 366}, {'bus': 'B19', 'crew': 82}, {'bus': 'B20', 'crew': 75}, {'bus': 'B21', 'crew': 447}, {'bus': 'B22', 'crew': 96}, {'bus': 'B23', 'crew': 296}, {'bus': 'B24', 'crew': 460}, {'bus': 'B25', 'crew': 279}, {'bus': 'B26', 'crew': 381}, {'bus': 'B27', 'crew': 194}, {'bus': 'B28', 'crew': 18}, {'bus': 'B29', 'crew': 300}, {'bus': 'B30', 'crew': 360}, {'bus': 'B31', 'crew': 89}, {'bus': 'B32', 'crew': 248}, {'bus': 'B33', 'crew': 454}, {'bus': 'B34', 'crew': 256}, {'bus': 'B35', 'crew': 407}, {'bus': 'B36', 'crew': 49}, {'bus': 'B37', 'crew': 158}, {'bus': 'B38', 'crew': 105}, {'bus': 'B39', 'crew': 89}, {'bus': 'B40', 'crew': 356}, {'bus': 'B41', 'crew': 195}, {'bus': 'B42', 'crew': 371}, {'bus': 'B43', 'crew': 356}, {'bus': 'B44', 'crew': 166}, {'bus': 'B45', 'crew': 77}, {'bus': 'B46', 'crew': 331}, {'bus': 'B47', 'crew': 53}, {'bus': 'B48', 'crew': 220}, {'bus': 'B49', 'crew': 188}, {'bus': 'B50', 'crew': 232}, {'bus': 'B51', 'crew': 201}, {'bus': 'B52', 'crew': 288}, {'bus': 'B53', 'crew': 64}, {'bus': 'B54', 'crew': 473}, {'bus': 'B55', 'crew': 350}, {'bus': 'B56', 'crew': 407}, {'bus': 'B57', 'crew': 133}, {'bus': 'B58', 'crew': 163}, {'bus': 'B59', 'crew': 461}, {'bus': 'B60', 'crew': 477}, {'bus': 'B61', 'crew': 131}, {'bus': 'B62', 'crew': 339}, {'bus': 'B63', 'crew': 102}, {'bus': 'B64', 'crew': 414}, {'bus': 'B65', 'crew': 431}, {'bus': 'B66', 'crew': 120}, {'bus': 'B67', 'crew': 59}, {'bus': 'B68', 'crew': 22}, {'bus': 'B69', 'crew': 327}, {'bus': 'B70', 'crew': 96}, {'bus': 'B71', 'crew': 407}, {'bus': 'B72', 'crew': 140}, {'bus': 'B73', 'crew': 133}, {'bus': 'B74', 'crew': 254}, {'bus': 'B75', 'crew': 37}, {'bus': 'B76', 'crew': 467}, {'bus': 'B77', 'crew': 497}, {'bus': 'B78', 'crew': 108}, {'bus': 'B79', 'crew': 222}, {'bus': 'B80', 'crew': 51}, {'bus': 'B81', 'crew': 360}, {'bus': 'B82', 'crew': 330}, {'bus': 'B83', 'crew': 157}, {'bus': 'B84', 'crew': 170}, {'bus': 'B85', 'crew': 72}, {'bus': 'B86', 'crew': 239}, {'bus': 'B87', 'crew': 247}, {'bus': 'B88', 'crew': 480}, {'bus': 'B89', 'crew': 122}, {'bus': 'B90', 'crew': 87}, {'bus': 'B91', 'crew': 407}, {'bus': 'B92', 'crew': 121}, {'bus': 'B93', 'crew': 299}, {'bus': 'B94', 'crew': 92}, {'bus': 'B95', 'crew': 369}, {'bus': 'B96', 'crew': 437}, {'bus': 'B97', 'crew': 137}, {'bus': 'B98', 'crew': 357}, {'bus': 'B99', 'crew': 361}, {'bus': 'B100', 'crew': 436}]
# Execution Time: 1.3020472526550293 seconds

# Final Analysis:
# Total number of buses: 100
# Total number of crews: 500
# No of buses that didn't get assigned to any crew members: 0
# Buses without assignments: []
# Total number of unassigned crews: 411
# Crews without assignments: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 50, 52, 54, 55, 56, 58, 61, 62, 63, 65, 66, 67, 68, 69, 70, 71, 73, 74, 76, 78, 79, 80, 81, 83, 84, 85, 86, 88, 90, 91, 93, 94, 95, 97, 98, 99, 100, 101, 103, 104, 106, 107, 109, 110, 111, 112, 113, 114, 115, 116, 117, 118, 119, 123, 124, 125, 126, 127, 128, 129, 130, 132, 134, 135, 136, 138, 139, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 152, 153, 154, 155, 156, 159, 160, 161, 162, 164, 165, 167, 168, 169, 171, 172, 173, 174, 175, 176, 177, 178, 179, 180, 181, 182, 183, 184, 185, 186, 187, 190, 191, 192, 193, 196, 197, 198, 199, 200, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 218, 219, 221, 223, 225, 226, 227, 228, 229, 230, 231, 233, 234, 235, 236, 237, 238, 240, 241, 242, 243, 244, 245, 246, 249, 250, 251, 252, 253, 255, 257, 258, 259, 260, 262, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 280, 281, 282, 283, 284, 285, 287, 289, 290, 291, 292, 293, 294, 295, 297, 298, 302, 303, 304, 305, 306, 307, 308, 309, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 328, 329, 332, 333, 334, 335, 336, 337, 338, 340, 341, 342, 343, 344, 345, 347, 348, 349, 351, 352, 353, 354, 355, 358, 359, 362, 363, 365, 367, 368, 370, 372, 373, 374, 375, 376, 377, 378, 379, 380, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 399, 400, 401, 402, 403, 404, 405, 406, 408, 409, 410, 411, 412, 413, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 426, 427, 428, 429, 430, 432, 433, 434, 435, 438, 440, 441, 442, 443, 444, 445, 446, 448, 449, 450, 451, 452, 453, 455, 456, 457, 458, 459, 462, 463, 464, 465, 466, 468, 470, 471, 472, 474, 475, 476, 478, 479, 481, 482, 483, 484, 485, 486, 487, 488, 489, 490, 491, 492, 493, 495, 496, 499, 500]
# Total number of assigned crews: 89
# Percentage of crews assigned: 17.80%