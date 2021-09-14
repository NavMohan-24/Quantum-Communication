#!/usr/bin/env python
# coding: utf-8

# In[113]:


from qiskit import*
from qiskit.tools.visualization import*
from qiskit.quantum_info import random_statevector
from qiskit.extensions import Initialize


# In[114]:


qr=QuantumRegister(3,'qr')
crx=ClassicalRegister(1,'crx')
crz=ClassicalRegister(1,'crz')
qc=QuantumCircuit(qr,crx,crz)
#qc.draw('mpl')


# In[115]:


#creation of entanglement channel for communication (1/sqrt(2)(|00>+|11>))
def create_ent_channel(qc,a,b):
    qc.barrier()
    qc.h(qr[a])
    qc.cx(qr[a],qr[b])
    
#Bell Measurement by alice
def bell_measurement(qc,a,b):
    qc.barrier()
    qc.cx(qr[a],qr[b])
    qc.h(qr[a])
    qc.measure(qr[a],crx)
    qc.measure(qr[b],crz)
    

#Bobs transformation
def bob_transformation(qc,qubit):
    qc.barrier()
    qc.x(qubit).c_if(crx,1)
    qc.z(qubit).c_if(crz,1)
#note: bob's transformation may change depending upon the entanglement channel

#creating a state that we want to teleport : alice will be the sender
state=random_statevector(2,seed=3)
state.probabilities()
init_gate=Initialize(state.data)
qc.append(init_gate,[0])


# In[116]:


create_ent_channel(qc,1,2)
bell_measurement(qc,0,1)
bob_transformation(qc,2)
#qc.draw('mpl')

#thus the bob qubit will be transformed to state which alice want to sent. 
#state of the alice's qubit get collapsed during the process

#checking the bobs state
backend=BasicAer.get_backend('statevector_simulator')
in_state=state
plot_bloch_multivector(in_state)
# In[117]:


disentangler=init_gate.gates_to_uncompute() #re
qc.append(disentangler,[2]) 

out_state=execute(qc,backend).result().get_statevector()
plot_bloch_multivector(out_state)
# In[118]:


#to check bob received corect state
qc.measure(qr[2],crx)
#qc.draw('mpl')


# In[119]:


backend=BasicAer.get_backend('qasm_simulator')
counts=execute(qc,backend,shots=1024).result().get_counts()
plot_histogram(counts)


# In[120]:


qc.draw('mpl')


# In[ ]:




