# Naked Twins
In naked twins technique we first select a box and find all its peers that contain the same value. If the number of possible values of that box equals the count of its peers containing same value, then we are going to eliminate those values from all peers of the box (excluding the ones having same value). This technique helps to solve stalled sudoku problem in many cases.

For solving diagonal grid used constaint propagation by repeatedly applying elimination and only choice technique. Each time we apply elimination/only choice technique, it leads to more solved sudoku which might eventually lead to solution. 
