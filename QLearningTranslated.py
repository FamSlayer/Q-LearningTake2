import random, decimal, 

class QLearning():

    #final DecimalFormat df = new DecimalFormat("#.##");
 
    ## path finding
    alpha = 0.1;
    gamma = 0.9;

    ## states A,B,C,D,E,F
    ## e.g. from A we can go to B or D
    ## from C we can only go to C 
    ## C is goal state, reward 100 when B->C or F->C
    ## 
    ## _______
    ## |A|B|C|
    ## |_____|
    ## |D|E|F|
    ## |_____|
    ##
    stateA = 0
    stateB = 1
    stateC = 2
    stateD = 3
    stateE = 4
    stateF = 5

    statesCount = 6
    states = [stateA,stateB,stateC,stateD,stateE,stateF]
 
    ## http://en.wikipedia.org/wiki/Q-learning
    ## http://people.revoledu.com/kardi/tutorial/ReinforcementLearning/Q-Learning.html
 
    ## Q(s,a)= Q(s,a) + alpha * (R(s,a) + gamma * Max(next state, all actions) - Q(s,a))
 
    ## int[][] R = new int[statesCount][statesCount]; ## reward lookup
    ## double[][] Q = new double[statesCount][statesCount]; ## Q learning
    R = []#[[0]*statesCount] * statesCount
    Q = []#[[0]*statesCount] * statesCount
    
    ## Just going to initialize all these values?
    for x in range(statesCount):
        l = [0] * statesCount
        l2 = [0] * statesCount
        R.append(l)
        Q.append(l2)
    #print "R:",R
    #print "Q:",Q
 
    actionsFromA = [ stateB, stateD ]
    actionsFromB = [ stateA, stateC, stateE ]
    actionsFromC = [ stateC ]
    actionsFromD = [ stateA, stateE ]
    actionsFromE = [ stateB, stateD, stateF ]
    actionsFromF = [ stateC, stateE ]
    actions = [ actionsFromA, actionsFromB, actionsFromC,
                actionsFromD, actionsFromE, actionsFromF ]

    #print "actions:",actions
    stateNames = [ "A", "B", "C", "D", "E", "F" ]
    
    def __init__(self):
        print "R:",self.R
        print "Q:",self.Q
        print "actions",self.actions
        self.R[self.stateB][self.stateC] = 100
        self.R[self.stateF][self.stateC] = 100


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
            print
            print "iteration",i
            state = random.randint(0,self.statesCount-1)
            print "starting from",state

            while state != self.stateC:

                print state
                actionsFromState = self.actions[state]
                index = random.randint(0,len(actionsFromState)-1)
                action = actionsFromState[index]

                ## Action outcome is set to deterministic in this example
                ## Transition probability is 1
                ## what happens when the transition is probabilistic?
                nextState = action ## data structure

                
                ## Using this possible action, consider to go to the next state
                q = self.getQ(state,action)
                
                maxQ = self.maxQ(nextState)
                r = self.getR(state,action)

                value = q + self.alpha * (r + self.gamma * maxQ - q)
                self.setQ(state,action,value)
                state = nextState

            print state

##  get maxQ from state
    def maxQ(self, s):                          ##    double maxQ(int s) {
        actionsFromState = self.actions[s]      ##        int[] actionsFromState = actions[s];
        maxValue = float('-inf')                ##        double maxValue = Double.MIN_VALUE;
        for i in range(len(actionsFromState)):  ##        for (int i = 0; i < actionsFromState.length; i++) {
            nextState = actionsFromState[i]     ##            int nextState = actionsFromState[i];
            value = self.Q[s][nextState]        ##            double value = Q[s][nextState];
                                                ## 
            if(value > maxValue):               ##            if (value > maxValue)
                maxValue = value                ##                maxValue = value;
                                                ##        }
        return maxValue                         ##        return maxValue;
        

##  get policy from state                       ##    // get policy from state
    def policy(self, state):                    ##    int policy(int state) {
        actionsFromState = self.actions[state]  ##        int[] actionsFromState = actions[state];
        maxValue = float('-inf')                ##        double maxValue = Double.MIN_VALUE;   
        policyGotoState = state                 ##        int policyGotoState = state; // default goto self if not found
        for i in range(len(actionsFromState)):  ##        for (int i = 0; i < actionsFromState.length; i++) {
            nextState = actionsFromState[i]     ##            int nextState = actionsFromState[i];
            value = self.Q[state][nextState]    ##            double value = Q[state][nextState];
                                                ##
            if value > maxValue:                ##            if (value > maxValue) {
                maxValue = value                ##                maxValue = value;
                policyGotoState = nextState     ##                policyGotoState = nextState;
                                                ##            }
                                                ##        }
        return policyGotoState                  ##        return policyGotoState;
    

    def getQ(self, s, a):
        return self.Q[s][a]

    def setQ(self, s, a, val):
        self.Q[s][a] = val

    def getR(self, s, a):
        return self.R[s][a]

    def printResult(self):
        print "Print result" 
        for i in range(len(self.Q)):
            print "out from " + self.stateNames[i] + ":  "
            string = ""
            for j in range(len(self.Q[i])):
                string += ("{:.2f}\t").format( self.Q[i][j] )
            print string

    def showPolicy(self):
        print "\nshowPolicy"
        for i in range(len(self.states)):
            from_ = self.states[i]
            to_ = self.policy(from_)
            print "from " + self.stateNames[from_] + " goto " + self.stateNames[to_]

   
