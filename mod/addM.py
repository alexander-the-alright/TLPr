readme = """
 ===============================================================================
 Auth: Sam Celani
 Prog: addM.py
 Revn: 08-22-2019 Ver 1.0
 Func: Add an entrant to the global dictionary in tlpr.py

 TODO: 
 ===============================================================================
 CHANGE LOG
 -------------------------------------------------------------------------------
 07-14-2019:    pulled finished add() function from tlpr.py and pasted here
                added newEntrant local variable
                removed global references
                removed call to update global data set
                added a return variable
 07-17-2019:    changed topic loop condition from entering 'END' to entering
                    an empty string in add()
                added local test import alongside final product import of
                    caseEngine
*08-22-2019:    add flag to local testing, so it will always run in the use case
                consistency changes for printed test

 ===============================================================================
"""

try:
    # Import for local testing use ( running purely this script )
    import caseEngine
    local = True
except:
    # Import for actual use case ( running from tlpr.py )
    from mod import caseEngine
    local = False

"""
 ===============================================================================
 Revn: 07-17-2019
 Func: Prompt user for a new entrant to global data set
 Meth: Exhaustively :/ take input, make whatever inferences are possible, prompt
       user to make sure, take new input if inference is wrong, store, return
 Args: str e: an input English word, or None if nothing was implicitly given
 Retn: dict newEntrant: dictionary of length 1 to be added to global data set
       or None if add was aborted

 TODO: Add gender and part of speech to topic, deprecate attribute list??
 ===============================================================================
"""
def add( e = None ):

    dataList = []       # Store all new data before updating old data
    attributeList = []  # Store gender and part of speech ( for now )
    topicList = []      # Store topic metadata
    newEntrant = None   # Variable to be rewritten and returned upon success
    
    if e is None:       # If no input is explicitly given...
        # explicitly ask for one
        e = input( 'What word do you want to add?\n>> ' ).lower()
    else:
        e = e.lower()   # Otherwise, just force lowercase

    print()

    # Ask user for translation
    r = input( 'What does that translate to?\n>> ' ).lower()
    print()

    dataList.append( [ r ] )    # Put translation in list, and add to new data
    
    gender = caseEngine.parse( r )  # Outsource determining gender

    # Probe user for confirmation
    print( 'Gender automatically found to be %s.\nIs this correct?' % gender )
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
    print('\naj\t: Adjective\nav\t: Adverb\nc\t: Conjunction\ni\t: Interjection')
    print( 'n\t: Noun\npn\t: Pronoun\npp\t: Preposition\nv\t: Verb' )
    print( '\nWhat part of speech is %s?' % r )

    decision = input('>> ').lower()

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
    decision = input( '\nIs there topic metadata?\n>> ' ).lower()

    # Can't start with an empty string, otherwise the while will always be
    # skipped. The print() and input()/assignment statements can also be
    # pulled out above the while AND moved to below the ternary to acheive
    # the same effect, in a way that is cleaner than having a non-empty string
    # initialized, but that's also a few more lines of code, and kind of clunky
    # in my opinion. This works, it's just eh
    metadata = 'X'
    if decision in [ 'y', 'ye', 'yes', 'yeah', 'yeet' ]:
        # Literally just prompt user until they enter END
        while len( metadata ) is not 0:
            print( 'Input a new topic, or press ENTER to finish.' )
            metadata = input( '>> ' )
            # Kieckhafer would take my diploma from me for this
            # if the length of metadata isn't 0 ( ergo, it's empty, or just
            # a newline ), append metadata.lower(), otherwise don't do
            # anything. I just didn't want to make an if and have to indent
            # for only one line
            topicList.append( metadata.lower() ) if len( metadata ) is not 0 else None


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
        newEntrant = { e : dataList }
        print()
    # If not, just completely drop it
    # Probably a better way to do it, but I don't wanna nest everything
    # in a while loop just yet
    else:
        print( 'Add aborted.\n' )

    return newEntrant


### ============================================================================
###
### BODY 
###
### ----------------------------------------------------------------------------

# Add comment before """ to enable script to run on its own
if local:
    try:
        while True:
            n = add( input( 'What word would you like to add?\n>> ' ).lower() )
            print( n )
    except KeyboardInterrupt:
        exit()

### ============================================================================

