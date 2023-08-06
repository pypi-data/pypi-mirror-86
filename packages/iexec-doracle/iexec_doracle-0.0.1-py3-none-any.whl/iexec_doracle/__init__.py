import eth_abi
import json
import os

def submitCallback(data=[], types=[], path=os.environ.setdefault('IEXEC_OUT', ''), log=None):
	callback = '0x{}'.format(eth_abi.encode_abi([*types], [*data]).hex())
	if log: log('[Offchain Computing for Smart-Contracts]')
	if log: log('> data:     {}'.format(data))
	if log: log('> types:    {}'.format(types))
	if log: log('> callback: {}'.format(callback))

	output = '{path}/{filename}'.format(path=path, filename='computed.json')
	with open(output, 'w+') as f:
		json.dump({ 'callback-data' : callback}, f)
