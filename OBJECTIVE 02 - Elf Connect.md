# OBJECTIVE 2 - Snowball Hero #

## OBJECTIVE : ##
>Help Angel Candysalt connect the dots in a game of connections.
#  

## PROCEDURE : ##
By reading through the instructions we know that this objective consists of a trivia game in which we need to group words that fall within the same sub-category.

### SILVER MEDAL ###

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
|__Internet Protocols:__|	IGMP	IPX	IP	ICMP
|__Security Protocols:__|	TLS	SSL	IPSec	SSH
|__Network Technologies:__|	Ethernet	PPP	IEEE 802.11	ARP
|__Application Layer Protocols:__|	HTTP	FTP	SMTP	DNS


