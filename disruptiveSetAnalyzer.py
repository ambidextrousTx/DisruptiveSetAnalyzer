"""
 distuptiveSetAnalyzer.py
 Divide a given set into two sets: solved and hard
 Empirically determine delta_solved, delta_hard, and delta_tied
 Granularity: lemma (100 points to plot)
 Plots: between two uncorrelated systems that both do well (see Diana's dendrogram)

 LRE JPaper: CLLS
 Ravi S Sinha
 Mar 2011
 University of North Texas
"""

from collections import defaultdict
import matplotlib as M
M.use('Agg') # Makes it work for ssh [no X server]
import matplotlib.pyplot as P

def readRawData():
    rawFile = open('./first_comparison.csv', 'r') # CHANGE THIS to point to your CSV
    for line in rawFile:
        items = line.rstrip().split(',')
        system = items[1].replace('"', '')
        lexelt = items[2].replace('"', '')
        if 'sys' not in system:
            score = eval(items[3])
            # To comply with the 0-10 range
            data[system][lexelt] = score * 10
    rawFile.close()
        
def getRangeOfValues(system):
    max = 0
    min = 100
    for lexelt in data[system].keys():
        if data[system][lexelt] > max:
            max = data[system][lexelt]
            ranges[system]['maxlexelt'] = lexelt
        if data[system][lexelt] < min:
            min = data[system][lexelt]
            ranges[system]['minlexelt'] = lexelt

    ranges[system]['min'] = min
    ranges[system]['max'] = max

def getRange():
    for system in ranges.keys():
        print "System %s has min value %s (%s) and max value %s (%s)" % (system, str(ranges[system]['min']), ranges[system]['minlexelt'], str(ranges[system]['max']), ranges[system]['maxlexelt'])

def get_absolute_min_max():
    min = 999
    max = 0
    for system in ranges.keys():
        curr_min = ranges[system]['min']
        curr_max = ranges[system]['max']
        if curr_min < min:
            min = curr_min
        if curr_max > max:
            max = curr_max

    return (min, max)

def divideIntoSetsIndividual():
    min, max = get_absolute_min_max()
    DELTA_SOLVED = (max - min) * 2 / 3
    DELTA_HARD = (max - min) * 1 / 3
    DELTA_TIED = (max - min) / 5
    
    sets = open('setsIndividual.txt', 'w')
    for system in data.keys():
        sets.write('---\n' + system + ': \n---\n')
        hard = []
        solved = []
        for lexelt in data[system].keys():
            if data[system][lexelt] < DELTA_HARD:
                hard.append(lexelt)
            if data[system][lexelt] > DELTA_SOLVED:
                solved.append(lexelt)

        sets.write('Hard: ')
        for h in hard:
            sets.write(h + ' ')
        sets.write('\n\n')

        sets.write('Solved: ')
        for s in solved:
            sets.write(s + ' ')
        sets.write('\n')

        sets.write('\n--- --- ---\n')

    sets.close()
    
def divideIntoSetsPairs():
    min, max = get_absolute_min_max()
    DELTA_SOLVED = (max - min) * 2 / 3
    DELTA_HARD = (max - min) * 1 / 3
    DELTA_TIED = (max - min) / 5
    setsP = open('setsPairs.txt', 'w')
    erledigt = defaultdict(dict)

    for system1 in data.keys():
        for system2 in data.keys():
            erledigt[system1][system2] = 0

    for system1 in data.keys():
        for system2 in data.keys():
            if system1 != system2 and not erledigt[system1][system2]:
                erledigt[system1][system2] = 1
                erledigt[system2][system1] = 1
                twoEngineSolved = []
                twoEngineHard = []
                tied = []
                disruptiveI = []
                disruptiveII = []
            
                setsP.write('---\n' + system1 + ' and ' + system2 + ': \n---\n')
                
                for k in data[system1].keys():
                    if data[system1][k] > DELTA_SOLVED and data[system2][k] > DELTA_SOLVED:
                        twoEngineSolved.append(k)

                    elif data[system1][k] < DELTA_HARD and data[system2][k] < DELTA_HARD:
                        twoEngineHard.append(k)

                    elif abs(data[system1][k] - data[system2][k]) < DELTA_TIED:
                        tied.append(k)

                    elif data[system1][k] > data[system2][k]:
                        disruptiveI.append(k)
            
                    elif data[system1][k] < data[system2][k]:
                        disruptiveII.append(k)

                setsP.write('Two-engine solved: ')
                for x in twoEngineSolved:
                    setsP.write(x + ' ')
                setsP.write('\n\n')

                setsP.write('Two-engine hard: ')
                for x in twoEngineHard:
                    setsP.write(x + ' ')
                setsP.write('\n\n')

                setsP.write('Tied: ')
                for x in tied:
                    setsP.write(x + ' ')
                setsP.write('\n\n')

                setsP.write('Disruptive ' + system1 + ': ')
                for x in disruptiveI:
                    setsP.write(x + ' ')
                setsP.write('\n\n')

                setsP.write('Disruptive ' + system2 + ': ')
                for x in disruptiveII:
                    setsP.write(x + ' ')
                setsP.write('\n')

                setsP.write('\n--- --- ---\n')

    setsP.close()

def generatePlots():
    erledigt = defaultdict(dict)
    min, max = get_absolute_min_max()
    DELTA_SOLVED = (max - min) * 2 / 3
    DELTA_HARD = (max - min) * 1 / 3
    DELTA_TIED = (max - min) / 5

    for system1 in data.keys():
        for system2 in data.keys():
            erledigt[system1][system2] = 0

    for system1 in data.keys():
        for system2 in data.keys():
            if system1 != system2 and not erledigt[system1][system2]:
                erledigt[system1][system2] = 1
                erledigt[system2][system1] = 1
                sys1Scores = []
                sys2Scores = []
                sys1Labels = []
                sys2Labels = []
                for s in data[system1].keys():
                    sys1Scores.append(data[system1][s]) # The value
                    sys1Labels.append(s) # The lemmas

                for s in data[system2].keys():
                    sys2Scores.append(data[system2][s]) # The value
                    sys2Labels.append(s) # The lemmas

                # Check: # of items = 101
                # print(len(sys1Scores))
                # print(len(sys2Scores))

                # 'o' for points, default = line
                P.plot(sys1Scores, sys2Scores, 'ro')

                for i in xrange(len(sys1Labels)):
                    point_label = sys1Labels[i]
                    point_x = sys1Scores[i]
                    point_y = sys2Scores[i]
                    P.annotate(point_label, xy = (point_x, point_y), xytext = (-10, 10), textcoords = 'offset points', ha = 'right', va = 'bottom', bbox = dict(boxstyle = 'round,pad=0.5', fc = 'yellow', alpha = 0.5), arrowprops = dict(arrowstyle = '->', connectionstyle = 'arc3,rad=0'))

                P.xlabel(system1)
                P.ylabel(system2)
                P.title('Disruptive Set Plot')
                P.text(DELTA_SOLVED + 1, DELTA_SOLVED + 1, '2-Engine-solved')
                P.text(DELTA_HARD - 2, DELTA_HARD - 2, '2-Engine-hard')
                P.text((DELTA_SOLVED + DELTA_HARD)/2, (DELTA_SOLVED + DELTA_HARD)/2, 'Tied', rotation = 45)
                P.text(DELTA_SOLVED, (DELTA_SOLVED + DELTA_HARD) / 2 - 2, 'DisruptiveI')
                P.text(DELTA_HARD - 2, DELTA_SOLVED, 'DisruptiveII')

                xs1 = [0, DELTA_HARD, DELTA_HARD]
                ys1 = [DELTA_HARD, DELTA_HARD, 0]
                xs2 = [DELTA_SOLVED, DELTA_SOLVED, max]
                ys2 = [max, DELTA_SOLVED, DELTA_SOLVED]
                xs3 = [DELTA_HARD - DELTA_TIED/2, DELTA_SOLVED]
                ys3 = [DELTA_HARD, DELTA_SOLVED + DELTA_TIED/2]
                xs4 = [DELTA_SOLVED + DELTA_TIED/2, DELTA_HARD]
                ys4 = [DELTA_SOLVED, DELTA_HARD - DELTA_TIED/2]

                # The lines
                P.plot(xs1, ys1, color = 'g', linewidth = 2.0)
                P.plot(xs2, ys2, color = 'g', linewidth = 2.0)
                P.plot(xs3, ys3, color = 'g', linewidth = 2.0)
                P.plot(xs4, ys4, color = 'g', linewidth = 2.0)

                f = system1 + '_' + system2 + '.png'
                P.savefig(f)    
                P.close()   
                    
                    


# Constants and globals
# Experimental values
# CHANGE THESE to suit your needs
# DELTA_SOLVED = 6
# DELTA_HARD = 3
# DELTA_TIED = 2

data = defaultdict(dict)
ranges = defaultdict(dict)
sets = defaultdict(list)

# Start

readRawData()
for system in data.keys():
    getRangeOfValues(system)

print "Range of values"
getRange()

print "Dividing into sets for each system, see setsIndividual.txt"
divideIntoSetsIndividual()

print "Dividing into sets for each pair, see setsPairs.txt"
divideIntoSetsPairs()

print "Generating disruptive set plots, see all .png files"
generatePlots()










