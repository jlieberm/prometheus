# prometheus tools:

This directory is dedicated to all tools implemented to run for each event during the main loop.
Each tool must have `initialize`, `execute` and `finalize` methods. The `execute` method will be call
for each event (entry) into the `ntuple`. The user will have access to all `prometheus` services inside 
of the tool.

## Organization:

Each tool will be dedicated to one type of analysis. You can see the description and usage of each tool
inside of each tool directory.


