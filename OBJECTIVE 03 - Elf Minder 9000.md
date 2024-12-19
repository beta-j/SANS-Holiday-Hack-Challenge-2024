# OBJECTIVE 3 - Elf Miner 9000 #

## OBJECTIVE : ##
>Assist Poinsettia McMittens with playing a game of Elf Minder 9000.
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 3</summary>
  
>-	Some levels will require you to click and rotate paths in order for your elf to collect all the crates.
>-	Be sure you read the "Help" section thoroughly! In doing so, you will learn how to use the tools necessary to safely guide your elf and collect all the crates.
>-	When developing a video game—even a simple one—it's surprisingly easy to overlook an edge case in the game logic, which can lead to unexpected behavior.

</details>

#  

## PROCEDURE : ##
### GOLD MEDAL ###

You can just complete the levels normally to get a **Silver Medal**, but quite honestly, it’s a bit of headache to figure them all out and it’s more worth your while to go straight for the gold and hack your way through the levels.

Looking at the console we find two javascript files; `guide.js` and `game2.js`.  There are some interesting points that stand out here:
-	`guide.js` declares a variable called `whyCantIholdAllTheseSprings`.  The variable contains ASCII art of a man holding three springs and appears to be sent to the console output when the number of springs is greater than 2 (*lines 367-369*)
-	A chunk of `console.log` debug text in `game2.js` stands out in *lines 522 to 530*.  The text implies that there is an ‘editor’ mode and we can see that the `isEditor` variable is being obtained from the URL parameter `edit` in *line 520*
    -	We can also see that the level of the game is determined by the URL parameter `level`.
    -	We can get the current values for Resource ID and Level Number by typing `urlParams.id` and `urlParams.level` in the console
-	*Lines 1064 to 1069* include a congratulations message that is shown when all the levels are completed and it hints at the existence of a hidden level called ‘**A Real Pickle**’

From the ‘elements’ tab of the console we know that the URL for the game’s iframe is [https://hhc24-elfminder.holidayhackchallenge.com/index.html](url) .  So now we can access the game directly in a new window to any level we like (including A Real Pickle) by calling the following url: [https://hhc24-elfminder.holidayhackchallenge.com/index.html?id=4f72a2c3-3329-417d-9559-28f75c4303c7&level=A%20Real%20Pickle](url)

We can also enter **editor mode** by adding `&edit=true` to the end of the URL.  The editor screen allows us to edit the existing game elements and place new ones, but most importantly it allows us to place springs in positions which would otherwise be disallowed – for example right next to the start flag or right next to boulders.  The console also conveniently tells us that all the level data is stored in a variable called `game.entities`.  If we type this variable name in console, we can see that it is an array consisting of several sets, each set gives the x and y coordinates and the element type for each element.  The entity types are defined at the start of `guide.js` as `start`, `end`, `crate`, `blocker`, `hazard`, `steam`, `portal` and `spring` assigned to numbers 0 to 7 respectively.

Nevertheless, it’s not as easy as it looks now.  We can’t just remove all the obstacles and crates and draw a straight path to the finish.  The game has a number of checks and will throw a Captain Planet themed (lol) error if our elf passes through a location which is supposed to be occupied by an obstacle – so all the boulders and crates must remain where they stand.

Using console, we can add spring and tunnel elements to the game where they would otherwise not have been possible in editor mode.  For example, we can fit in a tunnel exit in the tiny gap between the finish flag and the boulder in *A Real Pickle* with a console command such as `game.entities[23]=[10,9,6]`  (be sure to check the length of `game.enitities` first so you use the correct array index).

This way we can plot a course for this level that does not need any clicks and uses multiple springs (I also added some hot sand just to make the elf go faster).  Mine looks like this:
![image](https://github.com/user-attachments/assets/023c6289-7261-4fa8-8abc-dc065a579a5a)

And that completes the objective with a gold medal.

#
[<<< Previous Objective (02)](OBJECTIVE%2002%20-%20Elf%20Connect.md)|......................................................................................................| [Next Objective (04) >>>](OBJECTIVE%2004-%20cURLing.md)|
:-|--|-:
