



# Transformación de Park & Clarke

El módulo de Park (dq0) & Clarke (α, *β* ) incluye 

- Transformación de  componentes del tiempo, marco  A, B, C  a ejes nuevos ejes de referencia estacionario ortogonal   α, *β*.
- Inversa de Clarke, ejes de referencia estacionario ortogonal  α, *β*  a  componentes del dominio del tiempo, marco  A, B , C.
- Transformación de componentes  del tiempo, marco ABC hacia un sistema de referencia dq0 en régimen permanente.
- Inversa de Park, ejes de referencia rotatorio dq0 a componentes  del dominio del tiempo, marco A, B, C.
- Transformación de referencia estacionario ortogonal α, *β* hacia un marco de referencia rotatorio dq0.

## Instalación

La instalación del módulo se realiza con :

```Python
pip install ClarkePark
```

## Transformación (a,b,c) - (α, *β*)

El módulo tiene dependencias siendo necesario instalar `numpy` para procesar la información. También será necesario importar `matplotlib.pyplot` para visualizar los resultados.

```tex
alpha, beta, z = ClarkePark.abc_to_alphaBeta0(A,B,C)
```

Para poder usar la transformación es necesario generar las tres señales monofásicas en desfase y balanceadas.

```python
import ClarkePark
import numpy as np
import matplotlib.pyplot as plt

end_time = 10/float(60)
step_size = end_time/(1000)
t = np.arange(0,end_time,step_size)
wt = 2*np.pi*float(60)*t

rad_angA = float(0)*np.pi/180
rad_angB = float(240)*np.pi/180
rad_angC = float(120)*np.pi/180

A = (np.sqrt(2)*float(127))*np.sin(wt+rad_angA)
B = (np.sqrt(2)*float(127))*np.sin(wt+rad_angB)
C = (np.sqrt(2)*float(127))*np.sin(wt+rad_angC)

alpha, beta, z = ClarkePark.abc_to_alphaBeta0(A,B,C)
```

Graficando se obtiene las señales de tensión (A, B, C)

![ABC](https://i.ibb.co/59wxgbm/02.jpg)



Graficando el marco de referencia (α, *β*)

<img src="https://i.ibb.co/7KSKL1F/01.jpg" alt="Clark" style="zoom:93%;" />



## Transformación (ABC) - (dq0)

La transformación del marco ABC al sistema de referencia dq0, implementando la misma señal se obtiene con

```python
d, q, z = ClarkePark.abc_to_dq0(A, B, C, wt, delta)
```

Un sistema rotatorio puede ser analizado con la transformación de Park generándose dos señales de valor constante  en régimen permanente.

<img src="https://i.ibb.co/qFMxWg1/03.jpg" alt="dq0" style="zoom:100%;" />

## Transformación inversa (dq0) - (ABC)

La transformación inversa de Park, ejes de referencia rotatorio dq0 a componentes  del dominio del tiempo, marco A, B, C.

```python
a, b, c = ClarkePark.dq0_to_abc(d, q, z, wt, delta)
```

## Transformación inversa (α, *β*) - (dq0)

La transformación inversa de Park, ejes de referencia rotatorio dq0 a componentes  del dominio del tiempo, marco A, B, C.

```python
d, q, z= ClarkePark.alphaBeta0_to_dq0(alpha, beta, zero, wt, delta)
```



## Referencias

[1] Kundur, P. (1994). *Power System Stability and Control.* McGraw-Hill Education.

[2]  J.C.DAS. (2016). *Understanding Symmetrical Components for Power System Modeling.* Piscataway: IEEE Press Editorial Board.

 

