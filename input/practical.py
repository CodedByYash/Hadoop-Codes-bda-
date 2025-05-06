import sys
import os

def mapper():

    i_max = int(os.environ.get("i_max",3))
    k_max = int(os.environ.get("j_max",3))

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")
        matrix = parts[0]

        if matrix == "A":
            _, i, j, value = parts
            i, j = int(i),int(j)
            value = float(value)

            for k in range(k_max):
                print(f"{i},{k}\tA,{j},{value}")

        elif matrix == "B":
            _, i, j, value = parts
            i, j = int(i),int(j)
            value = float(value)

            for k in range(k_max):
                print(f"{i},{k}\tA,{j},{value}")