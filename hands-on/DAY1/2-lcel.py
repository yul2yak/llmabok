from langchain_core.runnables import RunnableLambda, RunnableSequence, RunnableParallel

print('-- lambda --')


def increment(x):
    return x + 1


# r = RunnableLambda(lambda x: x + 1)
r = RunnableLambda(increment)
result = r.invoke(1)
print(result)           # 2

result = r.batch([1, 2, 3])
print(result)           # [2, 3, 4]


def square(x):
    return x * x


r2 = RunnableLambda(square)
result = r2.invoke(2)
print(result)           # 4
result = r2.batch([1, 2, 3])
print(result)           # [1, 4, 9]

print('-- sequence --')
r3 = RunnableSequence(r, r2)
result = r3.invoke(1)
print(result)           # 4
result = r3.batch([1, 2, 3])
print(result)           # [4, 9, 16]

chain = r | r2
print(chain.invoke(1))  # 4
print(chain.batch([1, 2, 3]))  # [4, 9, 16]

print('-- parallel --')
r4 = RunnableParallel(increment=r, square=r2)
result = r4.invoke(1)
print(result)           # {'0': 2, '1': 1}
result = r4.batch([1, 2, 3])
# [{'0': 2, '1': 1}, {'0': 3, '1': 4}, {'0': 4, '1': 9}]
print(result)

chain = r | {'increment': r, 'square': r2}
result = chain.invoke(1)
print(result)  # {'increment': 3, 'square': 4}
result = chain.batch([1, 2, 3])
# [{'increment': 3, 'square': 4}, {'increment': 4, 'square': 9}, {'increment': 5, 'square': 16}]
print(result)
