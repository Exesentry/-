#!/usr/bin/env python
# coding: utf-8

# In[ ]:


Results = {} 
Result = 0

def PUSK(): 
    global Result, Results
    inp = input('Ввод ')
    
    if 'save' in inp: 
        Results[inp[inp.index(' ')+1:]]=Result
        print('save success')
        PUSK()
    elif 'del' in inp: 
        Results.pop(inp[inp.index(' ')+1:])
        print('delete success')
        PUSK()
    elif inp in Results.keys(): 
        Result=Results[inp]
        if Result[0]<Result[2]: 
            print(str(Result[0]) + '/' + str(Result[2]))
        elif Result[0]>Result[2]: 
            print(str(Result[0]//Result[2]) + '(' + str(Result[0]%Result[2]) + '/' + str(Result[2]) + ')')
        else: 
            print(1)
        PUSK()
    elif inp=='to double':
        print(Result[0]/Result[2])
        PUSK()
    elif inp=='exit': 
        None
    else:
        

        inp = inp.replace(' ', '') 
        
        for key in Results.keys(): 
            inp = inp.replace(key, str(Results[key][0]) + '/' + str(Results[key][2]))
        
        inp = list(inp)
        
        i = 0
        while i<(len(inp)): 
            try:
                inp[i] = int(inp[i])
                inp[i+1] = int(inp[i+1])
            except:
                i+=1
            else:
                inp[i]=int(str(inp[i])+str(inp[i+1]))
                inp.pop(i+1)

        for i in range(len(inp)-1): 
            if (inp[i]=='-') and (i==0):
                inp.pop(i)
                inp[i] = -inp[i]
            elif inp[i]=='-':
                inp[i] = '+'
                inp[i+1] = -inp[i+1]

        i = 0
        while i < len(inp)-5: 
            if (type(inp[i])==int) and (inp[i+1]=='(') and (type(inp[i+2])==int) and (inp[i+3]=='/') and (type(inp[i+4])==int) and (inp[i+5]==')'):
                inp[i+2]+=inp[i]*inp[i+4]
                inp.pop(i)
            i += 1

        def brackets(X): 
            X.remove('(')
            counter=0
            start=0
            while counter<X.count(')'):
                start = X.index(')', start,)
                counter+=1
            X.pop(start)
            return X

        def Add(A, B): 
            if (len(A)==1) and (len(B)==1):
                return [A[0]+B[0]]
            elif (len(A)==1) and (len(B)==3):
                return [A[0]*B[2]+B[0], '/', B[2]]
            elif (len(A)==3) and (len(B)==1):
                return [B[0]*A[2]+A[0], '/', A[2]]
            elif (len(A)==3) and (len(B)==3):
                return [A[0]*B[2]+B[0]*A[2], '/', A[2]*B[2]]

        def Mult(A, B):
            if (len(A)==1) and (len(B)==1):
                return [A[0]*B[0]]
            elif (len(A)==1) and (len(B)==3):
                return [A[0]*B[0], '/', B[2]]
            elif (len(A)==3) and (len(B)==1):
                return [B[0]*A[0], '/', A[2]]
            elif (len(A)==3) and (len(B)==3):
                return [A[0]*B[0], '/', A[2]*B[2]]

        
        primitives = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499)

        def DivRecursion(A, B): 
            for nod in primitives:
                if (A[0]%nod==0) and (B[0]%nod==0):
                    A[0]=A[0]//nod
                    B[0]=B[0]//nod
                    DivRecursion(A, B)

        def Div(A, B): 
            DivRecursion(A, B)
            if len(A) == 3:
                if len(B) == 3:
                    return [A[0]*B[2], '/', A[2]*B[0]]
                else:
                    return [A[0], '/', A[2]*B[0]]
            elif len(B) == 3:
                return [A[0]*B[2], '/', B[0]]
            else:
                return [A[0], '/', B[0]]

        def F(X): 
            if ('+' in X) and ((('(' not in X) and (')' not in X)) or (X.index('(')>X.index('+')) or (X.index(')')<X.index('+'))):
                A = X[0:X.index('+')]
                B = X[X.index('+')+1:]
                return (Add(F(A), F(B)))
            elif ('*' in X) and ((('(' not in X) and (')' not in X)) or (X.index('(')>X.index('*')) or (X.index(')')<X.index('*'))):
                A = X[0:X.index('*')]
                B = X[X.index('*')+1:]
                return (Mult(F(A), F(B)))
            elif ('/' in X) and ('(' in X) and (')' in X) and (not ((X.count('(') == 1) and (X.count(')') == 1) and (X.index('(') == 0) and (X.index(')') == len(X)-1))):
                for i in range(len(X)):
                    if (X[i] == '/') and (X[:i].count('(') == X[:i].count(')')):
                        A = X[0:i]
                        B = X[i+1:]
                        if A[1] == B[1] and A[3] == B[3]:
                            return ([1])
                        else:
                            return (Div(F(A), F(B)))
                
            elif ('(' in X) and (')' in X):
                brackets(X)
                return(F(X))
            else:
                return X
        
        Result = F(inp) 
        if len(Result) > 1:
            Result = Div([Result[0]], [Result[2]]) 

      
        if len(Result) == 1:
            print(Result[0])
        elif Result[0]<Result[2]:
            print(str(Result[0]) + '/' + str(Result[2]))
        elif Result[0]>Result[2]:
            print(str(Result[0]//Result[2]) + '(' + str(Result[0]%Result[2]) + '/' + str(Result[2]) + ')')
        else:
            print(1)
        PUSK() 
PUSK() 

