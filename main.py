"""
Operations Research / Optimization Techniques Interactive Solver
Features:
1. Transportation Problem:
   - North-West Corner Method (NWCM)
   - Least Cost Method (LCM)
   - Vogel's Approximation Method (VAM)
   - Compare all 3 + MODI (u-v) Method for Global Optimality
2. Assignment / Scheduling Problem:
   - Hungarian Method (Kuhn-Munkres) with full step-by-step reductions, line coverings, and adjustments
"""

import sys
from utils import (
    print_banner,
    print_section,
    print_transportation_table,
    print_matrix,
    get_int_input,
    get_list_input
)
from transportation import TransportationSolver
from assignment import AssignmentSolver

def run_transportation():
    print_banner("TRANSPORTATION PROBLEM")
    print("Choose input mode:")
    print("  1. Enter custom problem")
    print("  2. Load classic textbook example (3 Sources, 4 Destinations)")
    mode = get_int_input("Enter choice (1 or 2): ", 1, 2)

    if mode == 2:
        cost_matrix = [
            [19, 30, 50, 10],
            [70, 30, 40, 60],
            [40, 8, 70, 20]
        ]
        supply = [7, 9, 18]
        demand = [5, 8, 7, 14]
        print("\nLoaded Textbook Problem:")
        print_transportation_table(cost_matrix, None, supply, demand, "Initial Transportation Table")
    else:
        m = get_int_input("\nEnter number of Sources (origins/supply nodes m): ", min_val=1)
        n = get_int_input("Enter number of Destinations (demand nodes n): ", min_val=1)

        print(f"\nEnter the {m}x{n} Unit Cost Matrix row by row:")
        cost_matrix = []
        for i in range(m):
            row = get_list_input(f"  Cost row {i+1} (enter {n} values separated by space): ", n, val_type=float)
            cost_matrix.append(row)

        while True:
            print("\nEnter Supply capacities for each source:")
            supply = get_list_input(f"  Supply vector (enter {m} values): ", m, val_type=float)
            print("\nEnter Demand requirements for each destination:")
            demand = get_list_input(f"  Demand vector (enter {n} values): ", n, val_type=float)

            sum_s = sum(supply)
            sum_d = sum(demand)
            if abs(sum_s - sum_d) > 1e-6:
                print(f"\n[!] Unbalanced problem detected: Total Supply ({sum_s}) != Total Demand ({sum_d}).")
                print("Currently, balanced problems are supported. Please re-enter supply and demand.")
            else:
                print(f"\nProblem is balanced: Total Supply = Total Demand = {sum_s}")
                break

    solver = TransportationSolver(cost_matrix, supply, demand)

    print("\nSelect Method to Solve:")
    print("  1. North-West Corner Method (NWCM)")
    print("  2. Least Cost Method (LCM)")
    print("  3. Vogel's Approximation Method (VAM)")
    print("  4. Compare all 3 methods & find the most optimal solution (MODI / u-v Method)")
    print("  5. Direct MODI (u-v) Method (Optimality test)")

    method_choice = get_int_input("Enter choice (1-5): ", 1, 5)

    if method_choice == 1:
        solver.solve_nwcm(verbose=True)
    elif method_choice == 2:
        solver.solve_lcm(verbose=True)
    elif method_choice == 3:
        solver.solve_vam(verbose=True)
    elif method_choice == 4:
        solver.compare_and_optimize()
    elif method_choice == 5:
        solver.solve_modi()

def run_assignment():
    print_banner("ASSIGNMENT / SCHEDULING PROBLEM (HUNGARIAN METHOD)")
    print("Choose input mode:")
    print("  1. Enter custom problem")
    print("  2. Load classic textbook example (5 Workers x 5 Jobs)")
    mode = get_int_input("Enter choice (1 or 2): ", 1, 2)

    if mode == 2:
        cost_matrix = [
            [9, 11, 14, 11, 7],
            [6, 15, 13, 13, 10],
            [12, 13, 6, 8, 8],
            [11, 9, 10, 12, 9],
            [7, 12, 14, 10, 14]
        ]
        n = 5
        print("\nLoaded Textbook Problem (Time/Cost Matrix):")
        print_matrix(cost_matrix, title="5x5 Assignment Matrix")
    else:
        n = get_int_input("\nEnter dimension of the matrix n (n workers and n jobs): ", min_val=2)
        print(f"\nEnter the {n}x{n} Cost/Time Matrix row by row:")
        cost_matrix = []
        for i in range(n):
            row = get_list_input(f"  Row {i+1} (Worker {i+1}) values (enter {n} values): ", n, val_type=float)
            cost_matrix.append(row)

    solver = AssignmentSolver(cost_matrix)
    solver.solve()

def main():
    while True:
        print_banner("OPTIMIZATION TECHNIQUES & OPERATIONS RESEARCH SOLVER")
        print("Select the problem type to solve:")
        print("  1. Transportation Problem (NWCM, LCM, VAM, MODI / u-v Method)")
        print("  2. Assignment / Scheduling Problem (Hungarian Method)")
        print("  3. Exit")

        choice = get_int_input("\nEnter choice (1-3): ", 1, 3)

        if choice == 1:
            run_transportation()
        elif choice == 2:
            run_assignment()
        elif choice == 3:
            print("\nThank you for using the Optimization Solver. Good luck with your class!\n")
            sys.exit(0)

        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
