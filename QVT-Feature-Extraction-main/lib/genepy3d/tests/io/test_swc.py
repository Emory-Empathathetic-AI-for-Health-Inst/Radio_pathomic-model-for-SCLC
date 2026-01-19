# -*- coding: utf-8 -*-
# test io.swc module

from genepy3d.io import swc
import numpy as np
import os

DIRECTORY = os.path.join("tests","data","swc")
FILENAME = "ECL10_GrCellNr7_OML_IML.CNG"
FILE = os.path.join(DIRECTORY,FILENAME+".swc")

class TestSWC:
    """Test SWC class.
    """
    
    @staticmethod
    def check_matching(target, ref, sort=False):
        """Check if two numerical arrays having similar elements.
        """
        if len(target)!=len(ref):
            return False
        else:            
            if sort==True:
                return np.sum(np.abs((np.sort(target) - np.sort(ref)))) == 0
            else:
                return np.sum(np.abs((np.array(target) - np.array(ref)))) == 0
    
    def test_init(self):
        
        # from a directory without recursion
        importer = swc.SWC(DIRECTORY,False)        
        assert len(importer.filelst)==2
        
        # from a directory without recursion
        importer = swc.SWC(DIRECTORY,True)        
        assert len(importer.filelst)==2
        
        # from a directory without recursion
        importer = swc.SWC(FILE)        
        assert importer.neuronnamelst[0]==FILENAME
        
    def test_get_neuron_id(self):
        
        importer = swc.SWC(DIRECTORY,True)        
        df = importer.get_neuron_id()
        flag = [neuronname==FILENAME for neuronname in importer.neuronnamelst]
        ID = np.array(importer.neuronidlst)[flag][0]
        assert df.loc[FILENAME]==ID
        
    # def test_get_neurons(self): # TODO: define simple_tree.swc to test
        
    #     importer = swc.SWC(DIRECTORY,False)
    #     neurons = importer.get_neurons()
    #     for neuid in neurons.keys():
    #         neuron = neurons[neuid]
    #         if neuron.name == "simple_tree":
    #             assert len(neuron.get_preorder_nodes()) == 8
    #             assert self.check_matching(neuron.get_leaves(),[6,7,8],sort=True)
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    