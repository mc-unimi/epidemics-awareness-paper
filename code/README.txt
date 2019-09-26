Copyright (C) 2019 Samira Maghool and Marco Cremonini
All files of this folder are part of the research project described in the paper titled "A multicomponent model of awareness for different categories of network epidemics", by Samira Maghool, Nahid Maleki-Jirsaraei, and Marco Cremonini.

Our multiagent epidemic simulator is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Our multiagent epidemic simulator is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License

File Parameters_Configuration_Chart.pdf lists all parameters with reference values and descriptions.

How to use the simulator:
1.	Open MySimulation.py module.
2.	Specify number of nodes, time of simulation and network configuration.
3.	In the main function of MySimulation.py module, define density of types (L/H).
4.	In the NetworkSimulation module, you can change the number of trials.
5.	In the SIRSAgent module, you are able to change the P_S_base, P_IR_base, P_R_base probabilities and agents behavioral function (like imitation).
6.	Run the MySimulation.py module, you will get the “trial_values_infected.csv” file. (Please notice that the plotted diagram in the result folder, “plot_SIR.png”, is the average over all trials, even non-epidemic trials) 

