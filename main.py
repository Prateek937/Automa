import subprocess as sb

def docker_install():
	output = sb.getstatusoutput('rpm -q docker-ce')
	if output[0] == 1:
		if 'not installed' in output[1]:
			sb.call("echo 'Fetching Repository...'", shell=True)

			sb.call("echo 'y' | cp /root/dockercw123.repo /etc/yum.repos.d/", shell=True)
			
			sb.call("echo 'Downloading docker-ce, please wait ...'", shell=True)
			sb.call("echo 'Installing docker-ce...'", shell=True)
			
			outd = sb.getstatusoutput('yum install docker-ce --nobest -y')
			
			sb.call("echo 'Enabling container services...", shell=True)
			
			sb.call("systemctl enable docker", shell=True)
			
			if outd[0] == 0:
				listd = outd[1].split("\n")
				if listd[-1] == 'complete!':
					return 'Docker-ce successfully installed !'
				else:
					return 'Installation failed !', outd[1]
			else:
				return 'Installtion failed !', outd[1]	
	else:
		return 'Docker-ce already installed !'

def pull_docker_images(img_name):
	sb.call("docker pull {}".format(img_name), shell=True)

def show_docker_images():
	sb.call("docker images", shell=True)

def display_all_containers():
	sb.call("docker ps -a", shell=True)

def run_docker_container(os_name,version, title):
	sb.call("docker run -it --name {} {}:{}".format(title, os_name, version), shell=True)

def remove_all_containers():
	sb.call("docker rm `docker ps -a -q`", shell=True)

def remove_one_container(id):
	sb.call("docker rm id {}".format(id), shell=True)
	print("Successfully Removed {}".format(id))

out = docker_install()
print(out)
while True:
	choice = int(input('Enter choice: '))
	if choice == 1:
		img_name = input('Enter image name: ')
		pull_docker_images(img_name)
	if choice == 2:
		display_all_containers()
	if choice == 3:
		os_name = input('Enter os name: ')
		version = input('Enter os version :')
		title = input('Enter title name : ')
		run_docker_container(os_name,version,title)
	if choice == 4:
		show_docker_images()
	if choice == 5: 
		remove_one_container()
	if choice == 6:
		remove_all_containers()