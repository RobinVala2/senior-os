import subprocess

subprocess.run(f'umount /dev/mapper/EncHome', shell=True)
subprocess.run(f'cryptsetup luksClose EncHome', shell=True)
