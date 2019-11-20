import collections
import numpy as np
​
def select(scenes, n):
    d = sum(s[1] for s in scenes)
    p = [s[1]/d for s in scenes]
    for _ in range(n):
        yield np.random.choice([s[0] for s in scenes], 3, replace=False, p=p)
​
scenes = [('a', 1), ('b', 1), ('c', 2), ('d', 1), ('e', 1), ('f', 2)]
​
print(collections.Counter(x for y in select(scenes, 10000) for x in y))