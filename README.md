# Etherscan-Transaction
This repository demonstrates how you can use webscrapping to fetch transaction details on Ethereum blockchain using Etherscan.com  
This script has a function that takes the transaction ID and gets the details of that transaction as dictionary.

# How to use
Get requests   
`pip install requests`   

Get BeautifulSoup   
`pip install beautifulsoup4`   

Store etherfetch.py in your current working directory and import etherfetch in your project   
`import etherfetch`      

Call the function info() with transaction ID   
`result = info(tx)`   
Here tx is transaction Hash   
