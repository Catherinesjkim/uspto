# USPTOExtractXML2Grant.py
# USPTO Bulk Data Parser - Extract XML 2 Grants
# Description: Imported to the main USPTOParser.py.  Extracts grant data from USPTO XML v2 files.
# Author: Joseph Lee
# Email: joseph@ripplesoftware.ca
# Website: www.ripplesoftware.ca
# Github: www.github.com/rippledj/uspto

# Import Python Modules
import xml.etree.ElementTree as ET
import time
import traceback
import os
import sys
import re

# Import USPTO Parser Functions
import USPTOLogger
import USPTOSanitizer

# Function used to extract data from XML2 formatted patent grants
def extract_XML2_grant(raw_data, args_array):

    #
    # Data documentation on the fields in XML2 Grant data can be found
    # in the /documents/data_descriptions/PatentGrantSGMLv19-Documentation.pdf file
    #

    # Import logger
    logger = USPTOLogger.logging.getLogger("USPTO_Database_Construction")

    # Pass the url_link and format into local variables
    url_link = args_array['url_link']
    uspto_xml_format = args_array['uspto_xml_format']

    #print raw_data

    # Define all arrays needed to hold the data
    processed_grant = []
    processed_applicant = []
    processed_examiner = []
    processed_assignee = []
    processed_agent = []
    processed_inventor = []
    processed_usclass = []
    processed_intclass = []
    processed_gracit = []
    processed_forpatcit = []
    processed_nonpatcit = []
    processed_foreignpriority = []

    # Start timer
    start_time = time.time()

    try:
        # Pass the raw data into Element tree xml object
        patent_root = ET.fromstring(raw_data)

    except ET.ParseError as e:
        print_xml = raw_data.split("\n")
        for num, line in enumerate(print_xml, start = 1):
            print(str(num) + ' : ' + line)
        logger.error("Character Entity prevented ET from parsing XML in file: " + url_link )
        # Print traceback
        traceback.print_exc()
        # Print exception information to file
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        logger.error("Exception: " + str(exc_type) + " in Filename: " + str(fname) + " on Line: " + str(exc_tb.tb_lineno) + " Traceback: " + traceback.format_exc())


    # Start the parsing process for XML
    for r in patent_root.findall('SDOBI'):

        # Collect main grant document data
        for B100 in r.findall('B100'):
            try:
                document_id = USPTOSanitizer.return_element_text(B100.find('B110'))
                document_id = USPTOSanitizer.fix_patent_number(document_id)[:20]
            except:
                document_id = None
                logger.error("No Patent Number was found for: " + url_link)
            try:
                kind = USPTOSanitizer.return_element_text(B100.find('B130'))[:2]
                app_type = USPTOSanitizer.return_xml2_app_type(args_array, kind)
            except: kind = None
            try:
                # PATENT ISSUE DATE
                pub_date = USPTOSanitizer.return_formatted_date(USPTOSanitizer.return_element_text(B100.find('B140')), args_array, document_id)
            except: pub_date = None
            try:
                # PATENT APPLICANT COUNTRY??
                pub_country = USPTOSanitizer.return_element_text(B100.find('B190'))
            except: pub_country = None

        # Collect apllication data in document
        for B200 in r.findall('B200'):
            # TODO: find this in XML2 applications
            app_country = None
            try:
                # Application number
                app_no = USPTOSanitizer.return_element_text(B200.find('B210'))[:20]
            except: app_no = None
            try:
                # Application date
                app_date = USPTOSanitizer.return_formatted_date(USPTOSanitizer.return_element_text(B200.find('B220')), args_array, document_id)
            except: app_date = None
            try:
                series_code = USPTOSanitizer.return_element_text(B200.find('B211US'))[:2]
            except: series_code = None

        # Collect the grant length
        grant_length = USPTOSanitizer.return_element_text(r.find("B474"))

        # Collect US classification
        for B500 in r.findall('B500'):
            # US Classification
            for B520 in B500.findall('B520'):
                position = 1
                # USCLASS
                for B521 in B520.findall('B521'):
                    n_class_info = USPTOSanitizer.return_element_text(B521)
                    n_class_main, n_subclass = USPTOSanitizer.return_class(n_class_info)
                    n_class_main = n_class_main[:5]
                    n_subclass = n_subclass[:15]

                    # Append SQL data into dictionary to be written later
                    processed_usclass.append({
                        "table_name" : "uspto.USCLASS_G",
                        "GrantID" : document_id,
                        "Position" : position,
                        "Class" : n_class_main,
                        "SubClass" : n_subclass,
                        "FileName" : args_array['file_name']
                    })

                    position += 1
                for B522 in B520.findall('B522'):
                    # USCLASS FURTHER
                    n_class_info = USPTOSanitizer.return_element_text(B522)
                    n_class_main, n_subclass = USPTOSanitizer.return_class(n_class_info)
                    n_class_main = n_class_main[:5]
                    n_subclass = n_subclass[:15]

                    # Append SQL data into dictionary to be written later
                    processed_usclass.append({
                        "table_name" : "uspto.USCLASS_G",
                        "GrantID" : document_id,
                        "Position" : position,
                        "Class" : n_class_main,
                        "SubClass" : n_subclass,
                        "FileName" : args_array['file_name']
                    })

                    position += 1

            # Collect International Class data
            # TODO: check if I need to set all variables to empty or can just leave as null
            # TODO: check if classification is parsed correctly
            for B510 in B500.findall('B510'): # INTERNATIONAL CLASS
                #logger.warning("International Classifcation found in XML2: " + args_array['url_link'] + " document: " + str(document_id))
                # Reset position
                position = 1
                for B511 in B510.findall('B511'): #MAIN CLASS
                    i_class_version_date = None
                    i_class_action_date = None
                    i_class_gnr = None
                    i_class_level = None
                    i_class_sec = None
                    int_class = USPTOSanitizer.return_element_text(B511)
                    # TODO: check international classification and rewrite this parsing piece.
                    if(len(int_class.split())>1):
                        i_class, i_subclass = int_class.split()
                        i_class = i_class[:15]
                        i_subclass = i_subclass[:15]
                    else:
                        i_class = int_class[:15]
                        i_subclass = None
                    i_class_mgr = None
                    i_class_sgr = None
                    i_class_sps = None
                    i_class_val = None
                    i_class_status = None
                    i_class_ds = None

                    # Append SQL data into dictionary to be written later
                    processed_intclass.append({
                        "table_name" : "uspto.INTCLASS_G",
                        "GrantID" : document_id,
                        "Position" : position,
                        "Section" : i_class_sec,
                        "Class" : i_class,
                        "SubClass" : i_subclass,
                        "MainGroup" : i_class_mgr,
                        "SubGroup" : i_class_sgr,
                        "FileName" : args_array['file_name']
                    })

                    position += 1

                #INTERNATIONAL CLASS FURTHER
                for B512 in B510.findall('B511'):
                    i_class_version_date = None
                    i_class_action_date = None
                    i_class_gnr = None
                    i_class_level = None
                    i_class_sec = None
                    int_class = USPTOSanitizer.return_element_text(B512)
                    # TODO: splitting int class does not include possible multiple subclasses
                    if(len(int_class.split())>1):
                        i_class = int_class.split()[0][:15]
                        i_subclass = int_class.split()[1][:15]
                    else:
                        i_class = int_class[:15]
                        i_subclass = None
                    i_class_mgr = None
                    i_class_sgr = None
                    i_class_sps = None
                    i_class_val = None
                    i_class_status = None
                    i_class_ds = None

                    # Append SQL data into dictionary to be written later
                    processed_intclass.append({
                        "table_name" : "uspto.INTCLASS_G",
                        "GrantID" : document_id,
                        "Position" : position,
                        "Section" : i_class_sec,
                        "Class" : i_class,
                        "SubClass" : i_subclass,
                        "MainGroup" : i_class_mgr,
                        "SubGroup" : i_class_sgr,
                        "FileName" : args_array['file_name']
                    })

                    position += 1

            # Collect Tite
            for B540 in B500.findall('B540'):
                try: title = USPTOSanitizer.return_element_text(B540)[:500]
                except: title = None

            # Collect Citations
            for B560 in B500.findall('B560'): # CITATIONS

                # Reset position counter for all citations loop
                position = 1

                for B561 in B560.findall('B561'): #PATCIT
                    # TODO: find out how to do PCIT, DOC without loop.  Only B561 needs loop
                    PCIT = B561.find('PCIT')
                    # Determien if the patent is US or not
                    #TODO: needs to check better, what does non US patent look like
                    # If all patents have PARTY-US then perhaps a databse call to check the country of origin
                    # would still allow to separate into GRACIT and FORPATCIT_G
                    #if PCIT.find("PARTY-US") == True:
                        #print "CiTATION OUNTRY US"
                        #citation_country == "US"
                    #else:
                        #citation_country = "NON-US"
                        #logger.warning("NON US patent found")

                    citation_country = "US"

                    DOC = PCIT.find('DOC')
                    try: citation_document_number = USPTOSanitizer.return_element_text(DOC.find('DNUM'))[:15]
                    except: citation_document_number = None
                    try: pct_kind = USPTOSanitizer.return_element_text(DOC.find('KIND'))[:10]
                    except: pct_kind = None
                    try: citation_date = USPTOSanitizer.return_formatted_date(USPTOSanitizer.return_element_text(DOC.find('DATE'), args_array, document_id))
                    except: citation_date = None
                    try: citation_name = USPTOSanitizer.return_element_text(PCIT.find('PARTY-US'))[:100]
                    except: citation_name = None

                    # Parse citation category
                    if(len(B561.getchildren()) > 1):
                        citation_category = B561.getchildren()[1].tag.replace("\n", "").replace("\r", "")
                        #print type(citation_category)
                        # TODO: check that the citation category tag matches correctly
                        #print "Citation Category = " + citation_category + " Length: " + str(len(citation_category))
                        if "CITED-BY-EXAMINER" in citation_category:
                            citation_category = 1
                        elif "CITED-BY-OTHER" in citation_category:
                            citation_category = 2
                        else:
                            citation_category = 0
                            logger.warning("Cited by unknown type")
                    else: citation_category = None

                    #TODO: be aware that there may be something crazy in the citation document number
                    if citation_country == "US":

                        # Append SQL data into dictionary to be written later
                        processed_gracit.append({
                            "table_name" : "uspto.GRACIT_G",
                            "GrantID" : document_id,
                            "Position" : position,
                            "CitedID" : citation_document_number,
                            "Kind" : pct_kind,
                            "Name" : citation_name,
                            "Date" : citation_date,
                            "Country" : citation_country,
                            "Category" : citation_category,
                            "FileName" : args_array['file_name']
                        })

                        position += 1

                    else:

                        # Append SQL data into dictionary to be written later
                        processed_forpatcit.append({
                            "table_name" : "uspto.FORPATCIT_G",
                            "GrantID" : document_id,
                            "Position" : position,
                            "CitedID" : citation_document_number,
                            "Kind" : pct_kind,
                            "Name" : citation_name,
                            "Date" : citation_date,
                            "Country" : citation_country,
                            "Category" : citation_category,
                            "FileName" : args_array['file_name']
                        })

                        position += 1

                # Reset position counter for non-patent citations loop
                position = 1
                for B562 in B560.findall('B562'): #NON-PATENT LITERATURE
                    for NCIT in B562.findall('NCIT'):
                        # sometimes, there will be '<i> or <sup>, etc.' in the reference string; we need to remove it
                        non_patent_citation_text = USPTOSanitizer.return_element_text(NCIT)
                        non_patent_citation_text = re.sub('<[^>]+>','',non_patent_citation_text)

                        # parse citation cateory into code
                        ncitation_category = ET.tostring(NCIT)
                        if(len(B562.getchildren())>1):
                            ncitation_category = B562.getchildren()[1].tag.replace("\n", "").replace("\r", "")
                            #print type(ncitation_category)
                            #rint "Non patent citation category" + ncitation_category
                        if "CITED-BY-EXAMINER" in ncitation_category:
                            ncitation_category = 1
                        elif "CITED-BY-OTHER" in ncitation_category:
                            ncitation_category = 2
                        else:
                            ncitation_category = 0


                    # Append SQL data into dictionary to be written later
                    processed_nonpatcit.append({
                        "table_name" : "uspto.NONPATCIT_G",
                        "GrantID" : document_id,
                        "Position" : position,
                        "Citation" : non_patent_citation_text,
                        "Category" : ncitation_category,
                        "FileName" : args_array['file_name']
                    })

                    position += 1

            # Collect number of claims
            for B570 in B500.findall('B570'):
                try: claims_num = USPTOSanitizer.return_element_text(B570.find('B577'))
                except: claims_num = None

            # Collect number of drawings and figures
            for B590 in B500.findall('B590'):
                for B595 in B590.findall('B595'):
                    try:
                        number_of_drawings = USPTOSanitizer.return_element_text(B595)
                        number_of_drawings = number_of_drawings.split("/")[0]
                    except: number_of_drawings = None
                for B596 in B590.findall('B596'):
                    try: number_of_figures = USPTOSanitizer.return_element_text(B596)
                    except: number_of_figures = None

            # TODO: B582 find out what it is.  Looks like patent classifications but it's all alone in the XML

        # Collect party information
        # TODO: find the applicant data and append to array
        for B700 in r.findall('B700'): #PARTIES

            # Collect inventor data
            for B720 in B700.findall('B720'): #INVENTOR
                # Reset position for inventors
                position = 1

                # Collect inventor information
                for B721 in B720.findall('B721'):
                    for i in B721.findall('PARTY-US'):
                        itSequence = position
                        try: inventor_first_name = USPTOSanitizer.return_element_text(i.find('NAM').find('FNM'))[:100]
                        except: inventor_first_name = None
                        try: inventor_last_name = USPTOSanitizer.return_element_text(i.find('NAM').find('SNM'))[:100]
                        except: inventor_last_name = None
                        try: inventor_city = USPTOSanitizer.return_element_text(i.find('ADR').find('CITY'))[:100]
                        except: inventor_city = None
                        try:
                            inventor_state = USPTOSanitizer.return_element_text(i.find('ADR').find('STATE'))[:3]
                        except: inventor_state = None
                        # Inventor country
                        try: inventor_country = USPTOSanitizer.return_element_text(x.find("ADR").find('CTRY'))[:3]
                        except:
                            try:
                                if USPTOSanitizer.is_US_state(inventor_state):
                                    inventor_country = "US"
                                else:
                                    inventor_country = None
                            except: inventor_country = None
                        inventor_nationality = None
                        inventor_residence = None

                    # Append SQL data into dictionary to be written later
                    processed_inventor.append({
                        "table_name" : "uspto.INVENTOR_G",
                        "GrantID" : document_id,
                        "Position" : position,
                        "FirstName" : inventor_first_name,
                        "LastName" : inventor_last_name,
                        "City" : inventor_city,
                        "State" : inventor_state,
                        "Country" : inventor_country,
                        "Nationality" : inventor_nationality,
                        "Residence" : inventor_residence,
                        "FileName" : args_array['file_name']
                    })

                    position += 1

            # Collect Assignee data
            # TODO: check if finding child of child is working
            # Reset position for assignees
            position = 1
            for B730 in B700.findall('B730'):
                for B731 in B730.findall('B731'):
                    for x in B731.findall('PARTY-US'):
                        try: asn_orgname = USPTOSanitizer.return_element_text(x.find('NAM').find("ONM"))[:500]
                        except: asn_orgname = None
                        asn_role = None
                        try: asn_city = USPTOSanitizer.return_element_text(x.find("ADR").find('CITY'))[:100]
                        except: asn_city = None
                        try: asn_state = USPTOSanitizer.return_element_text(x.find("ADR").find('STATE'))[:30]
                        except: asn_state = None
                        # Assignee country
                        try:
                            asn_country = USPTOSanitizer.return_element_text(x.find("ADR").find('CTRY'))[:3]
                        except:
                            try:
                                if USPTOSanitizer.is_US_state(asn_state):
                                    asn_country = "US"
                                else:
                                    asn_country = None
                            except: asn_country = None

                    # Append SQL data into dictionary to be written later
                    processed_assignee.append({
                        "table_name" : "uspto.ASSIGNEE_G",
                        "GrantID" : document_id,
                        "Position" : position,
                        "OrgName" : asn_orgname,
                        "Role" : asn_role,
                        "City" : asn_city,
                        "State" :  asn_state,
                        "Country" : asn_country,
                        "FileName" : args_array['file_name']
                    })

                    # Increment the position placement
                    position += 1

            # Collect agent data
            for B740 in B700.findall('B740'):
                # Reset position for agents
                position = 1
                for B741 in B740.findall('B741'):
                    for x in B741.findall('PARTY-US'):
                        try: agent_orgname = USPTOSanitizer.return_element_text(x.find('NAM').find("ONM"))[:300]
                        except: agent_orgname = None
                        try: agent_last_name = USPTOSanitizer.return_element_text(x.find('NAM').find('FNM'))[:100]
                        except: agent_last_name = None
                        try: agent_first_name = USPTOSanitizer.return_element_text(x.find('NAM').find('SNM'))[:100]
                        except: agent_first_name = None
                        # Attorney Address information
                        try: agent_city = USPTOSanitizer.return_element_text(x.find("ADR").find('CITY'))[:100]
                        except: agent_city = None
                        try: agent_state = USPTOSanitizer.return_element_text(x.find("ADR").find('STATE'))[:30]
                        except: agent_state = None
                        # Agent country
                        try:
                            agent_country = USPTOSanitizer.return_element_text(x.find("ADR").find('CTRY'))[:3]
                        except:
                            try:
                                if USPTOSanitizer.is_US_state(agent_state):
                                    agent_country = "US"
                                else:
                                    agent_country = None
                            except: agent_country = None

                        # Append SQL data into dictionary to be written later
                        processed_agent.append({
                            "table_name" : "uspto.AGENT_G",
                            "GrantID" : document_id,
                            "Position" : position,
                            "OrgName" : agent_orgname,
                            "LastName" : agent_last_name,
                            "FirstName" : agent_first_name,
                            "Country" : agent_country,
                            "FileName" : args_array['file_name']
                        })

                        position += 1

            # Collect examiner data
            for B745 in B700.findall('B745'):
                position = 1
                # Primary Examiner
                for B746 in B745.findall('B746'):
                    for x in B746.findall('PARTY-US'):
                        try: examiner_last_name = USPTOSanitizer.return_element_text(x.find('NAM').find('SNM'))[:50]
                        except: examiner_last_name = None
                        try: examiner_fist_name = USPTOSanitizer.return_element_text(x.find('NAM').find('FNM'))[:50]
                        except:  examiner_fist_name = None
                        #TODO: find out if 748US is the department
                        examiner_department = None

                        # Append SQL data into dictionary to be written later
                        processed_examiner.append({
                            "table_name" : "uspto.EXAMINER_G",
                            "GrantID" : document_id,
                            "Position" : position,
                            "LastName" :  examiner_last_name,
                            "FirstName" : examiner_fist_name,
                            "Department" : examiner_department,
                            "FileName" : args_array['file_name']
                        })

                        position += 1

                # Assistant Examiner
                for B747 in B745.findall('B747'):
                    for x in B747.findall('PARTY-US'):
                        try: examiner_last_name = USPTOSanitizer.return_element_text(x.find('NAM').find('SNM'))[:50]
                        except: examiner_last_name = None
                        try: examiner_fist_name = USPTOSanitizer.return_element_text(x.find('NAM').find('FNM'))[:50]
                        except: examiner_fist_name = None
                        #TODO: find out if 748US is the department
                        examiner_department = None

                        # Append SQL data into dictionary to be written later
                        processed_examiner.append({
                            "table_name" : "uspto.EXAMINER_G",
                            "GrantID" : document_id,
                            "Position" : position,
                            "LastName" :  examiner_last_name,
                            "FirstName" : examiner_fist_name,
                            "Department" : examiner_department,
                            "FileName" : args_array['file_name']
                        })

                        position += 1

        # Collect foreign priotiry data
        position = 1
        for B300 in r.findall('B300'):
            # Country
            try: pc_country = USPTOSanitizer.return_element_text(B300.find('B330').find('CTRY'))[:5]
            except: pc_country = None
            # Prority filing date
            try: pc_date = USPTOSanitizer.return_formatted_date(USPTOSanitizer.return_element_text(B300.find('B320').find('DATE'))[:45])
            except: pc_date = None
            # Prority document number
            try: pc_doc_num = USPTOSanitizer.return_element_text(B300.find('B310').find('DNUM'))[:45]
            except: pc_doc_dum = None

            # Set the fields that are not in gXML2
            pc_kind = None

            # Append SQL data into dictionary to be written later
            processed_foreignpriority.append({
                "table_name" : "uspto.FOREIGNPRIORITY_G",
                "GrantID" : document_id,
                "Position" : position,
                "Kind" : pc_kind,
                "Country" : pc_country,
                "DocumentID" : pc_doc_num,
                "PriorityDate" : pc_date,
                "FileName" : args_array['file_name']
            })
            #print(processed_foreignpriority)
            # Increment Position
            position += 1

        # Collect Abstract from data
        try:
            abstr = patent_root.find('SDOAB')
            abstract = USPTOSanitizer.return_element_text(abstr).strip()
            #print abstract
        except: abstract = None

        # Collect claims from data
        try:
            cl = patent_root.find('SDOCL')
            claims = USPTOSanitizer.return_element_text(cl)
            #print claims
        except:
            traceback.print_exc()
            claims = None


        # Append SQL data into dictionary to be written later
        processed_grant.append({
            "table_name" : "uspto.GRANT",
            "GrantID" : document_id,
            "Title" : title,
            "IssueDate" : pub_date,
            "Kind" : kind,
            "GrantLength" : grant_length,
            "USSeriesCode" : series_code,
            "Abstract" : abstract,
            "ClaimsNum" : claims_num,
            "DrawingsNum" : number_of_drawings,
            "FiguresNum" : number_of_figures,
            "ApplicationID" : app_no,
            "Claims" : claims,
            "FileDate" : app_date,
            "AppType" : app_type,
            "FileName" : args_array['file_name']
        })


    # Return a dictionary of the processed_ data arrays
    return {
        "processed_grant" : processed_grant,
        "processed_applicant" : processed_applicant,
        "processed_examiner" : processed_examiner,
        "processed_assignee" : processed_assignee,
        "processed_agent" : processed_agent,
        "processed_inventor" : processed_inventor,
        "processed_usclass" : processed_usclass,
        "processed_intclass" : processed_intclass,
        "processed_gracit" : processed_gracit,
        "processed_forpatcit" : processed_forpatcit,
        "processed_nonpatcit" : processed_nonpatcit,
        "processed_foreignpriority" : processed_foreignpriority
    }
