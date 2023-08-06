import numpy as np
from . import funcDictionary as dic
from . import funcDictionaryLevenshtein as dicLeven
from . import plotData as pD

def test():
    plotData = pD.PlotDataLevenshtein()
    plotData.clusterMinLen = 1
    
    # info: plotData.N: the total number of sequences, which is loaded
    plotData.N = 1*10**3
    
    # info: set min_ldVal and max_ldVal
    plotData.min_ldVal = -1
    plotData.maxVal = 3
    plotData.max_ldVal = plotData.maxVal
    
    step = 0
    
    #maxVals = [1, 2, 3, 4, 5] - I think, that can be put away
    
    big_samples = 1
    name = "mouse"
    gpu_l = 1000
    
    a, a4, seq, filename, ls = dic.loadSequence(step, plotData, isExtractNum=False, animal=name)
    #seq = ["ABCD", "ABCDFA", "FFF"]    
    
    g = dicLeven.make_graph(seq, min_ld=plotData.min_ldVal,
                    max_ld=plotData.max_ldVal, gpu_l=gpu_l)
    
    print("\n g.edges(): ", list(g.edges()))
