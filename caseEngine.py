readme = """
 ===============================================================================
 Auth: Sam Celani
 Prog: caseEngine.py
 Revn: 07-11-2019 Ver 0.4
 Func: Takes in a Russian word, parses it, determines the gender, spits out the
       general case-by-case transformations

 TODO: write in a way to update soft lists
 ===============================================================================
 CHANGE LOG
 -------------------------------------------------------------------------------
 06-01-2019:    init
                wrote parse(), began endings()
 06-04-2019:    wrote endings()
 07-09-2019:    changed m, f, and n to masculine, feminine, and neuter
 07-11-2019:    replaced X with - as negative space character in endings()

 ===============================================================================
"""

# ==============================================================================
#
#   GLOBAL VARIABLES
#
# ------------------------------------------------------------------------------

# Collection of words ending in ь that are masculine
softMasculine = [ 'медведь' ]
# Collection of words ending in ь that are feminine
softFeminine = [ 'лошадь' ]

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
 Args: word::unicode string - Russian word to be processed
 Retn: gender::string - cooresponds to the gender of the input word

 TODO: deprecate, tbh
 ===============================================================================
"""
def parse( word ):
    global softMasculine            # Include collection of ь masculine words
    global softFeminine             # Include collection of ь feminine words
    
    end = word[-1]                  # Grab last letter of word

    if end in [ 'о', 'е' ]:         # -о and -е endings signify...
        gender = 'neuter'           # neuter gender
    elif end in [ 'а', 'я' ]:       # -а and -я endings signify...
        gender = 'feminine'         # feminine gender
    elif end in [ 'ь' ]:            # -ь ending could be either...
        if word in softMasculine:   # masculine...
            gender = 'masculine'
        elif word in softFeminine:  # or feminine...
            gender = 'feminine'
        else:
            gender = None           # or it's possible that I don't know
    else:                           # If the word doesn't fit those criteria...
        gender = 'masculine'        # it's a masculine word
        
    #endings( word, gender )
    return gender                   # Return the gender to main module


"""
 ===============================================================================
 Revn: 06-01-2019
 Func: Print out the different cases of the input word
 Meth: Lookup tables, mostly
 Vars: word::unicode string - word to be parsed
       gender::string - gender of Russian word
 Retn: dictionary::dict(string) - gender-specific dictionary for mapping cases
                                  to endings

 TODO: store output in dictionary, tag as metadata
       allow manual override
 ===============================================================================
"""
def endings( word, gender ):
    global masc                             # Include masculine endings
    global fem                              # Include feminine endings
    global neut                             # Include neuter endings

    if gender in [ 'masculine' ]:           # If the word is masculine
        dictionary = masc                   # Set general dictionary to masc
    elif gender in [ 'feminine' ]:          # If the word is feminine
        dictionary = fem                    # Set general dictionary to fem
    elif gender in [ 'neuter' ]:            # If the word is neuter
        dictionary = neut                   # Set general dictoinary to neuter
        word = word[:-1]
    elif gender is None:                    # Otherwise...
        print( 'Gender unknown, cases also unknown.' )  # No fucking clue
        return
    else:                                   # This should never be possible, but
        print( 'ERROR: unexpected argument in caseEngine.ending' )
        input()                             # always plan for the worst
        exit()                              # Exuent

    for key in dictionary.keys():           # Iterate over the different cases
        strip = dictionary[key].count('-')  # Keep track of the amount of -'s
                                            # ( letters to get rid of )
        print( key, ' : ', end = '' )       # Print just the case
        if not strip is 0:                  # If there are -'s in the ending
            # Print everything but the last few letters
            print( word[:-1*strip], end = '' )
        else:                               # If there are no -'s in the ending
            print( word, end = '' )         # Print the whole word
        # Finally, print the case-by-case ending
        print( dictionary[key][strip:] )
    print()                                 # New line to look cute af

    return dictionary                       # Return appropriate endings dict
    
### ============================================================================
###
### BODY 
###
### ----------------------------------------------------------------------------

"""
try:                                # Wrap in try-catch for CTRL-C
    while True:                     # Loop forever
        parse( input( '>> ' ) )     # Print line start chars, call first func
except KeyboardInterrupt:           # Wait for CTRL-C
    exit()                          # EXEUNT
"""

### ============================================================================

