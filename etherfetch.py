import requests
import re
from bs4 import BeautifulSoup
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
block_re = re.compile('/block/(\d+)')
timestamp_re = re.compile('<i class=\'far fa-clock small mr-1\'></i>(.*?)\n</div>')
from_re = re.compile('<span id=\'spanFromAdd\' style=\'display:none;\'>(.*?)</span>')
to_re = re.compile('<a id=\'contractCopy\' href=\'/address/(.*?)\'')

def info(tx):
	url = 'https://etherscan.io/tx/' + str(tx)
	r = requests.get(url, headers=headers)
	if r.status_code != 200:
		return int(r.status_code)
	data = {'txhash':tx,
			'status':None,
			'block':None,
			'timestamp':None,
			'from':None,
			'to':None,
			'to_readable':None,
			'action':None,
			'value':None,
			'txfee':None,
			'maxfee':None,
			'gaslimit':None,
			'gasprice':None,
			'nonce':None,
			}
	# block number 
	block_result = block_re.findall(r.text)
	if(len(block_result) > 0):
		data['block'] = block_result[0]
	else:
		data['block'] = 'Pending'
	# timestamp 
	timestamp_result = timestamp_re.findall(r.text)
	if(len(timestamp_result) > 0):
		data['timestamp'] = timestamp_result[0]
	else:
		data['timestamp'] = 'Unconfirmed'
	# from
	from_result = from_re.findall(r.text)
	if(len(from_result) > 0):
		data['from'] = from_result[0]
	else:
		data['from'] = 'Not found'
	# to 
	to_result = to_re.findall(r.text)
	if(len(to_result) > 0):
		data['to'] = to_result[0]
	else:
		data['to'] = 'Not found'
	# to readable 
	toreadable_re = re.compile(data['to'] + '</span> <span class=\'mr-1\'>(.*?)</span>')
	toreadableresult = toreadable_re.findall(r.text)
	if(len(toreadableresult) > 0):
		data['to_readable'] = toreadableresult[0]
	else:
		data['to_readable'] = 'Not readable'
	# action, value, fee, price, limit, nonce
	data['action'] = '---'
	soup = BeautifulSoup(r.text, 'html.parser')
	all_divs = soup.find_all('div', attrs = {'class':'row'}) # all divs with class row
	for div in all_divs:
		# status 
		if 'Status:' in div.text:
			if 'Success' in div.text:
				data['status'] = 'Success'
			elif 'Fail' in div.text:
				data['status'] = 'Failure'
			elif 'Pending' in div.text:
				data['status'] = 'Pending'
			else:
				data['status'] = 'Unknown'
		# action 
		if 'Transaction Action:' in div.text:
			sub_div = div.find_all("div", attrs = {'class':'media-body'})
			if len(sub_div) > 0:
				sub_div = sub_div[0]
				transaction_action = ''
				for element in sub_div.contents:
					if len(element.text) > 0:
						transaction_action = transaction_action + ' ' + element.text
				data['action'] = transaction_action 
		# value 
		if 'Value:' in div.text:
			value_result = div.find_all(id="ContentPlaceHolder1_spanValue")
			if len(value_result) > 0:
				data['value'] = value_result[0].text
			else:
				data['value'] = 'Not found'
		# transaction fee 
		if 'Transaction Fee:' in div.text:
			fee_result = div.find_all(id='ContentPlaceHolder1_spanTxFee')
			if len(fee_result) > 0:
				data['txfee'] = fee_result[0].text
			else:
				data['txfee'] = 'Not found'
		# maximum transaction fee 
		if 'Max Txn Cost/Fee:' in div.text:
			fee_result = div.find_all(id='ContentPlaceHolder1_spanTxFee')
			if len(fee_result) > 0:
				data['maxfee'] = fee_result[0].text
			else:
				data['maxfee'] = 'Not found'
		# gas limit
		if 'Gas Limit:' in div.text:
			limit_result = div.find_all(id='ContentPlaceHolder1_spanGasLimit')
			if len(limit_result) > 0:
				data['gaslimit'] = limit_result[0].text
			else:
				data['gaslimit'] = 'Not found'
		# gas price 
		if 'Gas Price:' in div.text:
			price_result = div.find_all(id='ContentPlaceHolder1_spanGasPrice')
			if len(price_result) > 0:
				data['gasprice'] = price_result[0].text
			else:
				data['gasprice'] = 'Not found'
		# Nonce 
		if 'Nonce' in div.text:
			nonce_result = div.find_all(attrs={'title':'Transaction Nonce'})
			if len(nonce_result) > 0:
				data['nonce'] = nonce_result[0].text
			else:
				if 'Pending' in div.text:
					data['nonce'] = 'Pending'
				else:
					data['nonce'] = 'Not found'
	return data