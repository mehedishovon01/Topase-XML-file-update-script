from lxml import etree

def update_xml_data(root, new_revision_number, new_version, new_start_datetime, namespace):
    """
    Update XML data with new_revision_number, new_version, and new_start_datetime.

    Args:
        root (Element): The root element of the XML document.
        new_revision_number (str): The new revision number.
        new_version (str): The new version.
        new_start_datetime (str): The new start datetime.
        namespace (str): The XML namespace.

    Returns:
        Element: The updated root element.
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

    return root


def datapoint(root, element_name, new_quantity, namespace):
    # try:
        mRIDs = [
            "RPH_ESQUES01_20230924",
            "RPB_ESQUES01_20230924",
            "RPH_FLINS1TB_20230924",
            "RPB_FLINS1TB_20230924"
        ]

        values = [
            "2",
            "2",
            "11",
            "11"
        ]

        # Iterate through the <Series> elements
        for mRID, value in zip(mRIDs, values):
            series_elements = root.xpath(".//ns:Series[ns:mRID = $mRID]", namespaces={"ns": namespace, "xsi": "http://www.w3.org/2001/XMLSchema-instance"}, mRID=mRID)

            for series in series_elements:
                point_elements = series.findall(".//ns:Point", namespaces={"ns": namespace})

                # Iterate through <Point> elements and remove <quantity> and <positions> elements
                for point in point_elements[0:10]:
                    # point.clear()
                    quantity_element = point.find(".//ns:quantity", namespaces={"ns": namespace})
                    positions_element = point.find(".//ns:position", namespaces={"ns": namespace})

                    for q in quantity_element:
                         quantity_element.remove(q)

                    for p in positions_element:
                         quantity_element.remove(p)

                    # # Check if <quantity> element is found and remove it
                    # if quantity_element is not None:
                    #     point.remove(quantity_element)

                    # # Check if <positions> element is found and remove it
                    # if positions_element is not None:
                    #     point.remove(positions_element)


                # for point in points_to_remove:
                #     series.remove(point)
                    # Remove the point element
                    # series.remove(point)

    # except Exception as e:
    #     print(f"An error occurred while changing '{element_name}' quantity values: {e}")

# Example usage:
xml_file_path = "PA_mobility_20230924_1 (1) (copy).xml"
namespace = "urn:iec62325.351:tc57wg16:451-n:MultipleScheduleDocument:1:1"

# Parse the XML file
tree = etree.parse(xml_file_path)
root = tree.getroot()

# Update the XML data
new_revision_number = "2"
new_version = new_revision_number
new_start_datetime = "2023-10-24T12:00:00Z"
updated_root = update_xml_data(root, new_revision_number, new_version, new_start_datetime, namespace)


# Update the XML data
element_name = "Point"
new_quantity = "3"
datapoint(root, element_name, new_quantity, namespace)


# You can save the updated XML back to a file if needed
etree.ElementTree(updated_root).write(xml_file_path)

# print(etree.tostring(root, pretty_print=True).decode())
