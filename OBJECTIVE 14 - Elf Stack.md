# OBJECTIVE 14 - Elf Stack #
Difficulty: ❄️❄️❄️❄️❄️

[Direct Link](https://hhc24-elfstack.holidayhackchallenge.com)

## OBJECTIVE : ##
>Help the ElfSOC analysts track down a malicious attack against the North Pole domain.

#

## HINTS: ##
<details>
  <summary>Hints provided for Objective 14</summary>
  
>-  I'm part of the ElfSOC that protects the interests here at the North Pole. We built the Elf Stack SIEM, but not everybody uses it. Some of our senior analysts choose to use their command line skills, while others choose to deploy their own solution. Any way is possible to hunt through our logs!
>-	If you are using your command line skills to solve the challenge, you might need to review the configuration files from the containerized Elf Stack SIEM.
>-	One of our seasoned ElfSOC analysts told me about a great resource to have handy when hunting through event log data. I have it around here somewhere, or maybe it was online. Hmm.
>-	Our Elf Stack SIEM has some minor issues when parsing log data that we still need to figure out. Our ElfSOC SIEM engineers drank many cups of hot chocolate figuring out the right parsing logic. The engineers wanted to ensure that our junior analysts had a solid platform to hunt through log data.
>-	I was on my way to grab a cup of hot chocolate the other day when I overheard the reindeer talking about playing games. The reindeer mentioned trying to invite Wombley and Alabaster to their games. This may or may not be great news. All I know is, the reindeer better create formal invitations to send to both Wombley and Alabaster.
>-	Some elves have tried to make tweaks to the Elf Stack log parsing logic, but only a seasoned SIEM engineer or analyst may find that task useful.

</details>

#  

## PROCEDURE : ##
### 🥈 SILVER MEDAL ###

Once Elastic search is up and running go to **_Analytics -> Discover_** and we can start answering questions:

**Question 1:** _How many unique values are there for the event_source field in all logs?_

Search for `event_source: *` then click on the **edit visualization** button at the top right and set the vertical axis to **unique count of event_source**.  There are <ins>**5**</ins> values for `event_sourc`e called `WindowsEvent`, `NetflowPmacct`, `GreenCoat`, `SnowGlowMailPxy` and `AuthLog`.

![image](https://github.com/user-attachments/assets/34bc31d8-5a5f-41b3-8928-59a99160a9ee)

**Question 2:** _Which event_source has the fewest number of events related to it?_

On the same visualisation we can simply change the vertical axis to show **Count of event_source** and we can see that the `event_source` with the least events related to it is <ins>**AuthLog**</ins> with 265 events.

**Question 3:**_ Using the event_source from the previous question as a filter, what is the field name that contains the name of the system the log event originated from?_

Back in the **Discover** screen we can open any one of the events and scroll through the available fields until we see a field called <ins>**hostname**</ins>.

**Question 4:** _Which event_source has the second highest number of events related to it?_

We can use the same visualisation we used for **Q2**, to determine that the `event_source` with the second highest number of events is <ins>**Netflowpmacct**</ins> with 34,679 events.

**Question 5:** _Using the event_source from the previous question as a filter, what is the name of the field that defines the destination port of the Netflow logs?_

In the **Discover** screen we filter for ``event_source : “NetflowPmacct”`` and open any one of the events to see a field called <ins>**event.port_dst**</ins> which contains the destination port number.

**Question 6:**_ Which event_source is related to email traffic?_

This is quite obvious from the name of the event; <ins>**SnowGlowMailPxy**</ins> is the event source related to email traffic.

**Question 7:** _Looking at the event source from the last question, what is the name of the field that contains the actual email text?_

Filter for ``event_source : “SnowGlowMailPxy”`` and open any one of the events. <ins>**event.Body**</ins> contains the body of the emails.

**Question 8:** _Using the 'GreenCoat' event_source, what is the only value in the hostname field?_

Filter for ``event_source : “GreenCoat”`` and open any one of the events to see that the hostname is <ins>**SecureElfGwy**</ins>.

**Question 9:** _Using the 'GreenCoat' event_source, what is the name of the field that contains the site visited by a client in the network?_

Similarly to **Q8** we can see that the field called <ins>**event.url**</ins> contains the site visited by the client.

**Question 10:**_ Using the 'GreenCoat' event_source, which unique URL and port (URL:port) did clients in the TinselStream network visit most?_

We can create a visualisation that plots the top five values of `event.url` against the number of records for each one and we find that the most visited URL is <ins>**pagead2.googlesyndication.com:443**</ins>.

![image](https://github.com/user-attachments/assets/47e132f6-8924-4ed6-9b3b-0f8a20915633)

**Question 11:** _Using the 'WindowsEvent' event_source, how many unique Channels is the SIEM receiving Windows event logs from?_

Filter for ``event_source: “WindowsEvent” and event.Channel : *`` , edit the visualisation and plot Top 10 values of `event.Channel` and we see that we only have <ins>**5**</ins> channels; `Security`, `Microsoft-Windows-Sysmon/Operational`, `Microsoft-Windows-PowerShell/Operational`, `System` and `Windows PowerShell`

**Question 12:**_ What is the name of the event.Channel (or Channel) with the second highest number of events?_

From the same visualisation we used for **Q11** we see that the channel with the second highest number of events is <ins>**Microsoft-Windows-Sysmon/Operational**</ins> with 17,421 records.

**Question 13:** _Our environment is using Sysmon to track many different events on Windows systems. What is the Sysmon Event ID related to loading of a driver?_

A quick [Goole Search](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90006) tells us that the Sysmon event ID for “Driver Loaded” is <ins>**6**</ins>.

**Question 14:** _What is the Windows event ID that is recorded when a new service is installed on a system?_

Similarly, we can [use Google](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4697) to determine that the Sysmon event ID for this is <ins>**4697**</ins>.

**Question 15:** _Using the WindowsEvent event_source as your initial filter, how many user accounts were created?_

Filter for ``event_source: “WindowswEvent” and event.EventID : 4720``  and there are no results so the answer to this question is <ins>**0**</ins>.


### 🥇 GOLD MEDAL ###

**Question 1:** _What is the event.EventID number for Sysmon event logs relating to process creation?_

A quick [Google Search](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=90001) tells us the answer is <ins>**1**</ins>.  

**Question 2:** _How many unique values are there for the 'event_source' field in all of the logs?_

We already answered this in **Q1 of Easy Mode**, it’s <ins>**5**</ins>.

**Question 3:** _What is the event_source name that contains the email logs?_

We already answered this in **Q6 of Easy Mode**, it’s <ins>**SnowGlowMailPxy**</ins>.

**Question 4:** _The North Pole network was compromised recently through a sophisticated phishing attack sent to one of our elves. The attacker found a way to bypass the middleware that prevented phishing emails from getting to North Pole elves. As a result, one of the Received IPs will likely be different from what most email logs contain. Find the email log in question and submit the value in the event 'From:' field for this email log event._

Looking through the logs in `SnowGlowMailPxy`, we can see that the value for `ReceivedIP1` and `ReceivedIP2` are usually from the `172.24.25.0 /24` network range, so we can filter for anything outside this network using the following filter:
```kql
event_source : “SnowFlowMailPxy” and ((NOT event.ReceivedIP1 : 172.24.25.*) or (NOT event.ReceivedIP2 : 172.24.25.*))
```
This returns an email log for an email received from <ins>**kriskring1e@northpole.local**</ins>.

![image](https://github.com/user-attachments/assets/5808a16f-42f0-4cfa-a0e8-c20697eced1f)

**Question 5:** _Our ElfSOC analysts need your help identifying the hostname of the domain computer that established a connection to the attacker after receiving the phishing email from the previous question. You can take a look at our GreenCoat proxy logs as an event source. Since it is a domain computer, we only need the hostname, not the fully qualified domain name (FQDN) of the system._

Filter for ``event_source : “GreenCoat” and event.url : *hollyhaven*`` and we get a single entry with an `event.host` value of <ins>**SleighRider**</ins>.

**Question 6:**_ What was the IP address of the system you found in the previous question?_

The event in **Q5** has an event.ip of <ins>**172.24.25.12**</ins>.

**Question 7:** _A process was launched when the user executed the program AFTER they downloaded it. What was that Process ID number (digits only please)?_

If we search for Windows Events which include `howtosavexmas` in the Process Name, we get a lot of events with a `ProcessID` of 4 – we can exclude these to find our answer: 
```kql
event_source : “WindowsEvent” and event.ProcessName : *howtosavexmas* and event.ProcessID : (NOT 4)
```
and we find `event.ProcessID` <ins>**10014**</ins>.

**Question 8:**_ Did the attacker's payload make an outbound network connection? Our ElfSOC analysts need your help identifying the destination TCP port of this connection._

```kql
event_source : “WindowsEvent” and event.ProcessID : 10014 and event.DestinationPort : * and event.DestinationIp : (NOT 172.24.25.*)
```  
This gives us a single event for a connection created by `processID 10014` to an IP outside our network, in this case it’s towards `103.12.187.43` on port <ins>**8443**</ins>.

**Question 9:** _The attacker escalated their privileges to the SYSTEM account by creating an inter-process communication (IPC) channel. Submit the alpha-numeric name for the IPC channel used by the attacker._

Search for `cmd.exe` commands on the hostname `SleighRider.northpole.local`:
```kql
event_source : “WindowsEvent” and event.Hostname : *Sleigh* and event.ServiceFileName: *cmd.exe*
```
This gives us an event with an `eventID` of `4697` and the following `event.ServiceFileName`: `cmd.exe /c echo ddpvccdbr &gt; \\. \pipe\ddpvccdbr`

**Question 10:** _The attacker's process attempted to access a file. Submit the full and complete file path accessed by the attacker's process._

Filter for `eventID 4663` (_an attempt was made to access an object_) triggered by `processID 10014`:
```kql
 event_source : “WindowsEvent” and event.EventID : 4663 and event.ProcessID : 10014
```
This returns a single event with a field value for `event.ObjectName` of <ins>**C:\Users\elf_user02\Desktop\kkringl315@10.12.25.24.pem**</ins>
 
**Question 11:** _The attacker attempted to use a secure protocol to connect to a remote system. What is the hostname of the target server?_

We can guess that the secure protocol used is ssh and just search for that in the `AuthLog`:
```kql
event_source: “AuthLog” and event.service : *ssh*
```
The hostname we find from this is <ins>**kringleSSleigH**</ins>.

**Question 12:**_ The attacker created an account to establish their persistence on the Linux host. What is the name of the new account created by the attacker?_

Filter for `*useradd*` which is the Linux command used to create a new user.  We get a single event telling us that the user account created is <ins>**ssdh**</ins> on Sep 16, 2024 @ 16:59:46.000.

![image](https://github.com/user-attachments/assets/f8c54932-7298-4c0f-9add-bb724e8e392d)

**Question 13:** _The attacker wanted to maintain persistence on the Linux host they gained access to and executed multiple binaries to achieve their goal. What was the full CLI syntax of the binary the attacker executed after they created the new user account?_

We can have a look at some more commands that were executed over this ssh connection by filtering out events that contain `COMMAND` in the message and that happened after the `ssdh` user was created:
```kql
 hostname : “kringleSSleigH” and @ timestamp >= “2024-09-16T13:59:45.985591” and event.message : *COMMAND*
```
By sorting the resulting events chronologically, we can see that a sequence of commands was executed, the first one being <ins>**/usr/sbin/usermod -a -G sudo ssdh**</ins>

**Question 14:** _The attacker enumerated Active Directory using a well known tool to map our Active Directory domain over LDAP. Submit the full ISO8601 compliant timestamp when the first request of the data collection attack sequence was initially recorded against the domain controller._

This took me a while to figure out, trying to search for all sorts of AD enumeration tools.  Eventually I searched for all [LDAP bind events](https://www.manageengine.com/products/active-directory-audit/kb/system-events/event-id-2889.html) using windows event ID `2889` and sorted the results chronologically to retrieve the oldest record. So by applying the filter ``Event.EventID : 2889``, we find that the first request happened on `Event.Date` = <ins>**2024-09-16T11:10:12-04:00**</ins>

**Question 15:** _The attacker attempted to perform an ADCS ESC1 attack, but certificate services denied their certificate request. Submit the name of the software responsible for preventing this initial attack._

We can search for [Windows Event ID 4888 – Certificate Services denied a certificate request](https://www.ultimatewindowssecurity.com/securitylog/encyclopedia/event.aspx?eventid=4888): `Event.EventID : 4888` returns a single document.  In the document’s `event.ReasonForRejection` field we find “<ins>**KringleGuard**</ins> EDR flagged the certificate request.”

**Question 16:** _We think the attacker successfully performed an ADCS ESC1 attack. Can you find the name of the user they successfully requested a certificate on behalf of?_

I found [this article by Beyond Trust](https://www.beyondtrust.com/blog/entry/esc1-attacks) to be very helpful in answering this question.  The article suggests that to detect an ADCS ESC1 attack we should focus on Event IDs `4886` and `4887`.  If we apply the filter `event.EventID : 4886` in ELK, it returns a single document showing that a certificate was granted to <ins>**nutcrakr@northpole.local**</ins>.

**Question 17:**_ One of our file shares was accessed by the attacker using the elevated user account (from the ADCS attack). Submit the folder name of the share they accessed._

We can use the newly-discovered username to search for events along with a string such as `\\` (remembering to escape each `\` character) to find references to network share locations:
```kql
event.SubjectUserName : “nutcrakr” and \\\\*
```
By looking at the contents of the `event.ShareName` field we can see that the attacker first accessed the share called <ins>**\\*\WishLists**</ins>.

**Question 18:** _The naughty attacker continued to use their privileged account to execute a PowerShell script to gain domain administrative privileges. What is the password for the account the attacker used in their attack payload?_

For some reason I wasn’t able to get to the answer of this question through Kibana, it looks like some logs were not parsed properly – which is maybe what one of the hints is referring to.  However, I was able to search for log entries that included `nutcrakr` and `New-Object` to detect possible powershell scripts that were executed by `nutcrakr`:
```bash
# cat log_chunk_2.log | grep nutcrakr | grep New-Object -i
```
This returns a log entry that includes ``Admins,CN=Users,DC=northpole,DC=local\"\n$username = \"nutcrakr\"\n$pswd = 'fR0s3nF1@k3_s'``

**Question 19:** _The attacker then used remote desktop to remotely access one of our domain computers. What is the full ISO8601 compliant UTC EventTime when they established this connection?_

To answer this, we can filter for [event ID 4624 (successful logon attempts)](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4624) with a [logon type of 10 (remote interactive)](https://learn.microsoft.com/en-us/windows-server/identity/securing-privileged-access/reference-tools-logon-types):
```kql
 event.EventID : 4624 and event.LogonType : 10
```
This returns a single event with the timestamp: <inis>**2024-09-16T15:35:57.000Z**</ins>

This log entry indicates that the user `nutcrakr` successfully established a Remote Desktop (RDP) connection to the computer `dc01.northpole.local` from the IP address `10.12.25.24`. The logon type `10` confirms that it was a _RemoteInteractive_ logon, typically associated with RDP sessions.

**Question 20:** _The attacker is trying to create their own naughty and nice list! What is the full file path they created using their remote desktop connection?_

We know that the username is `nutcrak`r and that they accessed the `WishLists` fileshare so we can try filtering for all events that include `nutcrakr` and `WishLists`: 
```kql
*nutcrakr* and *WishLists*
```
The `event.CommandLine` field for the most recent event shows us `C:\Windows\system32\NOTEPAD.EXE `<ins>**C:\WishLists\santadms_only\its_my_fakelst.txt**</ins>

**Question 21:** _The Wombley faction has user accounts in our environment. How many unique Wombley faction users sent an email message within the domain?_

Apply the following filter to find any email with a **From** address that starts with `wc`:
```kql
event_source : “SnowGlowMailPxy” and event.From : wc* and event.To : *northpole.local
```
Now look at the Field Statistics tab and there are <ins>**4**</ins> distinct values for `event.From`; `wcube311`, `wcub303`, `wcub808` and `wcub101`

**Question 22:** _The Alabaster faction also has some user accounts in our environment. How many emails were sent by the Alabaster users to the Wombley faction users?_

Similarly to the previous question, we can use the following filter to find emails sent to any address starting with `wc` from any address starting with `as`:
```kql
 event_source : “SnowGlowMailPxy” and event.From : as* and event.To : wc*
```
 Then look at the Field Statistics tab and there are <ins>**22**</ins> returned mail events.

**Question 23:** _Of all the reindeer, there are only nine. What's the full domain for the one whose nose does glow and shine? To help you narrow your search, search the events in the 'SnowGlowMailPxy' event source._

The reindeer “_whose nose does glow_” is of course **Rudolph**, so we can filter for any mail records that contain the string `Rudolph`:
```kql
event_source : “SnowGlowMailPxy” and *Rudolph*
```
If we scroll to through the results, one of the emails sticks out because it has a Rudolph-related domain: <ins>**RudolphRunner@rud01ph.glow**</ins>.

**Question 24:** _With a fiery tail seen once in great years, what's the domain for the reindeer who flies without fears? To help you narrow your search, search the events in the 'SnowGlowMailPxy' event source._

The riddle in the question is referring to **Comet** which is the name of one of Santa’s reindeer as well as a cosmic event with a “Fiery tail”.  The problem is that many of the domains we’ve seen in the `SnowGlowMailPxy` logs are written in _leetspeak_, so we need to search for a number of different possible ways of writing `comet`:
```kql
event_source : "SnowGlowMailPxy" and event.From : *comet* or event.From : *c0met* or event.From : *c0m3t*
```
With this filter we find that our answer is <ins>**c0m3t.halleys**</ins>.


 #
[<<< Previous Objective (13 - Santa Vision)](OBJECTIVE%2013%20-%20Santa%20Vision.md)|.........................................................| [Next Objective (15 - Decrypt the Naughty-Nice List) >>>](OBJECTIVE%2015%20-%20Decrypt%20the%20Naughty-Nice%20List.md)|
:-|--|-:


