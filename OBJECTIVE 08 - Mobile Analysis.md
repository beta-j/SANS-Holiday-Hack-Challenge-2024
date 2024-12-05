# OBJECTIVE 8 - Mobile Analysis #

## OBJECTIVE : ##
>Help find who has been left out of the naughty AND nice list this Christmas.  Please speak with Eve Snowshoes for more information.
#
## HINTS: ##
<details>
  <summary>Hints provided for Objective 8</summary>
  
>-	EASY
>    -  Try using apktool or jadx
>    -  Maybe look for what names are included and work back from that?
>-  HARD
>    -  So yeah, have you heard about this new Android app format?  Want to convert it to an APK file?
>    -  Obfuscated and encrypted?  Hmph.  Shame you can’t just run strings on the file.
  
</details>

#  

## PROCEDURE : ##
### SILVER MEDAL ###
For this objective we are given an .apk file with a mobile application.  Just to see what it does, we can install it on an android phone (or an emulator).  Next let’s try and figure out who got left off the Naughty/Nice list.  Let’s start by decompiling the apk file using apktooL:
```console
┌──(kali㉿kali)-[/tmp/mobapp]
└─$ apktool d SantaSwipe.apk
```

We see that we have an `index.html` file and looking inside it we see that `Android.getNormalList()`, `AndroidgetNiceList()` and `Android.getNaughtyList()` methods are being called by the app to bring up the names on the phone screen.

So, we know the names must be listed somewhere and just by using the app we know what names are included on the list.  We can simply `grep` for one of these names and open the file that shows up in the result:
```console
┌──(kali㉿kali)-[/tmp/mobapp/SantaSwipe]
gre└─$ grep -r Carlos   
smali_classes3/com/northpole/santaswipe/DatabaseHelper.smali:130:    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Carlos, Madrid, Spain\');"
```
Now that we know to look inside DatabaseHelper.smali, we can go through the names in the file one by one and swipe them off the list on the app until we find one that isn’t included in the app….and it looks like the unlucky girl is **Ellie**, from **Alabama, US**.

If we run another `grep` for `Ellie` this time we can see that her entry is being specifically excluded in `smali_classes3/com/northpole/santaswipe/MainActivity$WebAppInterface.smali`
```console
┌──(root㉿kali)-[/home/kali/mobile_analysis/SantaSwipe]
└─# grep -r Ellie 
smali_classes3/com/northpole/santaswipe/DatabaseHelper.smali:    const-string v0, "INSERT INTO NormalList (Item) VALUES (\'Ellie, Alabama, USA\');"
smali_classes3/com/northpole/santaswipe/MainActivity$WebAppInterface.smali:    const-string v3, "SELECT Item FROM NormalList WHERE Item NOT LIKE \'%Ellie%\
```
