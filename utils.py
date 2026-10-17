"""
Utility helper functions for table formatting and safe user inputs.
"""

def print_banner(title, char="="):
    border = char * max(60, len(title) + 8)
    print(f"\n{border}")
    print(f"   {title}")
    print(f"{border}\n")

def print_section(title):
    print(f"\n--- {title} ---")

def format_cell(val, width=8):
    return str(val).center(width)

def print_matrix(matrix, row_labels=None, col_labels=None, title=None):
    if title:
        print_section(title)
    
    m = len(matrix)
    n = len(matrix[0]) if m > 0 else 0
    if m == 0 or n == 0:
        print("Empty matrix.")
        return

    if row_labels is None:
        row_labels = [f"R{i+1}" for i in range(m)]
    if col_labels is None:
        col_labels = [f"C{j+1}" for j in range(n)]

    max_r_label = max(len(str(lbl)) for lbl in row_labels)
    col_width = max(8, max(len(str(lbl)) for lbl in col_labels) + 2)

    # Header
    header = " " * (max_r_label + 3) + "| " + " | ".join(format_cell(lbl, col_width) for lbl in col_labels) + " |"
    divider = "-" * (max_r_label + 3) + "+" + "-+-".join("-" * col_width for _ in col_labels) + "-+"

    print(header)
    print(divider)
    for i in range(m):
        row_str = f"{str(row_labels[i]).rjust(max_r_label)} | "
        row_str += " | ".join(format_cell(matrix[i][j], col_width) for j in range(n)) + " |"
        print(row_str)
    print(divider)

def print_transportation_table(cost_matrix, alloc_matrix=None, supply=None, demand=None, title=None):
    if title:
        print_section(title)
        
    m = len(cost_matrix)
    n = len(cost_matrix[0])
    
    col_labels = [f"D{j+1}" for j in range(n)]
    if supply is not None:
        col_labels.append("Supply")

    max_r_label = max(len(f"S{i+1}") for i in range(m))
    if demand is not None:
        max_r_label = max(max_r_label, len("Demand"))
    col_width = 12

    header = " " * (max_r_label + 3) + "| " + " | ".join(format_cell(lbl, col_width) for lbl in col_labels) + " |"
    divider = "-" * (max_r_label + 3) + "+" + "-+-".join("-" * col_width for _ in col_labels) + "-+"

    print(header)
    print(divider)
    
    for i in range(m):
        row_str = f"S{i+1}".rjust(max_r_label) + " | "
        cells = []
        for j in range(n):
            c = cost_matrix[i][j]
            if alloc_matrix is not None and alloc_matrix[i][j] > 0:
                # Format showing cost and allocation: e.g. 19 [x=5]
                cell_repr = f"{c} [{alloc_matrix[i][j]}]"
            else:
                cell_repr = f"{c}"
            cells.append(format_cell(cell_repr, col_width))
        
        if supply is not None:
            cells.append(format_cell(str(supply[i]), col_width))
        row_str += " | ".join(cells) + " |"
        print(row_str)

    print(divider)
    
    if demand is not None:
        dem_str = "Demand".rjust(max_r_label) + " | "
        dem_cells = [format_cell(str(d), col_width) for d in demand]
        if supply is not None:
            dem_cells.append(format_cell(f"{sum(demand)}", col_width))
        dem_str += " | ".join(dem_cells) + " |"
        print(dem_str)
        print(divider)

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            val_str = input(prompt).strip()
            val = int(val_str)
            if min_val is not None and val < min_val:
                print(f"Value must be at least {min_val}. Try again.")
                continue
            if max_val is not None and val > max_val:
                print(f"Value must be at most {max_val}. Try again.")
                continue
            return val
        except ValueError:
            print("Invalid input! Please enter a valid integer.")

def get_list_input(prompt, length, val_type=int):
    while True:
        try:
            line = input(prompt).strip()
            parts = line.replace(",", " ").split()
            if len(parts) != length:
                print(f"Expected {length} values, but received {len(parts)}. Try again.")
                continue
            return [val_type(p) for p in parts]
        except ValueError:
            print("Invalid values entered. Please enter numbers separated by spaces or commas.")
