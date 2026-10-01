import math

a = 'Sohaib'
x = 'Sohaib'
b = 'Bob'
c = 'KANGAROO'
d = 10
e = 20
f = 30
g = 'i'
h = 'I'
y = math.pi
print(f'{y:.10f}')

# Some change for github workflow

# Situation 1: Check if user input is equal a, b, or c
"""
user_input = input("Enter a name: ")

if (user_input == a):
    print(f'The user inputted value { user_input } is equal to a')
elif (user_input == b):
    print(f'The user inputted value { user_input } is equal to b')
elif (user_input.upper() == c):
    print(f'The user inputted value { user_input } is equal to c')
else:
    print(f'The user input, { user_input } did not match any of the conditions')
"""

# Situation 2: Check if user input is equal to c
"""
user_input = input("Please Enter a Name: ")
if (user_input == c):
    print(f'User Input is equal to c')
elif (user_input != c):
    print(f'{ user_input } is NOT equal to c')
"""

# Situation 3: Check if 2 user input add to value of d
# Situation 3.1: Check if 2 user input are greater than or less than e
"""
user_input1 = int(input("Please enter Number 1: "))
user_input2 = int(input("Please enter number 2: "))

sum = user_input1 + user_input2

if (sum > d):
    print(f'User inputs are greater than the value of d: { d }')
elif (sum < d):
    print(f'The sum of the 2 user inputs are less than the value of d: { d }')
else:
    print(f'The sum of the 2 user inputs EQUAL to the value of d: { d }')
"""

# Situation 4: Check if 2 user input multiply to value of f
"""
mult = user_input1 * user_input2

if (mult == f):
    print(f'The multiplication of the 2 user inputs EQUAL to the value of f: { f }')
else:
    print(f'The multiplication of the 2 user inputs Is NOT EQUAL to the value of f: { f }')
"""

# Situation 5: Check if 2 user input names are equal AND 2 user input numbers are greater than f
input1 = input("Enter name 1: ")
input2 = input("Enter name 2: ")
input3 = input("Enter number 1: ")
input4 = input("Enter number 2: ")

# a = b = d
# a, b, c = 10, 20, 30

sum = int(input3 + input4)

if input1 == input2 and sum > f:
    print(f'All conditions satisfied')
else:
    print(f'NO conditions satisfied')