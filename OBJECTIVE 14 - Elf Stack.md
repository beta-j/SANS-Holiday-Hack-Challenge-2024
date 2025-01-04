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

Search for `event_source: *` then click on the **edit visualization** button at the top right and set the vertical axis to **unique count of event_source**.  There are 5 values for event_source called WindowsEvent, NetflowPmacct, GreenCoat, SnowGlowMailPxy and AuthLog.



### 🥇 GOLD MEDAL ###
