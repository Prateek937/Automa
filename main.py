import subprocess as sb

def file_handeling(file_path, ip, namenode):
	file = open("{}".format(file_path), 'r')
	string_list = file.readlines()
	file.close()

	index_initial = string_list.index('<configuration>\n')
	index_final = string_list.index('</configuration>\n')

	del string_list[index_initial+1:index_final]
	if file_path == '/etc/hadoop/hdfs-site.xml':
		string_list.insert(index_initial + 1, "<property>\n")
		if namenode == True:
			string_list.insert(index_initial + 2, "<name>dfs.name.dir</name>\n")
		else:
			string_list.insert(index_initial + 2, "<name>dfs.data.dir</name>\n")
		string_list.insert(index_initial + 3, "<value>/nn</value>\n")
		string_list.insert(index_initial + 4, "</property>\n")
	elif file_path == '/etc/hadoop/core-site.xml':
		string_list.insert(index_initial + 1, "<property>\n")
		string_list.insert(index_initial + 2, "<name>fs.default.name</name>\n")
		string_list.insert(index_initial + 3, "<value>hdfs://{}:9001</value>\n".format(ip))
		string_list.insert(index_initial + 4, "</property>\n")
	else: sb.call('echo "configuration file not found"', shell=True)

	file = open("{}".format(file_path), "w")
	new_file_content = "".join(string_list)
	file.write(new_file_content)
	file.close()

def configure_namenode_hadoop(Type):
	if Type == 1:
		ip = '0.0.0.0'
	else:
		ip = input('Enter the ip of namenode : ')
	sb.call("echo 'Configuring hdfs-site.xml file...'", shell=True)
	file_handeling('/etc/hadoop/hdfs-site.xml', '0.0.0.0', True)
	sb.call("echo 'ConfiguredConfigured hdfs-site.xml file...'", shell=True)
	sb.call("echo 'Configuring core-site.xml file...'", shell=True)

	file_handeling('/etc/hadoop/core-site.xml', ip, True)
	sb.call("echo 'Configured core-site.xml file...'", shell=True)
	sb.call("echo 'Formatting Namenode...'", shell=True)
	out = sb.getstatusoutput("echo 'Y' | hadoop namenode -format")
	if out[0] == 0:
		sb.call("echo 'Namenode successfully fomatted !'", shell=True)
	else: print('Something went Wrong !')
	sb.call("echo 'Starting Namenode...'", shell=True)
	sb.call("echo 3 > /proc/sys/vm/drop_caches", shell=True)
	out = sb.getstatusoutput("hadoop-daemon.sh start namenode")
	
	if 'running' in out[1]:
		sb.call("hadoop-daemon.sh stop namenode",shell=True)
		out = sb.getstatusoutput("hadoop-daemon.sh start namenode")
	elif out[0] == 0:
		sb.call("echo 'Namenode started successfully !'", shell=True)
	else:
		print('Something went Wrong !')
		print(out[1])

def configure_datanodes_hadoop(Type):
	ippp = input('Enter the ip of namenode : ')
	if Type == 1:
		file = open('/home/ec2-user/Automa/ip.txt', 'w')
		file.write(ippp)
		file.close()
	ips = list(input('Enter IPs of Datanodes separated by space : ').split(" "))
	Type = input('Type of Datanode AWS Instance(1)/local(2): ')
	for ip in ips:

		if type == 1:
			sb.call('ssh -i -o StrictHostKeyChecking=No /home/ec2-user/Automa/aws2.pem ec2-user@{} "sudo python3 datanode.py"'.format(ip), shell=True)
		else:
			sb.call('ssh root@{} "sudo python3 datanode.py"'.format(ip), shell=True)
def configure_cluster():
	configure_namenode_hadoop(1)
	configure_datanodes_hadoop(1)
	sb.call("hadoop dfsadmin -report", shell=True)

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

while True:
	print("""1.pull_docker_images
			2.display_all_containers
			3.run_docker_container
			4. show_docker_images
			5. remove_one_container
			6. remove_all_containers
			7. configure_namenode_hadoop
			8. configure_datanode_hadoop
			9. configure_cluster""")
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
	if choice == 7:
		configure_namenode_hadoop(1)
	if choice == 8:
		configure_datanodes_hadoop(1)
	if choice == 9:
		configure_cluster()
