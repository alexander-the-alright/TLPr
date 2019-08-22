# -*- coding: utf-8 -*-

readme = u"""
 ===============================================================================
 Auth: Sam Celani
 Prog: tlpr.py
 Revn: 08-08-2019  Ver 4.0
 Func: 

 TODO: Standardize printed whitespace in edit submenu
       Fix README for GitHub
       COMMENTS
       Write delete, fadd, fedit, fdel
       Add plural declension
           Replace Attributes with Plural Declension, put contents of Attribute
               into Topic
       Digital notecard thing
       Add commands to show() i.e. SHOW declension soup/суп
       Merge with original TLP, add switch between languages
       Add verb support
 ===============================================================================
 CHANGE LOG
 -------------------------------------------------------------------------------
 04-14-2019:    got unicode stored in structures
                got script to read from and write to file
                added add() function to add to dict
 04-15-2019:    added comment headers, basic polling-lookup dynamics
                changed x to data
 04-17-2019:    commented a few functions
                theorized the new data storage format
 04-19-2019:    added metadata in the add() function
                set first meta value to gender
                changed init() to work with new data format
                removed writeback for testing of metadata
*04-20-2019:    added HELP 'function' for user
                defined maxLen variable for formatted print
                rewrote show() function to take in topic and search for it
                added formatted print logic to show()
                wrote first draft of edit()
                removed input to fileUpdate(), added Deprecate to TODO
                added note to install delimiter in add() and edit()
                added note to allow multiple translations in add
*04-21-2019:    made data containment format to be a list of lists, no delim
 05-17-2019:    changed data containment format, hopefully last iteration
                theorized the toString() method for writing data to file
                prints opening comment header in README.md when script is run
                let user clear screen, found shell/cmd bug, removed cls code
 06-26-2019:    futzed with wording in DATA CONTAINMENT FORMAT
                added flag to update README and exit
                finished and commented init()
                added caseNames global variable to make data file smaller
 06-27-2019:    wrote fileUpdate()
                tested init() and fileUpdate()
                implemented maxLen in init() when reading words for format print
                fixed bug where the first entry in a file can't be found
                    in init(), see ord( eng[0] ) > 256
                show() is no longer showWIP() :)
                SUCCESFULLY ADDED READ/WRITE OF METADATA
 07-03-2019:    begin rewriting add() to work with metadata, and correct auto
                    settings when caseEngine is wrong
                removed plural ending from Data Structure for now, as it varies
                    with case, and will eventually be appended after declension
 07-08-2019:    finished add() in 131 lines!
                updated Data Structure in DATA CONTAINMENT FORMAT to show
                    translated word is in a list, to better reflect actual
                    storage
 07-09-2019:    replaced iterative lookup in show() with in keyword
                added support for SHOW all command to dump all entries
                added boolean update flag to do file writeback before successful
                    exit, added file writeback in main loop
                began adding comments to add()
*07-11-2019:    replaced X with - as negative space character in add()
                finished commenting add()
 07-14-2019:    began writing note()
 07-15-2019:    removed add function, placed in separate module
                placed caseEngine in folder, updated import
                fixed bug where exiting with EXIT command wouldn't update file
                fixed topic data cutoff bug, in init()
 07-16-2019:    commented add()
                wrote edit()
 07-24-2019:    commented edit()
 07-31-2019:    added reverse lookup functionality
 08-01-2019:    made show() search through attribute list as well, so user can
                    search for masculine/feminine/nouns/etc.
 08-05-2019:    updated metadata1 description in Data Containment Format to show
                    that capital X is no longer being used as the dropped letter
                    character, but is now the hyphen (-)
                changed metadata2 description in Data Containment Format to show
                    genders being stored as the whole word, and not the first
                    letter. Did not update Data Structure for lack of space
 08-08-2019:    imported lineCounter to print project size
                added call to lineCounter.size() in show() with command
                    'SHOW size'
                added argument to edit() call to allow single-line command call,
                    i.e. 'EDIT soup'
                merged attribute and topic descriptions in the DATA CONTAINMENT
                    FORMAT; metaData2 is now a dictionary of PLURAL declension
                    to mirror metaData1, but plural
                    
                    NOTE: This doesn't entirely work for adjectives and verbs
                          Try to find away to store ALL data in an efficient
                          manner, such that the least amount of things are
                          changed or wasted between different parts of speech
*08-22-2019:

 ===============================================================================
 DATA CONTAINMENT FORMAT
 -------------------------------------------------------------------------------
 Data Structure
 
 { english : [ [ russian ], { a:X, ... }, [ m/f/n/None, ...], [ topic, ... ] ] }

 Explicit File Storage

 english|russian|X,Y,...|m/f/n/None,pl,...|topic,...\n


 Data is stored in a dictionary
 All data is stored in unicode strings
 The value paired with the key is a list of length 4

 The first position of the list will always contain the base translation

 Everything after the first position is metadata

     metaData1 will always be a dictionary containing the cases as keys and the
     ending as values. To denote that a letter is dropped, and not merely
     added, the ending will contain a hyphen (-) for every letter dropped.
     The keys are hardcoded as follows.
         a      : accusative
         d      : dative
         g      : gentitive
         i      : instrumentive
         n      : nominative
         p      : propositional
         
     metaData2 will always be follow the same criterion as metaData1, but will
     show the PLURAL declension, instead of the singlular declension.

     metaData3 begins the topic and attribute data. This will contain things like
     the part of speech, gender, and the animateness as attributes, as well as
     other characteristics that make the word irregular in some way. metaData3
     will also contain words like "animal", etc. for use with SHOW command.

         masculine      : Masculine
         feminine       : Feminine
         neuter         : Neuter
         None           : Unknown or not applicable

         The program will attempt to determine the gender and declension
         when the user is adding the data, but the user can override.

         aj     : Adjective
         av     : Adverb
         c      : Conjunction
         i      : Interjection
         n      : Noun
         pn     : Pronoun
         pp     : Preposition
         v      : Verb

"""

# ==============================================================================
#
#   IMPORTS
#
# ------------------------------------------------------------------------------

# Used for parsing Russian words, determining gender and declension
from mod import caseEngine

# Used for adding new translations to the master data set
from mod import addM

# Used for editing old translation in the master data set
from mod import editM

# Used to print out the size of the entire project in lines
from mod import lineCounter

import codecs       # Used for handling unicode files
#import os           # Used for clearing the screen
import sys          # Used for looking at command line arguments


# ==============================================================================
#
#   UPDATE README
#
# ------------------------------------------------------------------------------

# Open README for updating every time script is run
rd = codecs.open( 'README.md', 'w' , encoding = 'utf-8' )
rd.write( '# TLPr\n' )              # Reprint Title
rd.write( u'%s' % readme )          # Print comment header
rd.close()                          # Close file, flush write buffer


# ==============================================================================
#
#   PARSE FLAGS
#   TODO:   check for contains, work out differing logic and flow
# ------------------------------------------------------------------------------

if len( sys.argv ) is 2:            # Check for command line flag
    # If the flag is readme
    if sys.argv[1].lower() == 'readme':
        exit()                      # Quit, you've already updated the readme
    # If the flag is debug
    elif sys.argv[1].lower() == 'debug':
        # I don't really know what to do for this, but it might be useful...
        pass
    
# ==============================================================================
#
#   FUNCTIONS
#
# -----------------------------------------------------------------------------

"""
 ===============================================================================
 Revn: 12-27-2018 (TLP)
 Func: Clears the screen
 Meth: Import os, lambda
 Args: None
 Retn: None, clears screen

 TODO: make system independent
 ===============================================================================
"""
#cls = lambda: os.system( 'cls' )    # Call cls through the system
                                    # Needs to be made more robust

"""
 ===============================================================================
 Revn: 07-15-2019
 Func: Prompt user for new translation, update dict, update file
 Meth: Call external module, watch for changes
 Args: str e: an input English word, or None if nothing was implicitly given
 Retn: None

 TODO: Comment
 ===============================================================================
"""
def add( e = None ):
    global update                       # Import update flag
    
    newEntrant = addM.add( e )          # Pass input to module, save return
    if not newEntrant is None:          # Check to see if there was a new entry
        data.update( newEntrant )       # Add new entry to current dictionary
        update = True                   # Set flag to update file before exiting
"""
 ===============================================================================
 Revn: 07-16-2019
 Func: Edit an existing translation pair 
 Meth: Take input, if not in data, prompt to add; ask if new tranlation or data
       is being added, add to specific place depending on what it was, ask if
       user is sure
 Args: str modifier: specify opening mode of file, e.g. read, write, append
 Retn: None

 TODO: Actually add appropriate \n char
       NOT rewrite every entry, actually append
 ===============================================================================
"""
def edit( e = None ):
    global data         # Import data
    global update       # Import file update flag

    if e is None:
        # Take user input
        e = input( 'What word would you like to edit?\n>> ' ).lower()
    if not e in data:
        # If the word doesn't exist, try to add it
        print( 'That word does not exist in the the table.' )
        dec = input( 'Would you like to add it?\n>> ' ).lower()
        if dec in [ 'y', 'ye', 'yes', 'yeah', 'yeet' ]:
            add( e )
        return                      # Return, to avoid editing a new entrant

    
    old = data[e]                   # Store copy of old entrant
    new = editM.edit( e, data[e] )  # Send off to module and save return

    # If the entrant was modified, set file update flag
    update = old is not new and new is not None

"""
 ===============================================================================
 Revn: 06-27-2019
 Func: Rewrite entire file to update 
 Meth: Open with codecs, parse data and metadata, concat into string with
       special delimiters, write as unicode string
 Args: None
 Retn: None

 TODO: Comment
 ===============================================================================
"""
def fileUpdate():
    global data         # Import data
    global caseNames    # Import names of different cases
    # Open file in unicode mode

    file = codecs.open( 'data.txt', 'w' , encoding='utf-8' )
    for key in data:                    # Iterate over all keys
        dataString = ''                 # Make empty string to concat to
        dataString += key               # Add English word
        for item in data[key]:          # Iterate over all data attached to word
            dataString += '|'           # Add pipe delimiter
            # If not in position 1 (not the case endings)
            if not data[key].index( item ) is 1:
                for element in item:    # Iterate for all data in metadata field
                    # Concat data, add comma to delimit distinct in-field data
                    dataString += element + ','
            # If dealing with cases, must grab the letters to do a lookup and
            # write back IN ORDER. IS NOT imperative, but saves space
            else:
                for letter in caseNames:
                    # Dict lookup of case, to ensure order, concat with comma
                    dataString += data[key][1][letter] + ','
            dataString = dataString[:-1]    # Remove last hanging comma
            
        # LOL breaks if I don't use format specificiers RIP
        file.write( u'%s\n' % dataString )

"""
 ===============================================================================
 Revn: 07-15-2019
 Func: Pull data from file and store in dictionary
 Meth: Open with codecs, parse each line in accordance with DATA CONAINMENT
       FORMAT, load into data structures, and add to final data container
 Args: None
 Retn: None

 TODO: 
 ===============================================================================
"""
def init():
    global data                         # Import data
    global maxLen                       # Import max length of english word
    global caseNames                    # Import names of different cases
    
    # Open file in unicode 
    file = codecs.open( 'data.txt', encoding='utf-8' )
    for line in file:                       # Iterate over all lines in file
        # Make empty list for Russian word for ease of writeback
        rus = list()
        
        line  = line[:-1].split( '|' )      # Rip out newline, split over pipes
        eng   = line[0]                     # Save English word

        # First character in file is a weird unicode char with huge ord()
        if ord( eng[0] ) > 256:             # Get rid of the first character
            eng = eng[1:]

        # Keep track of longest word with ternary statement for format print
        maxLen = maxLen if maxLen > len( eng ) else len( eng )

        rus.append( line[1] )               # Save Russian word
        case  = line[2].split( ',' )        # Make list of case endings
        meta  = line[3].split( ',' )        # Make list of other metadata
        topic = line[4].split( ',' )   # Make list of topic data
        #topic = line[4][:-1].split( ',' )
        # This line caused a bug where topic data wouldn't return properly
        # because the last letter of the word would be cut off. For example
        # 'animal' -> 'anima'
        # I don't know why it changed all of a sudden, after working for a week

        dataIn = list()                     # Make empty list for metadata
        # Put the Russian word in list for ease of writing back to a file later
        dataIn.append( rus )                # Add Russian in first position

        c = dict()                          # Make dict for cases and endings

        # Iterate over letters in the string of case names
        for pos in range( len( caseNames ) ):
            # Add specific case name and case ending to dict
            c.update( { caseNames[pos] : case[pos] } )

        dataIn.append( c )                  # Add cases in second position
        dataIn.append( meta )               # Add metadata as is in third
        dataIn.append( topic )              # Add topic data as is last
        data.update( { eng : dataIn } )     # Add to final data container

"""
 ===============================================================================
 Revn: 07-14-2019
 Func: Open and display digital notecards for editing
 Meth: Prompt user for a file, read into string, print, prompt for edit?
 Args: str topic: string that corresponds to file topic
 Retn: None

 TODO: write
 ===============================================================================
"""
def note( topic = None ):
    helpString = '''
Usage::NOTE [topic]
            alph -> Alphabet and Pronunciation
            and  -> Conjunctions
            case -> The Six Cases
            poss -> Possesive Pronouns
            pro  -> Nominative Pronouns

            new  -> Make a new file
    '''

    if topic == 'help' or topic is None:
        print( helpString )
    elif topic == 'alph':
        pass
    elif topic == 'and':
        pass
    elif topic == 'case':
        pass
    elif topic == 'poss':
        pass
    elif topic == 'pro':
        pass
    elif topic == 'new':
        fileName = input( 'What is the name of the new file?\n' ).lower()
        #newFile = codecs.open( fileName + '.txt', 'w' , encoding='utf-8' )
    else:
        print( helpString )

"""
 ===============================================================================
 Revn: 08-01-2019
 Func: Show all translation pairs that pertain to the input topic
 Meth: Iterate over all pairs *sigh* and see if the topic is tied to it
 Args: str topic: string to search all metadata for
 Retn: None

 TODO: allow support for multiple commands, i.e. SHOW masculine noun
 ===============================================================================
"""
def show( topic ):
    global data                                 # Import data
    global maxLen                               # Import max length of word

    if topic in [ 'size' ]:                     # If user wants project size
        lineCounter.size()                      # Call module that counts lines
        return                                  # Return, don't print topic

    # 8 is used because a tab on the IDLE is 8 characters, and this program can
    # only run on the IDLE thus far. + 1 for if maxLen is below 8, that way
    # a tab is still printed
    tabNum = ( maxLen // 8 ) + 1                # Calculate apt number of tabs

    print( '\n', topic.upper(), '\n' )          # Print topic in all caps
    for key in data:                            # Iterate over all english words
        # If data matches input, or user wants all entries
        if topic in data[key][3] or topic == 'all':
            print( key, end = '' )              # Print english word
            for number in range( tabNum ):      # Iterate by amnt. tabs needed
                print( '\t', end = '' )         # Print a tab, no newline
            print( ':', data[key][0][0] )       # Print translation

        # If attribute matches input, i.e. masculine, feminine, noun, etc.
        if topic in data[key][2]:
            print( key, end = '' )              # Print english word
            for number in range( tabNum ):      # Iterate by amnt. tabs needed
                print( '\t', end = '' )         # Print a tab, no newline
            print( ':', data[key][0][0] )       # Print translation

    print()

# ==============================================================================
#
#   GLOBAL VARIABLES
#
# ------------------------------------------------------------------------------

data = {}           # Master data container
maxLen = 0          # Init max English word length, for formatted printing

update = False      # Flag to enable file writeback if the data was updated

####
#### Consider making cases a list...
####
caseNames = 'adginp'    # First letter of each case, for reading for file

# Basic help prompt
helpM = 'What word do you want to look up?\nType HELP for help.\n>> '
# In-depth help prompt
instr = '''Type ADD to add a new entry
Type EDIT to edit an existing entry
Type SHOW <topic> to show all entries relating to that topic
Type SHOW all to dump all entries in the table
Type EXIT or QUIT to close the program
Type HELP to display this message
'''
#Type CLS to clear the screen'''

i = ''      # Init string to hold user input

### ============================================================================
###
### BODY 
###
###     Revn: 07-15-2019
###     Func: main, continuously prompt user for english words
###     Meth: Loop until user says no, check input for commands, set input to
###           lowercase, search dictionary of 
### ----------------------------------------------------------------------------

init()      # Pull data out of data file, store in dictionary

# Store Russian words for easy reverse lookup
russian = []
for english in data.keys():
    russian.append( data[english][0][0] )

# Wrap in try-except to quit gracefully on a keyboard interrupt
try:
    while True:     # Loop forever
        i = input( helpM )  # Print help menu, take input
        if i in ['EXIT','E','STOP','QUIT','KILL']:  # Compare to stop signals
            fileUpdate() if update else None    # Update datafile if need be
            exit()          # Exit if user entered stop signal
        if i == 'HELP':     # If the user needs help
            print( instr )  # Print in-depth help menu
            continue        # Skip to top of loop
        if i[:3] == 'ADD':  # If user is trying to add
            print()
            # Grab first word if given, otherwise begin add procedure with no arg
            add( i[4:].split( ' ' )[0] or None )
            continue        # Skip to top of loop
        if i[:4] == 'EDIT':     # If user wants to edit an entry
            print()
            # Grab first word if given otherwise begin edit procedure with no arg
            edit( i[5:].split( ' ' )[0] or None )
            continue        # Skip to top of loop
        # CLS doesn't work because this runs in the shell
##        if i == 'CLS':      # If user wants to clear the screen
##            cls()           # Call clear lambda function
##            continue        # Skip to top of loop
        if i[:4] == 'SHOW': # If user wants to dump metadata
            print()
            # Only grab the first word after SHOW
            show( i[5:].split( ' ' )[0] )   # Dump words related to metadata
            continue        # Skip to top of loop
        i = i.lower()       # Force input to be lowercase
        if i in data:       # If the user input is in the dataset
            print( data[i][0][0], '\n' )    # Print it out
        elif i in russian:  # If user input is in the translation set
            for english in data.keys():         # Iterate through all keys
                if data[english][0][0] == i:    # Look for the corresponding key
                    print( english, '\n' )      # Print as normal
        else:               # If the user input is not in the dataset
            print( 'Entry', i, 'does not exist\n' )
except KeyboardInterrupt:
    fileUpdate() if update else None    # Update datafile if need be
    exit()                  # EXEUNT

### ============================================================================
