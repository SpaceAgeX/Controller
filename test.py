# import subprocess


# command = input("Enter a command: ")
# val = subprocess.check_output(command, shell=True)

# print(str(val).split("'")[1])


for i in range(255):
    for j in range(255):
        print(f"192.168.{i}.{j}")