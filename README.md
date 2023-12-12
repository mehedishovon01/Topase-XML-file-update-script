# Introduction
We have working with Topase UI XML file regularly. We need to update the XML file regularly. But updating manually is very difficult. So, I just create a script and simply update the XML file with it.

As the booking has been pre-defined by TMH so we must have to use that booking. For this reason I have read the XML file and get all the information and then process the file.

## Step-1 (# Setup)
To use this script to your own machine follow this steps

### Requirements
You must have to need the following components to you machine

* Python3.10

#### Python3.10
_Python 3.10_ is provided by Official _Ubuntu 22.04 LTS_ repositories and is preinstalled by default. To see which version of Python your machine have installed.

    python3 --version

If you have not install pyhton3.10 please follow this installation instructions

Just click here, [installation instructions](Download Python )

## Step-2 (# Prepare the Script to Execute)
You can clone the repository from GitHub or you can use the manual download.

#### Clone from GitHub
Clone this repository using this command

    git clone https://github.com/mehedishovon01/Topase-XML-file-update-script.git

Now, open the terminal from their. And then follow the bellow steps.

### Create a virtualenv
Make a virtual environment to your project directory. Let's do this,
If you have already an existing python3 virtualenv then run this

    virtualenv venv

Or if virtualenv is not install in you machine then run this

    python3 -m venv venv

Activate the virtual environment and verify it

    . venv/bin/activate

After successfully completed the these virtualenv process,

### Install the dependencies
Most of the projects/scripts have dependency name like requirements file which specifies the requirements of that projects/sripts. So, let’s install the requirements of it from the txt file.

    pip install -r requirement.txt

Boooooom! Setup is done.

## Execute the Script
We are almost done. Let's run the command from terminal and get output,

#### Run the Script

    python3 main.py

Note: Only the `main.py` file will be executable.

That’s it! Now your script is already running into the console. 

After successfully execute the script it will show a message like, **Serving at http://localhost:8000**

_Note:_ This Script will take few seconds or may be more depending.

## Step-3 (# Run the Script and Get Output)
Run the Script XML file in Browser. Now, open the browser and paste this development server http://127.0.0.1:8000/ and then you will see a UI like this.

Note: Please make sure the downloaded XML file and all the scripts are in the same folder.

## `Input Form Description`
> _Version Number_
> * We have updated the Version Number wherever it is and increment it by one which number already had.
> * As the Version Number & Revision Number are same so the script will automatically update the Revision Number.

> _Start Date_
> * Give only the date as input.

> _Time_
> * Update the running time with saling round figure. Plus one hour with that Minus six hour from that time. 
> * Note: The time input must be: XX:XX this format. Otherwise the script will give you an error.

> _Douai Present Quantity_
> * Here, you have to give input that the quantity you want to change.

> _Douai New Quantity_
> * Here, you have to give the new quantity you want to.

> _Add Another?_
> * Some times we have seen that there are many types of quantity has been setting up by TMH. So, if we need to update multiple types of quantity the click the Add Another and the it will open a new row where it will display Douai Present Quantity & Douai New Quantity.

> _Flins Present Quantity_
> * Same as Douai Present Quantity

> _Flins New Quantity_
> * Same as Douai New Quantity

After the fully fill-up the form click on the Generate. And then it will create a new XML file and exported in the same directory with the update.

### _`According to the Updating call schedules manually in Topase UI there are some limitations,`_

* The first covered period must be the next hour from the next full one.
* Any time earlier or later will not be accepted. Non-full hours will not be accepted.

<br>
<sub> Thanks for reading. </sub>