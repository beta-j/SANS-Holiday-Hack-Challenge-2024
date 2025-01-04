# OBJECTIVE 2 - Elf Connect #
Difficulty: ❄️
## OBJECTIVE : ##
>Help Angel Candysalt connect the dots in a game of connections.
#  

## PROCEDURE : ##
By reading through the instructions we know that this objective consists of a trivia game in which we need to group words that fall within the same sub-category.

### 🥈 SILVER MEDAL ###

To achieve the silver medal, you can just use your cybersecurity knowledge (and some Googling to fill-in the gaps).  Or you can have a look at the game’s code, which makes it really obvious what the correct groupings are. The sub-categories are defined in a cleartext array called `wordSets` which has four arrays of 16 elements each (0 to 15).  Each correct set is defined as the corresponding array position of 4 elements inside the array called `correctSets`. 

![image](https://github.com/user-attachments/assets/21c0fa34-c883-4fa2-8985-b9d2e63742f8)

As a short-cut we can copy and paste the contents of `wordSets` into a csv file and use that to create a spreadsheet that sorts the elements into the correct groups:

Array Index|Round 1|Round 2|Round 3|Round 4
---:|:---:|:---:|:---:|:---:|
0|Tinsel|Nmap|AES|IGMP|
5|Garland|netcat|RSA|IPX
10|Star|Wireshark|Blowfish|IP
14|Lights|Nessus|3DES|ICMP
 | | | | |
1|Sleigh|burp|WEP|TLS
3|Bag|OWASP|Zap|WPA2|SSL
7|Mittens|Nikto|TKIP|IPSec
9|Gifts|wfuzz|LEAP|SSH
 | | | | |
2|Belafonte|Frida|Symmetric|Ethernet
6|Jingle Bells|Cycript|Asymmetric|PPP
11|Crosby|AppMon|hash|IEEE 802.11
12|White Christmas|apktool|hybrid|ARP
| | | | |				
4|Comet|Metasploit|Caesar|HTTP
8|Vixen|Cobalt Strike|One-time Pad|FTP
13|Prancer|HAVOC|Ottendorf|SMTP
15|Blitzen|Empire|Scytale|DNS

In case you’re curious, the answers fall into the following sub-categories:

**Round 1 - Christmas :**
|    |     |     |     |     |
|---:|:---:|:---:|:---:|:---:|
|__Decorations:__|Tinsel|Garland|Star|Lights
|__Xmas Motifs:__|Sleigh|Bag|Mittens|Gifts
|__Carols:__|Belafonte|	Jingle Bells|	Crosby|	White Christmas
|__Reindeer:__|	Comet|	Vixen|	Prancer|	Blitzen

**Round 2 – Cybersecurity Tools:**
|    |     |     |     |     |
|---:|:---:|:---:|:---:|:---:|
|__Assessment Tools:__|	Nmap|	netcat|	Wireshark|	Nessus
|__WebApp Testing:__|	burp|	OWASP| Zap|	Nikto|	wfuzz
|__Mobile App Testing:__|	Frida|	Cycript|	AppMon|	apktool
|__C2 (Command & Control):__|	Metasploit|	Cobalt Strike|	HAVOC|	Empire

**Round 3 – Encryption:**
|    |     |     |     |     |
|---:|:---:|:---:|:---:|:---:|
|__Cryptographic Algorithms:__|	AES|	RSA|	Blowfish|	3DES
|__Wi-Fi Encryption:__|	WEP|	WPA2|	TKIP|	LEAP
|__Types of Cryptography:__|	Symmetric|	Asymmetric|	Hash|	Hybrid
|__Classical Ciphers:__|	Caeser|	One-Time Pad|	Ottendorf|	Scytale

**Round 4 – Networking**
|    |     |     |     |     |
|---:|:---:|:---:|:---:|:---:|
|__Internet Protocols:__|	IGMP	|IPX|	IP|	ICMP
|__Security Protocols:__|	TLS	|SSL|	IPSec|	SSH
|__Network Technologies:__|	Ethernet|	PPP|	IEEE 802.11|	ARP
|__Application Layer Protocols:__|	HTTP|	FTP|	SMTP|	DNS

### 🥇 GOLD MEDAL ###

For a gold medal we are tasked with beating the high-score of 50,000.  Playing the game normally, we are only awarded 100 points for each correct set of four words, so the maximum score is 1600 – quite far away from the target of 50,000.  So, it’s clear that we need to be a bit sneakier in our approach.

Having a look through the code again, we can see a variable called `score` that is being updated with our score every time we complete a set.  It is initially set to `0`, and by typing `score` in the browser console we can see it getting updated every time we complete a set.  So, we can simply type in `score = 999999` to give ourselves a new score.

![image](https://github.com/user-attachments/assets/281b77c7-072b-45d8-93fb-803bbb02655b)


All that’s left for us to do now, is to complete at least one more set and we have the new high-score 😊
![image](https://github.com/user-attachments/assets/dc299621-6ccc-4a4f-9641-83f70d93321a)


#
[<<< Previous Objective (01 - Holiday Hack Orientation)](OBJECTIVE%2001%20-%20Holiday%20Hack%20orientation.md)|.........................................................| [Next Objective (03 - Elf Minder 9000) >>>](OBJECTIVE%2003%20-%20Elf%20Minder%209000.md)|
:-|--|-:


