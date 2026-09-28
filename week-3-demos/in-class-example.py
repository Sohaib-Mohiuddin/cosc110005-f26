# Variables and Constants

# Constants
PI = 3.14159

# String variable
greeting = 'Hello, world!'

# Integer variable
age = 25

# Float variable
age = 25.5

# Boolean variable
is_alive = True

# List variable
fruits = ['apple', 'banana', 'cherry']

# Dictionary variable
person = {
    'name': 'Sohaib',
    'weight': 200,
    'age': 35.5,
    'alive': True,
    'hobbies': ['Working Out, Teaching, Programming']
}

# Arithmetic 

# y = (m * x) + b
m = 5.0
x = 2
b = 25

# y = (m * x) + b
# print(f'The value of y is {((m * x) + b):.10f}')

# String Manipulation
first_name = 'sohaib mohiuddin'
# last_name = 'Mohiuddin'

# print(f'{ first_name[7:] }')
# print(f'{ first_name.replace('i', 'c', 2) }')

# Try/Except - Casting/Conversion
try:
    person_weight = float(input("Enter your weight now!: "))
except:
    print("You're Wrong!")

print(f'The person\'s weight + age is: {person_weight + 35}')

# Pseudocode
# while x is greater than 0
# Decrement x
# print x

x = 10
while (x > 0):
    x-=1
    print(f'x is { x }')