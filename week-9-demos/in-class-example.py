# def add(*args):
#     return sum(args)

# print(add(200, 200))
nums = [1, 2, 3, 4, 50, 20, 40]
def is_true(nums:list):
    for num in nums:
        if (num == 20):
            return True
    
    return False

if (is_true(nums) == True):
    print("You did it!")
else:
    print("Whoops, you messed up!")