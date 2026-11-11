alphabets = ['A', 'B', 'C', 'D', 'a', 'b', 'c', 'd']
albhed =    ['D', 'Y', 'Q', 'R', 'd', 'y', 'q', 'r']

def encode_function(some_str, key):
    empty_str = ''
    for index in range(len(some_str)):
        if some_str[index] in alphabets:
            some_str[index].replace(some_str[index], albhed[index])