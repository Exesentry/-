#!/usr/bin/env python
# coding: utf-8

# In[5]:


import math
def f1(p1, p2):
    assert isinstance(p1, tuple) and isinstance(p2, tuple), "Тип данных не float и не int"
    assert len(p1) == 2 and len(p2) == 2, "Кортеж имеет не 2 элемента"
    for i in p1:
        if not(isinstance(i, float) or isinstance(i, int)):
            raise TypeError("Некорректный тип данных в 1 котреже")
    for i in p2:
        if not(isinstance(i, float) or isinstance(i, int)):
            raise TypeError("Некорректный тип данных во 2 котреже")
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]
    ky = x1 - x2
    kx = y1 - y2
    b = x1 * y2 - x2 *y1
    if b>0:
        return f'{ky}y = {kx}x + {b}'
    else:
        return f'{ky}y = {kx}x - {-b}'
f1((2, 14), (6, 18))


# In[6]:


def f2():
    inter = 0
    payments = 0
    loan = 0
    monthly = 0
    duration = 0
    Price = input("Сумма займа: ")
    Rate = int(input("Процентная ставка: "))
    Time = input("Расчетное времяя выплаты: ")
    duration = float(Time)
    loan = float(Price)
    inter = float(Rate)
    payments = duration * 12
    monthly = loan * inter * (1 + inter) * payments                     / ((1+ Rate) * payments - 1)
    print(" %.2f $" % monthly)
f2()


# In[8]:


def f3():
    list_ = [216, 'qwerq', 213, 'ased', "qweg", 'cbvdfg', ['24', '22'], 'qwasda', [312, 12, 213]]
    list2 = ['qwerq', '213', 'cbvdfg', 12, [312, 12, 213]]
    match = []
    for i in list_:
        if i in match:
            continue
        for i2 in list2:
            if i == i2:
                match.append(i)
                break
    print(match)
f3()


# In[9]:


strangelist = ['q', 'qw', 'wq', 'qwe','12345','1233456789101112', '1', 'qwertyu', '22', 'zxcvbvbnmvmcbmvmcbmc22']
print(strangelist)
strangelist.sort(key = len)
print(strangelist)


# In[10]:


listner = []
for i in range(5):
    inputer = str(input('Требуется ввести слово  '))
    listner.append(inputer)
print(dict((x, listner.count(x)) for x in set(listner) if listner.count(x)> 1))


# In[ ]:




