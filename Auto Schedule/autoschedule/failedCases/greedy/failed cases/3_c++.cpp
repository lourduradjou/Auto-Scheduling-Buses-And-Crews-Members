#include <iostream>
#include <vector>
#include <map>

// Function to assign bus shifts to crews
void assignBusShiftsToCrews(int total_shifts, int total_crews) {
    std::map<int, int> assignments; // Crew -> Shift assignment

    // Distribute shifts evenly among crews
    for (int i = 1; i <= total_shifts; ++i) {
        int crew_id = (i % total_crews == 0) ? total_crews : i % total_crews;
        assignments[crew_id]++;
    }

    // Output results
    std::cout << "Total number of bus shifts: " << total_shifts << std::endl;
    std::cout << "Total number of crews: " << total_crews << std::endl;
    
    int assigned_crews = 0;
    for (int i = 1; i <= total_crews; ++i) {
        if (assignments[i] > 0) {
            assigned_crews++;
        } else {
            std::cout << "Crew without assignment: " << i << std::endl;
        }
    }
    
    std::cout << "Total number of assigned crews: " << assigned_crews << std::endl;
    std::cout << "Percentage of crews assigned: " 
              << (assigned_crews * 100.0 / total_crews) << "%" << std::endl;
}

int main() {
    int total_shifts = 2000;
    int total_crews = 500;

    assignBusShiftsToCrews(total_shifts, total_crews);

    return 0;
}
