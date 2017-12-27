import random
import math
def weight(alpha1,beta1,gamma1):  
    x1= (alpha1 << 1)& mask
    y1= (beta1  << 1)& mask
    z1= (gamma1  << 1)& mask
    not_x=(x1^mask)
    eq=((not_x)^y1)&(not_x^z1)
    s=eq&(alpha1^beta1^gamma1^(y1))
    if(s==0):        
        h=bin((~eq)& mask)
        wt=(h[1:].count("1"))
        return math.pow(2,-wt)
    else:
        return -200
    
def store(da,db,dc,wt):
    alpha.append(da)
    beta.append(db)
    gamma.append(dc)
    prob.append(wt)        
    return da,db,dc

def PDDT(n,p_thres,k,wt,da,db,dc):
    if(n==k):
        store(da,db,dc,wt)
        return 
    for x in range(0,2):
        for y in range(0,2):
            for z in range(0,2):
                new_da= (da | (x<<k) & mask)
                new_db= (db | (y<<k) & mask)
                new_dc= (dc | (z<<k) & mask)
                wt= weight(new_da,new_db,new_dc)
                if(wt >= p_thres or ((x==1 and y==1 and z==1) and (k+1)!=n)):                    
                    PDDT(n,p_thres,k+1,wt,new_da,new_db,new_dc)
    

mask = 2 ** 16 - 1
alpha,beta,gamma,prob=[],[],[],[]

  
PDDT(16,0.07,0,1,0,0,0)
for i in range(len(alpha)):
	  print(alpha[i])
print(len(prob))
for i in range(len(beta)):
	  print(beta[i])
print(len(prob))
for i in range(len(gamma)):
	  print(gamma[i])
for i in range(len(prob)):
	  print(prob[i])
print(len(prob))
	  
	  

	  
	  
	  
#print(len(prob))
#print(len(alpha))
#print(len(beta))
#print(len(gamma))