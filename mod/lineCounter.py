"""
 ================================================================================
 Auth: Sam Celani
 Prog: lineCounter.py
 Revn: 08-08-2019 Ver 1.0
 Func: Parse all Python files in a directory (and subdirectories), count all
       comments, whitespace, and instruction lines.

 TODO: CLEAN UP, FOR THE LOVE OF GOD
 ================================================================================
 CHANGE LOG
 --------------------------------------------------------------------------------
 08-05-2019:    init
 08-06-2019:    started adding multiline comment support
                imported re to remove whitespace on indented comments
                imported codecs for opening unicode files
                changed open() to codecs.open()
 08-07-2019:    finished adding multiline comment support
                made total whitespace count start at 1 instead of 0
                changed open() to open a variable argument instead of hardcoding
                    argument in open()
                added filename to output with Lines::
 08-08-2019:    removed command line argument
                imported os to get files in directory
                iterates over all files in directory
                encapsulated functionality in size() function
                copy-pasted body to run for TLPr, and then iterate over files
                    in mod/
                hardcoded in tlpr.py filename, and mod/ directory
                removed dictionary that holds filenames and counts in favor of
                    printing file stats as they are found, instead of after
*08-22-2019:

 ================================================================================
"""

import codecs   # Used to open unicode files
import os       # Used to get files in directory
import re       # Used to remove leading whitespace
import sys      # Used for getting system arguments


def size():

    # Pos 0 -> comments
    # Pos 1 -> whitespace
    # Pos 2 -> instructions
    total = [ 0, 0, 0 ]     # Keep track of the grand total line count

    # Filename is hardcoded -> bad and gay
    with codecs.open( 'tlpr.py', 'r' , encoding = 'utf-8' ) as file:
        
        In = False      # Keep track of when you're in a multiline comment
        Out = True      # Keep track of when you're out of a multiline comment
        
        # Pos 0 -> whitespace
        # Pos 1 -> comments
        # Pos 2 -> instructions
        # Total stats have been off by 1 for whitespace,
        # so update white->0 to white->1
        count = [ 1, 0, 0 ]
        
        for line in file:                   # Iterate over all lines in the file
            line = re.sub( ' ', '', line )  # Substitute spaces for nothing

            # First, check to see if it's a comment
            if line[0] == '#':              # If line starts with a comment...
                count[1] += 1               # and update total comments
                continue                    # Skip to next line

            # Second, check for multiline comment
            for letter in line:             # Iterate over all letters in a line
                # If not currently in a multiline comment AND find a double quote
                # ( which I as the author have reserved for multiline comments )
                if letter == '"' and not In:
                    # Set In state variable to true if next two characters are "
                    In = ( line[line.index( letter ) + 1] == '"' and
                           line[line.index( letter ) + 2] == '"' )
                    Out = not In            # Set out to the opposite
                    break                   # Leave letter-parsing loop
                elif letter == '"' and In:
                    # Set Out state variable to true if next two characters are "
                    Out = ( line[line.index( letter ) + 1] == '"' and
                            line[line.index( letter ) + 2] == '"' )
                    break                   # Leave letter-parsing loop

            # This block is to catch the ending """
            if Out and In:              # If previously in MLC, and breaking out
                In = not Out            # Set In to false -> leaving MLC
                count[1] += 1           # But increment comment count
            # This is to increment comment count if found to be In MLC
            elif In:
                count[1] += 1           # Update total comments
            # Third, check for newline
            elif line == '\n' or line == ( chr(13) + chr(10) ):
                count[0] += 1           # and update total whitespace
            # If it makes it here, it must be an instruction
            else:                       # Anything else is an instruction
                count[2] += 1           # Update total instructions

        # Update total count with comprehension, instead of expanded loop
        total = [ total[x] + count[x] for x in range( len( total ) ) ]

        # Print stats
        # Filename is hardcoded -> bad and gay
        print( 'Lines:: tlpr.py' )
        print( '  Whitespace:', count[0] )
        print( '  Comments:', count[1] )
        print( '  Instructions:', count[2] )
        print( '  TOTAL:', count[0] + count[1] + count[2] )
        print()

    # Directory is hardcoded -> bad and gay
    # Iterate over all files in /mod subdirectory
    for fileName in os.listdir( os.curdir + '/mod' ):
        if fileName[-3:] == '.py':      # If the file is a Python file
            # Open unicode file in read mode, named file
            # Directory is hardcoded -> bad and gay
            with codecs.open( 'mod/' + fileName, 'r', encoding = 'utf-8' ) as file:
                
                In = False      # Keep track of when in a multiline comment
                Out = True      # Keep track of when out of a multiline comment
                
                # Pos 0 -> whitespace
                # Pos 1 -> comments
                # Pos 2 -> instructions
                # Total stats have been off by 1 for whitespace,
                # so update white->0 to white->1
                count = [ 1, 0, 0 ]
                
                for line in file:           # Iterate over all lines in the file
                    # Substitute spaces for nothing
                    line = re.sub( ' ', '', line )

                    # First, check to see if it's a comment
                    if line[0] == '#':      # If line starts with a comment...
                        count[1] += 1       # and update total comments
                        continue            # Skip to next line

                    # Second, check for multiline comment
                    for letter in line:     # Iterate over all letters in a line
                        # If not in a multiline comment AND find a double quote
                        # ( which is reserved for multiline comments )
                        if letter == '"' and not In:
                            # Set In to true if next two characters are "
                            In = ( line[line.index( letter ) + 1] == '"' and
                                   line[line.index( letter ) + 2] == '"' )
                            Out = not In    # Set out to the opposite
                            break           # Leave letter-parsing loop
                        elif letter == '"' and In:
                            # Set Out to true if next two characters are "
                            Out = ( line[line.index( letter ) + 1] == '"' and
                                    line[line.index( letter ) + 2] == '"' )
                            break           # Leave letter-parsing loop

                    # This block is to catch the ending """
                    if Out and In:      # If previously in MLC, and breaking out
                        In = not Out    # Set In to false now
                        count[1] += 1   # But increment comment count
                    # This is to increment comment count if found to be In MLC
                    elif In:
                        count[1] += 1   # Update total comments
                    # Third, check for newline
                    elif line == '\n' or line == ( chr(13) + chr(10) ):
                        count[0] += 1   # and update total whitespace
                    # If it makes it here, it must be an instruction
                    else:               # Anything else is an instruction
                        count[2] += 1   # Update total instructions

                # Update total count with comprehension, instead of expanded loop
                total = [ total[x] + count[x] for x in range( len( total ) ) ]

                # Print file specific stats
                print( 'Lines::', fileName )
                print( '  Whitespace:', count[0] )
                print( '  Comments:', count[1] )
                print( '  Instructions:', count[2] )
                print( '  TOTAL:', count[0] + count[1] + count[2] )
                print()

    # Print total stats
    print()
    print( 'TOTAL Lines::' )
    print( '  TOTAL Whitespace:', total[0] )
    print( '  TOTAL Comments:', total[1] )
    print( '  TOTAL Instructions:', total[2] )
    print( '  GRAND TOTAL:', total[0] + total[1] + total[2] )
    print( '\n' )
