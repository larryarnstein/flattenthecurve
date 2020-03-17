import matplotlib.pyplot as plt
import numpy as np

duration = 200
survival = 0.96 #chance of surviving
recovery = 21 #median days to recover median
terminal = 14 #median days to die if not recovering
transmit = 5 #median days to transmit infection
start_of_lock_down = 40
max_lookahead = 60 #the extra space we need in the arrays to capture data that happens after the end of the simulation
lock_down_effectiveness = 0.9 #rate at which R0 declines after the start of lockdown

np.random.seed(1)
R0 = np.zeros([max_lookahead + duration])
sick = np.zeros([max_lookahead + duration])
recovered = np.zeros([max_lookahead + duration])
dead = np.zeros([max_lookahead + duration])
new = np.zeros([max_lookahead + duration])

# need to add patient zero fate to the other arrays
sick[0] = 1  #initial number of sick people to get things going. Can start with 1
new[0] = 1
R0[0] = 2.1 #this was the initial reported R0, this should decline with aggressive social constraints

days = range(duration)

for d in days :
    if (d>0) : 
        sick[d] = sick[d] + sick[d-1] + new[d]
        dead[d] = dead[d] + dead[d-1]
        recovered[d] = recovered[d] + recovered[d-1]
        if (d > start_of_lock_down) :
            newR0 = R0[d-1] * 0.95
            R0[d] = max(0.5, newR0)
        else :
            R0[d] = R0[d-1]
    newly_infected = 0
    for patient in range(int(new[d])) :
        newly_infected = int(newly_infected + min(max_lookahead,max(0,np.round(np.random.normal(R0[d],0.5)))))
    for n in range(int(newly_infected)) :
        outcome = np.random.uniform()
        date_infected = int(d + np.round(min(max_lookahead, max(1,np.random.normal(transmit,7)))))
        new[date_infected] = new[date_infected] + 1
        if (outcome < survival) :
            time_to_recover = int(np.round(min(max_lookahead, max(1,np.random.normal(recovery,7)))))
            recovered[date_infected+time_to_recover] = recovered[date_infected+time_to_recover] + 1
            sick[date_infected+time_to_recover] = sick[date_infected+time_to_recover]-1
        else :
            time_to_die = int(np.round(min(max_lookahead,max(1,np.random.normal(terminal,3)))))
            dead[date_infected+time_to_die] = dead[date_infected+time_to_die]+1
            sick[date_infected+time_to_die] = sick[date_infected+time_to_die]-1
    


fig, axs = plt.subplots(4)
plt.ylim(bottom=0)
axs[0].set_title('Currently Sick')
axs[0].plot(sick[0:duration])
axs[1].set_title('died')
axs[1].plot(dead[0:duration])
axs[2].set_title('recovered')
axs[2].plot(recovered[0:duration])
axs[3].set_title('R0')
axs[3].plot(R0[0:duration])
plt.subplots_adjust(top=3)

