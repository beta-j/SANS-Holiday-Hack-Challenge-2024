# OBJECTIVE 11 - Snowball Showdown #
Difficulty: ❄️❄️

[Direct Link](https://hhc24-snowballshowdown.holidayhackchallenge.com/)

## OBJECTIVE : ##
>Wombley has recruited many elves to his side for the great snowball fight we are about to wage. Please help us defeat him by hitting him with more snowballs than he does to us.

#  

## PROCEDURE : ##
### 🥈 SILVER MEDAL ###
At first glance this game reminds me a lot of last year’s **Snowball Hero** challenge, so I started off by reading through [the notes in my writeup for last year’s Holiday Hack Challenge](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023).  In a nutshell, last year we were able to edit the values of client-side variables to win the game, so that might be one approach to try this year too.

First, we need to figure out a way to play the game without having to team up with another player, which will make it a lot easier to test out some stuff in the browser console and see what it does.  The game conveniently launches in a new browser window and the URI ends with `&singlePlayer=false`.  It’s just a matter of changing this to `&singlePlayer=true` and reloading the page to launch the game in single-player mode. 

![image](https://github.com/user-attachments/assets/da0b0e94-1b01-48b1-b4ac-b005384fc51e)

Next, we can have a look at the game’s source code by hitting F12 to open the browser’s developer tools.  We can see there is a folder called `js` which contains four javascript files and we need to figure out which one we should start looking into.  `phaser.min.js` is a standard open-source JavaScript library for building HTML5 games, so we can ignore that for now.  `elfIds.js` declares a large number of constants to define elf names, taunts, etc…, so it’s not really interesting to us.  `phaser-snowball-game.js` has a single class called `SnowBallGame` and all the variables seem to be using `this.` notation.  In this case `this.` is defining each variable as a property of the `SnowBallGame` class and so they are not client-side accessible.  

![image](https://github.com/user-attachments/assets/64a47f29-01cf-4750-8c8a-882ffda51343)

However, we can still play around with some of these variables using local overrides in Chrome.  The developer tools in Chrome allow us to replace any element that is being downloaded to one that is already on our local machine.  This includes obvious things like images, but it can also be used to override specific variables by creating a local copy of the JavaScript file and loading that instead.

In the developer console we can type directly into the source code to modify the parameters we want.  I chose to edit the following variables:
•	**Line 26**:		`this.throwRateOfFire = 10;`
•	**Line 680**:	`this.onlyMoveHorizontally = false;`
•	**Line 1292**:	`"blastRadius": 20000,`

By changing these variables, we will be able to fire off snowballs at a much faster rate and each snowball will have a massive blast area.  We will also be able to move our sprite up and down – effectively flying over and around obstacles and any damage done to terrain.  Once we’ve edited all the variables we want to play around with, we can right click on the source file and select **_Save As_** and save it in the Overrides directory we set Chrome to look at.  It’s important to keep the same filename when saving this.

Finally, we right-click on the filename for `Phaser-snowball-game.js` and select **_Override content_** (you’ll notice that the filename on the left pane of developer view now has a purple dot 🟣 on it indicating that a local override version is being loaded instead).  This instructs Chrome to load the local version of `Phaser-snowball-game.js` that we saved earlier instead of the version being downloaded from the server.

![image](https://github.com/user-attachments/assets/d1816d97-746b-4476-adf8-0624f88b5e51)

All that’s left is to reload the page and use our new superpowers to win the snowball fight against Wombley to get our Silver Medal.

![image](https://github.com/user-attachments/assets/1fe7cebb-9789-4d43-b9a4-13b75cbedb00)


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



 #
[<<< Previous Objective (10 - PowerShell)](OBJECTIVE%2010%20-%20PowerShell.md)|.........................................................| [Next Objective (12 - Snowball Showdown >>>](OBJECTIVE%2012%20-%20Microsoft%20KC7.md)|
:-|--|-:
