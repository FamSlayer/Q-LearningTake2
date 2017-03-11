import time, QLearning, Map

def main():

##    print ' -'*(21)
##    map1 = Map.Map("chosen_map_1",True)
##    map2 = Map.Map("chosen_map_2",True)
##    map3 = Map.Map("chosen_map_3",True)
##    print ' -'*(21)
##    
##    map1.printMap()
##    map2.printMap()
##    map3.printMap()

    
    
##    running = False
##    while running:
##        map1 = Map.Map(1)
##        map1.printMap()
##
##        map2 = Map.Map(2)
##        map2.printMap()
##
##        map3 = Map.Map(3)
##        map3.printMap()
##
##        save = raw_input("Would you like to save any of these? ")
##        if save in ["yes", "y", "sure"]:
##            select = raw_input("Which ones would you like to save? [Ex - '1 2 3' to save all 3] ")
##            choices = select.split()
##            if "1" in choices:
##                f_name = raw_input("Enter a file name for map 1: (ignore file type) ")
##                map1.save(f_name)
##            if "2" in choices:
##                f_name = raw_input("Enter a file name for map 2: (ignore file type) ")
##                map2.save(f_name)
##            if "3" in choices:
##                f_name = raw_input("Enter a file name for map 3: (ignore file type) ")
##                map3.save(f_name)
##            
##        regenerate = raw_input("Would you like to generate again? ")
##        if not regenerate in ["yes","y","sure"]:
##            running = False
    

    BEGIN1 = time.time()
    obj1 = QLearning.QLearning("chosen_map_1")
    obj1.my_map.printMap()
    obj1.run(10000)
    #obj1.printResult()
    obj1.showPolicy()
    END1 = time.time()

    BEGIN2 = time.time()
    obj2 = QLearning.QLearning("chosen_map_2")
    obj2.my_map.printMap()
    obj2.run(10000)
    #obj2.printResult()
    obj2.showPolicy()
    END2 = time.time()

    BEGIN3 = time.time()
    obj3 = QLearning.QLearning("chosen_map_3")
    obj3.my_map.printMap()
    obj3.run(10000)
    #obj3.printResult()
    obj3.showPolicy()
    END3 = time.time()

    print '\n'
    obj1.followPolicy()
    print "Time: " + str( END1 - BEGIN1 ) + " sec.\n"
    obj2.followPolicy()
    print "Time: " + str( END2 - BEGIN2 ) + " sec.\n"
    obj3.followPolicy()
    print "Time: " + str( END3 - BEGIN3 ) + " sec.\n"
    print "Time: " + str( END3 - BEGIN1 ) + " sec.\n"

    












    

main()
