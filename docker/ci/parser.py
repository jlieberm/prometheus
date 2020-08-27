#!/usr/bin/env python3


from Gaugi.messenger    import LoggingLevel, Logger
import argparse
import sys,os


mainLogger = Logger.getModuleLogger("Parser")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()


parser.add_argument('-t','--test', action='store', dest='test', required = True ,
                    help = "ci test number")




def cmd( f, command ):
  print(command)
  f.write(command+'\n')


if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

# Get the number of cpus
import multiprocessing
ncpu = multiprocessing.cpu_count()



f = open('/command.sh', 'w')

# pull and setup prometheus
cmd( f,  '. /setup_envs.sh' )

command = 'python /ci/ci.py -i /ci/sample.root -o /ci/output.root --nov 100 -t %s'%args.test

# Run it!
cmd( f, command )
f.close()

os.system('. /command.sh')



