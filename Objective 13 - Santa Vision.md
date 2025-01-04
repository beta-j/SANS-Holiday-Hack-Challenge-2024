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

We can now have a look at the html code for the page by hitting F12 on the keyboard to bring up the browser’s developer tools and just by having a quick look through the html, we can quickly spot a comment with what appears to be a username and password for MQTT.  We can successfully use these to log in to the SantaVision portal.  This also gives us our answer for Santa Vision A.




### 🥇 GOLD MEDAL ###

In the silver medal we’ve already eliminated the possibility of `elfIds.js` and  `Phaser-snowball-game.js` having any client-side accessible variables.

This leaves us with the final `.js` file called `reconnecting-websocket.min.js` which also appears to be a standard library, but on closer inspection it seems to have some added code at the end.  The code adds a function which refers to a `MOASB`  (I’m guessing this stands for **_Mother Of All Snowball Bombs_**) and assigns it to `window.bgDebug` which makes it globally accessible via the `bgDebug` property on the `window` object.  The first line of the function is:     
```javascript
if (e.type && "moasb_start" === e.type && mainScene && !mainScene.moasb_started) {
```
This checks whether the event `e` has a type property with the value `moasb_start`, if this condition is met the function triggers the MOASB scene.

Now that we’ve identified this crucial bit of code with a client-side exposed property, all we need to do is start a new game, head to the browser’s console and type in `window.bgDebug({type: “moasb_start”})`. Now sit back and enjoy the show as a bomber aircraft flies in carrying the MOASB and launches it with Jared riding it, wielding an axe and using some questionable elf language!

This attack quickly flattens the opposition and grants us a gold medal – **Yippee-Ka-Yay!**

![image](https://github.com/user-attachments/assets/7eae4eff-e7d0-46a1-b865-facec154c119)   ![image](https://github.com/user-attachments/assets/bd2c36aa-f45e-4121-bd03-fd4963aaef13)


