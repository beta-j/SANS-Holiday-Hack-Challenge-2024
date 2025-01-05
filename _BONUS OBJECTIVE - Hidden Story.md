# BONUS OBJECTIVE - Hidden Story #


When we retrieve the strips of paper from the shredder in [Objective 5 – Frosty Keypad](OBJECTIVE%2005%20-%20Frosty%20Keypad.md) we get a zip file with _“one thousand little tiny shredded pieces of paper—each scrap whispering a secret, waiting for the right hardware hacker to piece the puzzle back together!”_.  We were able to piece these together for [Objective 6](OBJECTIVE%2006%20-%20Hardware%20Hacking%20101%20(Part%201).md), but that’s not the only hidden message they hold!

Each jpg file in the zip file appears to hold an interesting string in the **comments** field of the metadata.  I used a python script to extract comments field from metadata to a text file and then pasted the contents in cyberchef and converted from base64.  This gives us pairs of strings enclosed in quotation marks, separated by a comma and enclosed in square brackets, eg:
```
["==gN", "e s"]["==QO", "eal"]["=IjM", "y i"]["=ETM", "f t"]["=MTM", "Nor"]["=MjM", "f y"]["=kjM", "r),"]["=cTM", "not"]["=YTM", "e ("]["=gjM", "dee"]["==gM", "g a"]["=UjM", "re "]["==AO", "y r"]["==QN", " th"]["==AN", " in"]["=QTM", "th "]["==wM", "go,"]["=YjM", "a r"]["=ATM", "m o"]["=kTM", "o f"]
```

We can clean up this data in Cyberchef by:
-	Matching REGEX ``\[([^\]]+)\]`` to extract the strings from the square brackets
-	Replacing `“, “` with a `%` to create a %-delimited list
-	Removing all `“`
  
This is the full cyberchef recipe used for this operation:
```cyberchef
From_Base64('A-Za-z0-9+/=',true,false)
Regular_expression('User defined','\\[([^\\]]+)\\]',false,false,false,false,false,false,'List capture groups')
Find_/_Replace({'option':'Regex','string':', '},'%',true,false,true,false)
Find_/_Replace({'option':'Simple string','string':'"'},'',true,false,true,false)
```

This gives us data that looks something like this:
```
==gN%e s
==QO%eal
=IjM%y i
=ETM%f t
=MTM%Nor
=MjM%f y
=kjM%r),
=cTM%not
=YTM%e (
```

You will notice a lot of `=` and `==` patterns at the start of each string to the left of the `%`, but with base64 encoding we’d normally expect these to be at the end.  It looks like the strings are a mirror image of what they should be – just like the reconstructed image we got in Objective 6.  On the other hand, the strings to the right of the `%` appear to form legible English words as they are.

Next, we can copy and save all data to a text file and open text file with excel using the `%` as the cell delimiter and save as `.xlsx`.  We can use an Excel formula on each line to reverse the order of characters in the first column: ``=TEXTJOIN("",1,MID(A1,{10,9,8,7,6,5,4,3,2,1},1))``. Then copy the entire column into [https://www.base64decode.org/](https://www.base64decode.org/) which allows us to base64 “_decode each line separately_” which Cyberchef doesn’t do.  The resulting output is a list of numbers which presumably are telling us the order in which we need to stort the pieces of English text.  We can paste the list of numbers back in Excel and sort the whole thing by that column in ascending order.

Finally, we can copy the column with the story text and paste it in Cyberchef and clean it all up with a **remove whitespace** recipe:
```cyberchef
Remove_whitespace(false,true,true,true,true,false)
```

And this gives us the following hidden story – cool!


>Long ago, in the snowy realm of the North Pole (not too far away if you're a reindeer), there existed a magical land ruled by a mysterious figure known as the Great Claus. Two spirited elves Twinkle and Jangle roamed this frosty kingdom defending it from the perils of holiday cheerlessness. Twinkle, sporting a bright red helmet-shaped hat that tilted just so, as quick-witted and even quicker with a snowball. Jangle, a bit taller wore a green scarf that drooped like a sleepy reindeer’s ears. Together, they were the Mistletoe Knights, the protectors of the magical land and the keepers of Claus’ peace.
>
> One festive morning the Great Claus summoned them for a critical quest. 'Twinkle, Jangle, the time has come,' he announced with a voice that rumbled like thunder across the ice plains. 'The fabled Never-Melting Snowflake, a relic that grants one wish, lies hidden beyond the Peppermint Expanse. Retrieve it and all marshmallow supplies will be secured!' Armed with Jangle’s handmade map (created with crayon and a lot of optimism) the duo set off aboard their toboggan the Frostwing.
However the map led them in endless loops around the Reindeer Academy much to the amusement of trainee reindeer perfecting their aerial manoeuvres. Blitzen eventually intercepted them chuckling, 'Lost fellas? The snowflake isn’t here. Try the Enchanted Peppermint Grove!' Twinkle facepalmed as Jangle pretended to adjust his map. With Blitzen’s directions they zoomed off again, this time on the right course.
>
>The Peppermint Grove was alive with its usual enchantments - candy cane trees swayed and sang ancient ballads of epic sleigh battles and the triumphs of Claus’ candy cane squadrons. Twinkle and Jangle joined the peppermint choir, their voices harmonizing with the festive tune. Hours later the duo stumbled upon a hidden cave guarded by giant gumdrop sentinels (luckily on their lunch break). Inside the air shimmered with Claus’ magic.
>
>There it was - the Never-Melting Snowflake, glistening on a pedestal of ice. Twinkle’s eyes widened, 'We’ve found it Jangle! The key to infinite marshmallows!' As Twinkle reached for the snowflake, a voice boomed from the cave walls 'One wish, you have. Choose wisely or face the egg-nog of regret.' Without hesitation Jangle exclaimed, 'An endless supply of marshmallows for our cocoa!' The snowflake glowed, and with a burst of magic, marshmallows poured down, covering the cave in a fluffy, sweet avalanche. Back at the workshop, the elves were hailed as heroes - the Marshmallow Knights of Claus. They spent the rest of the season crafting new cocoa recipes and sharing their bounty with all. And so, under the twinkling stars of the northern skies, Twinkle and Jangle continued their adventures, their mugs full of cocoa, their hearts full of joy, and their days full of magic. For in the North Pole, every quest was a chance for festive fun, and every snowflake was a promise of more marshmallows to come.
