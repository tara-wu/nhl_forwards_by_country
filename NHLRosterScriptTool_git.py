#-------------------------------------------------------------------------------
# Name:        NHLRosterScriptTool_git.py
# Purpose:     Script tool allows for  retrieval of current NHL players born in
#              a particular country who play a position of choice. Users select
#              a country and a position of choice to in ArcGIS, and a feature
#              class is created with those chosen individuals. Weight and height
#              are converted into kilograms and centimeters, respectively.
# Author:      Tara Wu
# Created:     07/09/2025
#-------------------------------------------------------------------------------"""


# import modules
import arcpy

# define workspace
arcpy.env.workspace = arcpy.GetParameterAsText(0)
arcpy.env.overwriteOutput = True


# define variables
nhlRosterFC = arcpy.GetParameterAsText(1) # user selects roster
countriesFC = arcpy.GetParameterAsText(2) # user selects country template
countryField = arcpy.GetParameterAsText(3) # user selects country field
countrySelected = arcpy.GetParameterAsText(4) # user selects target country
positionField = arcpy.GetParameterAsText(5) # user selects position field
positionsSelected = arcpy.GetParameterAsText(6).split(";") # user selects positions of choice
weightField = arcpy.GetParameterAsText(7) # user selects weight field
heightField = arcpy.GetParameterAsText(8) # user selects height field
height_cm = "height_cm"
weight_kg = "weight_kg"


# make feature layer of a particular country
try:
    countrySelection = arcpy.management.SelectLayerByAttribute(countriesFC, "NEW_SELECTION", countryField + " = " + "'" + countrySelected + "'")
    arcpy.AddMessage("Successfully made a feature layer for " + countrySelected + ".")
except:
    arcpy.AddMessage("Failed to create feature layer of target country.")

try:
    for position in positionsSelected:

        # create spatial query to select all players within target Country
        try:
            countryPlayers = arcpy.management.SelectLayerByLocation(nhlRosterFC, "WITHIN", countrySelection)
        except:
            arcpy.AddMessage("Spatial query did not work.")

        # perform attribute query to select players in forward positions (RW/LW/C)
        try:
            countryPosition = arcpy.management.SelectLayerByAttribute(countryPlayers, "SUBSET_SELECTION", positionField + " = " + "'" + position + "'")
            arcpy.AddMessage("Successfully selected all players in " + position + ".")
        except:
            arcpy.AddMessage("Selecting all positions did NOT work.")

        # use Copy Features tool to save selected features into a new feature class
        try:
            newFCName = countrySelected.replace(" ", "") + position + ".shp"
            finalFC = arcpy.management.CopyFeatures(countryPosition, newFCName)
            arcpy.AddMessage("Created new feature class for " + position + ".")
        except:
            arcpy.AddMessage("Did not successfully copy all selected features into new FC.")

        # go through new position shapefile, use "Add Field" tool to add "height_cm" and "weight_kg" fields
        arcpy.management.AddField(finalFC, height_cm, "SHORT")
        arcpy.management.AddField(finalFC, weight_kg, "FLOAT")

        # use UpdateCursor to loop through all rows, populate new fields
        try:
            with arcpy.da.UpdateCursor(finalFC, (height_cm, weight_kg, heightField, weightField)) as cursor:
                for row in cursor:

                    # convert existing height (text field in ft/in) to cm, used to populate  numerical height_cm field
                    splitLocation = row[2].index("'")
                    feetPart = int(row[2][:splitLocation])
                    inchPart = int(row[2][splitLocation+2:-1])
                    heightCentimeters = (feetPart * 12 + inchPart) * 2.54
                    row[0] = heightCentimeters

                    # convert existing weight (lbs) to kg, used to populate weight_kg field
                    newWeight = row[3] * 0.453592
                    row[1] = newWeight

                    # save cursor updates
                    cursor.updateRow(row)
            arcpy.AddMessage("Added converted heights and weights to " + position + " feature class.")
        except:
            arcpy.AddMessage("Failed to add converted heights and weights to new feature classes.")

        # delete row and cursor for first iteration of update cursor
        del row, cursor
        arcpy.Delete_management(countryPosition)

        # delete temporary feature layers in for loop
        del newFCName

except:
    arcpy.AddMessage(arcpy.GetMessages())

# delete  layers
arcpy.Delete_management(countrySelection)
arcpy.Delete_management(countryPlayers)





