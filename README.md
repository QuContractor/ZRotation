# Rz Rotation 

This tool finds T-optimal approximations of single-qubit Z-rotations using quantum circuits consisting of Clifford and T gates.

The algorithm and method are presented in [ref2].  Here we only take the result and package it inside a short python script. 

The interface is for HiQ/ProjectQ. However, one can easily modify it to other QSAM such as IBM or Rigetti's.

![image-20191118221700801](Rz.jpg)

```python
from zrot import * 

circuit = ['Rz(0.383185307179586) | Qureg[3]']
print ('The length is:',len(zrot(circuit, T_cutoff = 3)))
zrot(circuit, T_cutoff = 3)
```

Then you get: 

```
The length is: 27
['Sdag | Qureg[3]\n',
 'T | Qureg[3]\n',
 'H | Qureg[3]\n',
 'Sdag | Qureg[3]\n',
 'T | Qureg[3]\n',
 'H | Qureg[3]\n',
 'T | Qureg[3]\n',
 'H | Qureg[3]\n',
 'T | Qureg[3]\n',
 'H | Qureg[3]\n',
 'T | Qureg[3]\n',
 'Sdag | Qureg[3]\n',
 'Z | Qureg[3]\n',
 'H | Qureg[3]\n',
 'T | Qureg[3]\n',
 'Sdag | Qureg[3]\n',
 'Z | Qureg[3]\n',
 'H | Qureg[3]\n',
 'T | Qureg[3]\n',
 'Sdag | Qureg[3]\n',
 'Z | Qureg[3]\n',
 'H | Qureg[3]\n',
 'T | Qureg[3]\n',
 'Sdag | Qureg[3]\n',
 'Z | Qureg[3]\n',
 'H | Qureg[3]\n',
 'T | Qureg[3]\n']
```



### Reference

1. arXiv: 1212.6964, Practical approximation of single-qubit unitaries by single-qubit quantum Clifford and T circuits