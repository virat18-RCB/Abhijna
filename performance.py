import time
import hashlib
import matplotlib.pyplot as plt

def mine(difficulty):
    nonce = 0
    start = time.time()

    while True:
        text = f"Performance Test {nonce}".encode()
        hash_result = hashlib.sha256(text).hexdigest()

        if hash_result.startswith("0" * difficulty):
            break

        nonce += 1

    end = time.time()
    return end - start


difficulties = [2, 3, 4, 5]
times = []

for d in difficulties:
    print(f"Testing Difficulty {d}...")
    t = mine(d)
    times.append(t)

plt.plot(difficulties, times)
plt.xlabel("Difficulty Level")
plt.ylabel("Mining Time (seconds)")
plt.title("Performance Analysis of Proof-of-Work")
plt.show()