import subprocess as sb

out = sb.getstatusoutput("rpm -q git")
if out[0] == 1:
        if 'not installed' in out[1]:
                out = sb.getstatusoutput('yum install git -y')
                sb.call("echo 'git not found'", shell=True)
                if 'complete!' in out[1]:
                        sb.call("echo 'Successfully installed git...'", shell=True)


sb.call("rm -rf /home/ec2-user/Automa", shell=True)
sb.call("git clone https://github.com/Prateek937/Automa.git",shell=True)
"""if out[0] == 0:
        sb.call("echo 'repository cloned successfully...", shell=True)
else:
        sb.call("echo 'Repository clone  failed...", shell=True)
        print(out[1])"""
