# OBJECTIVE 7 - Hardware Hacking 101 (Part 2) #

## OBJECTIVE : ##
>Santa’s gone missing, and the only way to track him is by accessing the Wish List in his chest—modify the access cards database to gain entry!

#
## HINTS: ##
<details>
  <summary>Hints provided for Objective 7</summary>
>-	It is so important to keep sensitive data like passwords secure. Often times, when typing passwords into a CLI (Command Line Interface) they get added to log files and other easy to access locations. It makes it trivial to step back in history and identify the password.
>-	I seem to remember there being a handy HMAC generator included in [CyberChef](https://gchq.github.io/CyberChef/).

</details>

#  

## PROCEDURE : ##
### SILVER MEDAL ###

One of the hints comes very close to giving this objective away with it’s reference to ‘*step[ping] back in history*’.

At the terminal we choose the first option “Startup System (Default)” and we are presented with the SLH Tool terminal.  Just hit the up arrow key to see the last commands entered at the prompt.  Keep pressing up until you see a line that contains a password:
```console
slh@slhconsole\> slh –passcode CandyCaneCrunch77 –set-access 1 –id 143
```

All we need to do is modify the `–id` switch to `42` instead of `143`:

![image](https://github.com/user-attachments/assets/ea4f895b-e02a-4779-aa06-a33f5a75f653)

### GOLD MEDAL ###
To obtain the gold medal, Jewel Loggins tells us that we need to find a way of changing the access for card No. 42 by directly manipulating the database rather than using the SLH tool.  He also mentions that we will need to generate our own HMAC to do this successfully.

In the terminal prompt we can see that there is a single file called `access_cards` and that it is a SQLite 3.x database:
```console
slh@slhconsole\> ls
access_cards
slh@slhconsole\> file access_cards 
access_cards: SQLite 3.x database, last written using SQLite version 3040001, file counter 4, database pages 32, cookie 0x2, schema 4, UTF-8, version-valid-for 4
```

This means we can access the database directly using sqlite3.
```console
slh@slhconsole\> sqlite3 access_cards 
SQLite version 3.40.1 2022-12-28 14:03:47
Enter ".help" for usage hints.
```

Next, we can look at the schema for access_cards to see what column names are in the table:
```sql
sqlite> .schema access_cards    
CREATE TABLE access_cards (
            id INTEGER PRIMARY KEY,
            uuid TEXT,
            access INTEGER,
            sig TEXT
```

We now know that each entry in the table has four values; `id`, `uuid`, `access` and `sig`.  `id` contains the card number, `uuid` contains the actual card UUID, `access` contains a `0` or `1` value depending on whether access is granted for that card or not and `sig` contains the HMAC hash for that table entry.

We can now look at the entry for card `42` specifically with `SELECT * FROM access_cards where id = 42;`

```sql
sqlite> SELECT * FROM access_cards WHERE id=42;
42|c06018b6-5e80-4395-ab71-ae5124560189|0|ecb9de15a057305e5887502d46d434c9394f5ed7ef1a51d2930ad786b02f6ffd
```

We can also update the database entry to change the value for `access` from `0` to `1`:
```sql
sqlite> UPDATE access_cards SET access=1 WHERE id = 42;
```
But this is not enough, since the HMAC value stored in the `sig` column no longer corresponds to the entry for card no. 42.  We need to find a way to generate our own HMAC.  We already know we can use Cyberchef for this part (thanks to the hints), but generating a HMAC requires us to know the exact formatting of the inputted data to be hashed and the key used for HMAC hashing.

We can see that our database has another table apart from `access_cards` and it is called `config`…which makes it sound interesting enough for us to have a look inside it:
```sql
sqlite> .tables
access_cards  config      
sqlite> SELECT * FROM config;
1|hmac_secret|9ed1515819dec61fd361d5fdabb57f41ecce1a5fe1fe263b98c0d6943b9b232e
2|hmac_message_format|{access}{uuid}
3|admin_password|3a40ae3f3fd57b2a4513cca783609589dbe51ce5e69739a33141c5717c20c9c1
4|app_version|1.0
```

This is just what we were looking for.  The first entry in the config table gives us the HMAC key that we should use and the second entry gives us the correct message format.  
So, all that we need to do now is prepend the UUID for card 42 with a `1` and paste it into Cyberchef in the Input field.  Paste the value of `hmac_secret` into the **Key** field and click on **BAKE**!

![image](https://github.com/user-attachments/assets/92321330-6a08-4544-9750-ba3d85e07a3c)

We now have our freshly-baked HMAC value for card no. 42 with an access value of `1`.  All that remains is for us to update the datatbase with this new value:

```sql
sqlite> UPDATE access_cards SET sig='135a32d5026c5628b1753e6c67015c0f04e26051ef7391c2552de2816b1b7096' WHERE id=42;
sqlite> 
       *   *   *   *   *   *   *   *   *   *   *
   *                                             *
*      ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄  ❄     *
 *  $$$$$$\   $$$$$$\   $$$$$$\  $$$$$$$$\  $$$$$$\   $$$$$$\  * 
  * $$  __$$\ $$  __$$\ $$  __$$\ $$  _____|$$  __$$\ $$  __$$\ *
   *$$ /  $$ |$$ /  \__|$$ /  \__|$$ |      $$ /  \__|$$ /  \__| *
    $$$$$$$$ |$$ |      $$ |      $$$$$\    \$$$$$$\  \$$$$$$\   
   *$$  __$$ |$$ |      $$ |      $$  __|    \____$$\  \____$$\  *
  * $$ |  $$ |$$ |  $$\ $$ |  $$\ $$ |      $$\   $$ |$$\   $$ | *
*   $$ |  $$ |\$$$$$$  |\$$$$$$  |$$$$$$$$\ \$$$$$$  |\$$$$$$  |   *
 *  \__|  \__| \______/  \______/ \________| \______/  \______/  *
*         *    ❄             ❄           *        ❄    ❄    ❄   *
   *        *     *     *      *     *      *    *      *      *
   *  $$$$$$\  $$$$$$$\   $$$$$$\  $$\   $$\ $$$$$$$$\ $$$$$$$$\ $$$$$$$\  $$\  *
   * $$  __$$\ $$  __$$\ $$  __$$\ $$$\  $$ |\__$$  __|$$  _____|$$  __$$\ $$ | *
  *  $$ /  \__|$$ |  $$ |$$ /  $$ |$$$$\ $$ |   $$ |   $$ |      $$ |  $$ |$$ |*
  *  $$ |$$$$\ $$$$$$$  |$$$$$$$$ |$$ $$\$$ |   $$ |   $$$$$\    $$ |  $$ |$$ | *
 *   $$ |\_$$ |$$  __$$< $$  __$$ |$$ \$$$$ |   $$ |   $$  __|   $$ |  $$ |\__|*
  *  $$ |  $$ |$$ |  $$ |$$ |  $$ |$$ |\$$$ |   $$ |   $$ |      $$ |  $$ |   *
*    \$$$$$$  |$$ |  $$ |$$ |  $$ |$$ | \$$ |   $$ |   $$$$$$$$\ $$$$$$$  |$$\ *
 *    \______/ \__|  \__|\__|  \__|\__|  \__|   \__|   \________|\_______/ \__|  *
  *                                                            ❄    ❄    ❄   *
   *      *    *    *    *    *    *    *    *    *    *    *    *    *    *    
```

