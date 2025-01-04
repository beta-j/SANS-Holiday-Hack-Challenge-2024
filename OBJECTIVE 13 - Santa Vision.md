# OBJECTIVE 13 - Santa Vision #
Difficulty: ❄️❄️❄️❄️

[Direct Link](https://hhc24-gatexor.holidayhackchallenge.com/timey-whimey?env=prod&page=santavision&&challenge=term)

## OBJECTIVE : ##
>Alabaster and Wombley have poisoned the Santa Vision feeds! Knock them out to restore everyone back to their regularly scheduled programming.

  >  A.	What username logs you into the SantaVision portal?

  >  B.	Once logged on, authenticate further without using Wombley's or Alabaster's accounts to see the northpolefeeds on the monitors. What username worked here?

  >  C.	Using the information available to you in the SantaVision platform, subscribe to the frostbitfeed MQTT topic. Are there any other feeds available? What is the code name for the elves' secret operation?

  >  D.	There are too many admins. Demote Wombley and Alabaster with a single MQTT message to correct the northpolefeeds feed. What type of contraption do you see Santa on?

#

## HINTS: ##
<details>
  <summary>Hints provided for Objective 13</summary>
  
>-  [Mosquitto](https://mosquitto.org/) is a great client for interacting with MQTT, but their spelling may be suspect. Prefer a GUI? Try [MQTTX](https://mqttx.app/)
>-	Santa Vison A:	See if any credentials you find allow you to subscribe to any [MQTT](https://en.wikipedia.org/wiki/MQTT) feeds.
>-  Santa Vision A:	[jefferson](https://github.com/onekey-sec/jefferson/) is great for analyzing JFFS2 file systems.
>- 	Santa Vision A: Consider checking any database files for credentials...
>-	Santa Vision C:	Discovering the credentials will show you the answer, but will you see it?


</details>

#  

## PROCEDURE : ##
### 🥈 SILVER MEDAL ###

#### SANTA VISION A: ####
Once GateXOR has granted us an IP address to target, it hints us in the right direction telling us to scan the IP address provided.  This part is quite easy as a `nmap` scan for the most commonly used port quickly gives us a result with three open ports; `22`, `8000` and `9001`.  Port `22` is for SSH which would require us to know a username and password to access it and at this stage it is unclear what port `9001` is used for.  On the other hand, `8000` is a common alternative to port `80` for web browsing.  So, we can just enter `http://35.188.194.54:8000` in our browser to access the SantaVision login page.

![image](https://github.com/user-attachments/assets/2a90b368-4b24-4698-81c7-931c9c0369d5)

We can now have a look at the html code for the page by hitting **F12** on the keyboard to bring up the browser’s developer tools and just by having a quick look through the html, we can quickly spot a comment with what appears to be a username and password for MQTT.  We can successfully use these to log in to the SantaVision portal.  This also gives us our answer for Santa Vision A.

![image](https://github.com/user-attachments/assets/0417993a-6882-4232-a973-9c9e7125381f)

#### SANTA VISION B: ####
Once logged in to the SantaVision portal, we’re quite limited in what we can do.  It looks like we need to provide a username, password, server address and port number to be able to power on the monitors.  However, we can still click on the **_List Available Clients_** and **_List Available Roles_** to bring up the respective lists.  At this stage it’s clear that we should use `elfmonitor` as our username since the objective specifically tells us not to use the `WomblyC` or `AlabasterS` accounts.  The server address is given by the IP address we are using to access the portal and the port number is probably `9001` since that was the other unknown open port we found in our `nmap` scan earlier.

Looking through the source for `mqttJS.js` confirms this with a helpful comment near the port variable declaration.

![image](https://github.com/user-attachments/assets/28c8d882-8a9f-4fd8-9057-4ee50fd009fb)

All that remains is for us to guess a password that goes with the username.  At this stage I tried all sorts of common password possibilities such as `elfmonitor`, `Password`, `passw0rd`, `12345`, `letmein`, etc… but nothing seemed to work. Then an idea hit me and I tried entering the available roles as a password and sure enough I managed to power on the Monitors with the `elfmonitor` / `SiteElfMonitorRole`.  This allows us to view the `northpolefeeeds` broadcast on the screens.

#### SANTA VISION C: ####
For this part of the objective, we connect to the `frostbitfeed` broadcast.  This doesn’t show us any images, but outputs a number of messages seemingly at random.  It’s important to pay attention here as it’s very easy to miss, but one of the messages reads **“Additional messages available in santafeed”**

```mqtt
Error msg: Unauthorized access attempt. /api/v1/frostbitadmin/bot/<botuuid>/deactivate, authHeader: X-API-Key, status: Invalid Key, alert: Warning, recipient: Wombley
Let's Encrypt cert for api.frostbit.app verified. at path /etc/nginx/certs/api.frostbit.app.key
Frostbit is a leading cause of network downtime
To prevent frostbite, you should wear appropriate clothing and cover exposed skin and ports
Frostbite is a serious condition that can cause permanent damage to the body and/or network
While good backups are important, they won't prevent frostbite
Do you conduct regular frostbite preparedness exercises?
Frostbite can occur in as little as 30 minutes in extreme cold - faster in flat networks
Additional messages available in santafeed
```

We can now have a look at the santafeed broadcast instead.  This time we are again presented with a number of repeating messages including one which reads “Sixteen elves launched operation: Idemcerybu” which gives us our answer to the Santa Vision C objective.
Santa is on his way to the North Pole
Santa is checking his list
superAdminMode=true
singleAdminMode=false
Santa role: superadmin
WombleyC role: admin
AlabasterS role: admin
Santa is checking his list
Sixteen elves launched operation: Idemcerybu

### 🥇 GOLD MEDAL ###

