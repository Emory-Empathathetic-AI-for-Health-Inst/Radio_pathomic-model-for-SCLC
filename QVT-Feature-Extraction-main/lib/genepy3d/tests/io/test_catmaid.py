# -*- coding: utf-8 -*-
# test io.catmaid module

from genepy3d.io import catmaid

HOST = "http://www.lob.cnrs.fr/catmaid/"
TOKEN = "47c09faf14145f96f70e7aa75d32a97a008f3aa9"
PID = 18

NEUCSV = "tests/localfiles/catmaid/catmaid_dfneu.csv"
CONCSV = "tests/localfiles/catmaid/catmaid_dfcon.csv"

class TestCatmaid:
    """Test Catmaid class.
    """
    
    # def test_csv_input(self): # TODO: csv file not found
    #     importer = catmaid.Catmaid.from_csv(NEUCSV,CONCSV)
    #     assert len(importer.get_neuron_id()) == 2
    #     assert importer.get_neuron_id("neuron 25800").values[0]==25799
    #     assert importer.get_neuron_name().loc[25799].values[0] == "neuron 25800"
        
    #     neurons = importer.get_neurons()
    #     assert neurons[27559].name == "neuron 27560"
    #     assert neurons[25799].get_coordinates()["z"].values[0] == 91200.0
    #     connectors = neurons[25799].get_connectors()
    #     assert connectors.index[0]==48994
    #     assert connectors['relation'].iloc[0]=='postsynaptic_to'
    #     assert connectors['id'].iloc[0]==48993
        
    # def test_server_input(self):
    #     neuronidlst = [5072, 5063, 5068, 4853, 19111, 16429]
        
    #     importer = catmaid.Catmaid.from_server(HOST,TOKEN,PID,neuronidlst)
    #     assert len(importer.get_neuron_id())==6
        
#        dfmi = importer.get_multi_innervations()
#        assert dfmi.index.get_level_values("post_neuron_id").unique()[0]==5068
#        
#        dfmp = importer.get_multi_postsynaptic()
#        assert dfmp.index.get_level_values("pre_neuron_id").unique()[0]==4853

#class TestCatmaidServer:
#    """Test CatmaidServer class.
#    """
#    
#    def test_get_neurons(self):
#        
#        # unvalid HOST
#        with pytest.raises(ValueError):
#            importer = catmaid.CatmaidServer("xxxx",TOKEN)
#            importer.get_neuron_id(project_id=18)
#            
#        # unvalid TOKEN
#        with pytest.raises(ValueError):
#            importer = catmaid.CatmaidServer(HOST,"xxxx")
#            importer.get_neuron_id(project_id=18)
#            
#        # unvalid project id
#        with pytest.raises(ValueError):
#            importer = catmaid.CatmaidServer(HOST,TOKEN)
#            importer.get_neuron_id(project_id=9999)
#            
#        # valid project id
#        importer = catmaid.CatmaidServer(HOST,TOKEN)           
#        neulst = importer.get_neuron_id(project_id=PID)
#        assert len(neulst)>0
#        
#        # test get neurons
#        neuid = neulst[0]
#        subneulst = neulst[:2]
#        
#        # neuron id is "int", return type is "dataframe"
#        dic = importer.get_neurons(project_id=PID,neuron_id=neuid)
#        assert len(dic)==1
#        
#        # neuron id is "list", return type is "dataframe"
#        dic = importer.get_neurons(project_id=PID,neuron_id=subneulst)
#        assert len(dic)==2
#        
#
#
#class TestCatmaidCSV:
#    """Test CatmaidCSV class.
#    """
#    
#    def test_get_neurons(self):
#        
#        importer = catmaid.CatmaidCSV(NEUCSV,CONCSV)
#        assert len(importer.get_neuron_id()) == 2
#        assert importer.get_neuron_id("neuron 25800").values[0]==25799
#        assert importer.get_neuron_name().loc[25799].values[0] == "neuron 25800"
#        
#        neurons = importer.get_neurons()
#        assert neurons[27559].name == "neuron 27560"
#        assert neurons[25799].get_coordinates()["z"].values[0] == 91200.0
#        connectors = neurons[25799].get_connectors()
#        assert connectors.index[0]==48994
#        assert connectors['relation'].iloc[0]=='postsynaptic_to'
#        assert connectors['id'].iloc[0]==48993
        
        
        
        
        
        
        
        
        
















