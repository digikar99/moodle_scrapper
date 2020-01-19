import json

with open('links.json', 'r') as jsonFile :
    nameToHref = json.load(jsonFile)
    # print(nameToHref)

    #   with open('changes.txt', 'r') as courseFile :
    #        lines = courseFile.split()
    # lines = [line.rstrip('\n') for line in open('changes.txt')]
    return_string = ""
    for course in nameToHref:
        # print (course)
        return_string += nameToHref[course] + " "
    print(return_string)
