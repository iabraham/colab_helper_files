spline = ['TT10\\cl-maze1.4', 'TT10\\cl-maze1.5', 'TT11\\cl-maze1.10',
          'TT11\\cl-maze1.2', 'TT11\\cl-maze1.3', 'TT11\\cl-maze1.4',
          'TT11\\cl-maze1.5', 'TT11\\cl-maze1.7', 'TT11\\cl-maze1.9',
          'TT12\\cl-maze1.1', 'TT12\\cl-maze1.2', 'TT12\\cl-maze1.3',
          'TT13\\cl-maze1.3', 'TT13\\cl-maze1.4', 'TT13\\cl-maze1.5',
          'TT14\\cl-maze1.1', 'TT14\\cl-maze1.2', 'TT14\\cl-maze1.5',
          'TT14\\cl-maze1.7', 'TT1\\cl-maze1.1', 'TT6\\cl-maze1.1',
          'TT6\\cl-maze1.4', 'TT6\\cl-maze1.6', 'TT6\\cl-maze1.8',
          'TT7_0001\\cl-maze1.1', 'TT7_0001\\cl-maze1.2', 
          'TT7_0001\\cl-maze1.3', 'TT7_0001\\cl-maze1.4', 
          'TT7_0001\\cl-maze1.5', 'TT7_0001\\cl-maze1.7',
          'TT8\\cl-maze1.1', 'TT8\\cl-maze1.2'] 

cell = ['TT10\\cl-maze1.4', 'TT10\\cl-maze1.5', 'TT10\\cl-maze1.6',
        'TT11\\cl-maze1.10', 'TT11\\cl-maze1.2', 'TT11\\cl-maze1.3',
        'TT11\\cl-maze1.4', 'TT11\\cl-maze1.5', 'TT11\\cl-maze1.6',
        'TT11\\cl-maze1.7', 'TT11\\cl-maze1.8', 'TT11\\cl-maze1.9',
        'TT12\\cl-maze1.1', 'TT12\\cl-maze1.2', 'TT12\\cl-maze1.3',
        'TT12\\cl-maze1.4', 'TT13\\cl-maze1.2', 'TT13\\cl-maze1.3',
        'TT13\\cl-maze1.4', 'TT13\\cl-maze1.5', 'TT14\\cl-maze1.1',
        'TT14\\cl-maze1.2', 'TT14\\cl-maze1.3', 'TT14\\cl-maze1.4',
        'TT14\\cl-maze1.5', 'TT14\\cl-maze1.6', 'TT14\\cl-maze1.7',
        'TT1\\cl-maze1.1', 'TT1\\cl-maze1.3', 'TT1\\cl-maze1.4',
        'TT1\\cl-maze1.5', 'TT6\\cl-maze1.1', 'TT6\\cl-maze1.4',
        'TT6\\cl-maze1.5', 'TT6\\cl-maze1.6', 'TT6\\cl-maze1.8',
        'TT7_0001\\cl-maze1.1', 'TT7_0001\\cl-maze1.2', 'TT7_0001\\cl-maze1.3',
        'TT7_0001\\cl-maze1.4', 'TT7_0001\\cl-maze1.5', 'TT7_0001\\cl-maze1.6',
        'TT7_0001\\cl-maze1.7', 'TT7_0001\\cl-maze1.8', 'TT8\\cl-maze1.1',
        'TT8\\cl-maze1.2', 'TT8\\cl-maze1.3']

graph_dict = {'A': {'0', '2'},
              'B': {'0', '3', '4'},
              'C': {'4', '5', '6'},
              'D': {'6', '7'},
              'E': {'1', '16', '2'},
              'F': {'1', '12', '14', '3'},
              'G': {'11', '12', '5', '8'},
              'H': {'8', '9'},
              'I': {'16'},
              'J': {'13', '14', '15'},
              'K': {'10', '11', '13'},
              'L': {'10'},
              '0': {'A', 'B'},
              '1': {'E', 'F'},
              '4': {'B', 'C'},
              '6': {'C', 'D'},
              '8': {'G', 'H'},
              '10': {'K', 'L'},
              '12': {'F', 'G'},
              '13': {'J', 'K'},
              '15': {'I', 'J'},
              '2': {'A', 'E'},
              '3': {'B', 'F'},
              '5': {'C', 'G'},
              '7': {'H'},
              '9': {'H', 'L'},
              '11': {'G', 'K'},
              '14': {'F', 'J'},
              '16': {'E'}}

blocks = {1: {'X': ['A', '0', '2'],
              'Y': ['B', '3', '4', 'C', '5', '6', 'D', '7']},
          2: {'X': ['4'], 
              'Y': ['A', '0', 'B', '2', '3', 'E', '1', 'F', '16', '14', 'I', '15', 'J']},
          3: {'X': ['6', 'D', '7'], 
              'Y': ['5', 'C', '4', '3', 'B', '0', '2', 'A']},
          4: {'X': ['16', "I", "15"], 
              'Y': ['14', 'J', '13', '11', 'K', '10', '9', 'L']},
          5: {'X': ['13'], 
              'Y': ['K', '10', 'L', '11', '9', 'G', '8', 'H', '5', '7', 'C', '6', 'D']},
          6: {'X': ['10', 'L', '9'],
              'Y': ['11', 'K', '13', '14', 'J', '15', '16', 'I']}}

for block, attribs in blocks.items():
    attribs['Z'] = [i for i in graph_dict.keys() if i not in (attribs['X'] + attribs['Y'])] 
    
layout = ['A','0', 'B', '4', 'C', '6', 'D', '2', '3', '5', '7', 'E', '1', 'F', 
          '12', 'G', '8', 'H', '16', '14', '11', '9', 'I', '15', 'J', '13', 
          'K', '10', 'L']

cityBlockIds = product([1,3], [1,3,5])
idxs = [(i,j) for i in range(5) for j in range(7)]

for v in cityBlockIds:
    idxs.remove(v)

gridbased_idxs = dict(zip(layout, idxs))
