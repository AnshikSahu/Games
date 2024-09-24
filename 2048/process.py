import numpy as np

import ast

def string_to_list(string):
    try:
        return ast.literal_eval(string)
    except (ValueError, SyntaxError) as e:
        print(f"Error: {e}")
        return None

def rotate_90(matrix):
    return np.rot90(matrix)

def rotate_180(matrix):
    return np.rot90(matrix, k=2)

def rotate_270(matrix):
    return np.rot90(matrix, k=3)

def are_rotations(list1, list2):
    if len(list1) != 16 or len(list2) != 16:
        raise ValueError("The input lists must have 16 elements")
    
    matrix1 = np.array(list1).reshape(4, 4)
    matrix2 = np.array(list2).reshape(4, 4)
    
    if np.array_equal(matrix1, matrix2):
        return 0

    if np.array_equal(rotate_90(matrix1), matrix2):
        return 1

    if np.array_equal(rotate_180(matrix1), matrix2):
        return 2

    if np.array_equal(rotate_270(matrix1), matrix2):
        return 3

    return -1

mapping={0:{'up':'up','down':'down','left':'left','right':'right'},1:{'up':'right','down':'left','left':'up','right':'down'},2:{'up':'down','down':'up','left':'right','right':'left'},3:{'up':'left','down':'right','left':'down','right':'up'}}

import pandas as pd

data=pd.read_csv('new_data.csv')

rotations=[-1]*len(data)

grids=data['grid'].apply(string_to_list)

# for i in range(len(data)):
#     grids[i]=np.array(grids[i]).reshape(4,4)
    
# for i in range(len(data)):
    
#     if rotations[i]!=-1:
#         continue
#     rotations[i]=0
#     one=rotate_90(grids[i])
#     two=rotate_180(grids[i])
#     three=rotate_270(grids[i])
#     for j in range(i+1,len(data)):
#         if rotations[j]!=-1:
#             continue
#         if np.array_equal(grids[i],grids[j]):
#             rotations[j]=0
#         elif np.array_equal(one,grids[j]):
#             rotations[j]=1
#         elif np.array_equal(two,grids[j]):
#             rotations[j]=2
#         elif np.array_equal(three,grids[j]):
#             rotations[j]=3
        
#     if i%100==0:
#         data['rotations']=rotations
#         data.to_csv('new_data.csv',index=False)
#         print("Saved at",i)
        
#     print("Done with",i)
            
            