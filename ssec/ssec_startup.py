import subprocess

file_path = /ssec/ssec_crypt.txt

with open(file_path, 'r') as file:
	first_line = file.readline()
	if first_line == 'Decrypted':
		subprocess.run(f'touch funguje_d.txt')
	else:
		subprocess.run(f'touch funguje_e.txt')
