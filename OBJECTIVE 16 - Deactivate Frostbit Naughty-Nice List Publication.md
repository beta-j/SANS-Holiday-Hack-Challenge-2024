# OBJECTIVE 16 - Deativate Frostbit Naughty-Nice List Publication #
Difficulty: ❄️❄️❄️❄️❄️

## OBJECTIVE : ##
>Wombley's ransomware server is threatening to publish the Naughty-Nice list. Find a way to deactivate the publication of the Naughty-Nice list by the ransomware server.

#

## HINTS: ##
<details>
  <summary>Hints provided for Objective 16</summary>
  
>-  There must be a way to deactivate the ransomware server's data publication. Perhaps one of the other North Pole assets revealed something that could help us find the deactivation path. If so, we might be able to trick the Frostbit infrastructure into revealing more details.
>-	The Frostbit author may have mitigated the use of certain characters, verbs, and simple authentication bypasses, leaving us blind in this case. Therefore, we might need to trick the application into responding differently based on our input and measure its response. If we know the underlying technology used for data storage, we can replicate it locally using Docker containers, allowing us to develop and test techniques and payloads with greater insight into how the application functions.


</details>

#  

## PROCEDURE : ##

The starting point for this objective is not explicitly provided, but it’s quite clearly [the API call we spotted in Santa Vision](OBJECTIVE%2013%20-%20Santa%20Vision.md#santa-vision-c); `api/v1/frostbitadmin/bot/<botuuid>/deactivate, authHeader: X-API-Key`

To call this API we can use `curl` with the following command:
```bash
curl -X GET "https://api.frostbit.app/api/v1/frostbitadmin/bot/a0870d85-09c6-440a-b878-f7cc8253bf24/deactivate " -H "X-API-Key:test_value
```
Alternatively you can use GUI applications such as [BURP suite](https://portswigger.net/burp) or [Postman](https://www.postman.com/) which was my preferred choice as I found it made it a lot quicker and easier to try multiple payloads and keep track of the results.

To start off with let’s try sending a test request with a `X-API-Key`  header value set to `test`  and we find that this returns an error: `{"error": "Invalid Request"}`, which isn’t very useful.  However, from the [previous objective](OBJECTIVE%2015%20-%20Decrypt%20the%20Naughty-Nice%20List.md) we learned of a server-side parameter which can be enabled to provide us with more detailed error information, so let’s try tacking on `?debug=true`  to the API call.  This time the error we get is slightly different: `{"error":"Invalid Key"}`  - so at least now we know that the we are constructing our API call correctly, it’s just that the API Key that we are providing is incorrect (of course).

Let’s try tinkering with this API call and see what happens… If we try to pass some special characters such as `;` `*` `/` `\` or `` ` `` we get a different error saying `{"error":"Request Blocked"}`  which tells us that these specific characters are being blocked by the application.  However, if we try passing a `'` character in our `X-API-Key`  header, we get a far more interesting response from the server:
```json
{

"debug": true,

"error": "Timeout or error in query:\nFOR doc IN config\n FILTER doc.<key_name_omitted> == '{user_supplied_x_api_key}'\n <other_query_lines_omitted>\n RETURN doc"

}
```
Now this is extremely interesting – first of all the server throwing this kind of error to an input of a `'` character immediately indicates that is likely vulnerable to some kind of injection.  Secondly, the error helpfully outputs part of the query that it is using to try and match our API Key input.

From the query we can tell that this is not written in SQL and that is most likely written in **AQL** – [ArangoDB Query Language](https://docs.arangodb.com/3.10/aql/), we can also see that there is a table called `config`  and that the application is trying to match our input with the contents of a particular key in that table.  By providing a `'` as our input, the query on the server is evaluated as:

```sql
FOR doc IN config FILTER doc.<key_name_omitted> == ‘’’
```

And this causes a timeout error because it is FALSE.  So, what can we add to our input to make it always return TRUE?  Of course, it’s the classic SQLI test string of ``‘OR 1==1``.  That’s all well and good, however it doesn’t really tell us anything more about the database or its contents.

At this stage I decided to try and figure out what verbs are being blocked by the application and which aren’t – so I gathered as many command verbs as I could find from the [AQL documentation](https://docs.arangodb.com/3.12/aql/) and put them in a script that tries to submit each one as the header value and records the server’s response. I also tried a bunch of special characters and recorded the response.  In the end I came up with the following (non-exhaustive) list:


| **Allowed Commands** |**Blocked Commands**  |
|:--:|:--:|
|`SEARCH`  `SORT`  `SLEEP`  `LIMIT`  `COLLECT`  `WINDOW`  `REPLACE`  `REMOVE`  `UPSERT`  `NOOPT`  `FAIL`  `CONCAT`  `LEFT`  `RIGHT`  `SUBSTRING`  `LENGTH` | `FOR`  `RETURN`  `FILTER`  `LET`  `INSERT`  `UPDATE`  `WITH`  `VALUES`   
|**Allowed Special Characters**| **Blocked Special Characters**
|`!` `"` `#` `$` `%` `&` `'` `(` `)` `+` `,` `-` `.` `:` `<` `=` `>` `?` `@`  `[` `]` `^` `_` `{`  `|`  `}` `~` `¬` `¦` | `;` `*` `/` `\` `` ` ``

This table helped me plan my strategy from here.  I knew right away it would be useless to try to get the application to execute another `FOR IN` search or to RETURN  some other value, furthermore, no matter what payloads I tried I always got the same AQL error or “invalid key” – so this was going to have to be a blind injection.

Blind injection techniques usually attempt to determine the effectiveness of a payload by measuring the difference in response time from the server.  A longer response time typically indicates that the payload is causing the server to do some processing and thus probably executing the commands we passed.  Luckily for us, we can see that AQL’s `SLEEP()`  function is not being blocked and we can use this to our advantage by passing a payload such as the following in our header:
```sql
' OR 1==1 ? SLEEP(2) :'
```
This payload makes use of the ternary operator (`?`) which essentially is equivalent to “_IF TRUE THEN_”, so with the above payload. The query will always evaluate to TRUE thanks to the `OR 1==1`  operation and when that evaluates to true it instructs the server to pause for two seconds before sending a response.  Sure enough, although we receive the same old error with this payload, we can observe a noticeable delay before we receive the response.  This means that the server is evaluating the query before the `?`  and executing the commands that come after it.

Things start to get very interesting from this point on.  We can use this vulnerability in the application to enumerate the `config`  table of the database.  We can use a payload such as `' OR LENGTH(doc)>1 ? SLEEP(2) : '`  to determine whether the table has more than one field in it.  If we observe a delay, it means that there _is_ more than one field.  We can play around with this until we arrive at `' OR LENGTH(doc)==4 ? SLEEP(2) : '` which tells us that the `config`  table has exactly four fields.

These field names are considered as _ATTRIBUTES_ of the `config` table in AQL and we can use a payload such as the following to test for the presence of system attributes in the `config` table:
```sql
' OR "_key" IN ATTRIBUTES(doc) ? SLEEP(2) : '
```
We can also use the following payload to determine how many non-system attributes are in `config`: 
```sql
' OR LENGTH(ATTRIBUTES(doc,true))==1 ? SLEEP(2) : '
```
Note that by adding `,true` to the `ATTRIBUTES` function we instruct AQL to only return **non-system** attributes.

Finally, by playing around with these payloads we can determine that the `config` table is composed of three system attributes and one user-defined attribute and these are stored in this order:
```json
config: {<undisclosed_name>, _rev, _key, _id}
```
These attributes can be addressed as you would normally address a matrix. So, for example, ``ATTRIBUTES(doc)[1]`` = ``_rev``.

At this point it would be really great if we could possibly find the name of the user-defined attribute as this is probably where the API key is being stored.  We can start by determining the number of characters in the name by playing a quick game of Hi/Lo with payloads such as this one:
```sql
' OR LENGTH(ATTRIBUTES(doc,true)[0]) >10 ? SLEEP(2) : '
```

With this method we can eventually determine that the user-defined attribute has a name that is 18 characters long.  Armed with this information we can use the `LEFT()` command to return the first leftmost x number of letters in the name and then use the `LIKE` command with wildcards to match that value against test characters until we find one that invokes a delay in the server.  For example,  ```' OR LEFT((ATTRIBUTES(doc)[1]),4) LIKE "%v" ? SLEEP(2) : '``` will cause a delay since the first four characters of ``ATRRIBUTES(doc)[1]`` are ``_rev`` and therefore match with `%v` (where `%` is considered by AQL as a wildcard that can match any string).  At this point I drafted [a python script](Code/blind_AQLI_Attribute_Name.py) with help from [ChatGPT](https://chatgpt.com/) that is composed of two nested loops, which submit a payload for each allowed character until it causes a server delay, then adds that character to the final value and moves to the next one.  This gave me the name of the user-defined attribute as **deactivate_api_key**.

![image](https://github.com/user-attachments/assets/c72b32f3-67bd-4879-960d-9216ce86db88)


Now we can use the same technique to determine the length of the string inside the field `deactivate_api_key` by using the `CHAR_LENGTH()` function:

```sql
' OR CHAR_LENGTH(doc.deactivate_api_key) ==36 ? SLEEP(2) : '
```

From this payload we learn that the API key we are trying to retrieve has 36 characters, so we can modify the outer loop of [the same python script we used earlier](Code/blind_AQLI_Attribute_Name.py) to loop 36 times and we change the payload to the following:

```python
payload  =  f"' OR LEFT(doc.deactivate_api_key,36) LIKE '{known_part  +  char}%' ? SLEEP(2) : '"
```
You can find the revised script [here](Code/blind_AQLI_Key_Value.py).

We can now simply run the script and wait for it to run through all the 36 characters and give us our API KEY: **abe7a6ad-715e-4e6a-901b-c9279a964f91**

Finally, we can submit our last API call with the retrieved API key in the header and we receive the following message confirmation:
```json
{

"message": "Response status code: 200, Response body: {\"result\":\"success\",\"rid\":\"a0870d85-09c6-440a-b878-f7cc8253bf24\",\"hash\":\"02af9465e7eae22fb250dea497ea045952c1f7e8be0f7ea86fdf7c7df2020eb4\",\"uid\":\"28388\"}\nPOSTED WIN RESULTS FOR RID a0870d85-09c6-440a-b878-f7cc8253bf24",

"status": "Deactivated"

}
```
We can also confirm that the ransomware has been deactivated by revisiting the ransom note page:

![image](https://github.com/user-attachments/assets/1d0f658e-d18a-413c-910a-e3ad499b7fa1)




 #
[<<< Previous Objective (15 - Decrypt the Naughty-Nice List)](OBJECTIVE%2015%20-%20Decrypt%20the%20Naughty-Nice%20List.md)|.........................................................|[Next Objective (BONUS OBJECTIVE - Hidden Story) >>>](_BONUS%20OBJECTIVE%20-%20Hidden%20Story.md) |
:-|--|-:
