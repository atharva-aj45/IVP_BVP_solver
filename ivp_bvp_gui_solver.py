import tkinter as tk
from tkinter import messagebox
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Parameters
h = 0.01  # step size
N = 100   # number of steps
s_values = np.arange(0, 10, 0.1)  # range for s

# Function to perform Euler's method
def euler_method(P, s):
    u = 0  # u(0) = 0
    v = s  # v(0) = s
    for n in range(N):
        u += h * v
        v += h * (-P)
    return u

# Function to calculate the optimal initial value of s for a given P
def calculate_optimal_s(P):
    min_error = float('inf')
    optimal_s = None
    for s in s_values:
        u_at_1 = euler_method(P, s)
        error = abs(u_at_1 - 1)  # calculate error
        if error < min_error:
            min_error = error
            optimal_s = s
    return optimal_s

# Function for the analytical solution
def analytical_solution(P, y):
    return (-P / 2) * y**2 + (1 + P / 2) * y

# Function to plot the graph for a given P
def plot_graph():
    global P
    optimal_s = calculate_optimal_s(P)
    y_values = np.linspace(0, 1, N + 1)
    y_values_fd = np.linspace(0, 1, 100)
    
    plt.figure(figsize=(12, 8))
    
    u_analytical = analytical_solution(P, y_values)
    u_explicit = explicit_euler(P, h, N, optimal_s)
    u_implicit = implicit_euler(P, h, optimal_s)
    u_fd = finite_difference_bvp(P, len(y_values_fd), 0, 1)
    
    plt.plot(u_analytical, y_values, label=f'Analytical (P={P})', linestyle='--')
    plt.plot(u_explicit, y_values, label=f'Explicit Euler (P={P}, s={optimal_s})')
    plt.plot(u_implicit, y_values, label=f'Implicit Euler (P={P}, s={optimal_s})', marker='x', markersize=3)
    plt.plot(u_fd, y_values_fd, label=f'Finite Difference BVP (P={P})', marker='o', markersize=3)

    plt.title(f'Comparison of Numerical and Analytical Solutions with Optimal s (P={P})')
    plt.xlabel('u(y)')
    plt.ylabel('y')
    plt.legend()
    plt.grid()
    #plt.ylim(0, 1)
    #plt.xlim(0, 2)
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.show()

# Button function to print u'(0) value for the given P
def print_u_prime():
    global P
    optimal_s = calculate_optimal_s(P)
    message = f"For IVP: d²u/dy² = {'-' if P > 0 else ''}{P}\n"
    message += f"u(0) = 0\nOptimal u'(0) = {optimal_s}\n"
    messagebox.showinfo("Optimal Initial Value", message)

# Button function to print Jacobian matrix and its eigenvalues for the given P
def print_jacobian():
    global P
    y, u, u1 = sp.symbols('y u u1')
    f1 = u1
    f2 = -P
    F = sp.Matrix([f1, f2])
    variables = sp.Matrix([u, u1])
    Jacobian = F.jacobian(variables)
    
    # Calculate eigenvalues
    eigenvalues = Jacobian.eigenvals()
    
    # Format Jacobian matrix and eigenvalues for display
    jacobian_list = Jacobian.tolist()
    jacobian_str = "\n".join(["[" + "  ".join(f"{item}" for item in row) + "]" for row in jacobian_list])
    eigenvalues_str = "\n".join([f"Eigenvalue: {val}" for val in eigenvalues.keys()])
    
    messagebox.showinfo("Jacobian Matrix and Eigenvalues", f"Jacobian Matrix:\n\n{jacobian_str}\n\n{eigenvalues_str}")

# Define Explicit Euler Method
def explicit_euler(P, h, N, s):
    u = np.zeros(N + 1)
    v = np.zeros(N + 1)
    v[0] = s
    for n in range(N):
        u[n + 1] = u[n] + h * v[n]
        v[n + 1] = v[n] + h * (-P)
    return u

# Define Implicit Euler Method
def implicit_euler(P, h, s):
    steps = int(1 / h)
    u = np.zeros(steps + 1)
    v = np.zeros(steps + 1)
    v[0] = s
    for n in range(steps):
        v_new = v[n] - h * P
        u[n + 1] = u[n] + h * v_new
        v[n + 1] = v_new
    return u

# Define Finite Difference BVP
def finite_difference_bvp(P, N, u0, u1):
    h = 1.0 / N
    A = np.zeros((N, N))
    b = np.zeros(N)
    for i in range(1, N - 1):
        A[i, i - 1] = 1 / h**2
        A[i, i] = -2 / h**2
        A[i, i + 1] = 1 / h**2
    for i in range(1, N - 1):
        b[i] = -P
    A[0, 0] = 1
    b[0] = u0
    A[-1, -1] = 1
    b[-1] = u1
    return np.linalg.solve(A, b)

def go_to_second_interface():
    global P, frame_second  # Declare frame_second as global
    
    try:
        # Get the input value of P
        P = float(entry_P.get())
        
        # Hide the first frame and display the second interface
        frame_first.pack_forget()
        
        # Second interface with buttons
        frame_second = tk.Frame(root, bg="black")
        frame_second.pack(pady=20, padx=20)

        btn_u_prime = tk.Button(frame_second, text="u'(0) for u(1)=1", command=print_u_prime,font=("Helvetica", 12,"bold"), bg="#6666ff", fg="white", width=30, height=2)
        btn_u_prime.grid(row=0, column=0, pady=10)

        btn_graph = tk.Button(frame_second, text="Plot Graph", command=plot_graph,font=("Helvetica", 12,"bold"), bg="#6666ff", fg="white", width=30, height=2)
        btn_graph.grid(row=1, column=0, pady=10)

        btn_jacobian = tk.Button(frame_second, text="Print Jacobian Matrix and Eigenvalues", command=print_jacobian,font=("Helvetica", 12,"bold"), bg="#6666ff", fg="white", width=30, height=2)
        btn_jacobian.grid(row=2, column=0, pady=10)

        # Back button to return to the first interface
        btn_back = tk.Button(frame_second, text="Back ", command=go_back_to_first_interface, font=("Helvetica", 12,"bold"), bg="#32CD32", fg="white", width=30, height=2)
        btn_back.grid(row=3, column=0, pady=10)

    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid numeric value for P.")

def go_back_to_first_interface():
    global frame_second
    
    # Destroy the second frame and go back to the first interface
    frame_second.destroy()
    
    # Show the first frame again
    frame_first.pack(pady=20, padx=20)
    
    # Clear the entry widget for P to enter a new value
    entry_P.delete(0, tk.END)

# Create the main Tkinter window
root = tk.Tk()
root.title("Differential Equation Solver GUI")
root.configure(bg="black")

header = tk.Label(root, text="IVP/BVP Solver", font=("Helvetica", 16, "bold"), fg="#333366", bg="#f0f0f5")
header.pack(pady=10)

# First interface to input P
frame_first = tk.Frame(root, bg="black")
frame_first.pack(pady=5, padx=5)


label_P = tk.Label(frame_first, text="Enter value for P:", bg="orange",width=15)
label_P.grid(row=0, column=0, padx=5, pady=5)
entry_P = tk.Entry(frame_first)
entry_P.grid(row=0, column=1, padx=5, pady=5)

btn_submit = tk.Button(frame_first, text="Submit", command=go_to_second_interface, width=15,bg="green")
btn_submit.grid(row=1, column=0, columnspan=2, pady=20)

btn_close = tk.Button(frame_first, text="Close", command=root.quit, width=15,bg="Red")
btn_close.grid(row=2, column=0, columnspan=2, pady=20)

# Run the Tkinter main loop
root.mainloop()
