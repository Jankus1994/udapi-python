# Jan Faryad
# 23. 3. 2017
#
# pdt module to conversion of the coreferennce information from chains to clusters

class PDT_clusterization:    
    def __init__( self, list_of_corefs):
        self.list_of_corefs = list_of_corefs
        self.list_of_cluster_records = []
        self.cluster_id = -1 # id of coreference clusters        
    
    def convert_chains_to_clusters( self):
        """
        called from outside
        """
        list_of_cluster_records = []
        
        for record in self.list_of_corefs:
            cluster_ID = self.find_coref_cluster( record.coref_node, record.coref_dropped)
            if ( cluster_ID == None ):
                # only for heads of the chains - their referents must be process seperately, as their don't have their own records
                cluster_ID = self.new_cluster()
                coref_cluster_record = Cluster_record( record.coref_node, cluster_ID, record.coref_dropped )
                self.list_of_cluster_records.append( coref_cluster_record)
            own_cluster_record = Cluster_record( record.own_node, cluster_ID, record.own_dropped )
            self.list_of_cluster_records.append( own_cluster_record)
        
        for cluster_record in self.list_of_cluster_records:
            if ( cluster_record.dropped ):
                cluster_record.node.misc["Drop_coref"] = cluster_record.cluster_ID
            else:
                cluster_record.node.misc["Coref"] = cluster_record.cluster_ID
        #return list_of_cluster_records
            
    def find_coref_cluster( self, node, dropped): # -> int (cluster number)
        """
        if this cluster was already used, returns its number. otherwise None - then will the caller set up a new cluster
        """
        for record in self.list_of_cluster_records:
            if ( record.node == node and record.dropped == dropped):
                return record.cluster_ID
        return None
    
    def new_cluster( self):
        self.cluster_id += 1
        return self.cluster_id
    
    #def get_cluster_id( self):
    #    return self.cluster_id
    
class Cluster_record:
    def __init__( self, node, cluster_ID, dropped):
        self.node = node
        self.cluster_ID = cluster_ID
        self.dropped = dropped
