# OBJECTIVE 4 - cURLing #

## OBJECTIVE : ##
>Team up with Bow Ninecandle to send web requests from the command line using Curl, learning how to interact directly with web servers and retrieve information like a pro!
#  

## HINTS: ##
<details>
  <summary>Hints provided for Objective 2</summary>
  
>-	The official [cURL man page](https://curl.se/docs/manpage.html) has tons of useful information on how to use cURL.
>-	Take a look at cURL’s “—path-as-is” option; it controls a default behaviour that you may not expect!
</details>

#  

## PROCEDURE : ##
### SILVER MEDAL ###

For a Silver Medal all you need to do is follow the instructions that pop up on the terminal screen.  Whenever you’re stuck just type in hint or refer to the cURL man page and it should be straightforward to complete.  You can also just copy the commands shown here:

```console
1) Unlike the defined standards of a curling sheet, embedded devices often have web servers on non-standard ports.  Use curl to retrieve the web page on host "curlingfun" port 8080.
alabaster@curlingfun:~$ curl curlingfun:8080
You have successfully accessed the site on port 8080!

2) Embedded devices often use self-signed certificates, where your browser will not trust the certificate presented.  Use curl to retrieve the TLS-protected web page at https://curlingfun:9090/
alabaster@curlingfun:~$ curl https://curlingfun:9090 --insecure
You have successfully bypassed the self-signed certificate warning!
Subsequent requests will continue to require "--insecure", or "-k" for short.

3) Working with APIs and embedded devices often requires making HTTP POST requests. Use curl to send a request to https://curlingfun:9090/ with the parameter "skip" set to the value "alabaster", declaring Alabaster as the team captain.
alabaster@curlingfun:~$ curl -d "skip=alabaster" https://curlingfun:9090 -k
You have successfully made a POST request!

4) Working with APIs and embedded devices often requires maintaining session state by passing a cookie.  Use curl to send a request to https://curlingfun:9090/ with a cookie called "end" with the value "3", indicating we're on the third end of the curling match.
alabaster@curlingfun:~$ curl --cookie "end=3" https://curlingfun:9090 -k
You have successfully set a cookie!

5) Working with APIs and embedded devices sometimes requires working with raw HTTP headers.  Use curl to view the HTTP headers returned by a request to https://curlingfun:9090/
alabaster@curlingfun:~$ curl https://curlingfun:9090 -k -v
* Server certificate:
*  subject: C=US; ST=Some-State; O=Internet Widgits Pty Ltd; CN=localhost
*  start date: Feb  7 16:23:39 2024 GMT

...

< Connection: keep-alive
< Custom-Header: You have found the custom header!
< 
You have successfully bypassed the self-signed certificate warning!
Subsequent requests will continue to require "--insecure", or "-k" for short.


6) Working with APIs and embedded devices sometimes requires working with custom HTTP headers.  Use curl to send a request to https://curlingfun:9090/ with an HTTP header called "Stone" and the value "Granite".
alabaster@curlingfun:~$ curl https://curlingfun:9090 -k -H "Stone:Granite"
You have successfully set a custom HTTP header!

7) curl will modify your URL unless you tell it not to.  For example, use curl to retrieve the following URL containing special characters: https://curlingfun:9090/../../etc/hacks
alabaster@curlingfun:~$ curl https://curlingfun:9090/../../etc/hacks -k --path-as-is
You have successfully utilized --path-as-is to send a raw path!
```
