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

def configure_datanode(ip):
        sb.call("echo 'Configuring hdfs-site.xml file...'", shell=True)
        file_handeling('/etc/hadoop/hdfs-site.xml', '0.0.0.0', False)
        sb.call("echo 'Configured hdfs-site.xml file...'", shell=True)
        sb.call("echo 'Configuring core-site.xml file...'", shell=True)
        file_handeling('/etc/hadoop/core-site.xml', ip, False)
        sb.call("echo 'Configured core-site.xml file...'", shell=True)
        sb.call("echo 'Starting Datanode...'", shell=True)
        sb.call("echo 3 > /proc/sys/vm/drop_caches", shell=True)
        out = sb.getstatusoutput("hadoop-daemon.sh start datanode")
        if 'running' in out[1]:
            sb.getstatusoutput("hadoop-daemon.sh stop datanode")
            out = sb.getstatusoutput("hadoop-daemon.sh start datanode")
        if out[0] == 0:
            print("Successfully started Datanode...")
        else:
            print('Something went Wrong !')
            print(out[1])




try:
    file = open("/home/ec2-user/Automa/ip.txt", 'r')
except:
    print("trying exception")
ip = '65.0.179.192'
configure_datanode(ip)