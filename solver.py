from pyscipopt import Model
import sys
import os

import data
from data import all_buildings, all_scores, all_categories, all_slots

if getattr(sys, "frozen", False) and hasattr(sys, '_MEIPASS'):
    pass #I'm pretty sure pyscipopt's library has its solver inside it (I'll have to check later after using pyinstaller)
else:
    pass

def convert_maybe(variable, default=None):
    value = variable.get()
    if value != "": return int(value)
    return default

def solve(main_frame):
    #requirements
    M = 10000

    # Get data from the Entry widgets
    orbitalfacilityslots = main_frame.available_slots_currently_vars["space"].get()
    groundfacilityslots = main_frame.available_slots_currently_vars["ground"].get()
    asteroidslots = main_frame.available_slots_currently_vars["asteroid"].get()
    maximize = data.from_printable(main_frame.maximizeinput.get())
    initial_T2points = main_frame.T2points_variable.get()
    initial_T3points = main_frame.T3points_variable.get()
    choose_first_station = main_frame.choose_first_station_var.get()

    if not choose_first_station and data.from_printable(main_frame.building_input[0].name_var.get()) not in all_buildings:
        main_frame.print_result("Error: pick your first station")
        return None

    nb_ports_already_present = sum(row.already_present for row in main_frame.building_input if row.is_port)
    max_nb_ports = orbitalfacilityslots + groundfacilityslots + nb_ports_already_present

    #problem
    model = Model('NON-LINEAR')
    direction = 'minimize' if maximize == "construction_cost" else 'maximize'
    objective = model.addVar("objective", vtype="C")

    #create all the variables for each of the facilities
    all_vars = {} # for each building name, the variables that decide how many will be BUILT
    first_station_vars = {} # for each building name, a boolean variable for the first station
    all_values = {} # for each building name, the expressions that give how many will be in TOTAL (=all_var + already_present)
    port_vars = {} # for ports: for each port name, kth variable is 1 if the k-th port built is of this type
    for n, b in all_buildings.items():
        if not data.is_port(b):
            all_vars[n] = model.addVar(n, vtype="I", lb=0)
        else:
            # orbital and planetary ports, subject to cost increase
            # Speculation for how construction points increase based on
            # https://old.reddit.com/r/EliteDangerous/comments/1jfm0y6/psa_construction_points_costs_triple_after_third/
            port_vars[n] = [ model.addVar(f"{n}_{k+1}", vtype='B') for k in range(max_nb_ports) ]
            all_vars[n] = sum(port_vars[n])
        all_values[n] = all_vars[n]

    if choose_first_station:
        for i in all_categories["First Station"]:
            first_station_vars[i] = model.addVar("first station binary variable for " + i, vtype='B')
            all_values[i] = all_values[i] + first_station_vars[i]

        T2_benefit = all_buildings[i].T2points
        if T2_benefit != "port" and T2_benefit > 0:
            initial_T2points = initial_T2points + T2_benefit * first_station_vars[i]
        T3_benefit = all_buildings[i].T3points
        if T3_benefit != "port" and T3_benefit > 0:
            initial_T3points = initial_T3points + T3_benefit * first_station_vars[i]

        if not main_frame.first_station_cb_coriolis_var.get():
            model.addCons(first_station_vars["Coriolis"] == 0)
        if not main_frame.first_station_cb_asteroid_var.get():
            model.addCons(first_station_vars["Asteroid_Base"] == 0)
        if not main_frame.first_station_cb_orbis_var.get():
            model.addCons(first_station_vars["Orbis_or_Ocellus"] == 0)
        model.addCons(sum(first_station_vars.values()) == 1)

    if not main_frame.criminalinput.get():
        model.addCons(all_vars["Pirate_Base"] == 0)
        model.addCons(all_vars["Criminal_Outpost"] == 0)
        if "Criminal_Outpost" in first_station_vars:
            model.addCons(all_vars["Criminal_Outpost"] == 0)

    # number of slots
    usedslots = {}
    for slot in ("space", "ground"):
        usedslots[slot] = sum(all_vars[building_name]
                                     for building_name, building in all_buildings.items()
                                     if building.slot == slot)

    #number of slots
    model.addCons(all_vars["Asteroid_Base"] <= asteroidslots)
    model.addCons(usedslots["space"] <= orbitalfacilityslots)
    model.addCons(usedslots["ground"] <= groundfacilityslots)

    # Include already present buildings as constants in all_values[...]
    for row in main_frame.building_input:
        if not row.valid:
            continue
        if row.first_station and choose_first_station:
            continue
        building_name = row.building_name
        already_present = row.already_present
        if already_present:
            if building_name != 'Let_the_program_choose_for_me':
                all_values[building_name] = all_values[building_name] + already_present

                if building_name in ["Pirate_Base", "Criminal_Outpost"] and not main_frame.criminalinput.get():
                    main_frame.print_result("Error: criminal outpost or pirate base already present, but you do not want criminal outposts to be built")
                    return False

    # Already present ports can not be built
    for port_var in port_vars.values():
        for k in range(nb_ports_already_present):
            model.addCons(port_var[k] == 0)

    # Constraints on the total number of facilities in the system
    for row in main_frame.building_input:
        if not row.valid:
            continue
        building_name = row.building_name
        at_least = convert_maybe(row.at_least_var)
        if at_least is not None:
            model.addCons(all_values[building_name] >= at_least)
        at_most = convert_maybe(row.at_most_var)
        if at_most is not None:
            model.addCons(all_values[building_name] <= at_most)

    # Consistency constraints for the port variables
    for k in range(max_nb_ports):
        # Only one port can be k-th
        model.addCons(sum(port_var[k] for port_var in port_vars.values()) <= 1)
        if k > nb_ports_already_present:
            # No k-th port if there was no (k-1)-th port
            model.addCons(sum(port_var[k] for port_var in port_vars.values()) <= sum(port_var[k-1] for port_var in port_vars.values()))

    # Computing system scores
    systemscores = {}
    for score in data.base_scores:
        if score != "construction_cost":
            systemscores[score] = sum(getattr(building, score) * all_values[building_name]
                                             for building_name, building in all_buildings.items())
        else:
            # Do not count already present buildings for construction cost, but count the chosen first station
            systemscores[score] = sum(getattr(building, score) * all_vars[building_name]
                                             for building_name, building in all_buildings.items())
            if choose_first_station:
                systemscores[score] += sum(getattr(all_buildings[building_name], score) * (1 + all_buildings[building_name].first_station_offset) * var
                                                  for building_name, var in first_station_vars.items())

    for score in data.compound_scores:
        systemscores[score] = data.compute_compound_score(score, systemscores)

    # Objective function
    if maximize in systemscores:
        model.addCons(systemscores[maximize] == objective)
    else:
        main_frame.print_result(f"Error: One or more inputs are blank: select an objective to optimize")
        return False

    # Constraints on minimum and maximum scores
    for score in all_scores:
        minvalue = convert_maybe(main_frame.minvars[score])
        maxvalue = convert_maybe(main_frame.maxvars[score])
        if minvalue is not None:
            model.addCons(systemscores[score] >= minvalue)
        if maxvalue is not None:
            model.addCons(systemscores[score] <= maxvalue)


    # Constraints on the construction points
    # Needs to be satisfied for each port, to prevent counting T2 points of last Coriolis station for building the first Ocellus ;)

    non_port_T2_cp = sum( building.T2points * all_vars[name]
                          for name, building in all_buildings.items()
                          if not data.is_port(building) ) + initial_T2points
    non_port_T3_cp = sum( building.T3points * all_vars[name]
                          for name, building in all_buildings.items()
                          if not data.is_port(building) ) + initial_T3points

    for port_idx in range(max_nb_ports):
        portsT2constructionpoints = sum( sum(port_var[k] for name, port_var in port_vars.items()
                                             if all_buildings[name].T2points == "port") * max(3, 2*k+1)
                                         for k in range(port_idx+1))
        portsT3constructionpoints = sum( sum(port_var[k] for name, port_var in port_vars.items()
                                             if all_buildings[name].T3points == "port") * max(6, 6*k)
                                         for k in range(port_idx+1))
        T3points_from_T2ports = sum( sum(port_var[k] * all_buildings[name].T3points
                                              for name, port_var in port_vars.items()
                                              if all_buildings[name].T3points != "port")
                                          for k in range(port_idx+1))
        model.addCons(- portsT2constructionpoints + non_port_T2_cp >= 0)
        model.addCons(T3points_from_T2ports - portsT3constructionpoints + non_port_T3_cp >= 0)

    finalT2points = - portsT2constructionpoints + non_port_T2_cp
    finalT3points = T3points_from_T2ports - portsT3constructionpoints + non_port_T3_cp

    #sort out dependencies for facilities
    indicator_dependency_variables = {}
    ap_counter = 1
    for target_name, target_building in all_buildings.items():
        if target_building.dependencies:
            deps = tuple(target_building.dependencies)
            if  deps not in indicator_dependency_variables:
                individual_variables = [ (name, model.addVar(f"indic {name}", vtype="B"))
                                         for name in target_building.dependencies ]
                for name, bool_var in individual_variables:
                    model.addCons(all_values[name] <= M * bool_var)
                    model.addCons(all_values[name] >= bool_var)
                if len(target_building.dependencies) == 1:
                    any_positive = individual_variables[0][1]
                else:
                    any_positive = model.addVar(f"any_positive {ap_counter}", vtype="B")
                    ap_counter += 1
                    for name, bool_var in individual_variables:
                        model.addCons(any_positive >= bool_var)
                    model.addCons(any_positive <= M * sum(bool_var for name, bool_var in individual_variables))
                indicator_dependency_variables[deps] = any_positive

            model.addCons(all_values[target_name] <= M * indicator_dependency_variables[deps])

    # Solve the problem
    model.setObjective(objective, sense=direction)
    model.optimize()
    sol = model.getBestSol()
    if model.getStatus() == "infeasible":
        main_frame.print_result("Error: There is no possible system arrangement that can fit the conditions you have specified")
        return False

    main_frame.clear_result()
    for building_name in all_buildings.keys():
        value = round(sol[all_vars[building_name]])
        if value <= 0:
            continue
        result_row = main_frame.get_row_for_building(building_name)
        result_row.set_build_result(value)

    for score in all_scores:
        main_frame.resultvars[score].set(round(sol[systemscores[score]]))

    main_frame.T2points_variable_after.set(round(sol[finalT2points]))
    main_frame.T3points_variable_after.set(round(sol[finalT3points]))

    main_frame.available_slots_after_vars["space"].set(orbitalfacilityslots - round(sol[usedslots["space"]]))
    main_frame.available_slots_after_vars["ground"].set(groundfacilityslots - round(sol[usedslots["ground"]]))
    main_frame.available_slots_after_vars["asteroid"].set(asteroidslots - round(sol[all_vars["Asteroid_Base"]]))

    port_types = set()
    port_order = []
    for port_index in range(nb_ports_already_present, max_nb_ports):
        for port_name, port_var in port_vars.items():
            if round(sol[port_var[port_index]]) >= 1:
                port_types.add(port_name)
                port_order.append(port_name)
    if len(port_types) > 1:
        main_frame.set_port_ordering(port_order)

    if choose_first_station:
        for fs_name, fs_var in first_station_vars.items():
            if round(sol[fs_var]) == 1:
                main_frame.building_input[0].name_var.set(data.to_printable(fs_name))
                main_frame.building_input[0].set_build_result(1)

    return True
