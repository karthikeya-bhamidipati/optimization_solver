"""
Assignment / Scheduling Problem Solver using the Hungarian Method (Kuhn-Munkres Algorithm).
Provides detailed step-by-step trace of reductions, line covering, matrix adjustments, and final assignments.
"""

from utils import print_banner, print_section, print_matrix, format_cell

class AssignmentSolver:
    def __init__(self, cost_matrix, row_names=None, col_names=None):
        self.n = len(cost_matrix)
        self.orig_matrix = [row[:] for row in cost_matrix]
        self.matrix = [row[:] for row in cost_matrix]
        
        self.row_names = row_names if row_names else [f"Worker {i+1}" for i in range(self.n)]
        self.col_names = col_names if col_names else [f"Job {j+1}" for j in range(self.n)]

    def solve(self):
        print_banner("HUNGARIAN METHOD - STEP-BY-STEP SOLUTION")
        
        # Initial Matrix
        print_matrix(self.orig_matrix, self.row_names, self.col_names, "Initial Cost / Time Matrix")

        # Step 1: Row Reduction
        print_section("Step 1: Row Reduction")
        print("Find the minimum element in each row and subtract it from all elements in that row.")
        row_mins = [min(row) for row in self.matrix]
        for i in range(self.n):
            print(f"  {self.row_names[i]}: minimum = {row_mins[i]}")
            for j in range(self.n):
                self.matrix[i][j] -= row_mins[i]

        print_matrix(self.matrix, self.row_names, self.col_names, "Matrix after Row Reduction")

        # Step 2: Column Reduction
        print_section("Step 2: Column Reduction")
        print("Find the minimum element in each column and subtract it from all elements in that column.")
        col_mins = [min(self.matrix[i][j] for i in range(self.n)) for j in range(self.n)]
        for j in range(self.n):
            print(f"  {self.col_names[j]}: minimum = {col_mins[j]}")
            for i in range(self.n):
                self.matrix[i][j] -= col_mins[j]

        print_matrix(self.matrix, self.row_names, self.col_names, "Matrix after Column Reduction")

        # Step 3 & 4: Line Covering & Matrix Modification loop
        iteration = 1
        while True:
            print_section(f"Step 3: Minimum Line Covering (Iteration {iteration})")
            print("Draw the minimum number of horizontal and vertical lines to cover all zeros.")

            # Bipartite matching on zeros
            adj = [[] for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.n):
                    if self.matrix[i][j] == 0:
                        adj[i].append(j)

            match_col = [-1] * self.n
            match_row = [-1] * self.n

            def dfs(u, visited):
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        if match_col[v] < 0 or dfs(match_col[v], visited):
                            match_col[v] = u
                            match_row[u] = v
                            return True
                return False

            matching_size = 0
            for i in range(self.n):
                visited = [False] * self.n
                if dfs(i, visited):
                    matching_size += 1

            # König's Theorem to identify exact covered lines
            unmatched_rows = [i for i in range(self.n) if match_row[i] == -1]
            visited_rows = [False] * self.n
            visited_cols = [False] * self.n

            queue_rows = list(unmatched_rows)
            for r in queue_rows:
                visited_rows[r] = True

            while queue_rows:
                curr_r = queue_rows.pop(0)
                for c in adj[curr_r]:
                    if not visited_cols[c]:
                        visited_cols[c] = True
                        r_next = match_col[c]
                        if r_next != -1 and not visited_rows[r_next]:
                            visited_rows[r_next] = True
                            queue_rows.append(r_next)

            covered_rows = [i for i in range(self.n) if not visited_rows[i]]
            covered_cols = [j for j in range(self.n) if visited_cols[j]]
            num_lines = len(covered_rows) + len(covered_cols)

            print(f"Number of lines to cover all zeros = {num_lines}")
            h_lines = [self.row_names[r] for r in covered_rows]
            v_lines = [self.col_names[c] for c in covered_cols]
            print(f"  - Horizontal lines ({len(covered_rows)}): {', '.join(h_lines) if h_lines else 'None'}")
            print(f"  - Vertical lines   ({len(covered_cols)}): {', '.join(v_lines) if v_lines else 'None'}")

            # Display matrix with line coverage indication
            self._print_line_covered_matrix(covered_rows, covered_cols)

            if num_lines == self.n:
                print(f"\nCondition satisfied: Number of lines ({num_lines}) == Matrix dimension ({self.n}).")
                print("An optimal assignment is possible directly from the zero cells!")
                return self._finalize_assignment(match_row)

            # Step 4: Matrix Adjustment
            print_section(f"Step 4: Matrix Adjustment (Since lines {num_lines} < dimension {self.n})")
            uncovered_elements = []
            for i in range(self.n):
                if i not in covered_rows:
                    for j in range(self.n):
                        if j not in covered_cols:
                            uncovered_elements.append(self.matrix[i][j])

            k = min(uncovered_elements)
            print(f"1. Smallest uncovered element k = {k}")
            print(f"2. Subtract k ({k}) from all uncovered cells.")
            print(f"3. Add k ({k}) to all intersection cells (covered by both a horizontal and vertical line).")
            print("4. Cells covered by only one line remain unchanged.")

            for i in range(self.n):
                for j in range(self.n):
                    is_r_cov = (i in covered_rows)
                    is_c_cov = (j in covered_cols)
                    if not is_r_cov and not is_c_cov:
                        self.matrix[i][j] -= k
                    elif is_r_cov and is_c_cov:
                        self.matrix[i][j] += k

            print_matrix(self.matrix, self.row_names, self.col_names, f"Adjusted Matrix (After Iteration {iteration})")
            iteration += 1

    def _print_line_covered_matrix(self, covered_rows, covered_cols):
        print("\nMatrix Line-Cover Status:")
        print("  Key: [U] = Uncovered, [H] = Covered by Horizontal Line, [V] = Covered by Vertical Line, [X] = Intersection")
        col_width = 10
        max_r_label = max(len(str(lbl)) for lbl in self.row_names)

        header = " " * (max_r_label + 3) + "| " + " | ".join(format_cell(lbl, col_width) for lbl in self.col_names) + " |"
        divider = "-" * (max_r_label + 3) + "+" + "-+-".join("-" * col_width for _ in self.col_names) + "-+"
        print(header)
        print(divider)

        for i in range(self.n):
            row_str = f"{str(self.row_names[i]).rjust(max_r_label)} | "
            cells = []
            for j in range(self.n):
                val = self.matrix[i][j]
                is_r = i in covered_rows
                is_c = j in covered_cols
                if is_r and is_c:
                    tag = "X"
                elif is_r:
                    tag = "H"
                elif is_c:
                    tag = "V"
                else:
                    tag = "U"
                cells.append(format_cell(f"{val} ({tag})", col_width))
            row_str += " | ".join(cells) + " |"
            print(row_str)
        print(divider)

    def _finalize_assignment(self, match_row):
        print_banner("OPTIMAL ASSIGNMENT RESULTS")
        
        # Display Final Assignment Matrix
        assigned_matrix = []
        for i in range(self.n):
            row_vals = []
            for j in range(self.n):
                orig_c = self.orig_matrix[i][j]
                if match_row[i] == j:
                    row_vals.append(f"[{orig_c}]*")
                else:
                    row_vals.append(f"{orig_c}")
            assigned_matrix.append(row_vals)

        print_matrix(assigned_matrix, self.row_names, self.col_names, "Final Assignment Matrix (* indicates assigned cell)")

        total_time = 0
        print("\nIndividual Pairings & Schedule:")
        print("-" * 50)
        for i in range(self.n):
            j = match_row[i]
            cost = self.orig_matrix[i][j]
            total_time += cost
            print(f"  {self.row_names[i]}  -->  {self.col_names[j]}  |  Time/Cost = {cost}")
        print("-" * 50)
        print(f"Total Minimum Time / Cost = {total_time}")
        print("=" * 50 + "\n")
        return match_row, total_time
