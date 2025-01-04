# OBJECTIVE 9 - Drone Path #
Difficulty: ❄️❄️❄️

## OBJECTIVE : ##
>Help the elf defecting from Team Wombley get invaluable, top secret intel to Team Alabaster. Find Chimney Scissorsticks, who is hiding inside the DMZ.
#

## PROCEDURE : ##
### 🥈 SILVER MEDAL ###
When accessing the terminal, we can either access a login screen or a fileshare.  Given that we don’t have any login credentials (yet), let’s have a look at the fileshare.  There is a single file we can download called `fritjolf-Path.kml`.

Kml files typically store a number of coordinates in sequence to create a path between each point.  The most popular program to open such files is [Google Earth](https://earth.google.com/web/).  If we download the file and open it in Google Earth we can see what is presumably a flight path which interestingly describes the outline of a word: `GUMDROP1` over Antartica:
![image](https://github.com/user-attachments/assets/058d2439-321b-49ed-91bd-006d22a04906)

This looks suspiciously like a potential password, and we can safely assume that the user creating this is `fritjolf` based on the file name.

So, we can now try logging in with these credentials:
![image](https://github.com/user-attachments/assets/daee2b59-0e66-47b7-a2ef-783b39fbec8b)

Having logged-in successfully we now have access to some new areas:
-	**Elf Drone Workshop** which requires us to provide a _Drone name _as an input
-	**Profile Page** with details about the elf with the username `fritjolf` – there’s also an interesting link to a csv file 
-	**Admin console** which requires us to provide a drone fleet administration code
  
Let’s start off by downloading the csv file that is linked under the profile section.  According to the note on the same profile page , the name of the drone is the same as the location of the secret snowball warehouses.

![image](https://github.com/user-attachments/assets/ff492e68-bf0e-4178-bf94-4ee897169133)

The csv file consists of a number of lat/long coordinate sets and the associated flight altitude at each point.  We can use these to create [our own .kml file](Code/secret-Path.kml) and open it in Google Earth again.

If we follow the flight path from one coordinate to the next, we see that each coordinate is on top of a geographical feature that resembles a letter of the alphabet.  We get `ELF-HAWK` which must be the name of the drone.  We can check this on the Elf Drone Workshop page:
![image](https://github.com/user-attachments/assets/0ba78a60-c1de-4587-b1cb-7736fd4feecc)

And we are now pointed to a new csv file `ELF-HAWK-dump.csv`.  It’s interesting how **LONG** and **LATTER** are capitalised – I’m guessing this is a hint referring to the LAT/LONG values in the csv.

Opening the csv file we are now faced with another list of coordinate points, but this time the list is huge with a total of 3272 individual points!

We can do the same thing we did earlier and convert these to a `.kml` file.  The easiest way is to clean up the `.csv` file by removing the headers and anything that is not longitude or latitude data.  This leaves us with a file containing comma-separated values for longitude and latitude which we simply paste into a text editor to create a custom `.kml` file.

Nevertheless, it’s not going to be that easy this time around.  Opening the `.kml` file shows us a whole mess of overlapping paths going around the globe in the northern hemisphere.   Looking closely at the path, some letters are recognisable but it’s impossible to make out a coherent string of text.

Let’s have another look at the list of coordinate pairs in the `.csv` file…  It looks like the values for longitude tend to increase the further down the list we go – it’s not a 100% consistent increase – but there’s a definite pattern.  It’s also strange that the longitude values can get really large, whereas actual longitude values can only be between -180 and 180 degrees.  This leads me to think that the path that these coordinates describe, goes round and round the globe passing over itself several times.

The next step takes a while to complete – so get a cup of coffee and settle down.  We need to manually split the `.kml` file into multiple paths.  Each path starts when the longitude values start to consistently exceed 180, 360, 540, 720, 900, 1080, 1260 and 1440 respectively (i.e. in steps of 180 each), thus dividing the data into nine parts.  We can use this to create 9 separate `.kml` files ([or a single .kml file with 9 separate placemark sets](Code/All_Secret_Paths.kml)).   If we open these in Google Earth, we can now view them one by one and reconstruct the hidden message: **DroneDataAnalystExpertMedal**

![image](https://github.com/user-attachments/assets/292e0aff-32f6-49a0-93c3-c6d87ae55cb0)

Submit this as the password to the admin panel to get the Silver Medal:

![image](https://github.com/user-attachments/assets/3838cb61-a750-4eb1-98e5-e6b24a9f95d6)

#
### 🥇 GOLD MEDAL ###
Having obtained access to the drone fleet administration, Chimney Scissorsticksticks tells us to _“dig deeper”_ and hints at the existence of an _“injection flaw”_ that we might be able to exploit.

Chimney’s hint is very helpful and it immediately points us towards looking for an SQL injection point.  While still logged in with the `fritjolf` account we have access to two user-input fields that might possibly be susceptible to SQLi, so it’s just a matter of pasting in the infamous `‘OR 1=1 –` string to see if it does anything interesting.  Luckily we see some interesting results when testing this in the search box of the Workshop page.

![image](https://github.com/user-attachments/assets/b8d48759-a600-4d7d-b885-2b2a8f318b5a)

We now have a list of valid drone names along with their specifications.  We can start searching for the drone names in the same search box one by one, until we find something useful.

The listing for **Pigeon-Lookalike-v4** seems to be giving us some hints to point us in the right direction for a gold medal.  It tells us that _“There is something fhishing with [sic] some of the files”_ and that _“there was some talk about only TRUE carvers would find secrets and that FALSE ones would never find it”_.

The capitalised _“TRUE”_ and _“FALSE”_ in that last sentence immediately remind me of the `ELF-HAWK-dump.csv` file which had loads of columns with values for `TRUE` or `FALSE` in them.  Typically another way to represent `TRUE` and `FALS`E values in electronics is with a `1` or `0`, so my first thought is that there might be a binary message hidden in the `.csv` file.

Extracting this message is quite simple, but it requires us to play around with the formatting of the `.csv` file.  I used Microsoft Excel to remove all the columns that had data that wasn’t a TRUE/FALSE value.  Then I removed all the rows which were all `TRUE` or all `FALSE` as these will not be able to provide me with any information.  Next I used a simple “find and replace” in Excel to change all the `TRUE` entries into `1`s and all the `FALSE` entries into `0`s.  Finally I used a `CONCAT` function at the end of each row to concatenate all the `0` and `1` values for each row into a 58-bit binary number.

I could then copy and paste the binary numbers into [Cyberchef](https://icyberchef.com/) and use a “From Binary” recipe with an 8-bit byte length to convert the binary into a beautiful piece of ASCII art which also contains our password for the admin panel to grant us a gold medal:

![image](https://github.com/user-attachments/assets/55310b81-c2a5-495f-b77d-599ac5dce91f)



