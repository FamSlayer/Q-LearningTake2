import random

class Map():
    
    def __init__(self, info, load=False):
##        Load a provided map
        if load == True:
            self.load(info)
##        Make up your own map
        else:       
            self.map = self.emptyMap()
            if info == 1:
                self.generateObstacles1()
            elif info == 2:
                self.generateObstacles2()
            elif info == 3:
                self.generateObstacles3()
                
            self.generateStartFinish()     

##    Returns an "empty" 10x10 2D list/map
    def emptyMap(self):
        m = []
        for x in range(10):
            m.append(['.']*10)
        return m

##    Returns a copy of the map
    def copy(self):
        print "inside copy"
        new_map = Map(0)
        print new_map == self
        new_map.map = []

        for x in range(10):
            l = []
            for y in range(10):
                char = self.map[x][y]
                l.append(char)
            new_map.map.append(l)

        print "end of copy"
        print new_map == self
        return new_map

##    Print out the map all nice and pretty like
    def printMap(self):
        print ' ' + '- '*(11)
        for y in range(10):
            line = '| '
            for x in range(10):
                line += self.map[x][y] + ' '
            line += '|'
            print line
        print ' ' + '- '*(11)

##    Save the map to a given file
    def save(self, fname):
        fpath = "Saved Maps/" + fname + ".txt"
        dash_line = ' ' + '- '*(11)
        fout = open(fpath,"w")
        fout.write(dash_line + '\n')
        for row in self.map:
            line = '| '
            for col in row:
                line += col + ' '
            line += '|'
            fout.write( line + '\n' )
        fout.write(dash_line + '\n')
        fout.close()

        print ' -'*(17)
        print "Saved map to " + fpath
        print ' -'*(17)

##    Load the map from a given file
    def load(self, fname, pretty_print=False):
        self.map = []
        path = "Saved Maps/" + fname + ".txt"
        
        lines = open(path,"r").read().split('\n')
        rows = lines[1:-2]

        rowXcolumns = []
        for col_str in rows:
            cols = col_str.split()[1:-1]
            rowXcolumns.append(cols)
        
        for i in range(10):
            cs = []
            for r in rowXcolumns:
                cs.append(r[i])
            self.map.append(cs)           
        
        if pretty_print:
            print ' -'*(17)
            print "Loaded map from " + path
            print ' -'*(17)

##    Try to place an obstacle. Returns 0 on failure, 1 on success
    def placeObstacle(self,x,y):
        if self.map[x][y] == '.':
            self.map[x][y] = 'X'
            return 1
        return 0

##    Randomly place a Start and Finish on unoccupied locations in the map
    def generateStartFinish(self):
        while True:
            rand_row = random.randint(0,9)
            rand_col = random.randint(0,9)
            if self.map[rand_row][rand_col] == '.':
                self.map[rand_row][rand_col] = 'S'
                break

        while True:
            rand_row = random.randint(0,9)
            rand_col = random.randint(0,9)
            if self.map[rand_row][rand_col] == '.':
                self.map[rand_row][rand_col] = 'F'
                break
    
##    Generate obstacles by placing 3 walls in a row vertically or horizontally
    def generateObstacles1(self, num_obstacles=10):
        obstacles_placed = 0
        while obstacles_placed < num_obstacles:
            rand_row = random.randint(1,8)
            rand_col = random.randint(1,8)
            obstacles_placed += self.makeWall1(rand_row, rand_col)

##    Randomly place individual obstacles until the amount has been placed
    def generateObstacles2(self, num_obstacles=10):
        obstacles_placed = 0
        while obstacles_placed < num_obstacles:
            rand_row = random.randint(1,8)
            rand_col = random.randint(1,8)
            obstacles_placed += self.placeObstacle(rand_row,rand_col)

##    Generate randomly sized walls - up to max of 2 * stretch - vertically or horizontally
    def generateObstacles3(self, num_obstacles=10, stretch=3):
        obstacles_placed = 0
        while obstacles_placed < num_obstacles:
            rand_row = random.randint(1,8)
            rand_col = random.randint(1,8)
            obstacles_placed += self.makeWall3(rand_row, rand_col, stretch)

##    Places the wall used by placeObstacles1
    def makeWall1(self, x, y):
        num_placed = 0
        if random.randint(0,99) < 50:   ## HORIZONTAL
            num_placed += self.placeObstacle(x,y-1)
            num_placed += self.placeObstacle(x,y)
            num_placed += self.placeObstacle(x,y+1)
        else:                           ## VERTICAL
            num_placed += self.placeObstacle(x-1,y)
            num_placed += self.placeObstacle(x,y)
            num_placed += self.placeObstacle(x+1,y)
        return num_placed

##    Places the wall used by placeObstacle3
    def makeWall3(self, x, y, num):
        num_placed = 0
        if random.randint(0,99) < 50:   ## HORIZONTAL
            num_placed += self.placeObstacle(x,y)
            num_right = random.randint(0,num)
            num_left = random.randint(0,num)
            for r in range(1,num_right+1):
                if y+r > 9:
                    break
                else:
                    num_placed += self.placeObstacle(x,y+r)
            for l in range(1, num_left+1):
                if y-l < 0:
                    break
                else:
                    num_placed += self.placeObstacle(x,y-l)            
        else:                           ## VERTICAL
            num_placed += self.placeObstacle(x,y)
            num_up = random.randint(0,num)
            num_down = random.randint(0,num)
            for u in range(1,num_up+1):
                if x-u < 0:
                    break
                else:
                    num_placed += self.placeObstacle(x-u,y)
            for d in range(1, num_down+1):
                if x+d > 9:
                    break
                else:
                    num_placed += self.placeObstacle(x+d,y)
        return num_placed


