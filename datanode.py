from main.py import file_handeling

def configure_datanode(ip):
	sb.call("echo 'Configuring hdfs-site.xml file...'", shell=True)
	file_handeling('/etc/hadoop/hdfs-site.xml', '0.0.0.0', False)
	sb.call("echo 'Configured hdfs-site.xml file...'", shell=True)
	sb.call("echo 'Configuring core-site.xml file...'", shell=True)
	file_handeling('/etc/hadoop/core-site.xml', ip, False)
	sb.call("echo 'Configured core-site.xml file...'", shell=True)
	sb.call("echo 'Starting Datanode '{}'...'".format(ip), shell=True)
	sb.call("echo 3 > /proc/sys/vm/drop_caches", shell=True)
	out = sb.getstatusoutput("hadoop-daemon.sh start datanode")
	if out[0] == 0:
		sb.call("echo 'Datanode {} started successfully !'".format(ip), shell=True)
	else:
		print('Something went Wrong !')
		print(out[1])


try:
	file = open("/home/ec2-user/ip.txt", 'r')
except:
	print("trying exception")
	file = open("/root/Automa/ip.txt", 'r')

ip = file.read()
configure_datanode(ip)