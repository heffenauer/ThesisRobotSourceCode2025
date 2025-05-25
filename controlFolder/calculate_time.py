import numpy as np
import matplotlib.pyplot as plt

# Data
time = np.array([1.25, 1.5, 1.75, 2.0, 2.25, 2.75, 3.0, 3.25, 3.5, 4.0, 5.0])
distance = np.array([5, 17, 33, 52, 63, 77, 98.5, 113.5, 125, 148, 200])

# Fit a polynomial of degree 2 (quadratic) for time as a function of distance
coefficients = np.polyfit(distance, time, 2)
polynomial = np.poly1d(coefficients)

# Print coefficients
# print("Fitted coefficients for time based on distance:")
# print(f"a: {coefficients[0]}")
# print(f"b: {coefficients[1]}")
# print(f"c: {coefficients[2]}")

# Function to calculate time based on distance
def calculate_time(D):
    return polynomial(D)

# Example usage
# input_distance = float(input("Enter distance (cm): "))
# calculated_time = calculate_time(input_distance)
# print(f"The calculated time for {input_distance:.2f} cm is: {calculated_time:.2f} seconds")