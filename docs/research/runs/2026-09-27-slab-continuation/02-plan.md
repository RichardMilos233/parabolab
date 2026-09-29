# Fixed execution and experimental protocol

Theory→Lean→code. Conventional C1–C7 are recorded before implementation and reviewed independently. Start numerical implementation only after the relevant Lean algebra/projection/recurrence core builds with no placeholders; later semantic review remains mandatory.

The planned algorithm uses the existing raw Allen–Cahn derivative-code law on short slabs, plus an explicitly biased three-sine continuation interface. The task is a bounded one-dimensional MC reference implementation, not an NN or latent/Fourier model project. No existing algorithm, old run evidence or prior formal entrypoint is to be rewritten.

## Numerical object and parameters

Forward elapsed-time PDE u_s=u_xx/2+u−u³ on a torus. Terminal inputg=A sn(κx|m),m=.05,A=√(2/21),κ=√(40/21),periodL=4ellipk(m)/κ. Basis√2 sin(nωx),n=1,3,5. Projectioncaps(.23,.003,.00005). Rate2,slab≤.08. Eachstage estimates coefficients from iiduniformX and complete localtrees. Exactterminalg andg′onlyatstage1; all laterleaves read frozen learnedcoefficients. This dependency is to be enforced by a test that makes any late oraclecall fail.

Vectorized normalized code law must reproduce original sampler value distribution: Id→F0; Dx→(F1,Dx); Fk chooses rawq=.5 before handling its tuple; labels0 have coefficient2 after probability correction, labels1 coefficient−1, then lifetimefactor exp(2τ)/2. Structural zero tuples may return0 immediately after the label is selected, without probability renormalization; record this exact optimization in cost accounting. Every started root completes; no depth/node cutoff, failed-tree deletion, clipping of treeweights or adaptive samplecount based on the output.

## Checks before production runs

1. Deterministic scripted-draw checks of leaf survival, unaryId branch, positive and negative F labels, zero labels and shared childbirthposition. Verify the six normalized signed and squared polynomials independently, not by repeating the sampler logic in a test.
2. Distribution checks against existing sample_tree for a frozen admissible polynomial at multiple rootcodes/points. Predetermined independent seeds; compare means and secondmoments with uncertainty, and record deviations instead of selecting seeds. These are numerical diagnostics alongside the moment theorem.
3. Exact coefficient projection/range/derivative-bound checks including adversarial outsideboxvectors. Confirm identical frozen-interface use across one entire stage; no true-solution resets afterstage1.
4. Jacobi reference, stationarity, Fouriercoefficients and tail cross-check using an independent high-precision/library calculation after the Lean gate. Keep analytical proof as the guarantee; sampled-grid agreement alone is insufficient.

## Production study

Primary:N=200000 perstage,50slabs,T=4,seeds2026092701/2026092702/2026092703. Saveeveryintermediate stage,includingT=.8,1.6,2,4. Allthree runs complete even if one looksbad. A smallerN=50000 sensitivityrun atseed2026092799 is allowed after primary, to diagnose budgetdependence; label empirical only. Do not retunecapsorvariancecertificateafterseeingresultswithoutversioningthetheory.

Perstage records:raw andprojectedcoefficients,projectionmask/distortion,rootcount,totalnodes,rootbranchcount,terminalcodecounts,maxobservedweight,first/secondmomentdiagnostics,coefficientcovariance,time. Save root-level X,H,nodecounts in compressed chunked archives where feasible; productiontarget10millionroots/run means roughly240MB/run forfloat64X/H,int32nodes beforecompression. Ifstorageisprohibitive,preserveperbatchsufficientstatisticsandrecordthelossofindividualsampleaudit ratherthanclaimrawsampleswerekept.

MeasureL²error by exact known Fouriercoefficients plus analyticaltail; cross-check a fineperiodicgrid. Reportactualrunerrors separatelyfromtheensembleRMSbound. The latter isspatiallynormalizedL², notpointwiseorhigh-probability. Validatefinitefloatoutputs; floating/special-functionerror isnotincludedintheanalyticreal-arithmeticcertificate.

Comparator:one full bounded-majority tree per randomspatialroot, same three coefficientobservations/projection andPDE. InitiallyT=.8 and2,N=8000 each,seeds2026092711/2026092712/2026092713. This uses sufficient secondmoment≤1 toobtain coefficientvariance≤3/N plusnegligibletail. T=4 fullmajority expectednodes/root=(3exp16−1)/2 makes its prescribed8000-root budget expensive; do notrunthatbudgetjustforatable. Report its theoreticalwork separately, clearly distinguishedfrommeasuredtiming.

Run theoriginal unsplitrawalgorithm onlyatmatchedsmallhforidentityverificationunlessa boundedtheoryaudityieldsasafeglobalcomparison. Neverapplythepreviousflat1.44551thresholdtothisstationarynonconstantg.

## Stop and failure rules

Initialimplementation smokecheck beforeproduction; reserveatmosttwoCPUhoursforthisboundedstudy. Ifa productionrunexceedsthecap,keepitscheckpointandmarkincomplete; partialcompletedtreesmaynotbesilentlyaveragedasafullresult. NeverchangethePDEoritsamplitudetoimproveobservedplots. Ifstatisticalcheckscontradicttheidentity,returntotheory/correspondencebeforefurtherlongTsampling.

Expected theoreticalnodecost is an upperbound, not measuredspeed. Comparisonunderthesesufficienterrorbudgetsdoesnotproveoptimalityofthemethodorofeitherbudget. A stationary exactsolutionisalimited feasibilityexample; successdoesnotestablishmovingfront,arbitraryterminal,high-dimensionalorhigher-jetcapability.
