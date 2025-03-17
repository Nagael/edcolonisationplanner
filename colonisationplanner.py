import pulp
import re
#requirements
M = 10000
inittier2conpoints = 0
inittier3conpoints = 0
minorbis = 0
minasteroidbase = 0
mincoriolis = 0
mincommericaloutpost = 0
minindustrialoutpost = 0
mincriminaloutpost = 0
mincivilianoutpost = 0
minscientificoutpost = 0
minmilitaryoutpost = 0
maxpiratebase = 0
maxcriminaloutpost = 0
maximize = input("Input what you want to maximize (initial population increase, maximum population increase, security, tech level, wealth, standard of living, development level): ")
mininitialpopulationincrease = int(input("Input the minimum initial population increase: "))
minmaxpopulationincrease = int(input("Input the minimum maximum population increase: "))
minsecurity = int(input("Input the minimum security: "))
mintechlevel = int(input("Input the minimum tech level: "))
minwealth = int(input("Input the minimum wealth: "))
minstandardofliving = int(input("Input the minimum standard of living: "))
mindevelopmentlevel = int(input("Input the minimum development level: "))
orbitalfacilityslots = int(input("Input the number of orbital facility slots you have (including the first station): "))
groundfacilityslots = int(input("Input the number of ground facility slots you have: "))
asteroidslots = int(input("Input the number of orbital facility slots that can hold asteroid bases: "))
idk2 = input("Do you want contraband stations in your system? (pirate base, criminal outpost) (yes/no) ")
if idk2 == "yes":
    maxpiratebase = M
    maxcriminaloutpost = M
idk = input("What is your first station? (Type the station name with no capital letters, e.g. scientific outpost, coriolis, asteroid base) ")
if idk == "orbis" or idk == "ocellus":
    minorbis = 1
    inittier3conpoints += 6
elif idk == "asteroid base":
    minasteroidbase  = 1
    inittier2conpoints += 3
elif idk == "coriolis":
    mincoriolis = 1
    inittier2conpoints += 3
elif idk == "commerical outpost":
    mincommericaloutpost = 1
elif idk == "industrial outpost":
    minindustrialoutpost = 1
elif idk == "criminal outpost":
    mincriminaloutpost = 1
elif idk == "civilian outpost":
    mincivilianoutpost = 1
elif idk == "scientific outpost":
    minscientificoutpost = 1
elif idk == "military outpost":
    minmilitaryoutpost = 1
#create all the variables for each of the facilities
#orbital facilities
#note that min. industrial outpost is 1
coriolis = pulp.LpVariable('coriolis', lowBound = mincoriolis, cat='Integer')
orbis = pulp.LpVariable('orbis', lowBound = minorbis, cat='Integer')
commercialoutpost = pulp.LpVariable('commercialoutpost', lowBound = mincommericaloutpost, cat='Integer')
industrialoutpost = pulp.LpVariable('industrialoutpost', lowBound = minindustrialoutpost, cat='Integer')
civilianoutpost = pulp.LpVariable('civilianoutpost', lowBound = mincivilianoutpost, cat='Integer')
scientificoutpost = pulp.LpVariable('scientificoutpost', lowBound = minscientificoutpost, cat='Integer')
militaryoutpost = pulp.LpVariable('militaryoutpost', lowBound = minmilitaryoutpost, cat='Integer')
satellite = pulp.LpVariable('satellite', lowBound = 0, cat='Integer')
communicationstation = pulp.LpVariable('communicationstation', lowBound = 0, cat='Integer')
spacefarm = pulp.LpVariable('spacefarm', lowBound = 0, cat='Integer')
miningoutpost = pulp.LpVariable('miningoutpost', lowBound = 0, cat='Integer')
relaystation = pulp.LpVariable('relaystation', lowBound = 0, cat='Integer')
military = pulp.LpVariable('military', lowBound = 0, cat='Integer')
securitystation = pulp.LpVariable('securitystation', lowBound = 0, cat='Integer')
government = pulp.LpVariable('government', lowBound = 0, cat='Integer')
medical = pulp.LpVariable('medical', lowBound = 0, cat='Integer')
researchstation = pulp.LpVariable('researchstation', lowBound = 0, cat='Integer')
tourist = pulp.LpVariable('tourist', lowBound = 0, cat='Integer')
bar = pulp.LpVariable('bar', lowBound = 0, cat='Integer')
asteroidbase = pulp.LpVariable('asteroidbase', lowBound = minasteroidbase, upBound = asteroidslots, cat='Integer')
criminaloutpost = pulp.LpVariable('criminaloutpost', lowBound = mincriminaloutpost, upBound = maxcriminaloutpost, cat='Integer')
piratebase = pulp.LpVariable('piratebase', lowBound = 0, upBound = maxpiratebase, cat='Integer')
#ground facilities
civilianplanetaryoutpost = pulp.LpVariable('civilianplanetaryoutpost', lowBound = 0, cat='Integer')
industrialplanetaryoutpost = pulp.LpVariable('industrialplanetaryoutpost', lowBound = 0, cat='Integer')
scientificplanetaryoutpost = pulp.LpVariable('scientificplanetaryoutpost', lowBound = 0, cat='Integer')
planetaryport = pulp.LpVariable('planetaryport', lowBound = 0, cat='Integer')
smallagriculturalsettlement = pulp.LpVariable('smallagriculturalsettlement', lowBound = 0, cat='Integer')
mediumagriculturalsettlement = pulp.LpVariable('mediumagriculturalsettlement', lowBound = 0, cat='Integer')
largeagriculturalsettlement = pulp.LpVariable('largeagriculturalsettlement', lowBound = 0, cat='Integer')
smallextractionsettlement = pulp.LpVariable('smallextractionsettlement', lowBound = 0, cat='Integer')
mediumextractionsettlement = pulp.LpVariable('mediumextractionsettlement', lowBound = 0, cat='Integer')
largeextractionsettlement = pulp.LpVariable('largeextractionsettlement', lowBound = 0, cat='Integer')
smallindustrialsettlement = pulp.LpVariable('smallindustrialsettlement', lowBound = 0, cat='Integer')
mediumindustrialsettlement = pulp.LpVariable('mediumindustrialsettlement', lowBound = 0, cat='Integer')
largeindustrialsettlement = pulp.LpVariable('largeindustrialsettlement', lowBound = 0, cat='Integer')
smallmilitarysettlement = pulp.LpVariable('smallmilitarysettlement', lowBound = 0, cat='Integer')
mediummilitarysettlement = pulp.LpVariable('mediummilitarysettlement', lowBound = 0, cat='Integer')
largemilitarysettlement = pulp.LpVariable('largemilitarysettlement', lowBound = 0, cat='Integer')
smallscientificsettlement = pulp.LpVariable('smallscientificsettlement', lowBound = 0, cat='Integer')
mediumscientificsettlement = pulp.LpVariable('mediumscientificsettlement', lowBound = 0, cat='Integer')
largescientificsettlement = pulp.LpVariable('largescientificsettlement', lowBound = 0, cat='Integer')
smalltourismsettlement = pulp.LpVariable('smalltourismsettlement', lowBound = 0, cat='Integer')
mediumtourismsettlement = pulp.LpVariable('mediumtourismsettlement', lowBound = 0, cat='Integer')
largetourismsettlement = pulp.LpVariable('largetourismsettlement', lowBound = 0, cat='Integer')
extractionhub = pulp.LpVariable('extractionhub', lowBound = 0, cat='Integer')
civilianhub = pulp.LpVariable('civilianhub', lowBound = 0, cat='Integer')
explorationhub = pulp.LpVariable('explorationhub', lowBound = 0, cat='Integer')
outposthub = pulp.LpVariable('outposthub', lowBound = 0, cat='Integer')
scientifichub = pulp.LpVariable('scientifichub', lowBound = 0, cat='Integer')
militaryhub = pulp.LpVariable('militaryhub', lowBound = 0, cat='Integer')
refineryhub = pulp.LpVariable('refineryhub', lowBound = 0, cat='Integer')
hightechhub = pulp.LpVariable('hightechhub', lowBound = 0, cat='Integer')
industrialhub = pulp.LpVariable('industrialhub', lowBound = 0, cat='Integer')
#problem
prob = pulp.LpProblem("optimal_system_colonization_layout", pulp.LpMaximize)
#objective function
if maximize == "initial population increase":
    prob += (5 * orbis) + (coriolis) + (scientificoutpost) + (militaryoutpost) + (10 * planetaryport) + (2 * civilianplanetaryoutpost) + (industrialplanetaryoutpost) + (scientificplanetaryoutpost) + (asteroidbase), "initial population increase"
elif maximize == "maximum population increase":
    prob += (orbis) + (10 * planetaryport) >= minmaxpopulationincrease, "maximum population increase"
elif maximize == "security":
    prob += (8 * securitystation) + (6 * military) + (2 * militaryoutpost) + (2 * government) + (communicationstation) + (relaystation) + (-1 * commercialoutpost) + (-1 * civilianoutpost) + (-2 * coriolis) + (-2 * bar) + (-3 * orbis) + (-3 * tourist) + (10 * militaryhub) + (6 * largemilitarysettlement) + (4 * mediummilitarysettlement) + (2 * smallmilitarysettlement) + (-1 * industrialplanetaryoutpost) + (-1 * scientificplanetaryoutpost) + (-1 * smalltourismsettlement) + (-1 * mediumtourismsettlement) + (-1 * largetourismsettlement) + (-1 * refineryhub) + (-1 * explorationhub) + (-2 * civilianplanetaryoutpost) + (-2 * hightechhub) + (-2 * outposthub) + (-3 * planetaryport) + (-3 * civilianhub) + (-1 * asteroidbase) + (-4 * piratebase) + (-2 * criminaloutpost), "security"
elif maximize == "tech level":
    prob += (8 * researchstation) + (6 * orbis) + (3 * communicationstation) + (3 * scientificoutpost) + (3 * industrialoutpost) + (3 * medical) + (coriolis) + (10 * hightechhub) + (10 * largescientificsettlement) + (10 * scientifichub) + (6 * explorationhub) + (6 * mediumscientificsettlement) + (5 * scientificplanetaryoutpost) + (5 * planetaryport) + (3 * refineryhub) + (3 * smallscientificsettlement) + (3 * industrialhub) + (largeextractionsettlement) + (3 * asteroidbase), "tech level"
elif maximize == "wealth":
    prob += (7 * orbis) + (6 * tourist) + (3 * miningoutpost) + (2 * coriolis) + (2 * commercialoutpost) + (2 * bar) + (civilianoutpost) + (satellite) + (10 * extractionhub) + (7 * largeextractionsettlement) + (5 * planetaryport) + (5 * mediumextractionsettlement) + (5 * largetourismsettlement) + (5 * refineryhub) + (5 * industrialhub) + (2 * industrialplanetaryoutpost) + (2 * smallextractionsettlement) + (2 * largeindustrialsettlement) + (2 * mediumtourismsettlement) + (smalltourismsettlement) + (-2 * hightechhub) + (5 * asteroidbase) + (3 * piratebase) + (2 * criminaloutpost), "wealth"
elif maximize == "standard of living":
    prob += (6 * government) + (5 * orbis) + (5 * medical) + (5 * commercialoutpost) + (5 * spacefarm) + (3 * coriolis) + (3 * securitystation) + (3 * bar) + (civilianoutpost) + (satellite) + (-2 * miningoutpost) + (10 * largeagriculturalsettlement) + (6 * planetaryport) + (6 * mediumagriculturalsettlement) + (3 * civilianplanetaryoutpost) + (3 * outposthub) + (3 * civilianhub) + (3 * smallagriculturalsettlement) + (-2 * refineryhub) + (-2 * largeextractionsettlement) + (-4 * industrialhub) + (-4 * extractionhub) + (-4 * asteroidbase), "standard of living"
elif maximize == "development level":
    prob += (8 * orbis) + (2 * government) + (2 * coriolis) + (2 * securitystation) + (2 * researchstation) + (2 * industrialoutpost) + (2 * tourist) + (spacefarm) + (civilianoutpost) + (satellite) + (relaystation) + (10 * planetaryport) + (8 * largeindustrialsettlement) + (7 * refineryhub) + (5 * mediumindustrialsettlement) + (2 * outposthub) + (2 * civilianhub) + (2 * industrialhub) + (2 * extractionhub) + (2 * largescientificsettlement) + (2 * explorationhub) + (2 * largemilitarysettlement) + (2 * smallindustrialsettlement) + (mediumscientificsettlement) + (scientificplanetaryoutpost) + (smallscientificsettlement) + (7 * asteroidbase), "development level"
#minimum stats
prob += (5 * orbis) + (coriolis) + (scientificoutpost) + (militaryoutpost) + (10 * planetaryport) + (2 * civilianplanetaryoutpost) + (industrialplanetaryoutpost) + (scientificplanetaryoutpost) + (asteroidbase) >= mininitialpopulationincrease, "minimum initial population increase"
prob += (orbis) + (10 * planetaryport) >= minmaxpopulationincrease, "minimum maximum population increase"
prob += (8 * securitystation) + (6 * military) + (2 * militaryoutpost) + (2 * government) + (communicationstation) + (relaystation) + (-1 * commercialoutpost) + (-1 * civilianoutpost) + (-2 * coriolis) + (-2 * bar) + (-3 * orbis) + (-3 * tourist) + (10 * militaryhub) + (6 * largemilitarysettlement) + (4 * mediummilitarysettlement) + (2 * smallmilitarysettlement) + (-1 * industrialplanetaryoutpost) + (-1 * scientificplanetaryoutpost) + (-1 * smalltourismsettlement) + (-1 * mediumtourismsettlement) + (-1 * largetourismsettlement) + (-1 * refineryhub) + (-1 * explorationhub) + (-2 * civilianplanetaryoutpost) + (-2 * hightechhub) + (-2 * outposthub) + (-3 * planetaryport) + (-3 * civilianhub) + (-1 * asteroidbase) + (-4 * piratebase) + (-2 * criminaloutpost) >= minsecurity, "minimum security"
prob += (8 * researchstation) + (6 * orbis) + (3 * communicationstation) + (3 * scientificoutpost) + (3 * industrialoutpost) + (3 * medical) + (coriolis) + (10 * hightechhub) + (10 * largescientificsettlement) + (10 * scientifichub) + (6 * explorationhub) + (6 * mediumscientificsettlement) + (5 * scientificplanetaryoutpost) + (5 * planetaryport) + (3 * refineryhub) + (3 * smallscientificsettlement) + (3 * industrialhub) + (largeextractionsettlement) + (3 * asteroidbase) >= mintechlevel, "minimum tech level"
prob += (7 * orbis) + (6 * tourist) + (3 * miningoutpost) + (2 * coriolis) + (2 * commercialoutpost) + (2 * bar) + (civilianoutpost) + (satellite) + (10 * extractionhub) + (7 * largeextractionsettlement) + (5 * planetaryport) + (5 * mediumextractionsettlement) + (5 * largetourismsettlement) + (5 * refineryhub) + (5 * industrialhub) + (2 * industrialplanetaryoutpost) + (2 * smallextractionsettlement) + (2 * largeindustrialsettlement) + (2 * mediumtourismsettlement) + (smalltourismsettlement) + (-2 * hightechhub) + (5 * asteroidbase) + (3 * piratebase) + (2 * criminaloutpost) >= minwealth, "minimum wealth"
prob += (6 * government) + (5 * orbis) + (5 * medical) + (5 * commercialoutpost) + (5 * spacefarm) + (3 * coriolis) + (3 * securitystation) + (3 * bar) + (civilianoutpost) + (satellite) + (-2 * miningoutpost) + (10 * largeagriculturalsettlement) + (6 * planetaryport) + (6 * mediumagriculturalsettlement) + (3 * civilianplanetaryoutpost) + (3 * outposthub) + (3 * civilianhub) + (3 * smallagriculturalsettlement) + (-2 * refineryhub) + (-2 * largeextractionsettlement) + (-4 * industrialhub) + (-4 * extractionhub) + (-4 * asteroidbase) >= minstandardofliving, "minimum standard of living"
prob += (8 * orbis) + (2 * government) + (2 * coriolis) + (2 * securitystation) + (2 * researchstation) + (2 * industrialoutpost) + (2 * tourist) + (spacefarm) + (civilianoutpost) + (satellite) + (relaystation) + (10 * planetaryport) + (8 * largeindustrialsettlement) + (7 * refineryhub) + (5 * mediumindustrialsettlement) + (2 * outposthub) + (2 * civilianhub) + (2 * industrialhub) + (2 * extractionhub) + (2 * largescientificsettlement) + (2 * explorationhub) + (2 * largemilitarysettlement) + (2 * smallindustrialsettlement) + (mediumscientificsettlement) + (scientificplanetaryoutpost) + (smallscientificsettlement) + (7 * asteroidbase) >= mindevelopmentlevel, "minimum development level"
#number of slots
prob += coriolis + orbis + commercialoutpost + industrialoutpost + civilianoutpost + scientificoutpost + militaryoutpost + satellite + communicationstation + spacefarm + miningoutpost + relaystation + military + securitystation + government + medical + researchstation + tourist + bar + asteroidbase + criminaloutpost + piratebase == orbitalfacilityslots, "orbital facility slots"
prob += civilianplanetaryoutpost + industrialplanetaryoutpost + scientificplanetaryoutpost + planetaryport + smallagriculturalsettlement + mediumagriculturalsettlement + largeagriculturalsettlement + smallextractionsettlement + mediumextractionsettlement + largeextractionsettlement + smallindustrialsettlement + mediumindustrialsettlement + largeindustrialsettlement + smallmilitarysettlement + mediummilitarysettlement + largemilitarysettlement + smallscientificsettlement + mediumscientificsettlement + largescientificsettlement + smalltourismsettlement + mediumtourismsettlement + largetourismsettlement + extractionhub + civilianhub + explorationhub + outposthub + scientifichub + militaryhub + refineryhub + hightechhub + industrialhub == groundfacilityslots, "ground facility slots"
#construction points
prob += (industrialoutpost) + (spacefarm) + (civilianoutpost) + (satellite) + (relaystation) + (commercialoutpost) + (miningoutpost) + (communicationstation) + (scientificoutpost) + (militaryoutpost) + (mediumindustrialsettlement) + (smallindustrialsettlement) + (scientificplanetaryoutpost) + (mediumagriculturalsettlement) + (civilianplanetaryoutpost) + (smallagriculturalsettlement) + (mediummilitarysettlement) + (smallmilitarysettlement) + (industrialplanetaryoutpost) + (mediumextractionsettlement) + (smallextractionsettlement) + (-3 * coriolis) + (-1 * government) + (-1 * securitystation) + (-1 * researchstation) + (-1 * tourist) + (-1 * medical) + (-1 * bar) + (-1 * military) + (-1 * largeindustrialsettlement) + (-1 * largescientificsettlement) + (-1 * largemilitarysettlement) + (-1 * largeagriculturalsettlement) + (-1 * largeextractionsettlement) + (-1 * largetourismsettlement) + (-1 * refineryhub) + (-1 * outposthub) + (-1 * civilianhub) + (-1 * industrialhub) + (-1 * extractionhub) + (-1 * explorationhub) + (-1 * mediumscientificsettlement) + (-1 * smallscientificsettlement) + (-1 * hightechhub) + (-1 * scientifichub) + (-1 * militaryhub) + (-1 * mediumtourismsettlement) + (-1 * smalltourismsettlement) + inittier2conpoints + piratebase + criminaloutpost + (-3 * asteroidbase) >= 0, "tier 2 construction points"
prob += (coriolis) + (government) + (securitystation) + (researchstation) + (tourist) + (medical) + (bar) + (military) + (2 * largeindustrialsettlement) + (2 * largescientificsettlement) + (2 * largemilitarysettlement) + (2 * largeagriculturalsettlement) + (2 * largeextractionsettlement) + (2 * largetourismsettlement) + (refineryhub) + (outposthub) + (civilianhub) + (industrialhub) + (extractionhub) + (explorationhub) + (mediumscientificsettlement) + (smallscientificsettlement) + (hightechhub) + (scientifichub) + (militaryhub) + (mediumtourismsettlement) + (smalltourismsettlement) + (-6 * orbis) + (-6 * planetaryport) + inittier3conpoints + asteroidbase >= 0, "tier 3 construction points"
#sort out dependencies for facilities
b1 = pulp.LpVariable("b1", cat="Binary")
b2 = pulp.LpVariable("b2", cat="Binary")
b3 = pulp.LpVariable("b3", cat="Binary")
prob += smalltourismsettlement <= M * b1
prob += smalltourismsettlement >= b1
prob += mediumtourismsettlement <= M * b2
prob += mediumtourismsettlement >= b2
prob += largetourismsettlement <= M * b3
prob += largetourismsettlement >= b3
any_positive1 = pulp.LpVariable("any_positive1", cat="Binary")
prob += any_positive1 >= b1
prob += any_positive1 >= b2
prob += any_positive1 >= b3
prob += any_positive1 <= M * (b1 + b2 + b3)
prob += tourist <= M * any_positive1
b4 = pulp.LpVariable("b4", cat="Binary")
b5 = pulp.LpVariable("b5", cat="Binary")
b6 = pulp.LpVariable("b6", cat="Binary")
prob += smallscientificsettlement <= M * b4
prob += smallscientificsettlement >= b4
prob += mediumscientificsettlement <= M * b5
prob += mediumscientificsettlement >= b5
prob += largescientificsettlement <= M * b6
prob += largescientificsettlement >= b6
any_positive2 = pulp.LpVariable("any_positive2", cat="Binary")
prob += any_positive2 >= b4
prob += any_positive2 >= b5
prob += any_positive2 >= b6
prob += any_positive2 <= M * (b4 + b5 + b6)
prob += researchstation <= M * any_positive2
b7 = pulp.LpVariable("b7", cat="Binary")
b8 = pulp.LpVariable("b8", cat="Binary")
b9 = pulp.LpVariable("b9", cat="Binary")
prob += smallmilitarysettlement <= M * b7
prob += smallmilitarysettlement >= b7
prob += mediummilitarysettlement <= M * b8
prob += mediummilitarysettlement >= b8
prob += largemilitarysettlement <= M * b9
prob += largemilitarysettlement >= b9
any_positive3 = pulp.LpVariable("any_positive3", cat="Binary")
prob += any_positive3 >= b7
prob += any_positive3 >= b8
prob += any_positive3 >= b9
prob += any_positive3 <= M * (b7 + b8 + b9)
prob += military <= M * any_positive3
b10 = pulp.LpVariable("b10", cat="Binary")
prob += relaystation <= M * b10
prob += relaystation >= b10
prob += securitystation <= M * b10
b11 = pulp.LpVariable("b11", cat="Binary")
prob += spacefarm <= M * b11
prob += spacefarm >= b11
prob += outposthub <= M * b11
b12 = pulp.LpVariable("b12", cat="Binary")
b13 = pulp.LpVariable("b13", cat="Binary")
b14 = pulp.LpVariable("b14", cat="Binary")
prob += smallextractionsettlement <= M * b12
prob += smallextractionsettlement >= b12
prob += mediumextractionsettlement <= M * b13
prob += mediumextractionsettlement >= b13
prob += largeextractionsettlement <= M * b14
prob += largeextractionsettlement >= b14
any_positive4 = pulp.LpVariable("any_positive4", cat="Binary")
prob += any_positive4 >= b12
prob += any_positive4 >= b13
prob += any_positive4 >= b14
prob += any_positive4 <= M * (b12 + b13 + b14)
prob += extractionhub <= M * any_positive4
b15 = pulp.LpVariable("b15", cat="Binary")
b16 = pulp.LpVariable("b16", cat="Binary")
b17 = pulp.LpVariable("b17", cat="Binary")
prob += smallagriculturalsettlement <= M * b15
prob += smallagriculturalsettlement >= b15
prob += mediumagriculturalsettlement <= M * b16
prob += mediumagriculturalsettlement >= b16
prob += largeagriculturalsettlement <= M * b17
prob += largeagriculturalsettlement >= b17
any_positive5 = pulp.LpVariable("any_positive5", cat="Binary")
prob += any_positive5 >= b15
prob += any_positive5 >= b16
prob += any_positive5 >= b17
prob += any_positive5 <= M * (b15 + b16 + b17)
prob += civilianhub <= M * any_positive5
b18 = pulp.LpVariable("b18", cat="Binary")
prob += miningoutpost <= M * b18
prob += miningoutpost >= b18
prob += industrialhub <= M * b18
b19 = pulp.LpVariable("b19", cat="Binary")
prob += military <= M * b19
prob += military >= b19
prob += militaryhub <= M * b19
b20 = pulp.LpVariable("b20", cat="Binary")
prob += satellite <= M * b20
prob += satellite >= b20
prob += smalltourismsettlement <= M * b20
prob += mediumtourismsettlement <= M * b20
prob += largetourismsettlement <= M * b20
b21 = pulp.LpVariable("b21", cat="Binary")
prob += communicationstation <= M * b21
prob += communicationstation >= b21
prob += explorationhub <= M * b21
#solve
prob.solve()
print("Status:", pulp.LpStatus[prob.status])
for v in prob.variables():
    if v.name != "__dummy":
        if v.varValue > 0 and not bool(re.fullmatch(r"b\d+", v.name)) and not bool(re.fullmatch(r"any_positive\d+", v.name)):
            if v.name == "orbis":
                print("orbis/ocellus =", v.varValue)
            else:
                print(v.name, "=", v.varValue)
print("Total initial population increase: " + str(pulp.value((5 * orbis) + (coriolis) + (scientificoutpost) + (militaryoutpost) + (10 * planetaryport) + (2 * civilianplanetaryoutpost) + (industrialplanetaryoutpost) + (scientificplanetaryoutpost) + (asteroidbase))))
print("Total maximum population increase: " + str(pulp.value((orbis) + (10 * planetaryport))))
print("Total security: " + str(pulp.value((8 * securitystation) + (6 * military) + (2 * militaryoutpost) + (2 * government) + (communicationstation) + (relaystation) + (-1 * commercialoutpost) + (-1 * civilianoutpost) + (-2 * coriolis) + (-2 * bar) + (-3 * orbis) + (-3 * tourist) + (10 * militaryhub) + (6 * largemilitarysettlement) + (4 * mediummilitarysettlement) + (2 * smallmilitarysettlement) + (-1 * industrialplanetaryoutpost) + (-1 * scientificplanetaryoutpost) + (-1 * smalltourismsettlement) + (-1 * mediumtourismsettlement) + (-1 * largetourismsettlement) + (-1 * refineryhub) + (-1 * explorationhub) + (-2 * civilianplanetaryoutpost) + (-2 * hightechhub) + (-2 * outposthub) + (-3 * planetaryport) + (-3 * civilianhub) + (-1 * asteroidbase) + (-4 * piratebase) + (-2 * criminaloutpost))))
print("Total tech level: " + str(pulp.value((8 * researchstation) + (6 * orbis) + (3 * communicationstation) + (3 * scientificoutpost) + (3 * industrialoutpost) + (3 * medical) + (coriolis) + (10 * hightechhub) + (10 * largescientificsettlement) + (10 * scientifichub) + (6 * explorationhub) + (6 * mediumscientificsettlement) + (5 * scientificplanetaryoutpost) + (5 * planetaryport) + (3 * refineryhub) + (3 * smallscientificsettlement) + (3 * industrialhub) + (largeextractionsettlement) + (3 * asteroidbase))))
print("Total wealth: " + str(pulp.value((7 * orbis) + (6 * tourist) + (3 * miningoutpost) + (2 * coriolis) + (2 * commercialoutpost) + (2 * bar) + (civilianoutpost) + (satellite) + (10 * extractionhub) + (7 * largeextractionsettlement) + (5 * planetaryport) + (5 * mediumextractionsettlement) + (5 * largetourismsettlement) + (5 * refineryhub) + (5 * industrialhub) + (2 * industrialplanetaryoutpost) + (2 * smallextractionsettlement) + (2 * largeindustrialsettlement) + (2 * mediumtourismsettlement) + (smalltourismsettlement) + (-2 * hightechhub) + (5 * asteroidbase) + (3 * piratebase) + (2 * criminaloutpost))))
print("Total standard of living: " + str(pulp.value((6 * government) + (5 * orbis) + (5 * medical) + (5 * commercialoutpost) + (5 * spacefarm) + (3 * coriolis) + (3 * securitystation) + (3 * bar) + (civilianoutpost) + (satellite) + (-2 * miningoutpost) + (10 * largeagriculturalsettlement) + (6 * planetaryport) + (6 * mediumagriculturalsettlement) + (3 * civilianplanetaryoutpost) + (3 * outposthub) + (3 * civilianhub) + (3 * smallagriculturalsettlement) + (-2 * refineryhub) + (-2 * largeextractionsettlement) + (-4 * industrialhub) + (-4 * extractionhub) + (-4 * asteroidbase))))
print("Total development level: " + str(pulp.value((8 * orbis) + (2 * government) + (2 * coriolis) + (2 * securitystation) + (2 * researchstation) + (2 * industrialoutpost) + (2 * tourist) + (spacefarm) + (civilianoutpost) + (satellite) + (relaystation) + (10 * planetaryport) + (8 * largeindustrialsettlement) + (7 * refineryhub) + (5 * mediumindustrialsettlement) + (2 * outposthub) + (2 * civilianhub) + (2 * industrialhub) + (2 * extractionhub) + (2 * largescientificsettlement) + (2 * explorationhub) + (2 * largemilitarysettlement) + (2 * smallindustrialsettlement) + (mediumscientificsettlement) + (scientificplanetaryoutpost) + (smallscientificsettlement) + (7 * asteroidbase))))