# Experiment

### Overview

This code implements a simple go/no-go task using pygame. However, there are some gaps that you have to fill in order to make the experiment run. After you got the experiment to run, we want you to collect some data from your fellow students or friends. The analysis we will do in the next two weeks will be based on this data. Each of your group members should try to find 2 friends to make the experiment.

For this assignment, you will need a library called pygame. To do this first activate your acc environment by
"conda activate acc."
Afterwards, type in "pip install pygame" in your terminal.
You are now ready to go!

The points for this assignment will be distributed as follows:
- Function to save Data as csv-file: **4 pts** (main experiment: line 76)
- Code for 'RT'(reaction time) and 'response': **2 pts** (main experiment: line 125 and 126)
- Set parameters: **2 pts** (parameter list: line 53 and 57)
- Number of total trials should be 100. Number of No-go trials should be 20.
- Create Datapath: **2 pts** (parameter list: line 73)
- When collecting datas, remember to change the subject ID for each participant!: (main experiment: line 139)

Additionally, you can get **2 points** for good coding style.

### Go/no-go Task

In a go/no-go task the participant is required to react to a “go” stimulus and refrain from reacting given a “no-go” signal. Measuring the response an the reaction time, in psychology this experiment paradigm is often used to evaluate impulsiveness and sustained attention.

In the following you will find a visualization of how the experiment should look like, once you successfully completed the code:

<img src="go-nogo.png" alt="drawing" width="450"/>
