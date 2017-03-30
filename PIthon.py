import sys
import clr

sys.path.append(r'C:\Program Files (x86)\PIPC\AF\PublicAssemblies\4.0')  
clr.AddReference('OSIsoft.AFSDK')

from OSIsoft.AF import *
from OSIsoft.AF.PI import *
from OSIsoft.AF.Asset import *
from OSIsoft.AF.Data import *
from OSIsoft.AF.Time import *
from OSIsoft.AF.UnitsOfMeasure import *

print("Welcome to PIthon!!")
# PI Data Archive
piServers = PIServers()  
piServer = piServers.DefaultPIServer;

pt = PIPoint.FindPIPoint(piServer, "sinusoid")
name = pt.Name.lower()
# CurrentValue
print('\nShowing PI Tag CurrentValue from {0}'.format(name))
current_value = pt.CurrentValue()
print( '{0}\'s Current Value: {1}'.format(name, current_value.Value))

#recordedvalues
timerange = AFTimeRange("*-3h", "*")
recorded = pt.RecordedValues(timerange, AFBoundaryType.Inside, "", False)
print('\nShowing PI Tag RecordedValues from {0}'.format(name))
for event in recorded:
    print('{0} value: {1}'.format(event.Timestamp.LocalTime, event.Value))

#plotValues
plotvalues = pt.PlotValues(timerange, 100)
print('\nShowing PI Tag PlotValues from'.format(name))
for event in plotvalues:
    print('{0} value: {1}'.format(event.Timestamp.LocalTime, event.Value))

#interpolatedvalues
span = AFTimeSpan.Parse("1h")
interpolated = pt.InterpolatedValues(timerange, span, "", False)
print('\nShowing PI Tag InterpolatedValues from'.format(name))
for val in interpolated:
    print('{0} value: {1}'.format(event.Timestamp.LocalTime, event.Value))

#summariesvalues
summaries = pt.Summaries(timerange, span, AFSummaryTypes.Average, AFCalculationBasis.TimeWeighted, AFTimestampCalculation.Auto)
print('\nShowing PI Tag SummariesValues(Average) from'.format(name))
for summary in summaries:
    for event in summary.Value:
        print('{0} value: {1}'.format(event.Timestamp.LocalTime, event.Value))

#writeValue
writept = PIPoint.FindPIPoint(piServer,"PleaseEnterWriteTagName")
writeptname = writept.Name.lower()
val = AFValue()
val.Value = 20
#val.Timestamp = AFTime("t+9h")

print('\nWrite value to {0} value: {1}'.format(writeptname, val.Value))
writept.UpdateValue(val, AFUpdateOption.Replace, AFBufferOption.BufferIfPossible)

#Connect to AF
print ('\nConnect to AF')
afServers = PISystems()
afServer = afServers.DefaultPISystem
DB = afServer.Databases.DefaultDatabase
#DB = afServer.Databases.get_Item("NuGreen")
element = DB.Elements.get_Item("NuGreen").Elements.get_Item("Little Rock").Elements.get_Item("Extruding Process").Elements.get_Item("Equipment").Elements.get_Item("K-435")

attribute = element.Attributes.get_Item("Steam Flow")
attval = attribute.GetValue()

print ('Element Name: {0}'.format(element.Name))
print ('Attribute Name: {0} | Value : {1} {2}'.format(attribute.Name, attval.Value, attribute.DefaultUOM))

#create element with attribute
print('\nCreate Element with Attribute')
if DB.Elements.get_Item("Test New Element") is not None:
    print("Already Existing Element: Test New Element")
else:
    newelement = DB.Elements.Add("Test New Element")
    newelement.Description = "Created element from PIthon"
    newattribute = newelement.Attributes.Add("Test Attribute")
    newattribute.DataReferencePlugIn = afServer.DataReferencePlugIns.get_Item("PI Point")
    newattribute.DataReference.ConfigString = "cdt158"
    DB.CheckIn()
    print("Created new Element : Test New Element")






