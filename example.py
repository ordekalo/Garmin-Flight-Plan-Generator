from xml.dom import minidom

root = minidom.Document()

xml = root.createElement('flight-plan')
xml.setAttribute('xmlns', 'http://www8.garmin.com/xmlschemas/FlightPlan/v1')
root.appendChild(xml)

productChild = root.createElement('product')
productChild.setAttribute('name', 'Geeks for Geeks')

xml.appendChild(productChild)

xml_str = root.toprettyxml(indent="\t")

save_path_file = "gfg.xml"

with open(save_path_file, "w") as f:
    f.write(xml_str)
