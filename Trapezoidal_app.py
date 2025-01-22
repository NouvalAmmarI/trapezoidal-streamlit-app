import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from sympy import sympify, lambdify, symbols

# Judul aplikasi
st.title("Numerical Integration with Trapezoidal Rule")
st.markdown("""
This app demonstrates the Trapezoidal Rule for numerical integration. You can input a function, specify integration limits, and observe the results.
""")

# Input dari pengguna
function_input = st.text_input("Enter the function to integrate (in terms of x):", value="sin(x)")
a = st.number_input("Lower limit of integration (a):", value=0.0)
b = st.number_input("Upper limit of integration (b):", value=np.pi)
n = st.slider("Number of sub-intervals:", min_value=1, max_value=100, value=10)

# Fungsi untuk menghitung integral trapezoidal
def trapezoidal_rule(f, a, b, n):
    x = np.linspace(a, b, n+1)
    y = f(x)
    h = (b - a) / n
    integral = h * (np.sum(y) - 0.5 * (y[0] + y[-1]))
    return integral

try:
    # Parsing fungsi pengguna
    x = symbols('x')
    sympy_func = sympify(function_input)
    f = lambdify(x, sympy_func, modules=["numpy"])

    # Hitung integral menggunakan trapezoidal rule
    numerical_integral = trapezoidal_rule(f, a, b, n)

    # Hitung integral eksak (opsional)
    exact_integral = None
    try:
        exact_integral = float(sympy_func.integrate((x, a, b)))
    except:
        pass

    # Tampilkan hasil
    st.header("Results")
    st.write(f"**Numerical integral (Trapezoidal Rule):** {numerical_integral:.6f}")
    if exact_integral is not None:
        st.write(f"**Exact integral:** {exact_integral:.6f}")
        st.write(f"**Error:** {abs(exact_integral - numerical_integral):.6f}")
    else:
        st.write("**Exact integral:** Could not be calculated symbolically.")

    # Plot grafik
    X = np.linspace(a, b, 1000)
    Y = f(X)
    x_trapezoid = np.linspace(a, b, n+1)
    y_trapezoid = f(x_trapezoid)

    fig, ax = plt.subplots()
    ax.plot(X, Y, label="Function", color="blue")
    ax.fill_between(x_trapezoid, y_trapezoid, step='mid', color="orange", alpha=0.4, label="Trapezoid Approximation")
    ax.set_title("Trapezoidal Approximation")
    ax.set_xlabel("x")
    ax.set_ylabel("f(x)")
    ax.legend()

    st.pyplot(fig)

except Exception as e:
    st.error(f"Error: {e}")
