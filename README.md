# NHL Player Spatial Analysis Scripts (ArcGIS Pro)

This repository contains two ArcGIS Pro Python scripts for performing spatial analysis on current NHL player data. Both scripts filter players based on country and position and converts physical attributes into metric units (height in cm, weight in kg).

---

## Contents

| Script                         | Description                                                                 |
|--------------------------------|-----------------------------------------------------------------------------|
| `NHLRosterScript_git.py`   | Filters and exports Sweden-born NHL forwards (RW, LW, C) as separate shapefiles with height and weight converted to metric units. |
| `NHLRosterScriptTool_git.py`    | Script tool for ArcGIS Pro that lets users select a country and position to create a filtered feature class, with height and weight converted to metric units. |


## Data Setup
1. Download or clone the repository.
2. Unzip the contents of both ZIP files into the `/data/` folder:
   - `nhlrosters.zip`
   - `Countries_WGS84.zip`
3. After extraction, your folder structure should look like this:

```your-repo/
├── data/
│ ├── nhlrosters.shp
│ └── Countries_WGS84.shp
├── scripts/
│ ├── nhl_forwards_by_country.py
│ └── nhl_player_filter_tool.py
├── README.md
```````

## Requirements

- ArcGIS Pro with Python 3.x
- ArcPy (included with ArcGIS Pro)
- Unzipped shapefiles in the `/data/` directory

---

## Script 1: `NHLRosterScript_git.py`
This standalone script:

- Filters NHL forwards (RW, LW, C) born in Sweden
- Creates a new shapefile for each position
- Converts and adds:
  - Height to **centimeters** from feet/inches
  - Weight to **kilograms** from pounds

**Note:** The country ("Sweden") is currently hardcoded. You can modify this in the script if needed.

**How to use:**
1. Ensure data files are unzipped into the data/ folder as described above.
2. Open the script (nhl_forwards_by_country.py) in ArcGIS Pro’s Python window or the ArcGIS Pro Python Command Prompt.
3. Check that the workspace path is correctly set in the script:
   ```python
   arcpy.env.workspace = "./data"
5. Run the script. It will output three new shapefiles (one for each forward position: RW, LW, C) in the same folder.

---

## Script 2: `NHLRosterScriptTool_git.py`
This script is designed to be added to a toolbox (.tbx) and used as a script tool within ArcGIS Pro. It:

- Prompts the user to select a country and player position
- Filters the NHL roster feature class based on these selections
- Creates a new output feature class
- Converts and adds:
  - Height to **centimeters** from feet/inches
  - Weight to **kilograms** from pounds

**How to use:**
- In ArcGIS Pro, create or open a toolbox (.tbx).
- Right-click the toolbox > Add > Script.
- Link it to nhl_player_filter_tool.py.
- Define the script parameters as needed (e.g., input feature classes, fields, output name).
- Run the tool from the toolbox and provide country/position selections when prompted.

