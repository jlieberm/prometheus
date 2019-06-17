
def launch( command, maxJobs, nthreads ):
  import os
  import subprocess
  from pprint import pprint
  process_pipe = []
  output_stack = []
  jobs = range(maxJobs)
  import time
  while len(jobs) > 0:
    time.sleep(5)
    if len(process_pipe) < int(nthreads):
      job_id = jobs.pop()
      pprint(command)
      proc = subprocess.Popen(command.split(' '))
      process_pipe.append( (job_id, proc) )
  
    for proc in process_pipe:
      if not proc[1].poll() is None:
        print( ('pop process id (%d) from the stack')%(proc[0]) )
        process_pipe.remove(proc)
  
  # Check pipe process
  # Protection for the last jobs
  while len(process_pipe)>0:
    for proc in process_pipe:
      if not proc[1].poll() is None:
        print( ('pop process id (%d) from the stack')%(proc[0]) )
        # remove proc from the pipe
        process_pipe.remove(proc)



launch( "./build/generator -m scripts/run2.mac", 100, 30)

