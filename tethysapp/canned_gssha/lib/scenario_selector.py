#Selects the closest scenario to the given parameters

class ScenarioSelector:
    dim = None
    scenarios = None
    nscen = None
    params = None
    maxmin = None
    
    def __init__(self, params, scenarios, maxmin = None):
        self.params = params
        self.scenarios = scenarios
        self.maxmin = maxmin
        self.dim = len(params)
        self.nscen = len(scenarios)
        if maxmin == None:
            self.populateMaxmin()
                    
    def populateMaxmin(self):
        maxmin = []
        for i in range(0, self.dim):
            minim = self.scenarios[i][0]
            maxim = self.scenarios[i][0]
            for j in range(1, self.nscen):
                value = self.scenarios[i][j]
                if value < minim:
                    minim = value
                if value > maxim:
                    maxim = value
            maxmin.append([minim, maxim])
        self.maxmin = maxmin

    def getClosest(self):
        minsqdist = None
        for j in range(0, self.nscen):
            sumsqdist = 0
            scenario = self.scenarios[j]
            for i in range(0, self.dim):
                minim = self.maxmin[i][0]
                maxim = self.maxmin[i][1]
                param = self.params[i]
                scenparam = scenario[i]
                if maxim > minim: #Non zero division
                    param_h = (param - minim) / float(maxim - minim)
                    scenparam_h = (scenparam - minim) / float(maxim - minim)
                    sqdist = (param_h - scenparam_h) ** 2
                else:
                    sqdist = 0
                sumsqdist = sumsqdist + sqdist
            #print str(sumsqdist)
            if minsqdist == None:
                minsqdist = sumsqdist
                closest = 0
            if sumsqdist < minsqdist:
                minsqdist = sumsqdist
                closest = j
        return closest


if __name__ == "__main__":
    ##==Usage======
    ## Input: instantiating the object: list of search parameters, scenarios, (optional) max and min for each parameter
    ## Output: getClosest() method provides the number of order of the closest scenario to the parameters
    ## Example:

    ''' Comment this line to toggle
    scenarios = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [6, 7, 8]]
    params = [4, 3, 2]

    ppp = ScenarioSelector(params, scenarios)

    '''

    scenarios = [[1, 2, 3], [2, 3, 4], [3, 4, 5], [4, 5, 6], [6, 7, 8]]
    params = [4, 3, 8]
    maxmin = [[1, 7], [1, 9], [2, 10]]

    ppp = ScenarioSelector(params, scenarios, maxmin)
    #'''

    order = ppp.getClosest()

    print(order)

    ##=============