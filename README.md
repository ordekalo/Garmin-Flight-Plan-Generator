
# Garmin Flight Plan Generator from KML

This project provides a tool to convert KML waypoint data into Garmin-compatible FPL (Flight Plan) files. It allows users to extract waypoint information from a KML file and create an FPL file that can be loaded into Garmin navigation systems.

## Features

- **KML to FPL Conversion**: Parse KML files to extract waypoint information and generate an FPL file.
- **Excel Export**: Export waypoint data into Excel `.xlsx` files using the `xlsxwriter` library.
- **Support for Multiple Waypoints**: Handles multiple waypoints and route points from the KML file.
- **XML Schema Compliance**: Generates FPL files that comply with Garmin's flight plan XML schema.

## Prerequisites

- **Python**: Ensure you have Python 3.7+ installed on your system.
- **Virtual Environment**: It is recommended to use a Python virtual environment for managing dependencies.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/ordekalo/Garmin-Flight-Plan-Generator.git
   cd Garmin-Flight-Plan-Generator
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Converting KML to FPL**:
   
   To convert a KML file containing waypoint information into an FPL file, run the `kml_to_fpl.py` script. Place your KML file in the `input/` directory and specify the output path for the FPL file.

   ```bash
   python kml_to_fpl.py
   ```

   Example:

   ```bash
   python kml_to_fpl.py --input input/example.kml --output output/generated_flight_plan.fpl
   ```

2. **Generating Excel Files**:
   
   You can also extract waypoint data from the KML file and export it to an Excel file:

   ```bash
   python kml_to_xlsx.py
   ```

   This will generate an Excel file with waypoint data in the `output/` directory.

## Example

If you have a KML file with waypoints and coordinates like this:

```xml
<Placemark>
    <name>Example Waypoint</name>
    <Point>
        <coordinates>34.12345,-118.12345,0</coordinates>
    </Point>
</Placemark>
```

The script will convert it into an FPL file that looks like:

```xml
<flight-plan xmlns="http://www8.garmin.com/xmlschemas/FlightPlan/v1">
    <created>2024-01-01T00:00:00Z</created>
    <waypoint-table>
        <waypoint>
            <identifier>EXAMP</identifier>
            <type>USER WAYPOINT</type>
            <country-code>US</country-code>
            <lat>34.12345</lat>
            <lon>-118.12345</lon>
            <comment></comment>
        </waypoint>
    </waypoint-table>
    <route>
        <route-name>Generated Route</route-name>
        <route-description>Description of the generated route</route-description>
        <flight-plan-index>1</flight-plan-index>
        <route-point>
            <waypoint-identifier>EXAMP</waypoint-identifier>
            <waypoint-type>USER WAYPOINT</waypoint-type>
            <waypoint-country-code>US</waypoint-country-code>
        </route-point>
    </route>
</flight-plan>
```

## File Structure

```
Garmin-Flight-Plan-Generator/
├── input/
│   └── example.kml           # KML input file containing waypoints
├── output/
│   └── generated_flight_plan.fpl  # Generated FPL output file
├── kml_to_fpl.py             # Main script to convert KML to FPL
├── kml_to_xlsx.py            # Script to export waypoints to Excel
├── requirements.txt          # Python dependencies
├── README.md                 # This README file
└── objects.py                # Waypoint, Route, and RoutePoint classes
```

## Requirements

The project uses the following Python libraries:

- **`xmltodict`**: For XML parsing and manipulation.
- **`openpyxl`**: For reading/writing Excel files.
- **`xlsxwriter`**: For generating Excel files.
- **`fastkml`**: For working with KML files.

These are listed in `requirements.txt` and can be installed with:

```bash
pip install -r requirements.txt
```

## Contributing

Feel free to open issues or submit pull requests if you want to contribute to this project. Make sure to follow best practices and include detailed documentation of any changes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
