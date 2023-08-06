
"""

This function prints all elements of a list and its child lists if any.
Before executing it also checks if the root argument is a list or not.

"""



def printNestedList(meraList, indent=False, level=0):

    if(isinstance(meraList, list)):

        for each_item in meraList:
            if isinstance(each_item, list):
                printNestedList(each_item, indent, level+1)
            else:
                if(indent):
                    for i in range(level):
                        print("\t", end='')
                    print(each_item)
                else:
                    print(each_item)
    else:
        print(meraList+" is not a list")

