
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

```console
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

We can now have a look at the `santafeed` broadcast instead.  This time we are again presented with a number of repeating messages including one which reads **“Sixteen elves launched operation: Idemcerybu”** which gives us our answer to the Santa Vision C objective.

```console
Santa is on his way to the North Pole
Santa is checking his list
superAdminMode=true
singleAdminMode=false
Santa role: superadmin
WombleyC role: admin
AlabasterS role: admin
Santa is checking his list
Sixteen elves launched operation: Idemcerybu
```

#### Santa Vision D: ####
The messages in `santafeed` reveal that both `WombleyC` and `AlabasterS` have `admin` roles and that Santa holds a `superAdmin` role.  We also get a message saying `singleAdminMode=true`.  Based on the objective’s instructions it looks like we need to change this to `false` to only allow a single admin on the system.

We can achieve this quite simply by connecting to the `northpolefeeds` broadcast again and then publishing the message `singleAdminMode=true` to the feed `santafeed`. 
![image](https://github.com/user-attachments/assets/32efad5e-d6ac-48a1-893a-45bbc718f911)

After a couple of seconds, the images on the monitor start to change and now show Santa riding a pogo stick, which is the answer we are looking for to complete this objective.
![image](https://github.com/user-attachments/assets/849a4da6-c143-457b-8268-953063951fb6)



### 🥇 GOLD MEDAL ###
#### Santa Vision A: ####
I’ll admit it took me a loooong time to figure out where to get started with obtaining the gold medal for this objective, until I spotted the answer literally staring me in the face at the bottom of the SantaVision login screen!

![image](https://github.com/user-attachments/assets/59169712-0af4-4cdc-897d-e59affa74feb)
 
It looks like there is another broadcast feed we can investigate, by logging in as `elfanon` and using the `elfmonitor` role to power on the monitors again and subscribing to the `sitestatus` feed.
We immediately see a very interesting message with a path to a **_Super Top Secret file_**.  We simply append this path to the url in the browser to download `applicationDefault.bin`

```console
File downloaded: /static/sv-application-2024-SuperTopSecret-9265193/applicationDefault.bin
Broker Authentication as superadmin succeeded
Broker Authentication as admin succeeded
Broker Authentication failed: WomblyC
Broker Authentication succeeded: WomblyC
Broker Authentication succeeded: AlabasterS
Broker Authentication failed: AlabasterS
```

Using the `file` command in Linux we can see that the .bin file we just downloaded uses the `jffs2` filesystem and the hint for this objective kindly points us towards a suitable tool called [Jefferson](https://github.com/onekey-sec/jefferson/) which we can use to analyse such files.
```bash
┌──(root㉿kali)-[/media/sf_SANS_Holiday_Hack_2024/Objective 13 - Santa Vision]
└─# ls
applicationDefault.bin
                                                                                                                                                           
┌──(root㉿kali)-[/media/sf_SANS_Holiday_Hack_2024/Objective 13 - Santa Vision]
└─# file applicationDefault.bin 
applicationDefault.bin: Linux jffs2 filesystem data little endian
                                                                                                                                                           
┌──(root㉿kali)-[/media/sf_SANS_Holiday_Hack_2024/Objective 13 - Santa Vision]
└─# apt-get install python3-jefferson
┌──(root㉿kali)-[/media/sf_SANS_Holiday_Hack_2024/Objective 13 - Santa Vision]
└─# jefferson applicationDefault.bin -d applicationdir                                                     
dumping fs to /media/sf_SANS_Holiday_Hack_2024/Objective 13 - Santa Vision/applicationdir (endianness: <)
Jffs2_raw_inode count: 47
Jffs2_raw_dirent count: 47
writing S_ISREG .bashrc
writing S_ISREG .profile
```

Once Jefferson outputs the contents of the .bin file to a directory, this objective starts to seem somewhat familiar to what we did with [Mobile Analysis](OBJECTIVE%2008%20-%20Mobile%20Analysis.md) earlier on.  So, my first thought is to `grep` recursively for anything containing `password` or `secret` and sure enough, this points us towards ``/app/src/accounts/views.py`` which contains a reference to a **_top-secret database file_** at ``/sv2024DB-Santa/SantasTopSecretDB-2024-Z.sqlite``

![image](https://github.com/user-attachments/assets/73cf4dee-6365-493b-ad33-8a687c154f70)
 
Once again, we can download this by simply appending the full path to the Santa Vision URL in the browser (or use `wget`).  All that remains is for us to open the file in `sqlite3` and look at the contents of the `users` table to get the username and password for `SantaSiteAdmin`!

```bash
┌──(root㉿kali)-[/media/sf_SANS_Holiday_Hack_2024/Objective 13 - Santa Vision]
└─# file SantasTopSecretDB-2024-Z.sqlite 
SantasTopSecretDB-2024-Z.sqlite: SQLite 3.x database, last written using SQLite version 3046000, file counter 16, database pages 5, cookie 0x2, schema 4, UTF-8, version-valid-for 16
```
```sql
sqlite> SELECT * from users;
1|santaSiteAdmin|S4n+4sr3411yC00Lp455wd|2024-01-23 06:05:29.466071|1
```

#### Santa Vision B: ####
We can use the newly acquired username and password combination to log in to the SantaVision portal.  When doing so, have a good look at the headers in the network response from the server – looks like the username and password we’re looking for have been served to us right away – nice!

![image](https://github.com/user-attachments/assets/227db7f6-784b-428b-b410-057a44585162)


#### Santa Vision C: ####
When subscribing to the broadcast with the new username and password we still get the same feed as we did for the silver medal, so maybe there’s more to the elves’ mission’s code-name than just a group of random letters.  The reference to **_“sixteen elves”_** and the lack of any special characters in the code-name immediately made me think of a **Caeser Cipher** – presumably with a shift key of 16, i.e. each letter is replaced by the corresponding letter of the alphabet 16 spaces down, so A becomes Q, B becomes R, etc…  To decode, we simply reverse the direction:

|Ciphertext:|Q|R|S|T|U|V|W|X|Y|Z|A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P
|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|--|
|Plaintext: |A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|W|X|Y|Z

So Idemcerybu decodes to **Snowmobile**.

#### Santa Vision D: ####
For the final part of this objective, we need to send the MQTT message `singleAdminMode=true` just as we did [for the silver medal](OBJECTIVE%2013%20-%20Santa%20Vision.md#santa-vision-d).  However, this time we have no web interface available to post the message.   No worries – we can simply use a tool such as [MQTTX](https://mqttx.app/) for this.  We use the `santashelper2024` username and password as our credentials and point it towards `ws://<santavision ip>:9001`.  

![image](https://github.com/user-attachments/assets/2b6991e0-62b5-4869-9522-98c0c8af5847)

![image](https://github.com/user-attachments/assets/53c031c2-0869-4ee4-90bd-1d9bd8063024)


Then simply send a message to `santafeed` saying `singleAdminMode=true`.

 ![image](https://github.com/user-attachments/assets/a6bf799c-fad4-4765-acf0-bcdbad046e75)

Now, if we go back to the SantaVision portal and load up the `northpolefeeds` broadcast, we can see Santa riding some cool hovercrafts and we have our answer for the gold medal 😊

 ![image](https://github.com/user-attachments/assets/c239f673-55f5-4593-8df0-25097f671954)





