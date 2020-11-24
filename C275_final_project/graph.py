import math
import priority_queue
from objects import alien
from utilities import euclidD
ALN_HOP_DIST = alien.Alien.radius

'''
This file contains:
-a graph class (and helper Node class)
-Djikstra's shortest path
-Ford-Fulkerson Max-Flow
-A helper function to reconstruct flows
-A function to create a graph object from the game asteroids
'''

class Node():
    '''
    Used as a wrapper for the game objects, handy when splitting the asteroids
    into incoming/outoing nodes
    '''
    def __init__(self, obj):
        self.position = obj.position
        self.obj = obj

    def __repr__(self):
        # Used primarily for debugging
        return "%s"%(self.position[0])

class Graph:
    """
    Directed Graph Class from the Jan 22/23 lectures.

    Modified to include flows, capacities, weights as dicts.
    """

    def __init__(self, vertices = set(), edges = list()):
        """
        Construct a graph with a shallow copy of
        the given set of vertices and given list of edges.

        Efficiency: O(# vertices + # edges)

        >>> g = Graph({1,2,3},[(1,2,0,0), (2,3,0,0)])
        >>> g._alist.keys() == {1,2,3}
        True
        >>> # == [2]
        >>> g.is_edge((1,2))
        True
        >>> g.is_edge((2,1))
        True
        >>> g.is_edge((2,3))
        True
        >>> g.is_edge((3,2))
        True
        >>> g.is_edge((1,4))
        False
        >>> h1 = Graph()
        >>> h2 = Graph()
        >>> h1.add_vertex(1)
        >>> h2._alist.keys() == set()
        True
        """

        self._alist = dict()
        self._flows = dict()
        self._weights = dict()
        self._capacities = dict()

        for v in vertices:
            self.add_vertex(v)
        for e in edges:
            self.add_edge(e[0],e[1],e[2],e[3])

    def capacity(self, e):
        '''
        Getter for _capacities dictionary.

        Args:
        Edge e, a tuple with (start, dest) nodes

        Returns:
        Capacity of edge e
        '''
        return self._capacities[e]

    def flow(self, *args):
        '''
        Getter and setter for _flows dictionary.
        Gets edge flow when passed: (edge)
        Sets edge flow when passed: (edge), flow 

        Args:
        1 args: 
            edge e, tuple containing (start, dest)
        2 args:
            arg1: edge e, tuple containing (start, dest)
            arg2: flow f, integer flow passing through e
        
        Returns:
        1 args: flow through edge e
        2 args: none

        '''
        if len(args)==1:
            return self._flows[args[0]]
        if len(args)==2:            
            self._flows[args[0]] = args[1]

    def flow_out(self, u):
        '''
        Getter for outgoing flow from node u

        Args: 
        node u
        
        Returns:
        flow out of node u
        '''
        flow = 0
        for v in self.neighbours(u):
            flow += self.flow((u,v))
        return flow

    def add_vertex(self, v):
        """
        Add a vertex v to the graph.
        If v exists in the graph, do nothing.

        Efficiency: O(1)

        >>> g = Graph()
        >>> len(g._alist)
        0
        >>> g.add_vertex(2)
        >>> g.is_vertex(2)
        True
        """
        
        if v not in self._alist:
            self._alist[v] = list()

    def add_edge(self, u, v, c, w):
        """
        Add edge e to the graph.
        Raise an exception if the endpoints of
        e are not in the graph.

        Args:
        u: start or source node
        v: dest or sink node
        c: edge capacity
        w: edge weight

        Efficiency: O(1)

        >>> g = Graph()
        >>> g.add_vertex(1)
        >>> g.add_vertex(2)
        >>> g.add_vertex(3)
        >>> g.add_edge(1,2,0,0)
        >>> g.neighbours(1)
        [2]
        >>> g.neighbours(2)
        [1]
        >>> g.add_edge(2,3,0,0)
        >>> g.neighbours(2)
        [1, 3]
        >>> g.neighbours(3)
        [2]
        >>> g.neighbours(1)
        [2]
        """

        if not self.is_vertex(u) \
                or not self.is_vertex(v):
            raise ValueError("an endpoint is not in graph")
    
        

        # Append all edge/redge to node adjency list
        self._alist[u].append(v)
        self._alist[v].append(u)
        
        # Init all edge flows to zero
        self._flows[(u,v)] = 0
        self._flows[(v,u)] = 0
        
        # Add edge weights 
        self._weights[(u,v)] = w
        self._weights[(v,u)] = w
        
        # Add edge capacities
        self._capacities[(u,v)] = c
        self._capacities[(v,u)] = 0

            
    def is_vertex(self, v):
        """
        Check if vertex v is in the graph.
        Return True if it is, False if it is not.
        """
        return v in self._alist

    def is_edge(self, e):
        """
        Check if edge e is in the graph.
        Return True if it is, False if it is not.

        Efficiency: O(# neighbours of e[0])

        >>> g = Graph({1,2}, [(1,2,3,4)])
        >>> g.is_edge((1,2))
        True
        >>> g.add_edge(1,2,0,0)
        >>> g.is_edge((1,2))
        True
        """
        
        if e[0] not in self._alist:
            return False
        else:
            return e[1] in self._alist[e[0]]

    def neighbours(self, v):
        """
        Return a list of neighbours of v.
        A vertex u appears in this list as many
        times as the (v,u) edge is in the graph.

        If v is not in the graph, then
        raise a ValueError exception.

        Efficiency: O(1)

        >>> Edges =\
        [(1,2,0,0),(1,4,0,0),(3,1,0,0),(3,4,0,0),(2,4,0,0),(1,2,0,0)]
        >>> g = Graph({1,2,3,4}, Edges)
        >>> g.neighbours(1)
        [2, 4, 3, 2]
        >>> g.neighbours(4)
        [1, 3, 2]
        >>> g.neighbours(3)
        [1, 4]
        >>> g.neighbours(2)
        [1, 4, 1]
        """

        if not self.is_vertex(v):
            raise ValueError("vertex not in graph")        
        return self._alist[v]

    def vertices(self):
        """
        Returns the set of vertices in the graph.

        Efficiency: O(# vertices)

        >>> g = Graph({1,2})
        >>> g.vertices() == {1,2}
        True
        >>> g.add_vertex(3)
        >>> g.vertices() == {1,2,3}
        True
        """

        # dict.keys() is not exactly a set, so we have to create
        # one before returning
        return set(self._alist.keys()) 

    def edges(self):
        """
        Returns a list of tuples (u,v) corresponding to
        edges in the graph. Multiple copies of an edge in the graph
        appear in the returned list just as many times.

        Efficiency: O((# vertices) + (# edges))

        >>> g = Graph({1,2,3},[(1,2,0,0),(2,3,0,0)])
        >>> set(g.edges())=={(1,2),(2,1),(2,3),(3,2)}
        True
        >>> g.add_edge(3,1,0,0)
        >>> set(g.edges()) == {(1,2),(2,1),(2,3),(3,2),(1,3),(3,1)}
        True
        >>> h = Graph({1,2},[(1,2,0,0),(1,2,0,0)])
        >>> set(h.edges()) == {(1,2),(2,1),(1,2),(2,1)}
        True
        """

        # iterates over tuples (v,nbrs) where v is a key and edges = _alist[v]
        e = []
        for v,nbrs in self._alist.items():
            e.extend([(v,u) for u in nbrs])
        return e


#END OF CLASS DEFINITION

def find_shortest_path(graph, start, dest):
    """
    Modified assignment 1 shortest path algorithm.

    Find and return the least cost path in graph from start
    vertex to dest vertex for edges with capacity > 0.
    
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
    vertex is always the dest, the last is always the start in the list.
    Any two consecutive vertices correspond to some
    edge in graph.
   
    >>> graph =\
    Graph(\
    {1,2,3,4,5,6,7,8,9,10,11},\
    [(1,2,15,7), (1,3,15,9), (1,6,15,14), (2,3,15,10), (2,4,15,15),\
    (3,4,15,11), (3,6,15,2),\
    (4,5,15,6), (6,5,15,9), \
    (8,7,15,1), (7,9,15,2), (7,11,15,1),\
    (8,11,15,3),(8,10,15,3),(8,9,15,2),\
    (9,11,15,2)])
    >>> cost = lambda e: weights.get(e, float("inf"))
    >>> find_shortest_path(graph, 1,5)
    [(6, 5), (3, 6), (1, 3)]
    >>> find_shortest_path(graph,3,5)
    [(6, 5), (3, 6)]
    >>> find_shortest_path(graph,3,3)
    []
    >>> find_shortest_path(graph,3,11)
    []
    >>> find_shortest_path(graph,8,11)
    [(7, 11), (8, 7)]
    """
    if not graph.is_vertex(start):
        raise ValueError("Start point not in graph")

    if not graph.is_vertex(dest):
        raise ValueError("End point not in graph")
    
    # Already at the dest
    if start == dest:
        return list()

    # An empty dictionary of nodes we've reached
    reached = {}
    # Init the priority queue
    pq = priority_queue.BinaryHeap()    
    
    # Add the first edge
    pq.add((start,start),0) # ((prev, curr), key)

    # Until we've explored all edges in the priority queue
    while pq:

        temp = pq.pop_min()

        if temp[0][1] not in reached:
            # Add the successor to the node which was reached
            reached[temp[0][1]] = temp[0][0]

            # Break out of the loop if we've reached the destination
            if temp[0][1] == dest:
                break

            # Add edges-to-neighbours to priority queue, with total dist for key
            for succ in graph.neighbours(temp[0][1]):
                residual = graph.capacity((temp[0][1],succ)) \
                    - graph.flow((temp[0][1],succ))
                # Only add if the edge has residual capacity
                if residual > 0:
                    pq.add((temp[0][1], succ), \
                               temp[1]+graph._weights.get((temp[0][1], succ)))

    # If no path
    if dest not in reached:
        return list()

    # Otherwise traverse the path, moving from dest->start
    path = []
    curr = dest
    while curr != start:
        succ = curr
        curr = reached[curr]
        path.append((curr,succ))

    return path

def max_flow(g, s, t):
    '''
    Give a graph g, computes the maximum flow from the source s to 
    the sink t.
    
    Modified code from wiki: Ford-Fulkerson
    
    Efficiency: O(|Edges|*network_flow)
    
    Args:
    graph g: a directed graph with reverse edges
    source s: node from which flow is produced
    sink t: node from which flow is consumed
    
    Returns:
    flow: integer value of flow which can pass through the graph g.

    >>> g = Graph({'s','o','p','q','r','t'})
    >>> g.add_edge('s','o',3,0)
    >>> g.add_edge('s','p',3,0)
    >>> g.add_edge('o','p',2,0)
    >>> g.add_edge('o','q',3,0)
    >>> g.add_edge('p','r',2,0)
    >>> g.add_edge('r','t',3,0)
    >>> g.add_edge('q','r',4,0)
    >>> g.add_edge('q','t',2,0)
    >>> max_flow(g, 's', 't')
    5
    '''
    # Start with a path
    path = find_shortest_path(g, s, t)

    # While we can still find a path in the residual network
    while len(path) != 0:
        # Find capacities of edges in path
        residuals = [g.capacity(e) - g.flow(e) for e in path]        
        # Find bottleneck
        flow = min(residuals)
        # Send bottleneck flowrate through path, update edge/redge flows
        for e in path:
            # add flow to edge
            g.flow(e, g.flow(e)+flow)
            u,v = e[0],e[1]
            re = (v,u)
            # remove flow from reverse edge
            g.flow(re, g.flow(re)-flow)
        # Attempt to find another path
        path = find_shortest_path(g, s, t)

    return g.flow_out(s)

def reconstruct_flows(g,s,t):
    '''
    Reconstructs the flow paths given a graph g and the source s and sink t.
    Note: the graph must have been operated upon by max flow, as the graph class
          initializes with all _flows == 0.

    Efficiency: O(|Edges|)

    Args:
    graph g
    source s: node from which flow is produced
    sink t: node from which flow is consumed
    
    Returns:
    paths: a list of paths outgoing from the source
    
    '''
    # to store multiple paths
    paths = []
    # to store a path
    path = []

    # Dict to store positive flows
    flows = {}
    # List to store flow out of source
    flows[s] = []
    # For all positive flows, add to dict or source outgoing list
    for k in [k for k,v in g._flows.items() if v > 0]:
        if k[0] == s:
            flows[s].append(k[1])
        else:
            flows[k[0]] = k[1]

    # for all outgoing edges from start, add a path to paths
    for first_node in flows[s]:
        path = []
        path.append(s.obj)
        path.append(first_node.obj)
        curr = first_node
        # Trace the flow path to sink
        while curr != t:          
            curr = flows[curr]
            path.append(curr.obj)
        paths.append(path)

    # return paths
    return paths

def gen_flow_network(l, s, t, radius):
    '''
    Given a list of game objects (asteroids), generates a directed graph
    using the graph class.

    Each asteroid is split into two nodes connected by an edge with capacity ==
    asteroid.capacity and weight == 0. One node is designated as incoming
    the other as outgoing.

    Edges are added between nodes based on euclidean distance. If dist<radius,
    the edge will be added.
    
    Note: because the source and sink nodes are also wrapped by the Node class,
          this method returns these new source/sink node object in addition 
          to the graph object.

    Efficiency: O(|Edges^2|)

    Args:
    list l containing asteroid object
    source s from which flow is produced
    sink t from which flow is consumed
    radius: dictates whether an edge is added between nodes based on euclid dist
    
    Returns:
    graph object g
    source node s
    sink node t
    '''
    # Add source and sink
    s = Node(s)
    t = Node(t)
    g = Graph({s,t})

    # To store incoming and outgoing nodes from asteroids
    outgoing = []
    incoming = []

    # For all asteroids, split into in/out node, add to proper list, add edge
    for ast in l:
        n_in = Node(ast)
        g.add_vertex(n_in)
        incoming.append(n_in)
        n_out = Node(ast)
        g.add_vertex(n_out)
        outgoing.append(n_out)
        g.add_edge(n_in, n_out,ast.capacity,0)        

    # Connect out nodes to in nodes if in range
    # Runtime: O(ast^2)
    for n_out in outgoing:
        # Check for connections to sink
        dist = euclidD(t.position,n_out.position) 
        if dist < radius:
            g.add_edge(n_out,t,1,dist)

        # Check ast/ast connections
        for n_in in incoming:            
            dist = euclidD(n_in.position,n_out.position) 
            if dist < radius and dist!=0:
                g.add_edge(n_out,n_in,1,dist)                

    # Check for connections to source
    for n_in in incoming:
        dist = euclidD(n_in.position,s.position)          
        if dist < radius:
            g.add_edge(s,n_in,1,dist)

    return g,s,t
