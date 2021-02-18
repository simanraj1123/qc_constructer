# Importing standard Qiskit libraries and configuring account
from qiskit import QuantumCircuit, execute, Aer, IBMQ, QuantumRegister, ClassicalRegister
from qiskit.compiler import transpile, assemble
from qiskit.tools.jupyter import *
from qiskit.visualization import *
from qiskit.circuit.library.standard_gates import U1Gate, U3Gate
from qiskit.converters import circuit_to_gate

import numpy as np

def circuit(params, phases,n):
    
    nq = n#np.log2(len(phases))
    
    qbits = QuantumRegister(nq, 'q')
    circ_main = QuantumCircuit(qbits)
    
    def q(x):
        return nq - 1 - x
    
    for i in range(len(params)):
        port1d, port2d = params[i][0]
        theta, phi = params[i][1]
        
        port1 = list(format(port1d, f'0{nq}b'))
        port2 = list(format(port2d, f'0{nq}b'))
#         print(port1, port2)
        
        qb = QuantumRegister(nq, 'q')
        circ = QuantumCircuit(qb, name=f'Select\n{port1d},{port2d}')
        
        for j in range(len(port1)-1):
            
            subport1 = port1[j:j+2]
            subport2 = port2[j:j+2]
#             print(subport1, subport2)
            
            if subport1 == subport2:
                if subport1[0] == '0':
                    circ.x(j)
                    port1[j] = '1'
                    port2[j] = '1'
                if subport1[1] == '0':
                    circ.x(j+1)
                    port1[j+1] = '1'
                    port2[j+1] = '1'
            
            elif subport1 == list('00'):
                if subport2 == list('01'):
                    circ.x(j)
                elif subport2 == list('10'):
                    circ.x(j+1)
                    circ.swap(j,j+1)
                elif subport2 == list('11'):
                    circ.x(j)
                    circ.cx(j+1, j)
                port1[j]='1'
                port1[j+1]='0'
                port2[j]='1'
                port2[j+1]='1'
            
            elif subport1 == list('01'):
                if subport2 == list('10'):
                    circ.swap(j,j+1)
                    circ.cx(j+1, j)
                elif subport2 == list('11'):
                    circ.swap(j,j+1)
                port1[j]='1'
                port1[j+1]='0'
                port2[j]='1'
                port2[j+1]='1'
        
        selection_gate = circuit_to_gate(circ)
        selection_gate_inv = circuit_to_gate(circ.inverse())
        
        circ_main.append(selection_gate, range(nq-1,-1,-1))
        ctrlu = U3Gate(-2*theta, 0, -phi).control(nq-1)
        circ_main.append(ctrlu, range(nq-1,-1,-1))
        circ_main.append(selection_gate_inv, range(nq-1,-1,-1))
        
    qb = QuantumRegister(nq, 'q')
    circ_phases = QuantumCircuit(qb, name="Phases")
    for i in range(len(phases)):
        port = format(i, f'0{nq}b')
        
        for k in range(len(port)):
            if port[k]=='0':
                circ_phases.x(q(k))
        
        ctrlphase = U1Gate(phases[i]).control(nq-1)
        circ_phases.append(ctrlphase, range(nq))
        
        for k in range(len(port)):
            if port[k]=='0':
                circ_phases.x(q(k))
                
    phases_gate = circuit_to_gate(circ_phases)
    
    circ_main.append(circ_phases, qbits)
    
    return circ_main
