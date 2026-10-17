"""
Transportation Problem Solver.
Includes:
- North-West Corner Method (NWCM)
- Least Cost Method (LCM)
- Vogel's Approximation Method (VAM)
- MODI / u-v Method (Stepping Stone Optimality Algorithm)
- Comparative Analysis of all methods
"""

from utils import (
    print_banner,
    print_section,
    print_transportation_table,
    print_matrix,
    format_cell
)

class TransportationSolver:
    def __init__(self, cost_matrix, supply, demand):
        self.m = len(supply)
        self.n = len(demand)
        self.cost = [row[:] for row in cost_matrix]
        self.supply = list(supply)
        self.demand = list(demand)

    def _calc_total_cost(self, alloc):
        return sum(self.cost[i][j] * alloc[i][j] for i in range(self.m) for j in range(self.n))

    # =========================================================================
    # 1. NORTH-WEST CORNER METHOD (NWCM)
    # =========================================================================
    def solve_nwcm(self, verbose=True):
        if verbose:
            print_banner("NORTH-WEST CORNER METHOD (NWCM)")
            print_transportation_table(self.cost, None, self.supply, self.demand, "Initial Transportation Problem")

        alloc = [[0] * self.n for _ in range(self.m)]
        basic_cells = set()
        s = self.supply[:]
        d = self.demand[:]
        i, j = 0, 0
        step = 1

        while i < self.m and j < self.n:
            qty = min(s[i], d[j])
            alloc[i][j] = qty
            basic_cells.add((i, j))
            s[i] -= qty
            d[j] -= qty

            if verbose:
                print_section(f"NWCM Step {step}: Considering Cell (S{i+1}, D{j+1})")
                print(f"  Unit Cost = {self.cost[i][j]}")
                print(f"  Available Supply at S{i+1} = {s[i] + qty}, Demand at D{j+1} = {d[j] + qty}")
                print(f"  Allocated Quantity = min({s[i] + qty}, {d[j] + qty}) = {qty}")
                print(f"  Remaining Supply at S{i+1} = {s[i]}")
                print(f"  Remaining Demand at D{j+1} = {d[j]}")

            if s[i] == 0 and d[j] == 0:
                if verbose:
                    print(f"  Both Supply at S{i+1} and Demand at D{j+1} are fully satisfied!")
                if i + 1 < self.m:
                    i += 1
                elif j + 1 < self.n:
                    j += 1
                else:
                    break
            elif s[i] == 0:
                if verbose:
                    print(f"  Supply at S{i+1} exhausted -> Move DOWN to S{i+2}")
                i += 1
            else:
                if verbose:
                    print(f"  Demand at D{j+1} satisfied -> Move RIGHT to D{j+2}")
                j += 1

            if verbose:
                print_transportation_table(self.cost, alloc, s, d, f"Allocation Matrix after Step {step}")
            step += 1

        total_cost = self._calc_total_cost(alloc)
        if verbose:
            self._print_result_summary("NWCM Initial Solution", alloc, total_cost)
        return alloc, basic_cells, total_cost

    # =========================================================================
    # 2. LEAST COST METHOD (LCM) / MATRIX MINIMUM METHOD
    # =========================================================================
    def solve_lcm(self, verbose=True):
        if verbose:
            print_banner("LEAST COST METHOD (LCM)")
            print_transportation_table(self.cost, None, self.supply, self.demand, "Initial Transportation Problem")

        alloc = [[0] * self.n for _ in range(self.m)]
        basic_cells = set()
        s = self.supply[:]
        d = self.demand[:]
        row_active = [True] * self.m
        col_active = [True] * self.n
        step = 1

        while any(row_active) and any(col_active):
            # Find unallocated cell with minimum cost among active rows & cols
            min_c = float('inf')
            candidates = []
            for i in range(self.m):
                if not row_active[i]:
                    continue
                for j in range(self.n):
                    if not col_active[j]:
                        continue
                    if self.cost[i][j] < min_c:
                        min_c = self.cost[i][j]
                        candidates = [(i, j)]
                    elif self.cost[i][j] == min_c:
                        candidates.append((i, j))

            if not candidates:
                break

            # Tie breaker: pick cell that can allocate maximum quantity
            best_cell = max(candidates, key=lambda cell: min(s[cell[0]], d[cell[1]]))
            i, j = best_cell
            qty = min(s[i], d[j])
            alloc[i][j] = qty
            basic_cells.add((i, j))
            s[i] -= qty
            d[j] -= qty

            if verbose:
                print_section(f"LCM Step {step}: Selected Minimum Cost Cell (S{i+1}, D{j+1})")
                print(f"  Minimum Unit Cost found = {min_c}")
                print(f"  Supply at S{i+1} = {s[i] + qty}, Demand at D{j+1} = {d[j] + qty}")
                print(f"  Allocated Quantity = min({s[i] + qty}, {d[j] + qty}) = {qty}")
                print(f"  Remaining Supply at S{i+1} = {s[i]}")
                print(f"  Remaining Demand at D{j+1} = {d[j]}")

            if s[i] == 0 and d[j] == 0:
                if sum(row_active) > 1:
                    row_active[i] = False
                    if verbose: print(f"  Row S{i+1} is crossed out.")
                else:
                    col_active[j] = False
                    if verbose: print(f"  Column D{j+1} is crossed out.")
            elif s[i] == 0:
                row_active[i] = False
                if verbose: print(f"  Row S{i+1} is crossed out.")
            else:
                col_active[j] = False
                if verbose: print(f"  Column D{j+1} is crossed out.")

            if verbose:
                print_transportation_table(self.cost, alloc, s, d, f"Allocation Matrix after Step {step}")
            step += 1

        total_cost = self._calc_total_cost(alloc)
        if verbose:
            self._print_result_summary("LCM Initial Solution", alloc, total_cost)
        return alloc, basic_cells, total_cost

    # =========================================================================
    # 3. VOGEL'S APPROXIMATION METHOD (VAM)
    # =========================================================================
    def solve_vam(self, verbose=True):
        if verbose:
            print_banner("VOGEL'S APPROXIMATION METHOD (VAM)")
            print_transportation_table(self.cost, None, self.supply, self.demand, "Initial Transportation Problem")

        alloc = [[0] * self.n for _ in range(self.m)]
        basic_cells = set()
        s = self.supply[:]
        d = self.demand[:]
        row_active = [True] * self.m
        col_active = [True] * self.n
        step = 1

        while any(row_active) and any(col_active):
            # 1. Compute Row Penalties
            row_penalties = {}
            for i in range(self.m):
                if not row_active[i]:
                    continue
                active_costs = sorted([self.cost[i][j] for j in range(self.n) if col_active[j]])
                if len(active_costs) >= 2:
                    row_penalties[i] = active_costs[1] - active_costs[0]
                elif len(active_costs) == 1:
                    row_penalties[i] = active_costs[0]
                else:
                    row_penalties[i] = 0

            # 2. Compute Column Penalties
            col_penalties = {}
            for j in range(self.n):
                if not col_active[j]:
                    continue
                active_costs = sorted([self.cost[i][j] for i in range(self.m) if row_active[i]])
                if len(active_costs) >= 2:
                    col_penalties[j] = active_costs[1] - active_costs[0]
                elif len(active_costs) == 1:
                    col_penalties[j] = active_costs[0]
                else:
                    col_penalties[j] = 0

            # Find Maximum Penalty
            max_row_p = max(row_penalties.values()) if row_penalties else -1
            max_col_p = max(col_penalties.values()) if col_penalties else -1
            overall_max_p = max(max_row_p, max_col_p)

            if verbose:
                print_section(f"VAM Step {step}: Penalty Calculation")
                print("  Row Penalties   : " + ", ".join(f"S{i+1}: {p}" for i, p in row_penalties.items()))
                print("  Column Penalties: " + ", ".join(f"D{j+1}: {p}" for j, p in col_penalties.items()))
                print(f"  Maximum Penalty = {overall_max_p}")

            # Pick the row or column with maximum penalty
            selected_cells = []
            if max_row_p >= max_col_p:
                best_rows = [i for i, p in row_penalties.items() if p == max_row_p]
                for r in best_rows:
                    min_c = min(self.cost[r][c] for c in range(self.n) if col_active[c])
                    for c in range(self.n):
                        if col_active[c] and self.cost[r][c] == min_c:
                            selected_cells.append((r, c))
            else:
                best_cols = [j for j, p in col_penalties.items() if p == max_col_p]
                for c in best_cols:
                    min_c = min(self.cost[r][c] for r in range(self.m) if row_active[r])
                    for r in range(self.m):
                        if row_active[r] and self.cost[r][c] == min_c:
                            selected_cells.append((r, c))

            # Tie breaker: maximum allocable quantity
            sel_i, sel_j = max(selected_cells, key=lambda cell: min(s[cell[0]], d[cell[1]]))
            qty = min(s[sel_i], d[sel_j])
            alloc[sel_i][sel_j] = qty
            basic_cells.add((sel_i, sel_j))
            s[sel_i] -= qty
            d[sel_j] -= qty

            if verbose:
                print(f"  -> Selected Cell (S{sel_i+1}, D{sel_j+1}) with minimum cost {self.cost[sel_i][sel_j]}")
                print(f"  Allocated Quantity = min({s[sel_i] + qty}, {d[sel_j] + qty}) = {qty}")
                print(f"  Remaining Supply at S{sel_i+1} = {s[sel_i]}")
                print(f"  Remaining Demand at D{sel_j+1} = {d[sel_j]}")

            if s[sel_i] == 0 and d[sel_j] == 0:
                if sum(row_active) > 1:
                    row_active[sel_i] = False
                    if verbose: print(f"  Row S{sel_i+1} satisfied and crossed out.")
                else:
                    col_active[sel_j] = False
                    if verbose: print(f"  Column D{sel_j+1} satisfied and crossed out.")
            elif s[sel_i] == 0:
                row_active[sel_i] = False
                if verbose: print(f"  Row S{sel_i+1} satisfied and crossed out.")
            else:
                col_active[sel_j] = False
                if verbose: print(f"  Column D{sel_j+1} satisfied and crossed out.")

            if verbose:
                print_transportation_table(self.cost, alloc, s, d, f"Allocation Matrix after Step {step}")
            step += 1

        total_cost = self._calc_total_cost(alloc)
        if verbose:
            self._print_result_summary("VAM Initial Solution", alloc, total_cost)
        return alloc, basic_cells, total_cost

    # =========================================================================
    # 4. MODI (u-v) METHOD FOR OPTIMAL SOLUTION
    # =========================================================================
    def solve_modi(self, initial_alloc=None, initial_basic=None):
        print_banner("MODI METHOD (u-v METHOD) - OPTIMALITY TEST & REFINEMENT")

        # 1. Determine Initial Solution if not provided (default to best IBFS)
        if initial_alloc is None or initial_basic is None:
            print("Finding Initial Basic Feasible Solution (IBFS) using Vogel's Approximation Method (VAM)...")
            initial_alloc, initial_basic, _ = self.solve_vam(verbose=False)

        alloc = [row[:] for row in initial_alloc]
        basic_cells = set(initial_basic)

        # Check for degeneracy: number of basic cells must be m + n - 1
        required_basic = self.m + self.n - 1
        print(f"Number of basic allocated cells: {len(basic_cells)} (Required: m + n - 1 = {required_basic})")
        if len(basic_cells) < required_basic:
            print("[WARNING] Degeneracy detected! Allocating zero (eps = 0) to independent unallocated cell(s)...")
            # Greedily add cells that do not form a cycle
            for i in range(self.m):
                for j in range(self.n):
                    if (i, j) not in basic_cells:
                        test_loop = self._find_loop(basic_cells, (i, j))
                        if test_loop is None:
                            basic_cells.add((i, j))
                            print(f"  Added independent basic cell (S{i+1}, D{j+1}) with eps = 0")
                            if len(basic_cells) == required_basic:
                                break
                if len(basic_cells) == required_basic:
                    break

        iteration = 1
        while True:
            print_section(f"MODI Iteration {iteration}")
            curr_cost = self._calc_total_cost(alloc)
            print(f"Current Solution Total Cost = {curr_cost}")
            print_transportation_table(self.cost, alloc, None, None, f"Current Allocation Table (Iteration {iteration})")

            # 1. Solve for u_i and v_j
            # u_i + v_j = c_ij for all (i, j) in basic_cells
            u = [None] * self.m
            v = [None] * self.n
            u[0] = 0  # Set arbitrary reference

            changed = True
            while changed:
                changed = False
                for r, c in basic_cells:
                    if u[r] is not None and v[c] is None:
                        v[c] = self.cost[r][c] - u[r]
                        changed = True
                    elif u[r] is None and v[c] is not None:
                        u[r] = self.cost[r][c] - v[c]
                        changed = True

            # If any u or v remains None due to disconnectivity, fill reference
            for i in range(self.m):
                if u[i] is None: u[i] = 0
            for j in range(self.n):
                if v[j] is None: v[j] = 0

            print("\nDual Variables (u_i, v_j) satisfying u_i + v_j = c_ij for basic cells:")
            for i in range(self.m):
                print(f"  u{i+1} = {u[i]}")
            for j in range(self.n):
                print(f"  v{j+1} = {v[j]}")

            # 2. Compute Opportunity Cost (Net Evaluation) Delta_ij = c_ij - (u_i + v_j) for non-basic cells
            deltas = {}
            min_delta = 0
            entering_cell = None

            print("\nNet Evaluation / Opportunity Cost for Non-Basic Cells: Delta_ij = c_ij - (u_i + v_j):")
            eval_matrix = [["-" for _ in range(self.n)] for _ in range(self.m)]

            for i in range(self.m):
                for j in range(self.n):
                    if (i, j) in basic_cells:
                        eval_matrix[i][j] = f"[{alloc[i][j]}]"
                    else:
                        d_ij = self.cost[i][j] - (u[i] + v[j])
                        deltas[(i, j)] = d_ij
                        eval_matrix[i][j] = str(d_ij)
                        print(f"  Cell (S{i+1}, D{j+1}): Delta_{i+1}{j+1} = {self.cost[i][j]} - ({u[i]} + {v[j]}) = {d_ij}")
                        if d_ij < min_delta:
                            min_delta = d_ij
                            entering_cell = (i, j)

            print_matrix(
                eval_matrix,
                [f"S{i+1} (u={u[i]})" for i in range(self.m)],
                [f"D{j+1} (v={v[j]})" for j in range(self.n)],
                "Opportunity Cost Matrix (Non-Basic Delta_ij and Basic [allocations])"
            )

            # Optimality condition
            if min_delta >= 0:
                print("\n=======================================================")
                print("[OPTIMAL] OPTIMALITY REACHED! All Delta_ij >= 0.")
                print("No further cost reduction is possible.")
                print("=======================================================")
                final_cost = self._calc_total_cost(alloc)
                self._print_result_summary("Final MODI Optimal Solution", alloc, final_cost)
                return alloc, final_cost

            # Non-optimal: find closed loop for entering cell
            print(f"\nCondition not satisfied: Most negative Delta_ij = {min_delta} at cell (S{entering_cell[0]+1}, D{entering_cell[1]+1}).")
            print(f"Entering variable into basis: (S{entering_cell[0]+1}, D{entering_cell[1]+1})")

            loop = self._find_loop(basic_cells, entering_cell)
            if loop is None:
                print("Error: Could not trace a closed stepping-stone loop. Stopping.")
                return alloc, curr_cost

            loop_nodes = loop[:-1]
            print("\nStepping-Stone Closed Loop Path:")
            loop_str = " -> ".join(f"(S{r+1}, D{c+1}) [{'-theta' if idx % 2 else '+theta'}]" for idx, (r, c) in enumerate(loop_nodes))
            print(f"  {loop_str} -> (S{loop_nodes[0][0]+1}, D{loop_nodes[0][1]+1})")

            # Determine theta: minimum allocation among negative cells (odd indices in loop)
            negative_cells = [loop_nodes[idx] for idx in range(1, len(loop_nodes), 2)]
            positive_cells = [loop_nodes[idx] for idx in range(0, len(loop_nodes), 2)]

            theta = min(alloc[r][c] for r, c in negative_cells)
            print(f"\nValue of theta (minimum allocation in -theta cells) = {theta}")

            # Identify leaving cell
            leaving_cell = None
            for r, c in negative_cells:
                if alloc[r][c] == theta:
                    leaving_cell = (r, c)
                    break
            print(f"Leaving variable from basis: (S{leaving_cell[0]+1}, D{leaving_cell[1]+1})")

            # Reallocate along the loop
            for r, c in positive_cells:
                alloc[r][c] += theta
            for r, c in negative_cells:
                alloc[r][c] -= theta

            basic_cells.add(entering_cell)
            basic_cells.remove(leaving_cell)

            iteration += 1

    def _find_loop(self, basic_cells, start_cell):
        """
        Finds the unique closed cycle alternating horizontal and vertical moves
        containing start_cell and a subset of basic_cells.
        """
        candidates = set(basic_cells) | {start_cell}

        # Iteratively prune cells with degree < 2 in row or column
        while True:
            row_counts = {}
            col_counts = {}
            for r, c in candidates:
                row_counts[r] = row_counts.get(r, 0) + 1
                col_counts[c] = col_counts.get(c, 0) + 1

            to_remove = set()
            for r, c in candidates:
                if (r, c) != start_cell:
                    if row_counts[r] < 2 or col_counts[c] < 2:
                        to_remove.add((r, c))
                else:
                    if row_counts[r] < 2 or col_counts[c] < 2:
                        return None
            if not to_remove:
                break
            candidates -= to_remove

        # DFS to order the alternating cycle
        def dfs(curr, target, move_type, path):
            if len(path) >= 4 and curr == target:
                return path
            r, c = curr
            if move_type == 'H':
                for next_c in range(self.n):
                    nxt = (r, next_c)
                    if nxt in candidates and next_c != c:
                        if nxt == target and len(path) >= 3:
                            return path + [nxt]
                        if nxt not in path:
                            res = dfs(nxt, target, 'V', path + [nxt])
                            if res: return res
            else:
                for next_r in range(self.m):
                    nxt = (next_r, c)
                    if nxt in candidates and next_r != r:
                        if nxt == target and len(path) >= 3:
                            return path + [nxt]
                        if nxt not in path:
                            res = dfs(nxt, target, 'H', path + [nxt])
                            if res: return res
            return None

        loop = dfs(start_cell, start_cell, 'H', [start_cell])
        if not loop:
            loop = dfs(start_cell, start_cell, 'V', [start_cell])
        return loop

    # =========================================================================
    # 5. COMPARE ALL 3 METHODS & RUN MODI
    # =========================================================================
    def compare_and_optimize(self):
        print_banner("COMPARISON OF ALL METHODS & GLOBAL OPTIMIZATION")

        print("Computing solutions using all 3 Initial Basic Feasible Solution (IBFS) methods...")
        a_nw, b_nw, c_nw = self.solve_nwcm(verbose=False)
        a_lc, b_lc, c_lc = self.solve_lcm(verbose=False)
        a_va, b_va, c_va = self.solve_vam(verbose=False)

        print_section("Summary Comparison of Initial Basic Feasible Solutions")
        print(f"  1. North-West Corner Method (NWCM)  : Total Cost = {c_nw}")
        print(f"  2. Least Cost Method (LCM)          : Total Cost = {c_lc}")
        print(f"  3. Vogel's Approximation Method (VAM): Total Cost = {c_va}")

        methods = [
            ("North-West Corner Method", a_nw, b_nw, c_nw),
            ("Least Cost Method", a_lc, b_lc, c_lc),
            ("Vogel's Approximation Method", a_va, b_va, c_va)
        ]
        best_name, best_alloc, best_basic, best_cost = min(methods, key=lambda x: x[3])

        print(f"\n[BEST] Best Initial Solution: {best_name} with Total Cost = {best_cost}")

        print("\nNow running MODI (u-v) Method on this best initial solution to check/reach global optimality...")
        final_alloc, final_cost = self.solve_modi(initial_alloc=best_alloc, initial_basic=best_basic)

        print_banner("FINAL VERDICT")
        print(f"  * Best Initial Feasible Cost ({best_name}): {best_cost}")
        print(f"  * Globally Optimal Transportation Cost (MODI) : {final_cost}")
        if final_cost < best_cost:
            print(f"  * Savings achieved via MODI iterations      : {best_cost - final_cost}")
        else:
            print(f"  * {best_name} was already globally optimal!")
        print("=" * 60 + "\n")
        return final_alloc, final_cost

    def _print_result_summary(self, title, alloc, total_cost):
        print_section(f"Results: {title}")
        print_transportation_table(self.cost, alloc, self.supply, self.demand, "Final Allocation Table")
        
        alloc_details = []
        for i in range(self.m):
            for j in range(self.n):
                if alloc[i][j] > 0:
                    alloc_details.append(f"({alloc[i][j]} * {self.cost[i][j]})")
        
        calc_str = " + ".join(alloc_details)
        print(f"Total Transportation Cost Calculation:")
        print(f"  = {calc_str}")
        print(f"  = {total_cost}")
