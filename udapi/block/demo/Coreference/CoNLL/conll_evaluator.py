# Jan Faryad
# 4. 5. 2017
#
# evaluation of automatic recognition of coreference

from udapi.core.block import Block
import sys

class Conll_evaluator( Block):
    def __init__( self):
        super( Conll_evaluator, self).__init__()
        self.gold_doc = None
    def process_document( self, doc):
        if ( self.gold_doc == None ):
            self.gold_doc = doc
            return
        gold_doc = self.gold_doc
        auto_doc = doc
        
        precision_sum = 0
        recall_sum = 0
        
        # lists of Eval_coref_records
        gold_coreferents = self.get_corefs( gold_doc) # what was supposed to be decided
        auto_coreferents = self.get_corefs( auto_doc) # what was decided
        
        relevant_gold_coreferents = [ coref for coref in gold_coreferents if ( coref.relevant ) ]
        relevant_auto_coreferents = [ coref for coref in auto_coreferents if ( coref.relevant ) ]
        
        print("")
        print( "Gold coreferents:   ", len( relevant_gold_coreferents))
        print( "Auto coreferents:   ", len( relevant_auto_coreferents))
        print("")
        
        gold_coref_ids = [ ( coref.coref_id, coref.dropped ) for coref in relevant_gold_coreferents ] # ids and dropped
        auto_coref_ids = [ ( coref.coref_id, coref.dropped ) for coref in relevant_auto_coreferents ]                 
        
        # words that that were supposed to be decided and also were. still clusters may differ
        common_gold_coreferents = [ coref for coref in gold_coreferents if ( ( coref.coref_id, coref.dropped ) in auto_coref_ids ) ]
        common_auto_coreferents = [ coref for coref in auto_coreferents if ( ( coref.coref_id, coref.dropped ) in gold_coref_ids ) ]
        #print( len( common_gold_coreferents), len( common_auto_coreferents))

        if ( len( common_gold_coreferents) == len( common_auto_coreferents) ): # should hold
            common_corefs_number = len( common_gold_coreferents)
            for i in range( common_corefs_number):
                gold_coref = common_gold_coreferents[i] # lists have the same ordering, so these two records refer to the same word
                auto_coref = common_auto_coreferents[i]
                gold_cluster = gold_coref.cluster # cluster assigned to this word in gold and auto data
                auto_cluster = auto_coref.cluster
                
                if (len( gold_cluster.coref_ids) == 1): # drops
                    continue
                
                # "-1" in the next: not counting the actual coreferent
                gold_size = len( gold_cluster.coref_ids) - 1 # relevant coreferents to this word 
                auto_size = len( auto_cluster.coref_ids) - 1 # selected coreferents to this word
                inter_size = len( set( gold_cluster.coref_ids) & set( auto_cluster.coref_ids)) - 1
                prec = inter_size / float( auto_size)
                rec = inter_size / float( gold_size)
                precision_sum += prec
                recall_sum += rec
                #print(prec, rec)
                #if ( auto_size != inter_size or gold_size != inter_size):
                    #print( auto_size, gold_size, inter_size)
            #"""
            #print( "Selected pronouns:\t\t\t", len( auto_coreferents))
            #print( "Relevant pronouns:\t\t\t", len( gold_coreferents))
            #print( "Selected relevant:\t\t\t", len( common_gold_coreferents))
            #print( "Correctly decided:\t\t\t", true_positives)
            #print( "")
            
            if ( len( gold_coreferents) == 0 ):
                recall = None
            else:
                recall = recall_sum / len( relevant_gold_coreferents)
                
            if ( len( auto_coreferents) == 0 ):
                precision = None
            else:
                precision = precision_sum / len( relevant_auto_coreferents)                
            
            print( "Precision:  ", precision) # teraz je vysledok ohrsi kvoli vyskrtnuti koreferentov prodropov
            print( "Recall:     ", recall)
            
            #for i in relevant_gold_coreferents:
            #    print( i.node.form, i.coref_id, i.cluster.cluster_id)
            #"""
            # if an id is missing in one of the id-lists, it will contribute 0 to precision/recall sum, but 1 to the divisor
            #return ( precision_sum / len( auto_coreferents), recall_sum / len( gold_coreferents) )
            
        
    def compare_clusters( self, cluster_1, cluster_2): # -> bool
        """
        if two given clusters have at least two common word ids
        one of the word, which is beaing checked, if its coreference was decided correctly
        this word has one cluster in the gold data, other in auto. now we are checking, if the clusters are identical:
        is there another common word in both clusters?
        """
        common = set( cluster_1.coref_ids) & set( cluster_2.coref_ids)
        return ( len( common) > 1 )
        
    def get_corefs( self, doc): # -> list of coreferenting expression (represented by Eval_coref_record object) in the given conll file        
        clusters = [] # list of Eval_cluster_records
        coreferents = [] # list of Eval_coref_records
        
        for bundle in doc.bundles:
            bundle_id = bundle.bundle_id
            for root in bundle.trees:
                for node in root.descendants:
                    if ( "Coref" in node.misc ):
                        cluster_id = node.misc['Coref']
                        # there should be at most one such cluster
                        appropriate_clusters = [ cluster for cluster in clusters if ( cluster.cluster_id == cluster_id ) ]
                        if ( appropriate_clusters == [] ): # first occurence of this cluster id - create a new instance
                            cluster = Eval_cluster_record( cluster_id)
                            clusters.append( cluster)
                        else: # already existing cluster
                            cluster = appropriate_clusters[0] # there is at most one element
                        coref_id = ( bundle.bundle_id, node.ord )
                        cluster.add_coreferent( coref_id) # adding coreferent id to the list of coreferents of the cluster
                        coref = Eval_coref_record( coref_id, cluster, False)
                        coreferents.append( coref) # output list of all pronouns, for which the coreference was detected  
                        coref.node = node
                        if ( self.has_upostag( node, [ "PRON", "DET" ]) # if we are supposed to detect coreference of this cluster
                             and self.has_feature( node, "PronType", [ "Prs", "Rel", "Dem" ]) ):
                            coref.relevant = True
                            
                    if ( "Drop_coref" in node.misc ):
                        cluster_id = node.misc['Drop_coref']
                        # there should be at most one such cluster
                        appropriate_clusters = [ cluster for cluster in clusters if ( cluster.cluster_id == cluster_id ) ]
                        if ( appropriate_clusters == [] ): # first occurence of this cluster id - create a new instance
                            cluster = Eval_cluster_record( cluster_id)
                            clusters.append( cluster)
                        else: # already existing cluster
                            cluster = appropriate_clusters[0] # there is at most one element
                        coref_id = ( bundle.bundle_id, node.ord )
                        cluster.add_coreferent( coref_id) # adding coreferent id to the list of coreferents of the cluster
                        coref = Eval_coref_record( coref_id, cluster, True)
                        coreferents.append( coref) # output list of all pronouns, for which the coreference was detected  
                        coref.node = node  
                        if ( self.verb_without_subject( node) ): # if we are supposed to detect coreference of this cluster
                            coref.relevant = True
                                                      
        return coreferents
    
    def get_coref_record_by_id( self, coreferents, id):
        for coref in coreferents:
            if ( coref.coref_id == id ):
                return coref
    
    def has_upostag( self, node, list_of_possible_upostags): # -> bool
        """
        controls if the node's upostag is on of the possible ones
        """
        return ( node.upos in list_of_possible_upostags )
    
    def has_deprel( self, node, list_of_possible_deprels): # -> bool
        """
        controls if the node's deprel is on of the possible ones
        """     
        return ( node.deprel in list_of_possible_deprels )    
    
    def has_feature( self, node, feature_name, list_of_possible_values): # -> bool
        """
        controls if the node has the given feature and if one of it's values is possible
        """
        list_of_real_values = node.feats[ feature_name ].split( ',')
        return ( len( set( list_of_real_values) & set( list_of_possible_values) ) > 0 )    
    
    def verb_without_subject( self, node):
        if ( not self.has_upostag( node, [ "VERB" ]) ): # not a verb
            return False
        for child in node.children:
            if ( self.has_deprel( node, [ "nsubj", "csubj" ]) ): # has a subject
                return False
        return True    

class Eval_cluster_record:
    def __init__( self, cluster_id):
        self.cluster_id = cluster_id
        self.coref_ids = []        
    def add_coreferent( self, coref_id):
        self.coref_ids.append( coref_id)
class Eval_coref_record:
    def __init__( self, coref_id, cluster, dropped):        
        self.coref_id = coref_id
        self.cluster = cluster
        self.dropped = dropped
        self.relevant = False
        
