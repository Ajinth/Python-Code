
def factorial(number):
    product = 1
    for i in range(number):
        i = i + 1
        product = product * i
    return product


a = eval(input("Enter a number: "))
b = factorial(a)
print(b)


