# -*- coding: utf-8 -*-
# test obj.tree module

import numpy as np
from anytree import Node, PreOrderIter

from genepy3d.obj import trees

class TestTree:
    """test Tree class.
    """
    
    @staticmethod
    def get_simple_tree():
        """Create simple testing tree.
        
        0--1--3--5
            --4--6--7
         --2--8

        """
        nodearr = {}
        nodearr[0] = Node(0)
        nodearr[1] = Node(1,parent=nodearr[0])
        nodearr[2] = Node(2,parent=nodearr[0])
        nodearr[3] = Node(3,parent=nodearr[1])
        nodearr[4] = Node(4,parent=nodearr[1])
        nodearr[5] = Node(5,parent=nodearr[3])
        nodearr[6] = Node(6,parent=nodearr[4])
        nodearr[7] = Node(7,parent=nodearr[6])
        nodearr[8] = Node(8,parent=nodearr[2])
        
        for i in range(len(nodearr)):
            nodearr[i].x = np.random.rand()
            nodearr[i].y = np.random.rand()
            nodearr[i].z = np.random.rand()
            nodearr[i].r = 0
            nodearr[i].structure_id = 0
            nodearr[i].connector_relation = "None"
            nodearr[i].connector_id = -1
            
        nodearr[2].connector_relation = "presynaptic_to"
        nodearr[2].connector_id = 1
        
#        print("Tree structure:")
#        print(RenderTree(nodearr[0], style=DoubleStyle).by_attr())
        
        return nodearr
    
    @staticmethod
    def get_simple_tree2():
        """
        0--1--2--3--4--6
                  --5--7
        """        
        
        nodearr = {}
        
        nodearr[0] = Node(0,x=0.,y=0.,z=0.)
        nodearr[1] = Node(1,parent=nodearr[0],x=1.,y=1.,z=0.)
        nodearr[2] = Node(2,parent=nodearr[1],x=2.,y=2.,z=0.)
        nodearr[3] = Node(3,parent=nodearr[2],x=3.,y=3.,z=0.)
        nodearr[4] = Node(4,parent=nodearr[3],x=3.,y=4.,z=0.)
        nodearr[5] = Node(5,parent=nodearr[3],x=4.,y=3.,z=0.)
        nodearr[6] = Node(6,parent=nodearr[4],x=3.,y=5.,z=0.)
        nodearr[7] = Node(7,parent=nodearr[5],x=5.,y=2.,z=0.)
        
        for i in range(len(nodearr)):
            nodearr[i].r = 0
            nodearr[i].structure_id = 0
            nodearr[i].connector_relation = "None"
            nodearr[i].connector_id = -1
            
        return nodearr
    
    @staticmethod
    def check_matching(target, ref, sort=False):
        if len(target)!=len(ref):
            return False
        else:            
            if sort==True:
                return np.sum(np.abs((np.sort(target) - np.sort(ref)))) == 0
            else:
                return np.sum(np.abs((np.array(target) - np.array(ref)))) == 0
    
    # def test_compute_orientation(self):
    #     nodes = self.get_simple_tree2()
    #     t = trees.Tree(nodes)
    #     assert len(t.get_leaves())==2
    #     df = t.compute_angles()
    #     sdf = df[df["seg_key"]==7]
    #     assert (sdf.loc[7]["thetay"] + sdf.loc[0]["thetay"])*180/np.pi == 180
    
    def test_prune_leaves(self):
        nodes = self.get_simple_tree2()
        t = trees.Tree(nodes)
        t_pruned = t.prune_leaves(length=2.01)
        assert 6 not in t_pruned.get_preorder_nodes()
        
    def test_copy(self):
        nodes = self.get_simple_tree2()
        t = trees.Tree(nodes)
        t_copied = t.copy()
        assert self.check_matching(t.get_preorder_nodes(),t_copied.get_preorder_nodes())
    
    def test_anytree_input(self):
        nodes = self.get_simple_tree()
        nodelst = [node.name for node in PreOrderIter(nodes[0])]
        nodecoors = np.array([[node.x,node.y,node.z] for node in PreOrderIter(nodes[0])])
        
        t = trees.Tree(nodes)
        
        # init
        assert t.id == 0
        assert t.name == "GeNePy3D"
        assert len(t.nodes) == len(nodes)
        
        # root
        assert t.get_root()[0]==0
        
        # nodes in pre-order iteration
        assert self.check_matching(t.get_preorder_nodes(),nodelst)
        
        # leaves
        assert self.check_matching(t.get_leaves(),[5,7,8],sort=True)
        
        # internodes
        assert self.check_matching(t.get_branchingnodes(),[0,1],sort=True)
        
        # spine
        assert self.check_matching(t.compute_spine(),[0,1,4,6,7])
        
        # strahler order
        strahler = t.compute_strahler_order()
        assert self.check_matching(strahler.index.values,nodelst)
        assert self.check_matching(strahler.values,[2,2,1,1,1,1,1,1,1])
        
        # connectors
        connectors = t.get_connectors()
        assert connectors.index.values[0]==2
        assert connectors['relation'].values[0]=="presynaptic_to"
        
        # coordinates
        coors = t.get_coordinates()
        assert self.check_matching(coors['x'].values,nodecoors[:,0])
        assert self.check_matching(coors['y'].values,nodecoors[:,1])
        assert self.check_matching(coors['z'].values,nodecoors[:,2])
        
        # decompose segments
        assert len(t.decompose_segments())==4
        
        # path
        assert self.check_matching(t.path(0,6),[6,4,1,0])
        
        # extract subtrees
        
        # upper tree
        subt = t.extract_subtrees(1,to_children=False)
        assert subt.get_root()[0]==0
        assert self.check_matching(subt.get_leaves(),[8])
        assert self.check_matching(t.get_leaves(),[5,7,8])
        
        # lower tree
        subt = t.extract_subtrees(1,to_children=True)
        assert subt.get_root()[0]==1
        assert self.check_matching(subt.get_leaves(),[5,7])
        assert self.check_matching(t.get_leaves(),[5,7,8])
        
        # lower trees separated by nb. of children
        subtlst = t.extract_subtrees(1,to_children=True,separate_children=True)
        
        # first lower tree
        subt = subtlst[0]
        assert subt.get_root()[0]==1
        assert self.check_matching(subt.get_leaves(),[5])
        assert self.check_matching(t.get_leaves(),[5,7,8])
        
        # second lower tree
        subt = subtlst[1]
        assert subt.get_root()[0]==1
        assert self.check_matching(subt.get_leaves(),[7])
        
        # decompose spines
        spines = t.decompose_spines()
        assert len(spines)==3
        
        # decompose leaves
        leafsegs = t.decompose_leaves()
        assert len(leafsegs)==3
        
        # summary
        resume = t.summary()
        assert resume['id']==t.id
        assert resume['name']==t.name
        assert resume['root']==t.get_root()
        
    def test_angles(self):
        nodes = self.get_simple_tree2()
        t = trees.Tree(nodes)
        angles = t.compute_angles()
        assert (angles.loc['3_6',4]['theta'] * 180 / np.pi) == 180

    # def test_swc_input(self): # TODO define simple_tree.swc
    #     filepath = "tests/localfiles/swc/simple_tree.swc"
    #     t = trees.Tree.from_swc(filepath)
    #     assert len(t.get_preorder_nodes())==8
    #     assert t.get_root()[0]==1
    #     assert self.check_matching(t.get_leaves(),[6,7,8],sort=True)
    #     assert self.check_matching(t.get_branchingnodes(),[1,2],sort=True)
        
    # def test_catmaid_server_input(self):
    #     catmaid_host = "http://www.lob.cnrs.fr/catmaid/"
    #     token = "47c09faf14145f96f70e7aa75d32a97a008f3aa9"
    #     project_id = 18
    #     neuron_id = 27559
    #     t = trees.Tree.from_catmaid_server(catmaid_host,token,project_id,neuron_id)
    #     assert t.name == "neuron 27560"
    #     assert t.get_coordinates(68094)["x"].values[0]==1158200.
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
