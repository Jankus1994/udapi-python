# Jan Faryad
# 2. 7. 2017
#
# conversion of the onto IDs to udapi nodes

from udapi.block.demo.Coreference.Conv.conv import Conv_word_converter

class Onto_word_converter( Conv_word_converter):
    def execute( self, list_of_onto_clusters, list_of_corresponding_words): # -> list of onto clusters        
        """
        list of clusters, cluster have list of coreferents of type Onto_coreferent
        correspondence ... pairs ( onto id, node )
        """
        self.list_of_corresponding_words = list_of_corresponding_words
        for onto_cluster in list_of_onto_clusters:
            new_coreferents = [] # will be filled with Nodes instead of onto ids
            for coreferent in onto_cluster.coreferents:
                new_coreferent = self.convert_coref( coreferent) # udapi node
                new_coreferents.append( new_coreferent)
            onto_cluster.coreferents = new_coreferents
        return list_of_onto_clusters
    
    def convert_coref( self, coreferent): # -> udapi node
        try:
            sentence_split = coreferent.position_string.split( '.') # a.b-c, a - sentence number, b/c - first/last word number
            sent_number = int( sentence_split[0])
            word_split = sentence_split[1].split( '-')
            first_word_number = int( word_split[0])
            last_word_number = int( word_split[1])
        except:
            return None            
        
        subtree = [] # the whole expression (interval of Nodes)
        for pair in self.list_of_corresponding_words:
            ( onto_sent_id, onto_word_id ) = pair[0]
            if ( onto_sent_id == sent_number and onto_word_id >= first_word_number and onto_word_id <= last_word_number ):
                subtree.append( pair[1]) # corresponding conll node
        
        #subtree_form = ""
        #for i in subtree:
        #    subtree_form += " " + i.form
        
        # we have to chose the head of the interval - this will be the only corefering word
        subtree_head = None
        for node in subtree: # finding the head of the interval
            head = True
            for other_node in subtree:
                if ( node.is_descendant_of( other_node) ): # head musn't be descendant of another node from the interval
                    head = False
                    break
            if ( head ):
                subtree_head = node
                break

        return subtree_head            
                
                
                
                
                
                
                
                
                
                
                
                
                
