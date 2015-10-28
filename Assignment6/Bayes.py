import sys
import getopt


class Bayes(object):
    pol = {}
    smo = {}
    can = {}
    dys = {}
    xra = {}

    def __init__(self):
        self.pol = {'low': 0.9}
        self.smo = {'true': 0.3}
        self.can = {'lt': 0.03, 'lf': 0.001, 'ht': 0.05, 'hf': 0.02}
        self.xra = {'ct': 0.9, 'cf': 0.2}
        self.dys = {'ct': 0.65, 'cf': 0.3}

    def setPrior(self, node, value):
        if node is 'P':
            self.pol['low'] = value
        elif node is 'S':
            self.smo['true'] = value
        else:
            print "Failed to set value, prior cause unrecognised."


def knot(var):
    return 1 - var


def trueVar(var):
    if var is 'P':
        return 'pol'
    if var is 'S':
        return 'smo'
    if var is 'C':
        return 'can'
    if var is 'D':
        return 'dys'
    if var is 'X':
        return 'xra'


def sumValue(matrix):
    total = 0
    for row in range(2):
        for column in range(2):
            total += matrix[row][column]
    return total


def calcMarginal(var, bnet):
    # true
    if var is 'p':
        P = bnet.pol['low']
        return P
    elif var is 's':
        S = bnet.smo['true']
        return S
    elif var is 'c':
        CPS = bnet.can['lt'] * calcMarginal('p', bnet) * calcMarginal('s', bnet)
        ChPS = bnet.can['ht'] * calcMarginal('~p', bnet) * calcMarginal('s', bnet)
        CPnS = bnet.can['lf'] * calcMarginal('p', bnet) * calcMarginal('~s', bnet)
        ChPnS = bnet.can['hf'] * calcMarginal('~p', bnet) * calcMarginal('~s', bnet)
        return CPS + ChPS + CPnS + ChPnS
    elif var is 'd':
        DC = bnet.dys['ct'] * calcMarginal('c', bnet)
        DnC = bnet.dys['cf'] * calcMarginal('~c', bnet)
        return DC + DnC
    elif var is 'x':
        XC = bnet.xra['ct'] * calcMarginal('c', bnet)
        XnC = bnet.xra['cf'] * calcMarginal('~c', bnet)
        return XC + XnC
    # false
    elif var is '~p':
        nP = knot(bnet.pol['low'])
        return nP
    elif var is '~s':
        nS = knot(bnet.smo['true'])
        return nS
    elif var is '~c':
        nCPS = knot(bnet.can['lt']) * calcMarginal('p', bnet) * calcMarginal('s', bnet)
        nChPS = knot(bnet.can['ht']) * calcMarginal('~p', bnet) * calcMarginal('s', bnet)
        nCPnS = knot(bnet.can['lf']) * calcMarginal('p', bnet) * calcMarginal('~s', bnet)
        nChPnS = knot(bnet.can['hf']) * calcMarginal('~p', bnet) * calcMarginal('~s', bnet)
        return nCPS + nChPS + nCPnS + nChPnS
    elif var is '~d':
        nDC = knot(bnet.dys['ct']) * sumValue(calcMarginal('c', bnet))
        nDnC = knot(bnet.dys['cf']) * sumValue(calcMarginal('~c', bnet))
        return nDC + nDnC
    elif var is '~x':
        nXC = knot(bnet.xra['ct']) * sumValue(calcMarginal('c', bnet))
        nXnC = knot(bnet.xra['cf']) * sumValue(calcMarginal('~c', bnet))
        return nXC + nXnC
    # distributions
    elif var is 'P':
        P = bnet.pol['low']
        nP = knot(bnet.pol['low'])
        return [P, nP]
    elif var is 'S':
        S = bnet.smo['true']
        nS = knot(bnet.smo['true'])
        return [S, nS]
    elif var is 'C':
        CPS = bnet.can['lt'] * calcMarginal('p', bnet) * calcMarginal('s', bnet)
        nCPS = knot(bnet.can['lt']) * calcMarginal('p', bnet) * calcMarginal('s', bnet)
        ChPS = bnet.can['ht'] * calcMarginal('~p', bnet) * calcMarginal('s', bnet)
        nChPS = knot(bnet.can['ht']) * calcMarginal('~p', bnet) * calcMarginal('s', bnet)
        CPnS = bnet.can['lf'] * calcMarginal('p', bnet) * calcMarginal('~s', bnet)
        nCPnS = knot(bnet.can['lf']) * calcMarginal('p', bnet) * calcMarginal('~s', bnet)
        ChPnS = bnet.can['hf'] * calcMarginal('~p', bnet) * calcMarginal('~s', bnet)
        nChPnS = knot(bnet.can['hf']) * calcMarginal('~p', bnet) * calcMarginal('~s', bnet)
        return [CPS + ChPS + CPnS + ChPnS, nCPS + nChPS + nCPnS + nChPnS]
    elif var is 'D':
        DC = bnet.dys['ct'] * sumValue(calcMarginal('c', bnet))
        DnC = bnet.dys['cf'] * sumValue(calcMarginal('~c', bnet))
        nDC = knot(bnet.dys['ct']) * sumValue(calcMarginal('c', bnet))
        nDnC = knot(bnet.dys['cf']) * sumValue(calcMarginal('~c', bnet))
        return [DC + DnC, nDC + nDnC]
    elif var is 'X':
        XC = bnet.xra['ct'] * sumValue(calcMarginal('c', bnet))
        XnC = bnet.xra['cf'] * sumValue(calcMarginal('~c', bnet))
        nXC = knot(bnet.xra['ct']) * sumValue(calcMarginal('c', bnet))
        nXnC = knot(bnet.xra['cf']) * sumValue(calcMarginal('~c', bnet))
        return [XC + XnC, nXC + nXnC]
    else:
        return "calcMarginal() has failed, variable not recognised and/or handled."


def isThere(l, x):
    if l.count(x) > 0:
        return True
    else:
        return False


def samesame(contents):
    if contents['p'] and contents['~p']:
        return True
    if contents['s'] and contents['~s']:
        return True
    if contents['c'] and contents['~c']:
        return True
    if contents['d'] and contents['~d']:
        return True
    if contents['x'] and contents['~x']:
        return True


def calcJoint(args, bnet):
    # case sanitizing
    if (isThere(args, 'p') or isThere(args, '~p') or isThere(args, 's') or isThere(args, '~s') or isThere(args, 'c') or isThere(args, '~c') or isThere(args, 'd') or isThere(args, '~d') or isThere(args, 'x') or isThere(args, '~x')) and (isThere(args, 'P') or isThere(args, 'S') or isThere(args, 'C') or isThere(args, 'D') or isThere(args, 'X')):
        print "calcJoint() has failed, cannot calculate distribution and specific values at once."
        return "Do not mix capital and lower case letters!"
    # distributions
    elif isThere(args, 'P') or isThere(args, 'S') or isThere(args, 'C') or isThere(args, 'D') or isThere(args, 'X'):
        contains = {'P': False, 'S': False, 'C': False, 'D': False, 'X': False}
        po = []
        sm = []
        ca = []
        dy = []
        xr = []
        if isThere(args, 'P'):
            contains['P'] = True
            po = [bnet.pol['low'], bnet.pol['high']]
        if isThere(args, 'S'):
            contains['S'] = True
            sm = [bnet.smo['true'], bnet.smo['false']]
        if isThere(args, 'C'):
            contains['C'] = True
            ca = [bnet.can['lt'], bnet.can['lf'], bnet.can['ht'], bnet.can['hf']]
        if isThere(args, 'D'):
            contains['D'] = True
            dy = [bnet.dys['ct'], bnet.smo['cf']]
        if isThere(args, 'X'):
            contains['X'] = True
            xr = [bnet.xra['ct'], bnet.xra['cf']]
        # !!!! There are no distribution calculations yet !!!!

    # specific variables
    else:
        contains = {'p': False, 's': False, 'c': False, 'd': False, 'x': False, '~p': False, '~s': False, '~c': False, '~d': False, '~x': False}
        if isThere(args, 'p'):
            contains['p'] = True
        if isThere(args, 's'):
            contains['s'] = True
        if isThere(args, 'c'):
            contains['c'] = True
        if isThere(args, 'd'):
            contains['d'] = True
        if isThere(args, 'x'):
            contains['x'] = True
        if isThere(args, '~p'):
            contains['~p'] = True
        if isThere(args, '~s'):
            contains['~s'] = True
        if isThere(args, '~c'):
            contains['~c'] = True
        if isThere(args, '~d'):
            contains['~d'] = True
        if isThere(args, '~x'):
            contains['~x'] = True

        if samesame(contains):
            print "The probability of something jointly happening and not happening is zero."
            return 0

        multi = 1
        po = 0
        sm = 0
        ca = 0
        dy = 0
        xr = 0
        # Pollution
        if contains['p']:
            po = bnet.pol['low']
            multi = multi * po
        if contains['~p']:
            po = knot(bnet.pol['low'])
            multi *= po
        # Smoker
        if contains['s']:
            sm = bnet.smo['true']
            multi = multi * sm
        if contains['~s']:
            sm = knot(bnet.smo['true'])
            multi *= sm
        # Cancer
        if contains['c']:
            if contains['p'] and contains['s']:
                ca = bnet.can['lt']
                multi = multi * ca
            elif contains['~p'] and contains ['~s']:
                ca = bnet.can['hf']
                multi = multi * ca
            elif contains['p'] and contains ['~s']:
                ca = bnet.can['lf']
                multi = multi * ca
            elif contains['~p'] and contains ['s']:
                ca = bnet.can['ht']
                multi = multi * ca
            elif contains['p']:
                ca = bnet.can['lt'] + bnet.can['lf']
                multi = multi * ca
            elif contains['~p']:
                ca = bnet.can['ht'] + bnet.can['hf']
                multi = multi * ca
            elif contains['s']:
                ca = bnet.can['ht'] + bnet.can['lt']
                multi = multi * ca
            elif contains['~s']:
                ca = bnet.can['hf'] + bnet.can['lf']
                multi = multi * ca
            else:
                ca = bnet.can['hf'] + bnet.can['lf'] + bnet.can['ht'] + bnet.can['lt']
                multi = multi * ca
        if contains['~c']:
            if contains['p'] and contains['s']:
                ca = knot(bnet.can['lt'])
                multi *= ca
            elif contains['~p'] and contains ['~s']:
                ca = knot(bnet.can['hf'])
                multi *= ca
            elif contains['p'] and contains ['~s']:
                ca = knot(bnet.can['lf'])
                multi *= ca
            elif contains['~p'] and contains ['s']:
                ca = knot(bnet.can['ht'])
                multi *= ca
            elif contains['p']:
                ca = knot(bnet.can['lt']) + knot(bnet.can['lf'])
                multi *= ca
            elif contains['~p']:
                ca = knot(bnet.can['ht']) + knot(bnet.can['hf'])
                multi *= ca
            elif contains['s']:
                ca = knot(bnet.can['ht']) + knot(bnet.can['lt'])
                multi *= ca
            elif contains['~s']:
                ca = knot(bnet.can['hf']) + knot(bnet.can['lf'])
                multi *= ca
            else:
                ca = knot(bnet.can['hf']) + knot(bnet.can['lf']) + knot(bnet.can['ht']) + knot(bnet.can['lt'])
                multi *= ca
        # !!!! everything below here needs absentee-cancer clauses !!!!
        # Dyspnoea
        if contains['d']:
            if contains['c']:
                dy = bnet.dys['ct']
                multi *= dy
            elif contains['~c']:
                dy = bnet.dys['cf']
                multi *= dy
            else:
                dy = bnet.dys['ct'] + bnet.dys['cf']
                multi *= dy
        if contains['~d']:
            if contains['c']:
                dy = knot(bnet.dys['ct'])
                multi *= dy
            elif contains['~c']:
                dy = knot(bnet.dys['cf'])
                multi *= dy
            else:
                dy = knot(bnet.dys['ct']) + knot(bnet.dys['cf'])
                multi *= dy
        # X-ray
        if contains['x']:
            if contains['c']:
                xr = bnet.xra['ct']
                multi *= xr
            elif contains['~c']:
                xr = bnet.xra['cf']
                multi *= xr
            else:
                xr = bnet.xra['ct'] + bnet.xra['cf']
                multi *= xr
        if contains['~x']:
            if contains['c']:
                xr = knot(bnet.xra['ct'])
                multi *= xr
            elif contains['~c']:
                xr = knot(bnet.xra['cf'])
                multi *= xr
            else:
                xr = knot(bnet.xra['ct']) + knot(bnet.xra['cf'])
                multi *= xr
        return multi


def calcConditional(variable, condition, bnet):
    if variable is condition:
        print "The chance of an event given the event is always 100%."
        return 1
    # pollution chances given _
    if variable is 'p':
        if condition is 's':
            return bnet.pol['low']
        elif condition is 'c':
            return (calcConditional(condition,variable,bnet) * bnet.pol['low']) / ((calcConditional(condition, variable, bnet) * bnet.pol['low']) + (calcConditional(condition, '~' + variable, bnet) + knot(bnet.pol['low'])))
        elif condition is 'd':
            return bnet.dys['cf'] + (bnet.dys['ct'] * calcConditional('c', variable, bnet))
        elif condition is 'x':
            return bnet.xra['cf'] + (bnet.xra['ct'] * calcConditional('c', variable, bnet))
    # smoking chances given _
    if variable is 's':
        if condition is 'p':
            return bnet.smo['true']
        elif condition is 'c':
            return (bnet.pol['low'] * bnet.can['lt']) + (bnet.pol['high'] * bnet.can['ht'])
        elif condition is 'd':
            
        elif condition is 'x':

    # cancer chances given _
    if variable is 'c':
        if condition is 'p':
            return (bnet.smo['true'] * bnet.can['lt']) + (knot(bnet.smo['true']) * bnet.can['lf'])
    # dyspnoea chances given _
    if variable is 'd':
        return 0
    # x-ray chances given _
    if variable is 'x':
        return 0


def main():
    net = Bayes()

    try:
        opts, args = getopt.getopt(sys.argv[1:], "m:g:j:p:")
    except getopt.GetoptError as err:
        # print help information and exit:
        print "You done goofed."
        print str(err)  # will print something like "option -a not recognized"
        sys.exit(2)
    for o, a in opts:
        if o in ("-p"):
            # set prior
            print "flag", o
            print "args", a
            print a[0]
            print float(a[1:])
            net.setPrior(a[0], float(a[1:]))
        elif o in ("-m"):
            # calculate the marginal probability | DONE
            print "flag", o
            print "args", a
            print type(a)
            # !!!! make a pretty print for the distribution matrix !!!!
            print calcMarginal(a, net)
        elif o in ("-g"):
            # calculate the conditional probability
            print "flag", o
            print "args", a
            print type(a)
            '''
            you may want to parse a here and pass the left of | and right of | as arguments to calcConditional
            '''
            p = a.find("|")
            print a[:p]
            print a[p + 1:]
            print calcConditional(a[:p], a[p+1:], net)
        elif o in ("-j"):
            # calculate the joint probability
            print "flag", o
            print "args", a
            b = list(a)
            while b.count('~') > 0:
                i = b.index('~')
                b[i + 1] = '~' + b[i + 1]
                b.remove('~')
            print calcJoint(b, net)
        else:
            assert False, "unhandled option"

            # ...


if __name__ == "__main__":
    main()
