# Automated Reasoning Project

## Running the Executable
To run the program navigate to the _dist_ directory which will contain two executables:
* `congruenceClosure`: contains the logic of the Congruence Closure Algorithm 
* `runner` contains the cli and the logic to spawn multiple congruenceClosure processes so as to run multiple inputs in parallel

Once you are in the directory move your input files(or directory) into the _dist_ directory.
To run the implementation execute the `runner` executable.
Then follow the instructions you can see on screen.
![](img/Screenshot%20from%202023-06-22%2022-05-59.png)

once the input file is processed the output can be viewed both on screen or alternatively into the _output_ directory.
If the user would like to use the output as input for an analysis a csv version of each output 
can be viewed in _output/csv_ directory.