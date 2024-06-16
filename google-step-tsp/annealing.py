#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def makedist(N, cities):
    dist = [[0] * N for i in range(N)]
    for i in range(N):
        for j in range(i, N):
            dist[i][j] = dist[j][i] = distance(cities[i], cities[j])
    return dist

def solve(N, dist):
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

def nrandom(n, N, tour, dist):
    if n==2:
        (sa, tour_index) =  random2(N, tour, dist)
    else:
        (sa, tour_index) =  random3(N, tour, dist)
    #絶対値が大きい値だと計算できないので
    if sa<-10000: sa = -10000
    elif sa>10: sa = 10
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

def mountain(cities):
    N = len(cities)
    dist = makedist(N, cities)
    tour = solve(N, dist)
    roop_count = 0
    base = [1.0898, 1000] #指数関数の底
    if N < 6:
        opt_range = [2,2]
    else:
        opt_range = [2,3]
    for n in opt_range:
        while roop_count < N:
            choice_border = 0
            while choice_border < 2*N:
                (sa, tour_index) = nrandom(n, N, tour, dist)
                if math.pow(base[n-2], sa) >= random.uniform(0.99, 1.0): #焼きなまし部分
                    new_tour = tour[:tour_index[0]+1]
                    for i in range(n-1): #0~n-2
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
            if choice_border > 2*N:
                break
            roop_count += 1

    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = mountain(read_input(sys.argv[1]))
    print_tour(tour)