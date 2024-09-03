import json
import time

class MinHeap:
    def __init__(self):
        self.heap = []

    def push(self, item):
        self.heap.append(item)
        self._heapify_up(len(self.heap) - 1)

    def pop(self):
        if len(self.heap) > 1:
            self._swap(0, len(self.heap) - 1)
            item = self.heap.pop()
            self._heapify_down(0)
        elif self.heap:
            item = self.heap.pop()
        else:
            item = None
        return item

    def _heapify_up(self, index):
        parent_index = (index - 1) // 2
        if index > 0 and self.heap[index][0] < self.heap[parent_index][0]:
            self._swap(index, parent_index)
            self._heapify_up(parent_index)

    def _heapify_down(self, index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2
        if left < len(self.heap) and self.heap[left][0] < self.heap[smallest][0]:
            smallest = left
        if right < len(self.heap) and self.heap[right][0] < self.heap[smallest][0]:
            smallest = right
        if smallest != index:
            self._swap(index, smallest)
            self._heapify_down(smallest)

    def _swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def is_empty(self):
        return len(self.heap) == 0


def linkedScheduling(crews, buses):
    global notAssigned, notAssignedBuses, unassignedCrews ,countShifts
    notAssigned = 0
    notAssignedBuses = []
    unassignedCrews = []

    bus_shifts = []

    for bus in buses:
        for shift in ["morning", "afternoon", "evening", "night"]:
            shift_details = bus.get(shift)
            # Check if shift_details is not None and has valid shift_start and shift_end
            if shift_details and shift_details["shift_start"] is not None and shift_details["shift_end"] is not None:
                bus_shifts.append({
                    "bus_id": bus["id"],
                    "shift_name": shift,
                    "shift_start": shift_details["shift_start"],
                    "shift_end": shift_details["shift_end"],
                    "crew": shift_details["crew"]
                })

    countShifts = len(bus_shifts)
    bus_shifts.sort(key=lambda x: x['shift_start'])

    assignments = []
    crew_heap = MinHeap()
    crew_index = 0

    for bus_shift in bus_shifts:
        shift_duration = bus_shift['shift_end'] - bus_shift['shift_start']

        # Remove crews that have completed their shifts or exceeded maxWork
        updated_heap = []
        while not crew_heap.is_empty():
            end_time, crew = crew_heap.pop()
            if crew['end'] >= bus_shift['shift_start'] and crew['maxWork'] >= shift_duration:
                updated_heap.append((end_time, crew))
        for item in updated_heap:
            crew_heap.push(item)

        while crew_index < len(crews) and crews[crew_index]['start'] <= bus_shift['shift_start']:
            if crews[crew_index]['maxWork'] >= shift_duration:
                crew_heap.push((crews[crew_index]['end'], crews[crew_index]))
            crew_index += 1

        assigned = False
        while not crew_heap.is_empty():
            _, crew = crew_heap.pop()
            if crew['start'] <= bus_shift['shift_start'] and crew['end'] >= bus_shift['shift_end'] and crew[bus_shift['shift_name']] == 1 and crew['maxWork'] >= shift_duration:
                assignments.append({'bus': bus_shift['bus_id'], 'crew': crew['id'], 'shift': bus_shift['shift_name']})
                crew['assigned'] = True
                crew['start'] = bus_shift['shift_end']
                crew['maxWork'] -= shift_duration
                assigned = True
                break

        if not assigned:
            assignments.append({'bus': bus_shift['bus_id'], 'crew': None, 'shift': bus_shift['shift_name']})
            notAssigned += 1
            notAssignedBuses.append(bus_shift['bus_id'] + " (" + bus_shift['shift_name'] + ")")

    for crew in crews:
        if not crew.get('assigned', False):
            unassignedCrews.append(crew['id'])

    return assignments, notAssigned, notAssignedBuses, unassignedCrews

def load_test_case(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
    return data['crews'], data['buses']

crews, buses = load_test_case('d:/Auto Schedule/autoschedule/greedy/test_case4.json')

start_time = time.time()

assignments, notAssigned, notAssignedBuses, unassignedCrews = linkedScheduling(crews, buses)

# print(assignments)

end_time = time.time()

print("Execution Time:", end_time - start_time, "seconds")

print("\nFinal Analysis:")
bus_shifts_len = countShifts
print(f"Total number of bus shifts: {bus_shifts_len}")
print(f"Total number of crews: {len(crews)}")
print(f"No of bus shifts that didn't get assigned to any crew members: {notAssigned}")
print(f"Buses without assignments: {notAssignedBuses}")
print(f"Total number of unassigned crews: {len(unassignedCrews)}")
# print(f"Crews without assignments: {unassignedCrews}")

assigned_crews = len(crews) - len(unassignedCrews)
# print(f"Total number of assigned crews: {assigned_crews}")
print(f"Percentage of crews assigned: {assigned_crews / len(crews) * 100:.2f}%")
