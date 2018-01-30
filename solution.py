assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'
diagonal1_boxes = {'A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9'}
diagonal2_boxes = {'A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1'}  

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values
                
def cross(a, b):
    "Cross product of elements in A and elements in B."
    cross = []
    for row in a:
        for column in b:
            cross.append(row+column)
    return cross

def add_diagonal_peers(non_diagonal_peers):

    for peer in non_diagonal_peers.keys():
        
        if peer in diagonal1_boxes:
            non_diagonal_peers[peer].update(diagonal1_boxes)
            non_diagonal_peers[peer].remove(peer)
        if peer in diagonal2_boxes:
            non_diagonal_peers[peer].update(diagonal2_boxes)
            non_diagonal_peers[peer].remove(peer)    
    return non_diagonal_peers        

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers_excluding_diagonals = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
peers = add_diagonal_peers(peers_excluding_diagonals)

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
    Returns:
        values(dict): the values dictionary with the naked twins eliminated from peers.
    """
    #stores all naked twins
    naked_twin = {}
    for unit in unitlist:
        naked_twin_unit = {}
        for box in unit:
            if len(values[box]) == 2:
                if not values[box] in naked_twin_unit:
                    naked_twin_unit[values[box]] = [box]
                else:
                    naked_twin_unit[values[box]].append(box)
                    
        for each_twin in naked_twin_unit:
            if len(naked_twin_unit[each_twin]) == 2:
                if not each_twin in naked_twin:
                    naked_twin[each_twin] = [unit]
                else:
                    naked_twin[each_twin].append(unit)
                    
    # iterate through naked twins and elminate them
    for each_twin in naked_twin:
        for unit in naked_twin[each_twin]:
            for box in unit:
                if values[box] != each_twin:
                    values[box] = values[box].replace(each_twin[0], '')
                    values[box] = values[box].replace(each_twin[1], '')
    return values   
      
def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    if len(grid) != 81:
        return "Invalid input!"
    boxes= cross(rows,cols)
    i=0
    result = {}
    for box in boxes:
        if grid[i] == '.':
            result[box] = '123456789'
        else:
            result[box] = grid[i]
        i = i + 1 
    return result
    
def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
    """
    print()
    i = 1
    for row in rows:
        j = 1
        for column in cols:
            print(values[row+column] + ' ', end='')  
            if(j == 3 or j == 6):
                print('| ', end='')
            j = j + 1
        if(i == 3 or i == 6):
            print('\n------+-------+------')
        else:
            print()
        i = i + 1   
    return    

def eliminate(values):
    solved = []
    for value in values.keys():
        if(len(values[value]) == 1):
            solved.append(value)
            
    for item in solved:
        digit = values[item]
        # Remove solved digit from the list of possible values for each peer
        for peer in peers[item]:
            values[peer] = values[peer].replace(digit,'') 

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            # list of all the boxes in the unit that contain the digit
            digit_boxes = []
            for box in unit:
                if digit in values[box]:
                   digit_boxes.append(box) 
            if len(digit_boxes) == 1:
                values[digit_boxes[0]] = digit
                    
def number_of_solved_boxes(values):
    num = 0
    for box in values:
        if len(values[box]) == 1:
            num = num + 1 
    return num
    
def reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = number_of_solved_boxes(values)
        
        eliminate(values)
        only_choice(values)
        
        solved_values_after = number_of_solved_boxes(values)
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def found_solution(values):
    """
    Checks if sudoku is solved.
    Args:
        A sudoku in dictionary form.
    Returns:
        True if solved or False if not solved.
    """
    for box in boxes:
        if len(values[box]) != 1:
            return False
    return True 

def get_square_with_least_possibilities(values):
    i=2
    while(i<10):
        for box in values:
            if len(values[box]) == i:
                return box
        i = i + 1     
    
def search(values):
    values = reduce_puzzle(values)
    if values is False:
        return False # Solution Not Found
    if found_solution(values):
        return values  # Solution Found
    # Choose one of the unfilled squares with the fewest possibilities
    least_possibility_box = get_square_with_least_possibilities(values)
    # try solving sudoku with each possible value of unfilled square
    for value in values[least_possibility_box]:
        new_sudoku = values.copy()
        new_sudoku[least_possibility_box] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    input_grid = grid_values(grid)
    return search(input_grid)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
