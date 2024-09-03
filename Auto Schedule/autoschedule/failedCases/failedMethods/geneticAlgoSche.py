import random
import time
import json

notAssigned = 0
notAssignedBuses = []
unassignedCrews = []

def geneticAlgorithmScheduling(crews, buses, generations=100, population_size=50, mutation_rate=0.1):
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

    def crossover(parent1, parent2):
        split = random.randint(0, len(parent1) - 1)
        child = parent1[:split] + parent2[split:]
        return child

    def create_initial_population():
        return [[{'bus': b['id'], 'crew': random.choice(crews)['id']} for b in buses] for _ in range(population_size)]

    population = create_initial_population()
    for generation in range(generations):
        population = sorted(population, key=lambda x: fitness(x), reverse=True)
        new_population = population[:population_size // 2]
        while len(new_population) < population_size:
            parent1, parent2 = random.sample(population[:10], 2)
            child = crossover(parent1, parent2)
            if random.random() < mutation_rate:
                child = mutate(child)
            new_population.append(child)
        population = new_population

    best_solution = max(population, key=lambda x: fitness(x))

    # Assignments and handling unassigned buses/crews
    assignments = []
    assigned_crews = set()
    for a in best_solution:
        crew_id = a['crew']
        bus_id = a['bus']
        bus = next(b for b in buses if b['id'] == bus_id)
        crew = next((c for c in crews if c['id'] == crew_id), None)
        if crew and crew['start'] <= bus['shift_start'] and crew['end'] >= bus['shift_end']:
            assignments.append({'bus': bus_id, 'crew': crew_id})
            assigned_crews.add(crew_id)
        else:
            assignments.append({'bus': bus_id, 'crew': None})
            notAssignedBuses.append(bus_id)
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

# Run the scheduling algorithm
assignments = geneticAlgorithmScheduling(crews, buses)

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


# Assignments: [{'bus': 'B1', 'crew': 132}, {'bus': 'B2', 'crew': 71}, {'bus': 'B3', 'crew': None}, {'bus': 'B4', 'crew': 309}, {'bus': 'B5', 'crew': None}, {'bus': 'B6', 'crew': None}, {'bus': 'B7', 'crew': None}, {'bus': 'B8', 'crew': 177}, {'bus': 'B9', 'crew': None}, {'bus': 'B10', 'crew': 227}, {'bus': 'B11', 'crew': None}, {'bus': 'B12', 'crew': 414}, {'bus': 'B13', 'crew': None}, {'bus': 'B14', 'crew': None}, {'bus': 'B15', 'crew': None}, {'bus': 'B16', 'crew': 299}, {'bus': 'B17', 'crew': None}, {'bus': 'B18', 'crew': 219}, {'bus': 'B19', 'crew': 155}, {'bus': 'B20', 'crew': 22}, {'bus': 'B21', 'crew': 262}, {'bus': 'B22', 'crew': None}, {'bus': 'B23', 'crew': None}, {'bus': 'B24', 'crew': 299}, {'bus': 'B25', 'crew': 299}, {'bus': 'B26', 'crew': 158}, {'bus': 'B27', 'crew': None}, {'bus': 'B28', 'crew': None}, {'bus': 'B29', 'crew': 342}, {'bus': 'B30', 'crew': 342}, {'bus': 'B31', 'crew': 27}, {'bus': 'B32', 'crew': None}, {'bus': 'B33', 'crew': 161}, {'bus': 'B34', 'crew': 33}, {'bus': 'B35', 'crew': None}, {'bus': 'B36', 'crew': 308}, {'bus': 'B37', 'crew': 69}, {'bus': 'B38', 'crew': None}, {'bus': 'B39', 'crew': 81}, {'bus': 'B40', 'crew': 67}, {'bus': 'B41', 'crew': None}, {'bus': 'B42', 'crew': 62}, {'bus': 'B43', 'crew': 83}, {'bus': 'B44', 'crew': None}, {'bus': 'B45', 'crew': 226}, {'bus': 'B46', 'crew': None}, {'bus': 'B47', 'crew': None}, {'bus': 'B48', 'crew': 186}, {'bus': 'B49', 'crew': None}, {'bus': 'B50', 'crew': None}, {'bus': 'B51', 'crew': None}, {'bus': 'B52', 'crew': 111}, {'bus': 'B53', 'crew': None}, {'bus': 'B54', 'crew': None}, {'bus': 'B55', 'crew': None}, {'bus': 'B56', 'crew': 476}, {'bus': 'B57', 'crew': 54}, {'bus': 'B58', 'crew': 247}, {'bus': 'B59', 'crew': 445}, {'bus': 'B60', 'crew': 489}, {'bus': 'B61', 'crew': 172}, {'bus': 'B62', 'crew': None}, {'bus': 'B63', 'crew': 176}, {'bus': 'B64', 'crew': None}, {'bus': 'B65', 'crew': None}, {'bus': 'B66', 'crew': None}, {'bus': 'B67', 'crew': None}, {'bus': 'B68', 'crew': None}, {'bus': 'B69', 'crew': 246}, {'bus': 'B70', 'crew': 360}, {'bus': 'B71', 'crew': None}, {'bus': 'B72', 'crew': 9}, {'bus': 'B73', 'crew': None}, {'bus': 'B74', 'crew': 435}, {'bus': 'B75', 'crew': None}, {'bus': 'B76', 'crew': 224}, {'bus': 'B77', 'crew': None}, {'bus': 'B78', 'crew': None}, {'bus': 'B79', 'crew': 379}, {'bus': 'B80', 'crew': None}, {'bus': 'B81', 'crew': None}, {'bus': 'B82', 'crew': 158}, {'bus': 'B83', 'crew': None}, {'bus': 'B84', 'crew': 240}, {'bus': 'B85', 'crew': 299}, {'bus': 'B86', 'crew': 218}, {'bus': 'B87', 'crew': 426}, {'bus': 'B88', 'crew': 441}, {'bus': 'B89', 'crew': None}, {'bus': 'B90', 'crew': 89}, {'bus': 'B91', 'crew': 399}, {'bus': 'B92', 'crew': None}, {'bus': 'B93', 'crew': 340}, {'bus': 'B94', 'crew': 452}, {'bus': 'B95', 'crew': 334}, {'bus': 'B96', 'crew': None}, {'bus': 'B97', 'crew': 445}, {'bus': 'B98', 'crew': 256}, {'bus': 'B99', 'crew': None}, {'bus': 'B100', 'crew': 240}]
# Execution Time: 6.646368741989136 seconds

# Final Analysis:
# Total number of buses: 100
# Total number of crews: 500
# No of buses that didn't get assigned to any crew members: 45
# Buses without assignments: ['B3', 'B5', 'B6', 'B7', 'B9', 'B11', 'B13', 'B14', 'B15', 'B17', 'B22', 'B23', 'B27', 'B28', 'B32', 'B35', 'B38', 'B41', 'B44', 'B46', 'B47', 'B49', 'B50', 'B51', 'B53', 'B54', 'B55', 'B62', 'B64', 'B65', 'B66', 'B67', 'B68', 'B71', 'B73', 'B75', 'B77', 'B78', 'B80', 'B81', 'B83', 'B89', 'B92', 'B96', 'B99']
# Total number of unassigned crews: 452
# Crews without assignments: [1, 2, 3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 55, 56, 57, 58, 59, 60, 61, 63, 64, 65, 66, 68, 70, 72, 73, 74, 75, 76, 77, 78, 79, 80, 82, 84, 85, 86, 87, 88, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 112, 113, 114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 133, 134, 135, 136, 137, 138, 139, 140, 141, 142, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 154, 156, 157, 159, 160, 162, 163, 164, 165, 166, 167, 168, 169, 170, 171, 173, 174, 175, 178, 179, 180, 181, 182, 183, 184, 185, 187, 188, 189, 190, 191, 192, 193, 194, 195, 196, 197, 198, 199, 200, 201, 202, 203, 204, 205, 206, 207, 208, 209, 210, 211, 212, 213, 214, 215, 216, 217, 220, 221, 222, 223, 225, 228, 229, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 241, 242, 243, 244, 245, 248, 249, 250, 251, 252, 253, 254, 255, 257, 258, 259, 260, 261, 263, 264, 265, 266, 267, 268, 269, 270, 271, 272, 273, 274, 275, 276, 277, 278, 279, 280, 281, 282, 283, 284, 285, 286, 287, 288, 289, 290, 291, 292, 293, 294, 295, 296, 297, 298, 300, 301, 302, 303, 304, 305, 306, 307, 310, 311, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 335, 336, 337, 338, 339, 341, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 353, 354, 355, 356, 357, 358, 359, 361, 362, 363, 364, 365, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377, 378, 380, 381, 382, 383, 384, 385, 386, 387, 388, 389, 390, 391, 392, 393, 394, 395, 396, 397, 398, 400, 401, 402, 403, 404, 405, 406, 407, 408, 409, 410, 411, 412, 413, 415, 416, 417, 418, 419, 420, 421, 422, 423, 424, 425, 427, 428, 429, 430, 431, 432, 433, 434, 436, 437, 438, 439, 440, 442, 443, 444, 446, 447, 448, 449, 450, 451, 453, 454, 455, 456, 457, 458, 459, 460, 461, 462, 463, 464, 465, 466, 467, 468, 469, 470, 471, 472, 473, 474, 475, 477, 478, 479, 480, 481, 482, 483, 484, 485, 486, 487, 488, 490, 491, 492, 493, 494, 495, 496, 497, 498, 499, 500]
# Total number of assigned crews: 48
# Percentage of crews assigned: 9.60%