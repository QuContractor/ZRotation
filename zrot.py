import re, copy, math

def cmd2pjq(sk_order, qbit, dagger = False):
    
    tt = sk_order[0].split('.') 
    cir = []
    if dagger:
        for gt in tt:
            if gt == 'P':
                cir.append('Sdag | Qureg[%s]\n'%qbit)
            elif gt == 'Pd':
                cir.append('S | Qureg[%s]\n'%qbit)
            elif gt == 'Td':
                cir.append('T | Qureg[%s]\n'%qbit)
            elif gt == 'T':
                cir.append('T | Qureg[%s]\n'%qbit)
                cir.append('Sdag | Qureg[%s]\n'%qbit)
            else:
                cir.append('%s | Qureg[%s]\n'%(gt,qbit))
    else:
        for gt in tt:
            if gt == 'P':
                cir.append('S | Qureg[%s]\n'%qbit)
            elif gt == 'Pd':
                cir.append('Sdag | Qureg[%s]\n'%qbit)
            elif gt == 'T':
                cir.append('T | Qureg[%s]\n'%qbit)
            elif gt == 'Td':
                cir.append('T | Qureg[%s]\n'%qbit)
                cir.append('Sdag | Qureg[%s]\n'%qbit)
            else:
                cir.append('%s | Qureg[%s]\n'%(gt,qbit))
    return cir

def pjq2cmd(input_circuit):
    
    circuit_cmd = []
    for circ in input_circuit:

        circ_str = circ.split("|")
        gate = circ_str[0][0:2].strip(' ')
        qbit = [int(x) for x in re.findall('(\d+)',circ_str[1])]
        n_bit = len(qbit)

        theta = None
        if circ_str[0][0] == 'R':
            theta = float(re.findall('.*\((.*)\).*',circ_str[0])[0])
            old_theta = theta
            if theta >3:
                theta = -(-theta%(2*math.pi))
        circuit_cmd.append([gate, qbit, theta])
        
    return circuit_cmd


def zrot(circuit_in, T_cutoff = 6):
    cir = []
    
    Ttable = {
        12 : ['H.X.T.H.P.T.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.T.H.T.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.T.H.T.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.T.H.P'],
        11 : ['P.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.T.H.T.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.T.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Id'],
        10 : ['H.T.H.P.T.H.T.H.T.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.T.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T'],
        9 : ['T.H.T.H.P.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.Td.Z.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Id'],
        8 : ['P.X.T.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.T.H.Td.Z.H.T.H.Td.Z.H.T.H.Td.Z'],
        7 : ['Z.T.H.Pd.T.H.T.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.T.H.T.H.T.H.T.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.P'],
        6 : ['H.X.T.H.T.H.T.H.Td.Z.H.T.H.T.H.Td.Z.H.T.H.T.H.Td.Z.H.Td.Z.H.P'],
        5 : ['Z.T.H.Pd.T.H.T.H.T.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.Td.Z.H.T.H.T.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.T.H.Td.Z.H.T.H.T'],
        4 : ['H.X.T.H.P.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.T.H.Td.Z.H.T.H.P'],
        3 : ['Pd.T.H.Pd.T.H.T.H.T.H.Td.Z.H.Td.Z.H.Td.Z.H.Td.Z.H.T'],
        2 : ['T'],
        1 : ['S'],
        0 : ['Z']
    }
    
    for circ in circuit_in:
        if circ[0:1] != 'R':
            cir.append(circ)
            continue
        theta = re.findall('.*\((.*)\).*', circ)[0]
        qbit = re.findall('(\d+)', circ)[-1]
        new_theta = abs(float(theta))
        
        if (circ[0:2] == 'Rx') & (abs(new_theta%(2*math.pi) - math.pi/2)<1E-4):
            cir.append('SqrtX | Qureg[%s]\n'%qbit)
            continue
        if (circ[0:2] == 'Rx') & (abs(new_theta%(2*math.pi) - 3*math.pi/2)<1E-4):
            cir.append('SqrtXdag | Qureg[%s]\n'%qbit)
            continue
        if (circ[0:2] == 'Rx') & (abs(new_theta%(2*math.pi) - 2*math.pi/2)<1E-4):
            cir.append('X | Qureg[%s]\n'%qbit)
            continue
        
#         if new_theta > 1.0:
#             cir.append(circ)
#             continue

        if theta[0] == '-':
            dagger = True
        else:
            dagger = False
        if (circ[0:2] == 'Rx') :
            cir.append('H | Qureg[%s]\n'%qbit)
        flag = copy.deepcopy(T_cutoff)     #控制精度只需控制这个参数即可，分为2^flag份
        divide = 2**flag
        k = round(divide*new_theta/math.pi)%(divide*2)
        
        while(k):
            if k%2 == 1:
                T_order = Ttable[flag]
                cir.extend(cmd2pjq(T_order, qbit, dagger))
                
            k = int(k/2)
            flag -= 1
        if circ[0:2] == 'Rx':
            cir.append('H | Qureg[%s]\n'%qbit)
    return cir

if __name__ == "__main__":
    
    ccc = ['Rz(6.193185307179586) | Qureg[3]']
    
    (zrot(ccc, T_cutoff = 5))

