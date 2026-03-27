2DFQ: Two-Dimensional Fair Queuing for
Multi-Tenant Cloud Services
Jonathan Mace1, Peter Bodik2, Madanlal Musuvathi2, Rodrigo Fonseca1,
Krishnan Varadarajan2
1Brown University, 2Microsoft
ABSTRACT throughputforothers.Systemsinthepasthavesufferedcas-
Inmanyimportantcloudservices,differenttenantsexecute cadingfailures[19,27],slowdown[14,20,27,28,33],andeven
theirrequestsinthethreadpoolofthesameprocess,requiring cluster-wideoutages[14,19,27]duetoaggressivetenantsand
fairsharingofresources.However,usingfairqueueschedulers insufficientresourceisolation.
toprovidefairnessinthiscontextisdifficultbecauseofhighex- However, it is difficult to provide isolation in these sys-
ecutionconcurrency,andbecauserequestcostsareunknown temsbecausemultipletenantsexecutewithinthesameprocess.
andhavehighvariance.UsingfairschedulerslikeWFQand Consider the HDFS NameNode process, which maintains
WF2Qinsuchsettingsleadstoburstyschedules,wherelargere- metadatarelatedtolocationsofblocksinHDFS.Usersinvoke
questsblocksmallonesforlongperiodsoftime.Inthispaper, variousAPIsontheNameNodetocreate,rename,ordelete
weproposeTwo-DimensionalFairQueuing(2DFQ),which files,createorlistdirectories,orlookupfileblocklocations.
spreadsrequestsofdifferentcostsacrossdifferentthreadsand Asinmostsharedsystems,requeststotheNameNodewait
minimizestheimpactoftenantswithunpredictablerequests. inanadmissionqueueandareprocessedinFIFOorderbya
InevaluationonproductionworkloadsfromAzureStorage, setofworkerthreads.Inthissettingtenantrequestscontend
alarge-scalecloudsystematMicrosoft,weshowthat2DFQ forresources,suchasCPU,disks,orevenlocks,fromwithin
reducestheburstinessofserviceby1-2ordersofmagnitude. thesharedprocess.Asaresult,traditionalresourcemanage-
Onworkloadswheremanylargerequestscompetewithsmall mentmechanismsintheoperatingsystemandhypervisor
ones, 2DFQ improves 99th percentile latencies by up to 2 areunsuitableforprovidingresourceisolationbecauseofa
ordersofmagnitude. mismatchinthemanagementgranularity.
Inmanydomains,resourceisolationisimplementedusing
CCS Concepts
afairqueuescheduler,whichprovidesalternatingserviceto
•Networks→Cloudcomputing;Packetscheduling; competingtenantsandachievesafairallocationofresources
•Computersystemsorganization→Availability; overtime.FairschedulerssuchasWeightedFairQueuing[46],
whichwereoriginallystudiedinthecontextofpacketschedul-
Keywords
ing,canbeappliedtosharedprocessessincethesettingis
FairRequestScheduling;Multi-TenantSystems
similar:multipletenantssubmitflowsofshort-livedrequests
thatarequeuedandeventuallyprocessedbyaserveroflim-
1. INTRODUCTION
itedcapacity.However,insharedprocessestherearethree
Manyimportantdistributedsystemsandcloudservicesexe-
additionalchallengesthatmustbeaddressed:
cuterequestsofmultipletenantssimultaneously.Theseinclude
storage,configurationmanagement,database,queuing,and ● Resourceconcurrency:Threadpoolsinsharedprocesses
execute many requests concurrently, often tens or even
co-ordinationservices,suchasAzureStorage[9],Amazon
hundreds,whereaspacketschedulersareonlydesignedfor
Dynamo[16],HDFS[53],ZooKeeper[36],andmanymore.
sequentialexecutionofrequests(i.e.onanetworklink);
Inthiscontext,itiscrucialtoprovideresourceisolationto
ensurethatasingletenantcannotgetmorethanitsfairshare ● Largecostvariance:Requestcostsvarybyatleast4orders
ofmagnitudeacrossdifferenttenantsandAPItypes,from
ofresources,topreventaggressivetenantsorunpredictable
sub-millisecond to many seconds. By contrast, network
workloadsfromcausingstarvation,highlatencies,orreduced
packets only vary in length by up to 1.5 orders of mag-
Permissiontomakedigitalorhardcopiesofallorpartofthisworkforpersonal nitude(between40and1500bytes).UnlikeCPUthread
orclassroomuseisgrantedwithoutfeeprovidedthatcopiesarenotmadeor
schedulers,requestsarenotpreemptiblebytheapplication;
distributedforprofitorcommercialadvantageandthatcopiesbearthisnotice
andthefullcitationonthefirstpage.Copyrightsforcomponentsofthiswork ● Unknownandunpredictableresourcecosts:Theexecu-
ownedbyothersthantheauthor(s)mustbehonored.Abstractingwithcreditis tiontimeandresourcerequirementsofarequestarenot
permitted.Tocopyotherwise,orrepublish,topostonserversortoredistributeto
knownatscheduletime,aredifficulttoestimateupfront,
lists,requirespriorspecificpermissionand/orafee.Requestpermissionsfrom
permissions@acm.org. andvarysubstantiallybasedonAPItype,arguments,and
SIGCOMM’16,August22-26,2016,Florianopolis,Brazil transientsystemstate(e.g.,caches).Bycontrast,thelength
©2016Copyrightheldbytheowner/author(s).Publicationrightslicensedto ofeachnetworkpacketisknownaprioriandmanypacket
ACM.ISBN978-1-4503-4193-6/16/08...$15.00 schedulersrelyonthisinformation.
http://dx.doi.org/10.1145/2934872.2934878
DOI:

Thesechallengesaffectthequalityofschedulesproducedby A C AAAAAAAAAA C AAAAAAAAAA C A…
algorithmssuchasWeightedFairQueuing(WFQ)[46]and B D BBBBBBBBBB D BBBBBBBBBB D B…
(a)Burstyschedule
Worst-CaseFairWeightedFairQueuing(WF2Q)[6].Figure1a
showsanexampleofaburstyrequestschedulewhichdoes ABABABABABABABABABABABABABABABABABABABABABABABABABAB…
C D C D C D …
occurinpracticeasweverifyinourevaluation.Inthebursty (b)Smoothschedule
schedule,theserviceratesallocatedtotenantsAandBoscillate Figure1:Anillustrationofrequestexecutionovertimewithfourtenants
significantlybecauseCandDhavelargerequests.Mostfair sharingtwothreads.TenantsAandBsendrequestswith1secondduration
whiletenantsCandDwith10secondduration.Ineachschedule,rowsrep-
packetschedulersproducetheburstyschedule,despitethe
resentthethreadsovertimelabeledbythecurrentlyexecutingtenant.Both
existenceofthebettersmoothschedule.Thisoccursinpart schedulesarefair;overlongtimeperiods,alltenantsreceivetheirfairshare.
becausetheschedulersonlyquantifyandevaluatefairness Top:burstyschedule;smallrequestsreceivenoservicefor10secondperiods.
intermsofworst-casebounds,whichtheburstyandsmooth Bottom:smoothschedulewithonly1secondgapbetweentworequestsof
tenantAandB.SchedulerssuchasWFQ,WF2Q,orMSF2Qgeneratethe
schedulesbothsatisfy.Forexample,considerMSF2Q[8],a
burstyschedule;2DFQisdesignedtogeneratethesmoothschedule.
packetschedulerthatextendsWF2Qtomultipleaggregated
Thecontributionsofthispaperareasfollows:
networklinks(asettinganalogoustorequestschedulingin
workerthreadpools).MSF2Qboundsbyhowmuchatenant ● UsingproductiontracesfromAzureStorage[4,9],alarge-
canfallbehinditsfairsharetoN⋅L whereNisthenumber scalesystemdeployedacrossmanyMicrosoftdatacenters,
max
ofthreadsandL isthecostofthelargestrequest.Italso wedemonstrateschedulingchallengesarisingfromhigh
max
boundsbyhowmuchatenanticangetaheadofitsfairshare concurrencyandvariable,unpredictablerequestcosts;
toN⋅Li whereLi isthecostofi’slargestrequest.Worst- ● WeimproveuponexistingfairschedulerswithTwo-Dimen-
max max
case bounds are sufficient to avoid unacceptable bursts in sionalFairQueuing(2DFQ),arequestschedulerbasedon
packetscheduling,butinourcontexttheyareinsufficientdue WF2Qthatavoidsburstyschedulesbybiasingrequestsof
tolargeconcurrency(largeN)andlargecostvariance(large differentsizestodifferentthreads;
L ).Itmightnotbepossibletoimproveworstcasebounds ● Tohandleunknownrequestcostswepresent2DFQE,which
max
in theory, so instead we seek a scheduler that, in practice, extends2DFQ’scost-basedpartitioningwithpessimistic
achievessmootherschedulesonaverage. cost estimation to mitigate the impact of unpredictable
Thepracticalobstacletosmoothschedulesiscostestima- tenantsthatcauseburstyschedules;
tion.Insharedservices,requestcostsarenotknownatsched- ● Weevaluate2DFQand2DFQEwithextensivesimulations
uletime;insteadtheschedulermustestimatecostsbasedon basedonproductionworkloadtracesfromAzureStorage.
pastrequestsorsomeothermodel.However,requestcosts Wefindthat2DFQhasupto2ordersofmagnitudeless
aredifficulttopredictandestimatescouldbeoffbyorders variationinserviceratesforsmallandmediumrequests
ofmagnitude.Whenatenantsendsmanyexpensiverequests comparedtoWFQandWF2Q.Acrossasuiteof150experi-
estimatedtobeverycheap,theschedulercanstartthemto- ments,2DFQEdramaticallyreducesmeanandtaillatency,
gether,blockingmanyorallavailablethreadsforlongperiods byupto2ordersofmagnitudeforpredictableworkloads
oftime.Thusincorrectcostsleadtoburstyschedulesandhigh whentheycontendagainstlargeorunpredictablerequests.
latencies,particularlyfortenantswithsmallrequests.
2. MOTIVATION
Inthispaper,wepresentTwo-DimensionalFairQueuing
(2DFQ)1,arequestschedulingalgorithmthatproducesfair NeedforFine-GrainedResourceIsolation.Manyimportant
andsmoothschedulesinsystemsthatcanprocessmultiple datacenterservicessuchasstorage,database,queuing,andco-
requestsconcurrently.Oursolutionbuildsontwoinsightsto ordinationservices[9,30,36,53],aresharedamongmultiple
addressthechallengesabove.First,wetakeadvantageofthe tenantssimultaneously,duetotheclearadvantagesintermsof
concurrencyofthesystemandseparaterequestswithdifferent cost,efficiency,andscalability.Inmostofthesesystems,mul-
costsacrossdifferentworkerthreads.Thisway,largerequests tipletenantscontendwitheachotherforresourceswithinthe
donottakeoverallthethreadsinthesystemanddonotblock samesharedprocesses.Examplesincludeperformingmeta-
smallrequestsforlongperiodsoftime. Second,whenrequest data operations on the HDFS NameNode and performing
costsareunknownapriori,weusepessimisticcostestimation dataoperationsonHDFSDataNodes[53].
toco-locateunpredictablerequestswithexpensiverequests, Whentenantscompeteinsideaprocess,traditionaland
keepingthemawayfromtenantswithsmallandpredictable well-studiedresourcemanagementtechniquesintheoperat-
requestsforwhomtheywouldcauseburstyschedules. ingsystemandhypervisorareunsuitableforprotectingten-
2DFQproducessmoothscheduleslikethescheduleillus- antsfromeachother.Insuchcases,aggressivetenantscan
tratedinFigure1b,eveninthepresenceofexpensiveorun- overloadtheprocessandgainanunfairshareofresources.
predictabletenants.2DFQimprovesper-tenantservicerates Intheextreme,thislackofisolationcanleadtoadenial-of-
comparedtoexistingschedulerssuchasWFQ,WF2Qand servicetowell-behavedtenantsandevensystemwideoutages.
MSF2Q.Whileitkeepsthesameworst-caseboundsasMSF Forexample,eBayHadoopclustersregularlysuffereddenialof
2Q,2DFQproducesbetterschedulesintheaveragecaseby serviceattackscausedbyheavyusersoverloadingtheshared
avoidingburstyscheduleswherepossible. HDFSNameNode[20,34].HDFSusersreportslowdownfor
avarietyofreasons:poorlywrittenjobsmakingmanyAPI
1Two-dimensionalbecauseitschedulesrequestsacrossbothtime calls[33];unmanaged,aggressivebackgroundtasksmaking
andtheavailablethreads. toomanyconcurrentrequests[32];andcomputationallyex-

pensiveAPIs[28].Impala[37]queriescanfailonoverloaded Second,theschedulershouldnotbeburstywhenservicing
Kudu[41]clustersduetorequesttimeoutsandalackoffair differenttenants.Forexample,aschedulerthatalternatesbe-
sharing[38].Cloudstackuserscanhammerthesharedman- tweenextendedperiodsofservicingrequestsfromonetenant
agementserver,causingperformanceissuesforotherusers andthentheotherisunacceptableeventhoughthetwoten-
orevencrashes[14].Guoetal.[27]describeexampleswhere antsgettheirfairshareinthelongrun.Providingfairnessat
alackofresourcemanagementcausesfailuresthatcascade smallertimeintervalsensuresthattenantrequestlatencyis
intosystem-wideoutages:afailureinMicrosoft’sdatacenter morestableandpredictable,andmitigatestheaforementioned
whereabackgroundtaskspawnedalargenumberofthreads, challengeslikedenial-of-serviceandstarvation.
overloading servers; overloaded servers not responding to FairQueuingBackground.Awidevarietyofpacketsched-
heartbeats,triggeringfurtherdatareplicationandoverload. ulershavebeenproposedforfairlyallocatinglinkbandwidth
Giventheburdenonapplicationprogrammers,inevitably, amongcompetingnetworkflows.Theirgoalistoapproximate
manysystemsdonotprovideisolationbetweentenants,or thesharethatwouldbeprovidedunderGeneralizedProces-
onlyutilizead-hocisolationmechanismstoaddressindividual sorSharing(GPS)[46],constrainedinthatonlyonepacket
problemsreportedbyusers.Forexample,HDFSrecentlyintro- canbesentonthenetworklinkatatime,andthatpackets
ducedpriorityqueuing[29]toaddresstheproblemthat“any mustbetransmittedintheirentirety.Well-knownalgorithms
poorlywrittenMapReducejobisapotentialdistributeddenial- includeWeightedFairQueueing(WFQ)[46],Worst-caseFair
of-serviceattack,”butthisonlyprovidescoarse-grainedthrot- WeightedFairQueueing(WF2Q)[6],Start-TimeFairQueue-
tlingofaggressiveusersoverlongperiodsoftime.CloudStack ing(SFQ)[23],DeficitRound-Robin(DRR)[50],andmore.
addresseddenial-of-serviceattacksinrelease4.1,addingman- WebrieflydescribeWFQ.
uallyconfigurableupperboundsfortenantrequestrates[13]. WFQkeepstrackoftheworkdonebyeachtenantover
ArecentHBaseupdate[31]introducedratelimitingforoper- timeandmakesschedulingdecisionsbyconsideringthework
atorstothrottleaggressiveusers,butitreliesonhard-coded donesofarandcostofeachtenant’snextrequest.Totrack
thresholds,manualpartitioningofrequesttypes,andlacks fairshare,thesystemmaintainsavirtualtimewhichincreases
cost-basedscheduling.Intheseexamples,thedevelopersiden- bytherateatwhichbackloggedtenantsreceiveservice,for
tifymulti-tenantfairnessandisolationasanimportant,but example,for4tenantssharingaworkerthreadofcapacity100
difficult,andas-yetunsolvedproblem[10,38,47]. unitspersecond,virtualtimeadvancesatarateof25unitsper
ResearchprojectssuchasRetro[43],Pulsar[3],Pisces[52], second;for4tenantssharingtwoworkerthreadseachwith
Cake[60],IOFlow[54],andmore[61],provideisolationin capacity100unitspersecond,virtualtimeadvancesatarate
distributedsystemsusingratelimitingorfairqueuing.Rate of50unitspersecond;andsoon.Weuse A(rj )todenote
f
limiters,typicallyimplementedastokenbuckets,arenotde- thewallclockarrivaltimeofthe jth requestoftenant f atthe
signedtoprovidefairnessatshorttimeintervals.Depending server,andv(A(rj ))todenotethesystemvirtualtimewhen
f
onthetokenbucketrateandburstparameters,theycaneither therequestarrived.WFQstampseachrequestwithavirtual
underutilizethesystemorconcurrentburstscanoverloadit starttimeS(rj )andvirtualfinishtimeF(rj )asfollows:
f f
withoutprovidinganyfurtherfairnessguarantees.Fairqueu- S(rj )=max{v(A(rj )),F(rj−1 )} F(rj )=S(rj )+ l f j
ingisanappealingapproachtoprovidefairnessandisolation f f f f f ϕ
f
becauseitisrobusttodynamicworkloads.However,aswe where ϕ istheweightoftenant f and lj isthesizeofthe
f f
demonstratein§3,inmanysystems,requestcostscanvaryby request.Forasingletenant,thestarttimeofthe jth requestis
uptofourordersofmagnitudeandareunpredictable,which simplythefinishtimeofthe(j−1)threquest,unlessthetenant
cancausehead-of-lineblockingforsmallrequestsandsignifi- was inactive, in which case it fast-forwards to the current
cantlyincreaselatencies. systemvirtualtime.Eachtimeathreadisfreetoprocessa
DesirableProperties.Inthispaper,wecharacterizearesource request,WFQschedulesthependingrequestwiththelowest
isolationmechanismthatprovides“soft”guaranteesbyusing virtualfinishtime.
afairscheduler.Theschedulerattemptstosharetheresources Worst-case Fair Weighted Fair Queuing (WF2Q) [6] ex-
availablewithinaprocessequallyorinproportiontosome tendsWFQandiswidelyconsideredtohavebetterfairness
weightsamongtenantscurrentlysendingrequeststothesys- bounds.Theauthorsidentifyandaddressaprominentcause
tem.Incomingrequestsaresentto(logical)per-tenantqueues. of bursty schedules that can occur on a single networking
Thesystemrunsasetofworkerthreads,typicallyinthelow10s, link.WF2QrestrictsWFQtoonlyschedulerequestsafterthey
butsometimesinthe100s,toprocesstheserequests.Whena become eligible, with a request becoming eligible only if it
workerthreadisidle,itpicksthenextrequestfromoneofthe wouldhavebegunserviceinthecorrespondingGPSsystem,
per-tenantqueuesbasedonaschedulingpolicythatseeksto i.e.S(r)≤v(now).
provideafairsharetoeachofthetenants. Requestschedulingacrossmanythreadsisanalogousto
We specify two desirable properties of such a scheduler. packetschedulingacrossmultipleaggregatedlinks.Blanquer
Firstandforemost,theschedulershouldbeworkconserving— andÖzdenpreviouslyextendedWFQtomultipleaggregated
aworkerthreadshouldalwaysprocesssomerequestwhenit linksandexaminedthechangestoitsfairnessbounds,packet
becomesidle.Thispropertyensuresthattheschedulermax- delays, and work conservation [8]. While they termed the
imizestheutilizationofresourceswithinadatacenter.This algorithmMSFQ,weretainthenameWFQintheinterestof
requirementprecludestheuseofad-hocthrottlingmecha- familiarity,anduseWF2Qtorefertothenaïveworkconserv-
nismstocontrolmisbehavingtenants. ingextensionofWF2Qtomultipleaggregatedlinks.

A llllllllllllllllllllllllllllllllllllllllllllllllllll lllllllllllllllllllllllllllllllllllllll ll lllllll B llllllllllllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllllllllllllllllll l l Clll llllllllllllllllllllllllllllllllllllllllllll lllllllllllllllllllllllllllllllllllllllllllllllllllll D lllllllllllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllll l llllllllllllll ll E llllllllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllllllllllllllllllllllll
F llllllllllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllllllllllllllllllll ll G llllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllllllllllllllllllllllllllllll H lllllllllllllllllllllllllllllllllllllllllllllllllll lllllllllllllllllllllllllllllllllllllllllllllllll J ll llllllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllllllllllllllllll llllll
K llllllllllllllllllllllllll llllllllllllllllllllllllll
100 100010000100000 106 107
Cost [Anonymized Units]
IPA T1 lllllllllllllllllllllll llllllllllllllllllllllll l T2 lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll l l T3 lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllllllllllllllllllllllllllll l lll T4 llllllllllllllllllllllllll lllllllllllllllllllllllllll T5 llllllllllllllllllllll llllllllllllllllllllll T6 llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll lllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll ll llllll
T7 lllllllllllllllllllllllllllllllll lllllllllllllllllllllllllllllllll T8 llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllll T9 llllllllllllllllllllll llllllllllllllllllllll T10 llllllllllllllllllllllllllllllllllllllllll llllllllllllllllllllllllllllllllllllllllll T11 llll llllll lllllllllll lllllllllllllllllllll
T12 l l lllllllll lllllllllll
100 1000 10000100000 106
Cost [Anonymized Units]
(a)Costdistributionsfor10APIs.
tnaneT T1 lllllllllllllllllllllll llllllllllllllllllllllll l T5 llllllllll llllllllll T6 llllllllllllllll llllllllllllllll
T7 lllllllllllllllll llllllllllllllllll T10 llllllllllll llllllllllll T11 lllll llll l
100 1000 104 105 106 107
Cost [Anonymized Units]
(b)Costdistributionsfor12tenants.
Figure2:MeasurementsofAzureStorageshowwidelyvaryingrequestcosts.
Whiskersextendto1stand99thpercentiles;violinsshowdistributionshape.
3. CHALLENGES
Inthissectionwedescribetwochallengestoprovidingfair-
nessinsharedprocesses.Thefirstchallenge,describedin§3.1,
ariseswhenrequestswithlargecostvariancearescheduled
acrossmultiplethreadsconcurrently.Thesecondchallenge,
describedin§3.2,ariseswhenrequestcostsareunknownand
difficulttopredict.Todemonstratethechallengeswecollect
statisticsfrom5-minuteworkloadsamplesacross50produc-
tionmachinesofAzureStorage[4,9],alarge-scalesystem
deployedacrossmanyMicrosoftdatacenters.
3.1 High Request Cost Variability
Wefirstillustratehowrequestcostsinsharedservicesvary
widely,byupto4ordersofmagnitude.Forcost,wereportthe
CPUcyclesspenttoexecutetherequest,andanonymizethe
units.Othermetricsweconsideredincludewallclockexecu-
tiontimeanddominantresourcecost[21].
Figure2ashowsanonymizedcostdistributionsforseveral
differentAPIsinAzureStorage,illustratinghowsomeAPIs
areconsistentlycheap(A),somevarywidely(K),andsome
areusuallycheapbutoccasionallyveryexpensive(G).
Figure2bshowscostdistributionsforseveraldifferentten-
antsofAzureStorage,illustratinghowsometenantsonlymake
smallrequestswithlittlevariation(T ),sometenantsmake
1
largerequestsbutalsowithlittlevariation(T ),andsome
11
tenantsmakeamixtureofsmallandlargerequestswithalot
ofvariation(T ).
9
InaggregateacrossalltenantsandAPIs,requestcostsspan
fourordersofmagnitude—amuchwiderrangethannet-
work packets, for which most scheduling algorithms were
developed,wheresizesonlyvaryby1.5ordersofmagnitude
(between40and1500bytes).Highcostvarianceisnotunique
tothisproductionsystemandissharedbymanypopularopen-
sourcesystemsaswell:instorageandkey-valuestores,users
canreadandwritesmallandlargeobjects;indatabases,users
canspecifyoperationsthatscanlargetables;inconfiguration
andmetadataservices,userscanenumeratelargelistsand
directories.Alloftheseoperationscanhaveveryhighcost
comparedtotheaverageoperationsinthesystem.
AsillustratedinFigure1,bothburstyandsmoothschedules
arepossiblewhentherearemultipleworkerthreads.Bursty
schedulesadverselyaffecttenantswithsmallrequestsbyservic-
ingtheminhigh-throughputburstsratherthanevenlypaced
overtime.Sincerealisticsystemshavesuchhighcostvariance,
tnaneT
A E H
B G 8 n o 4 ati ari 2 V
nt
of 1
ci e 0.5 o effi 0.25 C 0.125
100 1000 104 105 106 107
Mean Request Size
Figure3:Left:costdistributionsofsometenantsusingAPIG,illustrating
variabilityacrosstenants.Right:scatterplotshowing,foreachtenantand
API,theaveragerequestcost(x-axis)andcoefficientofvariation(y-axis)
forthetenant’suseofthatAPI.Eachpointrepresentsonetenantonone
API,indicatedbycolor.EachAPIhastenantsusingitinpredictableand
unpredictableways.
tenantslikeT willexperiencelargeserviceoscillationsifthe
1
schedulerletstoomanyexpensiverequestsoccupythethread
pool.In§6weverifythatexistingschedulerslikeWFQand
WF2Qdoproduceburstyschedulesinpractice.
Ourinsighttogeneratingsmoothschedulesisthatgiven
thelargenumberofavailablethreads,wecanspreadrequests
ofdifferentcostsacrossdifferentthreads.Insomecasesitwill
bepreferabletoprioritizesmallrequestsinordertoprevent
longperiodsofblockingthatwouldoccurifweselecteda
largerequest.Wediscussthedetailsofourapproachin§4.
3.2 Unknown Request Costs
Tomotivatethesecondchallengeweillustratehowsome
tenantsaredynamic,withvaryingandunpredictablerequest
costs.Figure4showstimeseriesforT ,T ,andT ,illustrat-
2 3 10
ingrequestratesandcostsfortheAPIsbeingused.T (4a)
2
hasastablerequestrate,smallrequests,andlittlevariation
inrequestcost.T (4b)submitsalargeburstofrequeststhat
3
thentapersoff,withcostsacrossfourAPIsthatvarybyabout
1.5ordersofmagnitude.T (4c)isthemostunpredictable
10
tenant,withburstsandlullsofrequests,andcoststhatspan
morethanthreeordersofmagnitude.
EvenwithineachAPI,requestcostsvarybytenant.Forex-
ample,whileAPIGillustratedinFigure2ahasseveralorders
ofmagnitudebetweenits1%and99%requestcosts,ifwealso
conditiononthetenant,seeFigure3(left),mosttenantsusing
thisAPIactuallyhaveverylowcostvariance.Figure3(right)
showsthescatterplotofmeanandcoefficientofvariation
(CoV=mean/stdev)ofrequestcostsacrossmanytenants
andAPIs.ThefigureillustratesthateachAPIhastenantsusing
itinpredictableandunpredictableways.
Unknownrequestcostsareachallengetomakingeffective
schedulingdecisions,sincepacketschedulersneedtoknow
costsapriori.Asaworkaround,costscanbeestimatedbased
onpastrequestsorsomeothermodel.However,whilecost
estimationissuitableforstable,predictabletenants,itloses
effectivenessfordynamictenants.Modelscanbeinaccurate
sincecostsdependonnumerousfactors:theAPIbeingcalled,
its parameters, content of various caches, sizes of internal
objectsthattherequestmightprocess,etc.Estimatesbasedon
recentrequesthistory,suchasmovingaverages,onlyreflect
thepastandcanbeconsistentlywrongproportionaltohow
frequentlycostsvary.

|        | A B |     |         |             | B   | H   | J C |     |                     |             | G   | H   |     |             |
| ------ | --- | --- | ------- | ----------- | --- | --- | --- | --- | ------------------- | ----------- | --- | --- | --- | ----------- |
|  10000 |     |     |  600    |  10000      |     |     |     |     |  1000               |  1x107      |     |     |     |  200        |
| ]      |     |     |         | ]           |     |     |     |     |                     | Units]      |     |     |     |             |
| s it   |     |     |   5 0 0 | Units       |     |     |     |     |                     |             |     |     |     |             |
| Un     |     |     |         | Requests/s] |     |     |     |     |   8 0 0 Requests/s] |   1 x 1 0 6 |     |     |     | Requests/s] |
| zed    |     |     |         | mized       |     |     |     |     |                     | mized       |     |     |     |   1 5 0     |
|        |     |     |   4 0 0 |             |     |     |     |     |                     |             |     |     |     |             |
m i
| nony   |     |     |         | Anony        |     |     |     |     |   6 0 0          | Anony  1 0 0 0 0 0 |     |     |     |                |
| ------ | --- | --- | ------- | ------------ | --- | --- | --- | --- | ---------------- | ------------------ | --- | --- | --- | -------------- |
|  1000  |     |     |   3 0 0 | Rate [  1000 |     |     |     |     | Rate [           |                    |     |     |     |   1 0 0 Rate [ |
| A t [  |     |     |         | Cost [       |     |     |     |     |                  | Cost [             |     |     |     |                |
| Cos    |     |     |         | Request      |     |     |     |     |   4 0 0 Request  |   1 0 0 0 0        |     |     |     | Request        |
|        |     |     |   2 0 0 |              |     |     |     |     |                  |                    |     |     |     |                |
| t      |     |     |         | Request      |     |     |     |     |                  | Request            |     |     |     |                |
| Reques |     |     |         |              |     |     |     |     |                  |                    |     |     |     |   5 0          |
|        |     |     |         |              |     |     |     |     |   2 0 0          |   1 0 0 0          |     |     |     |                |
|        |     |     |   1 0 0 |              |     |     |     |     |                  |                    |     |     |     |                |
|  100   |     |     |  0      |  100         |     |     |     |     |  0               |  100               |     |     |     |  0             |
 0  5  10  15  20  25  30  0  5  10  15  20  25  30  0  5  10  15  20  25  30
|     | Time [s] |     |     |     |     |     | Time [s] |     |     |     |     | Time [s] |     |     |
| --- | -------- | --- | --- | --- | --- | --- | -------- | --- | --- | --- | --- | -------- | --- | --- |
(a)Stabletenant(T ) (b)Stablewithgradualchanges(T ) (c)Unstabletenantwithfrequentchanges(T )
|     |     | 2   |     |     |     |     |     | 3   |     |     |     |     |     | 10  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure4:DetailsofthreeAzureStoragetenantsovera30secondinterval.EachcolorrepresentsadifferentAPIlabeledconsistentlywithFigure2a.Points
representindividualrequestswiththeircostsonthelefty-axis.Linesrepresenttheaggregaterequestrateduring1secondtimeintervals(righty-axis).
Incorrectcostestimatesleadtoburstyschedules.Theyoc-
|     |     |     |     |     |     |     | W1 a1 | b1 a2 | b a3 | b a4 b | a5 b a6 | b a7 b | a8 b | a9 … |
| --- | --- | --- | --- | --- | --- | --- | ----- | ----- | ---- | ------ | ------- | ------ | ---- | ---- |
curwhenanexpensiverequestmasqueradesasacheaprequest 2 3 4 5 6 7 8
|                                                   |     |     |     |     |     |     | W0  | c   |     | d   | c   | d   |     | c3 … |
| ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ---- |
| andisscheduledasthoughitischeap,blockingitsworker |     |     |     |     |     |     |     | 1   |     | 1   | 2   |     | 2   |      |
(a)Idealrequestscheduleovertimeontwothreads
threadforlongerthanexpected.Whenaburstofthesere-
|     |     |     |     |     |     |     | R e | q u es t a 1 | a 2 a 3 | a 4 a 5 a 6 | a 7 a 8 a 9 | R e q | u es t c 1 c | 2 c 3 |
| --- | --- | --- | --- | --- | --- | --- | --- | ------------ | ------- | ----------- | ----------- | ----- | ------------ | ----- |
questsoccurs,theycanblockmanyorallworkerthreadsfora Sta r t  T im e 0 1 2 3 4 5 6 7 8 Sta r t  T im e 0 4 8
|     |     |     |     |     |     |     |     |     |     |     |     | …   |     | …   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
longperiodoftime,impactingthelatencyofallotherwaiting Finish Time 1 2 3 4 5 6 7 8 9 Finish Time 4 8 12
tenants.Thechallengeisorthogonaltotheschedulingstrategy Request b1 b b b b b b b b9 Request d d d3
|     |     |     |     |     |     |     |            |     | 2 3 | 4 5 6 | 7 8   |              | 1   | 2     |
| --- | --- | --- | --- | --- | --- | --- | ---------- | --- | --- | ----- | ----- | ------------ | --- | ----- |
|     |     |     |     |     |     |     | Start Time | 0   | 1 2 | 3 4 5 | 6 7 8 | … Start Time | 0   | 4 8 … |
–itaffectsnotonlyexistingschedulers,butalsonewschedulers Finish Time 1 2 3 4 5 6 7 8 9 Finish Time 4 8 12
designedtoaddressthecostvariabilitychallengeof§3.1. (b)RequeststartandfinishtimesforWFQandWF2Q
Feedbackdelaysexacerbatetheimpactofunderestimates.
|     |     |     |     |     |     |     | W1 b | 1 b 2 b | 3 b 4 | d 1 | b 5 b 6 b 7 | b8  | d 2 | b 9 … |
| --- | --- | --- | --- | --- | --- | --- | ---- | ------- | ----- | --- | ----------- | --- | --- | ----- |
Consideranestimatorbasedonper-tenantmovingaverages, W0 a1 a2 a3 a4 c 1 a5 a6 a7 a8 c 2 a9 …
(c)RequestscheduleproducedunderWFQ
atypicalapproachtoestimatingrequestcosts[3,42,43,51,52].
| Thereisaninherentfeedbackdelaybetweenestimatingare- |     |     |     |     |     |     |       |     | d   |             | d   |       |         |      |
| --------------------------------------------------- | --- | --- | --- | --- | --- | --- | ----- | --- | --- | ----------- | --- | ----- | ------- | ---- |
|                                                     |     |     |     |     |     |     | W1 b1 |     | 1   | b 2 b 3 b 4 | b 5 | 2 b 6 | b 7 b 8 | b9 … |
| quest’scostandeventuallyupdatingtheestimatorwiththe |     |     |     |     |     |     |       |     | c   |             | c   |       |         |      |
|                                                     |     |     |     |     |     |     | W0 a1 |     | 1   | a2 a3 a4    | a5  | 2 a6  | a7 a8   | a9 … |
(d)RequestscheduleproducedunderWF2Q
actualcostoncetherequestfinishes.Ifatenanttransitions
fromcheaptoexpensiverequeststhentheschedulerwillin- Figure5:ExampleschedulescomparingWFQandWF2Qtotheidealsched-
correctlyschedulenotjustonerequest,butpotentiallyuptoN uleforfourtenantssharingtwoworkerthreads.TenantsAandBhavere-
questsize1;tenantsCandDhaverequestsize4.Seedescriptionin§4.
| requests(whereN | isthenumberofthreads),sincetheexpen- |     |     |     |     |     |     |     |     |     |     |     |     |     |
| --------------- | ------------------------------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
sivecostswon’tbereflectedbackintheestimatoruntilafter
outlinesthedesignof2DFQ,arequestschedulerforknownre-
oneoftheexpensiverequestshascompleted.Whileabursty
questcosts;in§5wepresent2DFQE,aschedulerforunknown
scheduleisinevitablewhenatenanttransitionsfromcheap
requestcosts.
toexpensiverequests,inthisscenarioitcanbesignificantly
WebeginbydemonstratinghowWFQandWF2Qproduce
amplified.Thetenantwillalsodeviatefromitsfairshareun-
burstyschedules.Considerfourbackloggedtenants(A...D)
lesstheschedulerreconcilestheerrorbetweeneachrequest’s
|                         |     |     |     |     |     |     | sharingtwoworkerthreads(W |     |     |     | andW).TenantsAandB |     |     |     |
| ----------------------- | --- | --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | ------------------ | --- | --- | --- |
| estimatedandactualcost. |     |     |     |     |     |     |                           |     |     |     | 0                  | 1   |     |     |
havesmallrequests(size1),whiletenantsCandDhavelarge
Ourinsighttogeneratingsmoothschedulesunderunknown
|     |     |     |     |     |     |     | requests | (size | 4). Figure | 5a illustrates |     | an ideal | schedule | of  |
| --- | --- | --- | --- | --- | --- | --- | -------- | ----- | ---------- | -------------- | --- | -------- | -------- | --- |
requestcostsstemsfromthefollowingobservations.Ifthe
schedulerunderestimatesarequest’scost,thentherequest requestsoverthreadsinthisscenario.
Figure5boutlinesthevirtualstartandfinishtimesusedby
canblockthethreadpoolforalongperiodoftimeleading
WFQandWF2Q.Figure5cillustratestheresultingschedule
toburstyschedulesforothertenants.However,ifthesched-
forWFQ.SinceWFQschedulesrequestsinascendingorderof
| uler overestimates | a request’s | cost, | it only | immediately |     | af- |     |     |     |     |     |     |     |     |
| ------------------ | ----------- | ----- | ------- | ----------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
finishtime,itusesboththreadstoexecute4requestseachfor
fectstheonetenantthatwasforcedtowaitforlongerthanit
AandB.Onlyatt=4doCandDhavethelowestfinishtime
shouldhave.Sinceworkloadstypicallycontainamixtureof
causingWFQtosimultaneouslyexecuteonerequesteachfor
predictableandunpredictabletenants,itisbettertogivegood
CandD,occupyingthethreadpooluntilt=8.Thisschedule
servicetoapredictabletenantthantotry–andfail–togive
isburstyforAandB,becausetheyeachgetaperiodofhigh
goodservicetoanunpredictabletenant.Inordertoprevent
throughputfollowedbyaperiodofzerothroughput.Ingen-
unpredictabletenantsfrominterferingwithpredictableten-
eral,WFQ’sburstsareproportionaltothemaximumrequest
ants,wetrytoreducethechanceofunderestimatingrequest
|     |     |     |     |     |     |     | size(i.e.,thesizeofC |     |     | andD’srequests)andthenumberof |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | -------------------- | --- | --- | ----------------------------- | --- | --- | --- | --- |
costs.Wediscussthedetailsofourapproachin§5.
tenantspresent(i.e.,doublingthenumberoftenantswould
doubletheperiodofblocking).
4. TWO-DIMENSIONALFAIRQUEUING
Figure5dillustratestheresultingscheduleunderWF2Q
ThegoalofTwo-DimensionalFairQueuing(2DFQ)isto whichalsohasperiodsofblockingproportionaltomaximum
producesmoothschedulesfortenantswithsmallrequests,by requestsize.WF2Qalsoschedulesrequestsinascendingorder
minimizingburstinessovertimeandoverspace.Thissection offinishtime,butwiththeadditionalconditionthatarequest

cannotbescheduledifitsvirtualstarttimehasnotyetarrived. Request a1 a2 a3 a4 a5 a6 a7 a8 a9 Request c c c3
1 2
Asaresult,WF2QdoesnotschedulethesecondrequestsofA Eligible W 0 1 2 3 4 5 6 7 8 Eligible W 0 4 8
|     |     |     |     |     |     | 0   |     |     |     | …   | 0   | …   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
orB–theirvirtualstarttimeis1,whichmeanstheycannot Eligible W 1 -0.5 0.5 1.5 2.5 3.5 4.5 5.5 6.5 7.5 Eligible W 1 -2 2 6
|     |     |     |     |     |     | Request b1 | b 2 b 3 | b 4 b 5 b | 6 b 7 b | 8 b9 | Request d 1 d | 2 d3 |
| --- | --- | --- | --- | --- | --- | ---------- | ------- | --------- | ------- | ---- | ------------- | ---- |
bescheduleduntilt=2.TheonlyremainingrequestsforWF Eligible W 0 1 2 3 4 5 6 7 8 Eligible W 0 4 8
|     |     |     |     |     |     | 0   |     |     |     | …   | 0   | …   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
2QtopickarethoseofCandD.LikeWFQ,WF2Qproduces Eligible W -0.5 0.5 1.5 2.5 3.5 4.5 5.5 6.5 7.5 Eligible W -2 2 6
|     |     |     |     |     |     | 1   |     |     |     |     | 1   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
aburstyschedulethatalternatesbetweenconcurrentservice (a)Modifiedeligibilitytimesunder2DFQ
forAandB,followedbyconcurrentserviceforCandD. W1 b1 a2 b 2 a3 b 3 a4 b 4 a5 b 5 a6 b 6 a7 b 7 a8 b 8 a9 b9 …
|     |     |     |     |     |     | a1  | c   | d   |     | c   | d   |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
BurstinessoccursunderWF2Qwhenmultipleworkerthreads W0 1 1 2 2 …
(b)Requestscheduleproducedunder2DFQ.
| become available | and only large | requests | are eligible | to be |     |     |     |     |     |     |     |     |
| ---------------- | -------------- | -------- | ------------ | ----- | --- | --- | --- | --- | --- | --- | --- | --- |
scheduled.Sinceeachrequestisinstantaneouslyeligibleto Figure6:Schedulefor2DFQfortheexampledescribedin§4andFig.5.
runonallworkerthreadswhenitsvirtualstarttime S(r ) 5. SCHEDULING REQUESTS WITH
j
arrives,ifsmallrequestsareineligibleforonethreadthenthey
|     |     |     |     |     |     | UNKNOWN |     | COST |     |     |     |     |
| --- | --- | --- | --- | --- | --- | ------- | --- | ---- | --- | --- | --- | --- |
willbeineligibleforallthreads.Thekeyto2DFQistobreak
Thissectionoutlinesthedesignof2DFQE,whichextends
thistie.2DFQmodifiesWF2Q’seligibilitycriteriontomakea
2DFQwithmechanismsforeffectivelydealingwithunknown
requesteligibleatdifferenttimesfordifferentworkerthreads,
requestcosts.Weoutlinethepessimisticestimationstrategy
avoidingWF2Q’s“allornothing”behavior.2DFQuniformly
staggerseachrequest’seligibilityacrossthreads,makingthem of2DFQEaswellastwopracticalbookkeepingmechanisms
–retroactivechargingandrefreshcharging–formanaging
eligibletorunonhigh-indexthreadssoonerthanlow-index
unpredictablerequestcosts.
| threads.Formally,inasystemwithnthreads,r |     |     | iseligibleon |     |     |     |     |     |     |     |     |     |
| ---------------------------------------- | --- | --- | ------------ | --- | --- | --- | --- | --- | --- | --- | --- | --- |
j
threadi atvirtualtimeS(r i ×l where0≤ i n.This Bookkeeping:RetroactiveCharging Sincerequestcostsaren’t
|                           | j )−   |      | j <                |     |                                                     |     |     |     |     |     |     |     |
| ------------------------- | ------ | ---- | ------------------ | --- | --------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
|                           |        | n    |                    | lj. | knownapriori,mostschedulersupdatecountersatschedule |     |     |     |     |     |     |     |
| staggerstheeligibilityofr | j acro | ssth | readsinintervalsof |     |                                                     |     |     |     |     |     |     |     |
n
OnceS(r )arrives,r willbeeligibleonallworkerthreads. timeusinganestimateofthecost,forexampleusingamoving
| j   | j   |     |     |     |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Withthesemodifiedeligibilitycriteria,eachworkerthread averagethatisupdatedwhenrequestscomplete.Forsched-
hasadifferentthresholdforwhenarequestwillbecomeeligi- ulersbasedonvirtualtime(cf.§2)thisisl ,usedtocalculate
r
|                                                     |     |     |     |     | finishtimes:F(r)=S(r)+l |     |     |     | /ϕ . |     |     |     |
| --------------------------------------------------- | --- | --- | --- | --- | ----------------------- | --- | --- | --- | ---- | --- | --- | --- |
| ble;whileonethreadmightfindthatonlylargerequestsare |     |     |     |     |                         |     |     |     | r f  |     |     |     |
eligible,otherthreadsmightstillseeeligiblesmallrequests Schedulingonlybasedonestimatescanleadtoarbitrary
andselectthoseinstead.Thepracticaleffectof2DFQistopar- unfairnessinsystemswheremultiplerequestscanexecute
concurrently.Forexample,supposeweusethecostofthemost
titionrequestsacrossthreadsbysize.Smallrequestsbecome
eligibleonhigh-indexthreadsfirstandtendtobedequeued recentlycompletedrequestasourestimate.Theninathread
andservicedonthosethreadsbeforetheyareevereligiblefor poolwithnthreads,anytenantcanachieveapproximatelyn
timestheirfairsharebyalternatingbetweenonesmallrequest
low-indexthreads.Ontheotherhand,duetothelackofeligi-
ofsize1,followedbynconcurrentlargerequestsofsizek.The
blesmallrequests,low-indexthreadsendupmostlyservicing
largerequests. schedulerwouldpredictsizenforthesmallrequest,andsize1
Returningtothepreviousexample,Figure6aoutlinesthe forthelargerequests,therebychargingn+kforkn+1work.
Retroactivechargingensuresthatatenantiseventuallychar-
modifiedeligibilitytimesofrequestsunder2DFQ,whichare
nowdifferentforW andW.Figure6billustratestheschedule gedfortheresourcesitactuallyconsumedandnotjustour
0 1
under2DFQ.Thistime,thesecondrequestsofAandBwill aprioriestimate.Thesystemmeasurestheresourceusagec
r
|                  |                   |     |                     |     | ofeach | request,and |     | reportsit | back | to the | schedulerupon |     |
| ---------------- | ----------------- | --- | ------------------- | --- | ------ | ----------- | --- | --------- | ---- | ------ | ------------- | --- |
| notbeeligibleonW | 0 untilt=2,butonW |     | 1 theyareeligibleat |     |        |             |     |           |      |        |               |     |
t=1.Asaresult,2DFQschedulesc onW ,butselectsa for completion. If c r > l r , we charge the tenant for its excess
|     |     | 1   | 0   | 2   |     |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
W .Thereafter,AandBcontinuealternatingrequestsonW . consumption; if c < l , we refund the tenant for unused
| 1   |     |     |     | 1   |     |     | r   | r   |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Thefollowingtheoremshowsthat2DFQisfairbyproving resources.Todothisweadjustthetenant’sstartandfinish
|     |     |     |     |     | tagsbyc | −l  | .Regardlessoftheinitialestimatel |     |     |     | ,retroactive |     |
| --- | --- | --- | --- | --- | ------- | --- | -------------------------------- | --- | --- | --- | ------------ | --- |
a bound on how far tenants can fall behind the fair share r r r
providedbytheidealfluidGPSserver. chargingeventuallyreconcilestheerrorbetween l and c ,
|     |     |     |     |     |     |     |     |     |     |     | r   | r   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
therebyguaranteeingthatthetenantwillreceiveitstruefair
f
Theorem 1. Atanyinstantt,ifW (0,t)representsthe shareofresourcesinthelongrun.
2 DFQ
| amountofresourcesconsumedbytenant        |     |     | f under2DFQand |     |                           |             |             |     |                          |     |                |     |
| ---------------------------------------- | --- | --- | -------------- | --- | ------------------------- | ----------- | ----------- | --- | ------------------------ | --- | -------------- | --- |
|                                          |     |     |                |     | PessimisticCostEstimation |             |             |     | Itisimportanttohaveagood |     |                |     |
| Wf (0,t)representstheresourcesconsumedby |     |     | f underGPS,    |     |                           |             |             |     |                          |     |                |     |
| GPS                                      |     |     |                |     | cost                      | estimatorto | avoidbursty |     | schedules                | in  | the shortterm. |     |
then
Followingfrom§3.2,wearemostconcernedaboutthecase
Wf (0,t)−Wf (0,t)≤N×Lmax whenourcostestimateforatenantislowandittransitions
GPS 2DFQ
|     |     |     |     |     | toexpensiverequests;i.e.l |     |     |     | ≪c .Iftheschedulermistakenly |     |     |     |
| --- | --- | --- | --- | --- | ------------------------- | --- | --- | --- | ---------------------------- | --- | --- | --- |
|     |     |     |     |     |                           |     |     | r   | r                            |     |     |     |
whereN isthenumberofthreadsandLmax isthemaximum estimatesanexpensiverequesttobecheap,theexpensivere-
resourceconsumedbyanyrequestinthesystem.
questcanoccupyaworkerthreadforsignificantlylongerthan
Proof. Theprooffollowsfromthecorrespondingtheorem theschedulermayhaveanticipated.Iftheschedulermistak-
forMSFQ(Theorem3in[8])andthefactthataddingaregu- enlyestimatesmultipleexpensiverequeststobecheap,then
latordoesnotmodifythisbound(Theorem1in[6])provided theycanconcurrentlyblockpartofallofthethreadpool.This
theregulatormakesarequesteligibleforscheduleatorbefore willcauseaburstofservicetothistenantfollowedbyalull
thestarttimeoftherequestintheGPSserver.Theeligibility oncetheschedulerincorporatesthetruecostandcompen-
conditionof2DFQhasthisproperty. satesothertenantsforthisaggressiveallocation.Theduration

1: procedureEnqueue(rj) ▷request joftenant f 19: procedureDequeue(i) ▷dequeuetothreadi
f
2: if f ∉Athen 20: E now ←{f ∈A∶S f − n iL m f ax <v(now)}
3: A←A∪ f 21: f∗← f ∈E
now
withsmallestS
f
+L
m
f ax/ϕ
f
4: S f ←max(S f ,v(now)) 22: r f j ∗ ←Pop(Q f∗) ▷requesttorun
5: endif 23: c
f
j
∗
=L
m
f∗
ax
▷rememberhowmuchwepaidforr
f
j
∗
6: Push(Q f ,r f j ) ▷enqueuer f j 24: S f∗ =S f∗+L m f∗ ax/ϕ f∗
7: endprocedure 25: returnrj
f∗
26: endprocedure
8: procedureRefresh ▷runsperiodically
9: for rj ∈Runningrequests do 27: procedureComplete(rj) ▷Servicewascompleted
f f
10: c←newresourceusage 28: c←newresourceusage
11: if c<cj then ▷alreadypaidforc 29: T←totalresourceusageofrj
f f
12: c
f
j ←c
f
j −c 30: L
m
f
ax
←max(αL
m
j
ax
,T) ▷updateL
m
j
ax
13: else ▷notpaidyet,chargethetenant 31: S
f
←S
f
+(c−c
f
j )/ϕ
f
▷reconcileusage
14: S
f
←S
f
+(c−c
f
j )/ϕ
f
32: if∣Q f∣=0then
15: cj ←0 33: A←A∖ f
f
16: endif 34: endif
17: endfor 35: endprocedure
18: endprocedure
Figure7:2DFQEonnthreads.Aisthesetofactivetenants.cj keepstrackofhowmuchcreditwehaveleftforthisrequest.Itisinitializedonline23basedon
thecostestimatewechargethetenantanditisupdateddurin f gRefresh;foreachnewmeasurementofrequestrj,ifwestillhavecredit,wesubtractfromit
f
(line12),otherwiseweincreasetenant’sclockforward(line14).Aftercompletionofrequest,wereconcilethefinalresourcemeasurementwiththeremaining
creditonline31.Weupdatetheper-tenantLf estimateonline30,anduseitforeligibilityandfinishtimecalculationonlines20and24.
max
oftheburstisproportionaltoc –thelongertherequest,the tenantswithcheaprequestswillmaintainlowerestimatesand
r
longer it will take to incorporate the true cost back in the remainonthehigh-indexthreads.Theαparameterallowsus
schedulerandthelongerothertenantswillbeblocked. totunethetrade-offbetweenhowaggressivelyweseparate
Wearelessconcernedwiththeotherextremewhenaten- predictabletenantsfromunpredictableones,andhowmuch
ant’scostestimateishighandittransitionstocheaprequests; leewayatenanthastosendtheoccasionalexpensiverequest.
i.e. l r ≫ c r . If the scheduler mistakenly estimates a cheap Bookkeeping: Refresh Charging When a tenant submits
requesttobeexpensive,thentheschedulermightdelaythe cheap requests for a sustained period of time, 2DFQE will
requestforlongerthannormal.However,onceitisscheduled besusceptibletounderestimationifthetenanttransitionsto
therequestwillnotoccupyaworkerthreadforanylonger expensiverequests.Whenthishappens,Li willbealow
max
thanthescheduleranticipated,sotherequestwillnotcause valuethatunderestimatestheexpensiverequestsuntiltheir
burstiness to other tenants. The effect will only persist for costcanbeincorporatedintotheestimator.Asweoutlinedin
ashortdurationsincethecheaprequestscompletequickly. §3.2,uptoN underestimatedrequestscanrunconcurrently
Retroactivechargingwillrefundtheunusedcosttothetenant duetothislargefeedbackdelayinupdatingtheestimator.
therebyguaranteeingthatitwillreceiveitsfairshareofservice Refreshchargingisa‘damagecontrol’mechanismthatperi-
inthelongrun.Mostimportantly,overestimationdoesnot odicallymeasurestheresourceusageoflong-runningrequests
causeprolongedthreadpoolblockingforothertenants. andincorporatesmeasurementsintotheschedulerimmedi-
Withknowncosts(§4)2DFQspreadsrequestsacrossthreads ately.Itletsusnoticeexpensiverequestsquicklyandimme-
by size, a property we take advantage of to handle unpre- diatelychargethetenantfortheexcesscostwhiletherequest
dictablecosts.Sinceworkloadscontainamixofpredictable isstillrunning,short-circuitingthetypicalcostestimation
andunpredictabletenants,welimittheimpactofunpredictable feedbackloop.Thecomputationaloverheadformeasuringre-
tenantsbytreatingthemasiftheyareexpensive.Webiasun- sourceconsumptionisnon-negligible,sotheschedulermust
predictabletenantstowardslow-indexthreadstokeepthem strikeabalancebetweenfrequentmeasurementsandaccept-
awayfromsmallrequestsonhigh-indexthreads.2DFQEuses ableoverheads.Inpracticewefoundthatrefreshcharging
apessimisticcostestimatorthatoverestimatescostsasfollows: every10mshadnosignificantoverhead.
individuallyforeachtenantoneachAPI,ittracksthecost
Algorithm Wesummarize2DFQEinFigure7.
ofthelargestrequest,Li ;afterreceivingthetruecostmea-
max
surementc ofajust-completedrequest,ifc >Li ,weset
r r max
Li =c ,otherwisewesetLi =αLi ,whereα<1,but 6. EVALUATION
max r max max
closeto1.Ineffect,2DFQEpenalizesunpredictabletenants
Inthissection,weevaluatethefollowinggoals:that2DFQ
thatrepeatedlyvarybetweencheapandexpensiverequestsby
providessmoothservicetoalltenantswhenrequestcostsare
justtreatingallrequestsasexpensive.Requestswillrunonlow-
known,despitethepresenceofexpensiverequests;andthat
indexthreadsmixedinamongexpensiverequests.Theywill
2DFQEprovidessmoothservicetopredictabletenantswhen
notrunonthehigh-indexthreadsandtherebynotinterfere
request costs are unknown, despite the presence of unpre-
withothertenants’smallrequests.Ontheotherhand,stable
dictablerequests.

| WFQ | WF²Q | 2 DFQ |        111111 012345 |     |     |     |  0.6 |     |     |
| --- | ---- | ----- | -------------------- | --- | --- | --- | ---- | --- | --- |
W F Q
Q
| e   3 0 0 |     |     | F            0123456789 |     |     |     | W F ² Q |     |     |
| --------- | --- | --- | ----------------------- | --- | --- | --- | ------- | --- | --- |
| at        |     |     | W                       |     |     |     |   0 . 5 |     |     |
| R         |     |     |                         |     |     |     | 2 D F Q |     |     |
e    2 0 0
| c          |     |     |                          |     |     |     | g)        |     |     |
| ---------- | --- | --- | ------------------------ | --- | --- | --- | --------- | --- | --- |
| vi         |     |     |        111111 012345     |     |     |     | a   0 . 4 |     |     |
| er   1 0 0 |     |     |                          |     |     |     | L         |     |     |
| S          |     |     | Q                        |     |     |     | e         |     |     |
|   0        |     |     | F²            0123456789 |     |     |     | c   0 . 3 |     |     |
vi
|  0  |  5  |  1 0 |  15 W |     |     |     | er  |     |     |
| --- | --- | ---- | ----- | --- | --- | --- | --- | --- | --- |
s)
| g (   2 |     |     |                        |     |     |     | S   0 . 2 |     |     |
| ------- | --- | --- | ---------------------- | --- | --- | --- | --------- | --- | --- |
|         |     |     |        111111 012345   |     |     |     | σ(        |     |     |
a   1
| L     |     |     | Q                       |     |     |     |         |     |     |
| ----- | --- | --- | ----------------------- | --- | --- | --- | ------- | --- | --- |
| e     |     |     | F            0123456789 |     |     |     |   0 . 1 |     |     |
| c   0 |     |     | D                       |     |     |     |         |     |     |
| vi    |     |     | 2                       |     |     |     |         |     |     |
er - 1
| S   |          |     |      |          |     |     |   0                             |         |              |
| --- | -------- | --- | ---- | -------- | --- | --- | ------------------------------- | ------- | ------------ |
| 0   | 5        | 10  | 15 0 | 5        | 10  | 15  |  0                              |  20  40 |  60  80  100 |
|     | Time (s) |     |      | Time (s) |     |     | Number of expensive tenants (n) |         |              |
(a)Top:servicereceivedbyasmalltenantovertime,(b)Threadoccupancyovertime.Horizontallinesrep-(c)Standarddeviation(inseconds)ofasmalltenant’s
measuredin100msintervals.Bottom:servicelagin resentworkerthreads;shadedindicatestheworkeris servicelaginthepresenceofincreasinglymanyex-
secondscomparedtoanidealGPSserver. processinganexpensiverequest,unshadedindicates pensivetenants.Notethatsmalltenant’srequestexe-
|     |     |     | acheaprequest. |     |     |     | cutiontimeis0.001s. |     |     |
| --- | --- | --- | -------------- | --- | --- | --- | ------------------- | --- | --- |
Figure8:Syntheticworkloaddescribedin§6.1.1.
Weimplementedallschedulersinadiscreteeventsimula- tosmallandmediumtenantsthathasonetotwoordersof
torwhererequestswerescheduledacrossafixednumberof magnitudereductioninservicelagvariation.
threads.WeusedsyntheticworkloadsandtracesfromAzure ● Whenmanytenantshaveexpensiverequests,2DFQmain-
Storage[4,9]tokeeptheserverbusythroughouttheexperi- tainslowservicelagvariationforsmalltenants(§6.1.1).
ments,butalsoranexperimentsatlowerutilizations. ● Whenrequestcostsareunknown,2DFQEreducestheser-
Wecompare2DFQtoWFQandWF2Qasbaselinealgo- vicelagvariationbyonetotwoordersofmagnitudefor
rithms. BesidesWFQandWF2Q,weimplementedseveral smallandmediumtenants(§6.2.2).
otheralgorithmsincludingSFQ[23],MSF2Q[8],andDRR[50]. Withincreasinglyunpredictableworkloads,2DFQEimpro-
●
However,weomitthesealgorithmsfromourevaluationaswe vestaillatencyofpredictabletenantsbyupto100×(§6.2.1).
foundtheresultstobevisuallyindistinguishablefromeither ● Acrossasuiteofexperimentsbasedonproductionwork-
WFQorWF2Q–occurringbecausethekeydifferencesbe- loads, 2DFQE improves 99th percentile latency for pre-
tweenthealgorithmsareincidentaltotheirfairnessbounds. dictabletenantsbyupto198×(§6.2.2)
Forexample,sincewedonotuseavariablerateserver,thepri-
maryfeatureofSFQisnotnecessaryandSFQandWFQpro- 6.1 Known Request Costs
ducednearlyidenticalschedules.Similarly,WF2QandMSF Our first set of experiments focuses on scheduling with
2Qproducednearlyidenticalresults;MSF2Q’sdistinguishing knownrequestcoststhatmayvarybyseveralordersofmag-
featurehandlesthecasewhereonetenanthasahighweight nitude.Wefirstevaluate2DFQunderworkloadswithincreas-
orfewtenantsaresharingmanylinks,whereasweevaluate
inglymanyexpensiverequests,andcomparewiththeservice
withmanytenants(uptoseveralhundred)andequalweights. providedunderWFQandWF2Q.Second,weevaluatethe
Furthermore, many algorithms such as DRR [50] and WF overallserviceandfairnessprovidedby2DFQonaworkload
2Q+[5]improvealgorithmiccomplexitybutdonotimprove derivedfromproductiontraces.
fairnessboundsoraddadditionalfeatures;inpracticethey
havesimilarorworsebehaviorcomparedtoWFQorWF2Q. 6.1.1 ExpensiveRequests
Toevaluatetheschedulers,weusethefollowingmetrics:
Inthisexperimentwesimulatetheservicereceivedby100
Servicelag:thedifferencebetweentheserviceatenantshould backloggedtenantssharingaserverwith16workerthreads,
havereceivedunderGPSandtheactualworkdone.ForN eachwithacapacityof1000unitspersecond.Forvarying
valuesofn,wedesignatenofthetenantsassmalland100−n
threadswithrprocessingrate,weuseareferenceGPSsystem
withrateNr. ofthetenantsasexpensive.Smalltenantssamplerequestsizes
Servicelagvariation:thestandarddeviation, σ ofservice fromanormaldistributionwithmean1,standarddeviation0.1;
largetenantssamplerequestsizesfromanormaldistribution
lag.Burstyscheduleshavehighservicelagvariationdueto
| oscillationsinservice. |     |     |     |     | withmean1000,standarddeviation100. |     |     |     |     |
| ---------------------- | --- | --- | --- | --- | ---------------------------------- | --- | --- | --- | --- |
Servicerate:workdonemeasuredin100msintervals. Figure8aexaminestheservicereceivedovera15second
intervalforoneofthesmalltenants,T,when50%oftenants
Latency:timebetweentherequestbeingenqueuedandfin-
areexpensive(n=50).Sincethethreadpoolhas16threads,
ishingprocessing.Wefocusonthe99thpercentileoflatency,
unlessotherwisenoted. theidealschedulewouldsplitcheapandexpensiverequests
intoseparatethreads,producingsteadyserviceof160units
Giniindex:aninstantaneousmeasureofschedulerfairness
persecondpertenant.Figure8a(top)showsthattheservice
acrossalltenants[49].
|                   |     |                               |     |     | provided | by WFQ | has large-scale | oscillations. | This occurs |
| ----------------- | --- | ----------------------------- | --- | --- | -------- | ------ | --------------- | ------------- | ----------- |
| Evaluationsummary |     | Ourevaluationof2DFQshowsthat: |     |     |          |        |                 |               |             |
becauseWFQalternatesbetweenphasesofservicingallof
● Whenrequestcostsareknown,forbothsynthetic(§6.1.1) the50smalltenants,followedbyallofthe50largetenants,in
andreal-world(§6.1.2)workloads,2DFQprovidesservice burstsofupto1thousandunitspertenant.Figure8a(bottom)

|     | WFQ | WF²Q | 2DFQ |                        1111111111222222222233           0123456789012345678901 |     |     |     |
| --- | --- | ---- | ---- | ------------------------------------------------------------------------------ | --- | --- | --- |
d   3 0 0
| e xxxxx111110000033333 |     |     |     |     |     |     | 1 0 7 |
| ---------------------- | --- | --- | --- | --- | --- | --- | ----- |
v
| ei        |     |     |     | Q   |     |     |     |
| --------- | --- | --- | --- | --- | --- | --- | --- |
| c   2 0 0 |     |     |     | F   |     |     |     |
| e         |     |     |     | W   |     |     |     |
R
| e        |     |     |     | 0123456789 |     |     |       |
| -------- | --- | --- | --- | ---------- | --- | --- | ----- |
| c  1 0 0 |     |     |     |            |     |     | 1 0 6 |
vi
er
S   0
|  0         |     |  5  |  10 |  15                        1111111111222222222233           0123456789012345678901 |     |     |       |
| ---------- | --- | --- | --- | ---------------------------------------------------------------------------------- | --- | --- | ----- |
| s)   3 . 6 |     |     |     |                                                                                    |     |     | 1 0 5 |
Siz e
| g (   3 . 4 |     |     |     | Q          |     |     |         |
| ----------- | --- | --- | --- | ---------- | --- | --- | ------- |
|             |     |     |     | ²          |     |     | est     |
| a   3 . 2   |     |     |     | F          |     |     |         |
| L           |     |     |     | W          |     |     | q u     |
| e    3      |     |     |     | 0123456789 |     |     | e       |
| c           |     |     |     |            |     |     | 1 0 4 R |
vi   0
er
S - 0 . 2
| 0   |     | 5   | 10  | 15                                                                             |     |     |     |
| --- | --- | --- | --- | ------------------------------------------------------------------------------ | --- | --- | --- |
| 3   |     |     |     |                        1111111111222222222233           0123456789012345678901 |     |     |     |
66
| xx 11 | 00  |     |     |     |     |     | 1 0 3 |
| ----- | --- | --- | --- | --- | --- | --- | ----- |
x 2
| e      |     |     |     | Q   |     |     |     |
| ------ | --- | --- | --- | --- | --- | --- | --- |
| d 1    |     |     |     | F   |     |     |     |
| n ni I |     |     |     | D   |     |     |     |
3
| x 1    | 0 4 |     |     | 2 0123456789 |     |     |       |
| ------ | --- | --- | --- | ------------ | --- | --- | ----- |
| Gi 2.5 |     |     |     |              |     |     | 1 0 0 |
2
| 0                                                                                                                                          |     | 5        | 10  | 15 0 | 5        | 10  | 15  |
| ------------------------------------------------------------------------------------------------------------------------------------------ | --- | -------- | --- | ---- | -------- | --- | --- |
|                                                                                                                                            |     | Time (s) |     |      | Time (s) |     |     |
| (a)Top:servicereceivedbyT,atenantoutlinedin§3.2,whilereplayingtraces(b)Illustrationofrequestsizesrunningoneachthread.Horizontallinesrepre- |     | 1        |     |      |          |     |     |
fromaproductionserverwith32threads.Middle:servicelagforthesametenant,sentworkerthreads;fillcolorindicatestherunningrequestsizeateachinstant
comparedtoanidealGPSserver;redhorizontallineis2DFQ,whichhasveryintime.WF2Qserviceoscillationscanbeidentifiedinthemiddleplotbydark-
littleservicelag.Bottom:Giniindex[49]acrossalltenants. coloredblocksofexpensiverequests.2DFQpartitionsrequestsbysize.
Figure9:Timeseriesforaproductionworkloadonaserverwith32threads
|  1  |     | 4   |           | randomnessinrequestsizesthatenablesexpensiverequests |     |     |     |
| --- | --- | --- | --------- | ---------------------------------------------------- | --- | --- | --- |
|     |     | WFQ | WF²Q 2DFQ |                                                      |     |     |     |
y
| c   |     | 3   |     | totemporarilyrunon9oftheworkerthreadsinsteadof8. |     |     |     |
| --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- |
n
| u e |     | s]2 |     | Wevariedtheproportionofexpensivetenantsnbetween0 |     |     |     |
| --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- |
q
e g [ 1 a n d 10 0 a n d s h o w t h e r e s u l ti n g s t a n d a r d d e v i a t i o n o f s e r v ic e
| Fr  |     | a   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- |
e   0.5 L l a g i n F ig u r e 8 c . W F Q a n d W F Q e x p e r i e n c e a l i n e a r in c r e a s e
| v   |     | e  0 |     |     | 2   |     |     |
| --- | --- | ---- | --- | --- | --- | --- | --- |
| ati |     | c    |     |     |     |     |     |
ul vi - 1 i n s t a n d a r d d e v i ati o n a s t h e p r o p o r t io n o f e x p e n s i v e t e n a n t s
| m   |     | er   |     |                                                 |     |     |     |
| --- | --- | ---- | --- | ----------------------------------------------- | --- | --- | --- |
| u   |     |      |     | grows.WFQgrowsunboundedly,whereasWF2Qeventually |     |     |     |
| C   |     | S -2 |     |                                                 |     |     |     |
plateaus.Withonly25%oftheworkloadcomprisingexpensive
|  0            |                  | -3  |     |     |     |     |     |
| ------------- | ---------------- | --- | --- | --- | --- | --- | --- |
| 1 0 -4 1 0 -3 | 1 0 -2 1 0 - 1 1 | 1 0 |     |     |     |     |     |
σ (S e rv i ce  L a g )  P e r  Te nan t -4 t1t2t3t4t5t6t7 t1t2t3t4t5t6t7 t1t2t3t4t5t6t7 tenants,WF2Qconvergestoitsworst-casebehavior.Onthe
Figure10:Left:CDFofservicelagstandarddeviationacrossalltenants. otherhand,while2DFQalsoseesgraduallyincreasedstandard
2DFQreducesservicelagstandarddeviationfortenantswithsmallrequests. deviation,itisanorderofmagnitudelowercomparedtoother
| Right:Distributionofservicelagexperiencedbyt |     |     | ...t .Thewiderthedis- | schedulers. |     |     |     |
| -------------------------------------------- | --- | --- | --------------------- | ----------- | --- | --- | --- |
1 7
tributionofservicelag,themoreoscillationsatenantwillexperience.
|     |     |     |     | 6.1.2 ProductionWorkloads |     |     |     |
| --- | --- | --- | --- | ------------------------- | --- | --- | --- |
plotstheservicelagovertime,showingthatsmalltenants
oscillatebetween1and2secondsaheadoftheirfairshare, Inthisexperimentweevaluatefairshareprovidedby2DFQ
withaperiodofapproximately6.25seconds.Smalltenantsare with a workload derived from production traces of Azure
consistentlyaheadoftheirfairsharebecausesmallrequests Storage.Wesimulatetheservicereceivedbytenantssharing
havetheearliestfinishtimesoWFQservicesthemfirst.WF2Q aserverof32workerthreads,eachwithcapacity1million
haslesslong-termoscillation,butsuffersfrommoreextreme units.Wereplay250randomlychosentenantsdrawnfrom
oscillationsovershortertimescales;thesmalltenantreceives workloadtracesof50servers.Asabaselineforevaluationin
noserviceforalmostasecond.Bydesign,WF2Qprevents thisandsubsequentexperiments,weincludetenantsT ...T
1 12
Tfromgettingtoofaraheadofitsfairshare,butduetothe describedin§3.2.Inaggregateacrossalltenants,requestcosts
presenceoftheexpensivetenants,Tcontinuallyfallsbehindby forthisexperimentvaryfrom250to5million.
upto1second.ThisoccursbecauseWF2Qdeterminesthatall We first illustrate the improved service for tenants with
smalltenantsareineligible,andschedulesexpensiverequests smallrequests.Figure9a(top)showsa15secondtimeseries
to run on every worker thread, as illustrated in Figure 8b. forT ,comprisingprimarilysmallrequestsbetween250and
1
Notethatbecauseaverageexecutiontimeofasmalltenant’s 1000insize.Figure9a(middle)plotsT ’sservicelag.Under
1
requestis1ms,suchrateoscillationdelaysthetenantbyupto WFQ,theservicereceivedoscillatesbetween3sand3.7sahead
1000requests.Finally,theserviceprovidedby2DFQismore ofGPS.WF2QmorecloselymatchesGPS,butoccasionally
stable,butstillwithoccasionaloscillations.Theoscillationsare fallsbehindbyupto50msduetothethreadpoolbecoming
characterizedasaperiodofslightlyreducedservicefollowed occupiedbyexpensiverequests.2DFQ(thehorizontalred
by a burst of increased service. As illustrated in Figure 8b line) closely matches GPS at all times. Figure 9a (bottom)
(bottom),2DFQmostlypartitionsrequestsbysizeacrossthe plotstheGiniindex[49]overtime,anaggregatemeasureof
threads, and the remaining oscillations are a side effect of fairnessacrossalltenants.WFQissignificantlylessfairin

|     | WFQE          | WF²QE | 2DFQE |     | 1111111111222222222233 0123456789012345678901 |     |     |     |
| --- | ------------- | ----- | ----- | --- | --------------------------------------------- | --- | --- | --- |
| 300 | xx110033 x103 |       |       |     |                                               |     |     | 107 |
%0
200
0123456789
| 100 |     |     |     |     |     |     |     | 106 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
0
| 0   |     | 5   | 10  | 15  | 1111111111222222222233 0123456789012345678901 |     |     |     |
| --- | --- | --- | --- | --- | --------------------------------------------- | --- | --- | --- |
devieceRecivreS
x103 x103
| 300 |     |     |     |     |     |     |     | 105 eziStseuqeR |
| --- | --- | --- | --- | --- | --- | --- | --- | --------------- |
%33
200
| 100 |     |     |     |     | 0123456789 |     |     |     |
| --- | --- | --- | --- | --- | ---------- | --- | --- | --- |
104
0
| 0   |      | 5   | 10  | 15  | 1111111111222222222233 0123456789012345678901 |     |     |     |
| --- | ---- | --- | --- | --- | --------------------------------------------- | --- | --- | --- |
| 300 | x103 |     |     |     |                                               |     |     | 103 |
| 200 |      |     |     |     | %66                                           |     |     |     |
| 100 |      |     |     |     | 0123456789                                    |     |     | 100 |
0
| 0   |     | 5 Time(s) | 10  | 15  | 0   | 5 Time(s) | 10  | 15  |
| --- | --- | --------- | --- | --- | --- | --------- | --- | --- |
(a)ServicereceivedbyT,apredictabletenantsubmittingsmallrequests.Each (b)Thread occupancy over time for 2DFQE for increasingly unpredictable
1
figureillustratestheservicereceivedbyT underWFQE,WF2QE,and2DFQE. workloads.Horizontallinesrepresentworkerthreads;fillcolorindicatescost
1
2DFQcontinuestoprovidestableserviceastheworkloadmixbecomesunpre- oftherunningrequestateachinstantintime.2DFQEisolatespredictable,small
dictable,withonlyaminorincreaseinoscillations. requestsevenasincreasinglymanytenantsareunpredictable.
Figure11:Timeseriesastheoverallserverworkloadmixcomprises0%(top),33%(middle),and66%(bottom)unpredictabletenants.
aggregate,while2DFQandWF2Qarecomparable.Figure9b erages(α=0.99).Werefertothem,respectively,asWFQE
illustrates sizes of requests running on threads during the andWF2QE.Wealsoimplementedbothretroactivecharging
experiment.ServicespikesunderWF2Qcorrelatewithsev- andrefreshchargingforWFQEandWF2QE.Withoutthese
erallargerequestsoccupyingthreadssimultaneously.2DFQ techniques,wefoundthatthequalityofschedulesdeteriorated
partitionsrequestsacrossthreadsaccordingtorequestsize, byasurprisingamount.Itturnedouttoberelativelycommon
avoidingsuchspikes.Figure10plotsaCDFoftheservicelag forworkloadstohaveback-to-backrequeststhatdifferbysev-
standarddeviationsacrossalltenantsincludedintheexperi- eralordersofmagnitude;withoutretroactivechargingittakes
ment.Alowstandarddeviationisdesirable,asitcorresponds toolongtoincorporatemeasurementsbackintothemoving
tofeweroscillationsinservice.Thefigureshowsthatthefirst averagetorectifyestimationerror.Forthesamereason,with-
quartileoftenantshaveapproximately50xlowerstandard outrefreshchargingitwouldquicklyleadtomultiplelarge
deviationunder2DFQthanWF2Qand100xlowerstandard requeststakingoverthethreadpool.Sincethebookkeeping
deviationunder2DFQthanWFQ.Thesetenantsaretheones techniquesarestraightforwardtoimplement,weappliedthem
withprimarilysmallrequests. toallalgorithms,andourexperimentresultsonlyreflectthe
Tomorepreciselyunderstandhow2DFQimpactstenants differencesbetweenschedulinglogicandestimationstrategy.
basedonrequestsizes,werepeattheexperimentandinclude Wefirstevaluate2DFQEforworkloadswhereanincreasing
|     |     | t ...t |     |     |     |     | unpredictable, |     |
| --- | --- | ------ | --- | --- | --- | --- | -------------- | --- |
an additional seven tenants, 1 7 . These tenants submit proportion of the tenants are comparing to
requests with fixed costs of 28,210,212,...,220 respectively serviceunderWFQEandWF2QE.Second,wecomparethe
(from256to1million),spanningtherangeofcostsinour schedulers across a suite of 150 workloads generated from
workload.Figure10(right)plotsthedistributionofservicelag productionworkloadtraces,andassesstheoveralleffecton
experiencedbyt ...t underWFQ,WF2Qand2DFQ.Each servicelagandrequestlatency.
1 7
| distribution | shows | how much the | tenant deviates | from its |     |     |     |     |
| ------------ | ----- | ------------ | --------------- | -------- | --- | --- | --- | --- |
fairshare.Underallschedulers,largerequests(t )experience 6.2.1 UnpredictableWorkloads
7
a wide range of service lag, because service is received in Inthisexperimentweevaluate2DFQE’spessimisticcost
large,coarse-grainedbursts.Forprogressivelysmallerrequests
estimationstrategy,demonstratinghowitco-locatesunpre-
(t ...t ),WFQreducesservicelagtoarangeof0.8seconds;
| 6 1 |     |     |     |     | dictableandexpensivetenants,keepingthemawayfrompre- |     |     |     |
| --- | --- | --- | --- | --- | --------------------------------------------------- | --- | --- | --- |
WF2Qreducesitto0.5seconds,while2DFQreducesitto
|     |     |     |     |     | dictable tenants | with small requests. | We examine | a single |
| --- | --- | --- | --- | --- | ---------------- | -------------------- | ---------- | -------- |
0.01seconds.Theseresultsillustratehow2DFQparticularly workloadindetail;in§6.2.2wegiveaggregateresultsacross
improvestheservicereceivedbytenantswithsmallrequests.
asuiteofexperiments.Weshowthat2DFQEimprovesser-
viceforthosetenantscomparedtoWFQEandWF2QE,which
| 6.2 Unknown |     | Request Costs |     |     | deteriorateunderthesameconditions. |     |     |     |
| ----------- | --- | ------------- | --- | --- | ---------------------------------- | --- | --- | --- |
Oursecondsetofexperimentsevaluatesschedulerswhen Weexamineaworkloadof300randomlyselectedtenants
request costs are not known a priori. We compare 2DFQE plus T ...T as in §6.1.2. We repeat the experiment three
|     |     |     |     |     | 1   | 12  |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
(α=0.99)tovariantsofWFQandWF2Qthatestimatere- times.Initially,mosttenantsintheworkloadarepredictable,
questcostsusingper-tenantper-APIexponentialmovingav- and2DFQEprovideslittle,ifany,improvementoverWFQE

| 10     | 0% Unpredictable |     | 10         | 33%Unpredictable |     | 10         | 66%Unpredictable |     |     |
| ------ | ---------------- | --- | ---------- | ---------------- | --- | ---------- | ---------------- | --- | --- |
| 1      |                  |     | 1          |                  |     | 1          |                  |     |     |
| s ]    |                  |     | ]s[ycnetaL |                  |     | ]s[ycnetaL |                  |     |     |
|  [ 0.1 |                  |     | 0.1        |                  |     | 0.1        |                  |     |     |
y c
n
| e at10-2 |     |     | 10-2 |     |     | 10-2 |     |     |     |
| -------- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- |
L
| 10-3 |     |     | 10-3 |     |     | 10-3 |     |     |     |
| ---- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- |
T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12 T1 T2 T3 T4 T5 T6 T7 T8 T9 T10 T11 T12
| 10-4 |     |     | 10-4 |     |     | 10-4 |     |     |     |
| ---- | --- | --- | ---- | --- | --- | ---- | --- | --- | --- |
   WFQE    WF²QE    2DFQE 10 0% Unpredictable 33% Unpredictable 66% Unpredictable
 1
|     | 0%  | 33% | 6666%% |     |     |     |     |     |     |
| --- | --- | --- | ------ | --- | --- | --- | --- | --- | --- |
y c
| n   |     |     |     | 1   |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| e   |     |     | s]  |     |     |     |     |     |     |
q u
| e       |     |     | y [ |     |     |     |     |     |     |
| ------- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Fr      |     |     | c   | 0.1 |     |     |     |     |     |
| e   0.5 |     |     | n   |     |     |     |     |     |     |
e at
ati v
|     |     |     | L   | 10-2 |     |     |     |     |     |
| --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
ul
m
u
| C   |     |     |     | 10-3     |             |             |             |             |       |
| --- | --- | --- | --- | -------- | ----------- | ----------- | ----------- | ----------- | ----- |
|     |     |     |     | t1 t2 t3 | t4 t5 t6 t7 | t1 t2 t3 t4 | t5 t6 t7 t1 | t2 t3 t4 t5 | t6 t7 |
 0
|   10- 4  10- 3  10 - 2  10-11 | 10   1 0- 4  10- 3  10 - 2  10-11 | 10   1 0- 4  10- 3  10 - 2  10-11 | 10   |     |     |     |     |     |     |
| ----------------------------- | --------------------------------- | --------------------------------- | ---- | --- | --- | --- | --- | --- | --- |
σ(Service Lag) Per Tenant
Figure12:Requestlatenciesastheoverallserverworkloadmixisincreasinglyunpredictable.Toprow:latencydistributionsforT ...T with1%and99%
|     |     |     |     |     |     |     |     | 1 12 |     |
| --- | --- | --- | --- | --- | --- | --- | --- | ---- | --- |
whiskers;eachclusterofthreebarsshowsthelatencydistributionforonetenantunderWFQE,WF2QE,and2DFQErespectively.2DFQEmitigatestheimpact
ofunpredictabletenantsandsignificantlyimproveslatenciesforpredictabletenantswithsmallrequests,suchasT.Bottomleft:CDFsofservicelagstandard
1
| deviation.Bottomright:latencyboxplotsforfixed-costtenantst |     |     |     | 1 ...t 7 . |     |     |     |     |     |
| ---------------------------------------------------------- | --- | --- | --- | ---------- | --- | --- | --- | --- | --- |
andWF2QE.However,forthesecondandthirdrepetitionsof for T ...T (top row), with whiskers highlighting 1st and
1 12
theexperiment,wemake33%and66%ofthesetenantsexplic- 99th percentile latencies. Each cluster of three bars shows
itlyunpredictable,bysamplingeachrequestpseudo-randomly thelatencydistributionunderWFQE,WF2QE,and2DFQE
fromacrossallproductiontracesdisregardingtheoriginating respectivelyforonetenantinoneexperiment.Forthebaseline
serveroraccount.Theresultingtenantslackpredictabilityin workload(0%Unpredictable)medianandtaillatenciesunder
APItypeandcostthatiscommontoreal-worldtenantsas WFQEand2DFQEarecomparable.WF2QEhassimilarme-
shownin§3.2,andastheworkloadbecomesunpredictable, dianlatencies,buthigher99thpercentilelatenciesforsmall
WFQEandWF2QErapidlydeteriorate. requestsbecauseoftheblockingeffectsoutlinedin§2.
Figure11aplotsatimeseriesoftheservicereceivedbyT However,with33%and66%unpredictabletenantspresent,
1
underWFQE,WF2QE,and2DFQE.Thetopfigureshowsthat latenciesunderWFQEandWF2QEincreasenearlyuniformly
withthebaselineworkload,WFQEprovidesservicewiththe acrossalltenants,toapproximately1second99thpercentile
mostoscillations;WF2QEprovidesservicewithoccasional latency.Therelativeincreaseinlatencyismostnoticeablefor
spikes,and2DFQEprovidesconsistentlysmoothservice.Os- tenantswithsmallerrequests(T ...T ),withmedianand99th
1 4
cillationsunderWFQE arelowerthantheywereinexperi- percentilelatenciesincreasingbyafactorofmorethan100×.
ment6.1.2sinceasideeffectofEMAaveragingistomake Bycontrastwith2DFQEthesetenantsaresignificantlyless
costsmoreuniformacrosstenants:fortenantswithanyvaria- impactedbytheunpredictabletenants,with99thpercentile
tioninrequestsize,smallrequestsareperceivedtobelarger latenciesincreasingbyamaximumfactorof10×amongex-
thantheyareandlargerequestsareperceivedtobesmaller. periments.With66%oftheworkloadunpredictable,2DFQE
Themiddleandbottomfiguresdemonstratehowtheservice providesa99thpercentilelatencyspeedupofupto100×over
deteriorateswithincreasinglyunpredictableworkloads(33% WFQEfortenantssuchasT withsmall,predictablerequests.
1
middle;66%bottom).WFQEandWF2QEproducelargescale On the other hand, tenants such as T do not experience
10
oscillationsinservice,while2DFQEhasoccasionalspikesof significantlatencyimprovements.RecallFigure4cfrom§2:
| service. |     |     |     |     | T ’srequestsvarywidelyincost,bymorethan3ordersof |     |     |     |     |
| -------- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- |
10
Figure11billustratestheschedulesproducedby2DFQEfor magnitude.2DFQEdoesnotimproveT ’sservicebecauseit
10
thethreeexperiments.Thefigureshowshow2DFQEinitially isanexampleoftheexpensiveandunpredictabletenantsthat
partitionsrequestsaccuratelyaccordingtocost,butasmore mustbeisolatedfromothers.
unpredictabletenantsarepresent,thepartitioningbecomes Despitesometenantsbeingmorepredictablethanothers,
morecoarsegrained.Thisoccurswhenarequestisestimated T ...T nonethelesshavevariationinrequestcosts.Tomore
1 12
tobelargebutitissmall,orviceversa.Itcanbeobservedby preciselyunderstandhow2DFQEaffectslatenciesfortenants
smallrequestsinterspersedamonglargerequests,andvice basedonrequestsize,werepeattheexperimenttoincludethe
versa.EachofthebriefspikesinserviceexperiencedbyT in fixed-costtenantst ...t asdescribedin§6.1.2.Figure12(bot-
|     |     |     |     | 1   |     | 1 7 |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
Figure11acanbecorrelatedwithantemporaryimbalanceof tomright)showsboxplotlatencydistributionsfort ...t ,and
|     |     |     |     |     |     |     |     | 1   | 7   |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
expensiverequests. illustrateshowtherelativelatencydegradationdisproportion-
Oscillations in service can have a profound effect on re- atelyaffecttenantst ...t ,whoserequestsarethesmallest.
1 4
questlatencies.Figure12showsboxplotlatencydistributions Acrossalltenants,astheworkloadbecomeslesspredictable,

| latenciesconvergetowardsthelatencyofthemostexpensive |     |     |     |     | 1000x |     |     |     |     |     |
| ---------------------------------------------------- | --- | --- | --- | --- | ----- | --- | --- | --- | --- | --- |
WFQE
| r e q u e s t s | i n t h e s y s t e m | .   |     |     | p   |     | ncy (s) | 10 0 |     |     |
| --------------- | --------------------- | --- | --- | --- | --- | --- | ------- | ---- | --- | --- |
u 10 0 x
| F i g u r e | 1 2 ( b o t t o m | l e ft ) p l o t s C D | F s o f t h e s e r v | i c e l a g s t a n - | e d       |     |     |     |     |     |
| ----------- | ----------------- | ---------------------- | --------------------- | --------------------- | --------- | --- | --- | --- | --- | --- |
|             |                   |                        |                       |                       | e         |     | e   |     |     |     |
|             |                   |                        |                       |                       | S p 1 0 x |     | at  | 1 0 |     |     |
d a r d d e v i a t i o n a c r o s s a ll t e n a n t s . I t s h o w s t h e s u c c e s s iv e i n - %  %  L
9
c r e a s e i n t h e p r o p o r t i o n o f t e n a n t s w i t h h i g h s t a n d a r d d e v i- 9 0 9 9 1
|     |     |     |     |     | E  Q |     | E   |     |     |     |
| --- | --- | --- | --- | --- | ---- | --- | --- | --- | --- | --- |
a t i o n – t h i s c o r r e s p o n d s t o t h e u n p r e d i c t a b l e t e n a n t s . Th e F Q
|     |     |     |     |     | D-10x |     | F    |     |     |     |
| --- | --- | --- | --- | --- | ----- | --- | ---- | --- | --- | --- |
|     |     |     |     |     | 2     |     | W0.1 |     |     |     |
remainingpredictabletenantsexperienceapproximately10to T1 T2 T3 T4 T5 T6 T7 T8 T9T10T11T12 T10
-100x
| 15×reducedstandarddeviationunder2DFQEcomparedto |     |     |     |     |     |     |     | 0.1 | 1   | 10 100 |
| ----------------------------------------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | ------ |
2DFQE  99% Latency (s)
WFQEandWF2QE.
1000x
WF²QE
ncy (s) 10 0
| 6 . 2 . 2 | P r o d u c t i o | n W o r k l o a d | s   |     | u p 10 0 x |     |     |     |     |     |
| --------- | ----------------- | ----------------- | --- | --- | ---------- | --- | --- | --- | --- | --- |
e d
|     |     |     |     |     | e   |     | e   |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
F i n a l ly , w e r u n a s u i t e o f 1 5 0 e x p e r im e n t s d e r iv ed f r o m p r o - S p 1 0 x at 1 0
|               |                       |                       |                       |                     | %     |     | %  L |     |     |     |
| ------------- | --------------------- | --------------------- | --------------------- | ------------------- | ----- | --- | ---- | --- | --- | --- |
| d u c t i o n | w o r k l o a d s o f | A z u r e S t o r a g | e . W e s i m u l a t | e th e s er v i c e |       |     |      |     |     |     |
|               |                       |                       |                       |                     | 9 9 0 |     | 9 9  |     |     |     |
|               |                       |                       |                       |                     | E     |     | E    | 1   |     |     |
r e c e i v e d b y t e n a n t s u n d e r W F Q E , W F 2 Q E , a n d 2 D F Q E , a s Q Q
|     |     |     |     |     | F D - 1 0 x |     | F²  |     |     |     |
| --- | --- | --- | --- | --- | ----------- | --- | --- | --- | --- | --- |
w e r a n do m l y v a r y s e v er a lp a r a m e te r s : t he n u m b e r o f w o r k e r 2 W 0.1
|                |                   |                    |                       |                     | T1 T2    | T3 T4 T5 T6 T7 T8 | T9T10T11T12 |     | T10 |        |
| -------------- | ----------------- | ------------------ | --------------------- | ------------------- | -------- | ----------------- | ----------- | --- | --- | ------ |
| th re a d s (2 | t o 6 4 ) ; t h e | n u m b e r o f te | n a n t s to r e pl a | y ( 0 t o 4 0 0 ) ; | -1 0 0 x |                   |             |     |     |        |
|                |                   |                    |                       |                     |          |                   |             | 0.1 | 1   | 10 100 |
thereplayspeed(0.5-4×);thenumberofcontinuouslyback- 2DFQE  99% Latency (s)
|                                                        |     |     |     |     | (a) 99th percentile                               | latency speedups | for T | ...T comparing |     | 2DFQE to |
| ------------------------------------------------------ | --- | --- | --- | --- | ------------------------------------------------- | ---------------- | ----- | -------------- | --- | -------- |
| loggedtenants(0to100);thenumberofartificiallyexpensive |     |     |     |     |                                                   |                  | 1     | 12             |     |          |
|                                                        |     |     |     |     | WFQE(toprow)andWF2QE(bottomrow).ScatterplotsshowT |                  |       |                |     | ’s99th   |
| tenants(0to100);andthenumberofunpredictabletenants     |     |     |     |     |                                                   |                  |       |                |     | 10       |
percentilelatenciesindetail,eachpointrepresentingoneexperiment.
(0to100).Tocomparebetweenexperiments,wealsoinclude
| T ...T                                           | .   |     |     |     | 1000x            | WFQE | 1000x            |     | WF²QE E |     |
| ------------------------------------------------ | --- | --- | --- | --- | ---------------- | ---- | ---------------- | --- | ------- | --- |
| 1 12                                             |     |     |     |     | pudeepS %99EQFD2 |      | pudeepS %99EQFD2 |     |         |     |
| Wemeasurethe99thpercentilelatencyoftenantsineach |     |     |     |     | 100x             |      | 100x             |     |         |     |
experimentandcalculatetherelativespeedupof2DFQEcom-
|     |     |     |     |     | 10x |     | 10x |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
paredtoWFQEandWF2QE.Asanexample,inthe“0%Unpre-
|                               |     |                            |     |     | 0   |     | 0   |     |     |     |
| ----------------------------- | --- | -------------------------- | --- | --- | --- | --- | --- | --- | --- | --- |
| dictable”experimentof§6.2.1,T |     | ’s99thpercentilelatencywas |     |     |     |     |     |     |     |     |
1
| 3.3msunder2DFQE,4.5msunderWFQE,and28msunder    |     |     |     |     | -10x           |                | -10x                           |     |          |       |
| ---------------------------------------------- | --- | --- | --- | --- | -------------- | -------------- | ------------------------------ | --- | -------- | ----- |
|                                                |     |     |     |     | t1             | t2 t3 t4 t5 t6 | t7 t1                          | t2  | t3 t4 t5 | t6 t7 |
| WF2QE,giving2DFQEaspeedupof1.4×overWFQEand8.5× |     |     |     |     | -100x          |                | -100x                          |     |          |       |
|                                                |     |     |     |     | (b)Resultsfort | 1 ...t         | 7 fromrepeatedexperimentsuite. |     |          |       |
overWF2QE.
Figure13a(left)plotsthedistributionof2DFQE’sspeedup Figure13:Comparisonof99thpercentilelatenciesacross150experiments
basedonproductionworkloads.Whiskersextendtominandmaxvalues.
overWFQEandWF2QE.Acrosstheexperiments,2DFQEsig-
nificantlyimproves99thpercentilelatencyfortenantssuch both were true. WFQE and WF2QE rapidly deteriorate as
asT ,whoserequestsaresmallandpredictable(illustratedin
| 1   |     |     |     |     | theworkloadbecomesunpredictable,increasingtherelative |     |     |     |     |     |
| --- | --- | --- | --- | --- | ----------------------------------------------------- | --- | --- | --- | --- | --- |
§2).T hasamedianimprovementof3.8×overWFQEand
| 1   |     |     |     |     | improvement | of 2DFQE. | For example, | in  | §6.2.1, the | initial |
| --- | --- | --- | --- | --- | ----------- | --------- | ------------ | --- | ----------- | ------- |
142×overWF2QE.However,2DFQEdoesnotimprove99th
workload(0%Unpredictable)wasmorepredictablethana
percentilelatencyasmuchfortenantswithlargeand/orun- typicalworkload,and2DFQonlyimproved99thpercentile
| predictablerequests,suchasT                            |     | andT | .Figure13a(right) |     |             |                                       |     |     |     |     |
| ------------------------------------------------------ | --- | ---- | ----------------- | --- | ----------- | ------------------------------------- | --- | --- | --- | --- |
|                                                        |     | 10   | 12                |     | latencyforT | byafactorofapproximately1.5×overWFQE. |     |     |     |     |
| plotsthe99thpercentilelatenciesacrossallexperimentsfor |     |      |                   |     |             | 1                                     |     |     |     |     |
Ontheotherhand,thefinalworkload(66%Unpredictable)
T ,comparing2DFQEtoWFQE(top)andWF2QE(bottom). waslesspredictablethanatypicalworkload,andT ’s99th
| 10                                            |     |     |     |      |                                                 |     |     |     |     | 1   |
| --------------------------------------------- | --- | --- | --- | ---- | ----------------------------------------------- | --- | --- | --- | --- | --- |
| 2DFQEresultedinworse99thpercentilelatencyforT |     |     |     | in64 |                                                 |     |     |     |     |     |
|                                               |     |     |     | 10   | percentilelatencyimprovementoverWFQEwasmorethan |     |     |     |     |     |
oftheexperimentsforWFQEand47forWF2QE.However,
100×.Thesuiteof150experimentspresentedheresimilarly
when2DFQEdidimprovelatenciesforT 10 ,itwasbysignif- varyinhowpredictabletheyare,andtherangeof99thper-
icantlylargerfactors(upto61×)thanwhenlatencieswere
centilelatencyspeedupsillustratedinFigure13a(left)reflect
worse(upto5×).
thisrange.
Tobetterunderstandhow2DFQEimproveslatenciesfor
tenantswithsmallerrequests,werepeattheexperimentsuite
7. DISCUSSION
| toincludethefixed-costtenantst |     | ...t | asdescribedin§6.1.2. |     |     |     |     |     |     |     |
| ------------------------------ | --- | ---- | -------------------- | --- | --- | --- | --- | --- | --- | --- |
|                                |     | 1    | 7                    |     |     |     |     |     |     |     |
Figure 13b plots the distribution of 2DFQE’s speedup over 2DFQIntuition 2DFQimprovesservicecomparedtoWFQ
WFQE andWF2QE for t 1 ...t 7 ,andillustrateshowlatency andWF2Qprimarilyduetothemanageablemixofpredictable,
is primarily improved for tenants with small requests (t ). unpredictable,cheapandexpensiverequestsinrealworkloads.
1
Conversely,tenantswithveryexpensiverequestssuchast ConsidertheillustrationinFigure14.Atoneextremewehave
7
andT seelittle,ifanyimprovement. predictableworkloadswithlowvariationinrequestcost((cid:192)).
12
Overall, the experiments where WFQE and WFQE per- Thisscenarioisrepresentativeofpacketschedulingonnet-
formedbestcorrelatedwithlownumbersofbothunpredictable worklinks,andWFQ,WF2Qand2DFQwouldprovidesimi-
andexpensivetenants,forwhichrequestcostestimateswere larlygoodqualityofservicebecauselittle,ifany,blockingcan
accurateandtherewaslittlechanceforthreadpoolblocking. occur.Attheotherextremeliesworkloadswithhugelyvarying
Ontheotherhand,theexperimentswhere2DFQEperformed requestcostsandcompletelyunpredictabletenants((cid:193)).Inthis
best correlated with high numbers of either unpredictable scenario,allschedulerswouldbehavepoorlybecauseblocking
orexpensivetenants,withmostspeedupsoccurringwhen wouldbeunavoidable,evenfor2DFQ.However,startingfrom

andtokeeplow-levelresourcequeues(e.g.,disk)short.
➀ typical
workloads Thechallengespresentedinthispaperaretheresultofwide
➂
costvariationincloudservices.Analternativeapproachis
quality to reduce cost variation by splitting up long requests into
of shorterones[15].Forexample,after100msofworkarequest
service 2DFQ
couldpauseandre-entertheschedulerqueue.However,this
WF²Q
WFQ ➁ approachimpliesmoreoverheadonthedeveloper;itcanbe
appliedonlytocertainrequesttypes;anditaffectsexecutionef-
unpredictable workloads,
ficiencybecauseof,e.g.,dataloadedinvarioussystemcaches.
expensive requests
Figure14:Illustrationoftheintuitionbehind2DFQ’ssignificantlyimproved
serviceforourworkloads. 8. RELATED WORK
Wediscussrelatedworkbasedonthecorechallengesad-
thefirstextremeandtransitioningtothesecond,withwork-
dressedinthispaper.
loadsbecominglesspredictable,2DFQdoesnotdeteriorateas
PacketSchedulingFairqueueschedulinghasbeendevel-
rapidlyasWFQorWF2Qdo.Betweenthetwoextremeslies
opedinthecontextofpacketscheduling[6,23,46,50],where
amiddlegroundwhereWFQandWF2Qexperienceblock-
packetsaresentsequentiallyacrossasinglelink.Becauseof
ingandreducedqualityofservice,but2DFQdoesnot((cid:194)).
this,themajorityofpapersinthisareaonlyconsidersequen-
Manyreal-worldworkloadsliebetweenthesetwoextremes,
tialexecution.Anexceptionis,forexample,MSF2Q[8],where
containingbothunpredictableandpredictabletenants.Our
theauthorsconsiderschedulingpacketsacrossmultipleag-
resultsin§6.2.1and§6.1.1demonstratedthisdeterioration.
gregatedlinks.Whilethissettingisveryclosetoours,the
Estimators Wedesigned2DFQE’spessimisticestimationstrat- schedulerisadirectextensionofWF2Qandwefoundthatit
egytotakeadvantageof2DFQ’scost-basedpartitioning.WFQ producesnearidenticalbehaviorinthepresenceoflargere-
andWF2Qlackcost-basedpartitioning,sothereisnothing quests.Single-linkschedulerssuchasWFQ[46]orWF2Q[6]
fundamentalaboutthemthatwouldbenefitfromthisesti- requirepacketsizetoschedulebecausetheyorderflowsbased
mationstrategy.Nonetheless,wecanapplyittothesealgo- ontheirfinishtag.SFQ[23]doesnotneedthepacketsizebe-
rithms; we experimented with numerous combinations of foreschedulingthepacketbecauseitselectspacketsbasedon
schedulerandestimator,andfoundthatWFQandWF2Qwith theirstarttag,whichiscomputedbasedonsizesofprevious
pessimisticestimationperformednobetter,andoftensignifi- packets.Whenapacketcompletes,itsobservedcostisused
cantlyworse,thanusinganEMA.Weviewestimatorchoice toupdatethestarttagofitsflow.Whenappliedtorequest
asanimportantdesignpointforfutureworkinthisspace–to schedulingwheremultiplerequestsofthesametenantcan
ensuregoodbehaviorwhenover-orunder-estimatingrequest executeconcurrently,thisapproach,however,doesnotwork
costs. becausewewouldhavetoexecuteeachtenantsequentially.
Limitations While2DFQimprovesqualityofservicewhen ThreadSchedulingandPre-EmptionThreadscheduling
thesystemisbacklogged,work-conservingschedulersingen- in the operating system is analogous to packet scheduling.
eralcannotimproveservicewhenthesystemisunder-utilized. Intheresearchliterature,lotteryscheduling[58]andstride
Inevitably,allworkerthreadscouldbeservicingexpensivere- scheduling[59]wereindependentlydevelopedandlaterfound
questsifnootherrequestsarepresent.Anysubsequentburst tobeequivalenttofairqueuing[17,46].Schedulingalgorithms
of small requests would have to wait for the expensive re- haveproliferatedinbothdomains,forexamplestart-timefair
queststofinish.Thisbehavioroccursunder2DFQandall queuing was proposed for both hierarchical link [23] and
non-preemptiveschedulers,andcreateslargedelayforthe CPU[22]sharing.Onmulticoresystems,hierarchicalsched-
smallrequests.Onewaytoavoidthisistomakethesched- ulerssuchastheLinuxCompletelyFairScheduler[45]and
ulernotwork-conserving,forexample,byallowingthreads DistributedWeightedRoundRobin[40]extendfairqueuing
toremainidledespitethepresenceofqueuedrequests.An- to multiple cores by maintaining per-core run queues and
otheroptionistoallowavariablenumberofworkerthreads load-balancingrunnablethreadsacrosscores.
andtospawnnewthreadswhensmallrequestsshowup.This Threadschedulerscancontroltheamountoftimeathread
would over-saturate the CPU and thus slow down already spendsrunningonacore(i.e.,thequantumortimeslice).
runningrequests,butwouldallowthesmallrequeststofinish Thus they have the means to explicitly bound how long a
faster;however,itwouldincuradditionaloverheadfrommore corecanbeoccupiedbeforeadifferentthreadgetstorun.In
context-switching.Intheextreme,wecouldtakeathread-per- theworstcase,thisreducesburstinesstothegranularityof
tenantapproach;however,thisresultsinmorecontextswitch- thelargesttimeslice.Forexample,Lietal.[40]discussfor
ing,contentionforapplicationlevel(e.g.,locks,caches)and infeasiblethreadweights:“Eventually,thisthreadbecomesthe
systemlevel(e.g.,disk)resources,andsubstantiallyreduced onlyoneonitsCPU,whichisthebestanydesigncandotofulfill
goodput.Thisisespeciallyrelevantsincerequestscanbevery aninfeasibleweight.”
short–lessthan1msindurationformanyrequests–which However,applicationscannotcontrolpreemptionorspec-
exacerbatescontextswitchingoverheads.Ourapproachin ifyfairnessgoalsbecauseoperatingsystemsdonotexpose
thispaper–fairqueueschedulingattheapplicationlevel– sufficient control over these mechanisms. Current operat-
isthepreferredapproachincloudservices[15]forefficiency ingsystemsdonotgiveapplicationstheabilitytoconfigure

threadpreemption;atmost,WindowsUser-ModeSchedul- proportionallytotheestimationerror.Further,becausethe
ing[55](mostnotablyusedbyMicrosoftSQLServer[35]) resourcemodelsdependonwhichmodulesthepacketexe-
givesapplicationscontroloverthreadschedulingbutlacks cutedin,resourceaccountinghappensonlyaftertherequest
configurable time slices – threads only yield to the sched- completes,whichlimitsDRFQtoexecutingsingletenant’s
ulerwhentheymakeblockingsystemscallsoradirectcallto packetssequentially.
UmsThreadYield().Operatingsystemsalsolackapplication- StorageandI/OpClock[26],mClock[25],andPisces[52]
leveltenantinformationanddonothaveaccesstoapplication- proposequeueschedulersforphysicalstorage,whereseveral
levelrequestqueues.Fairnessmechanismslikecgroups[11] I/Orequestsexecuteconcurrently.I/Orequestcostsaremuch
enableoperatorstodivideresourcesbetweenprocessesand lessvariablethaninthecloudsetting,anddynamicworkloads
threadstoprovidefairnessandisolation,butdonothaveac- remainanopenchallenge[61].Similarrequestcostmodeling
cess to application-level queues. More importantly, due to hasbeendoneinthestoragedomainaswell[25,54],where
thehighnumberoftenants,athread-per-tenantapproach typeofoperationsandhardwarevariabilityarelimited.For
is infeasible; short requests less than 1ms in execution du- example,IOFlow[54]periodicallybenchmarksthestorage
ration exacerbate context-switching overheads and reduce devicetoestimatecostsoftokensusedforpacingrequests.
throughput,whilehigherconcurrencyincreasescontention Also,toboundtheuncertaintyofarbitrarylongIOrequests,
overapplication-level(e.g.,locks,caches)andsystem-level theybreaktheminto1MBrequests.
(e.g.,disk)resources. DistributedSystemsManydistributedsystemsschedulers,
Event-based systems have long been debated in the op- such as Retro [43], Cake [60], and Pulsar [3] periodically
erating systems community as a dual to thread-based sys- measure request costs and use these estimates in the next
tems[39,44,56].Akeyfeatureofevent-basedsystemsiscoop- interval.However,indynamicworkloads,suchasshownin
erativemultitasking:eventhandlersarenotpreemptibleand Figure4,suchapproachcanleadtoarbitraryunfairnessacross
rununtilcompletion,simplifyingconcurrentprogramming tenantsunlessestimationerrorsareaddressed.Thesesystems
onsingle-coremachinesbecauseeventhandlersareimplicitly enforcefairshareusingratelimiters,typicallyimplemented
atomic[44,56].Thread-basedsystemsalsoadaptedthisfea- astokenbuckets,whicharenotdesignedtoprovidefairness
tureintocooperativescheduling[1,57],wherebythreadsonly atshorttimeintervals.Dependingonthetokenbucketrate
yieldtothescheduleratpre-definedpointsspecifiedbythe andburstparameters,theycaneitherunder-utilizethesystem
developer.Forbothevent-basedandthread-basedsystems, orconcurrentburstscanoverloaditwithoutprovidingany
cooperativeschedulingisvulnerabletolong-runningevent furtherfairnessguarantees.
handlers, or threads that go for a long time without yield- Web Applications A large body of work – for example
ingtothescheduler.Whenthisoccurs,programscanblock [7,48]orsee[24]forasurvey–hasfocusedonproviding
forlargeperiodsoftimeandtheprogrammaybecomenon- differentiatedservicesorquality-of-service(QoS)forcluster-
responsive[1,44,57].Toavoidthisbehavior,developerscanex- basedapplications;theydefinemultipleuserclasses(orten-
plicitlysplituplong-runningthreadsorhandlersintosmaller ants)withdifferentschedulingpoliciesbasedonpriorities,
onesthatreentertheschedulermorefrequently.Thissolution achievedutilityorrequiredresources.Thesepaperstypically
is similarly applicable in our domain, and is the approach considerproblemsrelatedtoadmissioncontrol,allocating
taken,forexample,byGoogle’sWebsearchsystem[15].How- resourcestomaximizetotalutility,ordistributedscheduling
ever,itrequiresmanualinterventionfromdevelopers,and anddonotdealwithprovidingfine-grainedresourcefairness.
onlyreducestherangeofrequestcosts–itdoesnoteliminate Schedulingrequestswithinaccurateorunknownsizehasbeen
variationentirely.Theapproachisfundamentallyconstrained studiedpreviously[2,62].However,thesepapersconcentrate
byfactorsthataffectexecutionefficiency,e.g.dataloadedin onvariouspriority-basedpolicies,suchasshortest-job-first
varioussystemcachesandintermediarymemoryallocation, orshortest-remaining-time-first,andignoreresourcefairness.
andisburdenedbyneedfor“stackripping”[1].Analternative Forexample,Aalo[12],schedulesco-flowsinanetworkwith-
tomanualinterventionisframeworksupportforautomati- outpriorknowledgeoftheirsize;byusingapriorityqueue
callyreenteringthescheduler,forexamplebyanalyzingcode wherenewflowsstartatthehighestpriorityandtheirpriority
toidentifytheboundariesofcriticalsections[57],oraspartof decreasesastheysendmoredata.
thelanguageruntime[18].Inallofthesesystems,iffairnessis
agoal,then2DFQcanbeusedtoprovidesmoothaverage-case 9. CONCLUSION
schedules.
Inthispaperwedemonstratedthechallengesoffairqueu-
Middlebox Packet Processing Dominant-Resource Fair
inginmulti-tenantservices,whererequestswithlargecost
Queuing(DRFQ)[21],amulti-resourcequeueschedulerfor
varianceexecuteconcurrentlyacrossmanythreads.Wepro-
middleboxpacketprocessing,allowsconcurrentexecution
posedandevaluatedapracticalschedulerforsuchsettings,
ofmultiplerequests,suchasontheCPU,butdoesnotdeal
Two-DimensionalFairQueuing,whichachievessignificantly
withlargevariationinrequestcostsandonlypermitsserial
moresmoothschedulesandcanimprovelatenciesofsmall
executionforeachtenant.DRFQbuildsontopofSFQand
requestswhencompetingwithlargerequests.
useslinearresourceconsumptionmodelsfordifferenttypes
of requests. The authors show that for several middle-box
moduleslinearmodelsworkrelativelywell,butacknowledge
thatifmodelsareinaccurate,allocatedsharesmightbeoff

10. REFERENCES highlyavailablekey-valuestore.21stACMSymposiumon
OperatingSystemsPrinciples(SOSP’07).(§1).
[1] Adya,A.,Howell,J.,Theimer,M.,Bolosky,W.J.,and
|     |     |     |     |     |     |     | [17] Demers,A.,Keshav,S.,andShenker,S.Analysisand |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
Douceur,J.R.Cooperativetaskmanagementwithout
simulationofafairqueueingalgorithm.1989Conference
manualstackmanagement.2002USENIXAnnualTechni-
oftheACMSpecialInterestGrouponDataCommunication
| calConference(ATC’02).(§8). |     |     |     |     |     |     | (SIGCOMM’89).(§8). |     |     |     |     |     |     |     |
| --------------------------- | --- | --- | --- | --- | --- | --- | ------------------ | --- | --- | --- | --- | --- | --- | --- |
[2] Amico,M.D.,Carra,D.,andMichiardi,P.PSBS:Prac-
|     |     |     |     |     |     |     | [18] Deshpande,N.,Sponsler,E.,andWeiss,N.Analysis |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
ticalsize-basedscheduling.IEEETransactionsonCom-
ofthegoruntimescheduler.https://goo.gl/JRfNn3,2012.
puters(2016).(§8).
[Online;accessedJune2016].(§8).
[3] Angel,S.,Ballani,H.,Karagiannis,T.,O’Shea,G.,
|     |           |               |     |             |           |     | [19] SummaryoftheAmazonDynamoDBServiceDisruption. |     |     |     |     |     |     |     |
| --- | --------- | ------------- | --- | ----------- | --------- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
| and | Thereska, | E. End-to-end |     | performance | isolation |     |                                                   |     |     |     |     |     |     |     |
https://goo.gl/R2SKKs.[Online;accessedJune2016].(§1).
throughvirtualdatacenters.11thUSENIXSymposiumon
|     |     |     |     |     |     |     | [20] QualityofServiceinHadoop.http://goo.gl/diwR00.[On- |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
OperatingSystemsDesignandImplementation(OSDI’14).
line;accessedJune2016].(§1and2).
(§2,3.2,and8).
|               |       |          |                              |     |     |     | [21] Ghodsi, | A., | Sekar, | V., Zaharia, |     | M., and | Stoica, | I.  |
| ------------- | ----- | -------- | ---------------------------- | --- | --- | --- | ------------ | --- | ------ | ------------ | --- | ------- | ------- | --- |
| [4] Microsoft | Azure | Storage. | https://azure.microsoft.com/ |     |     |     |              |     |        |              |     |         |         |     |
Multi-resourceFairQueueingforPacketProcessing.2012
| services/storage/. |     | [Online; |     | accessed June | 2016]. | (§1, 3, |            |     |            |         |          |       |     |      |
| ------------------ | --- | -------- | --- | ------------- | ------ | ------- | ---------- | --- | ---------- | ------- | -------- | ----- | --- | ---- |
|                    |     |          |     |               |        |         | Conference |     | of the ACM | Special | Interest | Group | on  | Data |
and6).
Communication(SIGCOMM’12).(§3.1and8).
[5] Bennett,J.C.,andZhang,H.Hierarchicalpacketfair
|     |     |     |     |     |     |     | [22] Goyal,P.,Guo,X.,andVin,H.M.Ahierarchicalcpu |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
queueingalgorithms.1996ConferenceoftheACMSpecial
schedulerformultimediaoperatingsystems.2ndUSENIX
InterestGrouponDataCommunication(SIGCOMM’96).
SymposiumonOperatingSystemsDesignandImplementa-
(§6).
tion(OSDI’96).(§8).
[6] Bennett,J.C.,andZhang,H.WF2Q:Worst-casefair
|     |     |     |     |     |     |     | [23] Goyal, | P., | Vin, H. | M., and | Chen, | H. Start-time |     | fair |
| --- | --- | --- | --- | --- | --- | --- | ----------- | --- | ------- | ------- | ----- | ------------- | --- | ---- |
weightedfairqueueing.15thIEEEConferenceonComputer
queueing:aschedulingalgorithmforintegratedservices
Communications(INFOCOM’96).(§1,2,4,and8).
packetswitchingnetworks.1996ConferenceoftheACM
| [7] Blanquer, |     | J. M., Batchelli, |     | A., Schauser, | K., | and |         |          |       |     |                    |     |     |       |
| ------------- | --- | ----------------- | --- | ------------- | --- | --- | ------- | -------- | ----- | --- | ------------------ | --- | --- | ----- |
|               |     |                   |     |               |     |     | Special | Interest | Group | on  | Data Communication |     |     | (SIG- |
Wolski,R.Quorum:Flexiblequalityofserviceforin- COMM’96).(§2,6,and8).
ternetservices.2ndUSENIXSymposiumonNetworked
|     |     |     |     |     |     |     | [24] Guitart,J.,Torres,J.,andAyguadé,E.Asurveyon |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
SystemsDesignandImplementation(NSDI’05).(§8).
performancemanagementforinternetapplications.Con-
[8] Blanquer,J.M.,andÖzden,B.Fairqueuingforaggre-
currencyandComputation:PracticeandExperience22,1
gatedmultiplelinks.2001ConferenceoftheACMSpecial
(2010),68–106.(§8).
InterestGrouponDataCommunication(SIGCOMM’01).
|     |     |     |     |     |     |     | [25] Gulati,A.,Merchant,A.,andVarman,P.J.mClock: |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
(§1,2,4,6,and8).
handlingthroughputvariabilityforhypervisorIOschedul-
| [9] Calder, | B., | Wang, | J., Ogus, | A., Nilakantan, |     | N., |     |     |     |     |     |     |     |     |
| ----------- | --- | ----- | --------- | --------------- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
ing.9thUSENIXSymposiumonOperatingSystemsDesign
Skjolsvold,A.,McKelvie,S.,Xu,Y.,Srivastav,S.,Wu,
andImplementation(OSDI’10).(§8).
J.,Simitci,H.,etal.WindowsAzureStorage:ahighly
|     |     |     |     |     |     |     | [26] Gulati,A.,Merchant,A.,andVarman,P.J.pClock: |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
availablecloudstorageservicewithstrongconsistency.
anarrivalcurvebasedapproachforQoSguaranteesin
23rdACMSymposiumonOperatingSystemsPrinciples
sharedstoragesystems.2007ACMInternationalConfer-
(SOSP’11).(§1,1,2,3,and6).
enceonMeasurementandModelingofComputerSystems
[10] CASSANDRA-8032:Userbasedrequestscheduler.https:
(SIGMETRICS’07).(§8).
//goo.gl/PhHhai.[Online;accessedJune2016].(§2).
|     |     |     |     |     |     |     | [27] Guo,Z.,McDirmid,S.,Yang,M.,Zhuang,L.,Zhang, |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------ | --- | --- | --- | --- | --- | --- | --- |
[11] LinuxControlGroups.https://goo.gl/DDsmig.[Online;
P.,Luo,Y.,Bergan,T.,Musuvathi,M.,Zhang,Z.,and
accessedJune2016].(§8).
Zhou,L.FailureRecovery:WhentheCureIsWorseThan
[12] Chowdhury,M.,andStoica,I.Efficientcoflowschedul- theDisease.14thUSENIXWorkshoponHotTopicsinOp-
ing without prior knowledge. 2015 Conference of the eratingSystems(HotOS’13).(§1and2).
ACMSpecialInterestGrouponDataCommunication(SIG-
|     |     |     |     |     |     |     | [28] HADOOP-3810:NameNodeseemsunstableonaclus- |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ---------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
COMM’15).(§8).
terwithlittlespaceleft.https://goo.gl/nl2mWL.[Online;
[13] CLOUDSTACK-618:APIrequestthrottlingtoavoidma-
accessedJune2016].(§1and2).
liciousattacksonMSperaccountthroughfrequentAPI
|     |     |     |     |     |     |     | [29] HADOOP-9640:RPCCongestionControlwithFairCal- |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
request. https://goo.gl/m8F4Ic. [Online; accessed June lQueue.https://goo.gl/ucFHWJ.[Online;accessedJune
2016].(§2).
2016].(§2).
[14] APIRequestThrottling.https://goo.gl/gl1bGE.[Online;
|                             |     |     |     |     |     |     | [30] Apache           | HBase. | http://hbase.apache.org. |     |     |     | [Online; | ac- |
| --------------------------- | --- | --- | --- | --- | --- | --- | --------------------- | ------ | ------------------------ | --- | --- | --- | -------- | --- |
| accessedJune2016].(§1and2). |     |     |     |     |     |     | cessedJune2016].(§2). |        |                          |     |     |     |          |     |
[15] Dean,J.,andBarroso,L.A.Thetailatscale.Communi-
|     |     |     |     |     |     |     | [31] HBASE-11598:AddsimpleRPCthrottling.https://goo.gl/ |     |     |     |     |     |     |     |
| --- | --- | --- | --- | --- | --- | --- | ------------------------------------------------------- | --- | --- | --- | --- | --- | --- | --- |
cationsoftheACM56,2(2013),74–80.(§7and8).
mxokpa.[Online;accessedJune2016].(§2).
[16] DeCandia,G.,Hastorun,D.,Jampani,M.,Kakulap-
|     |     |     |     |     |     |     | [32] HDFS-4183: |     | Throttle | block | recovery. | https://goo.gl/ |     |     |
| --- | --- | --- | --- | --- | --- | --- | --------------- | --- | -------- | ----- | --------- | --------------- | --- | --- |
ati,G.,Lakshman,A.,Pilchin,A.,Sivasubramanian,
EGYvuX.[Online;accessedJune2016].(§2).
S.,Vosshall,P.,andVogels,W.Dynamo:Amazon’s

[33] HDFS-945:MakeNameNoderesilienttoDoSattacks(ma- 5thUSENIXSymposiumonOperatingSystemsDesignand
liciousorotherwise).https://goo.gl/YCAYgk.[Online;ac- Implementation(OSDI’02).(§8).
cessedJune2016].(§1and2). [49] Shi,H.,Sethu,H.,andKanhere,S.S.Anevaluationof
[34] DenialofServiceResilience.https://goo.gl/SXP1wG.[On- fairpacketschedulersusinganovelmeasureofinstanta-
line;accessedJune2016].(§2). neousfairness.Computercommunications28,17(2005),
[35] Henderson,K.Theguru’sguidetosqlserverarchitecture 1925–1937.(§6,9a,and6.1.2).
andinternals.(§8). [50] Shreedhar,M.,andVarghese,G.Efficientfairqueue-
[36] Hunt, P., Konar, M., Junqueira, F. P., and Reed, B. ing using deficit round robin. 1995 Conference of the
ZooKeeper: Wait-free Coordination for Internet-scale ACMSpecialInterestGrouponDataCommunication(SIG-
Systems.2010USENIXAnnualTechnicalConference(ATC COMM’95).(§2,6,and8).
’10).(§1and2). [51] Shue,D.,andFreedman,M.J.Fromapplicationrequests
[37] Kornacker,M.,Behm,A.,Bittorf,V.,Bobrovytsky, tovirtualiops:Provisionedkey-valuestoragewithlibra.
T.,Ching,C.,Choi,A.,Erickson,J.,Grund,M.,Hecht, 9thACMEuropeanConferenceonComputerSystems(Eu-
D.,Jacobs,M.,etal.Impala:Amodern,open-source roSys’14).(§3.2).
SQLengineforhadoop.7thBiennialConferenceonInno- [52] Shue,D.,Freedman,M.J.,andShaikh,A.Performance
vativeDataSystemsResearch(CIDR’15).(§2). isolationandfairnessformulti-tenantcloudstorage.10th
[38] KUDU-1395:ScannerKeepAliverequestscangetstarved USENIX Symposium on Operating Systems Design and
onanoverloadedserver.https://goo.gl/A5VNUO.[On- Implementation(OSDI’12).(§2,3.2,and8).
line;accessedJune2016].(§2). [53] Shvachko,K.,Kuang,H.,Radia,S.,andChansler,
[39] Lauer,H.C.,andNeedham,R.M.Onthedualityof R.TheHadoopDistributedFileSystem.26thIEEESym-
operatingsystemstructures.ACMSIGOPSOperatingSys- posiumonMassStorageSystemsandTechnologies(MSST
temsReview13,2(1979),3–19.(§8). ’10).(§1and2).
[40] Li, T., Baumberger, D., and Hahn, S. Efficient and [54] Thereska,E.,Ballani,H.,O’Shea,G.,Karagiannis,
scalablemultiprocessorfairschedulingusingdistributed T.,Rowstron,A.,Talpey,T.,Black,R.,andZhu,T.
weightedround-robin.14thACMSymposiumonPrinci- IOFlow:ASoftware-definedStorageArchitecture.24th
ples and Practice of Parallel Programming (PPoPP ’09). ACMSymposiumonOperatingSystemsPrinciples(SOSP
(§8). ’13).(§2and8).
[41] Lipcon, T., Alves, D., Burkert, D., Cryans, J.-D., [55] User-ModeScheduling.https://goo.gl/0JJRNl.[Online;
Dembo,A.,Percy,M.,Rus,S.,Wang,D.,Bertozzi,M., accessedJune2016].(§8).
McCabe,C.P.,andWang,A.Kudu:StorageforFastAn- [56] VonBehren,J.R.,Condit,J.,andBrewer,E.A.Why
alyticsonFastData.http://getkudu.io/kudu.pdf.[Online; eventsareabadidea(forhigh-concurrencyservers).14th
accessedJune2016].(§2). USENIXWorkshoponHotTopicsinOperatingSystems
[42] Lu,H.,Saltaformaggio,B.,Kompella,R.,andXu, (HotOS’03).(§8).
D.vFair:latency-awarefairstorageschedulingviaper-IO [57] VonBehren,R.,Condit,J.,Zhou,F.,Necula,G.C.,
cost-baseddifferentiation.6thACMSymposiumonCloud andBrewer,E.Capriccio:scalablethreadsforinternet
Computing(SoCC’15).(§3.2). services.19thACMSymposiumonOperatingSystemsPrin-
[43] Mace,J.,Bodik,P.,Fonseca,R.,andMusuvathi,M. ciples(SOSP’03).(§8).
Retro:TargetedResourceManagementinMulti-tenant [58] Waldspurger,C.A.,andWeihl,W.E.Lotteryschedul-
Distributed Systems. 12th USENIX Symposium on Net- ing:Flexibleproportional-shareresourcemanagement.
workedSystemsDesignandImplementation(NSDI’15). 1stUSENIXSymposiumonOperatingSystemsDesignand
(§2,3.2,and8). Implementation(OSDI’94).(§8).
[44] Ousterhout,J.Whythreadsareabadidea(formost [59] Waldspurger,C.A.,andWeihl,W.E.Strideschedul-
purposes). 1996 USENIX Annual Technical Conference ing:Deterministicproportionalshareresourcemanage-
(ATC’96).[Presentation].(§8). ment.(§8).
[45] Pabla,C.S.Completelyfairscheduler.LinuxJournal,184 [60] Wang,A.,Venkataraman,S.,Alspaugh,S.,Katz,R.,
(2009),4.(§8). andStoica,I.Cake:EnablingHigh-levelSLOsonShared
[46] Parekh,A.K.,andGallager,R.G.Ageneralizedpro- StorageSystems.3rdACMSymposiumonCloudComput-
cessorsharingapproachtoflowcontrolinintegratedser- ing(SoCC’12).(§2and8).
vicesnetworks-thesingle-nodecase.11thIEEEConference [61] Wang,H.,andVarman,P.J.Balancingfairnessandef-
on Computer Communications (INFOCOM ’92). (§1, 2, ficiencyintieredstoragesystemswithbottleneck-aware
and8). allocation.12thUSENIXConferenceonFileandStorage
[47] Schuller,P.Manhattan,ourreal-time,multi-tenantdis- Technologies(FAST14).(§2and8).
tributeddatabaseforTwitterscale.https://goo.gl/lcZJWC. [62] Wierman,A.,andNuyens,M.Schedulingdespiteinex-
[Online;accessedJune2016].(§2). actjob-sizeinformation.2008ACMInternationalConfer-
[48] Shen,K.,Tang,H.,Yang,T.,andChu,L.Integrated enceonMeasurementandModelingofComputerSystems
resourcemanagementforcluster-basedinternetservices. (SIGMETRICS’08).(§8).