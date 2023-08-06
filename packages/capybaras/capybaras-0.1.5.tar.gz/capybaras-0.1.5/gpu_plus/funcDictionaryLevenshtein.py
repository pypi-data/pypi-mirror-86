import networkx as nx

#from imnet import process_strings as p # info: commented out at 22rd of November 2020
#from plotData import InnerDataLevenshtein # info: commented out at 22rd of November 2020
from . import funcDictionary as dic
from . import opencl_matrix as om
#from . import opencl_matrixCopy2 as om
# --------------------------------- PAY ATTENTION: opencl_matrixCopy2 vd opencl_matrix

def make_graph(nets_i, min_ld,max_ld, gpu_l):
    """
    info: generate a network from the strings 
        in "nets_i" (usually an element of nets);
        for implementation on the gpu the opencl-script is called
    input: nets_i: list of DNA strings with same length (usually
            an element of net) # check that
           min_ld: minimum Levenshtein 
               distance to make an edge, usually -1
               (0 would exclude 0 distance, because BETWEEN)
           max_ld: maximum Levenshtein 
               distance to make an edge
               
               BETWEEN max_ld and min_ld 
           gpu_l: sidelength of the tiles in which the 
               matrix is divided for the gpu calculation.
               (the total matrix is too big to save it on the 
               GPU as a hole) (technical value)
    output: G: graph, that has been generated; every node denotes one 
               DNA string; an edge is drawn between two nodes, if the 
               Levenshtein distance is between min_ld, 
               max_ld (usually min_ld is 0)# right? 
    """
    #old: G = p.generate_graph(nets_i, min_ld, max_ld)

    # perh.: output of om list or np.array?

    # info: call of the opencl function for the GPU calculation
    #     return the entries of a sparse matrix:
    #     idxs_all: list of the row indices of nonzero values
    #     cols_all: list of the column indices of nonzero values
    #     vals_all: list the nonzero the values, is now made as "_", because it is not needed
    
    idxs_all, cols_all, _ = om.levenshtein_cl_total(nets_i, nets_i, gpu_l=gpu_l, min_ld=min_ld, max_ld=max_ld)
    
    # info: make a graph and 
    G = nx.Graph()
    
    # info: adding nodes, in order to first create all the nodes for the network
    """
    for i in range(len(nets_i)):
        if i%100000 == 0:
            print("\n paul in funcDictionaryLevenshtein.py: ", i, " / ", len(idxs_all))
        G.add_node(i) 
    """
    # info: adding the edges
    for i in range(len(idxs_all)):
        if i%100000 == 0:
            print("\n paul in funcDictionaryLevenshtein.py: ", i, " / ", len(idxs_all))
        G.add_edge(idxs_all[i], cols_all[i])
    
    # info: if the graph is empty, then add at least one node,
    #     which is called the "ZeroNode"
    if len(G.nodes()) == 0:
        G = nx.Graph()
        G.add_node("ZeroNode")
    
    return G

def sim(step, plotData, isExtractNum, lmax, gpu_l):

    """
    info: kind of, perform the total simulation
    input: step (0, if pre selection; 1, if post selection),  
        plotData: PlotData object, that contains the important data and parameters;
            for more detail see documentation in plotData.py
        isExtractNum: Bool, that says, if only a limited number of 
            letters should be extracted;
        lmax: maximum allowed number of nodes in each net
        gpu_l: sidelength of the tiles in which the 
               matrix is divided for the gpu calculation.
               (the total matrix is too big to save it on the 
               GPU as a hole) (technical value)
    output: plotData: PloData object with updated members
    """
 
    # todo: ... (see lenNet.py)
    
    # info: go through all samples for analysis (usually that 
    #     is chosen to be 1, because we don't do multiple samples)
    for sample in range(plotData.samples):
        # info: initialize the analyzed quantities
        innerData = InnerDataLevenshtein()
        
        # todo: for lsHist: # we still have to achieve, that the intervals have the 
        #     same limits for all samples
        a, a4, seq, filename, ls = dic.loadSequence(step, plotData, isExtractNum=isExtractNum)
        
        # info: make nets
        nets = dic.make_nets(ls, seq, lmax)

        # info: iterate through all i values, that are in the nets-array
        for i in list(nets):  
            print("\n net i: ", i, " / ", len(nets))

            # info: check, if the cluster has a certain minimum length
            if len(nets[i]) > plotData.clusterMinLen:
                
                # info: generate graph using the gpu
                G = make_graph(nets[i], min_ld=plotData.min_ldVal, 
                        max_ld=plotData.max_ldVal, gpu_l=gpu_l)
                print("\n len(G.nodes()): ", len(list(G.nodes())))
                
                # info: GSub: biggest subgraph
                GSub = dic.largest_sub_graph(G)
                	
                # append the values to the corresponding list:	
                innerData = dic.append_values(innerData, GSub, G)
            else: 
                innerData = dic.append_zero(innerData)
        
        plotData = dic.make_all_data(plotData, innerData, sample)
        plotData.xArgs = list(nets.keys())
    plotData = dic.mean_and_error_of(plotData)
    return plotData
