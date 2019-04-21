# -*- coding: utf-8 -*-

"""
 ===============================================================================
 Auth: Sam Celani
 Prog: tlpr.py
 Revn: 04-16-2019 Ver 0.0
 Func: 

 TODO: COMMENTS
       Write edit, delete, fadd, fedit, fdel
       Merge with original TLP, add switch between languages
       Add metadata
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
                


 ===============================================================================
 DATA CONTAINMENT FORMAT
 -------------------------------------------------------------------------------
 { english : 'russian1, russian2, ...,|, metaData1, metaData2, ...' }

###
### CONSIDER REMOVING N RUSSIAN WORDS AND THEIR CASES IN SEPARATE LISTS
### THIS WOULD ALLOW REMOVAL OF THE DELIMITER!!!!!
###

 Data is stored in a dictionary { : }
 All data is stored in unicode strings: english, russianN, metaDataN,|
 Strings that aren't 'english' are stored in a comma-separated string ',,,,'
 Split string into list, parse list until the delimiter, |, is found
 Everything after the delimiter is metadata
     metaData1 will always be the gender of the word
         m      : Masculine
         f      : Feminine
         n      : Neuter
         None   : Unknown

         The program will attempt to determine the gender, but user can override
     metaData2 will always be the part of the sentence that the word is
         n      : noun
         aj     : adjective
         p      : pronoun
         v      : verb
         av     : adverb
         
     metaData3 will always be the case of the word
         g      : gentitive
         a      : accusative
         p      : propositional
         
    metaData4 begins the topic data
 Parsing is gonna be interesting?

"""

# ==============================================================================
#
#   IMPORTS
#
# ------------------------------------------------------------------------------


import os           # Used for clearing the screen
import codecs       # Used for handling unicode files


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
    meta = [ 'gender', 'case' ]
    e = input( 'What word do you want to add?\n>> ' ).lower()
    r = input( 'What does that translate to?\n>> ' ).lower()
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
    print( m.split( ',' ) )

    """
    check = input().lower()
    if check == 'yes':
        data.update( { i : j } )
        fileUpdate('w')
    else:
        print('Add aborted')
    print()
    """


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
        if dec is in [ 'gender', 'g' ]:
            gender = input( 'What is the gender of the word?\n>> ' ).lower()
            oldData[0] = gender
        elif dec is in [ 'structure', 'struct', 's' ]:
            struct = input( 'What part of the sentence is the word?\n>> ' ).lower()
            oldData[1] = struct
        elif dec is in [ 'case', 'c' ]:
            case = input( 'What is the case of the word?\n>> ' ).lower()
            oldData[2] = case
        elif dec is in [ 'neither', 'n' ]:
            neither = input( 'What tag did you want to add?\n>> ' ).lower()
            oldData.append(neither)
        else:
            print( 'Command not recognized, edit aborted.' )
            return
        confirm = input( 'Are you sure you want to add ' ).lower()
        print( '%s : %s ?\n>> ' % ( e, str( oldData ) ), end = '' )
        if confirm is in [ 'yes', 'y' ]:
            data.update( { e : oldData } )
            #fileUpdate()
            print( 'Entry %s has been updated' % e )
    else:
        print( 'Command not recognized, edit aborted.' )


"""
 ===============================================================================
 Revn: 04-20-2019
 Func: Rewrite entire file to update 
 Meth: Open with codecs, write each KVP as line
 Args: None
 Retn: None

 TODO: Actually add appropriate \n char
       Deprecate
 ===============================================================================
"""
def fileUpdate():
    global data         # Import data
    # Open file in unicode mode, with variable mode (read/write/append)
    file = codecs.open('data.txt', 'w' , encoding='utf-8')
    for key in data:    # Iterate over all keys
        # Actually write unicode string to file
        # LOL breaks if I don't use format specificiers RIP
        file.write(u'%s,%s\n' % (key, data[key]))

"""
 ===============================================================================
 Revn: 04-20-2019
 Func: Pull data from file and store in dictionary
 Meth: Open with codecs, read each line as KVP
 Args: None
 Retn: None

 TODO:
 ===============================================================================
"""
def init():
    global data                         # Import data
    global maxLen                       # Import max length of english word
    # Open file in unicode 
    file = codecs.open('data.txt', encoding='utf-8')
    for line in file:                   # Iterate over all lines in file
        e = line.split(',')[0]          # Separate the english word
        r = line.split(',')[1:]         # Everything but english word is data
        r = r[-1][:-1]                  # Strip the newline off
        # Update max length of english word
        maxLen = len(e) if len(e) > maxLen else maxLen
        data.update( { e : r } )        # Add to dictionary


"""
 ===============================================================================
 Revn: 04-20-2019
 Func: Show all translation pairs that pertain to the input topic
 Meth: Iterate over all pairs *sigh* and see if the topic is tied to it
 Args: str topic: string to search all metadata for
 Retn: None

 TODO: Test, format print based on length
 ===============================================================================
"""
def showWIP( topic ):
    global data                                 # Import data
    global maxLen                               # Import max length of word

    tabNum = maxLen // 8                        # Calculate apt number of tabs

    print( '\n', topic.upper(), '\n' )          # Print topic in all caps
    for key in data:                            # Iterate over all english words
        for entry in data[key]:                 # Iterate over associated data
            if entry == topic:                  # If data matches input
                print( key, end = '' )          # Print english word
                for number in range(tabNum):    # Iterate by amnt. tabs needed
                    print( '\t', end = '' )     # Print a tab, no newline
                print( ': ', data[key] )        # Print translation

"""
 ===============================================================================
 Revn: 04-20-2019
 Func: show
 Meth: Iterate over KVPs, print
 Args: None
 Retn: None

 TODO: Deprecate
 ===============================================================================
"""
def show( topic ):
    global data                     # Import data
    for key in data:                # Iterate over all keys
        print(key, ':', data[key])  # Dump all entries

# ==============================================================================
#
#   GLOBAL VARIABLES
#
# ------------------------------------------------------------------------------

data = {}
maxLen = 0

helpM = 'What word do you want to look up?\nType HELP for help.\n>> '
instr = '''Type ADD to add a new entry
Type EDIT to edit an existing entry
Type SHOW <topic> to show all entries relating to that topic
Type EXIT or QUIT to close the program
Type HELP to display this message'''

i = ''

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
        if i[:4] == 'SHOW': # If user wants to dump metadata
            # Only grab the first word after SHOW
            show(i[5:].split(' ')[0])   # Dump everything related to metadata
            continue        # Skip to top of loop
        i = i.lower()       # Normalize input
        if i in data:       # If the user input is in the dataset
            print(data[i]+'\n') # Print it out
        else:               # If the user input is not in the dataset
            print('Entry', i, 'does not exist\n')
except KeyboardInterrupt:
    exit()                  # EXEUNT

### ============================================================================
