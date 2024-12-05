# OBJECTIVE 11 - Snowball Showdown #

## OBJECTIVE : ##
>Wombley has recruited many elves to his side for the great snowball fight we are about to wage. Please help us defeat him by hitting him with more snowballs than he does to us.

#  

## PROCEDURE : ##
### GOLD MEDAL ###
At first glance this game reminds me a lot of last year’s **Snowball Hero** challenge, so I started off by reading through [the notes in my writeup for last year’s Holiday Hack Challenge](https://github.com/beta-j/SANS-Holiday-Hack-Challenge-2023).  In a nutshell, last year we were able to edit the values of client-side variables to win the game, so that might be one approach to try this year too.

First, we need to figure out a way to play the game without having to team up with another player, which will make it a lot easier to test out some stuff in the browser console and see what it does.  The game conveniently launches in a new browser window and the URI ends with `&singlePlayer=false`.  It’s just a matter of changing this to `&singlePlayer=true` and reloading the page to launch the game in single-player mode. 

![image](https://github.com/user-attachments/assets/da0b0e94-1b01-48b1-b4ac-b005384fc51e)

Next, we can have a look at the game’s source code by hitting F12 to open the browser’s developer tools.  We can see there is a folder called `js` which contains four javascript files and we need to figure out which one we should start looking into.  `phaser.min.js` is a standard open-source JavaScript library for building HTML5 games, so we can ignore that for now.  `elfIds.js` declares a large number of constants to define elf names, taunts, etc…, so it’s not really interesting to us.  `phaser-snowball-game.js` has a single class called `SnowBallGame` and all the variables seem to be using `this.` notation.  In this case `this.` is defining each variable as a property of the `SnowBallGame` class and so they are not client-side accessible.  

![image](https://github.com/user-attachments/assets/64a47f29-01cf-4750-8c8a-882ffda51343)

This leaves us with the final `.js` file called `reconnecting-websocket.min.js` which also appears to be a standard library, but on closer inspection it seems to have some added code at the end.  The code adds a function which refers to a `MOASB`  (I’m guessing this stands for *Mother Of All Snowball Bombs*) and assigns it to `window.bgDebug` which makes it globally accessible via the `bgDebug` property on the `window` object.  The first line of the function is     `if (e.type && "moasb_start" === e.type && mainScene && !mainScene.moasb_started) {` which checks if the event `e` has a type property with the value `moasb_start`, if this condition is met the function triggers the MOASB scene.

Now that we’ve identified this crucial bit of code with a client-side exposed property, all we need to do is start a new game, head to the browser’s console and type in `window.bgDebug({type: “moasb_start”})`. Now sit back and enjoy the show as a bomber aircraft flies in carrying the MOASB and launches it with Jared riding it, wielding an axe and using some questionable elf language!

This attack quickly flattens the opposition and grants us a gold medal – **Yippee-Ka-Yay!**

![image](https://github.com/user-attachments/assets/7eae4eff-e7d0-46a1-b865-facec154c119)   ![image](https://github.com/user-attachments/assets/bd2c36aa-f45e-4121-bd03-fd4963aaef13)


