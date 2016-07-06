boolTest = None # creating an object for boolean
x = input("search for a number\n") # get input as it is, python will determine the formate
#if raw_input is used regardless of what the input is it will be converted to string

for i in range (0,10): # for i = 0, i <= 10, i++
    if x == i:
        print "found " + str(i) #sytem
        boolTest = True
    else:
        pass
if boolTest: #if boolTest == true
    print "Found the number" + str(x)
