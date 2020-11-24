'''
   CMPUT 275   Section B2   Assignment 1_i   Kevin Gordon   Anton Shlakhter
'''
import math, sys
import priority_queue
import graph_v2
import textserial
import serial

def city_graph_generator (graph):
    '''
    ***Copied directly from Roshan's post Saturday, 7 February 2015, 11:28 AM***
    Generates each line of the graph file.

    Args:
    graph: graph object

    Returns:
    Nothing.

    >>> g = graph_v2.Graph({1,2,3}, [(1,2), (2,3)])
    >>> print(*city_graph_generator(g), sep='', end='')
    V,1,0.0,0.0
    V,2,0.0,0.0
    V,3,0.0,0.0
    E,1,2,None
    E,2,3,None
    '''

    for v in sorted(graph.vertices()):
        yield 'V,{},0.0,0.0\n'.format(v)
    for (a, b) in sorted(graph.edges()):
        yield 'E,{},{},None\n'.format(a, b)

def read_undirected_city_graph(filename):
    '''
    ***Copied directly from Roshan's post Saturday, 7 February 2015, 11:28 AM***
    Opens the specified filename and calls the helper function. 
    Allows the helper function to have docstring tests.

    Args: 
    filename: file containing graph data.
    
    Returns: 
    graph object: constructed with data in filename.

    >>> input = graph_v2.random_graph(10000, 20000)
    >>> input_text = city_graph_generator(input)
    >>> result = read_undirected_city_graph_helper(input_text)
    >>> for (a, b) in input.edges():
    ...     input.add_edge((b, a))
    >>> result.vertices() == input.vertices()
    True
    >>> set(result.edges()) == set(input.edges())
    True
    '''

    with open(filename) as file:
        return read_undirected_city_graph_helper(file)

def read_undirected_city_graph_helper(file):
    '''
    Takes a CSV file containing graph information in the form
    of vertices and edges. Takes a dictionary to store ancillary
    graph data.

    Args: 
    file: containing graph data.

    Returns: 
    graph object constructed from the CSV file data.
    '''
    
    # Coordinate multiplier
    m = 100000

    g = graph_v2.Graph()
    
    # Consume a single line per iteration
    for line in file:        
        # Prepare line
        line_buffer = [x.strip('\n') for x in line.split(',')]
        # Handle cases by checking column 0        
        if line_buffer[0] == 'V':
            # Add graph vertex
            g.add_vertex(int(line_buffer[1]))
            if 'ancillary_data' in globals():
                # Store vertex coordinate data in dict, key is vertex ID,
                ancillary_data[int(line_buffer[1])] = \
                    (int(float(line_buffer[2])*m), int(float(line_buffer[3])*m))

        elif line_buffer[0] == 'E':
            # Create graph edge, bi-directional
            g.add_edge((int(line_buffer[1]), int(line_buffer[2])))
            g.add_edge((int(line_buffer[2]), int(line_buffer[1])))
            if 'ancillary_data' in globals():
                # Store street name in dict, key is vertex ID's (ID,ID), 
                # bi-directional
                ancillary_data[(int(line_buffer[1]), int(line_buffer[2]))] = \
                    line_buffer[3]
                ancillary_data[(int(line_buffer[2]), int(line_buffer[1]))] = \
                    line_buffer[3]

    return g

def least_cost_path(graph, start, dest, cost):
    """
    Find and return the least cost path in graph from start
    vertex to dest vertex.

    Efficiency: If E is the number of edges, the run-time is
    O( E log(E) ).

    Args:
    graph (Graph): The digraph defining the edges between the
    vertices.
    start: The vertex where the path starts. It is assumed
    that start is a vertex of graph.
    dest: The vertex where the path ends. It is assumed
    that start is a vertex of graph.
    cost: A function, taking a single edge as a parameter and
    returning the cost of the edge. For its interface,
    see the definition of cost_distance.

    Returns:
    list: A potentially empty list (if no path can be found) of
    the vertices in the graph. If there was a path, the first
    vertex is always start, the last is always dest in the list.
    Any two consecutive vertices correspond to some
    edge in graph.

    >>> graph = graph_v2.Graph({1,2,3,4,5,6,7,8,9,10,11}, [(1,2), (1,3), (1,6), \
    (2,1), (2,3), (2,4), (3,1), (3,2), (3,4), (3,6), (4,2), (4,3),\
    (4,5), (5,4), (5,6), (6,1), (6,3), (6,5), (7,8), (8,7),\
    (7,9), (9,7), (7,11), (11,7), (8,11), (11,8),(8,10), (10,8),\
    (8,9), (9,8), (9,11), (11,9)])
    >>> weights = {(1,2): 7, (1,3):9, (1,6):14, (2,1):7, (2,3):10,\
    (2,4):15, (3,1):9, (3,2):10, (3,4):11, (3,6):2,\
    (4,2):15, (4,3):11, (4,5):6, (5,4):6, (5,6):9, (6,1):14,\
    (6,3):2, (6,5):9, (7,8):1, (8,7):1, (7,9):2,\
    (9,7):2, (7,11):1, (11,7):1, (8,11):3, (11,8):3, (8,10):3,\
    (10,8):3, (8,9):2, (9,8):2, (9,11):2, (11,9):2 }
    >>> cost = lambda e: weights.get(e, float("inf"))
    >>> least_cost_path(graph, 1,5, cost)
    [1, 3, 6, 5]
    >>> least_cost_path(graph,3,5,cost)
    [3, 6, 5]
    >>> least_cost_path(graph,3,3,cost)
    [3]
    >>> least_cost_path(graph,3,11,cost)
    []
    >>> least_cost_path(graph,8,11,cost)
    [8, 7, 11]
    """

    if not graph.is_vertex(start):
        raise ValueError("Start point not in graph")

    if not graph.is_vertex(dest):
        raise ValueError("End point not in graph")
    
    reached = {}
    pq = priority_queue.BinaryHeap()    

    pq.add((start,start),0) # ((prev, curr), key_value)   

    while pq:
        temp = pq.pop_min() 
        if temp[0][1] not in reached:
            reached[temp[0][1]] = temp[0][0]
            # Add neighbours to priority queue, with total dist for key
            for succ in graph.neighbours(temp[0][1]):
                pq.add((temp[0][1], succ), temp[1]+cost((temp[0][1], succ)))

    # If no path
    if dest not in reached:
        return list()

    # Otherwise traverse the path, moving from dest->start
    path = [dest]
    curr = dest
    while curr != start:
        curr = reached[curr]
        path.append(curr)

    # Reorder to return start->dest
    path.reverse()

    return path


def cost_distance(e):
    '''
    Computes and returns the straight-line distance between the two
    vertices at the endpoints of the edge e.
   
    Dependent on global variable 'ancillary_data'

    Args:
    e: An indexable container where e[0] is the vertex id for the
    starting vertex of the edge, and e[1] is the vertex id for the
    ending vertex of the edge.

    Returns:
    numeric value: the distance between the two vertices.    
    '''
    
    p1 = (ancillary_data[e[0]][0], ancillary_data[e[0]][1])
    p2 = (ancillary_data[e[1]][0], ancillary_data[e[1]][1])

    # Return pythagorean distance
    return euclid_dist(p1,p2)


def find_nearest_waypoint(start, dest, distance_function):
    '''
    Compute and return the closest vertex to a given 
    start and end location.

    Dependent on global variable 'ancillary_data'

    Args:
    start: (tuple) start location requested by client
    dest: (tuple) dest location requested by client
    distance_function: function which computes distance between two points.
    
    Returns:
    Two integers: nearest vertex ID to start and dest as startID, destID
    '''

    dist_from_start = {}
    dist_from_dest = {}

    # Iterate through data, store distances in dictionaries.
    for vertex in ancillary_data.items():
        if(type(vertex[0]) == int):
            dist_from_start[vertex[0]] = distance_function(start, vertex[1])
            dist_from_dest[vertex[0]] = distance_function(dest, vertex[1])
            
    # Store ID with min distance, to be returned.
    startID = min(dist_from_start, key=dist_from_start.get)
    endID = min(dist_from_dest, key=dist_from_dest.get)

    return startID, endID
                

def wait_for_ack(acknowledge_key):
    '''
    Function which waits for acknowledge_key from client via standin in.

    Args:
    acknowledgement_key: expected acknowledge key sent from client.

    Returns:
    Nothing.
    '''

    ack = False
    while not ack:
        client_in = sys.stdin.readline()
        client_in = client_in.strip('\n')
        if client_in == acknowledge_key:
            ack = True

def euclid_dist(p1,p2):
    '''
    Computes the euclidean distance between two points, p1 and p2.

    Args: 
    p1, p2: Tuples, containing their respective (x,y,...,n) coordinates.
    
    Returns: 
    distance (float)

    >>> euclid_dist((0,0),(3,4))
    5.0
    >>> euclid_dist((0,0),(5,12))
    13.0
    >>> euclid_dist((0,0),(9,40))
    41.0
    '''

    total = 0
    
    for index in range(len(p1)):
        diff = (p1[index] - p2[index])**2
        total = total + diff

    return math.sqrt(total)

if __name__ == "__main__":
    # Init dict to store ancillary graph data.
    # cost_distance() and find_nearest_waypoint() are dependents.
    ancillary_data = {}
    
    filename = 'edmonton-roads-2.0.1.txt'
    
    # Read graph file into graph object, store ancillary_data
    le_graph = read_undirected_city_graph(filename)

    # Process Requests
    while True:
        # Get client input, parse
        with textserial.TextSerial(ser=serial.serial_for_url('loop://',timeout=0)) as f:
            client_in = f.readline().rstrip('\r\n')
        # If client is making request
            if client_in[0] == 'R':
                start = (int(client_in[1]), int(client_in[2]))
                dest = (int(client_in[3]), int(client_in[4]))
            # Find nearest vertices
                start, dest = find_nearest_waypoint(start, dest, euclid_dist)
            # Find shortest path
                shortest_path = \
                    least_cost_path(le_graph, start, dest, cost_distance)
            # Begin path transmission
                if len(shortest_path) <1:
                    print('N ' + str(len(shortest_path)) + "\n", file = f)

                else:
                    print('N ' + str(len(shortest_path)) + "\n", file = f)
                    wait_for_ack('A')
                    for wp in shortest_path:                
                        print(\
                            'W ' + str(ancillary_data[wp][0]) + ' ' + \
                                str(ancillary_data[wp][1]) +  "\n", file = f)
                        wait_for_ack('A')
                        
                    #sys.stdout.write("E\n")
                    print( "E\n", file = f)
