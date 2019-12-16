# USPTOProcessZipFile.py
# USPTO Bulk Data Parser - Processes ZIP Files
# Description: Imported to Process Modules.  Extracts XML file contents from a downloaded ZIP file.
# Author: Joseph Lee
# Email: joseph@ripplesoftware.ca
# Website: www.ripplesoftware.ca
# Github: www.github.com/rippledj/uspto

# ImportPython Modules
import time
import os
import sys
import traceback
import subprocess
import shutil
import zipfile
import urllib.request, urllib.parse, urllib.error

# Import USPTO Parser Functions
import USPTOLogger

# Extract a zip file and return the contents of the XML file as an array of lines
def extract_xml_file_from_zip(args_array):

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")

    # Extract the zipfile to read it
    try:
        zip_file = zipfile.ZipFile(args_array['temp_zip_file_name'], 'r')
        # Find the xml file from the extracted filenames
        for filename in zip_file.namelist():
            if '.xml' in filename:
                xml_file_name = filename
        # Print stdout message that xml file was found
        print('[xml file found. Filename: {0}]'.format(xml_file_name))
        logger.info('xml file found. Filename: ' + xml_file_name)
        # Open the file to read lines out of
        xml_file = zip_file.open(xml_file_name, 'r')
        # Extract the contents from the file
        xml_file_contents = xml_file.readlines()
        # Close the file being read from
        zip_file.close()
        # If not sandbox mode, then delete the .zip file
        if args_array['sandbox'] == False and os.path.exists(args_array['temp_zip_file_name']):
            # Print message to stdout
            print('[Purging .zip file ' + args_array['temp_zip_file_name'] + '...]')
            logger.info('Purging .zip file ' + args_array['temp_zip_file_name'] + '...')
            os.remove(args_array['temp_zip_file_name'])

        # Print message to stdout
        print('[xml file contents extracted ' + xml_file_name + '...]')
        logger.info('xml file contents extracted ' + xml_file_name + '...')
        # Return the file contents as array
        return xml_file_contents

    # The zip file has failed using python's ZipFile
    # Unzip the file using subprocess and find the xml file
    except:
        try:
            # Print message to stdout
            print('[Zip file ' + args_array['temp_zip_file_name'] + ' failed to unzip with python module]')
            logger.warning('[Zip file ' + args_array['temp_zip_file_name'] + ' failed to unzip with python module]')
            traceback.print_exc()
            # Check if an unzip directory exists in the temp directory
            if not os.path.exists(args_array['temp_directory'] + "/unzip"):
                os.mkdir(args_array['temp_directory'] + "/unzip")
            # Make a directory for the particular downloaded zip file
            os.mkdir(args_array['temp_directory'] + "/unzip/" + args_array['file_name'])
            # Use a subprocess to unzip linux command
            subprocess.call("unzip " + args_array['temp_zip_file_name'] + " -d " + args_array['temp_directory'] + "/unzip/" + args_array['file_name'], shell=True)
            # Go through each file in the directory and look for the xml file
            for filename in os.listdir(args_array['temp_directory'] + "/unzip/" + args_array['file_name']):
                # Look for file with .xml extention
                if filename.endswith(".xml"):
                    xml_file_name = filename
                    # Print stdout message that xml file was found
                    print('[xml file found. Filename: {0}]'.format(xml_file_name))
                    logger.info('xml file found. Filename: ' + xml_file_name)
            # Open the file to read lines out of
            xml_file = open(xml_file_name, 'r')
            # Extract the contents from the file
            xml_file_contents = xml_file.readlines()
            # Remove the temp directory created for the zip contents
            shutil.rmtree(args_array['temp_directory'] + "/unzip/" + args_array['file_name'])
            # Close the file being read from
            zip_file.close()
            # Return the file contents as array
            return xml_file_contents

        except:
            # Print message to stdout
            print('[Zip file ' + args_array['temp_zip_file_name'] + ' failed to unzip with linux subprocess module]')
            logger.warning('Zip file ' + args_array['temp_zip_file_name'] + ' failed to unzip linux subprocess module')
            traceback.print_exc()

            # Attempt to download the file again
            try:
                # Print message to stdout
                print('[Removing corrupted zip file ' + args_array['temp_zip_file_name'] + ']')
                logger.warning('Removing corrupted file ' + args_array['temp_zip_file_name'])
                # Remove the corrupted zip file
                delete_zip_file(args_array['temp_zip_file_name'])
                # Return None to signal failed status
                return None
            except:
                # Print message to stdout
                print('[Failed to remove zip file ' + args_array['temp_zip_file_name'] + ' ]')
                logger.warning('Failed to remove zip file ' + args_array['temp_zip_file_name'])
                traceback.print_exc()
                # Return False to signify that zip file could not be deleted
                return False

    # Finally, if nothing was returned already, return None
    finally:
        pass
        #TODO: need to remove the zip file here if



# Extract a zip file and return the contents of the XML file as an array of lines
def extract_dat_file_from_zip(args_array):

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")

    # Extract the zipfile to read it
    try:
        zip_file = zipfile.ZipFile(args_array['temp_zip_file_name'], 'r')
        data_file_name = ""
        for name in zip_file.namelist():
            if '.dat' in name or '.txt' in name:
                data_file_name = name
        # If xml file not found, then print error message
        if data_file_name == "":
            # Print and log that the xml file was not found
            print('[APS .dat data file not found.  Filename{0}]'.format(args_array['url_link']))
            logger.error('APS .dat file not found. Filename: ' + args_array['url_link'])

        # Process zip file contents of .dat or .txt file and .xml files
        data_file_contents = zip_file.open(data_file_name,'r')

        # Close the zip file
        zip_file.close()

        # If not sandbox mode, then delete the .zip file
        if args_array['sandbox'] == False and os.path.exists(args_array['temp_zip_file_name']):
            # Print message to stdout
            print('[Purging .zip file ' + args_array['temp_zip_file_name'] + '...]')
            logger.info('Purging .zip file ' + args_array['temp_zip_file_name'] + '...')
            os.remove(args_array['temp_zip_file_name'])

        # Print message to stdout
        print('[data file contents extracted ' + data_file_name + '...]')
        logger.info('data file contents extracted ' + data_file_name + '...')
        # Return the file contents as array
        return data_file_contents

    # Since zip file could not unzip, remove it
    except:
        # Remove the zip file and return error code
        try:
            # Print message to stdout
            print('[Removing corrupted zip file ' + args_array['temp_zip_file_name'] + ']')
            logger.warning('Removing corrupted file ' + args_array['temp_zip_file_name'])
            # Remove the corrupted zip file
            delete_zip_file(args_array['temp_zip_file_name'])
            # Return None to signal failed status
            return None
        except:
            # Print message to stdout
            print('[Failed to remove zip file ' + args_array['temp_zip_file_name'] + ' ]')
            logger.error('Failed to remove zip file ' + args_array['temp_zip_file_name'])
            traceback.print_exc()
            # Return False to signify that zip file could not be deleted
            return False


# Deletes a zip file
def delete_zip_file(filename):

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")

    # Check that a zip file
    if ".zip" in filename:
        # Remove the file
        os.remove(filename)
        print("[.Zip file " + filename + " has been removed...]")
        logger.warning(".Zip file " + filename + " has been removed...")
