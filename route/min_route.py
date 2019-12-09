import osmnx as ox
import pickle as pkl
from pathlib import Path
import os
import requests

import math
import time
import requests
import pandas as pd
import networkx as nx

from osmnx.core import save_to_cache
from osmnx.core import get_from_cache
from osmnx.utils import log
import os



def get_min_elevation_gain(start_point, end_point, r):
    graph=nx.read_gpickle('map_data.pkl')
    src = ox.get_nearest_node(graph, start_point)
    tar = ox.get_nearest_node(graph, end_point)

    path = nx.shortest_path(graph, source=src, target=tar)
    min_dist = sum([graph[path[i]][path[i+1]][0]['length'] for i in range(0, len(path)-1)])
    min_gain = sum([max(0, graph[path[i]][path[i+1]][0]['grade']) for i in range(0, len(path)-1)])
    old_min_gain = min_gain
    
    node = {}
    for n in graph.nodes:
        node[n] = {}
        if n == src:
            node[n]['elevation_gain'] = 0
            node[n]['dist'] = 0
        elif n == tar:
            node[n]['elevation_gain'] = min_gain
            node[n]['dist'] = min_dist
        else:
            node[n]['elevation_gain'] = float("inf")
            node[n]['dist'] = float("inf")
    
        node[n]['prev'] = None
    
    node_list = []
    for n in graph.nodes:
        # tuple: (elevation_gain, id, dist)
        if n == src:
            node_list.append((0, n, 0))
        else:
            node_list.append((float("inf"), n, float("inf")))
    assert src == path[0] and tar == path[-1]

    max_dist = min_dist * r

    
    
    import heapq
    heapq.heapify(node_list)
    get_neighbors = lambda x: [i for i in x]
    visit = set()
    while len(node_list):
        # tuple: (elevation_gain, id, dist)
        egain, cur_node, dist = heapq.heappop(node_list)
        neighbors = get_neighbors(graph[cur_node])
        
        for neighbor in neighbors:
            if (cur_node, neighbor) in visit:
                continue
            visit.add((cur_node, neighbor))
            
            grade = max(0, graph[cur_node][neighbor][0]['grade']) # ignore negative grade
            length = graph[cur_node][neighbor][0]['length']
            if (dist + length > max_dist) or (egain + grade > min_gain):
                continue
            if egain + grade < node[neighbor]['elevation_gain']:
                node[neighbor]['elevation_gain'] = egain + grade
                node[neighbor]['dist'] = dist + length
                node[neighbor]['prev'] = cur_node
            elif egain + grade == node[neighbor]['elevation_gain']:
                if dist + length <= node[neighbor]['dist']:
                    node[neighbor]['dist'] = dist + length
                    node[neighbor]['prev'] = cur_node
            
            min_gain = min(min_gain, node[tar]['elevation_gain'])
            
            neighbor_tup = (node[neighbor]['elevation_gain'], neighbor, node[neighbor]['dist'])
            heapq.heappush(node_list, neighbor_tup)
    
    def get_path(node, cur):
        if cur is None:
            return
        ret = [cur]
        if node[cur]['prev'] is not None:
            ret.extend(get_path(node, node[cur]['prev']))
        return ret
    
    if min_gain == old_min_gain:
        xy_pos = [[graph.nodes[i]['x'], graph.nodes[i]['y']] for i in path]
        return {"new_path": xy_pos, "new_dist": min_dist, "new_elevation_gain": min_gain}
    
    new_path = get_path(node, tar)[::-1]
    assert min_gain == sum([max(0, graph[new_path[i]][new_path[i+1]][0]['grade']) for i in range(0, len(new_path)-1)])
    new_dist = sum([graph[new_path[i]][new_path[i+1]][0]['length'] for i in range(0, len(new_path)-1)])
    assert new_dist <= max_dist
    xy_pos = [[graph.nodes[i]['x'], graph.nodes[i]['y']] for i in new_path]
    return {"new_path": xy_pos, "new_dist": new_dist, "new_elevation_gain": min_gain}
