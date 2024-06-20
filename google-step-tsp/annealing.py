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

def greedy_solve(start, N, dist): #greedy
    current_city = start
    unvisited_cities = set(range(N))
    unvisited_cities.remove(current_city)
    tour = [current_city]

    while unvisited_cities:
        next_city = min(unvisited_cities,
                        key=lambda city: dist[current_city][city])
        unvisited_cities.remove(next_city)
        tour.append(next_city)
        current_city = next_city
    return tour

def optn(n, N, tour, dist):
    if n==2:
        (sa, tour_index) =  opt2(N, tour, dist)
    elif n==3:
        (sa, tour_index) =  opt3(N, tour, dist)
    else:
        (sa, tour_index) =  opt4(N, tour, dist)
    return (sa,tour_index)

def opt2(N, tour, dist):
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

def opt3(N, tour, dist):
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

def opt4(N, tour, dist):
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


def total_distance(tour, N, dist):
    return sum(dist[tour[i]][tour[(i + 1) % N]] for i in range(N))

def mountain(cities):
    N = len(cities)
    dist = makedist(N, cities)
    best_tour = []
    best_distance = 10000000000000
    opt_range = [2,3,2,3,4]
    roop_count = 0
    for start in [0,int(N/3),int(N*2/3)]: #O(1)
        roop_count = 0
        tour = greedy_solve(start, N, dist)
        while roop_count < N*3: #O(N)
            for n in opt_range: #O(1)
                choice_border = 0
                while choice_border < N/2: #O(N)
                    (calculate_distance, tour_index) = optn(n, N, tour, dist)
                    if calculate_distance>=(1-roop_count/(N*10))*10:
                        new_tour = tour[:tour_index[0]+1]
                        for i in range(n-1):
                            if tour_index[i*2+1] < tour_index[i*2+2]:
                                new_tour += tour[tour_index[i*2+1]:tour_index[i*2+2]+1]
                            else:
                                reverse_tour = tour[tour_index[i*2+2]:tour_index[i*2+1]+1] #O(N)
                                reverse_tour.reverse()
                                new_tour += reverse_tour
                        new_tour += tour[tour_index[n*2-1]:]
                        tour = new_tour
                        break
                    choice_border += 1
            roop_count += 1
        current_distance = total_distance(tour, N, dist)
        if current_distance < best_distance:
            best_distance = current_distance
            best_tour = tour

    return best_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = mountain(read_input(sys.argv[1]))
    print_tour(tour)