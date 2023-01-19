import numba
import random

@numba.jit
def monte_carlo_pi(n_samples: int):
    acc = 0
    for i in range(n_samples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / n_samples

print(monte_carlo_pi(10000000))