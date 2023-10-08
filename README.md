# Introduction
We have regularly need to update the XML file. But it's a very hard to update it manually.
So, I just make a script and update the XML file with it easyly.

# Setup
To use this script to your own machine follow this steps

## Requirments

_You_ must have to need the following components to you machine
* Python3.10

### Python3.10

_Python 3.10_ is provided by Official _Ubuntu 22.04 LTS_ repositories and is preinstalled by default. To see which version of Python your machine have installed.

    python3 --version

If you have not install _pyhton3.10_ please follow this installation instructions

Just click here, [installation instructions](https://www.python.org/downloads/)
    

## Prepare the Script to Execute

### Clone repository from github

First of all, clone this repository using this command

    git clone https://github.com/mehedishovon01/Opsgenie-Note-Export-Script.git

### Create a virtualenv

Make a virtual environment to your project directory. Let's do this,

If you have already an existing python3 virtualenv then run this

    virtualenv venv

Or if virtualenv is not install in you machine then run this

    python3 -m venv venv
    
Activate the virtual environment and verify it

    . venv/bin/activate

### Install the dependencies

Most of the projects/scripts have dependency name like requirements.txt file which specifies the requirements of that projects/sripts. So, let’s install the requirements of it from the txt file.

    pip install -r requirements.txt

Boooooom! Setup is done.

## Execute the Script

### Run the Script
We are almost done. Let's run the command from terminal and get output,

    python3 topase.py

Note: Only the `topase.py` file will be workable. And other two files are for trying with xml & lxml library. But not successfull.

That’s it! Now your script is already running into the console.

After successfully execute the script it will show a message like, **_This script took X.X seconds to generate the results_**
#### _Note:_ This _Script_ will take few minutes or may be more depending on data range.
<br/>
<sub> Thanks for reading. </sub>
