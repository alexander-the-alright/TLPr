# -*- coding: utf-8 -*-

readme = u"""
 ===============================================================================
 Auth: Sam Celani
 Prog: tlpr.py
 Revn: 07-11-2019  Ver 3.0
 Func: 

 TODO: COMMENTS
       Write edit, delete, fadd, fedit, fdel
       Add plural declension
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
     added, the ending will contain a capital X before the appending hyphen.
     The keys are hardcoded as follows.
         a      : accusative
         d      : dative
         g      : gentitive
         i      : instrumentive
         n      : nominative
         p      : propositional
         
     metaData2 will always contain firstly the gender of the word. Second is
     the part of a speech. This is all that is strictly defined, more varies.
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


import caseEngine   # Used for parsing Russian words, determining gender and 
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
 Revn: 07-08-2019
 Func: Prompt user for new translation, update dict, update file
 Meth: 
 Args: None
 Retn: None

 TODO: Comment
       Remove, and make external module
       Add gender and part of speech to topic, deprecate attribute list??
       Fix topic, so user doesn't need to enter END to finish
 ===============================================================================
"""
def add( e = None ):
    global data         # Grab global data so information can be written back
    global update       # If file is updated, set update flag

    dataList = []       # Store all new data before updating old data
    attributeList = []  # Store gender and part of speech ( for now )
    topicList = []      # Store topic metadata
    
    if e is None:       # If no input is explicitly given...
        # explicitly ask for one
        e = input( 'What word do you want to add?\n>> ' ).lower()
    else:
        e = e.lower()   # Otherwise, just force lowercase

    # Ask user for translation
    r = input( 'What does that translate to?\n>> ' ).lower()

    dataList.append( [ r ] )    # Put translation in list, and add to new data
    
    gender = caseEngine.parse( r )  # Outsource determining gender

    # Probe user for confirmation
    print( 'Gender automatically found to be %s. Is this correct?' % gender )
    decision = input('>> ').lower() # Grab answer, force lowercase

    ## Probably a way to do this with like 5 less lines, but if it aint broke...
    # If user answered in the affirmative
    if decision in [ 'y', 'ye', 'yes', 'yeah', 'yeet' ]:
        attributeList.append( gender )  # Store gender in list
    else:   # User answer in negative
        # Prompt user for actual gender
        print( 'What is the actual gender of %s?' % r )
        gender = input( '>> ' ).lower() # Force input to lowercase

        # If masculine, store masculine
        if gender in [ 'm', 'masc', 'masculine' ]:
            attributeList.append( 'masculine' )
        # If feminine, store feminine
        elif gender in [ 'f', 'fem', 'feminine' ]:
            attributeList.append( 'feminine' )
        # If neuter, store neuter
        elif gender in [ 'n', 'neut', 'neuter' ]:
            attributeList.append( 'neuter' )
        # Otherwise, just say None
        else:
            print( 'Input gender not recognized.' )
            attributeList.append( None )

    print( '\nDeclension automatically found to be as follows.\n' )
    # Outsource printing declension to caseEngine.endings
    endings = caseEngine.endings( r, gender )
    # Ask user if it looks right
    # Spoiler Alert: It's not, Russian is permanently irregular WOOOOOO
    print( 'Is this correct?' )

    decision = input('>> ').lower()
    # Get decision, loop until user is happy
    # because multiple cases may be incorrect
    while decision not in [ 'y', 'ye', 'yes', 'yeah', 'yeet' ]:
        print( 'Which case ending is incorrect?' )
        # Print each case abbreviation
        for key in endings:
            print( key, end=' ' )
        print()
        # Get user feedback on which is wrong
        case = input( '>> ' ).lower()
        # If it's not an acceptable answer, prompt
        if case not in endings.keys():
            print( 'Input case not recognized.' )
        # Else, prompt user for real declension
        else:
            print( 'What is the appropriate ending?' )
            # Don't sanitize input, just added it
            endings[case] = input( '>> ' )

            ## Print new declension
            for key in endings.keys():          # Iterate over different cases
                strip = endings[key].count('-') # Keep track of amount of -'s
                                                # ( letters to get rid of )
                print( key, ' : ', end = '' )   # Print just the case
                if not strip is 0:              # If there are -'s in the ending
                    # Print everything but the last few letters
                    print( r[:-1*strip], end = '' )
                else:                           # If there are no -'s in ending
                    print( r, end = '' )        # Print the whole word
                # Finally, print the case-by-case ending
                print( endings[key][strip:] )
            print()

        # Ask user if satisfied, loop if not
        print( 'Is this correct?' )
        decision = input('>> ').lower()

    dataList.append( endings )      # Finish declension, add to working dataset

    ## Prompt about part of speech
    print( '\nWhat part of speech is %s?\n' % r )
    print('aj\t: Adjective\nav\t: Adverb\nc\t: Conjunction\ni\t: Interjection')
    print( 'n\t: Noun\npn\t: Pronoun\npp\t: Preposition\nv\t: Verb' )

    decision = input('\n>> ').lower()

    # If decision isn't in narrow list, assign decision None
    # Sanitizing this input for all parts of speech would be obnoxious for
    # me as an author and probably also as a user, so fuck it
    # Enter them as is, or don't
    if decision not in [ 'aj', 'av', 'c', 'i', 'n', 'pn', 'pp', 'v']:
        print( 'Input part of speech not recognized.' )
        decision = None

    # Append decision, either as a part of speech, or as None, idgaf
    attributeList.append( decision )
    # Thus far, attribute list only contains gender and part of speech
    # Add to working dataset
    dataList.append( attributeList )

    # The real meat, as about topic stuffs
    decision = input( 'Is there topic metadata?\n>> ' ).lower()

    # There's probably a way better way to do this than waiting for user to
    # say 'END'
    metadata = ''
    if decision in [ 'y', 'ye', 'yes', 'yeah', 'yeet' ]:
        # Literally just prompt user until they enter END
        while metadata != 'END':
            print( 'Input a new topic, or enter END to finish.' )
            metadata = input( '>> ' )
            # Kieckhafer would take my diploma from me for this
            # if metadata != 'END', append metadata.lower(), otherwise don't do
            # anything. I just didn't want to make an if and have to indent
            # for only one line
            topicList.append( metadata.lower() ) if metadata != 'END' else None

    # Add topic stuffs to working dataset, now the final dataset
    dataList.append( topicList )

    # Print the English word entered
    print( '\nENGLISH\n%s' % e )

    # Print the Russian translation
    print( '\nRUSSIAN\n%s' % dataList[0][0] )

    # Print singular declension
    print( '\nDECLENSION')
    for key in dataList[1].keys():      # Iterate over the different cases
        strip = dataList[1][key].count('-') # Keep track of the amount of -'s
                                            # ( letters to get rid of )
        print( key, ' : ', end = '' )       # Print just the case
        if not strip is 0:                  # If there are -'s in the ending
            # Print everything but the last few letters
            print( r[:-1*strip], end = '' )
        else:                               # If there are no -'s in the ending
            print( r, end = '' )            # Print the whole word
        # Finally, print the case-by-case ending
        print( dataList[1][key][strip:] )

    # Print the gender and part of speech, for now
    print( '\nATTRIBUTES' )
    for attribute in dataList[2]:
        print( attribute )

    # Print any user-added topic data
    print( '\nTOPIC' )
    for topic in dataList[3]:
        print( topic )

    # Ask user if the given information is correct
    print( '\n\nIs this correct?' )
    decision = input( '>> ' ).lower()

    # Check if decision is affirmative
    if decision in [ 'y', 'ye', 'yes', 'yeah', 'yeet' ]:
        data.update( { e : dataList } )
        update = True
        print()
    # If not, just completely drop it
    # Probably a better way to do it, but I don't wanna nest everything
    # in a while loop just yet
    else:
        print( 'Add aborted.\n' )

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
 Revn: 07-09-2019
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
        # If data matches input, or user wants all entries
        if topic in data[key][3] or topic == 'all':
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
instr ='''Type ADD to add a new entry
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
###     Revn: 07-09-2019
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
            fileUpdate() if update else None    # Update datafile if need be
        if i == 'HELP':     # If the user needs help
            print(instr)    # Print in-depth help menu
            continue        # Skip to top of loop
        if i[:3] == 'ADD':  # If user is trying to add
            # Grab first word if given, otherwise begin add procedure with no arg
            add( i[4:].split(' ')[0] or None )
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
    fileUpdate() if update else None    # Update datafile if need be
    exit()                  # EXEUNT

### ============================================================================
