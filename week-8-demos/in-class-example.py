height = list()
weight = list()

for val in range(5):
    user_input_height = float(input("Enter your height in cm: "))
    user_input_weight = float(input("Enter your weight in lbs: "))

    height.append(user_input_height)
    weight.append(user_input_weight)

# print(f'The heights are: {height}\nThe weights are: {weight}')
print(f'The second user\'s information is: {height[1]}cm and {weight[1]}lbs')