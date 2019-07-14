# TLPr

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

 english|russian|X,Y,...|m/f/n/None,pl,...|topic,...



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

