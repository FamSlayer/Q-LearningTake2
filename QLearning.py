import random, copy, decimal, Map

class QLearning():
    
    ## Q(s,a)= Q(s,a) + alpha * (R(s,a) + gamma * Max(next state, all actions) - Q(s,a))
    
    """
    GENERAL CLASS INFORMATION AND STRUCTURE

    1.  States will look like states[x][y] = (x,y)

    2.  The path taken will be stored as [(x1,y1), (x2,y2), ... , (xn, yn)]
        States cannot be taken twice, and the path will ensure that

    3.  Will have a function called actionFromState that gets possible actions from a state
    
    4.  Will have member variables:
            self.start = (x,y) - starting state
            self.finish = (x,y) - goal state

    5.  Structure of R and Q dicts, and will be Q[(x1,y1)][(x2,y2)]

    6.  Will add setR() function in order to add punishment to the tiles
            Agent will be punished if it gets stuck because it can't move/go back on itself

    7.  Actions list will be actions[x][y] = [(x-1,y),(x,y+1),(x+1,y),(x,y-1)] - when no obstacles

    """

    statesCount = 100 # even obstacles will be technically 'states', although they won't be accessible

    states = []
    stateNames = []
    for x in range(10):
        state_list = []
        name_list = []
        for y in range(10):
##            print (x,y)
            state_list.append( (x,y) )
            name_list.append( '('+str(x)+','+str(y)+')' )
        states.append(state_list)
##        print state_list
        stateNames.append(name_list)

    default_r_value = -1
    R = {}
    Q = {}
    for y1 in range(10):
        for x1 in range(10):
            # and then
            r_dict = {}
            q_dict = {}
            for dy in range(-1,2):
                y2 = y1 + dy
                if y2!=y1 and y2>=0 and y2<=9:
                    r_dict[(x1,y2)] = default_r_value
                    q_dict[(x1,y2)] = 0
                
            for dx in range(-1,2):
                x2 = x1 + dx
                if x2!=x1 and x2>=0 and x2<=9:
                    r_dict[(x2,y1)] = default_r_value
                    q_dict[(x2,y1)] = 0
            R[(x1,y1)] = r_dict
            Q[(x1,y1)] = q_dict

    actions = [] # this will be filled by LoadFromMap()
    finish = (-1,-1)
    start = (-1,-1)
    
    def __init__(self, mapa=None, alpha=0.1, gamma=0.9):
        #print Map
        self.alpha = alpha
        self.gamma = gamma
        self.final_policy = {}
        if type(mapa) != type(None):
            self.mapa = mapa
            self.LoadFromMap(Map.Map(mapa, True))
            print "Loaded states from existing map"
            
        else:
            print "R:",self.R
            print "Q:",self.Q
            print "actions",self.actions
            self.R[self.stateB][self.stateC] = 100
            self.R[self.stateF][self.stateC] = 100

    def LoadFromMap(self,mapa):
        self.my_map = mapa
        
        # Generate self.actions
        for y in range(10):
            actions_list = []
            for x in range(10):
                if mapa.map[x][y] == 'S':
                    self.start = (x,y)
##                    print "start:",self.start
                if mapa.map[x][y] == 'F':
                    self.finish = (x,y)
                actions_list.append(self.GetActionsFrom(self.states[x][y]))
            self.actions.append(actions_list)
            
        # Set the values in the R table for finishing
        self.SetFinishRewards()
        self.Q[self.finish][self.finish] = 0

    def SetFinishRewards(self):
        actionsFromFinish = self.GetActionsFrom(self.finish, None, True)
##        print "Finish states:"
        for act in actionsFromFinish:
##            print act, self.finish
            self.R[act][self.finish] = 100
        

    def GetActionsFrom(self,(x,y), path=None, use_finish=False):
        acts = []
        
        if not use_finish and (x,y) == self.finish:
            acts.append(self.finish)
            return acts
        
##        Check left
        if x-1 >= 0 and self.my_map.map[x-1][y] != 'X':
            if path != None:
                if not (x-1,y) in path:
                    acts.append( (x-1,y) )
            else:
                acts.append( (x-1,y) )
##        Check up
        if y-1 >= 0 and self.my_map.map[x][y-1] != 'X':
            if path != None:
                if not (x,y-1) in path:
                    acts.append( (x,y-1) )
            else:
                acts.append( (x,y-1) )
##        Check right
        if x+1 < 10 and self.my_map.map[x+1][y] != 'X':
            if path != None:
                if not (x+1,y) in path:
                    acts.append( (x+1,y) )
            else:
                acts.append( (x+1,y) )
##        Check down
        if y+1 < 10 and self.my_map.map[x][y+1] != 'X':
            if path != None:
                if not (x,y+1) in path:
                    acts.append( (x,y+1) )
            else:
                acts.append( (x,y+1) )
        return acts
        
    
    def run(self, itr_count):
##        1. Set parameter , and environment reward matrix R 
##        2. Initialize matrix Q as zero matrix 
##        3. For each episode: Select random initial state
##            Do while not reach goal state o
##                Select one among all possible actions for the current state o 
##                Using this possible action, consider to go to the next state o 
##                Get maximum Q value of this next state based on all possible actions o 
##                Compute o Set the next state as the current state
        for i in range(itr_count):
            #print
            #print "iteration",i
			#state = self.start
            
            self.LoadFromMap(Map.Map(self.mapa, True))
            while True:
				rand_row = random.randint(0,9)
				rand_col = random.randint(0,9)
				if self.my_map.map[rand_row][rand_col] == '.':
					state = rand_row, rand_col
					break
            path = []
            path.append(state)
            
            exiting = False
            inf_loop_count = 0
            while state != self.finish and inf_loop_count < 100 and not exiting:
                inf_loop_count += 1
                
                #print state
				#get the available actions from the current state
                actionsFromState = self.GetActionsFrom(state,path)

                #print "actions from state:",actionsFromState
                
                if len(actionsFromState) == 0:
                    #print "Got stuck"
                    exiting = True
                    break

                action = random.choice(actionsFromState)
                
                ## Action outcome is set to deterministic in this example
                ## Transition probability is 1
                ## what happens when the transition is probabilistic?
                nextState = action ## data structure

                ## Using this possible action, consider to go to the next state
                q = self.getQ(state,action)
                
                maxQ = self.maxQ(nextState)
                r = self.getR(state,action)

                value = q + self.alpha * (r + (self.gamma * maxQ) - q)
                self.setQ(state,action,value)
                state = nextState
            if not exiting:
                pass
                #self.my_map.printMap()
            self.avgQvalue(i)

##  get maxQ from state
    def maxQ(self, s):                              ##    double maxQ(int s) {
        actionsFromState = self.GetActionsFrom(s)   ##        int[] actionsFromState = actions[s];
        maxValue = float('-inf')                    ##        double maxValue = Double.MIN_VALUE;
        for i in range(len(actionsFromState)):      ##        for (int i = 0; i < actionsFromState.length; i++) {
            nextState = actionsFromState[i]         ##            int nextState = actionsFromState[i];
            value = self.Q[s][nextState]            ##            double value = Q[s][nextState];
                                                    ## 
            if(value > maxValue):                   ##            if (value > maxValue)
                maxValue = value                    ##                maxValue = value;
                                                    ##        }
        return maxValue                             ##        return maxValue;
        
	
    def pickMaxQ(self, s):
		actionsFromState = self.GetActionsFrom(s)
		maxValue = float('-inf')  
		returnState = actionsFromState[0]
		for i in range(len(actionsFromState)):
			nextState = actionsFromState[i]
			value = self.Q[s][nextState]   
                                                
			if(value > maxValue):         
				maxValue = value
				returnState = nextState
		return returnState

##  get policy from state                               ##    // get policy from state
    def policy(self, s, path=None):                     ##    int policy(int state) {
        actionsFromState = self.GetActionsFrom(s,path)  ##        int[] actionsFromState = actions[state];
        maxValue = float('-inf')                        ##        double maxValue = Double.MIN_VALUE;   
        policyGotoState = s                             ##        int policyGotoState = state; // default goto self if not found
        for i in range(len(actionsFromState)):          ##        for (int i = 0; i < actionsFromState.length; i++) {
            nextState = actionsFromState[i]             ##            int nextState = actionsFromState[i];
            value = self.Q[s][nextState]                ##            double value = Q[state][nextState];
                                                        ##
            if value > maxValue:                        ##            if (value > maxValue) {
                maxValue = value                        ##                maxValue = value;
                policyGotoState = nextState             ##                policyGotoState = nextState;
                                                        ##            }
                                                        ##        }
        return policyGotoState                          ##        return policyGotoState;
    

    def getQ(self, s, a):
        return self.Q[s][a]

    def setQ(self, s, a, val):
        self.Q[s][a] = val

    def getR(self, s, a):
        return self.R[s][a]
	
	#print the average Q value over all actions
    def avgQvalue(self, epNum):
		#print "EPISODE NUMBER " + str(epNum)
		total = 0
		totalNum = 0
		for x in range(10):
			for y in range(10):
				for k in self.Q[(x,y)].keys():
					#print self.Q[(x,y)][k]
					total+= self.Q[(x,y)][k]
					totalNum+=1
		#print "AVG Q VALUE=> " + str(total/totalNum) + " NUM VALUES => " + str(totalNum)

    def printResult(self):
        print "Print result"
        for x in range(10):
            for y in range(10):
                print "out from " + self.stateNames[x][y] + ":  "
                string = ""
                for k in self.Q[(x,y)].keys():
                    string += ("({},{})={:.2f}\t").format( k[0],k[1],self.Q[(x,y)][k] )
                print string
##        for i in range(len(self.Q)):
##            print "out from " + self.stateNames[i] + ":  "
##            string = ""
##            for j in range(len(self.Q[i])):
##                string += ("{:.2f}\t").format( self.Q[i][j] )
##            print string

    def showPolicy(self):
        print "\nshowPolicy"
        for x in range(10):
            for y in range(10):
                from_ = self.states[x][y]
                to_ = self.policy(from_)
                self.final_policy[from_] = to_
                #print "from " + self.stateNames[from_[0]][from_[1]] + " goto " + self.stateNames[to_[0]][to_[1]]



    def followPolicy(self):
        print "Following Policy"
        count = 0
        state = self.start
        self.LoadFromMap(Map.Map(self.mapa, True))
        
        path = []
        path.append(state)

        while state != self.finish and count < 100:
            count += 1
            #state = self.final_policy[state]
            i = random.random() * 10
            prevState = state
			#if the policy is in the path, choose a random new state from the 
			#available options
            #print i
            """if(i>9) and self.final_policy[state] in path:
				#print "going rando!"
				actionsFromState = self.GetActionsFrom(state, path)
				if(len(actionsFromState)!=0):
					#print len(actionsFromState)
					state = self.policy(state, path)
					j = 0
					while((state in path)) and j<10:
						state = random.choice(actionsFromState)
						j+=1
					
					if(state in path):
						#print "Went back. " + str(count)
						state = self.pickMaxQ(prevState)
					
				else:
					state = self.policy(prevState, path)
					
            elif self.final_policy[state] in path:
				#print "Action already in path"
				actionsFromState = self.GetActionsFrom(state, path)
				if(len(actionsFromState)!=0):
					#print "Have options. Recalculating"
					state = self.policy(state, path)
					j = 0
					while((state in path)) and j<10:
						state = random.choice(actionsFromState)
						j+=1
					if(state in path):
						#print "Went back. Had options"
						state = self.pickMaxQ(prevState)
				#no unique positions you can move to, choose from all available ones
				else:
					#print "Action not in path, proceeding"
					actionsFromState = self.GetActionsFrom(state)
					if(len(actionsFromState)!=0):
						#print "Don't have options. Recalculating"
						state = self.policy(state, path)
						j = 0
						while((state in path)) and j<10:
							state = random.choice(actionsFromState)
							j+=1
						if(state in path):
							#print "Went back. Didn't have options"
							state = self.final_policy[prevState]
					else:
						state = self.pickMaxQ(prevState)
			#if the policy isn't in the path, but i is greater than 9, choose a random
			#policy from the path
            else:
				state = self.final_policy[state]  
			"""
            state = self.final_policy[state]
            if(state in path):
				actionsFromState = self.GetActionsFrom(prevState, path)
				#there are valid options
				if(len(actionsFromState)!=0):
					j = 0
					while((state in path)) and j<10:
						state = random.choice(actionsFromState)
						j+=1
				#otherwise, backtrack until there are valid options
				else:
					pastOptions = []
					if(i>9.5):
						state = self.pickMaxQ(prevState)
						
					else:
						while(len(actionsFromState)==0):
							prevState = path.pop()
							pastOptions.append(prevState)
							actionsFromState = self.GetActionsFrom(prevState, path)
							
						state = random.choice(actionsFromState)
						for item in range(len(pastOptions)):
							path.append(pastOptions[item])
					
            path.append(state)
            x,y = state
            if state != self.finish:
                self.my_map.map[x][y] = str(count%10)
            else:
				print "Done."
        self.my_map.printMap()

        
