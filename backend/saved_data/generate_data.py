import json

user_data = {}

user_data["name"] = "Mike Halligan"
user_data["admission_time"] = "04.02.2000"
user_data["room"] = "Room 115"
user_data["remark"] = "Nothing"
print(user_data)
with open("Patient1/Information/info.json", "w") as file:
    json.dump(user_data, file)
# with open("Patient1/Planung/plan.txt", "r") as f:
    
#     lines = f.readlines()
# print(lines)
# lines = [line.replace("\n", "") for line in lines]
# lines = [line.replace(" ", "") for line in lines]
# print(lines)
# result = []
# for line in lines:
#     med = line.split(",")
#     med[1] = int(med[1])
#     result.append(med)
# print(result)
