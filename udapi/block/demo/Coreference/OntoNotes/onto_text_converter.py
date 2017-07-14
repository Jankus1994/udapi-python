# Jan Faryad
#
# conversion of sentences fron onf file to plain text

import sys

from udapi.block.demo.Coreference.Conv.conv import Conv_text_converter

class Onto_text_converter( Conv_text_converter):
    def convert_file( self, input_file, output_file):
        converted = ""
        active = False # if we read the plain sentence
        for line in input_file:            
            if ( line == '\n'):
                active = False
            if ( active ):
                if ( line != "---------------\n"):                
                    converted += self.remove_punct_spaces( line[3:-1])
            elif ( "Coreference chains" in line ): # end of the section
                converted += "\n\n"
            elif ( "Plain sentence" in line ):
                active = True
        output_file.write( converted)

    def remove_punct_spaces( self, string): # -> string
        """ removing spaces before punctuation """
        if ( len( string) < 2 ):
            return string
        new_string = ""
        char_a = string[0]
        for char_b in string[1:]:
            if not ( char_a == ' ' and char_b in ".,?!:;'-\"" ):
                new_string += char_a
            char_a = char_b
        new_string += string[-1]
        return new_string
                

if ( len( sys.argv) == 3 ):
    c = Onto_text_converter( sys.argv[1], sys.argv[2])
