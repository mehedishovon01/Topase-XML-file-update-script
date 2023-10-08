import os
import re
import time
from datetime import datetime
from bs4 import BeautifulSoup

def get_user_input():
    """
    Prompt the user for input and return new_revision_number, new_version, and new_start_startDatetime.
    Returns:
        str: The path to the XML file.
        str: The revision number.
        str: The start datetime.
    """
    # xml_file_path = "PA_mobility_20230924_1 (1) (copy).xml"

    rV_number = input("Enter the new Revision Number: ")
    print("Note: The Version Number is assumed to be the same as the Revision Number.")
    version = rV_number
    
    while True:
        start_date = input("Enter the date (in the format 'YYYY-MM-DD'): ")
        start_time = input("Enter the time (in the format 'HH:MM'): ")
        startDatetime = start_date + 'T' + start_time + 'Z'  # Format: 'YYYY-MM-DDTHH:MMZ'
        
        if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z$', startDatetime):
            break
        else:
            print("startDatetime format is not matched! Please try again.")
    
    return rV_number, version, startDatetime


def update_xml_data(soup, rV_number, version, startDatetime):
    """
    Update XML data with new_revision_number, new_version, and new_start_startDatetime.
    Args: soup (BeautifulSoup): The BeautifulSoup object representing the XML document.
        new_revision_number (str): The new revision number.
        new_version (str): The new version.
        new_start_startDatetime (str): The new start startDatetime.
    """

    # Update the revisionNumber, version, and start startDatetime
    revision_number_element = soup.find("revisionNumber")
    if revision_number_element is not None:
        revision_number_element.string = rV_number

    version_elements = soup.find_all("version")
    for version_element in version_elements:
        version_element.string = version

    start_elements = soup.find_all("start")
    for start_element in start_elements:
        start_element.string = startDatetime


def datapointCalculatios(soup, startDatetime):
    """
    Calculate datapoint based on startDatetime and the total positions of the xml file. Read Quantity from user for both Grid 
    and process it to update. After that, remove the extra datapoint from here and change the value of the Quantity and Positions
    :return: None
    """ 
    while True:
        douaiQuantity = input("Enter the Quantity of Douai: ")
        flinsQuantity = input("Enter the Quantity of Flins: ")

        if (int(douaiQuantity) <= 4) is False:
            print("Douai Quantity must be less or equal 4! Please try again.")
        elif (int(flinsQuantity) <= 16) is False:
            print("Flins Quantity must be less or equal 16! Please try again.")
        else:
            break

    values = [
        douaiQuantity,
        douaiQuantity,
        flinsQuantity,
        flinsQuantity,
    ]

    # Parse the startDatetime string into a startDatetime object
    dt_object = datetime.strptime(startDatetime, "%Y-%m-%dT%H:%MZ")
    hour = dt_object.hour
    new_quantity = ((22 - hour) * 2)

    # Define a regular expression pattern to match elements with the desired prefixes
    prefix_pattern = re.compile(r'^(RPH_|RPB_)')        # For find the exact mrIDs

    # Find all occurrences of mRID elements with the specified prefixes using a lambda function
    mrid_elements = soup.find_all(lambda tag: tag.name == 'mRID' and prefix_pattern.match(tag.text))

    # Create a list of mRID values
    mRIDs = [mrid_element.text for mrid_element in mrid_elements]

    """
    This code processes each <Series> element in the XML, and identifies matching <Point> elements based on the mRIDs under the <Series>,
    removes a specified number of them, removes any empty <Point> elements,
    and updates the remaining <Point> elements with new values.
    """
    # Iterate through the <Series> elements
    for mRID, value in zip(mRIDs, values):
        series_elements = soup.find_all("Series")

        # Iterate through the <mRID> elements
        for series in series_elements:
            mrid_element = series.find("mRID")

            # Identifies <Point> elements based on the mRIDs
            if mrid_element.string == mRID:
                point_elements = series.find_all("Point")

                # Find the length_of_positions for calculate the Datapoints
                length_of_positions = []
                for point in point_elements:
                    positions_tag = point.find("position")
                    length_of_positions.append(positions_tag)

                # Calculate how much Datapoints need to be delete
                delete_datapoint = (len(length_of_positions) - new_quantity)

                # Delete datapoints amount based on delete_datapoint
                for point in point_elements[0:delete_datapoint]:
                    point.clear()   # Note: In BeautifulSoup, using .clear() removes all child elements, including text.

                # Remove empty 'Point' elements from the soup
                for point in soup.find_all('Point'):
                    if not point.contents:
                        point.decompose()

                # Updates the remaining <Point> elements with new values
                point_update = series.find_all("Point")

                # Iterate on the remaining <Point> and find the quantity & position to update
                for loop_count, point in enumerate(point_update, start=1):
                    quantity = point.find("quantity")
                    positions = point.find("position")

                    # Update the quantity & position from Values and serial number(loop_count)
                    quantity.string = value
                    positions.string = str(loop_count)


def export(soup, xml_file_path):
    """
    Export the updated XML soup object back to the file.
    Args: soup (BeautifulSoup): The BeautifulSoup object representing the updated XML.
        xml_file_path (str): The path to the XML file.
    """
    try:
        # Remove the auto xml_declaration
        xml_declaration = ''.join(str(tag) for tag in soup.contents)
        with open(xml_file_path, "w") as xml_file:
            xml_file.write(str(xml_declaration))

        print(f"Congratulations! Your XML file '{xml_file_path}' has been updated.")
    
    except FileNotFoundError:
        print(f"Error: The specified XML file '{xml_file_path}' does not exist.")


def load_xml(xml_file_path):
    """
    Load the XML file specified by 'xml_file_path' in read mode. Read the entire content of the XML file 
    and store it in 'xml_content'. Create a BeautifulSoup object by parsing the 'xml_content' using the "xml" parser.
    This allows us to work with the XML data more easily.
    :param title: xml_file_content
    :return: bs4
    """
    try:
        with open(xml_file_path, "r") as xml_file:
            xml_content = xml_file.read()
        return BeautifulSoup(xml_content, "xml")
    
    except FileNotFoundError:
        print(f"Error: The specified XML file '{xml_file_path}' does not found!")


if __name__ == "__main__":
    # Fetch file until the file exists
    while True:
        xml_file_path = input("Enter the XML file Name: ")
        if os.path.exists(xml_file_path):
            soup = load_xml(xml_file_path)
            break
        else:
            print(f"The file '{xml_file_path}' does not exist.")

    # Call the take_input function to get user input
    rV_number, version, startDatetime = get_user_input()
    
    # Call the update_xml_data function to update the XML
    update_xml_data(soup, rV_number, version, startDatetime)

    # Call the new function to change a data point
    datapointCalculatios(soup, startDatetime)
    
    # Call the export function to export the updated XML
    export(soup, xml_file_path)

    # Print in console to take time in seconds to execute this script
    start = time.time()
    print(f'Success! This script took {round(time.time() - start, 4)} seconds to generate the results')
