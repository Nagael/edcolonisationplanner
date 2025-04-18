from collections import Counter

import data

from_daftmav_to_edcp_dict = {
    "Orbital - Starport - Coriolis": "Coriolis",
    "Orbital - Starport - Asteroid Base": "Asteroid_Base",
    "Orbital - Starport - Ocellus": "Orbis_or_Ocellus",
    "Orbital - Starport - Orbis": "Orbis_or_Ocellus",
    "Orbital - Outpost - Commercial": "Commercial_Outpost",
    "Orbital - Outpost - Industrial": "Industrial_Outpost",
    "Orbital - Outpost - Criminal": "Criminal_Outpost",
    "Orbital - Outpost - Civilian": "Civilian_Outpost",
    "Orbital - Outpost - Scientific": "Scientific_Outpost",
    "Orbital - Outpost - Military": "Military_Outpost",
    "Orbital - Installation - Satellite": "Satellite",
    "Orbital - Installation - Comm Station": "Communication_Station",
    "Orbital - Installation - Space Farm": "Space_Farm",
    "Orbital - Installation - Pirate Base": "Pirate_Base",
    "Orbital - Installation - Mining Outpost": "Mining_Outpost",
    "Orbital - Installation - Relay Station": "Relay_Station",
    "Orbital - Installation - Military": "Military",
    "Orbital - Installation - Security Station": "Security_Station",
    "Orbital - Installation - Government": "Government",
    "Orbital - Installation - Medical": "Medical",
    "Orbital - Installation - Research Station": "Research_Station",
    "Orbital - Installation - Tourist": "Tourist",
    "Orbital - Installation - Space Bar": "Space_Bar",
    "Surface - Planetary Port - Outpost Civilian": "Civilian_Planetary_Outpost",
    "Surface - Planetary Port - Outpost Industrial": "Industrial_Planetary_Outpost",
    "Surface - Planetary Port - Outpost Scientific": "Scientific_Planetary_Outpost",
    "Surface - Planetary Port - Port": "Planetary_Port",
    "Surface - Settlement - Agriculture T1 S": "Small_Agricultural_Settlement",
    "Surface - Settlement - Agriculture T1 M": "Medium_Agricultural_Settlement",
    "Surface - Settlement - Agriculture T2 L": "Large_Agricultural_Settlement",
    "Surface - Settlement - Extraction T1 S": "Small_Extraction_Settlement",
    "Surface - Settlement - Extraction T1 M": "Medium_Extraction_Settlement",
    "Surface - Settlement - Extraction T2 L": "Large_Extraction_Settlement",
    "Surface - Settlement - Industrial T1 S": "Small_Industrial_Settlement",
    "Surface - Settlement - Industrial T1 M": "Medium_Industrial_Settlement",
    "Surface - Settlement - Industrial T2 L": "Large_Industrial_Settlement",
    "Surface - Settlement - Military T1 S": "Small_Military_Settlement",
    "Surface - Settlement - Military T1 M": "Medium_Military_Settlement",
    "Surface - Settlement - Military T2 L": "Large_Military_Settlement",
    "Surface - Settlement - Research Bio T1 S": "Small_Scientific_Settlement",
    "Surface - Settlement - Research Bio T1 M": "Medium_Scientific_Settlement",
    "Surface - Settlement - Research Bio T2 L": "Large_Scientific_Settlement",
    "Surface - Settlement - Tourism T1 S": "Small_Tourism_Settlement",
    "Surface - Settlement - Tourism T1 M": "Medium_Tourism_Settlement",
    "Surface - Settlement - Tourism T2 L": "Large_Tourism_Settlement",
    "Surface - Hub - Extraction": "Extraction_Hub",
    "Surface - Hub - Civilian": "Civilian_Hub",
    "Surface - Hub - Exploration": "Exploration_Hub",
    "Surface - Hub - Outpost": "Outpost_Hub",
    "Surface - Hub - Scientific": "Scientific_Hub",
    "Surface - Hub - Military": "Military_Hub",
    "Surface - Hub - Refinery": "Refinery_Hub",
    "Surface - Hub - High Tech": "High_Tech_Hub",
    "Surface - Hub - Industrial": "Industrial_Hub",
}

from_edcp_to_daftmav_dict = { edcp_name: daftmav_name
                              for daftmav_name, edcp_name in from_daftmav_to_edcp_dict.items() }

def from_daftmav_to_edcp(name):
    return from_daftmav_to_edcp_dict[name]

def from_edcp_to_daftmav(name):
    try:
        return from_edcp_to_daftmav_dict[name]
    except KeyError:
        return f"Unknown {name}"

def export_ordering(ordering):
    ordering = [ from_edcp_to_daftmav(line) for line in ordering ]
    return "\n".join(ordering)

def import_state(main_frame, text, with_system_name=False):
    lines = text.splitlines()
    for l in lines:
        l = l.strip()
    lines = [ l for l in lines if l != "" ]
    try:
        starting_point = 1 + lines.index("Construction")
    except ValueError:
        starting_point = 0
    try:
        converted = [ from_daftmav_to_edcp(line)
                      for line in lines[starting_point:] ]
    except KeyError as e:
        return f"Error: facility '{e}' unknown"
    if not converted:
        return "Error: no facilities found. Make sure you include the whole column"
    first_station = converted[0]
    facilities = [ name for name in converted[1:]
                   if not data.is_port(data.all_buildings[name]) ]
    facilities = Counter(facilities)
    ports = [ name for name in converted[1:]
              if data.is_port(data.all_buildings[name]) ]

    if starting_point > 3 and with_system_name:
        main_frame.system_name_var.set(lines[starting_point-4])
    main_frame.clear_result()
    main_frame.choose_first_station_var.set(False)
    main_frame.clear_already_built()
    main_frame.set_first_station(first_station)
    for name, nb in facilities.items():
        row = main_frame.get_row_for_building(name, include_first_station=False)
        row.already_present_var.set(nb)
    for name in ports:
        row = main_frame.add_empty_building_row(result_building=data.to_printable(name))
        row.already_present_var.set(1)

