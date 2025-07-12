# IVP_BVP_solver
A Python-based graphical user interface (GUI) tool to solve **Initial Value Problems (IVP)** and **Boundary Value Problems (BVP)** using numerical methods. This project supports multiple methods like Explicit Euler, Implicit Euler, and Finite Difference, with comparisons to the analytical solution.

---
##  Features

- Solve second-order ODEs of the form:  
  **d²u/dy² = -P**, with **u(0) = 0**, and **u(1) = 1**
- Calculates optimal value of u′(0) using shooting method (for IVP)
- Displays:
  - Analytical solution
  - Explicit Euler solution
  - Implicit Euler solution
  - Finite Difference solution
- Computes and displays **Jacobian matrix** and **eigenvalues**
- Interactive **Tkinter-based GUI**
---
- ## Numerical Methods Used
- **Euler’s Method**
  - Explicit Euler
  - Implicit Euler
- **Finite Difference Method** (for solving BVP)
- **Shooting Method** – to determine optimal initial slope u′(0) that satisfies the boundary condition u(1) = 1
- **Symbolic Jacobian Computation** – using **SymPy** for Jacobian matrix and eigenvalue analysis
---
##  Output Example
- **Optimal value of** u′(0) **that satisfies** u(1) = 1
- **Graphical plot** comparing:
  - Analytical solution
  - Explicit Euler
  - Implicit Euler
  - Finite Difference Method
- **Jacobian matrix** and its **eigenvalues** displayed in a dialog box
---

## Author
- **Atharva Joshi**<br>
- **IIT Hyderabad**
