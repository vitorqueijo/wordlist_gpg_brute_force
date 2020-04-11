import os
import sys
import time

import multiprocessing as mp
from itertools import product
from contextlib import contextmanager
import gnupg


def divide_list(wordlist, num_to_split):
	if num_to_split > mp.cpu_count():
		print("Changing to {} as a default".format(mp.cpu_count()))
		num_to_split = mp.cpu_count()
	num_to_split = 4
	splitted_wordlists = list()
	n_wordlist = list()
	try:
		with open(wordlist, 'rb') as words:
			wd = words.read().splitlines()
			for n_line, line in enumerate(wd):
				n_wordlist.append(line)
				if n_line % num_to_split == 0:
					splitted_wordlists.append([splitted_wordlists])
					n_wordlist = list()

	except OverflowError as error:
		print(error)
	except Exception as exception:
		print(exception)
	return splitted_wordlists

def brute_force_simple(wordlist):
	gpg = gnupg.GPG()
	for pwd in wordlist:
		try:
			with open('lab1.gpg', 'rb') as f:
				decrypted_file = gpg.decrypt_file(f, 
							passphrase=pwd)
				if decrypted_file.ok:
					print('status: ', decrypted_file.status)
					print('stderr: ', decrypted_file.stderr)
					return pwd
		except Exception as e:
			print("Exception: ", e)


def brute_force_simple_unpack(args):
	return brute_force_simple(*args)

@contextmanager
def poolcontext(*args, **kwargs):
    pool = mp.Pool(*args, **kwargs)
    yield pool
    pool.terminate()

if __name__ == "__main__":
	# Setting up numbers of cores to use
	print("There're {} cores available on machine".format(mp.cpu_count()))
	cpu_cores = int(input("How many cores do you want to use?"))
	if cpu_cores > mp.cpu_count() and cpu_cores <= 0:
		print("setting up to maximum")
		cpu_cores = mp.cpu_count()
	#TODO: argparse for any wordlist and gpg file
	target = '' # edit to your GPG file
	# Not a good way if you don't want to freeze your computer
	# wordlists = [wd for wd in os.listdir('.') if os.path.isfile(wd) if wd.endswith("_*.txt")]
	wordlists = divide_list('', cpu_cores) # edit to your wordlist
	start = time.time()
	# Source: https://stackoverflow.com/questions/5442910/python-multiprocessing-pool-map-for-multiple-arguments
	# Starting workers
	print("Starting workers", time.time() - start)
	with poolcontext(processes=cpu_cores) as pool:
		result_imap = pool.imap(brute_force_simple_unpack, product(wordlists, repeat=1))
	for i in result_imap:
		print("\nResults: ", i)
	end = time.time() - start
	print("End of process, time elapsed: {}".format(end))
