#copyright: Larry Arnstein 2020
#open source under the MIT License

import matplotlib.pyplot as plt
import numpy as np

duration = 200 #number of days to run the simulation from patient zero
survival = 0.96 #chance of surviving
recovery = 21 #median days to fully recover
terminal = 14 #median days to die if not recovering
transmit = 5 #median days to transmit infection
start_of_lock_down = 40 #days from start when lock-down begins
lock_down_effectiveness = 0.20 #precent by wich R0 declines pre day after the start of lockdown
initial_R0 = 2.1 # read this somewhere
minimum_R0 = 0.5 # best case R0 once lock down is fully in place


max_lookahead = 60 #not a model parameter. This is the extra space we need to allocate in the arrays to capture data that happens after the end of the simulation

# utility function for generating normally distributed random numbers with upper and lower bounds
def min_max_normal(mu,sigma,lb,ub) :
    return int(round(min(ub,max(lb,np.round(np.random.normal(mu,sigma))))))

def sim(start, effect) : 
    np.random.seed(1)
    R0 = np.zeros([max_lookahead + duration])
    sick = np.zeros([max_lookahead + duration])
    recovered = np.zeros([max_lookahead + duration])
    dead = np.zeros([max_lookahead + duration])
    new = np.zeros([max_lookahead + duration])
    
    sick[0] = 1  #initial number of sick people to get things going. Can start with 1
    new[0] = 1
    R0[0] = 2.1 #this was the initial reported R0, this should decline with aggressive social constraints

    days = range(duration)
    for d in days :
        # determine how many people each new patient will infect
        newly_infected = int(0)
        for patient in range(int(new[d])) :
            newly_infected = newly_infected + min_max_normal(R0[d],minimum_R0,0,max_lookahead)
            
        # determine future outcomes for each new patient
        for n in range(int(newly_infected)) :
            #determine date of infection
            date_infected = d + min_max_normal(transmit,7,1,max_lookahead)
            new[date_infected] += 1
            
            #determine survival
            outcome = np.random.uniform()
            if (outcome < survival) :
                time_to_recover = min_max_normal(recovery,7,1,max_lookahead)
                recovered[date_infected+time_to_recover] += 1 
                sick[date_infected+time_to_recover] += -1 #decrement sick on date of recovery
            else :
                time_to_die = min_max_normal(terminal,3,1,max_lookahead)
                dead[date_infected+time_to_die] += 1 
                sick[date_infected+time_to_die] += -1 # decrement sick on date of death
                
        # setup accumulators for next day
        sick[d+1] = (sick[d] + new[d+1]) + sick[d+1]
        dead[d+1] = dead[d+1] + dead[d]
        recovered[d+1] = recovered[d+1] + recovered[d]
        
        #adjust R0 based on lockdown date and effectiveness
        if (d+1 > start) :
            newR0 = R0[d] * (1-effect)
            R0[d+1] = max(0.5, newR0)
        else :
            R0[d+1] = R0[d]
    
    return sick,dead,recovered,R0

s1,d1,r1,a = sim(40,0.2)
s2,d2,r2,b = sim(47,0.1)

fig, axs = plt.subplots(4)
plt.ylim(bottom=0)
axs[0].set_title('Sick')
axs[0].plot(s1[0:duration])
axs[0].plot(s2[0:duration])
axs[1].set_title('Died')
axs[1].plot(d1[0:duration])
axs[1].plot(d2[0:duration])
axs[2].set_title('Recovered')
axs[2].plot(r1[0:duration])
axs[2].plot(r2[0:duration])
plt.ylim(top=2.5)
axs[3].set_title('R0')
axs[3].plot(a[0:duration])
axs[3].plot(b[0:duration])
plt.subplots_adjust(top=3)

