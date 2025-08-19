# list
fruits = ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
# Output: ['orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana']
print(fruits)
print(fruits[1])   # Output: 'apple'


# set
fruits = {'orange', 'apple', 'pear', 'banana', 'kiwi', 'apple', 'banana'}
print(fruits)      # Output: {'pear', 'kiwi', 'banana', 'apple', 'orange'}
# print(fruits[1])   # TypeError: 'set' object is not subscriptable


# tuple - immutable sequence
apple = ('apple', 100)
print(apple)       # Output: ('apple', 100)
print(apple[1])    # Output: 100
# apple[1] = 200     # TypeError: 'tuple' object does not support item assignment


# dictionary
costs = {'apple': 100, 'banana': 200, 'kiwi': 300}
print('kiwi' in costs)         # Output: True
print(costs['kiwi'])           # Output: 300
print(costs.get('orange', 0))  # Output: 0

for fruit, cost in costs.items():
    print(f"{fruit}: {cost}")  # Output: apple: 100, banana: 200, kiwi: 300
