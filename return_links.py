import json

return_string = ""

with open('links.json', 'r') as jsonFile :
    nameToHref = json.load(jsonFile)

    #   with open('changes.txt', 'r') as courseFile :
    #        lines = courseFile.split()
    lines = [line.rstrip('\n') for line in open('changes.txt')]

    for course in lines:
        #print course
        global return_string
        
        return_string += nameToHref[course] + " "
        
print return_string
