# OBJECTIVE 12 - Microsoft KC7 #
Difficulty: ❄️❄️❄️

[Direct Link](https://kc7cyber.com/go/hhc24)

## OBJECTIVE : ##
>[Answer](https://kc7cyber.com/go/hhc24) two sections for silver, all four sections for gold.
#  

## PROCEDURE : ##
### SECTION 1 ###

S1 Q1. Can you find out the name of the Chief Toy Maker?
```kql
Employees
| where role=="Chief Toy Maker"
```
✅ Shinny Upatree


S1Q2. How many emails did Angel Candysalt receive?
```kql
Employees
| where name=="Angel Candysalt";
Email
| where recipient == "angel_candysalt@santaworkshopgeeseislands.org"
| count
```
✅ 31

S1Q3. How many distinct recipients were seen in the email logs from twinkle_frostington@santaworkshopgeeseislands.org?
```kql
Email
| where sender has "twinkle_frostington@santaworkshopgeeseislands.org"
| distinct recipient
| count
```
✅ 32

S1Q4. How many distinct websites did Twinkle Frostington visit?
```kql
Employees
| where name =="Twinkle Frostington"
OutboundNetworkEvents
| where src_ip == "10.10.0.36"
| distinct url
| count
✅ 4
```

S1Q5: How many distinct domains in the PassiveDns records contain the word green?
```kql
PassiveDns
| where domain contains "green"
| distinct domain
| count
```
✅ 10

S1Q6: How many distinct URLs did elves with the first name Twinkle visit?
```kql
let twinkle_ips = 
Employees
| where name has "Twinkle"
| distinct ip_addr;
OutboundNetworkEvents
| where src_ip in (twinkle_ips)
| distinct url
| count
```
✅ 8

#
### SECTION 2 ###

S2Q1: Who was the sender of the phishing email that set this plan into motion?
```kql
Email
| where subject contains "surrender"
| distinct sender
```
✅ surrender@northpolemail.com

S2Q2: How many elves from Team Wombley received the phishing email?
```kql
Email
| where subject contains "surrender"
| distinct recipient
| count
```
✅ 22

S2Q3: What was the filename of the document that Team Alabaster distributed in their phishing email?
```kql
Email
| where subject contains "surrender"
| distinct link
```
✅ Team_Wombley_Surrender.doc

S2Q4: Who was the first person from Team Wombley to click the URL in the phishing email?
```kql
Employees
| join kind=inner (
    OutboundNetworkEvents
) on $left.ip_addr == $right.src_ip
| where url contains "Team_Wombley_Surrender.doc"
| project name, ip_addr, url, timestamp
| sort by timestamp asc
```
✅ Joyelle Tinseltoe

S2Q5. What was the filename that was created after the .doc was downloaded and executed?
```kql
Employees
| where name contains "Joyelle"
| project hostname
```
✅ keylogger.exe

#
### SECTION 3 ###

S3Q1. What was the IP address associated with the password spray?
```kql
AuthenticationEvents
| where result == "Failed Login"
| summarize FailedAttempts = count() by username, src_ip, result
| where FailedAttempts >= 10
| sort by FailedAttempts desc
```
✅ 59.171.58.12

S3Q2: How many unique accounts were impacted where there was a successful login from 59.171.58.12?
```kql
AuthenticationEvents
| where result == "Successful Login"
| where src_ip == "59.171.58.12"
| distinct username
| count
```
✅ 23

S3Q3: What service was used to access these accounts/devices?
```kql
AuthenticationEvents
| where result == "Successful Login"
| where src_ip == "59.171.58.12"
| distinct description
```
✅ RDP

S3Q4: What file was exfiltrated from Alabaster’s laptop?
```kql
ProcessEvents
| where username == "alsnowball"
| sort by timestamp asc
``` 
✅ Secret_Files.zip

S3Q5: What is the name of the malicious file that was run on Alabaster's laptop?

✅ EncryptEverything.exe

#
### SECTION 4 ###

S4Q1: What was the timestamp of first phishing email about the breached credentials received by Noel Boetie?
```kql
Email
| where subject contains "breach"
| sort by timestamp asc 
```
✅ 2024-12-12T14:48:55Z

S4Q2: When did Noel Boetie click the link to the first file?
```kql
let noel_ip = 
Employees
| where name has "Boetie"
| distinct ip_addr;
OutboundNetworkEvents
| where src_ip in (noel_ip)
| sort by timestamp asc 
| take 1
```
✅ 2024-12-12T15:13:55Z

S4Q3: What was the IP for the domain where the file was hosted?
```kql
let noel_ip = 
Employees
| where name has "Boetie"
| distinct ip_addr;
let bad_url =
OutboundNetworkEvents
| where src_ip in (noel_ip)
| order by timestamp asc 
| take 1
| distinct url
| extend bad_domain = parse_url(url).Host
| project bad_domain;
PassiveDns
| where domain in (bad_url)
| distinct ip
```
✅ 182.56.23.122

S4Q4: Let’s take a closer look at the authentication events. I wonder if any connection events from 182.56.23.122. If so, what hostname was accessed?
```kql
AuthenticationEvents
| where src_ip == "182.56.23.122"
```
✅ WebApp-ElvesWorkshop

S4Q5: What was the script that was run to obtain credentials?
```kql
ProcessEvents
| where hostname =="WebApp-ElvesWorkshop"
| distinct process_commandline
```
✅ Invoke-Mimikatz.ps1

S4Q6: What is the timestamp where Noel executed the file?
```kql
let problemtime =
Email
| where link contains "holidaybargainhunt"
| where recipient contains "noel_boetie"
| distinct timestamp
| order by timestamp asc 
| take 1
| project timestamp;
ProcessEvents
| where username == "noboetie" 
| order by timestamp asc
```

S4Q7: The first suspicious process in the list is Explorer.exe "C:\Users\noboetie\Downloads\echo.exe"

✅ 2024-12-12T15:14:38Z

S4Q8: What domain was the holidaycandy.hta file downloaded from?
```kql
OutboundNetworkEvents
| where url contains "holidaycandy"
| distinct url
| extend parse_url(url).Host
| project Host
```
✅ compromisedchristmastoys.com

S4Q9: What was the first file that was created after extraction?
```kql
let extraction_time = toscalar(
    ProcessEvents
    | where process_commandline contains "frosty.zip"
    | take 1 
    | project timestamp
);
ProcessEvents
| where timestamp > extraction_time
| where hostname =="Elf-Lap-A-Boetie"
```
✅ sqlwriter.exe

S4Q10: What is the name of the property assigned to the new registry key?

✅ frosty


 #
[<<< Previous Objective (11 - Snowball Showdown)](OBJECTIVE%2011%20-%20Snowball%20Showdown.md)|.........................................................| [Next Objective (13 - Santa Vision) >>>](OBJECTIVE%2013%20-%20Santa%20Vision.md)|
:-|--|-:
