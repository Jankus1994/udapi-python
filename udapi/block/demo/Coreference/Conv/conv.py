# Jan Faryad
# 12. 7. 2017

from udapi.core.block import Block

class Conv_text_converter:
    def __init__( self, input_file_name, output_file_name):
        input_file = open( input_file_name, 'r')
        output_file = open( output_file_name, 'w')
        self.convert_file( input_file, output_file)
        input_file.close()
        output_file.close()
    
    def conver_file( self, input_file, output_file):
        pass

class Conv_main( Block):
    def __init__( self):
        super( Conv_main, self).__init__()
        self.word_correspondence  = Conv_word_correspondence()
        self.coreference_getter   = Conv_coreference_getter()
        self.word_converter       = Conv_word_converter()
        self.coreference_setter   = Conv_coreference_setter()
    
    def process_document( self, document):
        
        path = "../coreference/" # the actual folder is udapi-python/udapi        
        name = document.filename[:-10] # .in.conllu
        full_name = path + name
        
        # building a matching between word ids and udapi nodes
        list_of_corresponding_words = self.word_correspondence.execute( full_name, document)
        
        # extracting information about coreference from
        list_of_coreferents = self.coreference_getter.execute( full_name)        
        
        # conversion of the coreferents' ids to nodes
        list_of_coreferents = self.word_converter.execute( list_of_coreferents, list_of_corresponding_words)
        
        # adding the coreference information into the CoNLL-U file    
        self.coreference_setter.execute( list_of_coreferents) # document is not needed, nodes are in the corespondence list

class Conv_word_correspondence:
    def execute( self):
        return

class Conv_coreference_getter:
    def execute( self):
        return

class Conv_word_converter:
    def execute( self):
        return

class Conv_coreference_setter:
    def execute( self):
        return
