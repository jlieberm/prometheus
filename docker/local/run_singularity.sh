singularity  shell --writable-tmpfs --nv --bind /data:/data --bind /afs:/afs --bind /eos:/eos --bind /cvmfs:/cvmfs  docker://jodafons/prometheus:local
