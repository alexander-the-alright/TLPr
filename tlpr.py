# -*- coding: utf-8 -*-

readme = u"""
 ===============================================================================
 Auth: Sam Celani
 Prog: tlpr.py
 Revn: 06-26-2019  Ver 2.3
 Func: 

 TODO: COMMENTS
       Write edit, delete, fadd, fedit, fdel
       Merge with original TLP, add switch between languages
       Add verb support
       Reverse lookup
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
                    in init(), see ord(eng[0]) > 256
                show() is no longer showWIP() :)
                SUCCESFULLY ADDED READ/WRITE OF METADATA


 ===============================================================================
 DATA CONTAINMENT FORMAT
 -------------------------------------------------------------------------------
 Data Structure
 
 { english : [ russian, { a:X, ... }, [ m/f/n/None, pl, ...], [ topic, ... ] ] }

 Explicit File Storage

 english|russian|X,Y,...|m/f/n/None,pl,...|topic,...\n


 Data is stored in a dictionary
 All data is stored in unicode strings
 The value paired with the key is a list of length 4

 The first position of the list will always contain the base translation

 Everything after the first position is metadata

     metaData1 will always be a dictionary containing the cases as keys and the
     ending as values. To denote that a letter is dropped, and not merely
     added, the ending will contain a capital X before the appending hyphen.
     The keys are hardcoded as follows.
         a      : accusative
         d      : dative
         g      : gentitive
         i      : instrumentive
         n      : nominative
         p      : propositional
         
     metaData2 will always contain firstly the gender of the word. Second is
     the plural ending of the word (it is assumed the user enters the singular
     form of the word). Third is the part of a speech. This is all that is
     strictly defined, more varies.
         m      : Masculine
         f      : Feminine
         n      : Neuter
         None   : Unknown

         The program will attempt to determine the gender and plural ending
         when the user is inputting the data, but the user can override.

         aj     : Adjective
         av     : Adverb
         c      : Conjunction
         i      : Interjection
         n      : Noun
         pn     : Pronoun
         pp     : Preposition
         v      : Verb
         
     metaData3 begins the topic data. This will contain things like "animal",
     etc. for use with SHOW command

"""

# ==============================================================================
#
#   IMPORTS
#
# ------------------------------------------------------------------------------


import codecs       # Used for handling unicode files
import os           # Used for clearing the screen
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

if len(sys.argv) is 2:              # Check for command line flag
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
cls = lambda: os.system('cls')  # Call cls through the system
                                # Needs to be made more robust

"""
 ===============================================================================
 Revn: 04-20-2019
 Func: Prompt user for new translation, update dict, update file
 Meth: Two inputs, add to global data using update()
 Args: None
 Retn: None

 TODO: Comment
       ADD DELIMITER
 ===============================================================================
"""
def add():
    global data

    e = input( 'What word do you want to add?\n>> ' ).lower()
    r = input( 'What does that translate to?\n>> ' ).lower()


    
    meta = [ 'gender', 'case' ]

    y = input( 'Is there metadata?\n>> ' ).lower()
    ##
    ## ADD DELIMITER
    ## ALLOW VARIABLE TRANSLATIONS
    ##
    if y in [ 'y', 'yes', 'yeet' ]:
        m = ''
        i = 'init'

        for dataType in meta:
            print( 'What data do you want for %s?' % dataType ) 
            i = input( 'Enter TOPIC to skip to topic. Enter X to quit.\n' )
            if i in [ 'X', 'TOPIC' ]:
                break
            m += i.lower() + ','
        while not i == 'X':
            i = input( 'What data do you want for topic? Enter X to quit.\n' )
            m += i + ','
        m = m[:-3]
    
        print( 'Are you sure you want to add (', e, ': [', r, '|', m, '] ) ?' )
    else:
        print( 'Are you sure you want to add (', e, ': [', r, '] ) ?' )
    #print( m.split( ',' ) )


    check = input().lower()
    if check == 'yes':
        data.update( { e : r } )
        #fileUpdate('w')
    else:
        print('Add aborted')
    print()



"""
 ===============================================================================
 Revn: 04-20-2019
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
def edit():
    global data         # Import data

    e = input( 'What word would you like to edit?\n>> ' ).lower()
    ##
    ## ADD DELIMITER
    ## ALLOW VARIABLE TRANSLATIONS
    ##
    if not e in data:
        print( 'That word does not exist in the the table.' )
        dec = input( 'Would you like to add it?\n>> ' )
        if dec in [ 'y', 'yes' ]:
            add()
        else:
            return

    change = input( 'Do you want to change a translation or metadata?\n>> ' )
    change = change.lower()

    oldData = data[key]

    if change in [ 'translation', 't' ]:
        r = input( 'What does %s translate to?\n>> ' % e ).lower()
        data[e][0] = r
    elif change in [ 'metadata', 'm' ]:
        print( 'Did you want to edit the gender, case, structure, or none?' )
        dec = input( '>> ' ).lower()
        if dec in [ 'gender', 'g' ]:
            gender = input( 'What is the gender of the word?\n>> ' ).lower()
            oldData[0] = gender
        elif dec in [ 'structure', 'struct', 's' ]:
            struct = input( 'What part of the sentence is the word?\n>> ' ).lower()
            oldData[1] = struct
        elif dec in [ 'case', 'c' ]:
            case = input( 'What is the case of the word?\n>> ' ).lower()
            oldData[2] = case
        elif dec in [ 'neither', 'n' ]:
            neither = input( 'What tag did you want to add?\n>> ' ).lower()
            oldData.append(neither)
        else:
            print( 'Command not recognized, edit aborted.' )
            return
        confirm = input( 'Are you sure you want to add ' ).lower()
        print( '%s : %s ?\n>> ' % ( e, str( oldData ) ), end = '' )
        if confirm in [ 'yes', 'y' ]:
            data.update( { e : oldData } )
            #fileUpdate()
            print( 'Entry %s has been updated' % e )
    else:
        print( 'Command not recognized, edit aborted.' )


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
            if not data[key].index(item) is 1:
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
 Revn: 06-27-2019
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
    global caseNames                   # Import names of different cases
    
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
        topic = line[4][:-1].split( ',' )   # Make list of topic data

        dataIn = list()                     # Make empty list for metadata
        # Put the Russian word in list for ease of writing back to a file later
        dataIn.append( rus )                # Add Russian in first position

        c = dict()                          # Make dict for cases and endings

        # Iterate over letters in the string of case names
        for pos in range( len( caseNames ) ):
            # Add specific case name and case ending to dict
            c.update( { caseNames[pos] : case[pos] } )

        dataIn.append(c)                    # Add cases in second position
        dataIn.append(meta)                 # Add metadata as is in third
        dataIn.append(topic)                # Add topic data as is last
        data.update( { eng : dataIn } )     # Add to final data container

"""
 ===============================================================================
 Revn: 06-27-2019
 Func: Show all translation pairs that pertain to the input topic
 Meth: Iterate over all pairs *sigh* and see if the topic is tied to it
 Args: str topic: string to search all metadata for
 Retn: None

 TODO: 
 ===============================================================================
"""
def show( topic ):
    global data                                 # Import data
    global maxLen                               # Import max length of word

    tabNum = ( maxLen // 8 ) + 1                # Calculate apt number of tabs

    print( '\n', topic.upper(), '\n' )          # Print topic in all caps
    for key in data:                            # Iterate over all english words
        for entry in data[key][3]:              # Iterate over associated data
            if entry == topic:                  # If data matches input
                print( key, end = '' )          # Print english word
                for number in range(tabNum):    # Iterate by amnt. tabs needed
                    print( '\t', end = '' )     # Print a tab, no newline
                print( ':', data[key][0][0] )   # Print translation

    print()

# ==============================================================================
#
#   GLOBAL VARIABLES
#
# ------------------------------------------------------------------------------

data = {}           # Master data container
maxLen = 0          # Init max English word length, for formatted printing

####
#### Consider making cases a list...
####
caseNames = 'adginp'    # First letter of each case, for reading for file

# Basic help prompt
helpM = 'What word do you want to look up?\nType HELP for help.\n>> '
# In-depth help prompt
instr ='''Type ADD to add a new entry
Type EDIT to edit an existing entry
Type SHOW <topic> to show all entries relating to that topic
Type EXIT or QUIT to close the program
Type HELP to display this message'''
#Type CLS to clear the screen'''

i = ''      # Init string to hold user input

### ============================================================================
###
### BODY 
###
###     Revn: 04-20-2019
###     Func: main, continuously prompt user for english words
###     Meth: Loop until user says no, check input for commands, set input to
###           lowercase, search dictionary of 
### ----------------------------------------------------------------------------

init()      # Pull data out of data file, store in dictionary

# Wrap in try-except to quit gracefully on a keyboard interrupt
try:
    while True:     # Loop forever
        i = input(helpM)    # Print help menu, take input
        if i in ['EXIT','E','STOP','QUIT','KILL']:  # Compare to stop signals
            exit()          # Exit if user entered stop signal
        if i == 'HELP':     # If the user needs help
            print(instr)    # Print in-depth help menu
            continue        # Skip to top of loop
        if i == 'ADD':      # If user is trying to add
            add()           # Begin add procedure
            continue        # Skip to top of loop
        if i == 'EDIT':     # If user wants to edit an entry
            edit()          # Begin edit procedure
            continue        # Skip to top of loop
        # CLS doesn't work because this runs in the shell
##        if i == 'CLS':      # If user wants to clear the screen
##            cls()           # Call clear lambda function
##            continue        # Skip to top of loop
        if i[:4] == 'SHOW': # If user wants to dump metadata
            # Only grab the first word after SHOW
            show(i[5:].split(' ')[0])   # Dump words related to metadata
            continue        # Skip to top of loop
        i = i.lower()       # Force input to be lowercase
        if i in data:       # If the user input is in the dataset
            print( data[i][0][0], '\n')     # Print it out
        else:               # If the user input is not in the dataset
            print('Entry', i, 'does not exist\n')
except KeyboardInterrupt:
    exit()                  # EXEUNT

### ============================================================================
