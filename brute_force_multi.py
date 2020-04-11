import os
import sys
import time

from multiprocessing import Semaphore
import multiprocessing as mp
import gnupg


#def worker(input, output):
#	for func, args in iter(input.get, 'STOP'):
#		result = calculate(func, args)
#		print(result)
#	sema.release()
#
#def calculate(func, args):
#    result = func(*args)
#    return '%s says that %s%s = %s' % \
#       (mp.current_process().name, func.__name__, args, result)

def chunkfy_list(wordlist):
	try:
		with open(wordlist, 'rb') as words:
			wd = words.read().splitlines()
			size_wd = len(wd)
			chunks = [wd[line:line+10000] for line in range(0, size_wd, 10000)]

	except OverflowError as error:
		print("OverFlow: ", error)
	except Exception as exception:
		print("Exception in divided: ", exception)
	return chunks

def brute_force_simple(name, wordlist, sema):
	sema.acquire()
	print("Process {} running".format(name))
	target = 'lab1.gpg' # edit to your GPG file
	gpg = gnupg.GPG()
	time_count = time.time()
	for pwd in wordlist:
		try:
			decrypted_file = gpg.decrypt_file(target, passphrase=pwd)
			if decrypted_file.ok:
				print('status: ', decrypted_file.status)
				print('stderr: ', decrypted_file.stderr)
				print("PASSWORD: ", pwd)
				sema.release()
		except Exception as e:
			print("Exception: ", e)
	print("not yet {}".format(time.time() - time_count))
	sema.release()

if __name__ == "__main__":
	# Setting up numbers of cores to use
	#print("There're {} cores available on machine".format(mp.cpu_count()))
	#cpu_cores = int(input("How many cores do you want to use?\n"))
	#if cpu_cores > mp.cpu_count() and cpu_cores <= 0:
	#	print("setting up to maximum")
	#	cpu_cores = mp.cpu_count()
	#TODO: argparse for any wordlist and gpg file
	# Not a good way if you don't want to freeze your computer
	# wordlists = [wd for wd in os.listdir('.') if os.path.isfile(wd) if wd.endswith("_*.txt")]
	print("Attack Initiated!")	
	start = time.time()
	resourses = chunkfy_list('rockyou.txt') # edit to your wordlist
	print("wordlist chunkfied, elapsed time: ", time.time() - start)
	print("Setting up concurrency at 1% of all tasks")
	print("Setting up tasks")
	concurrency = int(len(resourses) * 0.01)
	num_tasks = len(resourses)
	sema = Semaphore(concurrency)

	# Start
	processes = list()
	for i, r in enumerate(resourses):
		process = mp.Process(target=brute_force_simple, args=(i, r, sema))
		processes.append(process)
		process.start()

	# Finish
	for p in processes:
		p.join()

	print("Elapsed time: ", time.time() - start)
	end = time.time() - start
	print("End of process, time elapsed: {}".format(end))
