import regex as re

class RegexRedactor:
    def __init__(self):
        self.__honorifics_pattern = r'(?:Mr|Mrs|Ms|Miss|Mx|Dr)\.?'
        self.__patterns = [
            # Pattern, Replacement, [Optional additional flags]

            # Username
            ( r'\b(?:SSO ID|SSO Username|Directory ID|Network ID|NetID|Net ID|LDAP ID|Active Directory ID|AD Username|Windows Login|Workstation Login|Computer Login|Portal ID|Portal Username|Profile ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_-]{5,15}', "[SYSTEM ID]", re.IGNORECASE ),
            ( r'(?<=username\s*[:\-]?\s*)[A-Za-z0-9._-]+', "[USERNAME]", re.IGNORECASE ),
            ( r'(?<=user name\s*[:\-]?\s*)[A-Za-z0-9._-]+', "[USERNAME]", re.IGNORECASE ),
            ( r'\b(?:Username|User Name|UserID|User ID|System Username|Account Username|Login Username|Account Login|Login Name|Handle|Screen Name|Display Name|Profile Name)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._-]{5,15}', "[SYSTEM USERNAME]", re.IGNORECASE ),

            # Login ID
            ( r'\b(?:Email Login|Email Username|Office365 Login|Google Login|School Login Email|Office 365 Login)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_.-]{3,40}', "[EMAIL LOGIN]", re.IGNORECASE ),
            ( r'(?<=login id\s*[:\-]?\s*)[A-Za-z0-9._-]+', "[LOGIN ID]", re.IGNORECASE ),

            # Accounts
            #( r'(?<=account\s*[:\-]?\s*)[A-Za-z0-9._-]+', "[ACCOUNT]", re.IGNORECASE ),

            # Email Addresses 
            # [a-zA-Z0-9_.+-]+ - Repeated one or more times: Any lowercase/capital letter, number, underscore, period, plus sign, and dash
            # @ - Symbol splitting local part and domain 
            # [a-zA-Z0-9-]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
            # \. - Matches one period
            # [a-zA-Z0-9-.]+ - Repeated one or more times: Any lowercase/capital letter, number, and dash
            ( r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', "[EMAIL]" ),

            # Social Handle
            ( r'@[A-Za-z0-9._-]+', "[SOCIAL MEDIA]" ),

            # Web URL
            ( r"(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))", "[URL]", re.IGNORECASE ),

            # PO Box
            ( r'\b(?:P\.?\s*O\.?\s*(?:Box|Bin)|Post\s+Office\s+(?:Box|Bin)|(?:Box|Bin)\s*#?\s*\d+|#\s*\d+|Number\s*\d+)\b', "[PO BOX]", re.IGNORECASE ),

            # Health Insurance Policy/Member numbers
            ( r'(?:Policy No|Policy Number|Policy ID|Member #|Subscriber No|Coverage ID|Insurance #|Group ID|Plan ID|Plan #|Member ID|Policy #|Subscriber ID|Group #|Group Number|Insurance ID|Coverage #)\s*[:\-]?\s*[A-Za-z0-9- _/.]{4,20}', "[HEALTH INSURANCE #]", re.IGNORECASE ),

            # Routing Number
            ( r'(?<=\b(?:routing|aba|rtn)(?:\s+number)?\s*[:\-]?\s*)\d{9}\b', "[ROUTING #]", re.IGNORECASE ),

            # Bank Account Info
            ( r'(?:Account Number|Account #|Acct No|Acct #|Bank Account|Checking Account|Savings Acct|Account|Acct|Savings Account|Account Num|Acct Num|Acct Number|A/C No|A/C|ACCT#|AccountNo)\s*[:.\-]?\s*[-0-9_/ .A-Za-z]{6,17}', "[BANK ACCOUNT]", re.IGNORECASE ),

            # GPS Coordinate
            ( r'(?:Lat|Lon|Lat/Lon|Latitude|Longitude|Long|Lat-Log|Lat-Lon|GPS|GPS COORDINATES|Lat/Long)\s*[,:.\-]?\s*[+-]?\d{1,3}\.\d+\s*[NESW]?(?:\s*[, ]\s*[+-]?\d{1,3}\.\d+\s*[NESW]?)?', "[COORDINATE]", re.IGNORECASE ),

            # GPS Device ID
            ( r'\b(?:GPS ID|GPS Device ID|GPS Tracker ID|Tracking Device Number|Location Tracker ID|Unit ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_.-]{4,40}', "[GPS DEVICE]", re.IGNORECASE ),

            # Employment ID
            ( r'\b(?:Employee Number|Employee #|Employee No|Employee ID|Worker ID|Worker Number|Staff ID|Staff Number|Staff #|HR ID|Payroll ID|Payroll Number|Pay ID|Badge Number|Badge #|Contractor ID|Vendor ID|Associate ID|Operator ID)\b\s*[:#=.–—-]?\s*[0-9]{3,9}', "[EMPLOYMENT]", re.IGNORECASE ),

            # Employment Role
            ( r'\b(?:Job Title|Position Title|Role Title|Position|Job Level|Job Code|Employee Level|Band|Pay Grade|Pay Band|Department|Division|Team|Cost Center|Reporting To|Reports To|Supervisor|Supervisor Name|Manager|Manager Name|Direct Manager|Line Manager)\b\s*[:#=.–—-]?\s*[A-Za-z0-9\s&/.-]{3,40}', "[EMPLOYMENT ROLE]", re.IGNORECASE ),

            # Employment Evaluation Performance
            ( r'\b(?:Performance Rating|Performance Score|Performance Evaluation|Evaluation Rating|Evaluation Score|Review Rating|Review Score|Performance Review|Appraisal Rating|Appraisal Score|Goal Completion|KPI Score|KPI Rating|Objective Score|Performance Band|Performance Level)\b\s*[:#=.–—-]?\s*[A-Za-z0-9\s%/.-]{3,40}', "[EMPLOYMENT EVALUATION]", re.IGNORECASE ),

            # Employment Status
            ( r'\b(?:Employment Status|Job Status|Status|Employee Status|Work Status|Full-Time/Part-Time|FTE Status|Contract Type|Contract Status|Termination Reason|Separation Reason|Termination Type)\b\s*[:#=.–—-]?\s*[A-Za-z\s/-]{3,30}', "[EMPLOYMENT STATUS]", re.IGNORECASE ),

            # Academic Transcript ID
            ( r'\b(?:Transcript Number|Record Number|Academic Record ID|Report ID)\b\s*[:#=.–—-]?\s*[0-9]{3,7}', "[TRANSCRIPT ID]", re.IGNORECASE ),

            # Grades Score
            ( r'\b(?:Grade|Final Grade|Course Grade|Letter Grade|Exam Grade|Test Grade|Quiz Grade|Assignment Grade|Midterm Grade|Final Exam Grade|Score|Test Score|Exam Score|Quiz Score|Assignment Score|Final Score|Overall Score|Percentage|Percent Score|Percent Grade)\b\s*[:#=.–—-]?\s*[A-Za-z0-9+\-%.\s]{1,10}', "[ACADEMIC GRADES]", re.IGNORECASE ),

            # GPA
            ( r"\b(?:GPA|Cumulative GPA|Major GPA|Overall GPA|Term GPA|Semester GPA|Grade Point Average|CGPA|QPA)\b\s*[:#=.–—-]?\s*[0-9.]{1,5}", "[GPA]", re.IGNORECASE ),

            # Class Rank
            ( r"\b(?:Class Rank|Rank in Class|Rank|Standing|Academic Standing|Class Standing|Rank/GPA|Percentile Rank|Percentile|Top Percent|Top %|Dean's List Status|Probation Status|Academic Status)\b\s*[:#=.–—-]?\s*[A-Za-z0-9\s%/.-]{3,30}", "[CLASS RANK]", re.IGNORECASE ),

            # Test Score
            ( r'\b(?:SAT Score|ACT Score|GRE Score|GMAT Score|LSAT Score|MCAT Score|TOEFL Score|IELTS Score|Standardized Test Score|Entrance Exam Score|Admission Test Score)\b\s*[:#=.–—-]?\s*[0-9.]{2,5}', "[TEST SCORE]", re.IGNORECASE ),

            # Education ID
            ( r'\b(?:Student Number|Student #|Student No|Student ID|Campus ID|Campus-Wide ID|Banner ID|School ID|College ID|University ID|Enrollment ID|CWID|Registration ID|Applicant ID|Application Number|Candidate ID)\b\s*[:#=.–—-]?\s*[A-Z0-9]{3,10}', "[EDUCATION ID]", re.IGNORECASE ),

            # Generic Record ID
            ( r'\b(?:Employee ID|Emp ID|Staff ID|Badge #|ID Badge|Student ID|Campus ID|Banner ID|TTU ID|Customer ID|Client ID|User ID|Member ID|Login ID|ID #|ID Number|Record ID|Profile ID)\b\s*[#:.\-]?\s*[a-zA-Z0-9_-]{4,15}', "[GENERIC ID]", re.IGNORECASE ),

            # Tax Identifier Number
            ( r'\b(?:EIN|Employer ID|Employer Identification Number|Federal Tax ID|Tax ID|Tax Number|TIN|Business Tax ID|Company Tax ID)\b\s*[:#=.–—-]?\s*[0-9]{2}-[0-9]{7}', "[TIN]", re.IGNORECASE ),

            # License Keys
            ( r'\b(?:License Key|Product Key|Software Key|Activation Key|Registration Key|Serial Key|Serial Code)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_.-]{5,40}', "[LICENSE KEY]", re.IGNORECASE ),

            # Authentication Secrets
            ( r'\b(?:X-API-Key|API_KEY|SESSION_TOKEN|AUTHORIZATION|Set-Cookie|API Key|API Token|Access Token|Auth Token|Authorization|Bearer|JWT|Session ID|SessionID|Secret|API Secret|OAuth Token|PrivateKey|PublicKey|Key|Token|Cookie)\b\s*[:#=.–—-]?\s*[0-9A-Za-z_=./+\-]{15,200}', "[AUTH SECRET]",  re.IGNORECASE),

            # Financial Aid ID
            ( r'\b(?:FAFSA ID|Aid ID|Award ID|Loan Servicer ID|Student Aid Number|Federal School Code)\b\s*[:#=.–—-]?\s*[A-Za-z0-9]{3,12}', "[FINANCIAL AID ID]", re.IGNORECASE ),

            # Financial Identifiers
            ( r'\b(?:Loan Number|Loan #|Loan ID|Mortgage Number|Mortgage ID|Loan Account|Mortgage Account|Claim Number|Claim #|Claim ID|Case ID|Contract Number|Contract #|Agreement Number|Agreement #|Policy Reference|Policy Ref|Billing Account Number|Billing ID|Reference Number|Ref #|Customer Number)\b\s*[:#=.–—-]?\s*[0-9A-Za-z_/.\\-]{6,25}', "[FINANCIAL ID]", re.IGNORECASE ),

            # NPI
            ( r'\b(?:NPI|NPI Number|NPI #|NPI ID|NPI No)\b\s*[:#=.–—-]?\s*[0-9]{10}', "[NPI]", re.IGNORECASE ),

            # DEA Number
            ( r'\b(?:DEA|DEA #|DEA Number|DEA No|DEA ID)\b\s*[:#=.–—-]?\s*[A-Za-z]{2}[0-9]{7}', "[DEA #]", re.IGNORECASE ),

            # Professional License ID
            ( r'\b(?:Medical License|Nursing License|RN License|LPN License|NP License|PA License|Physician License|Provider License|Provider ID|Practitioner ID|State License|License #|License Number|Bar Number|Bar License|Attorney ID|Attorney Number|Professional ID|Certification ID|Registry ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9-]{5,15}', "[LICENSE ID]", re.IGNORECASE ),

            # IMEI
            ( r'\b(?:IMEI|IMEI Number|IMEI No|IMEI #|Device IMEI|Phone IMEI|IMEI ID)\b\s*[:#=.–—-]?\s*[0-9]{14,15}', "[IMEI]", re.IGNORECASE ),

            # IMSI
            ( r'\b(?:IMSI|IMSI Number|IMSI #|IMSI No|Subscriber IMSI)\b\s*[:#=.–—-]?\s*[0-9]{15}', "[IMSE]", re.IGNORECASE ),

            # ICCID
            ( r'\b(?:ICCID|ICCID Number|ICCID #|SIM ICCID|SIM Card Number|SIM Serial Number|SIM Number|SIM ID)\b\s*[:#=.–—-]?\s*[0-9]{19,22}', "[ICCID]", re.IGNORECASE ),

            # Device ID
            ( r'\b(?:Device ID|Device Number|Device Code|Machine ID|Machine Identifier|Host ID|Hostname|Computer Name|System Name|Workstation Name)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._-]{5,15}', "[DEVICE ID]", re.IGNORECASE ),

            # Generic Serial Number
            ( r'\b(?:Serial|Serial Number|Serial No|Serial #|S/N|SN|Device Serial|Device Serial Number|Phone Serial|Laptop Serial|Computer Serial|Mac Serial|iPhone Serial|Asset Tag|Asset ID|Asset Number|Product Serial|Product ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9-]{6,20}', "[GENERIC SERIAL #]", re.IGNORECASE ),

            # Biometric ID
            ( r'\b(?:Fingerprint|Fingerprint ID|Fingerprint Number|Fingerprint Scan|Finger ID|FP ID|Fingerprint Code|Retina Scan|Retina ID|Retina Number|Iris Scan|Iris ID|Eye Scan|Voice ID|Voiceprint|Voiceprint ID|Voice Authentication ID|Face ID|Facial ID|Facial Recognition ID|Face Recognition ID|DNA ID|DNA Number|Genome ID|Genetic ID|Genetic Record)\b\s*[:#=.–—-]?\s*[A-Za-z0-9\-]{6,32}', "[BIOMETRIC ID]", re.IGNORECASE ),

            # Password
            ( r'\b(?:Password|Temp Password|Temporary Password|New Password|Old Password|Password Hint|Passcode)\b\s[:#=.–—-]?\s\S{6,64}', "[PASSWORD]", re.IGNORECASE ),

            # PIN Number
            ( r'\b(?:PIN|PIN Code|PIN Number|Security PIN|ATM PIN|Card PIN)\b\s[:#=.–—-]?\s[0-9]{3,7}', "[PIN]", re.IGNORECASE ),

            # Security Answer (answers to security questions)
            ( r"\b(?:Security Answer|Answer|Answer 1|Answer 2|Security Response|Challenge Answer|Mother's Maiden Name|First Pet's Name|First Pet Name|Favorite Teacher|Favorite Color|Favorite Movie|Favorite Sports Team|City of Birth|Place of Birth|High School Name)\b\s[:#=.–—-]?\s[A-Za-z0-9\s-]{3,40}", "[SECURITY QUESTIONS]", re.IGNORECASE ),

            # Demographic
            ( r"\b(?:Gender|Sex|Sex at Birth|Assigned Sex at Birth|Gender Identity|Race|Ethnicity|Race/Ethnicity|Ethnic Group|Ethnic Background|Marital Status|Relationship Status|Spouse Name|Partner Name|Number of Dependents|Religion|Religious Affiliation|Faith|Religious Preference|Sexual Orientation|Disabled|Veteran with Disability|Special Needs|Accommodation Needed|Medical Condition|Citizenship|Citizenship Status|Immigration Status|Visa Status|Work Authorization|Disability|Disability Status)\b\s[:#=.–—-]?\s[A-Za-z0-9\s-]{3,40}", "[DEMOGRAPHIC]", re.IGNORECASE ),

            # Tracking Number
            ( r'\b(?:Tracking Number|Tracking #|USPS Tracking Number|UPS Tracking Number|FedEx Tracking Number|DHL Tracking ID|Generic Tracking #|Shipment ID|Package ID|Parcel ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_.-]{5,40}', "[TRACKING #]", re.IGNORECASE ),

            # Bluetooth / WiFi
            ( r'\b(?:WiFi Address|Bluetooth MAC|BLE Address|WiFi MAC|Wireless ID|Wi-Fi Identifier)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_.-]{5,40}', "[BLUETOOTH/WIFI]", re.IGNORECASE ),

            # Location Code
            ( r'\b(?:Building Code|Site ID|Location ID|Site Code|Location Code|Office Location|Department Location|Building Number|Floor Number|Room Number|Physical Location ID|Facility Code)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_.-]{3,40}', "[LOCATION CODE]", re.IGNORECASE ),


            # Billing Identifier
            ( r'\b(?:Billing ID|Billing Number|Billing Account|Billing Account Number|Statement Number|Statement ID|Invoice Number|Invoice #|Invoice ID|Bill Pay ID|Payment ID|Customer Billing ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._-]{6,25}', "[BILLING ID]", re.IGNORECASE ),

            # Subscription Membership ID
            ( r'\b(?:Subscription Number|Subscription ID|Subscription Account|Member Billing ID|Membership Number|Membership Account|Plan Number|Plan ID|Policy Billing ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._-]{5,25}', "[SUBSCRIPT MEMBERSHIP ID]", re.IGNORECASE ),

            # Payment ID
            ( r'\b(?:Payment Reference|Payment Reference Number|Transaction Reference|Reference Number|Reference ID|Transaction ID|Payout ID|Disbursement ID|Claim Payment ID|Refund ID|Refund Reference)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._-]{6,30}', "[PAYMENT ID]", re.IGNORECASE ),

            # Ecommerce Transaction ID
            ( r'\b(?:Order ID|Order Number|Receipt Number|Receipt ID|Checkout ID|Cart ID|Purchase ID|Sales Order Number|POS Transaction ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._-]{6,30}', "[TRANSACT ID]", re.IGNORECASE ),

            # Emergency Contact Info
            ( r'\b(?:Emergency Contact|Emergency Contact Name|Emergency Contact Number|Emergency Contact Phone|Emergency Contact Relationship|Emergency Contact Person|ICE Contact|In Case Of Emergency Contact|Emergency Phone|Emergency Mobile)\b\s*[:#=.–—-]?\s*[A-Za-z0-9\s().+\-]{3,40}', "[EMERGENCY CONTACT]", re.IGNORECASE ),

            # Household Info
            ( r"\b(?:Spouse Name|Partner Name|Husband Name|Wife Name|Father Name|Mother Name|Guardian Name|Child Name|Dependent Name|Son Name|Daughter Name|Parent Name|Sibling Name|Next of Kin|Next-Of-Kin|Family Member|Family Member Name)\b\s*[:#=.–—-]?\s*[A-Za-z\s'.-]{3,40}", "[HOUSEHOLD INFO]", re.IGNORECASE ),

            # Relationship Info
            ( r'\b(?:Relationship|Relationship to You|Relation|Guardian|Dependent|Dependent Name|Dependent ID|Next of Kin|Next-Of-Kin)\b\s*[:#=.–—-]?\s*[A-Za-z\s-]{3,30}', "[RELATIONSHIP]", re.IGNORECASE ),

            # Household Demographic
            ( r'\b(?:Household Size|Number of Children|Number of Adults|Number of Dependents|Married Filing Status|Filing Status|Family Income Bracket)\b\s*[:#=.–—-]?\s*[A-Za-z0-9\s+$,.-]{1,40}', "[HOUSEHOLD DEMOGRAPH]", re.IGNORECASE ),

            # Earnings
            ( r'\b(?:Salary|Base Salary|Annual Salary|Yearly Salary|Starting Salary|Current Salary|Hourly Rate|Hourly Wage|Pay Rate|Rate of Pay|Wage|Overtime Rate|Bonus|Annual Bonus|Signing Bonus|Commission|Commission Rate|Total Compensation|Total Comp|Pay Grade|Pay Band|Pay Level|Job Level|Salary Band|Compensation|Compensation Amount)\b\s*[:#=.–—-]?\s*[0-9,$%_.k\s\-]{4,25}', "[EARNINGS]", re.IGNORECASE ),

            # Course Case Docket ID
            ( r'\b(?:Case Number|Case No|Case #|Court Case Number|Court Case No|Docket Number|Docket No|Docket #|Citation Number|Citation No|Citation #|Ticket Number|Ticket No|Ticket #|Warrant Number|Warrant No|Warrant #|Summons Number|Summons No|Summons #)\b\s*[:#=.–—-]?\s*[A-Za-z0-9./\-]{5,25}', "[COURSE CASE DOCKET]", re.IGNORECASE ),

            # Law Incident Correction
            ( r'\b(?:Incident Number|Incident No|Incident #|Incident ID|Report Number|Report No|Report #|Police Report Number|Police Case Number|Arrest Number|Arrest No|Arrest ID|Booking Number|Booking No|Booking ID|Inmate Number|Inmate ID|Jail ID|Prisoner Number|Offender ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9./\-]{5,25}', "[LAW INCIDENT CORRECTION]", re.IGNORECASE ),

            # Government Benefit Claim ID
            ( r'\b(?:Medicare Number|Medicare ID|Medicaid Number|Medicaid ID|Social Security Claim Number|SS Claim Number|Benefit Claim Number|Benefit ID|Claim Number|Claim No|Claim #|Unemployment Claim ID|Unemployment Claim Number|SNAP Case Number|Food Stamps Case Number|VA File Number|VA Claim Number|Veterans Claim ID|Pension Claim Number|Disability Claim Number)\b\s*[:#=.–—-]?\s*[A-Za-z0-9./\-]{5,20}', "[GOV. BENEFIT CLAIM]", re.IGNORECASE ),

            # Immigration Citizenship ID
            ( r'\b(?:Alien Registration Number|Alien Number|A-Number|A Number|USCIS Case Number|USCIS Receipt Number|Receipt Number|Immigration Case Number|Visa Number|Visa No|Green Card Number|Green Card No|Naturalization Certificate Number|Naturalization Number|Citizenship Certificate Number|Passport Application Number)\b\s*[:#=.–—-]?\s*[A-Za-z0-9]{8,16}', "[IMMIGRATION CITIZENSHIP]", re.IGNORECASE ),

            # Bitcoin Address
            ( r'\b(?:Bitcoin Address|BTC Address|BTC Wallet|Bitcoin Wallet|BTC Deposit Address|Bitcoin Deposit Address)\b\s*[:#=.–—-]?\s*(?:[13][a-km-zA-HJ-NP-Z1-9]{25,34}|bc1[0-9ac-hj-np-z]{11,71})', "[BITCOIN ADDRESS]", re.IGNORECASE ),

            # Ethereum Address
            ( r'\b(?:Ethereum Address|ETH Address|ERC20 Address|ERC-20 Address|Token Address|Contract Address|Wallet Address|Crypto Address)\b\s*[:#=.–—-]?\s*0[xX][0-9a-fA-F]{40}', "[ETH ADDRESS]", re.IGNORECASE ),

            # Solana Address
            ( r'\b(?:Solana Address|SOL Address|Solana Wallet|SOL Wallet|Solana Public Key|SOL Public Key)\b\s*[:#=.–—-]?\s*[A-HJ-NP-Za-km-z1-9]{32,44}', "[SOL ADDRESS]", re.IGNORECASE ),

            # Ripple Address
            ( r'\b(?:XRP Address|Ripple Address|XRP Wallet|Ripple Wallet|XRP Account|Ripple Account|XRP Deposit Address)\b\s*[:#=.–—-]?\s*r[1-9A-HJ-NP-Za-km-z]{24,34}', "[XRP ADDRESS]", re.IGNORECASE ),

            # Litecoin Address
            ( r'\b(?:Litecoin Address|LTC Address|Litecoin Wallet|LTC Wallet|LTC Deposit Address)\b\s*[:#=.–—-]?\s*[LM3][a-km-zA-HJ-NP-Z1-9]{25,34}', "[LTC ADDRESS]", re.IGNORECASE ),

            # Generic Crypto Address
            ( r'\b(?:Crypto Address|Cryptocurrency Address|Wallet Address|Deposit Address|Blockchain Address)\b\s*[:#=.–—-]?\s*[A-Za-z0-9]{20,70}', "[CRYPTO ADDRESS]", re.IGNORECASE ),

            # Session Tracking Tokens
            ( r'\b(?:Session ID|SessionID|Session Identifier|Session Token|Session Key|Auth Session ID|Login Session ID|Tracking ID|TrackingID|Tracking Token|Tracking Code|Request ID|RequestID|Correlation ID|CorrelationID|Client Trace ID|Trace ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._\-]{8,128}', "[SESSION TOKEN]", re.IGNORECASE ),

            # Analytics Marketing ID
            ( r'\b(?:Analytics ID|AnalyticsID|Google Analytics ID|GA ID|GAID|Gclid|Client ID|ClientID|Adobe Visitor ID|Visitor ID|Marketing ID|Tracking Cookie|Tracking Cookie ID|Campaign ID|CampaignID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._\-]{6,64}', "[ANALYTICS ID]", re.IGNORECASE ),

            # Device Browser Fingerprint ID
            ( r'\b(?:Device Fingerprint|Fingerprint ID|FingerprintID|Browser ID|BrowserID|Device ID Hash|Device Hash|Machine Fingerprint|Client Fingerprint|Device Signature|Browser Signature)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._\-]{16,128}', "[BROWSER FINGERPRINT]", re.IGNORECASE ),

            # UUID/GUID
            ( r'\b(?:UUID|GUID|Unique ID|Unique Identifier|Global ID|Transaction UUID|Request UUID|Session UUID)\b\s*[:#=.–—-]?\s*[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}', "[UUID/GUID]", re.IGNORECASE ),

            # Hash Values
            ( r'\b(?:Hash|Hash Value|Checksum|Digest|MD5|SHA1|SHA-1|SHA256|SHA-256|SHA512|SHA-512|Integrity Hash|File Hash|Verification Hash)\b\s*[:#=.–—-]?\s*(?:[0-9a-fA-F]{32}|[0-9a-fA-F]{40}|[0-9a-fA-F]{64}|[0-9a-fA-F]{128})', "[HASHSUM]", re.IGNORECASE ),

            # User Agent ID
            ( r'\b(?:User Agent|User-Agent|Browser Agent|Client Agent|Device Agent|Device Info|Browser Info|UA String)\b\s*[:#=.–—-]?\s*[A-Za-z0-9\s().;/_:-]{10,300}', "[USER AGENT ID]", re.IGNORECASE ),

            # Cloud Key
            ( r'\b(?:AWS Access Key|AWS Secret Key|AWS Key|AWS Credentials|AWS Secret Access Key|AWS AccessKey|AWS SecretAccessKey|Azure Client Secret|Azure Secret|Azure Key|GCP Service Key|GCP API Key|Google Cloud Key|Cloud API Key)\b\s*[:#=.–—-]?\s*(?:AKIA[0-9A-Z]{16}|[A-Za-z0-9_\-+/=]{20,200})', "[CLOUD KEY]", re.IGNORECASE ),

            # API Key
            ( r'\b(?:API Key|APIKey|Access Key|AccessKey|Secret Key|SecretKey|Private Key|PrivateKey|Public Key|PublicKey|Client Secret|ClientSecret|Client Key|ClientKey|Consumer Key|ConsumerKey|Consumer Secret|ConsumerSecret|App Secret|AppSecret|App Key|AppKey)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_\-=/+]{16,200}', "[API KEY]", re.IGNORECASE ),

            # Crypto Key
            ( r'(-----BEGIN (?:PGP PUBLIC KEY BLOCK|PGP PRIVATE KEY BLOCK|RSA PRIVATE KEY|RSA PUBLIC KEY|OPENSSH PRIVATE KEY|EC PRIVATE KEY)-----[\s\S]+?-----END (?:PGP PUBLIC KEY BLOCK|PGP PRIVATE KEY BLOCK|RSA PRIVATE KEY|RSA PUBLIC KEY|OPENSSH PRIVATE KEY|EC PRIVATE KEY)-----)', "[CRYPTO KEY]", re.IGNORECASE ),

            # Environment Variable
            ( r'\b(?:ENV|Environment Variable|Environment Key|Secret|Secret Key|App Secret|APP_SECRET|SECRET_KEY|API_SECRET|DB_PASSWORD|DATABASE_PASSWORD|JWT_SECRET|TOKEN_SECRET)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_\-+/=]{6,200}', "[ENV VARIABLE]", re.IGNORECASE ),

            # Software Build ID
            ( r'\b(?:Build ID|Build Number|Release ID|Release Number|Version ID|Version Number|Commit Hash|Git Commit|Build Tag|Release Tag|Artifact ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._\-]{3,40}', "[SOFTWARE BUILD ID]", re.IGNORECASE ),

            # Debug Error Tokens
            ( r'\b(?:Error ID|ErrorID|Error Code|Exception ID|ExceptionID|Bug ID|BugID|Crash ID|Crash Report ID|Debug Token|Debug ID|TraceToken|Trace Token|Failure ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._\-]{3,40}', "[ERROR TOKEN]", re.IGNORECASE ),

            # File Paths
            ( r'\b(?:File Path|Path|Directory|Folder Path|System Path|User Path|Home Directory|Working Directory)\b\s*[:#=.–—-]?\s*(?:[A-Za-z]:\\[^\s]+|\/[A-Za-z0-9._\-\/]+)', "[FILE PATH]", re.IGNORECASE ),

            # Medical Metadata
            ( r'\b(?:Diagnosis Code|Dx Code|ICD Code|ICD10|ICD-10|Procedure Code|CPT Code|Treatment Code|Lab Code|Test Code|Provider Code)\b\s*[:#=.–—-]?\s*(?:[A-Z][0-9A-Z]{2}(?:\.[0-9A-Z]{1,4})?|[0-9]{5})', "[MEDICAL METADATA]", re.IGNORECASE ),

            # Financial Metadata
            ( r'\b(?:Routing Code|SWIFT Code|BIC Code|Bank Code|Branch Code|Sort Code|Tax Code|EFT Code|ACH Code)\b\s*[:#=.–—-]?\s*(?:[A-Z0-9]{8,11}|[0-9]{2}-?[0-9]{2}-?[0-9]{2})', "[FINANCIAL METADATA]", re.IGNORECASE ),

            # Shipping Fulfillment ID
            ( r'\b(?:Warehouse ID|Fulfillment ID|Fulfillment Center ID|Shipment Batch|Container Number|Pallet ID|Bin Number|Rack Number|Storage Location ID)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._\-]{3,20}', "[SHIPPING ID]", re.IGNORECASE ),

            # Employer Internal Codes
            ( r'\b(?:Cost Center|Cost Center Code|Dept Code|Department Code|Org Code|Business Unit Code|Location Code|Office Code|Work Unit Code)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._\-]{3,20}', "[INTERNAL EMPLOYMENT CODE]", re.IGNORECASE ),

            # Sensitive GEO Code
            ( r'\b(?:GPS Code|Geo Code|Geolocation Code|Map Grid|Census Tract|Block Code|Area Code|Region Code|District Code)\b\s*[:#=.–—-]?\s*[A-Za-z0-9._\-]{3,20}', "[GEO CODE]", re.IGNORECASE ),

            # Sensitive Account Metadata
            ( r'\b(?:Account Tier|Membership Level|Loyalty Level|Reward ID|Reward Number|Subscriber Level|Service Tier)\b\s*[:#=.–—-]?\s*[A-Za-z0-9\s._\-]{3,40}', "[ACCOUNT METADATA]", re.IGNORECASE ),
            
            # Medical Record Number
            ( r'(?i)medical\s*(?:record)?\s*(?:number|num|#)?[:\s]{0,10}(\d{6,12})\b', "[MEDICAL RECORD #]", re.IGNORECASE ),


            # Passport
            ( r'\b(?:Loan Number|Loan #|Loan ID|Mortgage Number|Mortgage ID|Loan Account|Mortgage Account|Claim Number|Claim #|Claim ID|Case ID|Contract Number|Contract #|Agreement Number|Agreement #|Policy Reference|Policy Ref|Billing Account Number|Billing ID|Reference Number|Ref #|Customer Number)\b\s*[:#=.–—-]?\s*[0-9A-Za-z_/.\\-]{6,25}', "[PASSPORT #]", re.IGNORECASE ),
            ( r'passport.*?[A-Z]{1}[0-9]{8}', "[PASSPORT #]", re.IGNORECASE ),

            # Vehicle Identifier Number
            ( r'\b(?:Reg Number|Tag #|Registration #|License Plate|License Plate Number|Plate #|Vehicle ID|Vehicle Number|Fleet ID|Tag Number|Registration Number)\b\s*[:#=.–—-]?\s*[A-Za-z0-9_.-]{5,40}', "[VIN]", re.IGNORECASE ),
            ( r'[A-HJ-NPR-Z0-9]{17}', "[VIN]" ),

            # Age
            ( r'\b(?:aged?\s*\d{1,3}|(?:\d{1,3}\s*(?:years?|yrs?|yo|y/o)\s*old?)|\d{1,3}-year-old)\b', "[AGE]" ),

            # Fax
            ( r'fax.{0,15}(\(?[0-9]{3}\)?[-\s]?[0-9]{3}[-\s]?[0-9]{4})', "[FAX]", re.IGNORECASE ),

            # Phone Number
            # \(? - Escapes parenthesis so it's taken as a literal character '(' instead of grouping
            # [0-9]{3} - Exactly 3 numbers in range of 0-9
            # \)? - Escapes parenthesis so it's taken as a literal character ')' instead of grouping
            # [-\s]? - Can choose one or none of the symbols (dash or space) to go in between groupings of numbers
            # [0-9]{3} - Exactly 3 numbers in range of 0-9
            # [-\s]? - Can choose one or none of the symbols (dash or space) to go in between groupings of numbers
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            ( r'\(?[0-9]{3}\)?[-\s]?[0-9]{3}[-\s]?[0-9]{4}', "[PHONE]" ),

            # Social Security Number
            # [0-9]{3} - Exactly 3 numbers in range of 0-9
            # \- - Exactly one dash
            # [0-9]{2} - Exactly 2 numbers in range of 0-9
            # \- - Exactly one dash
            # [0-9]{4} - Exactly 4 numbers in the range of 0-9
            ( r'[0-9]{3}\-[0-9]{2}\-[0-9]{4}', "[SSN]" ),

            # Credit/Bank Card Number
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            # [\s] - macthes one space
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            # [\s] - macthes one space
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            # [\s] - macthes one space
            # [0-9]{4} - Exactly 4 numbers in range of 0-9
            ( r'[0-9]{4}[\s][0-9]{4}[\s][0-9]{4}[\s][0-9]{4}', "[CREDIT/DEBIT CARD]" ),

            # Bank Account Number
            # [0-9]{9} - Exactly 9 numbers in range of 0-9
            ( r'[0-9]{6,17}', "[BANK ACCOUNT]" ),

            # Addresses 
            # [0-9]{1,5} - 1 to 5 numbers in the range of 0-9
            # [\sA-Za-z]+,\s - Matches one or more letters or whitespace, then a comma followed by a whitespace
            # [\sA-Za-z]+,\s - Matches one or more letters or whitespace, then a comma followed by a whitespace
            # [A-Z]{2}\s - Matches the state, two capital letters
            # [0-9]{5} - Matches the zip code, five numbers in range of 0-9
            ( r'[0-9]{1,5} [\sA-Za-z]+,\s[\sA-Za-z]+,\s[A-Z]{2}\s[0-9]{5}', "[ADDRESS]" ),

            # Zip Code (lookbehind pattern)
            ( r'(?<=zip(?: code)?\s*[:\-]?\s*)\d{5}(?:-\d{4}|\s?\d{4})?', "[ZIP CODE]", re.IGNORECASE ),

            # Zip Code
            ( r'\b\d{5}(?:-\d{4}|\s?\d{4})?\b', "[ZIP CODE]" ),

            # IPV4 Address
            ( r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}', "[ipv4]" ),

            # IPV6 Address
            ( r'[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}:[A-Fa-f0-9]{1,4}', "[ipv6]" ),
        
            # MAC Address
            ( r'[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}:[0-9A-Z]{2}', "[MAC]" ),

            # General License Plate
            ( r'[A-Z]{3}-*\d{4}', "[LICENSE PLATE #]" ),
            
            # Generic Student ID
            ( r'[A-Z]{1}[0-9]{6,8}', "[STUDENT #]" ),

            # United States Driver License Numbers
            (
                [
                    r"\d{7}",                       # AL, AK, DE, ME, OR, DC, WV
                    r"[a-zA-Z]\d{8}",               # AZ, GA, NE, VA
                    r"\d{9}",                       # AZ, CT, HI, IA, LA, MT, NM, SC, UT
                    r"9\d{8}",                      # AR
                    r"[a-zA-Z]\d{7}",               # CA
                    r"\d{2}-\d{3}-\d{4}",           # CO
                    r"[a-zA-Z](\d{3}-*){2}\d{2}-*\d{3}-*\d", # FL
                    r"[a-zA-Z]{2}\d{6}[a-zA-Z]",    # ID
                    r"[a-zA-Z]\d{3}-*(\d{4}-*){2}", # IL
                    r"\d{4}-\d{2}-\d{4}",           # IN
                    r"\d{3}[a-zA-Z]{2}\d{4}",       # IA
                    r"[a-zA-Z](\d{2}-){2}\d{4}",    # KA
                    r"[a-zA-Z]\d{2}-\d{3}-\d{4}",   # KY
                    r"[a-zA-Z]-*(\d{3}-*){4}",      # MD
                    r"[a-zA-Z]\d{9}",               # MA, MO, OK
                    r"[a-zA-Z](\s\d{3}){4}",        # MI
                    r"[a-zA-Z]\d{12}",              # MI, MN
                    r"\d{3}-\d{2}-\d{4}",           # MS
                    r"([0][1-9]|[1][0-2])\d{3}([1-9]\d{3})", # MT
                    r"\d{10}",                      # NV
                    r"([0][1-9]|[1][0-2])([a-zA-Z]\{3})(0[1-9]|[1-2][0-9]|3[0-1])\d", # NH
                    r"[a-zA-Z]\d{4}-*(\d{5}-*){2}", # NJ
                    r"(\d{3}){2}\s\d{3}",           # NY
                    r"\d{12}",                      # NC
                    r"[a-zA-Z]{3}-\d{2}-\d{4}",     # ND
                    r"\d{8}",                       # OH, SD, TX, VT
                    r"[a-zA-Z]{1}\d{4,8}",          # OH
                    r"[a-zA-Z]{2}\d{3,7}",          # OH
                    r"\d{2}( \d{3}){2}",            # PA
                    r"[1-9]{2}\d{5}",               # RI
                    r"\d{7,9}",                     # TN
                    r"\d{7}[a-zA-Z]",               # VT
                    r"[a-zA-Z](\d{2}-){2}\d{4}",    # VA
                    r"[a-zA-Z]{3}\*\*[a-zA-Z]{2}\d{3}[a-zA-Z]\d", # WA
                    r"[a-zA-Z]\d{6}",               # WV
                    r"[a-zA-Z]\d{3}-(\d{4}-){2}\d{2}", # WI
                    r"\d{6}-\d{3}",                 # WY
                ],
                "[DRIVER LICENSE #]" )
        ]


    def get_honorifics_pattern(self) -> str:
        return self.__honorifics_pattern

    def get_regex_patterns(self) -> list[str | list]:
        return self.__patterns

    def redact_text(self, text: str) -> str:
        content = text

        for pattern, replace, *extra_flags in self.__patterns:
            flags = re.M

            for f in extra_flags:
                flags |= f

            if not isinstance(pattern, list):
                content = re.sub(pattern, replace, content, flags=flags)
                continue

        return content


    def retrieve_pdf_rects(self, words_text: str) -> list[str]:
        retrieved_words = []

        for pattern, _, *extra_flags in self.__patterns:
            flags = re.M

            for f in extra_flags:
                flags |= f

            # TODO: do pattern for driver's license (list of patterns)
            if isinstance(pattern, list):
                continue
            
            retrieved_words = []
            for matched in re.finditer(pattern, words_text, flags=flags):
                matched_text = matched.group()

                if matched.lastindex:
                    matched_text = matched.group(1)

                retrieved_words.append(matched_text)

        return retrieved_words
