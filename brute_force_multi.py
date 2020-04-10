import multiprocessing as mp
import gnupg


def divide_list(wordlist, num_to_split):
	if num_to_split > mp.cpu_count():
		print("Changing to {} as a default".format(mp.cpu_count()))
		num_to_split = mp.cpu_count()
	num_to_split = 4
	splitted_wordlist = None
	try:
		with open(wordlist, 'rb') as words:
			wd = words.read().splitlines()
			for n_line, line in enumerate(wd):
				if n_line % num_to_split == 0:
					if splitted_wordlist:
						splitted_wordlist.close()
					n_splitted = "rockyou_{}.txt".format(n_line+num_to_split)
					splitted_wordlist = open(n_splitted, "wb")
				splitted_wordlist.write(str(line))
			if splitted_wordlist:
				splitted_wordlist.close()
	except OverflowError as error:
		print(error)
	except Exception as exception:
		print(exception)

def decrypt_gpg(gpg_file):
	gpg = gnupg.GPG()
	with open(gpg_file, 'rb') as f:
		decrypted_file = gpg.decrypt_file(f, passphrase=password_attempt)
		if decrypted_file.ok:
			print('status: ', decrypted_file.status)
			print('stderr: ', decrypted_file.stderr)

def brute_force_simple(wordlist, gpg_file):
	with open(wordlist, 'rb') as words:
		pwd_list = words.read().splitlines()
		for pwd in pwd_list:
			try:
				decrypt_gpg(gpg_file)
			except Exception as e:
				print("Exception: ", e)

if __name__ == "__main__":
	
	print("There're {} cores available on machine".format(mp.cpu_count())
	cpu_cores = input(int("How many cores do you want to use?"))
	if cpu_cores > mp.cpu_count():
		print("setting up to maximum")
