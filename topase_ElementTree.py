import xml.etree.ElementTree as ET
import re

def take_input():
    """
    Prompt the user for input and return new_revision_number, new_version, and new_start_datetime.
    """
    xml_file_path = "PA_mobility_20230924_1 (1) (copy).xml"
    new_revision_number = "0"  # Replace with your desired revision number
    new_version = "0"  # Replace with your desired version
    new_start_datetime = "2023-09-24T00:00Z"  # Replace with your desired start datetime
    
    # xml_file_path = input("Enter the XML file path: ")
    # new_revision_number = input("Enter new revisionNumber: ")
    
    # # Assume version number is the same as revisionNumber
    # new_version = new_revision_number
    
    # while True:
    #     new_start_date = input("Enter date (in format 'YYYY-MM-DD'): ")
    #     new_start_time = input("Enter time (in format 'HH:MM'): ")
    #     new_start_datetime = new_start_date + 'T' + new_start_time + 'Z'  # Format: 'YYYY-MM-DDTHH:MMZ'
        
    #     if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z$', new_start_datetime):
    #         break
    #     else:
    #         print("Datetime format is not matched! Please try again.")
    
    return xml_file_path, new_revision_number, new_version, new_start_datetime

def update_xml_data(root, new_revision_number, new_version, new_start_datetime, namespace):
    """
    Update XML data with new_revision_number, new_version, and new_start_datetime.
    
    Args:
        root (Element): The root element of the XML document.

        new_revision_number (str): The new revision number.
        new_version (str): The new version.
        new_start_datetime (str): The new start datetime.
    """

    # Update the revisionNumber, version, and start datetime
    revision_number_element = root.find(".//{{{}}}revisionNumber".format(namespace))
    if revision_number_element is not None:
        revision_number_element.text = new_revision_number

    version_elements = root.findall(".//{{{}}}version".format(namespace))
    for version_element in version_elements:
        version_element.text = new_version

    start_elements = root.findall(".//{{{}}}start".format(namespace))
    for start_element in start_elements:
        start_element.text = new_start_datetime


def datapoint(root, element_name, new_quantity, namespace):
    # try:
        mRIDs = [
            "RPH_ESQUES01_20230924",
            "RPB_ESQUES01_20230924",
            "RPH_FLINS1TB_20230924",
            "RPB_FLINS1TB_20230924"
        ]

        values = [
            "3",
            "3",
            "13",
            "13"
        ]

        # Iterate through the <Series> elements
        for mRID, value in zip(mRIDs, values):
            series_elements = root.findall(".//{{{}}}Series".format(namespace))

            for series in series_elements:
                mrid_element = series.find(".//{{{}}}mRID".format(namespace))

                if mrid_element.text == mRID:
                    point_elements = series.findall(".//{{{}}}Point".format(namespace))

                    for point in point_elements[0:10]:
                        point.clear()
                        # quantity = point.find(".//{{{}}}quantity".format(namespace))
                        # point.remove(quantity)

                        # positions = point.find(".//{{{}}}position".format(namespace))
                        # point.remove(positions)
                        # series.remove(point)

                    for loop_count, point in enumerate(point_elements, start=1):
                        quantity = point.find(".//{{{}}}quantity".format(namespace))
                        positions = point.find(".//{{{}}}position".format(namespace))

                        quantity.text = value
                        positions.text = str(loop_count)

                        # print("Updated position:", positions.text)
                        # print("Updated quantity:", quantity.text)

        # Check if the current element is empty (has no content)
        if not root.text and not root.tail and not root.attrib:
            root.getparent().remove(root)

    # except Exception as e:
    #     print(f"An error occurred while changing '{element_name}' quantity values: {e}")



def export(tree, xml_file_path):
    """
    Export the updated XML tree back to the file.
    
    Args:
        tree (ElementTree): The XML tree to be exported.
        xml_file_path (str): The path to the XML file.
    """
    try:
        # Save the updated XML back to the file
        tree.write(xml_file_path, encoding="utf-8")

        print(f"Congratulations! Your XML file '{xml_file_path}' has been updated.")
    
    except FileNotFoundError:
        print(f"Error: The specified XML file '{xml_file_path}' does not exist.")

def main():
    try:
        # Call the take_input function to get user input
        xml_file_path, new_revision_number, new_version, new_start_datetime = take_input()

        # Load the XML file
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Define the namespace URI
        namespace = "urn:iec62325.351:tc57wg16:451-n:MultipleScheduleDocument:1:1"
        ET.register_namespace('', namespace)

        # Call the update_xml_data function to update the XML
        update_xml_data(root, new_revision_number, new_version, new_start_datetime, namespace)

        # Call the new function to change a data point
        new_quantity = input("Enter the new quantity value: ")
        datapoint(root, "Point", new_quantity, namespace)
        
        # Call the export function to export the XML
        export(tree, xml_file_path)
    
    except KeyboardInterrupt:
        print("\nOperation aborted by the user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
