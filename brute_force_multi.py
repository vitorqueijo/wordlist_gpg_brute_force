import os
import sys
import time

from multiprocessing import Semaphore
import psutil
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

def limit_cpu_usage():
	pid = psutil.Process(os.getpid())
	pid.nice(19)

def chunkfy_list(wordlist):
	try:
		with open(wordlist, 'rb') as words:
			wd = words.read().splitlines()
			print("Tamanho da wd: ", len(wd))
			size_wd = len(wd)
			chunks = [wd[line:line+18000] for line in range(0, size_wd, 18000)]

	except OverflowError as error:
		print("OverFlow: ", error)
	except Exception as exception:
		print("Exception in divided: ", exception)
	return chunks

def gpg_attempt(gpg, wordlist, name):
	start = time.time()
	print("gpg attempt: ", name)
	for i, pwd in enumerate(wordlist):
		attemp = gpg.decrypt_file('', passphrase=str(pwd))
		if attemp.ok:
			print('status: ', attemp.status)
			print('stderr: ', attemp.stderr)
			print("PASSWORD: ", pwd)
	print("time elapsed for {}: \t".format(name) + str(start - time.time()))

def brute_force_simple(gpg, name, wordlist, sema):
	sema.acquire()
	# print("Process {} running".format(name))
	try:
		gpg_attempt(gpg, wordlist, name)
	except Exception as e:
		print("Exception: ", e)
	print("not yet {} just ended".format(name))
	sema.release()

if __name__ == "__main__":
	print("Attack Initiated!")	
	start = time.time()
	resourses = chunkfy_list('') # edit to your wordlist
	print("wordlist chunkfied, elapsed time: ", time.time() - start)
	print("Setting up concurrency at 2")
	print("Setting up tasks")
	concurrency = 2
	num_tasks = len(resourses)
	sema = Semaphore(concurrency)
	print("Number of processes: ", num_tasks)
	time.sleep(5)		
	gpg = gnupg.GPG()
	# Start
	processes = list()
	for i, r in enumerate(resourses):
		process = mp.Process(target=brute_force_simple, args=(gpg, i, r, sema))
		processes.append(process)
		process.start()

	# Finish
	for p in processes:
		p.join()

	print("Elapsed time: ", time.time() - start)
	end = time.time() - start
	print("End of process, time elapsed: {}".format(end))
