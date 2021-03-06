# USPTOProcessLinks.py
# USPTO Bulk Data Parser - Processes for Finding Links and Downloading Data Files
# Description: Processes links to data files.
# Author: Joseph Lee
# Email: joseph@ripplesoftware.ca
# Website: www.ripplesoftware.ca
# Github: www.github.com/rippledj/uspto

# Import Python Modules
import time
import re
import os
import sys
import shutil
import traceback
import urllib.request, urllib.parse, urllib.error
import ssl
from bs4 import BeautifulSoup

# Import USPTO Parser Functions
import USPTOLogger
import USPTOProcessXMLGrant
import USPTOProcessAPSGrant
import USPTOProcessXMLApplication
import USPTOExtractXML4Grant
import USPTOExtractXML2Grant
import USPTOExtractXML4Application
import USPTOExtractXML1Application

# Function to accept raw xml data and route to the appropriate function to parse
# either grant, application or PAIR data.
def extract_data_router(xml_data_string, args_array):

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")

    try:
        if args_array['uspto_xml_format'] == "gAPS":
            return extract_APS_grant(xml_data_string, args_array)
        elif args_array['uspto_xml_format'] == "gXML2":
            return USPTOExtractXML2Grant.extract_XML2_grant(xml_data_string, args_array)
        elif args_array['uspto_xml_format'] == "gXML4":
            return USPTOExtractXML4Grant.extract_XML4_grant(xml_data_string, args_array)
        elif args_array['uspto_xml_format'] == "aXML1":
            return USPTOExtractXML1Application.extract_XML1_application(xml_data_string, args_array)
        elif args_array['uspto_xml_format'] == "aXML4":
            return USPTOExtractXML4Application.extract_XML4_application(xml_data_string, args_array)
    except Exception as e:
        # Print and log general fail comment
        print("xml extraction failed for document type: " + args_array['uspto_xml_format'] + " link: " + args_array['url_link'])
        logger.error("xml extraction for document type: " + args_array['uspto_xml_format'] + " link: " + args_array['url_link'])
        # Print traceback
        traceback.print_exc()
        # Print exception information to file
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("Exception: " + str(exc_type) + " in Filename: " + str(fname) + " on Line: " + str(exc_tb.tb_lineno) + " Traceback: " + traceback.format_exc())


# This function accepts the filename and returns the file format code
def return_file_format_from_filename(file_name):

    # Declare XML type strings for regex
    format_types = {
        "gXML4":'ipgb.*.zip',
        "gXML2":'pgb.*.zip',
        "gXML2_4" : 'pgb2001.*.zip',
        "gAPS" : '[0-9]{4}.zip|pba.*.zip',
        "aXML4" : 'ipab.*.zip',
        "aXML1" : 'pab.*.zip'
    }

    # Check filetype and return value
    for key, value in list(format_types.items()):
        if re.compile(value).match(file_name):
            return key
        else:
            if re.compile(value).match(file_name.split("/")[-1]):
                return key

# Download a link into temporary memory and return filename
def download_zip_file(args_array):

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")
    # Set process start time
    start_time = time.time()
    # Strip the file from the url_link
    base_file_name = args_array['url_link'].split("/")[-1]
    # Set the context for SSL (not checking!)
    context = ssl.SSLContext()

    # Set the attempts number to 0
    download_attempts = 0
    max_attempts = 3
    # Loop for the max attempts
    while download_attempts < max_attempts:
        # Try to download the zip file to temporary location
        try:
            # Check if the file is in the downloads folder first
            if os.path.isfile(args_array['sandbox_downloads_dirpath'] + base_file_name):
                # Download the file and use system temp directory
                print('[Using previosly downloaded .zip file: {0}]'.format(args_array['sandbox_downloads_dirpath'] + base_file_name))
                # Use the previously downloaded file as the temp_zip filename
                return args_array['sandbox_downloads_dirpath'] + base_file_name
            else:
                print('[Downloading .zip file to sandbox directory: {0}]'.format(args_array['sandbox_downloads_dirpath'] + base_file_name))
                logger.info('Downloading .zip file to sandbox directory: {0}]'.format(args_array['sandbox_downloads_dirpath'] + base_file_name))
                with urllib.request.urlopen(args_array['url_link'], context=context) as response, open(args_array['sandbox_downloads_dirpath'] + base_file_name, 'wb') as out_file:
                    shutil.copyfileobj(response, out_file)
                print('[Downloaded .zip file: {0} Time:{1} Finish Time: {2}]'.format(base_file_name,time.time()-start_time, time.strftime("%c")))
                logger.info('Downloaded .zip file: {0} Time:{1} Finish Time: {2}]'.format(base_file_name,time.time()-start_time, time.strftime("%c")))
                # Return the file name
                return args_array['sandbox_downloads_dirpath'] + base_file_name

        except Exception as e:
            download_attempts += 1
            traceback.print_exc()
            print('Downloading  contents of ' + args_array['url_link'] + ' failed...')
            logger.info('Downloading  contents of ' + args_array['url_link'] + ' failed...')
            # Delete the failed zip file if it exists
            if os.path.exists(base_file_name):
                os.remove(base_file_name)
                print('Failed download contents of ' + args_array['url_link'] + ' have been purged...')
                logger.info('Failed download contents of ' + args_array['url_link'] + ' have been purged...')

# Function to route the extraction of raw data from a link
def process_link_file(args_array):

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")

    # Declare variable to track if file was extracted successfully
    file_processed_success = False
    file_processed_attempts = 0

    # Loop until file extraction completes or attempts exhausted
    while file_processed_success == False:
        # Download the file and append temp location to args array
        args_array['temp_zip_file_name'] = download_zip_file(args_array)

        #print args_array['uspto_xml_format']

        # Process the contents of file baed on type
        if args_array['uspto_xml_format'] == "gAPS":
            file_processed_success = USPTOProcessAPSGrant.process_APS_grant_content(args_array)
        elif args_array['uspto_xml_format'] == "aXML1" or args_array['uspto_xml_format'] == "aXML4":
            file_processed_success = USPTOProcessXMLApplication.process_XML_application_content(args_array)
        elif args_array['uspto_xml_format'] == "gXML2" or args_array['uspto_xml_format'] == "gXML4":
            file_processed_success = USPTOProcessXMLGrant.process_XML_grant_content(args_array)

        # If the file was not extracted add to attempts count
        if file_processed_success == False:
            file_processed_attempts += 1
            # If the file extraction limit breached then break loop
            if file_processed_attempts > 2:
                print("Extraction process for contents of: " + args_array['url_link'] + " failed 3 times at: " + time.strftime("%c"))
                logger.warning("Extraction process for contents of: " + args_array['url_link'] + " failed 3 times at: " + time.strftime("%c"))
                break
        # If the database insertion failed then break the loop
        elif file_processed_success == None:
            break
        # If the file was processed then
        elif file_processed_success == True:
            # Print to stdout and log
            print("Finished the data storage process for contents of: " + args_array['url_link'] + " Finished at: " + time.strftime("%c"))
            logger.info("Finished the data storage process for contents of: " + args_array['url_link'] + " Finished at: " + time.strftime("%c"))


# Collect all patent grant and publications data files
def get_all_links(args_array):

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")

    # returns a list
    # PG = Patent Grants
    # PA = Patent Applications

    # Patent grant and application bulk data url
    if args_array['bulk_data_source'] == "uspto":
        bulk_data_url = args_array['uspto_bulk_data_url']
    elif args_array['bulk_data_source'] == "reedtech":
        bulk_data_url = args_array['reedtech_bulk_data_url']
    # Classification url
    url_source_UPC_class = args_array["uspto_classification_data_url"]

    # TODO: fix the classification parser
    print('Started grabbing patent classification links... ' + time.strftime("%c"))
    classification_linklist = []
    classification_linklist.append([args_array['classification_text_filename'], "None"])
    print('Finished grabbing patent classification links... ' + time.strftime("%c"))
    # Log finished building all zip filepaths
    logger.info('Finished grabbing patent classification bibliographic links: ' + time.strftime("%c"))

    # Get all patent grant data
    print('Started grabbing patent grant bibliographic links... ' + time.strftime("%c"))
    grant_linklist = links_parser("PG", args_array['bulk_data_source'], bulk_data_url)
    print('Finished grabbing patent grant bibliographic links... ' + time.strftime("%c"))
    # Log finished building all zip filepaths
    logger.info('Finished grabbing patent grant bibliographic links: ' + time.strftime("%c"))

    # Get all patent application data
    print('Started grabbing patent application bibliographic links... ' + time.strftime("%c"))
    application_linklist = links_parser("PA", args_array['bulk_data_source'], bulk_data_url)
    print('Finished grabbing patent application bibliographic links... ' + time.strftime("%c"))
    # Log finished building all zip filepaths
    logger.info('Finished grabbing patent application bibliographic links: ' + time.strftime("%c"))

    #print 'Started grabbing patent application pair bibliographic links... ' + time.strftime("%c")
    # Get all patent application pair data
    #application_pair_linklist = links_parser("PAP", bulk_data_url)
    #print 'Finished grabbing patent application pair bibliographic links... ' + time.strftime("%c")
    # Log finished building all zip filepaths
    #logger.info('Finished grabbing patent application pair bibliographic links: ' + time.strftime("%c"))

    # Return the array of arrays of required links
    return {"grants" : grant_linklist, "applications" : application_linklist, "classifications" : classification_linklist}

# Parse USPTO bulk-data site to get document links
def links_parser(link_type, bulk_data_source, bulk_source_url):

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")
    print("Grabbing " + link_type + " links using " + bulk_data_source + " data source...")

    # Define array to hold all links found
    link_array = []
    temp_zip_file_link_array = []
    final_zip_file_link_array = []
    annualized_file_found = False
    annualized_file_link = ""

    # If using USPTO bulk data source
    if bulk_data_source == "uspto":
        # Set the context for SSL (not checking!)
        context = ssl.SSLContext()
        # First collect all links on USPTO bulk data page
        content = urllib.request.urlopen(bulk_source_url, context=context).read()
        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all('a', href=True):
            # Collet links based on type requested by argument in function call

            # Patent grant
            if link_type == "PG":
                if "https://bulkdata.uspto.gov/data/patent/grant/redbook/bibliographic/" in link['href']:
                    link_array.append(link['href'])
            # Patent Application
            elif link_type == "PA":
                if "https://bulkdata.uspto.gov/data/patent/application/redbook/bibliographic/" in link['href']:
                    link_array.append(link['href'])
            # Patent Application Pair
            elif link_type == "PAP":
                if "" in link['href']:
                    link_array.append(link['href'])

        # Go through each found link on the main USPTO page and get the zip files as links and return that array.
        for item in link_array:
            content = urllib.request.urlopen(item, context=context).read()
            soup = BeautifulSoup(content, "html.parser")
            for link in soup.find_all('a', href=True):
                if ".zip" in link['href']:
                    # Check if an annualized link.  If annualized link found then add flag so ONLY that link can be added
                    if re.compile("[0-9]{4}.zip").match(link['href']):
                        annualized_file_link = [item + "/" + link['href'], return_file_format_from_filename(link['href'])]
                        annualized_file_found = True
                    elif re.compile("[0-9]{4}[0-9_]{1,4}_xml.zip").match(link['href']) is None and re.compile("[0-9]{4}_xml.zip").match(link['href']) is None:
                        temp_zip_file_link_array.append([item + "/" + link['href'], return_file_format_from_filename(link['href'])])

            # Check if Annualized file found
            if annualized_file_found == True:
                if annualized_file_link not in final_zip_file_link_array:
                    # Append to the array with format_type
                    final_zip_file_link_array.append(annualized_file_link)
            else:
                for link in temp_zip_file_link_array:
                    if link not in final_zip_file_link_array:
                        final_zip_file_link_array.append(link)

    # If using Reedtech bulk data source
    if bulk_data_source == "reedtech":
        if link_type == "PG":
            full_source_url = bulk_source_url + "pgrbbib.php"
        elif link_type == "PA":
            full_source_url = bulk_source_url + "parbbib.php"

        # Set the context for SSL (not checking!)
        context = ssl.SSLContext()
        # First collect all links on USPTO bulk data page
        content = urllib.request.urlopen(full_source_url, context=context).read()
        soup = BeautifulSoup(content, "html.parser")
        for link in soup.find_all('a', href=True):
            # Collet links based on type requested by argument in function call

            # Patent grant
            if link_type == "PG":
                if "downloads/GrantRedBookBib/" in link['href'] and ".zip" in link['href'] and not is_duplicate_link("PG", link['href']):
                    final_zip_file_link_array.append([bulk_source_url + link['href'], return_file_format_from_filename(link['href'])])
            # Patent Application
            elif link_type == "PA":
                if "downloads/ApplicationRedBookBib/" in link['href'] and ".zip" in link['href'] and not is_duplicate_link("PA", link['href']):
                    final_zip_file_link_array.append([bulk_source_url + link['href'], return_file_format_from_filename(link['href'])])
            # Patent Application Pair
            elif link_type == "PAP":
                if "" in link['href']:
                    final_zip_file_link_array.append([bulk_source_url + link['href'], return_file_format_from_filename(link['href'])])

    print("Number of downloadable " + link_type + " .zip files found = " + str(len(final_zip_file_link_array)))
    logger.info("Number of downloadable " + link_type + " .zip files found = " + str(len(final_zip_file_link_array)))
    # Return the array links to zip files with absolute urls
    #print(final_zip_file_link_array)
    return final_zip_file_link_array

# Checks if link should be removed because duplicate of weekly
def is_duplicate_link(type, link):
    # Get the filename from link
    link = link.split("/")[-1]
    if type == "PG":
        #links_to_remove = ["2001.zip", "2000.zip", "1999.zip", "1998.zip", "1997.zip", "1996.zip"]
        links_to_remove = ["pgb2001", "pba2000", "pba1999", "pba1998",
        "pba1997", "pba1996"]
        is_duplicate = False
        for item in links_to_remove:
            if item in link:
                is_duplicate = True
        if is_duplicate: return True
        else: return False
    elif type == "PA":
        links_to_remove = [""]
        if link in links_to_remove:
            return True
        else: return False
