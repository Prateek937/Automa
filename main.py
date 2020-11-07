import subprocess as sb

def docker_install():
	output = sb.getstatusoutput('rpm -q docker')
	if output[0] == 0:
		if output == 'package docker is not installed':
			sb.getstatusoutput('wget https://download.docker.com/linux/centos/7/x86_64/stable/')
			outd = sb.getstatusoutput('yum install docker-ce --nobest')
			if outd[0] == 0:
				listd = outd[1].split("\n")
				if listd[-1] == 'complete':
					return 'Docker-ce successfully installed !'
				else:
					return 'Not installed !', outd[1]
		else:
			return 'Docker-ce already installed !'

out = list(docker_install())
for x in out:
	print(x)