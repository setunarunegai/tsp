#!/usr/bin/env python3

import sys
import math
import random

from common import print_tour, read_input


def distance(city1, city2):
    return math.sqrt((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2)

def dist_list(N, cities):
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

def mountain(cities):
    N = len(cities)
    dist = dist_list(N, cities)
    tour = solve(N, dist)
    roop_count = 0
    while roop_count < N*50:
        choice_border = 0
        while choice_border < N*100:
            #ランダ�?に二つの点a,cを選ぶ, tourにおいてのindexを与え�?
            a_tour_index = random.randrange(0, N-3)
            c_tour_index = random.randrange(a_tour_index, N-1)
            #二つの点の次の点b,dを確認a<b<c<d, citiesにおいてのindexを与え�?
            b = tour[a_tour_index+1]
            d = tour[c_tour_index+1]
            a = tour[a_tour_index]
            c = tour[c_tour_index]
            #ab+cdとacとbdのdistanceを比�?
            sa = (dist[a][b]+dist[c][d]) - (dist[a][c]+dist[b][d])
            base = 1.0898 #�?
            #絶対値が大きい値�?と計算できな�?ので
            if sa<-100: sa = -100
            elif sa>10: sa = 10
            if math.pow(base, sa) >= random.uniform(0.99, 1.0):
                #小さかったらacとbd:b~cをreverse
                reverse_list = tour[a_tour_index+1:c_tour_index+1] #b以上c以下をreverse
                tour[a_tour_index+1:c_tour_index+1] = list(reversed(reverse_list))
                break
            choice_border += 1
        if choice_border > N*N:
            break
        roop_count += 1
    return tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = mountain(read_input(sys.argv[1]))
    print_tour(tour)
