# Jan Faryad
# 10. 7. 2017
#
# when merging files with coreference into one for better evaluation rewriting of cluster IDs is needed, because they would repeat

from udapi.core.block import Block
import sys

class Conll_merger( Block):
    def __init__( self):
        super( Conll_merger, self).__init__()
        self.id_inc = 0
    def process_document( self, doc):
        max_id = 0
        for bundle in doc.bundles:
            bundle_id = bundle.bundle_id
            for root in bundle.trees:
                for node in root.descendants:
                    if ( "Coref" in node.misc ):
                        cluster_id = int( node.misc['Coref'])
                        if ( cluster_id > max_id ):
                            max_id = cluster_id
                        node.misc['Coref'] = cluster_id + self.id_inc
                    if ( "Drop_coref" in node.misc ):
                        cluster_id = int( node.misc['Drop_coref'])
                        if ( cluster_id > max_id ):
                            max_id = cluster_id
                        node.misc['Drop_coref'] = cluster_id + self.id_inc
        self.id_inc += max_id + 1 # indexing from 0
