#!/usr/bin/python3
import hashlib
import sys


def hex_to_binary(hash_hex):
    binary = ""
    for char in hash_hex:
        binary += format(int(char, 16), "04b")
    return binary


def count_leading_zeros(hash_hex):
    binary = hex_to_binary(hash_hex)
    count = 0
    for bit in binary:
        if bit == '0':
            count += 1
        else:
            break
    return count


def sha256_hash(data):
    return hashlib.sha256(data).hexdigest()


def parse_header(lines):
    initial_hash = ""
    pow_value = ""
    final_hash = ""
    lzb = ""

    for line in lines:
        line = line.strip()

        if line.startswith("Initial-hash:"):
            initial_hash = line.split(":", 1)[1].strip()

        elif line.startswith("Proof-of-work:"):
            pow_value = line.split(":", 1)[1].strip()

        elif line.startswith("Hash:"):
            final_hash = line.split(":", 1)[1].strip()

        elif line.startswith("Leading-zero-bits:"):
            lzb = line.split(":", 1)[1].strip()

    return initial_hash, pow_value, final_hash, lzb


def main():

    if len(sys.argv) != 3:
        print("Usage: python3 verify.py <header.txt> <message.txt>")
        return

    header_file = sys.argv[1]
    message_file = sys.argv[2]

    with open(header_file, "r") as hf:
        header_lines = hf.readlines()

    with open(message_file, "rb") as mf:
        message = mf.read()

    initial_hash = sha256_hash(message)

    header_initial, nonce, header_hash, lzb = parse_header(header_lines)

    fail = False

    # Check initial hash
    if header_initial != initial_hash:
        print("ERROR: Initial hash mismatch")
        fail = True
    else:
        print("PASSED: Initial hash correct")

    # Recalculate PoW hash
    new_hash = sha256_hash((initial_hash + nonce).encode())

    # Check leading zeros
    calculated_lzb = count_leading_zeros(new_hash)

    if calculated_lzb != int(lzb):
        print("ERROR: Leading zero bits incorrect")
        fail = True
    else:
        print("PASSED: Leading zero bits correct")

    # Check final hash
    if new_hash != header_hash:
        print("ERROR: Final hash mismatch")
        fail = True
    else:
        print("PASSED: Final hash correct")

    print("\nFINAL RESULT:", "PASS" if not fail else "FAIL")


if __name__ == "__main__":
    main()