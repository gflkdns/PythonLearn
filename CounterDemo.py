from collections import Counter

c = Counter({'ab': 4, 'b': 2})
c.update({'ab':1})
print(c)
print(c['ab'])
print(c['e'])
print(c['l'])
print(c['o'])
print(c['a'])
