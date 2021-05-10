import re

with open("result.txt", "r") as f:
    lines = f.readlines()

for i in range(len(lines)):
    tmp = lines[i].replace('\n', '')
    lines[i] = f"{tmp} $ {i}\n"

with open("result.txt", "w") as f:
    f.writelines(lines)