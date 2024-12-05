# OBJECTIVE 5 - Frosty Keypad #

## OBJECTIVE : ##
>In a swirl of shredded paper, lies the key. Can you unlock the shredder’s code and uncover Santa’s lost secrets?
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 4</summary>
  
>- Hmmmm. I know I have seen Santa and the other elves use this keypad. I wonder what it contains. I bet whatever is in there is a **National Treasure**!
>-	Well this is puzzling. I wonder if Santa has a seperate code. Bet that would cast some light on the problem. I know this is a stretch...but...what if you had one of those fancy UV lights to look at the fingerprints on the keypad? That might at least limit the possible digits being used...
>-	See if you can find a copy of that book everyone seems to be reading these days. I thought I saw somebody drop one close by...
</details>

#  

## PROCEDURE : ##
### SILVER MEDAL ###

Just a few steps away to the right-hand side of the screen there is a book lying on the ground – picking it up adds **‘Frosty Book’** to our inventory and it contains a poem over 14 pages.
The sticky note stuck to the shredder has five sets of three numbers each.  The first number in each set is between 2 and 14… which kind of reminds us of the number of pages in the book.  So, if the first number in each set refers to the page number, the second and third numbers in each set must refer to the word and letter positions respectively.  So 2:6:1 points to The 1st letter of the 6th word in Page 2, which is ‘*S*’.
Set|	Corresponding Letter
|---|:---:
2:6:1|	S
4:19:3|	A
6:1:1|	N
3:10:4|	T
14:8:3|	A

The result is “**SANTA**” which is a phrase that makes sense and indicates that we’re on the right track with this objective.  But we now need to change these letters into numbers we can key in on the keypad.  My first thought was a simple substitution cipher where A=1, B=2, C=3, etc..  but that won’t work in this case as we only have 10 possible digits.  So my next thought was to use the digit-to-letter allocation used on telephone keypads (like that shown in the image).
![image](https://github.com/user-attachments/assets/2cb95554-9b5b-4fbd-9e57-77eb931c3742)

This way we find that the key-code is **72682** which allows us to unlock the shredder.

Set|	Corresponding Letter|	Keypad Digit
---|:---:|:---:
2:6:1|	S|	7
4:19:3|	A|	2
6:1:1|	N|	6
3:10:4|	T|	8
14:8:3|	A|	2

![image](https://github.com/user-attachments/assets/9cba86e1-4d97-4566-88e7-073b6c6a9aee)![image](https://github.com/user-attachments/assets/0f1c72f2-2945-498f-a583-908a37db6cec)
This unlocks the shredder and allows me to collect a file called shreds.zip which appears to contain scanned copies of thin slivers of shredded paper as individual image files. 

### GOLD MEDAL ###
There is a UV flashlight hidden behind the stack of gifts just to the left of the shredder.  By using this on the keypad we can see that the numbers 2,6,7 and 8 where used.  Since we know that this is a five-digit pin, we must assume that one of the digits is used twice.

Microsoft CoPolit tells me that there are 960 possible unique combinations_("PROMPT: how many possible unique 5-digit combinations can you create with 4 digits where each digit is used at least once in each combination")_ so we need to find a way of automating this.  Since I got some practice using cURL recently, I decided to use Python to generate the possible 5-digit combinations and `POST` them to the game’s URL using cURL.  I used Microsoft Co-Pilot to help me generate the Python Code I used for this.  The code generates the possible combinations and submits each one in the format `{answer:pin}` as a JSON HTTP POST request and listens for a successful response code of `200`. I also included a 2 second delay between each combination attempt, since the server would only accept one request per second.

After running the script for a few minutes, I got a successful response with the combination **22786**.

![image](https://github.com/user-attachments/assets/7e2784b7-5913-49fa-b349-07f77a8e78b9)


