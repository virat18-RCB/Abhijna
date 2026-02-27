#!/usr/bin/python3
import hashlib
import sys
import time
import string
import itertools


# Convert hex hash to binary string
def hex_to_binary(hash_hex):
    binary = ""
    for char in hash_hex:
        binary += format(int(char, 16), "04b")
    return binary


# Count leading zero bits
def count_leading_zeros(hash_hex):
    binary = hex_to_binary(hash_hex)
    count = 0
    for bit in binary:
        if bit == '0':
            count += 1
        else:
            break
    return count


# Check if hash satisfies difficulty
def check_difficulty(hash_hex, nbits):
    binary = hex_to_binary(hash_hex)
    return binary.startswith('0' * nbits)


# SHA-256 hashing function
def sha256_hash(data):
    return hashlib.sha256(data).hexdigest()


# Generate combinations for nonce
def nonce_generator(characters):
    length = 1
    while True:
        for combo in itertools.product(characters, repeat=length):
            yield ''.join(combo)
        length += 1


# Proof-of-Work mining function
def create_pow(nbits, initial_hash):
    iterations = 0
    characters = string.ascii_letters + string.digits

    for nonce in nonce_generator(characters):
        combined = (initial_hash + nonce).encode()
        new_hash = sha256_hash(combined)
        iterations += 1

        if check_difficulty(new_hash, nbits):
            return nonce, new_hash, iterations


def main():

    if len(sys.argv) != 3:
        print("Usage: python3 pow.py <nbits> <message.txt>")
        return

    nbits = int(sys.argv[1])
    filename = sys.argv[2]

    with open(filename, "rb") as f:
        message = f.read()

    # Step 1: Initial hash
    initial_hash = sha256_hash(message)

    print("Mining started...")
    start_time = time.time()

    # Step 2: Create Proof-of-Work
    nonce, final_hash, iterations = create_pow(nbits, initial_hash)

    end_time = time.time()
    compute_time = end_time - start_time
    hash_rate = iterations / compute_time

    leading_zeros = count_leading_zeros(final_hash)

    # Step 3: Save to header.txt
    with open("header.txt", "w") as hf:
        hf.write(f"Initial-hash: {initial_hash}\n")
        hf.write(f"Proof-of-work: {nonce}\n")
        hf.write(f"Hash: {final_hash}\n")
        hf.write(f"Leading-zero-bits: {leading_zeros}\n")

    print("\n----- Mining Completed -----")
    print("File:", filename)
    print("Initial Hash:", initial_hash)
    print("Nonce (Proof-of-Work):", nonce)
    print("Final Hash:", final_hash)
    print("Leading Zero Bits:", leading_zeros)
    print("Iterations:", iterations)
    print("Time Taken:", round(compute_time, 4), "seconds")
    print("Hash Rate:", round(hash_rate, 2), "hashes/sec")


if __name__ == "__main__":
    main()