import pandas as pd
import numpy as np

def run_spsa_sigma(start_guess):
    initial_guess = start_guess
    best_estimate = np.copy(initial_guess)

    ck_manipulate = [1.0]