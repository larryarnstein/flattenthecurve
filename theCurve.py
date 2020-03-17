import matplotlib.pyplot as plt
import numpy as np

duration = 20
survival = 0.98 #chance of surviving
recovery = 21 #median days to recover median
terminal = 14 #median days to die if not recovering
transmit = 5 #median days to transmit infection

R0 = np.zeros([10*duration])
sick = np.zeros([10*duration])
recovered = np.zeros([10*duration])
dead = np.zeros([10*duration])
new = np.zeros([10*duration])

# need to add patient zero fate to the other arrays
sick[0] = 1 
R0[0] = 2.1

days = range(duration)

for d in days :
    if (d>0) : 
        sick[d] = sick[d] + sick[d-1]
        R0[d] = R0[d-1]
    newly_infected = 0
    for patient in range(int(sick[d])) :
        newly_infected = int(newly_infected + max(0,np.round(np.random.normal(R0[d],0.5))))
        new[d] = newly_infected
    for n in range(int(newly_infected)) :
        outcome = np.random.uniform()
        date_infected = int(d + np.round(max(1,np.random.normal(transmit,7))))
        sick[date_infected] = sick[date_infected] + 1
        if (outcome < survival) :
            time_to_recover = int(np.round(max(1,np.random.normal(recovery,7))))
            recovered[date_infected+time_to_recover] = recovered[d+time_to_recover] + 1
            sick[date_infected+time_to_recover] = sick[date_infected+time_to_recover]-1
        else :
            time_to_die = int(np.round(max(1,np.random.normal(terminal,3))))
            dead[date_infected+time_to_die] = dead[d+time_to_die]+1
            sick[date_infected+time_to_recover] = sick[date_infected+time_to_recover]-1
    
    
print("sick",sick)
print("new",new)
print("recovered", recovered)
print("dead", dead)

plt.plot(sick[0:duration])
