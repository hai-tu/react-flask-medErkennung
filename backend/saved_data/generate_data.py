

with open("Patient1/Planung/plan.txt", "r") as f:
    
    lines = f.readlines()
print(lines)
lines = [line.replace("\n", "") for line in lines]
lines = [line.replace(" ", "") for line in lines]
print(lines)
result = []
for line in lines:
    med = line.split(",")
    med[1] = int(med[1])
    result.append(med)
print(result)
# for line in lines:
#     print(line)