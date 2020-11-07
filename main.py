import subprocess as sb

def hadoop():
    out = sb.getstatusoutput("echo 'Y' | hadoop namenode -format")
    print(out[0])
    out2 = sb.getstatusoutput("rpm -q httpd")
    print(out[0])

hadoop()
