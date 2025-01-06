# OBJECTIVE 8 - Mobile Analysis #
Difficulty: ❄️❄️

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
### 🥈 SILVER MEDAL ###
For this objective we are given [an .apk file with a mobile application](Assets/SantaSwipe.apk).  Just to see what it does, we can install it on an android phone (or an emulator).  Next let’s try and figure out who got left off the Naughty/Nice list.  


Let’s start by decompiling the apk file using apktooL:
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

### 🥇 GOLD MEDAL ###

For the gold medal part of this objective, we are given [a revised mobile app – this time in `.aab` format](Assets/SantaSwipeSecure.aab).  Since we already have a general idea of how the app works from obtaining the silver medal, we should try to repeat our steps, but first we should take the advice of one of the hints we’re given and convert the `.aab` file into `.apk`.

I decided to use bundletool to do this:
```console
┌──(root㉿kali)-[/home/kali/mobile_analysis]
└─# wget https://github.com/google/bundletool/releases/download/1.17.2/bundletool-all-1.17.2.jar
┌──(root㉿kali)-[/home/kali/mobile_analysis]
└─# alias bundletool='java -jar bundletool-all-1.17.2.jar'
┌──(root㉿kali)-[/home/kali/mobile_analysis]
└─# bundletool build-apks --bundle=./SantaSwipeSecure.aab --output=./SantaSwipeSecure.apks --mode=universal
WARNING: The APKs won't be signed and thus not installable unless you also pass a keystore via the flag --ks. See the command help for more information.
                                                                                                                                                           
┌──(root㉿kali)-[/home/kali/mobile_analysis]
└─# ls
apktool  apktool.jar  bundletool-all-1.17.2.jar  SantaSwipe  SantaSwipe.apk  SantaSwipeSecure.aab  SantaSwipeSecure.apks
```

Bundletool creates a file with a .apks extension which needs to be changed into a zip file and extracted:
```console
┌──(root㉿kali)-[/home/kali/mobile_analysis]
└─# cp SantaSwipeSecure.apks SantaSwipeSecure.zip                       

┌──(root㉿kali)-[/home/kali/mobile_analysis]
└─# unzip SantaSwipeSecure.zip -d .
Archive:  SantaSwipeSecure.zip
 extracting: ./toc.pb                
 extracting: ./universal.apk         
```

Next, we can decompile with apktool like we did for the [silver medal](#SILVER-MEDAL):
```console
┌──(root㉿kali)-[/home/kali/mobile_analysis]
└─# apktool d universal.apk  
```

Now that we have a pretty good idea what to look out for, we can use `grep` to search for `SELECT` and `FROM` recursively in all the directories to try and narrow-down our search to a few interesting files where items are being called from the database.
```console
┌──(kali㉿kali)-[~/mobile_analysis/universal]
└─$ grep -r SELECT | grep FROM
smali/com/northpole/santaswipe/DatabaseHelper.smali:    const-string v3, "SELECT Item FROM "
smali/com/northpole/santaswipe/MainActivity$WebAppInterface.smali:    const-string v2, "SELECT Item FROM NaughtyList"
smali/com/northpole/santaswipe/MainActivity$WebAppInterface.smali:    const-string v2, "SELECT Item FROM NiceList"
smali/com/northpole/santaswipe/MainActivity$WebAppInterface.smali:    const-string v2, "SELECT Item FROM NormalList"
```

From the results of this search it looks like it’s worth having closer look at `smali/com/northpole/santaswipe/DatabaseHelper.smali`.  Towards the top of this file, we can see a method called `insertInitialData` which seems to be updating the database with a several encrypted srtings:

```javascript
.method private final insertInitialData(Landroid/database/sqlite/SQLiteDatabase;)V
    .locals 25
    const/16 v0, 0x10e
    .line 55
    new-array v0, v0, [Ljava/lang/String;
    const/4 v1, 0x0
    const-string v2, "L2HD1a45w7EtSN41J7kx/hRgPwR8lDBg9qUicgz1qhRgSg=="
    aput-object v2, v0, v1
    const/4 v1, 0x1
    .line 56
    const-string v2, "IWna1u1qu/4LUNVrbpd8riZ+w9oZNN1sPRS2ujQpMqAAt114Yw=="
```
Further down, towards the end of the file we can identify another private method, this time called `encryptData` that is most likely responsible for encrypting the data in the database.  From this we can tell that the data is being encrypted using a **AES-GCM** cipher and then encoded with base64.  AES-GCM encryption requires a *Key* and an *initial value*, which need to look for in our decompiled app.

```javascript
.method private final encryptData(Ljava/lang/String;)Ljava/lang/String;
    .locals 5
    .line 173
    :try_start_0
    const-string v0, "AES/GCM/NoPadding"
    invoke-static {v0}, Ljavax/crypto/Cipher;->getInstance(Ljava/lang/String;)Ljavax/crypto/Cipher;
    move-result-object v0
    .line 174
    new-instance v1, Ljavax/crypto/spec/GCMParameterSpec;
    iget-object v2, p0, Lcom/northpole/santaswipe/MainActivity$WebAppInterface;->this$0:Lcom/northpole/santaswipe/MainActivity;
    invoke-static {v2}, Lcom/northpole/santaswipe/MainActivity
.
.
.
>checkNotNullExpressionValue(Ljava/lang/Object;Ljava/lang/String;)V
    invoke-virtual {v0, p1}, Ljavax/crypto/Cipher;->doFinal([B)[B
    move-result-object p1
    const/4 v0, 0x0
    .line 177
    invoke-static {p1, v0}, Landroid/util/Base64;->encodeToString([BI)Ljava/lang/String;
.
.
.

.method public constructor tells us to look for the iv  (initial value) and ek (encryption key) value in /com/northpole/santaswipe/R$string
.method public constructor <init>(Landroid/content/Context;)V
.
.
.
    .line 25
    sget v0, Lcom/northpole/santaswipe/R$string;->ek:I
    invoke-virtual {p1, v0}, Landroid/content/Context;->getString(I)Ljava/lang/String;
.
.
.
    .line 26
   sget v2, Lcom/northpole/santaswipe/R$string;->iv:I
    invoke-virtual {p1, v2}, Landroid/content/Context;->getString(I)Ljava/lang/String;
.
.
.
```


If we have a look inside `R$string.smali`, it gives us the index for `iv` and `ek`:
```javascript
# static fields
.field public static app_name:I = 0x7f090001
.field public static ek:I = 0x7f090033
.field public static iv:I = 0x7f090037
```

We can now `grep` for these values and find `/universal/res/values/strings.xml` (the hint makes sense now).  From this we get the base64 encoded values for `iv` and `ek`:
```javascript
    <string name="ek">rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw=</string>
    <string name="iv">Q2hlY2tNYXRlcml4</string>
```

At this point I tried using Cyberchef to decode the encrypted values found in `DatabaseHelper.smali`, but it became apparent that I needed some kind of *Authentication tag*….so I asked [ChatGPT](https://chatgpt.com/) about this and it explained that AES-GCM normally appends a *16-byte tag* to the ciphertext and therefore I would need to split the last 16 bytes from the ciphertext for each entry and use that as my *authentication tag*.  ChatGPT also conveniently provided me with [a python script](Code/mobile_analysis_database_decrypt.py) which I could use to decode the entries.

Rather than entering all the entries one by one, I scrolled through `DatabaseHelper.smali` looking for something that looks a bit different and sure enough, at the end of the file I noticed a considerably larger chunk of encoded text:

```javascript
    .line 39
    const-string v0, "IVrt+9Zct4oUePZeQqFwyhBix8cSCIxtsa+lJZkMNpNFBgoHeJlwp73l2oyEh1Y6AfqnfH7gcU9Yfov6u70cUA2/OwcxVt7Ubdn0UD2kImNsclEQ9M8PpnevBX3mXlW2QnH8+Q+SC7JaMUc9CIvxB2HYQG2JujQf6skpVaPAKGxfLqDj+2UyTAVLoeUlQjc18swZVtTQO7Zwe6sTCYlrw7GpFXCAuI6Ex29gfeVIeB7pK7M4kZGy3OIaFxfTdevCoTMwkoPvJuRupA6ybp36vmLLMXaAWsrDHRUbKfE6UKvGoC9d5vqmKeIO9elASuagxjBJ"
So, I popped this interesting looking ciphertext into the Python script that ChatGPT so kindly created for me and deciphered it into an interesting SQL command:
CREATE TRIGGER DeleteIfInsertedSpecificValue
    AFTER INSERT ON NormalList
    FOR EACH ROW
    BEGIN
        DELETE FROM NormalList WHERE Item = 'KGfb0vd4u/4EWMN0bp035hRjjpMiL4NQurjgHIQHNaRaDnIYbKQ9JusGaa1aAkGEVV8=';
    END;
```

Once again, we find that there is a specific value that is being removed from the naughty and nice lists… all that remains is for us to decrypt the ciphertext containing this value and we get:

`Decoded String: Joshua, Birmingham, United Kingdom`

And finally we have our answer – this time it was **Joshua** from **Birmingham** who was intentionally being left out!


#
[<<< Previous Objective (07 - Hardware Hacking 101 - Part 2)](OBJECTIVE%2007%20-%20Hardware%20Hacking%20101%20(Part%202).md)|.........................................................| [Next Objective (09 - Drone Path >>>](OBJECTIVE%2009%20-%20Drone%20Path.md)|
:-|--|-:

