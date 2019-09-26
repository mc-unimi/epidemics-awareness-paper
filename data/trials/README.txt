In the trial folder are stored the CSV files corresponding to the simulation trials produced for figures 3,4,7, and 8. 
File names indicate the figure to which it refers and some configuration information.
For example:
- Fig3-trials-L_H-70_30.csv indicates Figure 3, and a proportion 70/30 between L/H type nodes.
- Fig3-trials-noAw_100.csv indicates that nodes have no awareness mechanism (therefore, no L or H).

- Fig4-trials-L_H-95_5.csv indicates that the population of agents is composed by L and H types with a proportion 95/5.
- Fig4-trials-noAw_L-50_50.csv indicates that the population of agents is composed by no awareness and L type agents with a proportion 50/50.

For Figure 7, in addition to the proportion L/H, the file name indicates the threshold value for Negative Imitation:
- Fig7-trials-L_H-70_30-Thr_08.csv, indicates a proportion 70/30 of L/H types and a threshold of 0.8.

For Figure 8, the population is always of L/H types, and the configuration could be set with:
- imitation mechanism ON (IM) or OFF (noIM);
- message mechanism ON, subject to a threshold about the number of messages needed to trigger Negative Imitation (T8 or T10), or 
message mechanism OFF (T1000 represents an unreachable message threshold):   
- Fig8-trials-noIM_MSG_T10-90_10.csv means that: 1) the imitation mechanism was turned OFF (noIM), 2) the message mechanism is ON with a 
threshold of 10 messahes (T10), and 3) the L/H proportion is 90/10.
-Fig8-trials-IM_MSG_T1000-70_30.csv means that 1) the imitation mechanism was turned ON (IM), 2) the message mechanism is OFF (T1000), 
and 3) the L/H proportion is 70/30.

At least 200 valid trials have been produced for each average result plotted in Fig.3/4/7/8.
Valid trials have been considered those that actually produced an epidemic diffusion, sustained until the end of the simulation (time step 20) or possibly terminating before that.
Non-valid trials have been considered those trials that, for probabilistic reason, failed to produce an epidemic diffusion, typically limited to few infected nodes (10 to 20 at most) and terminated in the first 2,3 time steps at most.
Given the reference configuration that we used throughout our simulations, with an infection probability P_SI = 0.2, and the presence of only a single seed node, the large majority of non-valid trials corresponded to simulations that terminated within the first time step.

