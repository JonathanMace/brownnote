Vibration Modelling of Waveguide Structures using the Wave and Finite Element
Method
Jamil M Renno, Brian R Mace
Institute of Sound and Vibration Research
University of Southampton
Southampton SO17 1BJ
United Kingdom
Email: renno@isvr.soton.ac.uk, brm@isvr.soton.ac.uk
ABSTRACT: The vibration modelling of waveguide structures is considered. These structures comprise waveguides connected
via joints. Traditionally, the wave behaviour of such structures can be analysed if they are simple (beams, rods, etc.). However,
if the waveguides are of complicated constructions (truss-like, layered media, etc.), obtaining the wave characteristics might be a
formidable task. In this paper, such structures are modelled using a hybrid wave and finite element/finite element (WFE/FE)
approach. The waveguides are modelled using the WFE method and thus their wave characteristics are obtained regardless of
the complexity of their cross-section. The joints are modelled using standard FE, and the WFE and FE models are coupled to
yield the scattering properties of the joints. These are used to describe the behaviour of the structure using relatively small
models while providing important information for other applications such as structure-borne sound, statistical energy analysis,
etc. Numerical examples are presented to illustrate the approach.
KEY WORDS: wave and finite element, train cross-section, reflection and transmission coefficients, structural networks.
1 INTRODUCTION [19] and to analyse the vibrational energy in built-up
structures [20-22]. Heron [23] used a line impedance wave
Many structures comprise waveguides which are connected
approach to calculate the transmission between two plates and
via joints into some configuration. The vibrational behaviour
Hambric et al. [24] compared various models of a T-joint and
of such a structural network can be described through the
showed that at higher frequencies the finite dimensions of the
waves that travel through the waveguides, and the scattering
joint become important and should be included in the model.
properties of each joint. For simple structures (where
The waveguides in the reviewed literature were mostly
waveguides are connected at point joints for example), the
isotropic and the joints were often idealised (e.g. point
wave characteristics of the waveguides can be obtained
connections). For such cases, analytical models can be
analytically along with the scattering properties of the joints
developed both for wave propagation and the continuity and
[1-3]. For complicated structures, analytical solutions might
equilibrium conditions at the joint. However, for complicated
be very difficult to obtain. In this case, the finite element (FE)
waveguides and/or complicated joints, finding the reflection
method is often used. However, FE models become
and transmission matrices of the joints using a purely
impractical at higher frequencies leading to a multitude of
analytical formulation can be extremely difficult at best, so
problems (computation speed, accuracy, etc.).
that a numerical approach might be required. In this paper, a
The analysis of waveguide structures has attracted much
hybrid approach for calculating the reflection and
research. The approaches developed can be categorised into
transmission matrices of joints is presented. Joints are
matrix- and wave-based methods. The former uses a matrix
modelled using standard FE methods whereas the waveguides
formulation to couple the waveguides that constitute the
are modelled using the wave and finite element (WFE)
structure [4]. Examples include the dynamic stiffness method
method. This relies on post-processing a standard FE model of
[5-7], mobility power-flow analysis [8], the wave scattering
a small segment of each waveguide using periodic structure
approach [9], and the spectral element method [10]. Other
theory. The degrees of freedom at the interfaces of the WFE
researchers presented a matrix formulation with wave
and FE models of the waveguides and the joint are
scattering [1, 11, 12] to analyse waveguide structures.
compatible. The models are coupled to yield the reflection and
Wave propagation methods rely on obtaining the reflection
transmission matrices of the joint. These can then be used to
and transmission coefficients of the joints. For thin beams,
obtain the response of the whole structure. The approach is
Cremer et al. [13] calculated the scattering coefficients of
similar to that described by Doyle [10] in which a joint is
joints due to an incident propagating wave. Mace [14]
modelled in FE and coupled with waveguides which are
considered the scattering due to an incident evanescent wave,
modelled by spectral elements formed from analytical models.
and later studied the properties of the scattering coefficients
However, this suffers from two possible problems: first if the
[15]. Researchers also used wave-based methods to treat
waveguide has a complicated construction (e.g. a laminate or
three-dimensional frames [9], truss-like structures [16], and
a solid or thin-walled section for which higher order
structural networks [2, 3]. Wave approaches were also used to
wavemodes are important), then finding the spectral element
calculate the reflection and transmission coefficients of
analytically can be very difficult. Secondly, in such an
plate/beam junctions [17], bolted joints [18], curved beams

approach, the models of the waveguides and the joint are not
|     |     |     |     |     |     |     |     |     | D  | D q |      | f   | e   |      |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | ----- | ----- | ---- |
|     |     |     |     |     |     |     |     |     | LL  | LR    | L  | L  | L ,  | (2)  |
compatible at their interface. While the models can be coupled   
|     |     |     |     |     |     |     |     |     | D  | D RRq | R  | f R | e R |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | ----- | ----- | --- |
(e.g. [10] or by the use of Lagrange multipliers), there is a  RL
| discontinuity  | in  the  | models,  | which  | results  | in  | spurious,  |     |     |     |     |     |     |     |     |
| -------------- | -------- | -------- | ------ | -------- | --- | ---------- | --- | --- | --- | --- | --- | --- | --- | --- |
where the subscripts L and R denote the left and right sides
| although  | often  small,  | additional  |     | scattering  | effects  | at  the  |     |     |     |     |     |     |     |     |
| --------- | -------------- | ----------- | --- | ----------- | -------- | -------- | --- | --- | --- | --- | --- | --- | --- | --- |
of the segment, respectively. When a wave propagates freely
interface [25, 26]. In the approach described here, these issues
|     |     |     |     |     |     |     | through the waveguide, the propagation constant  |     |     |     |     |     | eik  |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | -------- | --- |
are not relevant: the WFE method is used to determine the
relates the right and left nodal DOFs and forces by
| wavemodes                           | so  that              | the  complexity  |          | of  the  | construction  | is        |     |     |     |     |     |      |     |      |
| ----------------------------------- | --------------------- | ---------------- | -------- | -------- | ------------- | --------- | --- | --- | --- | --- | --- | ---- | --- | ---- |
| arbitrary,                          | and  the  interfaces  |                  | between  |          | the  joint    | and  the  |     |     |     |     |     |      |     |      |
|                                     |                       |                  |          |          |               |           |     |     | q   | λq | , f | λf | .   | (3)  |
| waveguides have compatible meshes.  |                       |                  |          |          |               |           |     |     |     | R   | L   | R    | L   |      |
The WFE method has been used to study the free [27] and
|     |     |     |     |     |     |     | Substituting  |     | Equation  | (3)  | into  | Equation  | (2)  yields  | an  |
| --- | --- | --- | --- | --- | --- | --- | ------------- | --- | --------- | ---- | ----- | --------- | ------------ | --- |
forced [28] vibration of waveguides. The WFE method for  eigenvalue problem for   which upon solving yields the
waveguides has also been used to study thin-walled structures  wave properties of the waveguide [34]. The eigenvalues occur
[29], laminated plates [27] and fluid filled pipes [30, 31]. It
|     |     |     |     |     |     |     | in  reciprocal  |     | pairs  | as    | and  |  1 |   [35,  36],  | with  |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | ------ | ------- | ---- | ------- | ------------- | ----- |
|     |     |     |     |     |     |     |                 |     |        |         | j    | j       | j             |       |
has also been extended to two dimensional plane [32] and
cylindrical structures [33].  wavenumbers  k and  k k, corresponding to positive-
|     |     |     |     |     |     |     |     |     | j   | j   | j   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
The remainder of this paper is organised as follows. In
and negative-going waves respectively. Associated with these
Section 2, the WFE method will be reviewed briefly. The
eigenvalues are the positive- and negative-going eigenvectors
scattering properties of joints will be obtained in Section  3.
|                                                             |     |     |     |     |     |     | φ  and  | φ  | respectively,  |     | which  | are  | also  called  | the  |
| ----------------------------------------------------------- | --- | --- | --- | --- | --- | --- | -------- | --- | -------------- | --- | ------ | ---- | ------------- | ---- |
| The response of finite waveguide structure is discussed in  |     |     |     |     |     |     | j        |     | j              |     |        |      |               |      |
Section  4 and numerical examples are presented in Section  5.  wavemodes. Every wavemode can be partitioned as
Finally, conclusions for this work are presented in Section  6.
 φ 
q
|                              |     |     |     |     |     |     |     |     |     | φ   |   |  .  |     | (4)  |
| ---------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | ---- |
| 2  REVIEW OF THE WFE METHOD  |     |     |     |     |     |     |     |     |     |     | j φ |      |     |      |
 f 
j
The WFE method is a method for modelling one and two-
dimensional piecewise homogenous/periodic structures. Waki
The wave modes can be grouped into
et al. [34] provides a comprehensive review of the method.
|                                                |     |     |     |     |     |     |     | Φ  | φ |     | φ,ΦΦ |     | Φ.  |      |
| ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --------- | --- | ----- | ---- |
|                                                |     |     |     |     |     |     |     |     |      |    |           |     |       | (5)  |
| 2.1  Free wave propagation and the wave basis  |     |     |     |     |     |     |     |     |     | 1   | n        |    |      |      |
The WFE method starts with obtaining the FE model of a  The left wavemodes can also be obtained. These are 12n
small segment of the waveguide (shown in Figure 1) using
vectors which can be partitioned as
any FE package with the only constraint being that the nodes
and their degrees of freedom (DOF)s are ordered identically
|                                              |     |     |     |     |     |     |     |     |     | ψ ψ |     | ψ  | ,   | (6)  |
| -------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- | ---- |
| on the left and right sides of the segment.  |     |     |     |     |     |     |     |     |     | j     |  f | q  |     |      |
j

and further grouped into
ψ
|     |     |     |     |     |     |     |     |     | Ψ |     |     | 1  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |

|     |     |     |     |     |     |     |     | Ψ | ,whereΨ |     |   |  , | j1,,n.  | (7)  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | ---- | --------- | ---- |
Ψ
|     |     |     |     |     |     |     |     |     |     |     |  ψ |    |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |

|     |     |     |     |     |     |     |     |     |     |     |     | n   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure 1 FE model of a segment of a waveguide with the  The left and right wavemodes can be normalised [34] such
that
waveguide’s local coordinate system.
Internal nodes can be eliminated via dynamic condensation  ΨΦ  
|     |     |     |     |     |     |     |     |     | I  | yielding |     | ΨTΦdiag |  ,  | (8)  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | -------- | ---- | ---- |
j
[34]. Time harmonic dependence of the form eit is assumed
throughout  this  work  and  is  suppressed  for  brevity.  The  where diag(.) represents a diagonal matrix. The partitions of
governing equation of the segment of Figure 1 is  the  left  and  right  eigenvectors  can  be  used  to  form  the
matrices
D=KiC2M,
|     | Dqf e | with |     |     |     | (1)  |     |     |     |     |     |     |     |     |
| --- | ------- | ---- | --- | --- | --- | ---- | --- | --- | --- | --- | --- | --- | --- | --- |
|     |         |      |     |     |     |      |     |     |     |     |     | ψ |    |     |
q,1
where  q,  f and  e  are  2n1  vectors  of  nodal  DOFs,  
|     |     |     |     |     |     |     |   Φ | φ |    | φ   | ,Ψ |   | , j1,,n.  | (9)  |
| --- | --- | --- | --- | --- | --- | --- | ---- | ---- | --- | ---- | ---- | ---- | ------------ | ---- |
|     |     |     |     |     |     |     |      | q   | q,1 | q,n | q    |      |              |      |
internal and external nodal forces respectively,  D,  M,  C   

 ψ ,n
and K are the dynamic stiffness, mass, viscous damping and  q
| stiffness matrices of the segment and  |     |     |     | n is the number of  |     |     |     |     |     |     |     |     |     |     |
| -------------------------------------- | --- | --- | --- | ------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
DOFs at each side of the segment. The dynamic stiffness  Similar expressions hold for  Φ and  Ψ. These matrices,
|     |     |     |     |     |     |     |     |     |     |     | f   |     | f   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
matrix can be partitioned to reflect the influence of the left  together  with  the  orthogonality  relations  of  Equation  (8),
and right nodes of the segment, and thus Equation (1) can be  define transformations between the physical domain, where
expressed as
the motion is described in terms of q and f, and the wave
domain, where the motion is described in terms of waves of

amplitudes a and a travelling in the positive and negative    a s a j,k 1,,p,  (12)
|     |     |     |     |     |     |     |     |     |     | k   | kj j |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- |
directions respectively. Specifically,
|     |     |     |     |      |     |     | where s |     | r  is the reflection matrix of the joint at the j-th  |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | ------- | --- | ------------------------------------------------------ | --- | --- | --- | --- |
|     | q  |    |     | a |     |     |         | jj  | jj                                                     |     |     |     |     |
L
   Φa , a .  (10)  waveguide, and st  (for  jk) is the transmission matrix
|     | f  |     |     | a |     |     |     |     |     | kj kj |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | --- |
|     |     | L  |     |    |     |     |     |     |     |       |     |     |     |
of the joint from the j-th to the k-th waveguides.
In practice, as in modal analysis, only m pairs of (positive-  It  is  assumed  that  the  DOFs  of  the  waveguides  are
and negative-going) waves might be retained, so that  Φ   compatible and all the waveguides are modelled using the
q,f
same number of DOFs. If the DOFs of the waveguides are
Ψ
and   are  nm and  mn matrices respectively. The  incompatible, the interface can then be modelled using full FE
q,f
number retained can be different at different frequencies [37].  and the results of the next section can be used.
Using the continuity and equilibrium conditions at the joint,
2.2  Forced response
the scattering matrix can be obtained as [37]
| A point excitation  |     | f  will generate positive- and negative- |     |     |     |     |     |     |     |     |     |     |     |
| ------------------- | --- | ---------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|                     |     | e                                        |     |     |     |     |     |     |     |     | 1  |     |     |
going waves of amplitudes a and a which will propagate    s C C,  (13)
|     |     |     |     |     |     |     |     |     |     |     |   |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
away from the excitation point in the right and left directions
| respectively. The amplitudes of these waves can be obtained  |     |     |     |     |     |     | where  |     |     |     |     |     |     |
| ------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
as [34]
|     |     |      |          |     |     |       |     | R Φ | D  | R Φ | R Φ      |  R Φ |         |
| --- | --- | ---- | -------- | --- | --- | ----- | --- | ----- | --- | ---- | --------- | ------ | -------- |
|     |     |      |          |     |     |       |     | 1     | f,1 | J 1  | q,1 2 f,2 | p      | f,p      |
|     | a  | Ψf | a Ψf |     |     |       |     |      |     |      |           |        |         |
|     |     |      | ,        |     | .   | (11)  |     |       | Φ  |      | Φ        |        |          |
|     |     | q e  |          | q e |     |       |     |      | R   |      | R        | 0 0    |         |
|     |     |      |          |     |     |       | C  |     | 1   | q,1  | 2 q,2     |        | . (14)  |
In the case of spatially distributed loads, the amplitudes of the       
excited waves can be obtained analytically by using contour   
|     |     |     |     |     |     |     |     |     |     |    |     |        |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | ---- |
|     |     |     |     |     |     |     |     |   | R Φ |     | 0   |  R Φ | ,p |
integration techniques along with the WFE model [38].  1 q ,1 p q
|     |     |     |     |     |     |     | Some  | waveguides  |     | might  | be  connected  | such  | that  the  |
| --- | --- | --- | --- | --- | --- | --- | ----- | ----------- | --- | ------ | -------------- | ----- | ---------- |
3  SCATTERING PROPERTIES OF JOINTS
outgoing waves from one joint are incident on a second join,
| The  reflection  | and  | transmission  | coefficients  |     | of  joints  | in  |     |     |     |     |     |     |     |
| ---------------- | ---- | ------------- | ------------- | --- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure 3.
waveguide structures will now be evaluated using a hybrid
FE/WFE approach. First, point joints will be treated, followed
by the case of joints of finite dimensions.
3.1  Point joints
| Figure 2 shows  | p waveguides with zero-dimensional cross- |     |     |     |     |     |     |     |     |     |     |     |     |
| --------------- | ----------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sections connected at a point joint1. For the j-th waveguide,
| the  local  | coordinate  | system  | is  | defined  | such  | that  the  |     |     |     |     |     |     |     |
| ----------- | ----------- | ------- | --- | -------- | ----- | ---------- | --- | --- | --- | --- | --- | --- | --- |
waveguide’s axis is directed towards the joint. The rotation

matrix R  transforms the DOFs from the local  x ,y  to the
| j   |     |     |     |     | j   | j   |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
global X,Y  coordinate system.  Figure 3 Waveguides connected at a point joint with incident
negative-going waves.
In this case, the scattering matrix becomes
1
|     |     |     |     |     |     |     |     |       |       | sC | C.             |                       |       |
| --- | --- | --- | --- | --- | --- | --- | --- | ----- | ----- | -------- | --------------- | --------------------- | ----- |
|     |     |     |     |     |     |     |     |       |       |          |                 |                       | (15)  |
|     |     |     |     |     |     |     |     |       |       |          |               |                       |       |
|     |     |     |     |     |     |     | If  | only  | m n  | pairs    | of  (positive-  | and  negative-going)  |       |
j
waves are retained for the WFE model of the j-th waveguide,
|     |     |     |     |     |     |     | then                                               | C  | is  not  | invertible.  | In  this  case,  | pseudo-inversion  |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------------------------------------- | --- | -------- | ------------ | ---------------- | ----------------- | --- |
|     |     |     |     |     |     |     | should be used, and the scattering matrix becomes  |     |          |              |                  |                   |     |
Figure 2 Waveguides connected at a point joint with incident  1GC 1GC,
|     |     |     |     |     |     |     |     | sGC |     |     | or sGC |     | (16)  |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | ------------- | --- | ----- |
|     |     |     |     |     |     |     |     |           |    |    |              |    |       |
positive-going waves.
where
The WFE model of each waveguide is obtained in its local
|     |     |    |    |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
coordinate  system  x ,y .  The  incident,  reflected  and  Ψ RT  0 
|     |     | j j |     |     |     |     |     |     |     |     |       |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----- | --- | --- |
|     |     |     |     |     |     |     |     |     |     |    | f,1 1 |    |     |
transmitted waves are related through the scattering matrix as    G     .  (17)
|     |     |     |     |     |     |     |     |     |     |    |        |    |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ | --- | --- |
|     |     |     |     |     |     |     |     |     |     |    | 0  Ψ | RT |     |
                                                             p
f,p
1 For simplicity the waveguides are assumed to lie in a plane: if this is not the
| case, the only difference is related to the transformation matrices R |     |     |     |     |     |  of the  |     |     |     |     |     |     |     |
| --------------------------------------------------------------------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | --- | --- | --- |
j
waveguides.

3.2  Finite joints
|     |     |     |     |     |     |     |     |     | sRΦ | D  | RΦ 1 | RΦ D | RΦ.  | (21)  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | -------- | --- | ------- | ------- | ------ | ----- |
|     |     |     |     |     |     |     |     |     |         |     | q      |        | q     |       |
|     |     |     |     |     |     |     |     |     |          | f   | ii      | f       | ii     |       |
Next, the reflection and transmission properties of joints of
finite size will be considered. Suppose  p waveguides are  Once again, if a reduced number of waves is retained, then
|     |     |     |     |     |     |     |     | pseudo-inversion  |     | is  required,  |     | and  the  | scattering  | matrix  |
| --- | --- | --- | --- | --- | --- | --- | --- | ----------------- | --- | -------------- | --- | --------- | ----------- | ------- |
attached at a joint, Figure 4. The waveguides are modelled
becomes
using the WFE method of Section  2, and the joint is modelled
using standard FE. The WFE model of each waveguide is
|     |     |     |     |     |     |     |     |          | RΦ |     | RΦ | 1        |                |     |
| --- | --- | --- | --- | --- | --- | --- | --- | -------- | ---- | --- | ----- | --------- | -------------- | --- |
|     |     |     |     |     |     |     |     |   sΨ |      | D  |       | Ψ RΦ  | D RΦ, (22)  | q  |
obtained in its local coordinate system   x ,y  using  n    f f ii q  f f ii
|     |     |     |     |     |     | j j |     | j   |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
or
| DOFs (on each side of the waveguide segment) and m |     |     |     |     |     |     |  pairs  |     |     |     |     |     |     |     |
| -------------------------------------------------- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- | --- | --- | --- |
j
of positive- and negative-going waves in the WFE model. It is  RΦ RΦ 1
|     |     |     |     |     |     |     |     |   sΨ |     | D  |     | Ψ RΦ | D RΦ, (23)  |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --------- | --- | --- | --- | ------- | -------------- | --- |
assumed that the interface DOFs of the joint are compatible   f f ii q  f  f ii q
with those of the WFE models.
|     |     |     |     |     |     |     |     | 4  FINITE WAVEGUIDE STRUCTURES  |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------------------------- | --- | --- | --- | --- | --- | --- |
Time harmonic behaviour of the joint is described through
The WFE models (developed in Section  2) and the scattering
|     |     | D | D  |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Q  F  properties of the joints (obtained in Section  3) can be used to
|     |     |       | ii in | i  | i ,  |     | (18)  |     |     |     |     |     |     |     |
| --- | --- | ----- | ------- | ----- | ----- | --- | ----- | --- | --- | --- | --- | --- | --- | --- |
|     |     |  D | D      |       |       |     |       |     |     |     |     |     |     |     |
Q  F  obtain the response of waveguide structures. Each waveguide
|     |     |     | ni nn | n   | n   |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
is modelled using the WFE approach using its local coordinate
where  Q and  F are vectors of DOFs and internal nodal  sjk of the
system. The calculation of the scattering matrix,
forces represented in the global coordinate system X,Y and  joint connecting the j-th and k-th waveguides, will depend on
the orientation of the axes of these waveguide.
the subscripts i and n represent interface and non-interface

nodes, respectively. Since it is assumed that no external forces
| are applied at the non-interface nodes (F |     |     |     |     | 0), the FE model  |     |     |     |     |     |     |     |     |     |
| ----------------------------------------- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
n
of the joint can be condensed as
D Q F,
|     |     | ii i i  |          |      |          |         | (19)  |     |     |     |     |     |     |     |
| --- | --- | ------- | -------- | ---- | -------- | ------- | ----- | --- | --- | --- | --- | --- | --- | --- |
|     |     | D D | D1D   |      | D1D |         |       |     |     |     |     |     |     |     |
|     | D   |         |          | andQ |          | Q       |       |     |     |     |     |     |     |     |
|     |     | ii ii   | in nn ni |      | n        | nn ni i |       |     |     |     |     |     |     |     |
The above condensation is the simplest; other approaches can
be used for enhanced computational speed and better accuracy
[10, 25]. Moreover, the interface nodes can be separated into
those corresponding to each waveguide, Figure 4.

Figure 5 A closed waveguide structure of four waveguides.
The orientation of the waveguides can be arbitrary, and any
waveguide can be excited at any point.

Figure 4 Schematic of two waveguides attached at a joint with  Figure 5 shows an example of a closed waveguide structure
j1,,4.
incident, reflected and transmitted waves (the number of  comprising four waveguides, each of length  L
j
waveguides conned to the joint could be arbitrary but here two
A point excitation is applied on waveguide 1, which generates
are shown for simplicity).
waves of amplitudes e. The amplitudes of these waves can
Vectors q and f  and matrices Φ ,  Ψ  and  R are now  be obtained directly from Equation (11). As for the amplitudes
|     |     |     |     | q,f | q,f |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
of the travelling waves, their amplitudes can be related to the
defined by concatenating the relevant vectors and matrices for
excited waves as
| the  individual  |     | waveguides  |     | (for  Φ | ,  Ψ |   and  | R,  the  |     |     |         |     |              |     |       |
| ---------------- | --- | ----------- | --- | -------- | ----- | ------ | -------- | --- | --- | ------- | --- | ------------ | --- | ----- |
|                  |     |             |     | q,f      |       | q,f    |          |     |     |         |     |              |     |       |
|                  |     |             |     |          |       |        |          |     | c  | e d | ,   | d e c.  |     | (24)  |
matrices are block-diagonal). The continuity and equilibrium
conditions can be used to formulate the scattering matrix as
The amplitudes of the incident and scattered waves are related
[37]
through the scattering matrices as
|     | sRΦ |     | RΦ | 1 RΦ |     | RΦ.  |       |     |       |     |      |       |       |       |
| --- | ------- | --- | ---- | ------- | --- | ------ | ----- | --- | ----- | --- | ---- | ----- | ----- | ----- |
|     |         |    | D   | q     | D  | q     | (20)  |     |       |     |      | s23 |       |       |
|     |         | f   | ii   |         | f   | ii     |       |     | s12  |    |      |       |      |       |
|     |         |     |      |         |     |        |       |     | a  | a | , b |     | b,  | (25)  |
s41
If the outgoing waves are incident upon the joint, then the   s34 
scattering matrix is
where

|     |     |     | a   |      | b |     |     |        |     |          |     |     |     |     |
| --- | --- | --- | ------ | ---- | ---- | --- | --- | ------ | --- | -------- | --- | --- | --- | --- |
|     |     |     | 1     |      |      | 1  |     |        |     | 100      |     |     |     |     |
|     |     |     |       |      |     |     |     |        |     |          |     |     |     |     |
|     |     | a  |   | , b |    | .  |     | (26)   |     |          |     |     |     |     |
|     |     |     |      |      |     |    |     |        |     | ]sN/m[ | |     |     |     |     |
|     |     |     | a     |      | b   |     |     |        |     |          |     |     |     |     |
|     |     |     |  4   |      |     | 4  |     |        |     |          |     |     |     |     |
yy
| Finally, in the unexcited waveguides (2, 3 and 4), the wave  |     |     |     |     |     |     |     |     |     | Y|   |     |     |     |     |
| ------------------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
| amplitudes are related through                               |     |     |     |     |     |     |     |     |     | 10-5 |     |     |     |     |
|                                                              |     |     |     |     |     |     |     |     |     | 101  |     |     | 102 | 103 |
L 
|     | a   |  τ  |     | b |         |           |     |        |     |     |     | Frequency [Hz] |     |     |
| --- | ------ | ------ | --- | ----- | --------- | --------- | --- | ------ | --- | --- | --- | -------------- | --- | --- |
|     | j1 | j      | j   |       | j         |           |     |        |     |     |     |                |     |     |
|     |       |        |     |     |          | , j2,3.  |     | (27)   |     | 100 |     |                |     |     |
|     | b     |        | τ   | L   | a        |           |     |        |     |     |     |                |     |     |
|     |  j   |    |     |     |  j1  |           |     |        |     |     |     |                |     |     |
|     |        |        |     | j j   |           |           |     |        |     | 50  |     |                |     |     |
]ged[ esahP
| where  |     |          |     |                 |      |          |     |       |     | 0   |     |     |     |     |
| ------ | --- | -------- | --- | --------------- | ---- | -------- | --- | ----- | --- | --- | --- | --- | --- | --- |
|        |     |          |     |                |      |         |     |       |     | -50 |     |     |     |     |
|        |     | xdiag |     | eik1  ,jx,,e | ikm |  j,jx   |     | (28)  |     |     |     |     |     |     |
τ
|     |     | j   |     |     |     |     |     |     |     | -100 |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- |
|     |     |     |     |     |     |     |     |     |     | 101  |     |     | 102 | 103 |
Frequency [Hz]
is the wave propagation matrix that gives the amplitudes of
the waves after travelling a distance x in the j-th waveguide.
Figure 6 Input mobility in the ydirection at x0.3 m on
For the excited waveguide (1 in Figure 5), these relations are
the lower beam: — analytical, -- WFE/FE.
|     |     | b τ x   | d,d | τ  | x b, |      |     |       |      |                  |     |     |     |     |
| --- | --- | ---------- | ------ | --- | ------- | ---- | --- | ----- | ---- | ---------------- | --- | --- | --- | --- |
|     |     | 4 1        | e      |     | 1 e     | 4    |     |       |      |                  |     |     |     |     |
|     |     |            |        |     |         |      |     | (29)  | 5.2  | Plate structure  |     |     |     |     |
|     |     | c τ Lx | a,a |     | τ Lx | c. |     |       |      |                  |     |     |     |     |
1 e 1 1 1 e Consider four plates that are connected at their edges to form
|            |       |          |       |      |     |         |            |      | a   | rectangular  | frame  | as  in Figure  | 5.  The  frame  | is  simply  |
| ---------- | ----- | -------- | ----- | ---- | --- | ------- | ---------- | ---- | --- | ------------ | ------ | -------------- | --------------- | ----------- |
| Equations  | (24)  | through  | (29)  | can  | be  | solved  | to  yield  | the  |     |              |        |                |                 |             |
supported at all the other edges. The plates are made of mild
| amplitudes  |     | of  the  | waves  | travelling  |     | through  | the  | whole  |     |     |     |     |     |     |
| ----------- | --- | -------- | ------ | ----------- | --- | -------- | ---- | ------ | --- | --- | --- | --- | --- | --- |
structure. Then, the response at any point of the waveguide  steel (material properties are given in the first example). The
plates have the same length L0.6, are 18 cm wide and 1.8
can be obtained straightforwardly [34].
mm thick.
5  NUMERICAL EXAMPLES
| In                                                         | this  section,  | three      | numerical  |             | examples  |     | are  presented.  |        |     |          |     |     |     |     |
| ---------------------------------------------------------- | --------------- | ---------- | ---------- | ----------- | --------- | --- | ---------------- | ------ | --- | -------- | --- | --- | --- | --- |
| Analytical                                                 |                 | solutions  | for        | the  first  | example,  |     | four             | Euler- |     |          |     |     |     |     |
| Bernoulli beams forming a rectangle, can be obtained. The  |                 |            |            |             |           |     |                  |        |     | ]sN/m[ | |     |     |     |     |
second example is of four simply supported plate strips also
|                                                             |     |     |     |     |     |     |     |     |     | zz 10-5 |     |     |     |     |
| ----------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------- | --- | --- | --- | --- |
| forming a rectangle and connected at line joints. The last  |     |     |     |     |     |     |     |     |     | Y|      |     |     |     |     |
example is of a cross-section of a train cabin where the hybrid
approach of Section  3.2 proves to be useful. In the following,  4000 10000 20000
Frequency [Hz]
all properties and dimensions are in SI units.
5.1  Beam structure
-500
| In this example, a rectangular beam structure is considered,  |     |     |     |     |     |     |     |     |     | ]ged[ esahP |     |     |     |     |
| ------------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- |
| Figure 5. The point joining every two beams has a mass of     |     |     |     |     |     |     |     |     |     | -1000       |     |     |     |     |
0.25 kg. The beams are made of mild steel with a density
|     |     |     |     |     | E200109, Poisson ratio  |     |     |     |     | -1500 |     |     |     |     |
| --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- |
7800, modulus of elasticity
|     |     |     |     |     |     |     |     |     |     | 4000 |     |     | 10000 | 20000 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- | --- | ----- | ----- |
0.3, and structural damping 0.03. The four beams  Frequency [Hz]

are identical and the width, thickness and length are b0.03,
Figure 7 Transfer mobility in the zdirection of the upper
h0.01 and L0.6 respectively. The beams are slender, so
plate: — full FE, -- WFE/FE.
Euler-Bernoulli beam theory is used (but other theories can be
Since the four plates are identical, then one WFE model is
equally used).
Since the beams are identical, then it is sufficient to obtain a  sufficient. This was obtained using a segment (with 0.02)
single WFE model. This is achieved via the FE model of a  of nine SHELL63 elements of ANSYS®. SHELL63 is a four-
single BEAM3 element of ANSYS® (0.01).BEAM3 is a
noded element with six DOFs per node. The segment has 20
two-noded element with 3 DOFs per node. The approach  nodes with a total of 120 DOFs. However, five DOFs are
removed from each of the four boundary nodes. Thus, the
presented in Section  3 and  4 is used to calculate the scattering
system to be processed as shown in Section  2 has 100 DOFs.
properties of the joints and subsequently find the response of
the structure. For comparison, the response can be obtained  For comparison, the whole structure is modelled with FE
analytically using a dynamic stiffness matrix approach, e.g.  using elements of the same size. The full FE model has 5992
DOFs. A unit amplitude force is applied normal to the lower
| [39]. A unit amplitude force in the  |         |          |        |        | ydirection is applied at  |           |       |      |           |                                                     |     |     |     |     |
| ------------------------------------ | ------- | -------- | ------ | ------ | -------------------------- | --------- | ----- | ---- | --------- | --------------------------------------------------- | --- | --- | --- | --- |
|                                      |         |          |        |        |                            |           |       |      | plate at  | 0.3,0.08, and the response of the upper plate is  |     |     |     |     |
| the                                  | middle  | of  the  | lower  | beam.  | Figure                     | 6  shows  | that  | the  |           |                                                     |     |     |     |     |
WFE/FE results are in good agreement with the analytical  observed at  0.5,0.08. The transfer mobility is shown in
results.

Figure 7. The WFE/FE results are in good agreement with the where possible). The FE model of the cell has 102 DOFs, but
full FE results. the internal DOFs can be condensed bringing down the size of
the FE model of the cell to 12 DOFs. The joints (also made of
5.3 Two-dimensional cross-section of train cabin
aluminium) are modelled using FE (with the same element
Train floor panels comprise panels with a truss-like core. length), and this results in an FE model of 111 DOFs. At low
These panels are usually made of aluminium with density frequencies, the truss-cored panel behaves like an orthotropic
2700, modulus of elasticity E 72109, Poisson ratio plate with an axial, shear and bending wave. At higher
frequencies, above 1100 Hz, the periodicity of the truss-core
0.34, and structural damping 0.03. Such a structure
in the x-direction becomes apparent and higher-order waves
is periodic in the xdirection and homogeneous in the
cut-on. These comprise motion in the face-plates and core
ydirection, Figure 8. The walls and ceiling of the train
webs which is difficult to divide into simple categories.
cabin are often of a similar construction.
10-4
100 101 102 103 104
Frequency [Hz]
Figure 8 Schematic of a train floor.
To illustrate the applicability of the developed approach for
studying the behaviour of such structures, the model of a
section in the ydirection will be developed, based on a
plain strain assumption. Thus, the section can be modelled
using beam elements of an equivalent modulus of elasticity
given as
E
E  . (30)
Equivelant 12
The results obtained will be valid per unit width. For
simplicity (and without any loss of generality), the walls and
ceiling are assumed to be identical to the floor with the joints
(also being identical) displayed in Figure 9. Each of the floor
and ceiling comprises 25 cells, whereas each of the two walls
comprises 20 cells.
Figure 9 Simplified cross-section of a train cabin.
The WFE model of the four waveguides (ceiling, floor, and
two walls) can be realised by modelling a single cell using
BEAM3 elements of ANSYS® (with an element length of 1cm
]sN/m[
|
Y|
xy
100
50
0
-50
-100
100 101 102 103 104
Frequency [Hz]
]ged[
esahP
Figure 10 Transfer mobility of the simplified train cabin: —
full FE, -- WFE/FE.
The approach presented in Section 4 is now used to
compute the scattering properties of the joints. Then, a point
force is applied to the lower waveguide at 1.3 m from its left
end. The response is observed at 1.3 m from the bottom end of
the right waveguide. For comparison, the whole cross-section
is modelled using FE with elements of the same size. This
yields a model of 4560 DOFs. The results of the WFE/FE
results, Figure 10, are in very good agreement with the full FE
results.
6 CONCLUSIONS
In this paper a hybrid wave finite element/finite element
(WFE/FE) approach for calculating the scattering properties
of joints is used to obtain the vibrational behaviour of a
waveguide structure. The waveguides are modelled using the
WFE method where the FE model of a small segment of the
waveguide is post-processed using periodic structure theory to
obtain the wave characteristics of the waveguide. The joints
are modelled using FE, and the WFE and FE models are
coupled to calculate the scattering properties of the joints.
Thus, the vibrational behaviour of the structure is described in
the wave domain which has many advantages. First, the
resulting models are smaller in size which becomes useful at
higher frequencies where FE models become impractical. On
the other hand, the knowledge of wave properties is useful for
other applications (statistical energy analysis, structure-borne
sound, disturbance propagation, etc). Numerical examples
were presented to illustrate the approach.

ACKNOWLEDGMENTS [23] K. H. Heron, Predictive sea using line wave impedences, in IUTAM
symposium on statistical energy analysis. 1997: Southampton, UK. p.
The authors gratefully acknowledge the financial support 107-118.
provided by the Engineering and Physical Sciences Research [24] S. A. Hambric, J. M. Cuschieri, C. R. Halkyard, B. R. Mace, and R. P.
Council under grant number EP/F069391/1 and the European Szwerc, Low-frequency measurements and predictions of the
structural-acoustic properties of the ince standard t-beam structure.
Commission in the context of the collaborative project “Mid-
Noise Control Engineering Journal, 2002. 50: p. 90-99.
Mod: Mid-frequency vibro-acoustic modelling tools- [25] Y. Waki, On the application of finite element analysis to wave motion
innovative CAE methodologies to strengthen European in one-dimensional waveguides. PhD thesis, Institute of Sound and
competitiveness” (Grant agreement number: 218508). Vibration Research, University of Southampton: Southampton (UK),
2007.
[26] S. P. Shone, A flexural wave scattering method for damage detection in
REFERENCES
beams. PhD thesis, Institute of Sound and Vibration Research,
[1] L. S. Beale and M. L. Accorsi, Power flow in two- and three- University of Southampton: Southampton (UK), 2006.
dimensional frame structures. Journal of Sound and Vibration, 1995. [27] B. R. Mace, D. Duhamel, M. J. Brennan, and L. Hinke, Finite element
185(4): p. 685-702. prediction of wave motion in structural waveguides. Journal of the
[2] D. W. Miller and A. von Flotow, A travelling wave approach to power Acoustical Society of America, 2005. 117(5): p. 2835 - 2843.
flow in structural networks. Journal of Sound and Vibration, 1989. [28] D. Duhamel, B. R. Mace, and M. J. Brennan, Finite element analysis of
128(1): p. 145-162. the vibrations of waveguides and periodic structures. Journal of Sound
[3] A. H. von Flotow, Disturbance propagation in structural networks. and Vibration, 2006. 294(1-2): p. 205 - 220.
Journal of Sound and Vibration, 1986. 106(3): p. 433-450. [29] L. Houillon, M. N. Ichchou, and L. Jezequel, Wave motion in thin-
[4] R. L. Sack, Matrix structural analysis. 1989, Boston, USA: PWS-Kent walled structures. Journal of Sound and Vibration, 2005. 281(3-5): p.
Publishing Company. 483 - 507.
[5] J. R. Banerjee and F. W. Williams, Coupled bending-torsional dynamic [30] M. Maess, N. Wagner, and L. Gaul, Dispersion curves of fluid filled
stiffness matrix for timoshenko beam elements. Computers and elastic pipes by standard fe models and eigenpath analysis. Journal of
Structures, 1992. 42: p. 301-310. Sound and Vibration, 2006. 296(1-2): p. 264 - 276.
[6] R. S. Langley, Analysis of power flow in beams and frameworks using [31] J.-M. Mencik and M. N. Ichchou, Wave finite elements in guided
the direct stiffness method. Journal of Sound and Vibration, 1990. 136: elastodynamics with internal fluid. International Journal of Solids and
p. 439-352. Structures, 2007. 44(7-8): p. 2148 - 2167.
[7] T. H. Richards and Y. T. Leung, An accurate method in structural [32] B. R. Mace and E. Manconi, Modelling wave propagation in two-
vibration analysis. Journal of Sound and Vibration, 1977. 55: p. 363- dimensional structures using finite element analysis. Journal of Sound
376. and Vibration, 2008. 318(4-5): p. 884 - 902.
[8] J. M. Cuschieri, Structural power-flow analysis using a mobility [33] E. Manconi and B. R. Mace, Wave characterization of cylindrical and
approach of an l-shaped plate. Journal of Acoustical Society of curved panels using a finite element method. Journal of the Acoustical
America, 1990. 87: p. 1159-1165. Society of America, 2009. 125(1): p. 154 - 163.
[9] G. Q. Cai and Y. K. Lin, Wave propagation and scattering in [34] Y. Waki, B. R. Mace, and M. J. Brennan, Numerical issues concerning
structural networks. Journal of Engineering Mechanics -- ASCE, 1991. the wave and finite element method for free and forced vibrations of
117: p. 1555-1574. waveguides. Journal of Sound and Vibration, 2009. 327(1-2): p. 92-
[10] J. F. Doyle, Wave propagation in structures: Spectral analysis using 108.
fast discrete fourier transforms. Second ed. Mechanical engineering [35] W. X. Zhong and F. W. Williams, On the direct solution of wave
series, ed. F.F. Ling. 2007, New York: Springer-Verlag. propagation for repetitive structures. Journal of Sound and Vibration,
[11] B. Chouvion, C. H. J. Fox, S. McWilliam, and A. A. Popov, In-plane 1995. 181(3): p. 485 - 485.
free vibration analysis of combined ring-beam structural systems by [36] W. X. Zhong, F. W. Williams, and A. Y. T. Leung, Symplectic analysis
wave propagation. Journal of Sound and Vibration, 2010. 329(24): p. for periodical electro-magnetic waveguides. Journal of Sound and
5087-5104. Vibration, 2003. 267(2): p. 227 - 244.
[12] B. Chouvion, A. A. Popov, S. McWilliam, and C. H. J. Fox, Vibration [37] J. M. Renno and B. R. Mace, A hybrid approach for the calculation of
modelling of complex waveguide structures. Computers & Structures. reflection and transmission coefficients of joints in waveguide
In Press, Corrected Proof. structures, in EURODYN2011, 8th International Conference on
[13] L. Cremer, M. Heckel, and B. A. T. Petersson, Structure-borne sound. Structural Dynamics. 2011: Leuven, Belgium.
third ed. 2005: Springer. [38] J. M. Renno and B. R. Mace, On the forced response of waveguides
[14] B. R. Mace, Wave reflection and transmission in beams. Journal of using the wave and finite element method. Journal of Sound and
Sound and Vibration, 1984. 72(2): p. 237-246. Vibration, 2010. 329(26): p. 5474-5488.
[15] B. R. Mace, Reciprocity, conservation of energy and some properties [39] J. R. Banerjee, Dynamic stiffness formulation and its application for a
of reflection and transmission coefficients. Journal of Sound and combined beam and a two degree-of-freedom system. Journal of
Vibration, 1992. 155(2): p. 375-381. Vibration and Acoustics, Transactions of the ASME, 2003. 125(3): p.
[16] Y. Young and Y. K. Lin, Dynamic response analysis of truss-type 351 - 358.
structural networks: A wave propagation approach. Journal of Sound
and Vibration, 1992. 156: p. 27-54.
[17] R. S. Langley and K. H. Heron, Elastic wave transmission through
plate/beam junctions. Journal of Sound and Vibration, 1990. 143(2): p.
241-253.
[18] I. Bosmans and T. Nightingale, Modeling vibrational energy
transmission at bolted junctions between a plate and a stiffening rib.
Journal of Acoustical Society of America, 2001. 109(3): p. 999-1010.
[19] S. J. Walsh and R. G. White, Vibrational power transmission in curved
beams. Journal of Sound and Vibration, 2000. 233(3): p. 455 - 488.
[20] E. C. N. Wester and B. R. Mace, Wave component analysis of energy
flow in complex structures - part i: A deterministic model. Journal of
Sound and Vibration, 2005. 285: p. 209-227.
[21] E. C. N. Wester and B. R. Mace, Wave component analysis of energy
flow in complex structures - part ii: Ensemble statistics. Journal of
Sound and Vibration, 2005. 285: p. 229-250.
[22] E. C. N. Wester and B. R. Mace, Wave component analysis of energy
flow in complex structures - part iii: Two coupled plates. Journal of
Sound and Vibration, 2005. 285: p. 251-265.