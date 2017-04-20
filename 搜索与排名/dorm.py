# -*- coding: utf-8 -*-
import random
import math

#代表宿舍，每个宿舍有两个可用的隔间
dorms = ['Zeus', 'Athena', 'Hercules', 'Bacchus', 'Pluto']

#代表学生及其首选和次选
prefs = [('Toby', ('Bacchus', 'Hercules')),
         ('Steve', ('Zeus', 'Pluto')),
         ('Andrea', ('Athena', 'Zeus')),
         ('Sarah', ('Zeus', 'Pluto')),
         ('Dave', ('Athena', 'Bacchus')),
         ('Jeff', ('Hercules', 'Pluto')),
         ('Fred', ('Pluto', 'Athena')),
         ('Suzie', ('Bacchus', 'Hercules')),
         ('Laura', ('Bacchus', 'Hercules')),
         ('Neil', ('Hercules', 'Athena'))]

domain = [(0, (len(dorms) * 2) - i-1)for i in range(0, len(dorms) * 2)]

def printsolution(vec):
    slots = []
    #为每个宿舍建两个槽
    for i in range(len(dorms)): slots += [i, i]

    #遍历每一名学生的安置情况：
    for i in range(len(vec)):
        x = int(vec[i])

        #从剩余槽中选择：
        dorm = dorms[slots[x]]
        #输出学生及其被分配的宿舍：
        print prefs[i][0], dorm
        #删除该槽
        del slots[x]
#成本函数
def dormcost(vec):
    cost = 0
    #建立一个槽序列
    slots = [0, 0, 1, 1, 2, 2, 3, 3, 4, 4]

    #遍历每一名学生
    for i in range(len(vec)):
        x = int(vec[i])
        dorm = dorms[slots[x]]
        pref = prefs[i][1]
        #首选成本为0，次选成本值为1
        if pref[0] == dorm: cost = 0
        elif pref[1] == dorm: cost += 1
        else: cost += 3

        del slots[x]

#遗传算法
def getneticoptimize(domain, costf, popsize = 20, step = 1,
                     mutprob = 0.2, elite = 0.1, maxtier = 100):

    #变异操作
    def mutate(vec):
        i = random.randint(0, len(domain)-1)
        if random.random() < 0.5 and vec[i] > domain[i][0]:
            return vec[0:i] + [vec[i] - step] + vec[i+1:]
        elif vec[i] < domain[i][1]:
            return vec[0:i] + [vec[i] + step] + vec[i+1:]
    #交叉操作
    def crossover(r1,r2):
        i = random.randint(1, len(domain)-2)
        return r1[0:i]+r2[i:]

    #构造初始种群(随机生成50组解)
    pop = []
    for i in range(popsize):
        vec = [random.randint(domain[i][0], domain[i][1])
               for i in range(len(domain))]
        pop.append(vec)

    #每一代中有多少胜出者
    topelite = int(elite * popsize)

    #主循环
    for i in range(maxtier):
        scores = [(costf(v), v) for v in pop]
        scores.sort()
        ranked = [v for (s, v) in scores]

        #从纯粹的胜出者开始
        pop = ranked[0:topelite]

        #添加变异和配对后的胜出者:
        while len(pop) < popsize:
            if random.random() < mutprob:
                #变异
                c = random.randint(0, topelite)
                pop.append(mutate(ranked[c]))
            else:
                #交叉
                c1 = random.randint(0, topelite)
                c2 = random.randint(0, topelite)
                pop.append(crossover(ranked[c1], ranked[c2]))

        #打印最优解
        print scores[0][0]

    return scores[0][1]

getneticoptimize(domain, dormcost)

