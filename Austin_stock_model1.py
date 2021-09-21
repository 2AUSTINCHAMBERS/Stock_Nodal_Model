#this is a stock and flow model 
import queue #queue is putting first in first out (stack is first in last out)
import random #tool from python that is brought into the program
from queue import Queue #tool from python that is brought into the program
from sys import maxsize #tool from python that is brought into the program
class Node: 
    def __init__(self, name, status = True) -> None:
        self.status = status
        self.name = name
        
       #def is defining a fuction
    #def___init creating a specific class with the 
#function 
#Class is a data structure (list, arrawy, 
    
    def stat(self):
        print(self.name,self.status)

    def report(self):
        if self.status == True:
            print(f"node {self.name} is on")
        else: 
            print(f"node {self.name} is off")

    def off(self):
        self.status = False

    def on(self):
        self.status = True

class Source(Node):
    def __init__(self, name, status, rescources, max_output, efficiency) -> None:
        super().__init__(name, status=status) #pay attention to "status = status" I think it should be "status = True"
        self.rescources = rescources
        self.max_output = max_output
        self.efficiency = efficiency
        self.desig = "source"
        self.requests = []
    def report(self):
        if self.status == True:
            print(f"node {self.name} is on and has {self.rescources} rescources")
        else: 
            print(f"node {self.name} is off and has {self.rescources} rescources")

    def supply(self, ammount): #define function supply with self and the amount (user puts in)
        if self.status == True: 
            if self.rescources*self.efficiency < ammount: #(resouces that we have times the effieciency is less than the amount inputted...)
                output = self.rescources*self.efficiency #(demand)
                self.rescources = 0
                print(f"{self.name} is out of rescources!") # defining that the tank is empty
                return output
            elif ammount > self.max_output:
                self.rescources -= self.max_output/self.efficiency
                return self.max_output #this line of code operates under the assumption that power stations cannot be overloaded
            else:
                self.rescources -= ammount/self.efficiency
                return ammount
        else: 
            print(f"{self.name} is not operational!")

    def replenish(self, ammount):
        self.rescources += ammount
    
    def request(self,source,ammount):
        self.requests.append((source,ammount))

class Transmission(Node):
    def __init__(self, name, status, capacity) -> None:
        super().__init__(name, status=status)
        self.capacity = capacity
        self.desig = "transmission"
        self.requests = []
    def report(self):
        if self.status == True:
            print(f"node {self.name} is on and has {self.capacity} capacity")
        else: 
            print(f"node {self.name} is off and has {self.capacity} capacity")

    def transmit(self,load):
        if self.status == True:
            if load > self.capacity:
                self.off()
                print(f"{self.name} has overloaded!")
                return 0
            else:
                return load
        else:
            print(f"{self.name} is off")
    
    def request(self,source,ammount):
        self.requests.append((source,ammount))

class Sink(Node):
    def __init__(self, name, status, demand, capacity) -> None:
        super().__init__(name, status=status)
        self.demand = demand
        self.capacity = capacity
        self.desig = "sink"

    def report(self):
        if self.status == True:
            print(f"node {self.name} is on and has {self.demand} demand and {self.capacity} capacity")
        else: 
            print(f"node {self.name} is off and has {self.demand} demand and {self.capacity} capacity")

    def recieve(self, load):
        if self.status == True:
            if load > self.capacity:
                self.off()
                print(f"{self.name} has overloaded!")
                return (False, 0)
            elif load != self.demand:
                return (False,self.demand-load)
            else:
                return(True,0)
                
        else:
            print(f"{self.name} is off")

    

def constructor(matrix):
    try: 
        node_index = {}
        tmp_matrix = matrix

        for i in matrix:
            node_index.update({matrix.index(i)+1:i[0]}) 

        x = 0
        for row in tmp_matrix:
            n = 0
            for column in row:
                if column == 1:
                    tmp_matrix[x][n] = node_index.get(n)
                n+=1
            x+=1

        for row in tmp_matrix:
            try:
                while True:
                    row.remove(0) #https://www.techiedelight.com/remove-all-occurrences-item-list-python/
            except:
                pass

        graph = {}
        for i in tmp_matrix:
            graph.update({i[0]:i[1:]})
        return graph
    except:
        pass

class Graph:
    def __init__(self, name, adj_matrix = None, adj_list=None) -> None:
        self.name = name
        self.adj_list = constructor(adj_list)
        self.adj_matrix = adj_matrix
        self.desig = "graph" 

    def report(self):
        print(f"adjacency matrix is:{self.adj_matrix}, adjacency list is: {self.adj_list}")
    
    def isconnected(self, node):
        return self.adj_list.get(node)

# net = Graph("powergrid",None,[["node1",0,0,1,0,1,0],["node2",1,0,1,1,1,1],["node3", 0,0,0,0,1,0],["node4",0,1,0,0,1,1],["node5",0,0,1,1,0,1],["node6",0,1,1,0,0,0]])


# station = Source("powerstation",True,100,20,.4)

# powerline = Transmission("line1", True, 30)

# house = Sink("home", True, 5, 30)


# def identifier(classs):
#     if classs.desig == "graph":
#         print("this is a graph")
#     elif classs.desig == "source":
#         print("this is a source")
#     elif classs.desig == "transmission":
#         print("this is a transmission")
#     else:
#         print("this is a sink")

# identifier(station)
# identifier(powerline)
# identifier(house)

class Model:

    def __init__(self, sources, trans, sinks, graphs) -> None:
        self.sources = sources
        self.trans = trans
        self.sinks = sinks
        self.graphs = graphs
        self.all_nodes = sources+trans+sinks

    def sim(self,timesteps,graph_index,daily_demand):# you might have trouble refrencing graphs within its own class
        t = 0
        for i in range(timesteps):
            #step 1: back propogates demand
            for i in self.all_nodes:
                i.stat()
            for sink in self.sinks: 
                sink.report()
                parents = self.graphs[graph_index].isconnected(sink)
                print(parents)
                weight_tot = 0
                for v in parents:
                    weight_tot += v.capacity #maybe use a dictionary to pair class names with classes
                    print(weight_tot)
                    print(type(v))
                for p in parents:
                    print(type(p))
                    p.request(sink,(p.capacity/weight_tot)*sink.demand)

            for tran in self.trans: 
                parents = self.graphs[graph_index].isconnected(tran)
                print(parents)
                weight_tot = 0
                for v in parents:
                    if v.desig == "source":
                        weight_tot += v.max_output #maybe use a dictionary to pair class names with classes
                        print(weight_tot)
                        print(type(v))
                print(tran.requests)
                load = 0
                for r in tran.requests:
                    load += r[1]
                print(load)

                for p in parents:
                    if p.desig == "source":
                        print(type(p))
                        p.request(sink,(p.max_output/weight_tot)*load)
            #step 2: forward propogates supply
            for s in self.sources:
                
                if s.status == True:

                    tot_load = 0
                    for r in s.requests:
                        tot_load += s.supply(r[1])
                    if tot_load < s.max_output:
                        for request in s.requests:
                            if request[0].desig == "transmission":
                                x = request[0].transmit(request[0].requests[1])
                                if request[0].status == True:
                                    request[0].demand -= x #i took away .request[0] to make this work!!! go back and fix
                                else:
                                    print(f"{request[0].name} has overloaded!")
                            else:
                                print("wrong type:", type(request[0]))
                    else:
                        print(f"{s.name} has overloaded!")
                else:
                    print(f"{s.name} is off")

            t+=1

            for so in self.sinks:
                so.demand += daily_demand

source1 = Source("source1", True, 100000, 100, 1)
source2 = Source("source2", True, 100000, 100, 1)
trans1 = Transmission("trans1", True, 50)
trans2 = Transmission("trans2", True, 50)
sink1 = Sink("sink1",True,10, 200)
sink2 = Sink("sink2", True, 10, 200)
sink3 = Sink("sink3", True, 10, 200)
power_grid = Graph("power_grid", None, [[source1,0,1,1,0,0,0],[source2,0,0,0,1,0,0,0],[trans1,1,0,0,0,1,1,0],[trans2,1,1,0,0,0,0,1],[sink1,0,0,1,0,0,0,0],[sink2,0,0,1,0,0,0,0],[sink3,0,0,0,1,0,0,0]])


source_list = [source1,source2]
trans_list = [trans1,trans2]
sink_list = [sink1,sink2,sink3]
grid_graph = [power_grid]
hello_world = Model(source_list, trans_list, sink_list,grid_graph)

hello_world.sim(10,0,10)
