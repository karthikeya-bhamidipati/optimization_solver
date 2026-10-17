# Optimization Techniques & Operations Research Solver

An interactive, educational Python application designed for **Optimization Techniques / Operations Research (OR)** coursework. It solves both **Transportation Problems** and **Assignment / Scheduling Problems** with complete step-by-step intermediate matrices, calculations, and final optimal costs/times.

---

## 📁 Project Structure

```text
optimization_solver/
├── main.py            # Main interactive CLI application & menus
├── transportation.py  # Transportation Problem Solver (NWCM, LCM, VAM, MODI)
├── assignment.py      # Assignment Problem Solver (Hungarian Method)
├── utils.py           # Table formatters, matrix printers, and input parsers
└── README.md          # Documentation and user guide
```

---

## 🚀 How to Run

1. Open your terminal or PowerShell in this directory:
   ```powershell
   cd C:\Users\karth\.gemini\antigravity\scratch\optimization_solver
   python main.py
   ```

2. Follow the on-screen prompts to choose your problem type and enter or load test matrices.

---

## 🎯 Features

### 1. Transportation Problem Solver
- **Matrix Inputs**:
  - Number of Sources ($m$) and Destinations ($n$).
  - $m \times n$ Unit Cost Matrix.
  - Supply vector (capacities of sources) and Demand vector (requirements of destinations).
  - Built-in balanced condition check ($\sum \text{Supply} = \sum \text{Demand}$).
- **Available Methods**:
  1. **North-West Corner Method (NWCM)**:
     - Starts from top-left cell $(S_1, D_1)$.
     - Step-by-step allocation $\min(\text{Supply}, \text{Demand})$.
     - Displays remaining supplies/demands and crossed-out rows/cols at every step.
  2. **Least Cost Method (LCM) / Matrix Minimum Method**:
     - Greedily selects the unallocated cell with the lowest unit cost.
     - Ties broken by maximum possible allocation.
  3. **Vogel's Approximation Method (VAM)**:
     - Calculates penalty costs (difference between the two lowest costs) for every active row and column.
     - Selects row/col with the largest penalty, allocating to its lowest-cost cell.
  4. **Compare All 3 IBFS & Global Optimization (MODI / u-v Method)**:
     - Computes and compares initial costs for NWCM, LCM, and VAM.
     - Picks the best Initial Basic Feasible Solution (IBFS).
     - Applies the **MODI ($u-v$) Method**:
       - Calculates dual variables $u_i$ and $v_j$ such that $u_i + v_j = c_{ij}$ for all basic cells.
       - Evaluates net opportunity costs $\Delta_{ij} = c_{ij} - (u_i + v_j)$ for all non-basic cells.
       - Checks optimality condition ($\Delta_{ij} \ge 0$).
       - If non-optimal, traces the closed stepping-stone cycle alternating $+ \theta$ and $- \theta$, determines $\theta$, and updates the basis.
  5. **Direct MODI Method**:
     - Runs the $u-v$ method directly from an initial feasible solution.

---

### 2. Assignment / Scheduling Problem Solver
- **Hungarian Method (Kuhn-Munkres Algorithm)**:
  - Takes an $n \times n$ matrix representing Worker/Task vs. Job/Machine costs or times.
  - **Step 1: Row Reduction**:
    - Identifies minimum element of each row and subtracts it.
  - **Step 2: Column Reduction**:
    - Identifies minimum element of each column and subtracts it.
  - **Step 3: Minimum Line Covering**:
    - Determines the minimum number of horizontal and vertical lines needed to cover all zeros (using König's theorem and bipartite matching).
    - Displays line coverage markers for every cell:
      - `[U]`: Uncovered
      - `[H]`: Covered by Horizontal line
      - `[V]`: Covered by Vertical line
      - `[X]`: Intersection of lines
  - **Step 4: Matrix Adjustment**:
    - If lines $< n$: finds smallest uncovered element $k$, subtracts $k$ from uncovered cells, and adds $k$ to intersection cells.
  - **Step 5: Final Zero Assignment**:
    - Produces the 1-to-1 optimal assignment pairings.
    - Displays final assigned matrix with `[ * ]` markers.
    - Computes and prints Total Minimum Time / Cost.

---

## 💡 Quick Testing
Both solvers include a **"Load classic textbook example"** option in the menu so you can immediately see the full step-by-step trace without having to type every matrix value manually!
