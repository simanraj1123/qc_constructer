import numpy as np
import scipy.linalg as la

def rz_decomp(u_temp):
    u = u_temp[:]
    u = np.array(u, dtype=complex)
    N = len(u)
    decomp = []
    params = []
    
    for i in range(N-1,0, -1):
        
        for j in range(i-1, -1, -1):
            a, b, c, d = u[j, j], u[j, i], u[i, j], u[i, i]
            
            if c != 0:
                if d == 0:
                    theta = np.pi/2
                    phi = 0
                
                else:
                    theta = np.arctan(np.abs(c/d)) % (2*np.pi)
                    phi = (np.pi + np.angle(c) - np.angle(d)) % (2*np.pi)
        
                t = np.identity(N, dtype=complex)
                t[j, j], t[j, i], t[i, j], t[i, i] = np.cos(theta), - np.sin(theta), np.exp(1j*phi)*np.sin(theta), np.exp(1j*phi)*np.cos(theta)
                
#                 print(np.round(t,2))

                u = np.matmul(u, t)
#                 print(np.real(np.round(u,2)))
                decomp.append(la.inv(t))
                params.append([(j,i), (theta, phi)])
    
    return (u, decomp, params)
