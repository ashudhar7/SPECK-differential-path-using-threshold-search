
# coding: utf-8

# ### function to calculate minimum probility p_min to check given condition

# In[1]:

def p_minimum(n,trail_cap,B_cap,B_bar):
        p_min = 1.0;
        for i in range(0,n):
            p_min *= trail_cap[i].wt
        p_min = p_min * B_cap[nrounds - 1 - (n + 1)]; 
        p_min = B_bar/p_min
        return p_min


# ### function to check given inputs are available in highways path list or not 

# In[2]:

def highwaylist():
    alph,bet,gam,pro = [],[],[],[]
    with open('alph.txt') as ip1, open('bet.txt') as ip2, open('gam.txt') as ip3, open('pro.txt') as ip4:
        for i1,i2,i3,i4 in zip(ip1,ip2,ip3,ip4):
            hw.append(NMTS(int(i1.strip()),int(i2.strip()),int(i3.strip()),float(i4.strip()))) 
            


# ### function to calculate weight 

# In[3]:

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


# In[4]:

##function to update croad with prob more than pmin and output is in highway


# In[5]:

def PDDT1(n,p_thres,k,wt,da,db,dc,s,maxddt,ddt,m):
    if(n==k):
        ddt.append(NMTS(da,db,dc,wt))
        if(wt>=s):
            maxddt.append(NMTS(da,db,dc,wt))
        return 
    
    for z in range(0,2):
        new_da= (da & ((2 ** m) - 1))
        new_db= (db & ((2 ** m) - 1))
        new_dc= (dc | (z<<k) & mask)
        wt= weight(new_da,new_db,new_dc)
        if(wt >= p_thres or ((z==1) and (k+1)!=n)):                    
            PDDT1(n,p_thres,k+1,wt,da,db,new_dc,s,maxddt,ddt,m+1)  
            
    if(len(ddt)==0):
        return 0,ddt,maxddt
    else:
        return 1,ddt,maxddt
   


# In[6]:

##fucntion to find output for which weight is max


# In[7]:

def PDDT(n,p_thres,k,wt,da,db,dc,s,maxddt,ddt,m):
    if(n==k):
        ddt.append(NMTS(da,db,dc,wt))
        #print(da,db,dc,wt,l)
        if(wt>=s):
            s=wt
            maxddt.append(NMTS(da,db,dc,s))
        return 
  
    for z in range(0,2):
        new_da= (da & ((2 ** m) - 1))
        new_db= (db & ((2 ** m) - 1))
        new_dc= (dc | (z<<k) & mask)
        wt= weight(new_da,new_db,new_dc)
        if(wt >= p_thres or ((z==1) and (k+1)!=n)):                    
            PDDT(n,p_thres,k+1,wt,da,db,new_dc,s,maxddt,ddt,m+1) 
            
    if(len(ddt)==0):
        return 0,ddt,maxddt
    else:
        return 1,ddt,maxddt
   
   


# ### function to perform left and right circular rotation 

# In[8]:


#right circular shifts
def ROR(x,r):
    x = ((x << (SPECK_TYPE - r)) + (x >> r)) & mask
    return x

#left circular shifts
def ROL(x,r):
    x = ((x >> (SPECK_TYPE - r)) + (x << r)) & mask
    return x


# ### main function for threshold search

# In[ ]:

def threshold_search(n,nrounds,hw,B_cap,B_bar,B_barlist,st0,st1,op,w1):
    if(n == 0): 
        B_cap_temp[nrounds-1]=w1*B_cap[nrounds-1-(n+1)]
        if(B_cap_temp[nrounds-1]>B_bar):
            B_barlist[n]=w1
            trail_cap[n]= NMTS(ROL(st1,alpha),st0,op,w1)
            st1=op
            st0=ROL(st0,beta)^st1
            return threshold_search(n+1,nrounds,hw,B_cap,B_bar,B_barlist,st0,st1,op,w1)
        else:
            return B_bar,B_cap 
            
    if((n > 0) & (n != (nrounds - 1))):
        print(n)
        st1=ROR(st1,alpha)
        p_min=p_minimum(n,trail_cap,B_cap,B_bar)
        croad=[]
        #function that check output is in highway and weight is greater than p_min or not, if it is update croad
        maxddt,ddt,max_p=[],[],0
        ck,ddt,maxddt=PDDT1(SPECK_TYPE,0.1,0,1,st1,st0,0,p_min,maxddt,ddt,1)
        if(ck==1):
            for i in range(0,len(maxddt)):
                croad.append(NMTS(maxddt[i].dx,maxddt[i].dy,maxddt[i].dz,maxddt[i].wt))
                         
        #opcheck_in_highways(0,p_min,st1,st0)
        #if croad is still empty then fill it with max probility value for other outputs except highway
        if(len(croad) == 0):
            crddt,ddt,max_p=[],[],0
            #print(st1,st0,max_p)
            ck,ddt,crddt=PDDT(SPECK_TYPE,0,0,1,st1,st0,0,max_p,crddt,ddt,1)
            #max_p,output,ck=max(0,st1,st0)
            if(ck==1):
                for i in range(0,len(crddt)):
                    croad.append(NMTS(crddt[i].dx,crddt[i].dy,crddt[i].dz,crddt[i].wt))
            else:
                return B_bar,B_cap
    
        crhw = []
        temphw=[]
        maxddt,ddt,max_p=[],[],0
        ck,ddt,maxddt=PDDT(SPECK_TYPE,0.1,0,1,st1,st0,0,max_p,maxddt,ddt,1)
        #val1,val2,val3,w,chk= searchinhighway(st1,st0)
        if(ck==1):
            for i in range(0,len(ddt)):
                crhw.append(NMTS(ddt[i].dx,ddt[i].dy,ddt[i].dz,ddt[i].wt))
        
        for i in range(0,len(croad)):
            crhw.append(NMTS(croad[i].dx,croad[i].dy,croad[i].dz,croad[i].wt))

            
        p_r=1
        for i in range(0,n):
            p_r *= trail_cap[i].wt
        for i in range(0,len(crhw)):
            B_cap_temp[nrounds-1]= p_r * crhw[i].wt * B_cap[nrounds - 1 - (n + 1)]
            if(B_cap_temp[nrounds-1]>B_bar):
                B_barlist[n]=p_r * crhw[i].wt
                trail_cap[n]=NMTS(ROL(crhw[i].dx,alpha),crhw[i].dy,crhw[i].dz,crhw[i].wt)
                st1=crhw[i].dz
                st0=ROL(st0,beta)^st1
                return threshold_search(n+1,nrounds,hw,B_cap,B_bar,B_barlist,st0,st1,op,w1)
            else:
                return B_bar,B_cap
            return B_bar,B_cap
                    
    if(n ==(nrounds - 1)):
        st1=ROR(st1,alpha)
        #print(n)
        crddt,ddt,max_p=[],[],0
        ck,ddt,crddt=PDDT(SPECK_TYPE,0.1,0,1,st1,st0,0,max_p,crddt,ddt,1)
        #max_p,output,ck=max(0,st1,st0)
        if(ck==1):
            p=crddt[0].wt
            op=crddt[0].dz
        else:
            crddt,ddt,max_p=[],[],0
            ck,ddt,crddt=PDDT(SPECK_TYPE,0,0,1,st1,st0,0,max_p,crddt,ddt,1)
            if(ck==1):
                p=crddt[0].wt
                op=crddt[0].dz
                if(p>=0.1):
                     hw.append(NMTS(st1,st0,op,p))
                
        if(ck==0):
            return B_bar,B_cap             
        p_r=1
        for i in range(0,n):
            p_r *= trail_cap[i].wt
        B_cap_temp[nrounds-1]=p * p_r
        if(B_cap_temp[nrounds-1]>B_bar):
            B_barlist[n]=B_cap_temp[nrounds-1]
            #print ("%.16f %.16f" % (B_cap_temp[n],B_bar))
            trail_cap[n]=NMTS(ROL(st1,alpha),st0,op,p)
            B_bar=B_cap_temp[nrounds-1]
            for i in range(0,len(B_cap)):
                B_cap[i]=B_barlist[i]
                B_bar=B_cap_temp[n]  
            for i in range(0,len(trail_cap)):
                print(trail_cap[i].dx,trail_cap[i].dy,trail_cap[i].dz,trail_cap[i].wt)
            return B_bar,B_cap
        else:
            return B_bar,B_cap
    


# In[ ]:

import random
import math 
#alpha beta are for left and right circular shift     
alpha, beta = 8,3
#speck total number of round epresented by nrounds
nrounds,n,s=13,0,0
SPECK_TYPE=32
mask,wshift = 2 ** 32 - 1, 31
#B_cap=[0.00048,0.00048,0.0625,0.00048,0.00048,0.00048,0.00048,0.00048,0.00048]
B_cap,B_bar=[2**(-50),2**(-100),2**(-150),2**(-200),2**(-250),2**(-300),2**(-350),2**(-400),2**(-450),2**(-500),2**(-550),2**(-600),2**(-650)],2 ** (-650)
B_barlist=[0]*nrounds
#B_cap,B_bar=[2**(-11),2**(-22),2**(-33),2**(-38)],2 ** (-38)
trail_cap,trail_bar=[0]*nrounds, [0]*nrounds
croad,hw,B_cap_temp=[],[],[0]*nrounds
hlen=3951388
max_p,output=0,0
maxddt,ddt,max_p=[],[],0
print ("%.30f" % B_bar)
class NMTS(object):
    """__init__() functions as the class constructor"""
    def __init__(self, dx=None, dy=None, dz=None, wt=None):
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.wt = wt
        
highwaylist()
for ch in range(1,len(hw)):
    #st0=(random.randint(1,mask))
    #st1=(random.randint(1,mask))
    B_bar,B_cap =threshold_search(n,nrounds,hw,B_cap,B_bar,B_barlist,hw[ch].dx,hw[ch].dy,hw[ch].dz,hw[ch].wt)
    print(B_bar,ch)

