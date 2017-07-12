# Jan Faryad
# 19. 6. 2017

from udapi.block.demo.Coreference.Conv.conv import Conv_word_correspondence
from udapi.block.demo.Coreference.Other.auxiliaries import get_interstring

class Pdt_word_correspondence( Conv_word_correspondence):
    def execute( self, filename, udapi_doc):
        """main method, called from outside"""
        # initialization
        self.pdt_w_input = open( filename + ".w", 'r') # surface (word) layer
        self.udapi_doc = udapi_doc        
        self.list_of_corresponding_words = []     
        self.punctuation = ",.?!;'-\""
        #
        
        nodes_to_omit = 0
        for bundle in self.udapi_doc.bundles:
            for root in bundle.trees:         
                for node in root.descendants:
                    if ( nodes_to_omit > 0 ):
                        nodes_to_omit -= 1
                        continue
                    
                    if ( node.multiword_token != None ): # originally one token, divided by UDPipe into multiple nodes. for the matching we use only 
                                                         # the first node, the rest must be omitted
                        nodes_to_omit += len( node.multiword_token.words) - 1                                  
                    
                    word_ID = node.ord
                    form = node.form
                    
                    ( pdt_ID, token ) = self.next_pdt_word() # the next word and its ID in the PDT file                    
                    
                    nodes_to_omit += self.token_division( token, form) # spaces and punctuation in the PDT word cause its division in CoNLL-U into more words
                    # for the matching we use only the first node, the rest must be omitted
                    self.list_of_corresponding_words += [ ( pdt_ID, node ) ]                                    
        
        self.pdt_w_input.close()
        return self.list_of_corresponding_words
    
    def token_division( self, token, form): # -> int
        """
        space or punctuation in the token - UDpipe divides it into more nodes
        """
        if ( token == form ):
            return 0
        lines_to_omit = 0
        for char in token:
            if ( char == ' '): # space divides the token into two parts
                lines_to_omit += 1
            elif ( char in self.punctuation ): # punctuation into three (the punctuation sign itself forms also a node)
                lines_to_omit += 2
        return lines_to_omit    
      
    def next_pdt_word( self): # -> ( pdt_ID (string), pdt token form (string) )
        pdt_line = self.pdt_w_input.readline()
        while ( not "</doc>" in pdt_line ):       
            if ( "<w id" in pdt_line ):
                pdt_ID = get_interstring( pdt_line, '"', '"')
                token_line = self.pdt_w_input.readline()
                token = get_interstring( token_line, '>', '<')
                return ( pdt_ID, token )
            elif ( pdt_line == "" ):
                return ( "", "" )
            pdt_line = self.pdt_w_input.readline()
        return ( "", "" )  
