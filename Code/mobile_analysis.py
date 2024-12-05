"""Database Decrypt - AES-GCM
#created by OpenAI ChatGPT

"""OpenAI ChatGPT Prompts Used:
-	I have a number of encoded strings such as this one: ""L2nc3+01t5wzVN92dNMR5wdr0Z9XAJhDurK0PoMIwB3/YInPpneEf/Q3blsrDg==" and I need to decode them.  To decode them, I first need to base64 decode the string and then decrypt with AES GCM using the following IV and Encryption Key (both are base64 encoded):  IV: Q2hlY2tNYXRlcml4  and Encryption Key: rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw=  Ideally I should either use a cyberchef recipe for this or a python script
-	I get the following error in python: ValueError: Authentication tag must be provided when decrypting. 
"""


import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

# Inputs
encoded_string = "KGfb0vd4u/4EWMN0bp035hRjjpMiL4NQurjgHIQHNaRaDnIYbKQ9JusGaa1aAkGEVV8="
iv_base64 = "Q2hlY2tNYXRlcml4"
key_base64 = "rmDJ1wJ7ZtKy3lkLs6X9bZ2Jvpt6jL6YWiDsXtgjkXw="

# Decode the IV and Encryption Key
iv = base64.b64decode(iv_base64)
key = base64.b64decode(key_base64)

# Decode the Base64 encoded ciphertext
ciphertext_with_tag = base64.b64decode(encoded_string)

# Split the ciphertext and tag (AES GCM requires the tag)
# Assuming the last 16 bytes are the tag (standard length for AES GCM)
ciphertext, tag = ciphertext_with_tag[:-16], ciphertext_with_tag[-16:]

# Decrypt using AES GCM
cipher = Cipher(algorithms.AES(key), modes.GCM(iv, tag), backend=default_backend())
decryptor = cipher.decryptor()
plaintext = decryptor.update(ciphertext) + decryptor.finalize()

# Print the result
print("Decoded String:", plaintext.decode("utf-8"))
