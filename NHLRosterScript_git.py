#-------------------------------------------------------------------------------
# Name:        NHLRosterScript_git.py
# Purpose:     Allows for the retrieval of current NHL players born in a particular
#              country (ie Sweden) who play forward positions.Makes three new shapefiles
#              for each of the positions. Adds, calculates and populates new fields
#              for height and weight of each player, expressed in cm/kg.
# Author:      Tara Wu
# Created:     07/09/2025
#-------------------------------------------------------------------------------
"""
Last Updated: September 18, 2023
Author: Tara Wu
Description: This script allows for the retrieval of current NHL players born in a particular country (in this instance, Sweden) who play forward positions.
It makes three new shapefiles for each of the positions. It also adds, calculates and populates new fields for height and weight of each player,
expressed in centimeters and kilograms, respectively.
Requirements: ArcGIS Pro
"""

# import modules
import arcpy

# define workspace
arcpy.env.workspace = r"./data"
arcpy.env.overwriteOutput = True


# define variables
nhlRosterFC = "nhlrosters.shp"
countriesFC = "Countries_WGS84.shp"
countryField = "CNTRY_NAME"
positionField = "position"
positionsSelected = ["RW", "LW", "C"]
weightField = "weight"
heightField = "height"
height_cm = "height_cm"
weight_kg = "weight_kg"


# make a feature layer of target country (ex Sweden)
try:
    targetCountry = arcpy.management.SelectLayerByAttribute(countriesFC, "NEW_SELECTION", countryField + " = 'Sweden'")
    print("Successfully made a feature layer of target country.")
except:
    print("Failed to create feature layer of target country.")


for position in positionsSelected:

    # Create spatial query to select all of the players within target country
    try:
        targetCountryPlayers = arcpy.management.SelectLayerByLocation(nhlRosterFC, "WITHIN", targetCountry)
        print("Successfully selected all players from target country in position " + position +".")
    except:
        print("Spatial query to select players from target country did not work.")



    # attribute query to select layers from target country in forward positions (RW/LW/C)
    try:
        countryPosition = arcpy.management.SelectLayerByAttribute(targetCountryPlayers, "SUBSET_SELECTION", positionField + " = " + "'" + position + "'")
    except:
        print("Selecting all positions did NOT work.")


    # use Copy Features tool to save selected features into a new feature class
    try:
        newFCName = "Sweden" + position + ".shp"
        finalFC = arcpy.management.CopyFeatures(countryPosition, newFCName)
    except:
        print ("Did not successfully copy all selected features into new FC.")


    # go through new position shapefile, use "Add Field" tool to add "height_cm" and "weight_kg" fields
    try:
        arcpy.management.AddField(finalFC, height_cm, "SHORT")
        arcpy.management.AddField(finalFC, weight_kg, "FLOAT")
        print("Created new height and weight fields for " + position + " feature class.")

    except:
        print("Creation of height and weight fields did not work for " + position + " feature class.")


    # use UpdateCursor to loop through all rows, populate new fields with appropriate values
    try:
        with arcpy.da.UpdateCursor(finalFC, (height_cm, weight_kg, heightField, weightField)) as cursor:

            for row in cursor:

                # Convert existing height (a text field, measured in feet/inches) to centimeters, which will be used to populate the numerical height_cm field
                splitLocation = row[2].index("'")
                feetPart = int(row[2][:splitLocation])
                inchPart = int(row[2][splitLocation+2:-1])
                heightCentimeters = (feetPart * 12 + inchPart) * 2.54
                row[0] = heightCentimeters

                # Convert existing weight (measured in pounds) to kilograms, which will be used to populate the weight_kg field
                newWeight = row[3] * 0.453592
                row[1] = newWeight

                # Save cursor updates
                cursor.updateRow(row)
        print("Added converted heights and weights to " + position + " feature class.")
    except:
        print("Failed to add converted heights and weights to new feature classes.")


    # delete row and cursor for first iteration of update cursor
    del row, cursor
    arcpy.Delete_management(countryPosition)


    # delete temporary feature layers in for loop
    del newFCName

# delete layers
arcpy.Delete_management(targetCountry)
arcpy.Delete_management(targetCountryPlayers)




