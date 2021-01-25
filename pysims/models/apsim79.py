import glob
import os
import shutil
import sys
import tarfile
import traceback
from model import Model
from subprocess import Popen, PIPE

class Apsim79(Model):

    def run(self, latidx, lonidx):
        try:
            executable = self.config.get('executable')
            apsim_dir = os.path.dirname(os.path.dirname(executable))
            
            # Create sim files
            # p = Popen('source %s/paths.sh ; mono %s/Model/ApsimToSim.exe Generic.apsim' % (apsim_dir, apsim_dir), shell=True, executable='/bin/bash', stdout=PIPE, stderr=PIPE)
            #### generic = open('Generic.apsim')
            #### for i in generic:
            ####    print(i)
            
            my_current_dir = os.getcwd()
            #### print(os.listdir('.'))
            #### shutil.copyfile('Generic.apsim', '/test/Generic.apsim')

            p = Popen('/data/uqjojeda/ApsimToSim.sh Generic.apsim', shell=True, executable='/bin/bash', stdout=PIPE, stderr=PIPE)
            stdout, stderr = p.communicate()
            stdout_file = open('RESULT.OUT', 'w')
            stdout_file.write(stdout)
            #### print(stdout)
            #### print(stderr)
            if p.returncode != 0:
                return False
            ####print(executable)
           
            # Run apsim for each sim file
            for sim in glob.glob('*.sim'):
                # p = Popen('source %s/paths.sh ; %s %s' % (apsim_dir, executable, sim), shell=True, executable='/bin/bash', stdout=PIPE, stderr=PIPE)
                p = Popen('/data/uqjojeda/Apsim.sh %s' % (sim), shell=True, executable='/bin/bash', stdout=PIPE, stderr=PIPE)
                stdout, stderr = p.communicate()
                stdout_file.write(stdout)
                if p.returncode != 0:
                    return False
            stdout_file.close()
            #### print(my_current_dir)
            #### print('Content of directory after-->', os.listdir('.'))
            return True
            

        except:
            print "[%s]: %s" % (os.path.basename(__file__), traceback.format_exc())
            return False
