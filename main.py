import os
import re
from datetime import datetime
from bs4 import BeautifulSoup
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

class CustomHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            with open('index.html', 'rb') as file:
                self.wfile.write(file.read())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        post_parameters = parse_qs(post_data)

        xml_file_path = post_parameters.get('xml_file_path', [''])[0]
        rV_number = post_parameters.get('rV_number', [''])[0]
        start_date = post_parameters.get('start_date', [''])[0]
        start_time = post_parameters.get('start_time', [''])[0]
        douai_quantity = post_parameters.get('douai_quantity[]')
        flins_quantity = post_parameters.get('flins_quantity[]')

        new_douai_quantity = post_parameters.get('new_douai_quantity[]')
        new_flins_quantity = post_parameters.get('new_flins_quantity[]')

        # Convert the quantity values to integers
        douai_quantities = [float(q) for q in douai_quantity]
        flins_quantities = [float(q) for q in flins_quantity]

        new_douai = [float(q) for q in new_douai_quantity]
        new_flins = [float(q) for q in new_flins_quantity]

        if not os.path.exists(xml_file_path):
            response = "Error: The specified XML file does not exist."
        else:
            soup = load_xml(xml_file_path)
            startDatetime = f"{start_date}T{start_time}Z"
            if re.match(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}Z$', startDatetime):

                # Call the update_xml_data function to update the XML
                update_xml_data(soup, rV_number, rV_number, startDatetime)

                # Call the new function to change a data point
                datapointCalculatios(soup, startDatetime, douai_quantities, flins_quantities, new_douai, new_flins)

                # Call the export function to export the updated XML
                export(soup, xml_file_path)

                # Respond to the client with a success message
                response = "Data received and processed successfully."
            else:
                response = 'Date & time format is not matched! Please try again!'
        
        response_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <!--  meta tags -->
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />

            <!-- Bootstrap CSS -->
            <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@4.0.0/dist/css/bootstrap.min.css"
                integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous" />

            <title>XML File Generator!</title>
        </head>
        <body>
            <nav class="navbar navbar-light bg-light">
                <a class="navbar-brand navbar-brand mx-auto text-center center-block" href="#">
                    <h2>Regenerate XML File<h2>
                </a>
            </nav>
            <div class="container">
                <!-- Just an image -->
                <div class="pt-5">
                    <div id="success-message">{response}</div>
                    <br>
                    <a href="/" type="submit" class="btn btn-success text-white">Get Back</a>
                </div>
            </div>
        </body>
        </html>
        """
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(response_html.encode('utf-8'))

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


def datapointCalculatios(soup, startDatetime, douai_quantity, flins_quantity, new_douai, new_flins):
    """
    Calculate datapoint based on startDatetime and the total positions of the xml file. Read Quantity from user for both Grid 
    and process it to update. After that, remove the extra datapoint from here and change the value of the Quantity and Positions
    :return: None
    """
    try:
        old_qtyies = [
            douai_quantity,
            douai_quantity,
            flins_quantity,
            flins_quantity,
        ]

        new_qtyies = [
            new_douai,
            new_douai,
            new_flins,
            new_flins,
        ]

        # Parse the startDatetime string into a startDatetime object
        dt_object = datetime.strptime(startDatetime, "%Y-%m-%dT%H:%MZ")
        hour = dt_object.hour
        dateTime = soup.find("end")
        dateTimeObject = datetime.strptime(dateTime.text, "%Y-%m-%dT%H:%MZ")
        dateTimeHour = dateTimeObject.hour
        if (hour == dateTimeHour):
            new_quantity = 48
        elif(hour > dateTimeHour):
            new_quantity = 46
        else:
            new_quantity = ((dateTimeHour - hour) * 2)

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
        for mRID, old_qty, new_qty in zip(mRIDs, old_qtyies, new_qtyies):

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

                        for data in quantity:
                            current_quantity = float(data.string)
                            for index, qty in enumerate(old_qty, start=0):
                                if (current_quantity == qty):
                                    quantity.string = str(new_qty[index])

                        # Update the position from Values and serial number(loop_count)
                        positions.string = str(loop_count)
    except Exception as error:
        print(f"Error! An error occurred while changing '{point_update}' quantity values: {error}")


def export(soup, xml_file_path):
    """
    Export the updated XML soup object back to the file.
    Args: soup (BeautifulSoup): The BeautifulSoup object representing the updated XML.
        xml_file_path (str): The path to the XML file.
    """
    try:
        # Remove the auto xml_declaration
        xml_declaration = ''.join(str(tag) for tag in soup.contents)
        new_xml_expo = f'Update_{xml_file_path}'
        
        with open(new_xml_expo, "w") as xml_file:
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

def main():
    host = 'localhost'
    port = 8000

    server = HTTPServer((host, port), CustomHandler)
    print(f"Serving at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

if __name__ == "__main__":
    main()
