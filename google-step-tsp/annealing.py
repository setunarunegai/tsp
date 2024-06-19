#!/usr/bin/env python3

import sys
import math
import random
from common import print_tour, read_input
from unionFind import unionFind

# Create a minimum spanning tree 
def create_mst(dist, N):
    edges = []
    for i in range(N):
        for j in range(i+1,N):
            edges.append((dist[i][j],i,j))
    edges.sort()
    uf = unionFind(N)
    mst = [[] for i in range(N)]
    
    for i in range(len(edges)):
        w,u,v = edges[i]
        # Not to create a cycle and not to have more than 2 edges
        if not uf.same(u,v) and len(mst[u]) < 2 and len(mst[v]) < 2:
            mst[u].append(v)
            mst[v].append(u)
            uf.unite(u,v)
    
    # Connect the two nodes with only one edge
    one_edge_node = []
    for i in range(N):
        if len(mst[i]) == 1:
            one_edge_node.append(i)
            
    # Check if there are two nodes with only one edge
    if len(one_edge_node) >= 2:
        mst[one_edge_node[0]].append(one_edge_node[1])
        mst[one_edge_node[1]].append(one_edge_node[0])

    return mst

# Create a path from the minimum spanning tree
def create_path(mst,N):
    visited = set()
    current = 0
    path = [current]
    visited.add(current)
    
    while len(path) < N:
        next_node = mst[current][0]
        if next_node in visited:
            next_node = mst[current][1]
        visited.add(next_node)
        path.append(next_node)
        current = next_node
    
    return path

# 2-opt algorithm to improve the solution
def two_opt(tour, dist):
    N = len(tour)
    while True:
        count = 0
        for i in range(N-2):
            for j in range(i+2, N):
                l1 = dist[tour[i]][tour[i + 1]]
                l2 = dist[tour[j]][tour[(j + 1) % N]]
                l3 = dist[tour[i]][tour[j]]
                l4 = dist[tour[i + 1]][tour[(j + 1) % N]]
                if l1 + l2 > l3 + l4:
                    tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
                    count += 1
        if count == 0:
            break
    return tour


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def makedist(N, cities):
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist

def solve(N, dist): #greedy
    current_city = 0
    unvisited_cities = set(range(1, N))
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour
"""

def solve(N, dist): #Hinano san
    mst = create_mst(dist, N)
    tour = create_path(mst,N)
    tour = two_opt(tour, dist)
    return tour
"""
def nrandom(n, N, tour, dist):
    if n==2:
        (sa, tour_index) =  random2(N, tour, dist)
    elif n==3:
        (sa, tour_index) =  random3(N, tour, dist)
    else:
        (sa, tour_index) =  random4(N, tour, dist)
    #絶対値が大きい値だと計算できないので
    if sa<-1000:
        sa = -1000
    elif sa>1000:
        sa = 1000
    return (sa,tour_index)

def random2(N, tour, dist):
    #tourにおいてのindexを与える
    a1_tour = random.randrange(0, N-3)
    b1_tour = random.randrange(a1_tour+2, N-1)
    #citiesにおいてのindexを与える
    a1_cities = tour[a1_tour]
    a2_cities = tour[a1_tour+1]
    b1_cities = tour[b1_tour]
    b2_cities = tour[b1_tour+1]
    #a1a2+b1b2とa1b1とa2b2のdistanceを比較
    sa = (dist[a1_cities][a2_cities]+dist[b1_cities][b2_cities]) - (dist[a1_cities][b1_cities]+dist[a2_cities][b2_cities])
    return (sa, [a1_tour, b1_tour, a1_tour+1, b1_tour+1])

def random3(N, tour, dist):
    #tourにおいてのindexを与える
    a1_tour = random.randrange(0, N-5)
    b1_tour = random.randrange(a1_tour+2, N-3)
    c1_tour = random.randrange(b1_tour+2, N-1)
    #citiesにおいてのindexを与える
    a1_cities = tour[a1_tour]
    a2_cities = tour[a1_tour+1]
    b1_cities = tour[b1_tour]
    b2_cities = tour[b1_tour+1]
    c1_cities = tour[c1_tour]
    c2_cities = tour[c1_tour+1]
    base_dist = (dist[a1_cities][a2_cities] + dist[b1_cities][b2_cities] + dist[c1_cities][c2_cities])
    replaced_dist = {}
    #以下四行、見づらい。良い書き方が分からない。
    replaced_dist[ (dist[a1_cities][b1_cities] + dist[a2_cities][c1_cities] + dist[b2_cities][c2_cities]) ] = [a1_tour, b1_tour, a1_tour+1, c1_tour, b1_tour+1, c1_tour+1]
    replaced_dist[ (dist[a1_cities][b2_cities] + dist[c1_cities][b1_cities] + dist[a2_cities][c2_cities]) ] = [a1_tour, b1_tour+1, c1_tour, b1_tour, a1_tour+1, c1_tour+1]
    replaced_dist[ (dist[a1_cities][b2_cities] + dist[c1_cities][a2_cities] + dist[b1_cities][c2_cities]) ] = [a1_tour, b1_tour+1, c1_tour, a1_tour+1, b1_tour, c1_tour+1]
    replaced_dist[ (dist[a1_cities][c1_cities] + dist[b2_cities][a2_cities] + dist[b1_cities][c2_cities]) ] = [a1_tour, c1_tour, b1_tour+1, a1_tour+1, b1_tour, c1_tour+1]
    sorted_replaced_dist = dict(sorted(replaced_dist.items(), key=lambda item: item[0]))
    min_distance = list(sorted_replaced_dist.keys())[0]
    sa = base_dist - min_distance
    return (sa, replaced_dist[min_distance])

def random4(N, tour, dist):
    #tourにおいてのindexを与える
    a1_tour = random.randrange(0, N-7)
    b1_tour = random.randrange(a1_tour+2, N-5)
    c1_tour = random.randrange(b1_tour+2, N-3)
    d1_tour = random.randrange(c1_tour+2, N-1)
    #citiesにおいてのindexを与える
    a1_cities = tour[a1_tour]
    a2_cities = tour[a1_tour+1]
    b1_cities = tour[b1_tour]
    b2_cities = tour[b1_tour+1]
    c1_cities = tour[c1_tour]
    c2_cities = tour[c1_tour+1]
    d1_cities = tour[d1_tour]
    d2_cities = tour[d1_tour+1]
    #a1a2+b1b2とa1b1とa2b2のdistanceを比較
    sa = (dist[a1_cities][a2_cities]+dist[b1_cities][b2_cities]+dist[c1_cities][c2_cities]+dist[d1_cities][d2_cities]) - (dist[a1_cities][c2_cities]+dist[a2_cities][c1_cities]+dist[b1_cities][d2_cities]+dist[b2_cities][d1_cities])
    return (sa, [a1_tour, c1_tour+1, d1_tour, b1_tour+1, c1_tour, a1_tour+1, b1_tour, d1_tour+1])

def mountain(cities):
    N = len(cities)
    dist = makedist(N, cities)
    tour = solve(N, dist)
    base = [1.0898, 1.04,1.0898, 1.04, 1.00000001] #指数関数の底 //1.506 46261 10 46354 100 46080
    if N < 6:
        opt_range = [2,2]
    else:
        opt_range = [2,3,2,3,4]
    roop_count = 0
    while roop_count < N*10:
        if(roop_count%(N)==0):
            print(roop_count)
        for n in opt_range:
            choice_border = 0
            while choice_border < N/2:
                (sa, tour_index) = nrandom(n, N, tour, dist)
                if sa>=(1-roop_count/(N*10))*10:
                #if sa>-1000 and math.pow(base[n-2], sa) >= random.uniform(0.2+roop_count/(N*10)*0.8, 1.0-roop_count/(N*10)*): #焼きなまし部分
                    print(f"change {n} sa {sa}")
                    new_tour = tour[:tour_index[0]+1]
                    for i in range(n-1):
                        if tour_index[i*2+1] < tour_index[i*2+2]:
                            new_tour += tour[tour_index[i*2+1]:tour_index[i*2+2]+1]
                        else:
                            reverse_tour = tour[tour_index[i*2+2]:tour_index[i*2+1]+1]
                            reverse_tour.reverse()
                            new_tour += reverse_tour
                    new_tour += tour[tour_index[n*2-1]:]
                    tour = new_tour
                    break
                choice_border += 1
            roop_count += 1

    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = mountain(read_input(sys.argv[1]))
    print_tour(tour)