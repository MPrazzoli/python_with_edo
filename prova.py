import networkx as nx
from collections import Counter
import numpy as np
import pandas as pd

df = pd.DataFrame({'a':[1,.5,.3],'b':[.5,1,.4],'c':[1, 2, 1]},index=list('abc'))
df = df.where(np.triu(np.ones(df.shape), 1).astype(np.bool))
print (df)
df = df.stack().reset_index()
df.columns = ['Row','Column','Value']
print (df)

EDGES = [
    ('A', 'B'),
    ('B', 'C'),
    ('A', 'C'),
    ('C', 'D'),
    ('A', 'B')
]

g = nx.DiGraph((x, y, {'weight': v}) for (x, y), v in Counter(EDGES).items())

Ed = list(zip(df['Row'], df['Column']))

for (x, y), v in Counter(EDGES).items():
    print('ecco')


g = nx.DiGraph((x, y, {'weight': v}) for (x, y), v in Counter(Ed).items())

# g = nx.DiGraph((x, y, {'weight': df.c[Ed.index((x, y))]}) for (x, y) in Ed)
nx.draw_networkx(g, with_labels = True)
print(*g.edges(data=True), sep='\n')

# import numpy as np
# import pandas as pd
#
# df = pd.DataFrame({'a':[1,.5,.3],'b':[.5,1,.4],'c':[.3,.4,1]},index=list('abc'))
# df = df.where(np.triu(np.ones(df.shape), 1).astype(np.bool))
# print (df)
# df = df.stack().reset_index()
# df.columns = ['Row','Column','Value']
# print (df)





