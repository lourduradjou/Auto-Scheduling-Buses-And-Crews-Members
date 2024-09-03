#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_CREWS 1000
#define MAX_BUSES 1000
#define MAX_SHIFTS 4

typedef struct {
    int id;
    int start;
    int end;
    int maxWork;
    int morning;
    int afternoon;
    int evening;
    int night;
    int assigned;
} Crew;

typedef struct {
    int id;
    char shift_name[10];
    int shift_start;
    int shift_end;
    int crew_id;
} BusShift;

int notAssigned = 0;
int notAssignedBuses[MAX_BUSES * MAX_SHIFTS];
int unassignedCrews[MAX_CREWS];

void linkedScheduling(Crew *crews, int num_crews, BusShift *bus_shifts, int num_bus_shifts, int bus_shifts_len) {
    int availableCrews[MAX_CREWS];
    int assignments[MAX_BUSES * MAX_SHIFTS][2]; // [bus_id, crew_id]
    int assignedCrews = 0;
    int availableCrewCount = 0;

    for (int i = 0; i < num_bus_shifts; i++) {
        int shift_duration = bus_shifts[i].shift_end - bus_shifts[i].shift_start;
        availableCrewCount = 0;

        // Update available crews based on shift start time and maxWork
        for (int j = 0; j < num_crews; j++) {
            if (crews[j].end >= bus_shifts[i].shift_start && crews[j].maxWork >= shift_duration) {
                availableCrews[availableCrewCount++] = j;
            }
        }

        // Sort available crews by end time
        for (int j = 0; j < availableCrewCount - 1; j++) {
            for (int k = j + 1; k < availableCrewCount; k++) {
                if (crews[availableCrews[j]].end > crews[availableCrews[k]].end) {
                    int temp = availableCrews[j];
                    availableCrews[j] = availableCrews[k];
                    availableCrews[k] = temp;
                }
            }
        }

        // Assign the first available crew with matching shift preference
        int assigned = 0;
        for (int j = 0; j < availableCrewCount; j++) {
            int crew_index = availableCrews[j];
            if (crews[crew_index].start <= bus_shifts[i].shift_start && 
                crews[crew_index].end >= bus_shifts[i].shift_end &&
                crews[crew_index].maxWork >= shift_duration &&
                ((strcmp(bus_shifts[i].shift_name, "morning") == 0 && crews[crew_index].morning == 1) ||
                 (strcmp(bus_shifts[i].shift_name, "afternoon") == 0 && crews[crew_index].afternoon == 1) ||
                 (strcmp(bus_shifts[i].shift_name, "evening") == 0 && crews[crew_index].evening == 1) ||
                 (strcmp(bus_shifts[i].shift_name, "night") == 0 && crews[crew_index].night == 1))) {
                
                assignments[i][0] = bus_shifts[i].id;
                assignments[i][1] = crews[crew_index].id;
                crews[crew_index].assigned = 1;
                crews[crew_index].start = bus_shifts[i].shift_end;
                crews[crew_index].maxWork -= shift_duration;
                assigned = 1;
                break;
            }
        }

        if (!assigned) {
            assignments[i][0] = bus_shifts[i].id;
            assignments[i][1] = -1; // No crew assigned
            notAssigned++;
            notAssignedBuses[notAssigned - 1] = bus_shifts[i].id;
        }
    }

    // Collect unassigned crews
    int unassignedCount = 0;
    for (int i = 0; i < num_crews; i++) {
        if (!crews[i].assigned) {
            unassignedCrews[unassignedCount++] = crews[i].id;
        }
    }

    // Final Analysis
    int assigned_crews = num_crews - unassignedCount;
    printf("Total number of bus shifts: %d\n", bus_shifts_len);
    printf("Total number of crews: %d\n", num_crews);
    printf("No of bus shifts that didn't get assigned to any crew members: %d\n", notAssigned);
    printf("Total number of unassigned crews: %d\n", unassignedCount);
    printf("Total number of assigned crews: %d\n", assigned_crews);
    printf("Percentage of crews assigned: %.2f%%\n", assigned_crews * 100.0 / num_crews);
}

// Load the test case from the file
void load_test_case(const char *filename, Crew *crews, int *num_crews, BusShift *bus_shifts, int *num_bus_shifts) {
    FILE *file = fopen(filename, "r");
    if (!file) {
        printf("Could not open file %s\n", filename);
        exit(1);
    }

    // For simplicity, let's assume a fixed number of crews and shifts in the input
    fscanf(file, "%d", num_crews);
    for (int i = 0; i < *num_crews; i++) {
        fscanf(file, "%d %d %d %d %d %d %d %d",
               &crews[i].id, &crews[i].start, &crews[i].end, &crews[i].maxWork,
               &crews[i].morning, &crews[i].afternoon, &crews[i].evening, &crews[i].night);
    }

    fscanf(file, "%d", num_bus_shifts);
    for (int i = 0; i < *num_bus_shifts; i++) {
        fscanf(file, "%d %s %d %d",
               &bus_shifts[i].id, bus_shifts[i].shift_name, &bus_shifts[i].shift_start, &bus_shifts[i].shift_end);
    }

    fclose(file);
}

int main() {
    Crew crews[MAX_CREWS];
    BusShift bus_shifts[MAX_BUSES * MAX_SHIFTS];
    int num_crews, num_bus_shifts;

    // Load the test case
    load_test_case("d:/Bus_Scheduling_SIH_2024/autoschedule/test_case3.json", crews, &num_crews, bus_shifts, &num_bus_shifts);

    // Measure the running time
    clock_t start_time = clock();

    // Run the scheduling algorithm
    linkedScheduling(crews, num_crews, bus_shifts, num_bus_shifts, num_bus_shifts);

    // Measure the end time and calculate the duration
    clock_t end_time = clock();
    double execution_time = (double)(end_time - start_time) / CLOCKS_PER_SEC;
    printf("Execution Time: %.2f seconds\n", execution_time);

    return 0;
}
