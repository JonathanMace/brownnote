On Numerical Issues for the Wave/Finite Element Method

Y. Waki, B.R. Mace and M.J. Brennan

ISVR Technical Memorandum No 964

December 2006

SCIENTIFIC PUBLICATIONS BY THE ISVR

Technical Reports are published to promote timely dissemination of research results
by ISVR personnel.  This medium permits more detailed presentation than is usually
acceptable  for  scientific  journals.    Responsibility  for  both  the  content  and  any
opinions expressed rests entirely with the author(s).

Technical  Memoranda  are  produced  to  enable  the  early  or  preliminary  release  of
information  by  ISVR  personnel  where  such  release  is  deemed  to  the  appropriate.
Information  contained  in  these  memoranda  may  be  incomplete,  or  form  part  of  a
continuing  programme;  this  should  be  borne  in  mind  when  using  or  quoting  from
these documents.

Contract Reports are produced to record the results of scientific work carried out for
sponsors,  under  contract.    The  ISVR  treats  these  reports  as  confidential  to  sponsors
and does not make them available for general circulation.  Individual sponsors may,
however, authorize subsequent release of the material.

COPYRIGHT NOTICE

(c) ISVR University of Southampton        All rights reserved.

ISVR  authorises  you  to  view  and  download  the  Materials  at  this  Web  site  ("Site")
only  for  your  personal,  non-commercial  use.    This  authorization  is  not  a  transfer  of
title  in  the  Materials  and  copies  of  the  Materials  and  is  subject  to  the  following
restrictions:  1)  you  must  retain,  on  all  copies  of  the  Materials  downloaded,  all
copyright  and  other  proprietary  notices  contained  in  the  Materials;  2)  you  may  not
modify  the  Materials  in  any  way  or  reproduce  or  publicly  display,  perform,  or
distribute  or  otherwise  use  them  for  any  public  or  commercial  purpose;  and  3)  you
must  not  transfer  the  Materials  to  any  other  person  unless  you  give  them  notice  of,
and they agree to accept, the obligations arising under these terms and conditions of
use.  You agree to abide by all additional restrictions displayed on the Site as it may
be  updated  from  time  to  time.    This  Site,  including  all  Materials,  is  protected  by
worldwide  copyright  laws  and  treaty  provisions.    You  agree  to  comply  with  all
copyright  laws  worldwide  in  your  use  of  this  Site  and  to  prevent  any  unauthorised
copying of the Materials.

UNIVERSITY OF SOUTHAMPTON

INSTITUTE OF SOUND AND VIBRATION RESEARCH

DYNAMICS GROUP

On Numerical Issues for the Wave/Finite
Element Method

by

Y. Waki, B.R. Mace and M.J. Brennan

ISVR Technical Memorandum No: 964

December 2006

Authorised for issue by
Professor M.J. Brennan
Group Chairman

© Institute of Sound & Vibration Research

 TABLE OF CONTENTS

ABSTRACT

1. INTRODUCTION ………………………………………………………………………... 1

1.1 Introduction ……………………………………………………………...……….. 1

1.2 Overview of Periodic Structure Analysis …………………………………..…….. 1

1.3 Outline of the Report ……………………………………………………………... 2

2. OVERVIEW OF WAVEGUIDE FINITE ELEMENT METHOD …………………… 3

2.1 Introduction ………………………………………………………………………. 3

2.2 Finite Element Formulation of a Structural Element …………………………….. 3

2.3 Wave Basis ……………………………………………………………………….. 4

2.3.1 Transfer Matrix ………………………………………………………….. 5

2.3.2 Eigenvalues and Eigenvectors …………………………………………... 5

2.4 Group Velocity …………………………………………………………………… 6

3. NUMERICAL ISSUES AND IMLEMENTATION …………………………………… 8

3.1 Introduction ………………………………………………………………………. 8

3.2 Conditioning of the Eigenvalue Problem ………………………………………… 8

3.2.1 Mathematical Background of Numerical Errors in the Eigenvalue

          Problem ………………………………………………………………... 8

3.2.2 Overview of the Conditioning for the Eigenvalue Problem …………...10

3.2.3 Zhong’s Method and Practical Implementation ………………………. 10

3.2.4 Application of SVD for Determination of Eigenvectors ……………... 12

3.3  Numerical  Errors  in  the  WFE  Method  ………………………………………...  13

3.3.1 Errors in the Conditioned Eigenvalue Problem ………………………. 14

3.3.2 FE Discretisation Error ……………………………………………….. 14

3.2.3 Round-Off Errors in the Dynamic Stiffness Matrix …………………... 14

4. NUMERICAL EXAMPLES OF A ROD AND A BEAM ……………………………. 16

4.1 Introduction ……………………………………………………………………... 16

4.2 Quasi-Longitudinal Waves in a Rod ……………………………………………. 16

4.2.1 Discretisation of a Rod Element ……………………………………… 16

4.2.2 Analytical Expressions for the Eigenvalues and Eigenvectors ……….. 17

4.2.3 Relative Errors in the Eigenvalues and Eigenvectors ………………… 18

4.2.4 Relative Errors in the Group Velocity ………………………………... 19

4.3 Flexural Waves in an Euler-Bernoulli Beam …………………………………… 20

4.3.1 Analytical Expression for the Discretised Beam Element ……………. 20

4.3.2 Relative Errors in the Eigenvalues and Eigenvectors ………………… 23

4.3.3 Relative Errors in the Group Velocity ………………………………... 26

5. NUMERICAL EXAMPLE OF A PLATE STRIP …………………………………… 28

5.1  Introduction  ……………………………………………………………………..  28

5.2 Analytical Expression for Flexural Waves in a Plate …………………………... 28

5.3 Flexural Waves in a Plate Strip Using the WFE Method ………………………. 29

5.3.1 The WFE Formulation ………………………………………………... 29

5.3.2 Results Using the Transfer Matrix ……………………………………. 29

5.3.3 Relationship between the Condition Number and Matrix Size ………. 32

5.3.4 Relative Errors in the Eigenvalues and Eigenvectors ………………… 34

5.3.5 Reducing Numerical Errors Using a FE Model with Internal Nodes … 38

5.3.6 Condensation Using Approximate Expressions ………………………. 42

5.3.7 Relative Errors in the Group Velocity ………………………………... 45

6. CONCLUSIONS AND DISCUSSION ………………………………………………… 47

6.1 Concluding Remarks ……………………………………………………………. 47

References

ABSTRACT

    The  waveguide  finite  element  (WFE)  method  is  a  numerical  method  to  investigate  wave

motion  in  a  uniform  waveguide.  Numerical  issues  for  the  WFE  method  are  specifically

illustrated in this report. The method starts from finite element mass and stiffness matrices of

only  one  element  of  the  section  of  the  waveguide.  The  matrices  may  be  derived  from

commercial  FE  software  such  that  existing  element  libraries  can  be  used  to  model  complex

general structures. The transfer matrix, and hence the eigenvalue problem, is formed from the

dynamic  stiffness  matrix  in  conjunction  with  a  periodicity  condition.  The  results  of  the

eigenvalue  problem  represent  the  free  wave  characteristics  in  the  waveguide.  This  report

concerns numerical errors occurring in the WFE results and proposing approaches to improve

the errors.

    In  the  WFE  method, numerical errors  arise because of (1) the FE discretisation error, (2)

round-off  errors  due  to  the  inertia  term  and  (3)  ill-conditioning.  The  FE  discretisation  error

becomes  large  when  element  length  becomes  large  enough  compared  to  the  wavelength.

However, the round-off error due to the inertia term becomes large for small element lengths

when  the  dynamic  stiffness  matrix  is  formed.  This  tendency  is  illustrated  by  numerical

examples for one-dimensional structures.

    Ill-conditioning occurs when the eigenvalue problem is formed and solved and the resulting

errors  can  become  large,  especially  for  complex  structures.  Zhong’s  method  is  used  to

improve  the  conditioning  of  the  eigenvalue  problem  in  this  report.  Errors  in  the  eigenvalue

problem  are  first  mathematically  discussed  and  Zhong’s  method  validated.  In  addition,

singular  value  decomposition  is  proposed  to  reduce  errors  in  numerically  determining  the

eigenvectors.  For  waveguides  with  a  one-dimensional  cross-section,  the  effect  of  the  aspect

ratio of the elements on the conditioning is also illustrated. For general structures, there is a

crude trade-off between the conditioning, the FE discretisation error and the round-off error

due to the inertia term. To alleviate the trade-off, the model with internal nodes is applied. At

low  frequencies,  the  approximate  condensation  formulation  is  derived  and  significant  error

reduction in the force eigenvector components is observed.

    Three approaches to numerically calculate the group velocity are compared and the finite

difference  and  the  power  and  energy  relationship  are  shown  to  be  efficient  approaches  for

general structures.

1. INTRODUCTION

1.1 Introduction

The  waveguide  finite  element  (WFE)  method  is  a  useful  method  when  the  dynamic

behaviour of a uniform structure is of concern. The method involves the reformulation of the

dynamic stiffness matrix, which includes the mass and stiffness matrices of  a section of the

structure,  into  the  transfer  matrix.  Structural  wave  motion  is  expressed  in  terms  of  the

eigenvalues and the eigenvectors of this matrix and these represent the wavenumbers and the

wave modes respectively. However, several numerical difficulties arise when the problem is

reformulated from a conventional finite element (FE) model. The aim of this report is (1) to

identify and quantify the potential numerical problems and (2) to suggest alternative ways of

determining the wave properties of a structure such that the numerical errors are reduced.

1.2 Overview of Periodic Structure Analysis

Many  structures  have  uniformity  or  periodicity  in  certain  directions.  To  analyse  such

structures,  Floquet  theory  [1],  which  is  one  of  the  basic  theories  of  wave  propagation  in

periodic structures, or the transfer matrix method e.g. [2] can be used. The basic idea is that

the  propagation  properties  of  waves  in  a  periodic  structure  can  be  obtained  from  the

propagation  constants  or  by  the  transfer  matrix.  Although  most  of  the  early  papers  give  the

analytical dispersion relationship for relatively simple structures [3,4], numerical calculation

is generally needed for complex structures. For complex structures, the finite element method

(FEM)  may be  applied  to  calculate  the propagation  constants  [5,6,7].  The  transfer  matrix  is

formed from the mass and stiffness matrices of discretised elements and the wave propagation

characteristics are then described by the eigenvalues and eigenvectors of the transfer matrix.

The  WFE  method  is  based  on  this  idea  and  several  applications  can  be  found  in  the

literature. Early work  can be found in [8] which investigated the propagation and stop band

for  periodic  structures  consisted  from  a  beam  and  a  plate.  The  forced  response  to  random

pressure fields was also presented. Thompson [9] and Gry et al [10,11] applied the method to

analyse railway vibration, and Houillon et al [12] investigated wave motion in a general thin-

shell structure. Duhamel et al [13] and Mace  et  al [14] discussed the  accuracy  of numerical

1

results  for  simple  structures  and  Hinke  et  al  [15]  analysed  wave  properties  in  a  sandwich

panel.  Mencik  [16]  formulated  the  problem  of  wave  coupling  between  two  general

substructures and Maess [17] analysed a fluid filled pipe using an eigenpath analysis. One of

the  advantages  of  the  WFE  method  is  the  computational  cost  [18]  since  this  method  needs

information  drawn  from  only  one  small  section  along  the  direction  which  the  waves

propagate.  Another  possible  way  of  analysing  such  structures  is  the  spectral  finite  element

method [19] which uses a special shape function to represent the motion of a cross-section of

the structure. However, this method needs special shape functions and element matrices to be

developed for different wave types.

The  WFE  method  needs  only  the  conventional  mass  and  stiffness  matrices  of  a  structure.

Since the standard FE-package can be utilised to generate the stiffness and mass matrices, the

full  power  of  existing  element  libraries  can  be  employed.  In  addition,  since  the  wave

characteristics are calculated for a given frequency, nearfield and oscillating decaying waves,

which  might  be  important  for  the  system  response  near  excitation  points  or  discontinuities,

can be effectively included. The forced response can be calculated using the wave approach

(e.g. [20]).

1.3 Outline of the Report

The  wave  motion  could  be  derived  from  the  eigenvalues  and  eigenvectors  of  the  transfer

matrix.  However,  numerical  difficulties  may  be  encountered  when  solving  the  eigenvalue

problem.  Most  papers  mention  the  matrix  conditioning  of  the  eigenvalue  problem

[9,10,11,13,14,17] but do not discuss many details.

In this report, only free wave propagation is described and, in particular, numerical issues

are  discussed.  First,  the  WFE  formulation  is  briefly  introduced  and  the  conditioning  of  the

eigenvalue problem is described. The application of the singular value decomposition (SVD)

to  determine  the  eigenvectors  is  proposed.  Numerical  errors  in  the  eigenvalue  problem  are

mathematically discussed and potential errors in the WFE method are enumerated. Numerical

examples  are  presented  for  simple  waveguides  where  the  analytical  solutions  are  available.

The  accuracy  and  validity  of  the  results  using  different  algorithms  and  FE  models  are  also

discussed. All calculations are performed in MATLAB. Finally some conclusions are drawn.

2

2. OVERVIEW OF THE WAVEGUIDE FINITE

ELEMENT METHOD

2.1 Introduction

    In  this  section,  a  brief  overview  of  the  WFE  formulation  is  given.  A  small  section  of  a

structure  is  first  modelled  using  FE.  From  the  dynamic  stiffness  matrix  of  the  elements  the

transfer matrix is formed. The transfer matrix describes the wave motion through the element

and  the  eigenvalues  and  the  eigenvectors  of  the  resulting  eigenvalue  problem  represent  the

wavenumbers and the wave modes in the structure.

2.2 Finite Element Formulation of a Structural Element

    The equation of motion for uniform structural waveguides can be expressed as

(cid:1)
Mq Cq Kq f

(cid:1)(cid:1)

=

+

+

(2.1)

where M, K, and C are the mass, stiffness and damping matrices respectively, f represents the

loading  vector  and  q  is  the  vector  of  the  nodal  displacement  degrees  of  freedom  (DOFs).

Throughout this report, time harmonic motion

j

te ω  is implicit. Equation (2.1) then becomes

Dq

(
= −

2
ω

M

+

j
ω

)
C K q f

=

+

(2.2)

where  D  is  the  dynamic  stiffness  matrix.  The  nodal  forces  and  DOFs  are  decomposed  into

sets  associated  with  the  left  (L),  right  (R)  cross-section  and  interior  (I)  nodes.  For  the  case

where there are no external forces on the interior nodes, equation (2.2) can be partitioned into

D

LL

D

LR

D
D

RL

IL

D
D

RR

IR







D

LI

D
RI
D

II

q

q
q

 
 
 
 
 

L

R

I







=

f

L

f
R
0













which may be expressed as





D
D

MM

IM

D
D

MI

II

 
 
 

q
M
q

I





=

f
M
0









(2.3)

(2.4)

where  the  subscript  M  represents  master  nodes  containing  the  left  and  right  cross-section

nodes. The second row of equation (2.4) leads to

3

such that

q

I

= −

D D q
IM M

−
1
II

q
M
q

I









=

I
1
−
D D
II

−





IM





q

M

=

Rq

M

(2.5)

(2.6)

where I is the identity matrix. Using the matrix R in equation (2.6), equation (2.4) becomes

T

R





D
D

MM

IM

D
D

MI

II

Rq

M

=

f

M

.





Expanding equation (2.7) leads to

D




MM

−

D D D

MI

1
−
II

q




M

IM

=

f

M

(2.7)

(2.8)

such that DOFs associated with internal nodes can be eliminated.

    If the group velocity is calculated from the power flow and energy relationship stated later

in  this  section,  the  form  of  equation  (2.7)  is  useful  to  derive  the  reduced

,M K  and  C

matrices.  Putting  these  matrices  instead  of  D  into  equation  (2.7)  readily  gives  the  reduced

matrices. The reduced mass matrix is, for example,

T

R MR M

=

−

MM

−
D D M M D D

1
−
II

+

IM

D D M D D .
II

MI

IM

1
−
II

1
−
II

1
−
II

IM

MI

MI

    After removing internal DOFs, equation (2.2) for the section can be written as

D
D





LL

RL

D
D

LR

RR

q
q

 
 
 

L

R





=

f
f





L

R





.

For a uniform section, the following relationships hold:

and

D

T
LL

=

D

,

LL

D

T
RR

=

D

,

RR

D

T
LR

=

D
RL

D

RRij

=

sgn

⋅

D

LLij

,

D

RLij

=

sgn

⋅

D

LRij

(2.9)

(2.10)

(2.11)

(2.12)

where  T⋅

 indicates the transpose and the signs in equations (2.12) depend on whether DOFs

at the element interface are symmetric or anti-symmetric [9].

2.3 Wave Basis

    Wave propagation can be described by the transfer matrix. The transfer matrix, hence the

eigenvalue  problem,  can  be  formulated  from  the  dynamic  stiffness  matrix.  The  eigenvalues

and eigenvectors represent the wavenumbers and the wave mode shapes.

4

2.3.1 Transfer Matrix

The transfer matrix can be defined on the basis of the continuity of displacements and the

equilibrium of forces of adjacent elements as [1]

L

T





q
f

L

=









q

R
−
f


R

(2.13)

where  T  is  the  transfer  matrix.  The  transfer  matrix  can  be  formed  from  the  elements  of  the

dynamic stiffness matrix as [13]

T


= 


−

D

1
−
D D
−
LR
LL
1
−
+
D D D
LR

RR

RL

1
−
D
LR
D D
RR

−

1
−
LR





.

LL

(2.14)

From a periodicity condition [1], free wave motion over the element length  ∆  is described in

the form of an eigenvalue problem such that

T

q
 
 
f
 

=

λ

q
 
 
f
 

.

 (2.15)

Although equation (2.15) formulates the basic principle for the WFE method, this eigenvalue

problem is likely to be ill-conditioned for general problems because of the ill-conditioning of

LRD  and  the  fact  that  the  elements  of  the  eigenvector  range  over  a  large  magnitude.  The

conditioning of the eigenvalue problem is described in Section 3.

2.3.2 Eigenvalues and Eigenvectors

The eigenvalues

iλ in equation (2.15) relate to wave propagation over the distance  ∆  such

that [1]

eλ −
=

i

ijk

∆

(2.16)

where

ik  represents  the  wavenumber  for  the  ith  wave.  The  wavenumber  can  be  purely  real,

purely  imaginary  or  complex,  associated  with  a  propagating,  a  nearfield  (evanescent)  or

oscillating  decaying  wave  respectively.  The  eigenvector  corresponding  to  the ith  eigenvalue

can be expressed as

Φ

i


= 


q

i

f

i





.

(2.17)

The  eigenvector  represents  a  wave  mode  and  contains  information  about  both  the

displacements  and  the  internal  forces.  For  uniform  waveguides,  there  exist  positive  and

negative  going  wave  pairs  in  the  form  of

eλ ±
± =
i

ijk

∆

 and  the  eigenvalues  and  associated

5

eigenvectors  are  expressed  as  (

iλ +Φ  and  (
)
1
,i

iλ −Φ .  Positive-going  waves  are  those  for
,i

)

which the magnitude of  the eigenvalues is less than 1, i.e.

iλ <  or if
1

iλ = , such that the

1

power  is  positive  going,  i.e.

Re

}
{
(cid:1)
H
f q

{
Im
ω=

}
H
f q

>

0

 [13,14]  where  H⋅

 represents  the

complex conjugate transpose or Hermitian.

2.4 Group Velocity

The group velocity is the velocity at which the wave propagates. The group velocity for the

ith wave is defined by (e.g. [21])

c

gi

=

ω∂
∂
k
i

.

(2.18)

There are several approaches to the numerical calculation of the group velocity.

    The finite difference method calculates the group velocity from a first order approximation

as

c

( )
n
gi

=

n

)
1
−

(

n

)
(
1
ω ω+
)
(
1
+
k
k
i

−
−

(
i

n

)
1
−

(2.19)

n

where n-1, n, n+1 are consecutive discrete frequencies. Other definitions for equation (2.19)

are  possible.  Once  the  dispersion  relationship  is  determined,  the  group  velocity  can  be

obtained.

    Another approach for the group velocity is in terms of the power and energy as [21]

c

gi

=

P
i
E

tot i
,

(2.20)

where  P  is  the  time  average  power  transmission  thorough  the  cross  section  of  a  waveguide

and Etot is the total energy density. These values are given by [14,21]

P
i

=

1
2

Re

{
(cid:1)
H
f q
i

i

}

=

ω
2

Im

{
H
f q
i

i

}

.

and

E

tot i
,

=

E

k i
,

+

E

,

p i
,

E

,
k i

=

1
∆
4

Re

{
(cid:1)
(cid:1)
H
q Mq
i

i

}

= −

2
ω
∆
4

Re

{
H
q Mq
i

i

}

,

E

,
p i

=

1
∆
4

Re

{
H
q Kq
i

i

}

(2.21)

(2.22)

where  Ek,i  and  Ep,i  represent  the  kinetic  and  potential  energy  densities  for  the  ith  wave.  The

dissipated power follows from the imaginary part of K and/or the damping matrix C.

6

In  addition,  the  group  velocity  could  be  determined  directly  by  differentiating  the

eigenproblem [22]. The group velocity can be expressed as

c

gi

=

ω
∂
∂
k
i

=

1
2
ω

2
ω
∂
∂
k
i

(2.23)

and

2
k ω∂ ∂

 is found from the differentiation of the eigenvalue problem (2.15) such that

∂
(
2
ω

)

∂

{
(

T

−

)
iλ
I Φ

}

=

0 .

(2.24)

Expanding  equation  (2.24),  using  equations  (2.16),  (2.23)  and  premultiplying  by  the  left

eigenvector

iΨ  leads to

Ψ

i




∂

∂
)2
(
ω

T

+

j
∆
i
λ
i
ω ω
2

k
∂
∂



I Φ



=

0

.

i

(2.25)

Recalling  equation  (2.14),  noting

the  differentiation  of

the  matrix

inverse  [23],

∂
(
2
ω

)

∂

D

1
−
LR

= −

D M D ,
LR

1
−
LR

1
−
LR

)2ω∂
(
∂T

 in equation (2.25) can be evaluated as

∂
(
2
ω

)

∂

T

=







−

1
−
LR

1
−
LR

D M D D
LR
−

M M D D

+

LL

1
−
LR

1
−
D M
LR
+

LL

D M D

1
−
LR

LR

1
−
LR

RL
D D M D D

RR

1
−
LR

1
−
LR

RR

LR

−

LL

LL
1
−
D D M
LR

RR

M D
RR

1
−
LR

−

LL

1
−
D D M D
LR

RR

LR

From the above equations the group velocity is given by

c

gi

= −

j
λ
∆
i
2
ω

Ψ

i

Ψ IΦ
i
∂
)2
(
ω

∂

i

.

TΦ

i







1
−
LR

.

(2.26)

(2.27)

    Three  formulations  of  the  group  velocity  have  been  introduced.  The  accuracy  of  each

approach is discussed later in this report.

7

3. NUMERICAL ISSUES AND

IMPLEMENTATION

3.1 Introduction

    In this section, the conditioning of the eigenvalue problem is illustrated. Numerical errors

occurring  in  the  eigenvalue  problem  are  mathematically  explained  and  the  conditioned

eigenvalue  problem  is  introduced.  In  particular,  the  singular  value  decomposition  (SVD)  is

applied to reduce errors for numerically determining the eigenvectors. Numerical errors in the

WFE method are then enumerated.

3.2 Conditioning of the Eigenvalue Problem

    The  eigenvalue  problem  was  formulated  using  the  transfer  matrix  (2.15).  However,  the

results  from  the  eigenvalue  problem  might  be  inaccurate.  In  this  section  the  conditioned

eigenvalue  problem  is  introduced  and  SVD  application  is  proposed  to  reduce  numerical

inaccuracies for determining the eigenvectors.

3.2.1  Mathematical  Background  of  Numerical  Errors  in  the

Eigenvalue Problem

    Numerical  errors  occur  (1)  when  the  eigenvalue  problem  is  formulated  and  (2)  when  the

eigenvalue problem is solved. When the eigenvalue problem (2.14) is formulated, numerical

errors can arise predominantly from the matrix inversion. The maximum resulting errors for

the  matrix  inversion

1−A  can  be  of  the  order  of

and

ε κ⋅ A  where ε is  the  machine  precision

(

)

(
κ

A

)

=

A A

1
−

=

σ σ
max

min

(3.1)

is  the  condition  number  [24],

⋅

 is  the  2-norm  and,  maxσ  and  minσ  are  the  largest  and

smallest  singular  values.  For  general  matrices,  the  matrix  can  be  ill-conditioned  if  there  are

comparatively  large  numbers  on  the  off-diagonal  elements,  e.g.[24,25].  When  the  transfer

8

matrix  approach  (2.15)  is  formed,

−D  should  be  calculated  which  in  general  might  be  ill-

1
LR

conditioned. This causes numerical errors when the eigenvalue problem is formed.

    Next,  numerical  errors  occurring  in  the  solution  of  the  eigenproblem  are  discussed.  The

matrix for the eigenvalue problem in the WFE method is square, complex and non-symmetric.

For such matrix Schur factorisation is known to be most useful in numerical analysis because

all  matrices,  including  defective  ones,  can  be  factored  in  this  way  [24].  Major  software

packages  such  as  MATLAB  and  Mathematica  use  Schur  factorisation  for  solving  such

eigenvalue problems.

    Many different approaches for assessing the error bounds on the computed eigenvalues and

eigenvectors have been proposed, e.g. [26,27]. A well-known estimate for the error bound is

given  by  Gerschgorin’s  theorem  [24].  However,  this  theorem  usually  gives  a  large  error

bound for an ill-conditioned matrix. More precisely, the following discussion holds for Schur

factorisation [25].

    When  the  eigenvalue  problem

λ=AΦ Φ  or

factorisation, the matrix A is factorised into the form

H

Hλ=Ψ A

Ψ  is  solved  using  Schur

H

Q AQ D N  where  Q  is unitary,  D

=

+

is  diagonal  and  N  is  strictly  upper-triangular  [25].  The  resulting  errors  for  the  eigenvalue

problem are estimated from

)κ Q  or  N  [25]. If

(

)κ Q  is large then the eigenvector matrix

(

is  ill-conditioned.  If  the  eigenvectors  are  far  from  orthogonal  to  each  other,  the  results  may

contain  large  errors  [24,25].  Since  the  eigenvectors  in  the  transfer  matrix  approach  (2.15)

contains both the displacement and force components and usually each eigenvector is far from

orthogonal to each other,

)κ Q  is likely to be issue for general cases. A large value for  N

(

means  that  A  is  far  from  normal,  e.g.  strongly  asymmetric  [25].  Such  eigenvalue  problems

are  likely  to  have  a  large  error  in  the  computed  results,  which  is  the  case  for  the  transfer

matrix approach stated in equation (2.14).

    Specifically, for

5n ≥  for the  n n×  matrix A, there is no analytical expression for the roots

of the characteristic polynomial so that the eigensolver must be iterative [24]. For a matrix of

large  size,  conditioning  becomes  more  important  for  errors  when  Schur  factorisation  is

applied to solve the eigenvalue problem. In this report, the matrix size for a rod and a beam is

n =

2, 4

 respectively  such  that  conditioning  effects  are  small.  However,  the  conditioning

becomes important for a plate example as the matrix size becomes large.

    It  is  worth  noting  that  if  the  eigenvalue  problem  is  ill-conditioned,  complex  conjugate

eigenvalues occur as numerical artefacts [25] if

9

Ε

A

≤

1
)2

(
s λ
i

−

1

(3.2)

where  Ε  is  the  perturbation  matrix  incurred  from  the  round-off  error  because  of  the  finite

digit arithmetic and

(
s λ  is the sensitivity of the eigenvalue with respect to the perturbation,

)i

given by [25]

(
s λ
i

)

=

1

H

Ψ

(
λ
i

)

Φ

(
λ
i

)

(

≥

)
1

with

Φ

i

=

Ψ

i

=

1

.  Under  the  condition  (3.2),  two  distinct  but  similar  eigenvalues

(3.3)

jλ λ
,i

become  repeated  eigenvalues

'

'

jλ λ  whose  values  are  different  from  both

,i

iλ  and

jλ  [25].

Examples using  MATLAB eigenvalue solvers can be found in [28,29].

3.2.2 Overview of the Conditioning for the Eigenvalue Problem

    To  improve  the  ill-conditioned  problem  (2.15),  several  works  [10,13,14,15,16]  applied

Zhong’s  algorithm  [30].  The  details  can  be  seen  in  [30,31,32].  This  method  formulates  the

conditioned, general eigenvalue problem such that

LRD  is not necessarily inverted. In addition,

since  the  eigenvector  contains  only  displacement  components,  numerical  error  could  be

reduced  because

)κ Q  can  be  smaller.  Thompson  [9]  also  derived  the  similar  eigenvalue

(

problem using symmetric relationships, e.g. equations (2.11), (2.12), which results in smaller

size of the eigenvalue problem.

    In  this  report,  Zhong’s  algorithm  has  been  applied  because  the  approach  seems  well

matched with the problems which have been considered so far.

3.2.3 Zhong’s Method and Practical Implementation

    Zhong’s method [30] is illustrated in this section. The method starts from a reformulation

of equation (2.13) into the relationships for the displacement vectors alone:

q
f





L

L

=





I
D





n

LL

0
D

LR

q
q

 
 
 

L

R





,





q
f

R

R

=





0
D

−





RL

I
n
D

RR

q
q

 
 
 

L

R





.

−

(3.4)

After some matrix operations using the periodicity condition and the symplectic relationship

[30], equations (3.4) can be rearranged as

−

RL

−

D
0





−
D
LL
−
D

RL

D

RR

q
L
λ
q

 
 
 

L





=


λ



0
D

−

RL

D
LR
0

q
L
λ
q

 
 
 

L

,





(3.5)

10

and





D

D
LR
+

D

RR

0
D

LR

LL

q
L
q
λ

 
 
 

L





=

1
λ





0
D

−

RL

D
LR
0

q
L
q
λ

 
 
 

L

.





Adding equations (3.5) and (3.6) gives the general eigenvalue problem:

µ
Z
1

q



λ
q






=

Z

2

q



λ
q






with

Z
1

=



−

0

D

RL

D

LR
0

,





Z

2


= 


(
(

D
D

LR

LL

−
+

D
D

RL

RR

)
)

−
(

LL

(
D
D

LR

D
+
−
D

RR

)

RL

(3.6)

(3.7)

(3.8)

)





where

µ λ λ
= +

1

 and  the  subscript  L  for  the  eigenvector  is  suppressed  for  clarity.  For

symmetric  elements,  several  elements  of

2Z  in  equation  (3.7)  cancel  each  other  as  certain

relationships (2.11), (2.12) hold and

1Z  and

2Z  in equation (3.7) become skew-symmetric.

    In  practice,  it  is  recommended  that  either

1Z  or

2Z  is  inverted  such  that  the  standard

eigenvalue problem

q


µ

q
λ






=

−
1
Z Z
1

2

q



q
λ






  or

1
µ

q



q
λ






=

−
1
Z Z
2
1

q



q
λ






(3.9)

is  formulated.  To  reduce  numerical  errors,  the  matrix  with  the  smaller  condition  number

should  be  inverted  [33]. In  addition,  the  pseudo  matrix  inverse  (e.g.  [24])  can  be  applied  to

reduce numerical errors.

    One might be interested in only several waves with small wavenumbers. A limiting case is

when  a  wave  is  at  the  cut-off  frequency  (usually

k → )  such  that  usually

0

µ λ λ

= + → .

2

1

In such cases, it is beneficial to take the form of

2µ−  (

or 1

0.5µ−

)

 rather than  µ (

)
1 µ  in

equations  (3.9)  such  that  the  important  eigenvalues  can  be  bounded  by  several  smallest

(largest) values.

    Equations (3.9) are a standard, double eigenvalue problem whose eigenvectors contain only

the  displacement  components.  The  original  eigenvalues

iλ λ  can  be  determined  from  the
,1i

calculated  eigenvalue

µ λ λ
i
i

+

=

1

i

 by  solving  the  quadratic  equation  or  by  using  a

trigonometric function of the form

µ λ λ −
1
+
e

=

=

i

i

jk

i

∆

jk

i

∆

+

e

=

2 cos

(

k
i

)
∆ .

    There  are  two  independent  eigenvectors

which are given by

,φ φ  associated  with  the  double  eigenvalues,

2

i

1

11

φ

1,2

q

1,2
= 
1,2λ
q






.

(3.10)

The  original  eigenvector  associated  with  eigenvalues

iλ λ  can  be  found  from  a  linear
,1i

combination of

,φ φ  [13,14,30], i.e.,

1

2

φ

=

q



q
λ






=

α α
2

φ
1 1

+

φ

2

.

Substituting equations (3.11) and (3.10) into equation (3.5) gives

−



λ


D

D

RL

RL

−

D

LL

−

D

−

λ

D

LR

RR
D

RL

−







α

1



q

1

λ
q

1





+

α
2

q


2

λ
q


2











=

0

.

(3.11)

(3.12)

Taking the scalar product of  H

1φ  leads to the relationship between

1α  and

2α  such that [13]

α
2
α
1

= −

H
q
1




H
q
λ
1

H
q
1




H
q
λ
1

−

D

LL

−

D

LL

−

D


 

D
λ

−
D

 

λ


D

RL

RL

RL

RL

RR
D
−
D

RR
D

−

RL

RL
−

−

−

D

−

λ

D

LR

λ

D

LR

q
1
q
λ
1
q

2
q
λ

 
 
 
 
 
 

2

.








(3.13)

Although  equation  (3.13)  is  algebraically  correct,  there  may  be  some  difficulties  when

calculating  it  numerically.  In  the  next  section,  an  alternative  way  of  determining  the

eigenvectors is investigated using singular value decomposition (SVD).

3.2.4 Application of SVD for Determination of Eigenvectors

    The  eigenvectors  could  be  obtained  from  equation  (3.13)  but  numerical  problems  may

occur.  For  the  limiting  case

1λ→ ,  equation  (3.13)  approaches

errors during arithmetic calculations become large.

α α →  and  round-off

0 0

2

1

    Alternatively, SVD may be applied. Equation (3.12) can be written in another form as

−

D

LL

−


λ


D
D

RL

RL

−

λ

D

LR

D
−
RR
−
D

RL

 
 
 

α
q
q
2
1
1
λ λ α
q
q
2
1

 
 
 

2

=

0

.





(3.14)

Writing equation (3.14) as

A

[
2α α =

]T

1

0  with an

2n ×  rectangular matrix A, where n is the

length  of  the  eigenvector,  the  problem  is  now  to  solve  an  overdetermined  simultaneous

equation  if

3n ≥ .  SVD  can  be  applied  to  solve  an  overdetermined  linear  equation  [34].

Performing SVD on A gives

H
=A USV

(3.15)

12

where  the  matrix  dimensions  are

A

∈

(cid:2)

(

n

×

)
2 ,

U

∈

(cid:2)

(

×
n n

)

,

S

∈

(cid:3)

(

n

×

)
2 ,

V

∈

(cid:2)

(

2 2
×

)

.

Equation (3.15) can be written as

A

v
11
v
21





v
12
v
22





=

U

σ

1

0


0
(

≈

0

)

σ
ε

0

0

(cid:4)

(cid:4)

T

0

0





.

(3.16)

The matrix S contains two singular values on its leading diagonal and one of these is almost

zero. The second column of equation (3.16) and expanding A to the original expression gives

−

D

LL

−


λ


D
D

RL

RL

−

λ

D

LR

D
−
RR
−
D

RL

 
 
 

q
q
2
1
λ λ
q
q
1

2

 
 
 

v
12
v
22





≈

0

such that [

2α α  are given by

1

]T

α
2
α
1

=

v
22
v
21

.

(3.17)

(3.18)

The advantages of SVD approach are

(1) equation  (3.18)  can  be  derived  from  only  one  matrix  multiplication  while  equation

(3.13)  needs  two  multiplications  for  both  the  denominator  and  numerator  such  that

numerical errors through the matrix operations can be reduced and,

(2) the  orders  of

,v
21

v  in  equation  (3.18)  are  typically
22

( )1O  while  that  of  the  original

values

,α α  in equation (3.13) may be very small.

1

2

    After  finding  the  vector  of  displacements  from  equations  (3.11)  and  (3.18),  the

corresponding force eigenvector can be calculated from the first row of equation (2.15) as

The original right eigenvector associated with

iλ is then

f

=

(

D

LL

+

LRλ

)
D q .

=
Φ Φ

i

(
λ
i

)

=

q
f





(
)
λ
i
)
(
λ
i





=





(

D

LL

+

(
)
q
λ
i
)
λ
D q
i
LR

.





(
λ
i

)

Similarly, the original left eigenvector can be obtained as [13]

Ψ Ψ
=

i

(
λ
i

)

=





q

(
1

λ
i

T

) (

D

RR

+

λ
i

D

LR

)

q

(
1

λ
i

)

T

.





(3.19)

(3.20)

(3.21)

3.3 Numerical Errors in the WFE Method

    Even  if  the  conditioned  eigenvalue  problem  is  solved,  numerical  errors  still  occur.  Errors

arising in the WFE method are enumerated and each is explained.

13

3.3.1 Errors in the Conditioned Eigenvalue Problem

The sequential procedure for the WFE method, based on the conditioned eigenvalue problem,

can be illustrated as follows. The damping matrix C is excluded for simplicity.

(1) Discretise a section of a structure of length  ∆  using FE such that K, M are formed.

(2) Calculate the dynamic stiffness matrix

D K

2ω=
−

M  for each frequency.

(3) Formulate the standard eigenvalue problem, i.e. equation (3.9).

(4) Solve the eigenvalue problem.

(5) Calculate the original eigenvalues and eigenvectors, i.e. equations (3.11) and (3.18).

(6) Calculate the force components from equation (3.20).

    For  steps  (3)-(5),  the  conditioning  is  essential  to  reduce  numerical  errors  for  a  matrix  of

large size. For step (1), the FE discretisation error should be first considered and specifically

for step (2), the round-off error can be important. Each error is explained.

3.3.2 FE Discretisation Error

    When  a  structure  is  discretised  using  FE,  FE  discretisation  errors  occur.  To  represent  the

system motion accurately, 6 or more FE are generally needed for each wavelength [35]. In the

WFE formula, this criterion can be expressed as [13]

k∆ ≤ .

1

(3.22)

Equation (3.22) should be satisfied both along the waveguide and over its cross-section.

    For accurate results, small  ∆  is needed for large wavenumbers. However, very small  ∆  is

inappropriate because the conditioning is likely to deteriorate and the round-off error due to

the  inertia  term  increases.  The  section  length  ∆  should  be  carefully  determined  when  the

structure is modelled. Examples will be shown in Sections 4 and 5.

3.3.2 Round-Off Errors in the Dynamic Stiffness Matrix

    The round-off errors occur in every numerical arithmetic operation. Specifically, this error

can be important when the dynamic stiffness matrix,

D K

2ω=
−

M , is numerically calculated.

The  error  becomes  large  when

2
M(cid:5)
ijωK

ij

 because  of  the  finite  precisions  of  arithmetic

operations.

    It  should  be  noted  that  the  criteria  where  the  round-off  errors  become  large  depends  not

only  on  ω  but  also  the  length  ∆ .  Small  ∆  increases

ijK  but  decreases

ijM  for  the

discretised elements. When significant effective digit numbers of the inertia term are rounded,

14

D  becomes  inaccurate  such  that  the  eigenvalue  problem  cannot  be  accurately  formed.  To

evaluate  the  round-off  error  due  to  the  inertia  term,

min

(

2

ω M K  may  be  a  indication

ii

)

ii

since  some  off-diagonal  terms  may  not  be  important.  To  reduce  this  error,  ∆  should  not  be

too small when the structure is modelled.

    To solve the compromise between the FE discretisation error and the round-off error due to

the  inertia,  condensation  using  internal  nodes  can  be  used.  If  a  structure  is  modelled  with

internal nodes and DOFs associated with the internal nodes are reduced using equation (2.7),

the round-off error could be reduced. A numerical example is shown in Section 5.

15

4. NUMERICAL EXAMPLES OF A ROD AND A

BEAM

4.1 Introduction

    The  quasi-longitudinal  waves  in  a  rod  and  flexural  waves  in  a  beam  are  considered.  The

accuracy of results calculated by the WFE method is discussed in this section. No damping is

assumed.

4.2 Quasi-Longitudinal Waves in a Rod

    The quasi-longitudinal waves in a rod are considered in this section. The WFE results are

compared with the analytical solution and the accuracies are evaluated.

4.2.1 Discretisation of a Rod Element

    The mass and stiffness matrices for the rod element can be modelled using a linear shape

function such that [35]

K

=

1

EA

−∆ 

1

−
1




1

,

M

=

Aρ 
∆

6


2 1

1 2





(4.1)

where E is the Young’s modulus, A is the cross-sectional area,  ρ is the mass density and  ∆  is

the length of a section. The dynamic stiffness matrix,

D K

2ω=
−

M , then becomes

D

=

EA
∆


1






−

(

k

2

)

∆
L
3

1
− −

(

k

2

)

∆
L
6

.
sym

1

−

(

k

2

)

∆
L
3








Lk

=

Eρ ω

(4.2)

(4.3)

where

is the quasi-longitudinal wavenumber [36]. The dynamic stiffness matrix in equation (4.2) is

accurate  for  the  analytical  dynamic  stiffness  matrix  [37]  up  to

{
(
LO k ∆

)

}2

 with  error  being

16

 for  small  Lk ∆ .  The  transfer  matrix  (2.14)  can  be  obtained  from  equation  (4.2)

)

}4

{
(
LO k ∆
[13] such that

T

=

1

1

+

(

k

2

)

∆
L
6









1

−

(

k

2

)

∆
L
3

(

2
)
∆ −

k

L


EA

(

∆ 


k

4

∆
)

L

12



−

∆
EA

1

−

(

k

2

)

∆

L
3

.









(4.4)

4.2.2 Analytical Expressions for the Eigenvalues and Eigenvectors

    The  analytical  solution  for  the  WFE  formulation  can  be  found  from  equation  (4.4).  The

eigenvalues are analytically given as [13]

λ±

=

1



1

)
∆ 

L
6

2

(

k

1

+

−

(

k

2

)

∆

L
3

∓

(
j k

L

∆

)

1

−

(

k

∆

L
12

2

)

.







(4.5)

For small  Lk ∆ , equation (4.5)can be expanded to

and this is accurate up to

λ±

=

1

∓

jk

L

∆ −

(

k

2

)

∆

L
2

5

±

j

{
(
LO k ∆

)

}2

 with error being

(

k

∆

3

)

L
24
{
(
LO k ∆

+

(cid:4)

(4.6)

)

}3

. It should be noted that the

error in the wavenumber given from

log

(
λ±

)

− = ∆  becomes from equation (4.6)

k

j

±

(

k

±

)

∆ = ± ∆ +
k

1

L






(

k

)2

∆

L
8


∓(cid:4)




(4.7)

such that relative error in the wavenumber is

{
(
LO k ∆
    The right eigenvectors associated with the eigenvalues (4.5) can be analytically obtained as

}2

.

)

±

Φ

=

u

f









=







1

∓

jEAk

1

−







)2

(

∆
k
L
12

(4.8)

where  u  is  the  longitudinal  displacement  and f  is  the  normal  force.  The  exact  solution  for  a

continuous rod is [36]

[

f u

± = ∓
]

jEAk

.

(4.9)

The force eigenvector per unit displacement in equation (4.8) can be simplified to

17

±

[

f u

]

WFE

=

∓

jEAk

{
1

−

(

k

L

∆

2

)

}
24

(4.10)

for small  Lk ∆  with the relative error being

{
(
LO k ∆

)

}2

.

4.2.3 Relative Errors in the Eigenvalues and Eigenvectors

    Figures  4.1,  4.2  show  the  relative  errors  in  the  wavenumber, (

k

−

k

)L

k

L

,  and  the  force

eigenvector  per  unit  displacement, (

f
WFE

−

f

)

f

,  respectively.  In  both  figures,  the  trend  of

the  curve  is  same.  The  relative  errors  increase  for

Lk

∆ > ⋅

3 10

−

4

 because  of  the  FE

discretisation  error  and,  for

Lk

∆ < ⋅

3 10

−
4

 because  of  the  round-off  errors  due  to  the  inertia

term. Although the size of the error is small for very small  Lk ∆ , it should be noted that not

only the magnitude but also the phase of the force eigenvector fluctuates such that the forced

response  of  the  system  will  fluctuate  because  of  the  numerical  errors.  When  the  forced

response  at  low  frequencies  is  of  concern,  length  of  the  element  ∆  should  be  chosen  as

enough large to reduce the round-off errors due to the inertia term.

    Asymptotic slopes in the relative errors at large  Lk ∆  and small  Lk ∆  are +20 dB/decade and

-20 dB/decade, respectively. For large  Lk ∆ , the asymptotic slope is about +20 dB/decade in

both  figures.  This  behaviour  can  be  explained  from  equations  (4.7)  for  the  wavenumber

(Figure 4.1) and equation (4.10) for the eigenvector (Figure 4.2).

    For  small

Lk ∆ ,  the  round-off  error  is  dominant  for  the  relative  errors  such  that  the

minimum  value  of

ω M K  is  of  concern  since  some  off-diagonal  terms  may  not  be

2

ii

ii

important  for  general  cases.  From  equations  (4.1),  it  is  given  that

min

(

2
ω

M K
ii

ii

)

=

1 3 Lk ∆ .  From  this  estimation,  the  round-off  error  due  to  the  inertia  term  is  related  to

(

)2

(

Lk

−∆
) 2

,  which  is  same  as  the  asymptotic  slope  in  the  relative  errors.  If  the  ratio  is  greater

than

1610  (

Lk

∆ <

−

)810

, all the inertia terms could be rounded in double precision calculation

as can be seen in the figures.

18

102

0
10

-2

10

10-4

-6

10

-8

10

|

L

k

/

L

)
k
-
k
(

|

-10

10

10-8

10-6

10-4
k
L∆

10-2

100

Figure 4.1: Relative error in the wavenumber: ····· asymptote  20dB decade

±

.

2
10

100

-2

10

-4

10

|

f

/

)
f
-

E
F
W

f
(

|

10-6

-8

10

10-10

10-8

10-6

10-4
k
L∆

10-2

100

Figure 4.2: Relative error in the eigenvector: ····· asymptote  20dB decade

±

.

4.2.4 Relative Errors in the Group Velocity

    The group velocity is numerically calculated using the approaches illustrated in Section 2.4.

The relative errors in the group velocity

(

c

(
g WFE

)

−

c

)g

c

g

 are plotted in Figure 4.3 where

gc

is  the  analytical  group  velocity,

gc

=

E ρ

 [21].  The  analysed  frequency  range  is  linearly

discretised into 1000 frequency steps in the log scale.

19

    For  all  methods,  the  relative  error  is  almost  same  above

Lk

∆ >

−
310

.  The  relative  error  of

the  power  and  energy  relationship  is  smallest  below

Lk

∆ <

−
310

.  Since  the  group  velocity  is

calculated from the power flow and the energy density given in equations (2.21) and (2.22),

small  fluctuated  errors  in  the  eigenvectors  can  be  improved  through  the  calculation.  At  this

frequency  range,  the  relative  error  for  the  differentiation  of  the  eigenproblem  shows  the

almost  same  curve  as  those  in  the  wavenumber  and  eigenvector  while  that  the  error  for  the

finite  difference  method  is  larger  very  slightly.  Although  the  error  for  the  finite  difference

method depends on the frequency step, too small frequency step does not always improve the

error because the error becomes more sensitive to the errors in the dispersion relationship.

100

10-5

|

g

c

/

)

g

c
-

E
F
W
g

c
(

|

10-10

10-8

10-6

10-4
k
L∆

10-2

100

Figure  4.3:  Relative  errors  in  the  group  velocity:  ―  finite  difference,  –  –  power  and  energy

relationship,  −·− differentiation of the eigenproblem.

4.3 Flexural Waves in an Euler-Bernoulli Beam

    The flexural waves in the Euler-Bernoulli beam (e.g. [36]) are considered. The WFE results

are evaluated with the analytical solution.

4.3.1 Analytical Expression for the Discretised Beam Element

    Using a cubic polynomial as a shape function, the mass and stiffness matrices of the beam

can be formulated as [35]

20

K

=

EI
3
∆

12

.
sym








∆
6
2
∆

4

−
12
− ∆
6

12

∆
6
2
∆

2

− ∆
6
2

4

∆

,

M

=










∆ 
ρ
A

420



156

∆
22
2
∆
4

54
13

− ∆
13
2
∆ − ∆
3

sym
.

156

22
− ∆
2
4
∆








(4.11)

where EI is the bending stiffness,  ρ is the mass density and A is the cross-sectional area. The

dynamic stiffness matrix then becomes

6

−

22
420

4

(

k

B

∆

)

4

−

4
420

(

k

B

∆

)

4















12

−

156
420

4

(

k

B

∆

)





∆

2

∆

sym
.
















D

=

EI
3
∆

where

−

12

−





∆ − −

6





54
420

13
420

4

(

k

B

∆

)

4

(

k

B

∆

)








∆

2

∆








2

+

6

+

13
420

(

k

B

∆

12

−





156
420

4

(

k

B

∆

)





∆ − +

6





2

∆





4

−

4

4

)

)























(4.12)





)

)

4

4

3
420

22
420

4
420

(

k

B

(

k

B

∆

∆

(

k

B

∆

k

B

=

4

A
ρ
EI

ω

(4.13)

is  the  bending  wavenumber  [36].  The  dynamic  stiffness  matrix  in  equation  (4.2)  is  accurate
}8

for the analytical dynamic stiffness matrix [37] up to

 with error being

{
(
BO k ∆

{
(
BO k ∆

}4

)

)

for small  Bk ∆ .

    The transfer matrix derived from equation (4.12) becomes [13]

21

T

=

302400 720

+

1
(

k

4
)
∆ +

(

k

∆

8

)

B

B

×

+
302400 13320

(

k

B

4
)
∆ +

26

(

k

B

∆

8

)

∆

(

302400 3240

+

(

k

B

4
)
∆ +

2

(

k

B

∆

8

)

)

50400

(

k

B

4
)
∆ +
∆

120

(

k

B

∆

8

)

302400

(

k

B

4
)
∆ +

2820

(

k

B

8
)
∆ +

3

∆

−

151200

(

k

B

4
)
∆ −

570

(

k

B

8
)
∆ −

(

k

B

∆

12

)

(

k

B

∆

12

)

7
2

1
4









EI

EI









+
302400 13320

(

k

B

4
)
∆ +

10

(

k

B

∆

8

)

151200

(

k

B

4
)
∆ +

570

(

k

B

8
)
∆ +

(

k

B

∆

12

)

1
4

2

∆

−

50400

(

k

B

4
)
∆ −

78

(

k

B

8
)
∆ −

1
60

(

k

B

∆

12

)
























EI

EI









3

∆

(

50400 180

+

EI

2

∆
(

k

4

∆

)

B

)

(
2
∆ −

151200 780

−

4

(

k

B

∆

)

EI

2

∆

(
151200 780

+

4

(

k

B

∆

)

)

EI

(
∆ −

302400 3240

−

4

(

k

B

∆

)

+
302400 13320
(
∆ −

302400 3240

−

(

k

B

4
)
∆ +

26

(

k

B

∆

8

)

−

50400

(

k

B

120

(

k

B

∆

8

)

4

(

k

B

∆

)

−

2

(

k

B

∆

8

)

)

+
302400 13320

4
)
∆ +

10

(

k

B

EI
4
)
∆ −
∆
(

k

B

)

)

.(4.14)

∆












)
∆ 

8

Approximate solutions for the characteristic equation derived from the transfer matrix (4.14)

are [13]

λ
1,2

(

k

B

)
∆ =

1

∓

(
j k

B

)
∆ −

(

k

B

2
)
∆ ±

1
2

j
6

(

k

B

3
)
∆ +

λ
3,4

(

k

B

)
∆ =

1

∓

(

k

B

)
∆ +

(

k

B

∆

2

)

∓

1
2

(

k

B

3
)
∆ +

1
6

1
24
1
24

(

4

(

k

B

∆

)

4

k

B

∆

)

∓

∓

j
23
2880
23
2880

(

(

k

B

5
)
∆ −

(cid:4)

,

k

B

5
)
∆ −

(cid:4)

(4.15)

where

1,2λ  are  related  to  the  propagating  waves  and
{
(
BO k ∆

equations (4.15) the eigenvalues are accurate up to

3,4λ  to  the  nearfield  waves.  From
}5

 with error being

{
(
BO k ∆

}4

.

)

)

The relative errors in the wavenumber,

log

(
λ − = ∆ , are from equation (4.15)

k

)

j

(

k

B

∆

)

1,2

=

(

k

B


)
∆ ±



1

∓

577
2880

(

k

B

4
)
∆ +

(cid:4)

,





such that the relative error in the wavenumbers are

(

k

B

∆

)

3,4

= −

(
j k

B


)
∆ ±



1

∓

B

(

k

577
2880
{
(
BO k ∆

4
)
∆ +

(cid:4)





)

}4

.

(4.16)

    The eigenvectors associated with

1,2λ  are also analytically given such that

22








w
12


∆
 =

EI



EI

θ
12
3
∆

2

∆

f
12
m
12











∓

(
j k

B

∆

±

(
j k

B

∆

3

)

−

(

k

B

∆

)

{
)
1
{
1
{
1

2

1

∓

(

k

B

∆

)

4

2880

±

6

(

k

B

∆

)

10800

∓

4

(

k

B

∆

)

∓
960 13

6

(

k

B

∆

)

302400

−

(

k

B

∆

)

4

1440

−

6

(

k

B

∆

)

18900











(4.17)

}
∓(cid:4)
}
(cid:4)
}
(cid:4)

±

−

where  w  is  the  translational  displacement  and

,f mθ

,

 are  the  rotational  displacement,  the

shear  force  and  the  moment  per  unit  displacement.  The  analytical  solution  is  available

anywhere  (e.g.  [20,36]).  The  relative  error  in  the  elements  of  the  analytical  eigenvectors

(4.17) are

{
(
BO k ∆

)

}4

. Similar expression holds for

3,4λ  with the relative error in the elements

of the eigenvectors being

{
(
BO k ∆

)

}4

.

    Although  the  details  are  omitted,  the  same  accuracies  are  given  using  the  conditioned

eigenvalue  problem  (3.9),  i.e.  the  relative  error  is

{
(
BO k ∆

)

}4

 for  the  wavenumbers  and

components in the eigenvectors.

4.3.2 Relative Errors in the Eigenvalues and Eigenvectors

    The relative errors in the wavenumbers (eigenvalues) and eigenvectors are investigated in

this section. The properties of the beam are assumed to be

EI =

0.175

,

Aρ =

0.078

 and  ∆  is

selected as

3
2 10−
⋅

, all in SI units. The results using both the transfer matrix approach (2.15)

and the conditioned eigenvalue problem (3.9) are compared.

Figure 4.4 shows the relative errors in the propagating wavenumber using both eigenvalue

problems.  Regardless  of  the  eigenvalue  problems,  the  relative  errors  take  the  minimum

around

Bk ∆ =

0.04

 and the similar trend with the quasi-longitudinal waves can be seen. That

is, the FE discretisation errors govern the relative errors for large  Bk ∆  while for the round-off

errors due to the inertia term become significant for small  Bk ∆ .

The  asymptotic  slopes  for  large

Bk ∆  and  for  small

Bk ∆  are  +40  dB/decade  and  -40

dB/decade.  For  large  Bk ∆  the  slope  can  be  explained  from  equations  (4.16).  The  value  of

min

(

2

)

ω M K  from  equations  (4.11)  explains  the  asymptotic  slope  for  small  Bk ∆  such

ii

ii

that

min

(

2
ω

M K
ii

ii

)

=

1 420

(

Bk

∆

)4

, which is related to

2
1 ω .

23

In this case, the transfer matrix results show marginally better accuracy. This is because the

fact  that  the  conditioned  eigenvalue  problem  gives  the  repeated  eigenvalues  such  that  the

method is more sensitive to perturbation [24]. For this example, the condition number of the

matrices to be inverted in the transfer matrix approach and that in the conditioned eigenvalue

problem  is  about  same,  as  shown  in  Figure  4.5  (the  peaks  in  the  figure  correspond  to

singularities  in  the  matrix  to  be  inverted).  In  addition,  the  matrix  size  is  small (

n =

)4

 such

that  the  ill-conditioning  of  the  eigenvalue  problem  is  not  so  significant.  Because  of  these

reasons, the transfer matrix approach show better results.

    Basically  the  same  discussion  holds  for  the  relative  errors  in  the  eigenvectors.  Figure  4.6

shows  the  relative  errors  in  the  rotational  displacement  of  the  eigenvector  per  unit

displacement,  which  is  analytically  given  by  w k

θ =  (e.g.  [20,36]).  The  same  trend  as  the

relative error in the wavenumber can be seen.

    The  eigenvectors  using  the  conditioned  eigenvalue  problem  contain  only  displacement

components such that force components are calculated using either equation (3.13) or (3.18).

The  shear  force  per  unit  displacement,  which  are  analytically  given  by

f w EIk
=

3

 (e.g.

[20,36]),  are  investigated.  The  relative  errors  in  the  shear  force  per  unit  displacement  are

plotted  in  Figure  4.7.  The  relative  error  associated  with  the  transfer  matrix  approach  shows

the minimum especially at low frequencies because of the reason as stated previously. For the

conditioned  eigenvalue  problem,  the  round-off  error  occurs  through  calculating  either  the

original  equation  (3.13)  or  the  SVD  approach  (3.18).  It  can  be  seen  that  the  proposed  SVD

approach marginally reduces the relative errors especially at low frequencies where the round-

off  errors  increase.  Although  the  details  are  omitted,  the  same  discussion  holds  for  the

moment component.

24

|

B

k

/

)

k
-
k
(
|

B

102

100

10-2

10-4

10-6

10-8

10-10

10-4

10-3

10-2

10-1

100

101

k
B∆

Figure 4.4: Relative errors in the propagation wavenumber for ― the conditioned eigenvalue problem

(3.9), – – the transfer matrix approach (2.15), ····· asymptote  40dB decade

±

.

108

106

104

κ

102

10-4

10-3

10-2

10-1

100

101

k
B∆

Figure  4.5:  The  condition  numbers  of  (a)  the  matrix  to  be  inverted:  ―  the  conditioned  eigenvalue

problem (3.9), – – the transfer matrix (2.15).

25

102

100

10-2

10-4

10-6

10-8

|

θ
/

)
θ
-

E
F
W
θ
(
|

10-10

10-4

10-3

10-2

10-1

100

101

k
B∆

Figure 4.6: Relative errors in the rotational displacement per unit displacement: ― the conditioned

eigenvalue  problem  (3.9),  –  –  the  transfer  matrix  approach  (2.15),  ·····  asymptote

40dB decade
±

.

2
10

0
10

-2

10

-4

10

-6

10

-8

10

|
f

/

)
f
-

E
F
W

f
(
|

-10

10

-4

10

-3

10

-2

10

-1

10

0
10

1
10

kB∆

Figure 4.7: Relative errors in the shear force per unit displacement. Notation is same as Figure 4.7.

4.3.3 Relative Errors in the Group Velocity

    The  group  velocity  is  numerically  calculated  using  the  methods  outlined  in  Section  2.4.

Figure  4.8  shows  the  relative  error  in  the  various  estimates  of  the  group  velocity.  The

26

analytical  solution  is  given  by

c

g

kω=
2

B

 (e.g.  [21]).  1000  discretised  frequencies  are

linearly taken in the log space of frequency.

    The  power  and  energy  relationship  and  the  differentiation  of  the  eigenproblem  show

accurate  results.  The  differentiation  of  the  eigenproblem  is  likely  to  suffer  from  numerical

errors because the method needs

−D  to be evaluated and a large number of matrix operations

1
LR

such that numerical errors may accumulate. Smaller frequency step improves the accuracy of

the result using the finite difference method for

Bk ∆ >

0.04

 and the error curve follows other

two lines, which is the error bound given from the accuracy of the wavenumber.

    Regardless  of  the  methods,  the  numerical  results  show  small  errors  for  the  range  of,  say,

0.01

Bk≤ ∆ ≤  where both the eigenvalues and eigenvectors are accurately calculated. For the

1

rod case, the range was about

610

− ≤ ∆ ≤ . The difference of the lower bound results from

1

Lk

the round-off errors due to the inertia term.

100

10-2

|

g

c

/

g

10-4

c
-

)

E
F
W
(
g

c
(
|

10-6

10-8

10-10

10-3

10-2

10-1

k
B∆

100

Figure  4.8:  Relative  errors  in  the  group  velocity:  ―  finite  difference,  –  –  power  and  energy

relationship,  −·− differentiation of the eigenproblem.

27

5. NUMERICAL EXAMPLE OF A PLATE STRIP

5.1 Introduction

    For  two-dimensional  structures,  the  conditioned  eigenvalue  problem  should  be  applied  to

improve  ill-conditioning  occurring  in  the  transfer  matrix  approach.  Numerical  examples  are

shown for flexural waves in a thin isotropic plate strip. No damping is assumed.

5.2 Analytical Expression for Flexural Waves in a Plate

    A plate strip of width

yL , shown in Figure 5.1, is considered. The plate is thin and isotropic

with simply supported boundary conditions along the y-wise plate edges. For such plate, the

analytical wavenumber is given by [36]

2

k

=

k

2
x

+

k

2
y

= ±

h
ρ
ω
D

(5.1)

where

=
D Eh

3

(
12 1

2
−
ν

)

 is the bending rigidity, h is the thickness of the plate strip and ν

is  the  Poisson’s  ratio.  For  the  simply  supported  boundary  condition  along  the  plate  edges

y

=

0,

L

y

,  the  wave  modes  have  displacements  proportional  to

sin

(

n y Lπ

)

y

 where  n  is  an

integer. The wavenumber along the x-direction is then given by

k

2
xn

= ±

ρ
h
−
ω
D

2






π
n
L

y






(

n

=

1, 2,

)
(cid:4) .

Substituting

xnk =  into equation (5.2) gives the cut-off frequency for the nth wave as

0

ω
n

=

π


D n


ρ
h L


y

2






(

n

=

1, 2,

)
(cid:4) .

The group velocity is given from equation (5.2) as

c

gn

=

ω
∂
∂
k

xn

=

2

D
ρ
h

k

xn

.

28

(5.2)

(5.3)

(5.4)

Ly

z

x

y

y

y∆

Ly

x∆

x

Figure 5.1: Simply supported plate strip.

5.3 Flexural Waves in a Plate Strip Using the WFE Method

    The  flexural  waves  in  the  plate  strip  are  solved  using  the  WFE  method  and  results

evaluated.  In  particular,  reducing  numerical  errors  is  suggested  using  a  FE  model  with

internal nodes.

5.3.1 The WFE Formulation

     The plate is assumed to be a steel plate with

yL =

0.18

,

E =

⋅
2.0 10

11

,

ρ=

7800

ν =
,

0.30

and

h

=

⋅
1.8 10

−

3

,  all  in  SI  units.  The  mass  and  stiffness  matrices  are  formed  using  ANSYS

7.1. A four node plane strain shell element (SHELL63), which uses cubic polynomial shape

functions for both the x- and y-directions, was chosen. The aspect ratio of FE

γ = ∆ ∆ ≈
1

x

y

is preferable since

k ∆ ≤  and
1
x

x

k ∆ ≤  should be satisfied.

1

y

y

5.3.2 Results Using the Transfer Matrix

    The ill-conditioning of the transfer matrix approach is illustrated in this section. Consider a

plate strip model comprising 4 elements as shown in Figure 5.2. After removing the in-plane

DOFs and DOFs associated with the boundary conditions, there are 22 resulting DOFs for the

model.  Since  the  y-wise  wavenumber  is

k

n Lπ=

y

y

 for  the  nth  wave  mode,  only  the  n=1

wave mode could be expected to be accurate since

k

π∆ =

y

y

4

(

)
1
< .

    The  dispersion  relationships  are  shown  in  Figures  5.3.  The  abscissa  represents  the  non-

dimensional  frequency

Ω =

2

yL

2

π ρ ω

h D

 and  the  cut-off  frequencies  occur  at

2nΩ =

(n=1,2,3…). The ordinate shows the non-dimensional wavenumber,

k L π, which becomes
x

y

29

-jn  for  the  nth  mode  at

0Ω =

.  When

k ∆ =  then
1
x

x

k L π =
x
y

3.18

,  so  that  the  FE

discretisation error should be small if

k L π <
x
y

3.18

.

    The wavenumber calculated from the transfer matrix (2.15) and that from the conditioned

eigenvalue  problem  (3.9)  are  shown  in  Figure  5.3  (a)  and  (b),  respectively.  There  are  two

waves associated with the n=1 mode. One is a propagating wave which cuts-on at

1Ω =  and

another  is  a  nearfield  wave.  In  Figure  5.3  (a),  it  can  be  seen  that  the  wave  near  the  cut-off

frequency (

)1Ω =

 is inaccurate. This is because the two roots associated with the positive and

negative going wave are such that

jkx

e± →  around the cut-off frequency and such roots are

1

likely to be estimated inaccurately because of the ill-conditioning. In turn, relatively accurate

results are obtained for the conditioned eigenvalue problem in Figure 5.3 (b) because of the

conditioning described in Section 3.

    The  condition  numbers  of  the  matrices  to  be  inverted  (

LRD  in  equation  (2.14)  and

2Z  in

equation  (3.9))  and  those  of  the  eigenvalue  problems  ( T  in  equation  (2.15)  and

1

−Z Z  in
1

2

equation  (3.9))  are  plotted  in  Figures  5.4.  Both  the  condition  number  for  the  matrix  to  be

inverted  in  Figure  5.4  (a)  and  that  for  the  eigenvalue  problem  in  Figure  5.4  (b)  are  worse-

conditioned  when  the  transfer  matrix  approach  is  used.  The  condition  numbers  are  almost

constant  in  this  frequency  range  of  interest.  For  plate  strip  models  with  more  elements,  the

numerical  artefact  around  the  cut-off  frequency  becomes  more  prominent  because  of  the

worse  conditioning  and the results using the transfer matrix approach will completely break

down.

y

x

Figure 5.2: The plate strip FE model,

∆ =
x

18

mm

,

∆ =
y

45

(
mm L

y

4

)

.

30

)
π
/

y

L

x

k
(
e
R

)
π
/

y

L

x

k
(
m

I

10

(a)

5

0

-5

0.5

)
π
/

y

L

x

k
(
e
R

)
π
/

y

L

x

k
(
m

I

(b)

1

0.5

0

-0.5

-1

-1.5

-2
0.5

1

1

1.5

1.5

Ω

Ω

2

2

Figures 5.3: Dispersion relationships: ― analytical solution, ···· the WFE result using (a) the transfer

matrix approach, (b) the conditioned eigenvalue problem.

6
10

(a)

κ

5
10

4
10

0.5

15

10

(b)

κ

10

10

5
10

0.5

1

1

1.5

1.5

Ω

Ω

2

2

Figures 5.4:  The condition numbers of (a) the matrices to  be inverted,  (b) the eigenvalue problems:

– – the transfer matrix approach, ― the conditioned eigenvalue problem.

31

5.3.3  Relationship  between  the  Condition  Number  and  Matrix

Size

    Even  for  the  conditioned  eigenvalue  problem,  the  conditioning  is  still  of  concern.  The

condition  number κ of  the  matrix  to  be  inverted  is  discussed  in  this  section.  For  flexural

waves  in  a  plate  strip,  the  condition  number  of

2Z  in  equation  (3.9)  is  examined.  If κ is

large,  numerical  errors  occur  when  the  matrix  is  inverted  and  the  resulting  eigenvalue

problem is likely to be numerically contaminated.

The  condition  number  depends  on  the  modelling  of  the  plate  strip  model.  Here κ are

determined  for  several  plate  strip  models  and  the  results  are  shown  in  Figure  5.5.  It  can  be

seen that as (1)

x∆  becomes smaller and (2) the matrix size increases and (3) the aspect ratio

γ of the element becomes large, κ increases. From the figure, the relationships between κ,

∆  and the number of elements, N, are approximately expressed as

xκ −∝ ∆     or

2

2Nκ∝

(5.5)

for the same element aspect ratio. As the number of elements increases, the condition number

gets  larger  because  the  number  of  the  singular  values  of  the  matrix  increases  which  usually

results in there being a wider range of the relative magnitudes of the singular values.

    Next the effect of the aspect ratio, γ, is determined for the same element area as Figure 5.6.

The case of

γ =

0.2

 is also included. For elements of the same  area, the dependence in γ is

shown in Figure 5.7. The ordinate shows the ratio of κ to that for

1γ = . From the figure, the

relationships between γ and κ are roughly estimated as

κ κ
γ

1
=

∝

(
2.1
γ γ

>

)
1 ,

κκ
γ

1
=

∝

γ

(
0.4
γ−

)
1
<

(5.6)

such  that  rectangular  elements  (

)1γ ≠  cause κ to  be  larger.  The  condition  number  of  the

matrix  to  be  inverted  is  usually  related  to

)LRκ D
(

.  The  matrix

LRD  represents  the

relationship between forces and displacements across an element, i.e.  L

=f

D x . When the

LR R

range  of  the  magnitude  of  elements  in

LRD  increases,  the  condition  number  often

deteriorates. For elements with

1γ ≠ , only some elements become large compared to others.

More  detail  expression  of  the  effect  of  γ  in

LRD  can  be  seen  in  [35].  Some  elements

approach  infinity  with  different  coefficients  for  the  limiting  case  of γ → ∞  or

0γ →  such

that

)LRκ D  deteriorates.

(

32

109

108

180

8
4
.
7
=
Ω

t
a
κ

107

106

105

90

36

γ=1
γ=2.5
γ=5
γ=0.4

100

180

150

180

90

45

18

101

75

30

90

36

12

18

 (mm)

∆x

Figure 5.5: Condition numbers of the matrix to  be inverted at  Ω = 7.48 . Each number in the figure

denotes the numbers of elements.

109

108

107

106

.

8
4
7
=
Ω

t

a
κ

γ=1
γ=2.5
γ=5
γ=0.4
γ=0.2

105

100

101

102

Area of an element ×10-6 (m2)

Figure 5.6: Condition numbers as a function of the area of an element.

33

102

)
1
=
γ
(
κ
/
κ

101

100

10-1

100
γ

101

Figure 5.7: Condition number as a function of the aspect ratio.

5.3.4 Relative Error in the Eigenvalues and Eigenvectors

Based on the previous discussions, the relative error in the eigenvalues is investigated using

the  conditioned  eigenvalue  problem.  An  18  elements (

∆ = ∆ =

y

x

10

mm

)

 plate  strip  model  is

first evaluated. The dispersion relationship is shown in Figure 5.8. For the model,

associated with

k L π =
x
y

5.73

 and

k ∆ =
y

y

1.05

 for the n=6 wave mode.

k ∆ =  is
x

1

x

Six wave modes cut on in the frequencies analysed. The dispersion relationship shows that

the WFE results generally agree well with the analytical solution. Some discrepancies can be

seen  for  higher  wave  modes  and  for  large

k L π  as  the  FE  discretisation  errors  (and  the
x

y

round-off error due to the inertia term at low frequencies) increase. At low frequencies, two

nearfield  waves  calculated  in  the  WFE  method  become  complex  conjugate  pairs  as  a

numerical artefact. The real part is small compared to the imaginary part by a factor of about

10. In the figure, only the imaginary part is plotted for clarity.

34

6

4

2

0

)
π
/

y

L

x

k
(
e
R

-2

)
π
/

y

L

x

k
(
m

I

-4

-6

0

5

10

15

20

25

30

35

40

45

Ω

Figure  5.8:  Dispersion  relationship  for  the  18  element  plate  strip (

solution, – – WFE result.(

k ∆
x

x

≈

1.16

)

.

max

∆ = ∆ =

x

y

10

mm

)

:  ―  analytical

The relative error in the wavenumber associated with the n=1 mode is shown in Figure 5.9.

The results are shown for three FE models, which are the 18 elements (

∆ = ∆ =

y

x

10

mm

)

, 36

elements (

∆ = ∆ =

x

y

5

mm

)

 and 90 elements (

∆ = ∆ =

x

y

2

mm

)

 plate strip models. The peaks at

the cut-off frequency (

)1Ω =

 occur because the denominator approaches 0 (

k → . The FE

)0

discretisation  errors  become  smaller  for  the  smaller

x∆  FE  models.  However,  the  round-off

errors due to the inertia term increase at low frequencies for small  ∆  (the 90 elements model).

For the 90 elements model,

k ∆  becomes 1 around
x

x

Ω =

900

.

Similarly,  the  relative  errors  in  the  eigenvector  (the  rotational  displacement  per  unit

displacement (

)wθ ) associated with the n=1 wave are shown in Figure 5.10. A similar trend

35

to the eigenvalue can be seen. The relative error in the eigenvector is generally larger than that

in the eigenvalues for large matrix size as can be seen also in this case.

    The shear force is next evaluated using the SVD approach (3.18). The analytical expression

for the shear force is [36]

τ

=
w jDk

(

k

2
x

x

+

(

2

)
−
ν

k

2
y

)

.

(5.7)

The  relative  error  in  the  calculated  shear  force  per  unit  translational  displacement (

)wτ  is

shown  in  Figure  5.11.  It  can  be  seen  that  the  errors  associated  with  the  18  and  36  elements

model are similar to that in the wavenumbers and eigenvectors. However, the error associated

with  the  90  elements  model  is  large  because  (1)

k ∆  is  small  such  that
x

x

1λ≈  in  equation

(3.19)  causes  the  round-off  errors  in  arithmetic  calculation  and  (2)  the  matrix  size  is  large

such that round-off errors may accumulate.

The  SVD  approach  for  numerically  determining  the  eigenvector  reduces  the  numerical

error. Although the error in each eigenvalue component (

,w θ  is small, the error in τ can be

)

substantial. Figure 5.12 shows the relative error in  wτ  using the original approach (3.13) and

the  SVD  approach  (3.18).  It  can  be  seen  that  the  relative  error  associated  with  the  SVD

approach is generally smaller especially at low frequencies and around the cut-off frequency

where  the  round-off  error  through  the  matrix  operations  in  the  original  approach  (3.13)  is

likely to occur.

|
k

/

)
k
-

E
F
W

k
(
|

100

10-2

10-4

10-6

10-2

k ∆ =
1

x

x

k ∆ =
1

x

x

10-1

100

101

102

Ω

Figure  5.9:  Relative  errors  in  the  wavenumber  for  the  n=1  mode:  (cid:0)

the  18  elements,  −·−  36

elements,  – – 90 elements plate strip model.

36

100

10-2

10-4

|

θ

/

)
θ
-

E
F
W
θ
(
|

10-6

10-2

k ∆ =
1

x

x

k ∆ =
1

x

x

10-1

100

101

102

Ω

Figure 5.10: Relative errors in  wθ  in the eigenvector. Notation is same as Figure 5.9.

100

10-2

10-4

|
τ

/

)
τ
E-
F
W
τ
(
|

10-6

10-2

k ∆ =
1

x

x

k ∆ =
1

x

x

10-1

100

101

102

Ω

Figure 5.11: Relative errors in  wτ  in the eigenvector. Notation is same as Figure 5.9.

37

100

10-1

10-2

10-3

|
τ

/

)
τ
-

E
F
W
τ
(
|

10-4

10-3

10-2

10-1
Ω

100

101

Figure  5.12:  Relative  errors  in  wτ  in  the  eigenvector:  (cid:0)

  the  SVD  approach,  ·····  the  original

approach.

5.3.5 Reducing Numerical Errors Using a FE Model with Internal

Nodes

    There  is  a  clear  trade-off  among  the  round-off  errors  due  to  the  inertia  term,  the  FE

discretisation error  and the conditioning especially  at low frequencies. To calculate accurate

results  at  low  frequencies,  using  internal  nodes  for  the  FE  model  (two  or  more  series  of

elements  jointed  together)  as  shown  in  Figure  5.13  can  be  used.  After  the  DOFs  associated

with  internal  nodes  are  condensed  using  equation  (2.7),  the  resulting  FE  model  can  reduce

both  the  round-off  error  due  to  the  inertia  term  and  the  FE  discretisation  error  because  the

length  ∆  is  increased  and  more  accurate  shape  function  is  equivalently  applied  in  the

direction  of  wave  propagation  after  removing  the  DOFs  associated  with  internal  nodes.  By

using this approach, the trade-off can be alleviated. The number of rows for internal nodes can

be  more  than  1  but  care  should  be  taken  because  the  large  condition  number  of

IID  in

equation (2.8) may cause another numerical error.

    The relative error in the wavenumber for the n=1 mode is shown in Figure 5.14. The results
using  a  FE  model  with  one  row  of  internal  nodes (

 are  compared  with

∆ =
y

∆ =
x

mm

mm

)

2

4

,

the original FE model (

∆ = ∆ =

x

y

2

mm

)

.  In addition, results using a model of 90 rectangular

38

elements (

∆ =
x

4

mm

,

∆ =
y

2

mm

)

 without internal nodes are also shown. It can be seen that the

relative error for the model with internal nodes is reduced especially at low frequencies.

    Table  5.1  shows  the  value  of

M K  associated  with

ii

ii

,
τ

m m
,x

y

 (the  DOFs  associated

with flexural motion) for small  Ω . Especially for DOFs associated with the moment

ym , the

value is increased because of the increase in

x∆  so that the round-off error due to the inertia is

reduced for the model with internal nodes and the model with rectangular elements. Since

y∆

is  same  for  all  FE  models,

min

(

2

ii

)

ii

ω M K  is  about  same  for  the  models  as  can  be  seen

from Table 5.1 (elements associated with

xm ). Figure 5.15 shows

min

(

2

)
ω M K  for the
ii

ii

model with internal nodes as a function of  Ω  as a rough estimate of the round-off errors. All

the models typically show similar results to Figure 5.15.

    Similarly, the  relative  error in  wτ  is considered. The results using the 90  element model

(

∆ = ∆ =

x

y

2

mm

)

 is poor (Figure 5.11) because of the round-off error due to the inertia term

and  the  small  value  of

k ∆   (

x

x

)1λ≈

.  These  errors  can  be  improved  using  the  model  with

internal nodes. Results using the model with internal nodes are shown in Figure 5.16. It can

be seen that the FE model using internal nodes can greatly improve accuracy of the result.

    The  condition  number

)IIκ D  for  the  FE  model  using  internal  nodes  is  about

(

1310  in  the

frequency  range  of  interest  and  the  pseudo-matrix  inverse  is  applied.  Even  for  such  a  large

condition number, it is seen that a FE model with internal nodes reduces numerical errors.

(a)

Lq

(b)

Rq

Lq

1

Iq

2

Iq

N

Iq

Rq

Figures  5.13:  (a)  Single  element,  (b)  multiple  elements  with  N  series  of  internal  nodes  to  be

concentrated.

39

|

k

/

)
k
-

k
(

|

E
F
W

-2

10

-3

10

-4

10

-5

10

-6

10

-3

10

-2

10

-1

10

0
10

Ω

1
10

2
10

Figure  5.14:  Relative  errors  in  the  wavenumber  for  the  n=1  mode:  ·····  original  FE  model,  ―  FE

model with internal nodes,  – – rectangular FE model.

Single element set
)
(

∆ = ∆ =

mm

2

x

y

xm θ
,x

ym θ
,y

, wτ

4.82 10−×

15

4.82 10−×

15

3.14 10−×

14

Table 5.1:

Two series of elements

Single element set

(with internal nodes)
)

∆ =
y

∆ =
x

mm
,

mm

4

2

(

(

∆ =
x

4

mm
,

∆ =
y

2

mm

)

5.24 10−×

15

3.42 10−×

14

7.64 10−×

14

5.92 10−×

15

5.70 10−×

14

7.74 10−×

14

M K  associated with each DOF.

ii

ii

40

)

i
i

i

/

K
Mi
ω

2

i

(
n
m

10-2

10-4

10-6

10-8

10-10

10-12

10-14

10-16

10-3

10-2

10-1

100

Ω

101

102

Figure 5.15:

min

(

2

ω M K  as a function of  Ω .

ii

)

ii

|
τ

/

)
τ
-

E
F
W
τ
(
|

100

-2

10

-4

10

-6

10

-2

10

-1

10

0
10

Ω

1
10

2
10

Figure  5.16:  Relative  errors  in  wτ  in  the  eigenvector:  ·····  original  FE  model,  ―  FE  model  with

internal nodes,  – – rectangular FE model.

41

5.3.6 Condensation Using Approximate Expressions

    In  Section  5.3.5,  the  FE  model  using  internal  nodes  has  been  validated  and  good

improvement  in  numerical  errors  has  been  shown.  However,  the  method  needs  the  matrix

inverse

−D  in equation (2.8) to be evaluated at each frequency and hence the calculation cost

1
II

is  high.  In  addition,  round-off  errors  may  be  large  in  the  calculation  of  the  elements  of  the

dynamic  stiffness  matrix.  It  should  be  noted  that  this  section  focuses  on  reducing  round-off

errors  in  numerical  calculations  for  elements  of  the  dynamic  stiffness  matrix,  not  for  the

inertia term.

−D  can be expressed as

1
II

D

1
−
II

=

(

K

II

−

2
ω

M

−

1

)

=

(

II

I

−

2
ω

)
1
−
K M K
II
II

1
−
II

−

1

(5.8)

where

M K  are  the  elements  of  the  mass  and  stiffness  matrices  associated  with  internal

,II

II

DOFs. For small

−K M  a series expansion can be applied, i.e. to the first order

1
II

II

D

1
−
II

=

K

1
−
II

+

O

(

)
K M

1
−
II

II

or, to the second order,

D

1
−
II

=

(

I

+

2
ω

K M K

1
−
II

II

)

1
−
II

+

O

(

)2
K M .
II

1
−
II

(5.9)

(5.10)

Equations (5.9) and (5.10) need only

−K  to be evaluated such that the calculation cost is low.

1
II

    For clarity, equation (5.9) is referred to the 1st order approximation and equation (5.10) is

referred  to  the  2nd  order  approximation  while  the  original  approach  is  referred  as  dynamic

condensation. Using equations (5.9) and (5.10), the original equation (2.8) and the associated

mass and stiffness matrices (for the calculation of the group velocity) can be derived.

    For the 1st order approximation (5.9), the condensation (2.8) becomes

K K M M K K
−
IM

MI

MI

1
−
II

1
−
II

)

.

IM

(5.11)

D

MM

−

D D D

MI

1
−
II

≈

K

MM

−

IM

K K K

MI

1
−
II

−

2
ω

(

M

−

MM

IM

The associated mass and stiffness matrices become

T

R KR K

≈

−

MM

K K K

MI

1
−
II

,

IM

T

R MR M

≈

−

MM

K K M M K K
−
IM

MI

MI

1
−
II

1
−
II

.

IM

(5.12)

It can be seen that the large terms associated with the stiffness and the small terms associated

with  the  inertia  are  appropriately  grouped  such  that  the  round-off  errors  in  the  arithmetic

operation can be reduced.

    Similarly, the 2nd order approximation (5.10) gives

42

D D D

MI

−
1
II

≈

K

MM

−

IM

K K K

MI

−
1
II

IM

−

2
ω

−

4
ω

(
(

M

MM

−

K K M M K K
−
IM

MI

MI

−
1
II

+

IM

1
−
K K M K K
II

−
1
II

MI

II

IM

M K M K K M K M M K M K K

−

−

MI

IM

MI

IM

MI

II

IM

II

−
1
II

−
1
II

−
1
II

−
1
II

−
1
II

−
1
II

(5.13)

)
)

D

MM

−

and

T

R KR K

≈

−

MM

K K K

MI

−
1
II

IM

+

4
ω

(

M K M K K M K M M K M K K

−

−

IM

MI

II

IM

MI

MI

II

−
1
II

−
1
II

−
1
II

−
1
II

−
1
II

T

R MR M

≈

−

MM

K K M M K K
−
IM

MI

MI

−
1
II

−
1
II

+

IM

1
−
K K M K K
II

−
1
II

MI

II

IM

)

,

IM

(5.14)

+

2
2
ω

(

M K M K K M K M M K M K K

−

−

MI

IM

MI

IM

MI

II

II

−
1
II

−
1
II

−
1
II

−
1
II

−
1
II

)

.

IM

    Using  these  two  approximations,  the  relative  errors  in  the  wavenumber  are  evaluated  and

compared with the result using dynamic condensation (as shown in Figure 5.14). The result is

shown  in  Figure  5.17.  The  relative  error  for  the  1st  order  approximation  is  poor  at  high

frequencies  and  becomes  about  1  %  at

Ω =

110−

 where

min

(

2

ω M K  is

10

10−

 as  seen

ii

)

ii

from Figure 5.15.  In the frequency range  analysed, the 2nd order  approximation gives  good

results  as  shown  in  Figure  5.18,  with  accuracy  comparable  to  that  using  the  dynamic

condensation.

    For  the  frequencies  where

2

ω M K  is  small  enough,  the  2nd  order  approximation,

ij

ij

equations  (5.13)  and  (5.14),  is  recommended  to  reduce  round-off  errors  in  arithmetic

2

ω M K  is small enough,

ij

ij

)IIκ K

(

calculations and to  reduce the  calculation  cost.  Since

is about same as

)IIκ D  as shown in Figure 5.19.

(

43

10-2

10-3

|

k

/

)
k
-

E
F
W

k
(

|

10-4

-5

10

-6

10

-4

10

-3

10

-2

10

-1

10

0
10

1
10

2
10

3
10

Ω

Figure 5.17: Relative errors in the wavenumber for the n=1 mode: ― dynamic condensation,  – – the

1st order approximation, ····· the 2nd order approximation.

|

k

/

)
k
-

E
F
W

k
(

|

-2

10

-1

10
Ω

0
10

Figure 5.18: Relative errors in the wavenumber for the n=1 mode: ― (thin) dynamic condensation,

 (cid:0)

 (thick) the 2nd order approximation.

44

(a)

κ

10-4

10-3

10-2

10-1

100

101

102

103

Ω

1.05

(b)

)
i
i

D
(
κ
/
)
i
i

K
(
κ

1

0.95

10-4

10-3

10-2

10-1

100

101

102

103

Ω

Figure 5.19: (a) Condition numbers: ―

)IIκ D ,    – –

(

)IIκ K . (b)

(

(
κ

)
(
κK

II

)
D .
II

5.3.7 Relative Errors in the Group Velocity

    In this section, the approaches for numerically calculating the group velocity, illustrated in

Section  2.4,  are  compared.  The  relative  errors  in  the  group  velocity  for  the  n=1  mode  are

shown  for  frequencies  around  the  cut-off  frequency  in  Figure  5.20.  Results  for  the  18

elements  model  are  shown.  A  frequency  increment  of

δ

Ω =

⋅
7.5 10

−

3

(
f
δ =

Hz
1

)

 is  chosen.

The  result  from  differentiation  of  the  eigenvalue  problem  shows  poor  accuracy.  This  is

because

LRD  must  be  inverted  which  is  ill-conditioned  and  the  fact  that  the  approach  needs

many matrix operations. Therefore numerical errors accumulate.

    Although  all  relative  errors  become  large  near  the  cut-off  frequency,  both  the  power  and

energy relationship and the finite difference approaches show reasonable accuracy. Both the

power  and  energy  relationship  and  the  finite  difference  method  have  advantages  and

disadvantages  in  terms  of  accuracy  and  calculation  cost.  When  both  the  eigenvalues  and

eigenvectors  are  accurately  calculated,  the  power  and  energy  relationship  seems  an

appropriate  approach.  However,  the  eigenvectors  are  likely  to  be  less  accurate  than  the

eigenvalues  such  that  the  finite  difference  method  is  typically  more  accurate.  However,  the

finite  difference  method  needs  a  small  frequency  increment  around  cut-off  frequencies  and

branch points because the wavenumbers may change rapidly.

45

g

|

c
|

/

|

g

c
-

E
F

g

W

c
|

100

10-2

10-4

10-6
1

1.5

2
Ω

2.5

3

Figure  5.20:  Relative  errors  in  the  group  velocity:  ―  finite  difference,  –  –  power  and  energy

relationship,  −·− differentiation of the eigenproblem.

46

6. CONCLUSIONS AND DISCUSSION

6.1 Concluding Remarks

In  this  report,  the  numerical  issues  for  the  waveguide  finite  element  (WFE)  method  have

been discussed.  In the WFE method, the transfer matrix, hence the eigenvalue problem, can

be  formed  from  the  elementary  mass  and  stiffness  matrix  of  a  general  structure.  However

because the transfer matrix might be ill-conditioned, the conditioning of the matrix is essential

for  general  complex  structures.  To  improve  the  matrix  conditioning,  Zhong’s  approach  [30]

has  been  applied  and  the  validity  has  been  investigated.  To  calculate  the  eigenvectors,  an

SVD approach has been proposed to improve numerical errors and the validity evaluated.

Potential  numerical  errors  have  been  discussed  and  categorised  into  the  FE  discretisation

errors, the round-off errors due to the inertia term and errors induced by ill-conditioning.

The  relative  errors  in  the  eigenvalues  and  eigenvectors  were  explained  by  the  FE

discretisation error and the round-off error due to the inertia term for rod and beam problems.

Ill-conditioning  becomes  prominent  for  plate  problems  as  the  matrix  size  increases.  The

relationship  between  the  condition  number  and  the  shape  of  a  FE  element  was  investigated.

The FE model, specifically the length of a section of a structure  ∆ , is important to determine

numerical errors. The FE model with internal nodes was used to alleviate the trade-off among

the potential numerical errors. The 1st order approximation for the condensation was derived,

which showed best accuracy at low frequencies.

Three approaches for numerically calculating the group velocity have been introduced and

the accuracy investigated. The power and energy relationship and the finite difference method

seem appropriate approaches specifically for general structures.

47

References

1.  L. Brillouin 1953 Wave Propagation in Periodic Structures (Second edition). Dover.

2.  D. J. Mead 1986 Journal of Sound and Vibration 104(1), 9-27. A New Method of Analysing
Wave  Propagation  in  Periodic  Structures;  Applications  to  Periodic  Timoshenko  Beams  and
Stiffened Plates.

3.  D. J. Mead 1971  Journal of Engineering for Industry  August,  783-792. Vibration Response

and Wave Propagation in Periodic Structures.

4.  D.  J.  Mead  1973  Journal  of  Sound  and  Vibration  27(2),  235-260.  A  General  Theory  of

Harmonic Wave Propagation in Linear Periodic Systems with Multiple Coupling.

5.  B.  Aalami  1973  Trans.  of  ASME,  Journal  of  Applied  Mechanics  December,  1067-1072.

Waves in Prismatic Guides of Arbitrary Cross Section.

6.  R. M. Orris, M. Petyt 1974 Journal of Sound and Vibration 33(2), 223-236. A Finite Element

Study of Harmonic Wave Propagation in Periodic Structures.

7.  R. M. Orris, M. Petyt 1975 Journal of Sound and Vibration 43(1), 1-8. Random Response of

Periodic Structures by a Finite Element Technique.

8.  A.  Y.  A.  Abdel-Rahmen  1980  Matrix  Analysis  of  Wave  Propagation  in  Periodic  Systems.

Ph.D. thesis, ISVR, University of Southampton.

9.  D.  J.  Thompson  1993  Journal  of  Sound  and  Vibration  161(3),  421-446.  Wheel-Rail  Noise

Generation, Part3: Rail Vibration.

10. L.  Gry  1996  Journal  of  Sound  and  Vibration  195(3),  477-505.  Dynamic  Modelling  of

Railway Track Based on Wave Propagation.

11. L.  Gry,  C.  Gontier  1997  Journal  of  Sound  and  Vibration  199(4),  531-558.  Dynamic
Modelling of Railway Track: A Periodic Model Based on a Generalised Beam Formulation.

12. L. Houillon, M. N. Ichchou, L. Jezequel 2005 Journal of Sound and Vibration 281, 483-507.

Wave Motion in Thin-Walled Structures.

13. D. Duhamel, B. R. Mace, M. J. Brennan 2003 ISVR Technical Memorandum No:922. Finite

Element Analysis of the Vibrations of Waveguides and Periodic Structures.

14. B.  R.  Mace,  D.  Duhamel,  M.  J.  Brennan,  L.  Hinke  2005  Journal  of  Acoustical  Society  of
America  117(5),  2835-2843.  Finite  element  prediction  of  wave  motion  in  structural
waveguides.

15. L.  Hinke,  B.  R.  Mace,  M.  J.  Brennan  2004  ISVR  Technical  Memorandum  No:932.  Finite

Element Analysis of Waveguides.

16. J. M. Mencik, M. N. Ichchou 2005 European Journal of Mechanics, A/Solids 24(5), 877-898.

Multi-Mode Propagation and Diffusion in Structures through Finite Elements.

17. M. Maess, N. Wagner, L. Gaul Journal of Sound and Vibration to appear. Dispersion Curves

of Fluid-Filled Elastic Pipes by Standard FE-Models and Eigenpath Analysis.

18. M. M. Ettouney, R. P. Daddazio, N. N. Abboud 1997 Computers and Structures 65(3), 423-
432.  Some  Practical  Applications  of  the  Use  of  Scale  Independent  Elements  for  Dynamic
Analysis of Vibrating Systems.

19. J. F. Doyle 1997 Wave Propagation in Structures, Second edition. Springer-Verlag.

20. B.  R.  Mace  1984  Journal  of  Sound  and  Vibration  97,  237-246.  Wave  Reflection  and

Transmission in Beams.

21. L.  Cremer,  M.  Heckl,  B.  A.  T.  Petersson  2005  Structure-Borne  Sound  (Third  edition).

Springer-Verlag.

22. S. Finnveden 2004 Journal of Sound and Vibration 273, 51-75. Evaluation of modal density

and group velocity by a finite element method.

23. L. A. Pipes 1963 Matrix Methods for Engineering. Prentice-Hall Inc.

24. L. N. Trefethen, D. B. III 1997 Numerical Linear Algebra. Society for Industrial and Applied

Mathematics.

25. G.  H.  Golub,  C.  F.  V.  Loan  1996  Matrix  Computations  (Third  edition).  Johns  Hopkins

University Press.

26. T.  Gudmundsson,  C.  Kenney,  A.  J.  Laub  1997  SIAM  Journal  on  Matrix  Analysis  and
Applications  18(4),  868-886.  Small-Sample  Statistical  Estimates  for  the  Sensitivity  of
Eigenvalue Problems.

27. J. H. Wilkinson 1965 The Algebraic Eigenvalue Problem. Oxford University Press.

28. S. V. Huffel, V. Sima, A. Varga, S. Hammarling, F. Delebecque 2004 IEEE Control System

Magazine February, 60-76. High-Performance Numerical Software for Control.

29. C. Moler (2004). Chapter 10, Eigenvalues and Singular Values. http://www.mathworks.com/

moler/eigs.pdf, avaiable 19/12/2005.

30. W. X. Zhong, F. W. Williams 1995 Journal of Sound and Vibration 181(3), 485-501. On the

Direct Solution of Wave Propagation for Repetitive Structures.

31. W. X. Zhong, G. Cheng 1991 Proceedings of the Asia-Pacific Conference on Computational
Mechanics,  Blakema,  Rotterdam,  373-378.  Regularization  of  Singular  Control  and  Stiffness
Shifting.

32. W. X. Zhong, F. W. Williams 1992 Proceedings of the Institution of Mechanical Engineers,
Part C 206, 371-379. Wave Problems for Repetitive Structures and Symplectic Mathematics.

33. G. W. Stewart 1972 SIAM Journal on Numerical Analysis 9(4), 669-686. On the sensitivity of

the Eigenvalue Problem Ax=λBx.

34. V. C. Klema, A. J. Laub 1980 IEEE Transactions on Automatic Control AC-25(2), 164-176.

The Singular Value Decomposition: Its Computation and Some Applications.

35. M.  Petyt  1990  Introduction  to  Finite  Element  Vibration  Analysis.  Cambridge  University

Press.

36. K. F. Graff 1975 Wave Motion in Elastic Solids. Dover.

37. J.  R.  Banerjee  2003  Journal  of  Vibration  and  Acoustics,  Trans.  of  ASME  125,  351-358.
Dynamic Stiffness Formulation and Its Application for a Combined Beam and a Two Degree-
of-Freedom System.

