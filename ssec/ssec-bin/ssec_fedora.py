import subprocess

password = 'komosny1'

subprocess.run(f'cloop=$(losetup -f --show $HOMEPATH')
subprocess.run(f'echo "{password}" | while ! cryptsetup luksOpen $cloop EncHomeFoo; do :; done;', shell=True)