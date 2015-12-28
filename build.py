import os
import platform
import sys
from subprocess import call, Popen, PIPE
import commands

if __name__ == "__main__":
    os.system('conan export lasote/stable')
   
    def test(settings, visual_version=None):
        argv =  " ".join(sys.argv[1:])
        curdir = os.path.abspath(os.path.curdir)
        if visual_version:
            vcvars = 'call "%vs' +  str(visual_version) + '0comntools%../../VC/vcvarsall.bat"'
            param = "x86" if "arch=x86 " in settings else "amd64"
            command = '%s %s && conan test . %s %s' % (vcvars, param, settings, argv)
        else:
            command = 'conan test . %s %s' % (settings, argv)
        retcode = os.system(command)
        if retcode != 0:
            exit("Error while executing:\n\t %s" % command)

        
    if platform.system() == "Windows":
        for visual_version in [ 12, 10, 14]:
            compiler = "-s compiler=\"Visual Studio\" -s compiler.version=%s " % str(visual_version)
            
            # Shared x86
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o libxml2:shared=True', visual_version)
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o libxml2:shared=True', visual_version)
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o libxml2:shared=True', visual_version)
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o libxml2:shared=True', visual_version)

            # Static x86
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MTd -o libxml2:shared=False', visual_version)
            test(compiler + '-s arch=x86 -s build_type=Debug -s compiler.runtime=MDd -o libxml2:shared=False', visual_version)
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MD -o libxml2:shared=False', visual_version)
            test(compiler + '-s arch=x86 -s build_type=Release -s compiler.runtime=MT -o libxml2:shared=False', visual_version)

              
            
            if visual_version != 10:
                
                # Static x86_64
                test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o libxml2:shared=False', visual_version)
                test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o libxml2:shared=False', visual_version)
                test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o libxml2:shared=False', visual_version)
                test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o libxml2:shared=False', visual_version)
               
       
                # Shared x86_64
                test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MDd -o libxml2:shared=True', visual_version)
                test(compiler + '-s arch=x86_64 -s build_type=Debug -s compiler.runtime=MTd -o libxml2:shared=True', visual_version)
                test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MD -o libxml2:shared=True', visual_version)
                test(compiler + '-s arch=x86_64 -s build_type=Release -s compiler.runtime=MT -o libxml2:shared=True', visual_version)


                   
           
     
    else:
           
        # Static x86
        test('-s arch=x86 -s build_type=Debug -o libxml2:shared=False')
        test('-s arch=x86 -s build_type=Release -o libxml2:shared=False')
        # Shared x86
        test('-s arch=x86 -s build_type=Debug -o libxml2:shared=True')
        test('-s arch=x86 -s build_type=Release -o libxml2:shared=True')
     
        
    
        # Shared x86_64
        test('-s arch=x86_64 -s build_type=Debug -o libxml2:shared=True')
        test('-s arch=x86_64 -s build_type=Release -o libxml2:shared=True')
     
        # Static x86_64
        test('-s arch=x86_64 -s build_type=Debug -o libxml2:shared=False')
        test('-s arch=x86_64 -s build_type=Release -o libxml2:shared=False')
 
   