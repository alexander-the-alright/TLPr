readme = """
 ===============================================================================
 Auth: Sam Celani
 Prog: caseEngine.py
 Revn: 06-01-2019 Ver 0.1
 Func: Takes in a Russian word, parses it, determines the gender, spits out the
       general case-by-case transformations

 TODO: create
 ===============================================================================
 CHANGE LOG
 -------------------------------------------------------------------------------
 12-25-2018:    expanded on import files & modules
                added comment fields for imports, variables, functions, body
 06-01-2019:    init
                wrote parse, began endings
 06-04-2019:    wrote endings

 ===============================================================================
"""

# ==============================================================================
#
#   GLOBAL VARIABLES
#
# ------------------------------------------------------------------------------


softMasculine = []      # Collection of words ending in ь that are masculine
softFeminine = []       # Collection of words ending in ь that are feminine

# Dictionary of cases and their respective endings for masculine nouns
masc = { 'a' : '',
         'd' : 'у',
         'g' : 'а',
         'i' : 'ом',
         'n' : '',
         'p' : 'е' }

# Dictionary of cases and their respective endings for feminine nouns
# Capital X's signify letters to be removed from the root
fem  = { 'a' : 'Xу',
         'd' : 'Xе',
         'g' : 'Xи',
         'i' : 'Xой',
         'n' : '',
         'p' : 'Xе' }

# Dictionary of cases and their respective endings for neuter nouns
# Capital X's signify letters to be removed from the root
neut = { 'a' : '',
         'd' : 'Xу',
         'g' : 'Xа',
         'i' : 'Xом',
         'n' : '',
         'p' : 'Xе' }

# ==============================================================================
#
#   FUNCTIONS
#
# -----------------------------------------------------------------------------

"""
 ===============================================================================
 Revn: 06-01-2019
 Func: Determine gender of input word
 Meth: Look at last letter, lookup table if last letter is ь
 Vars: word::unicode string - Russian word to be processed
 Retn: none, doesn't even print; pretty much just compartmentalizes the process

 TODO: deprecate, tbh
 ===============================================================================
"""
def parse( word ):
    global softMasculine            # Include collection of ь masculine words
    global softFeminine             # Include collection of ь feminine words
    
    end = word[-1]                  # Grab last letter of word

    if end in [ 'о', 'е' ]:         # -о and -е endings signify...
        gender = 'neut'             # neuter gender
    elif end in [ 'а', 'я' ]:       # -а and -я endings signify...
        gender = 'fem'              # feminine gender
    elif end in [ 'ь' ]:            # -ь ending could be either...
        if end in softMasculine:    # masculine...
            gender = 'masc'
        elif end in softFeminine:   # or feminine...
            gender = 'fem'
        else:
            gender = 'unknown'      # or it's possible that I don't know
    else:                           # If the words doesn't fit those criteria...
        gender = 'masc'             # it's a masculine word
        
    # Send the word and the gender to the function that actually does work
    endings( word, gender )


"""
 ===============================================================================
 Revn: 06-01-2019
 Func: Print out the different cases of the input word
 Meth: Lookup tables, mostly
 Vars: word::unicode string - word to be parsed
       gender::string - gender of Russian word
 Retn: none, just prints

 TODO: store output in dictionary, tag as metadata
       allow manual override
 ===============================================================================
"""
def endings( word, gender ):
    global masc                             # Include masculine endings
    global fem                              # Include feminine endings
    global neut                             # Include neuter endings

    if gender in [ 'masc' ]:                # If the word is masculine
        dictionary = masc                   # Set general dictionary to masc
    elif gender in [ 'fem' ]:               # If the word is feminine
        dictionary = fem                    # Set general dictionary to fem
    elif gender in [ 'neut' ]:              # If the word is neuter
        dictionary = neut                   # Set general dictoinary to neuter
    elif gender in [ 'unknown' ]:           # Otherwise...
        print( 'Gender unknown, cases also unknown.' )  # No fucking clue
    else:                                   # This should never be possible, but
        print( 'ERROR' )                    # always plan for the worst
        exit()                              # Exuent

    for key in dictionary.keys():           # Iterate over the different cases
        strip = dictionary[key].count('X')  # Keep track of the amount of X's
                                            # ( letters to get rid of )
    
        print( key, ' : ', end = '' )       # Print just the case
        if not strip is 0:                  # If there are X's in the ending
            # Print everything but the last few letters
            print( word[:-1*strip], end = '' )
        else:                               # If there are no X's in the ending
            print( word, end = '' )         # Print the whole word
        # Finally, print the case-by-case ending
        print( dictionary[key][strip:] )
    print()                                 # New line to look cute af
    
### ============================================================================
###
### BODY 
###
### ----------------------------------------------------------------------------

try:                                # Wrap in try-catch for CTRL-C
    while True:                     # Loop forever
        parse( input( '>> ' ) )     # Print line start chars, call first func
except KeyboardInterrupt:           # Wait for CTRL-C
    exit()                          # EXEUNT

### ============================================================================

