// dynamic-continuation-evidence.canvas.tsx
import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Grid,
  H1,
  H2,
  LineChart,
  Link,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  useHostTheme
} from "cursor/canvas";
import { jsx, jsxs } from "react/jsx-runtime";
var times = [0, 0.08, 0.16, 0.24, 0.32, 0.4, 0.48, 0.56, 0.64, 0.72, 0.8, 0.88, 0.96, 1.04, 1.12, 1.2, 1.28, 1.36, 1.44, 1.52, 1.6, 1.68, 1.76, 1.84, 1.92, 2, 2.08, 2.16, 2.24, 2.32, 2.4, 2.48, 2.56, 2.64, 2.72, 2.8000000000000003, 2.88, 2.96, 3.04, 3.12, 3.2, 3.2800000000000002, 3.36, 3.44, 3.52, 3.6, 3.68, 3.7600000000000002, 3.84, 3.92, 4, 4.08, 4.16, 4.24, 4.32, 4.4, 4.48, 4.5600000000000005, 4.64, 4.72, 4.8, 4.88, 4.96, 5.04, 5.12, 5.2, 5.28, 5.36, 5.44, 5.5200000000000005, 5.6000000000000005, 5.68, 5.76, 5.84, 5.92, 6, 6.08, 6.16, 6.24, 6.32, 6.4, 6.48, 6.5600000000000005, 6.640000000000001, 6.72, 6.8, 6.88, 6.96, 7.04, 7.12, 7.2, 7.28, 7.36, 7.44, 7.5200000000000005, 7.6000000000000005, 7.68, 7.76, 7.84, 7.92, 8, 8.08, 8.16, 8.24, 8.32, 8.4, 8.48, 8.56, 8.64, 8.72, 8.8, 8.88, 8.96, 9.040000000000001, 9.120000000000001, 9.200000000000001, 9.28, 9.36, 9.44, 9.52, 9.6, 9.68, 9.76, 9.84, 9.92, 10, 10.08, 10.16, 10.24, 10.32, 10.4, 10.48, 10.56, 10.64, 10.72, 10.8, 10.88, 10.96, 11.040000000000001, 11.120000000000001, 11.200000000000001, 11.28, 11.36, 11.44, 11.52, 11.6, 11.68, 11.76, 11.84, 11.92, 12, 12.08, 12.16, 12.24, 12.32, 12.4, 12.48, 12.56, 12.64, 12.72, 12.8, 12.88, 12.96, 13.040000000000001, 13.120000000000001, 13.200000000000001, 13.280000000000001, 13.36, 13.44, 13.52, 13.6, 13.68, 13.76, 13.84, 13.92, 14, 14.08, 14.16, 14.24, 14.32, 14.4, 14.48, 14.56, 14.64, 14.72, 14.8, 14.88, 14.96, 15.040000000000001, 15.120000000000001, 15.200000000000001, 15.280000000000001, 15.36, 15.44, 15.52, 15.6, 15.68, 15.76, 15.84, 15.92, 16];
var empiricalRms = [0, 23339408029152998e-20, 3784332342046206e-19, 5036523404201009e-19, 4746775942779389e-19, 4347182650571657e-19, 7309578549881803e-19, 4422355218909285e-19, 4403457402084484e-19, 719247790463001e-18, 9590485308689482e-19, 7629249782335103e-19, 8768325309002412e-19, 0.0011734078562671958, 0.0011404709982474402, 0.001510570355727619, 0.0018869374148109761, 0.0019515791924395582, 0.0021196228421959842, 0.0017777722818622514, 0.0018172240224462012, 0.00234227611374183, 0.002023578017299989, 0.0018131219329032815, 0.001510844855246385, 0.0013394761624785573, 0.0013376087576212762, 0.0010862705014295124, 0.00116603733190151, 0.0013002054346777326, 0.0018111534262245158, 0.0017851973748871277, 0.0018244300991134934, 0.0017425649863312617, 0.0021450485932708314, 0.0024284830593536573, 0.0022493217544041896, 0.0023672898338336556, 0.0019579752466244954, 0.0020137280456022405, 0.0021471798777769635, 0.001929073729303542, 0.0013482495605855792, 0.0010876461424942398, 9783630576227767e-19, 7913275901407557e-19, 5297245406827146e-19, 878304816894741e-18, 0.001049830028880273, 0.0012788684902770937, 0.0013793555306341552, 9357566694678011e-19, 8744327035888887e-19, 6301270473862713e-19, 5949872376023156e-19, 9727125097205828e-19, 0.0010856056798561622, 0.0014022874939508482, 0.0016797052792468631, 0.0018625051213208054, 0.002258402256167908, 0.0016585673788167892, 0.001310090041033374, 0.0016077250025341048, 0.0017091843294505206, 0.0015577549838365521, 0.0016083215661434052, 0.0013273433777414925, 0.0017351434597462885, 0.0023128646101954475, 0.002521097904127024, 0.002910895428399663, 0.003078270203235183, 0.00304945167803442, 0.00287631718725785, 0.002840002970833056, 0.002291375258155617, 0.002378727519012544, 0.0022255084232937926, 0.0025786990270745833, 0.002632222081746047, 0.0021516529870555267, 0.002252456734535609, 0.0016604606419398614, 0.0015216060308207199, 0.0023268349656839237, 0.0028335981917425005, 0.0035760788292035234, 0.0029168168073772896, 0.0033464490498027683, 0.0031675047522717833, 0.002862805382243056, 0.0028301770701410715, 0.002646391432044081, 0.0025977584750024674, 0.0027514189735796044, 0.0022714270193954, 0.0021168193370974045, 0.002463752141741039, 0.002249310813553365, 0.001976846176790009, 0.001426403287671042, 0.001512332921263693, 0.0012619721044253246, 0.0014161740700962405, 0.0016149649668466919, 0.002033436807288492, 0.0022290867137502984, 0.0025371769585057764, 0.002280862768547315, 0.002964034451337882, 0.003019046545815959, 0.0033667368438044685, 0.0037569478057603075, 0.003903670035959042, 0.003940481788456896, 0.004117203676336045, 0.004283056977782264, 0.004301094890799265, 0.004092416804684282, 0.004143172046840106, 0.0037297024676069017, 0.004176019521789957, 0.003698910024128224, 0.0037384541098862733, 0.004013755469617206, 0.004127987452345937, 0.004396649341446307, 0.003975946057421026, 0.003979674026873933, 0.0038929292223919168, 0.0034749071920048853, 0.0034572901129390006, 0.0034570560415171903, 0.0034431838416114973, 0.0034781239633636407, 0.003315751947728187, 0.0033940239165114613, 0.0030599101457576498, 0.0029714233751703388, 0.0027185266753584035, 0.0031981758195395037, 0.0033672880419520256, 0.003718105306127145, 0.004199882854325327, 0.003915029303037212, 0.003838780332482151, 0.004069711977800643, 0.003749209709393859, 0.0037371347318547656, 0.0034920186833606536, 0.003550256343512401, 0.0033856436360883203, 0.0034030267257128674, 0.003570014960387322, 0.004003611528317124, 0.003874106919670075, 0.004032167251146706, 0.0040962178615878775, 0.004680482579961569, 0.00429694869103198, 0.003950525169198855, 0.004117564033008005, 0.0039922960937781365, 0.004449619450760829, 0.004234289536001394, 0.004222522311746394, 0.004311257821127961, 0.0041777305039068045, 0.004140012328955068, 0.0038698022284405103, 0.003490612885542874, 0.003415561660999734, 0.003179932371091468, 0.003345930477726196, 0.003806357376898831, 0.00333805474835873, 0.0032165284883107345, 0.003275082008959066, 0.003415525459464136, 0.0038206320605214516, 0.003746640793326679, 0.003633832678634308, 0.0031187236958893708, 0.002996910412783156, 0.003128687379793468, 0.003262294699917086, 0.0035080597378183346, 0.004003934481368954, 0.004381898477312108, 0.0038599348497812425, 0.003807865429213176, 0.0036084291828965185, 0.0033073178550298973, 0.0032015904454595363, 0.002778125301223682, 0.002936893975379868, 0.0027093297332696094, 0.002746160442497317, 0.0036177458506608563, 0.003539624140161601];
var midpoint095g = [0.010945815911642037, 0.010732532959291363, 0.01052116182016813, 0.010311540784997708, 0.010103630781016674, 0.009897423269925473, 0.009692915034015577, 0.009490102183768034, 0.00928897930797963, 0.009089539770864935, 0.008891776117364508, 0.008695680374460588, 0.008501244243551375, 0.008308459216200848, 0.00811731664216826, 0.007927807769226839, 0.007739923766722856, 0.007553655739879444, 0.007368994738867987, 0.007185931764928976, 0.007004457774830104, 0.0068245636843895134, 0.006646240371471221, 0.006469478678684566, 0.006294269415920024, 0.006120603362795524, 0.005948471271060789, 0.0057778638669867865, 0.00560877185376129, 0.005441185913906358, 0.005275096711733376, 0.005110494895849807, 0.0049473711017367986, 0.004785715954417974, 0.004625520071244621, 0.004466774064828745, 0.0043094685461636814, 0.004153594127980335, 0.003999141428402752, 0.003846101074981465, 0.003694463709207597, 0.0035442199916415227, 0.0033953606078289656, 0.003247876275236401, 0.0031017577515119604, 0.002956995844490449, 0.0028135814245058652, 0.0026715054398016146, 0.00253075893613805, 0.0023913330821704842, 0.0022532192028709946, 0.002116408824351125, 0.001980893735135433, 0.001846666071656606, 0.0017137184402323028, 0.001582044095415927, 0.00145163720803555, 0.0013224932807810515, 0.0011946098161341157, 0.0010679874359871692, 9426318548738123e-19, 8185575761542394e-19, 6957953617580644e-19, 5744088749810594e-19, 4545369329049672e-19, 3365225887790585e-19, 2214382932255319e-19, 11463618972301581e-20, 6898423582806336e-20, 1519705814638516e-19, 25956545004248306e-20, 36991375165393216e-20, 4803502469379035e-19, 590208006172467e-18, 6992491690587449e-19, 8073715162943428e-19, 9145265886977706e-19, 0.0010206906660152556, 0.0011258526893456904, 0.0012300086162693245, 0.0013331585392375998, 0.0014353051087041201, 0.0015364526202841506, 0.0016366064611235353, 0.0017357727606901606, 0.0018339581629921665, 0.0019311696736208366, 0.0020274145543909923, 0.0021227002491173304, 0.0022170343302647844, 0.002310424459903831, 0.002402878360666113, 0.002494403793812703, 0.0025850085424476677, 0.0026747003985063272, 0.002763487152551636, 0.0028513765856866273, 0.00293837646307828, 0.0030244945287240415, 0.003109738501184898, 0.0031941160700781407, 0.0032776348931725955, 0.0033603025939664536, 0.0034421267596525624, 0.0035231149394009597, 0.003603274642899924, 0.0036826133391108617, 0.003761138455200419, 0.0038388573756226183, 0.003915777441324607, 0.003991905949060716, 0.004067250150796066, 0.004141817253188944, 0.00421561441714085, 0.0042886487574053025, 0.004360927342248507, 0.004432457193154836, 0.004503245284573602, 0.004573298543700614, 0.004642623850292537, 0.004711228036510339, 0.00477911788678824, 0.004846300137727389, 0.004912781478010782, 0.004978568548338061, 0.005043667941378881, 0.005108086201743636, 0.005171829825969476, 0.0052349052625208356, 0.00529731891180442, 0.005359077126196917, 0.005420186210084063, 0.005480652419911904, 0.005540481964248311, 0.005599681003854927, 0.005658255651768247, 0.005716211973390621, 0.005773555986589047, 0.005830293661803094, 0.005886430922159433, 0.005941973643595348, 0.0059969276549880855, 0.006051298738292106, 0.00610509262868163, 0.006158315014701, 0.006210971538419238, 0.006263067795591532, 0.006314609335826379, 0.006365601662756518, 0.006416050234216516, 0.006465960462423934, 0.006515337714166034, 0.006564187310989888, 0.00661251452939793, 0.006660324601046089, 0.006707622712947208, 0.006754414007677248, 0.006800703583585044, 0.006846496495005942, 0.006891797752478615, 0.006936612322964037, 0.006980945130068581, 0.007024801054269486, 0.00706818493314234, 0.007111101561592243, 0.007153555692086534, 0.007195552034890064, 0.007237095258302572, 0.007278189988898449, 0.007318840811767641, 0.00735905227075953, 0.007398828868727273, 0.007438175067774957, 0.007477095289505338, 0.00751559391526947, 0.007553675286417457, 0.007591343704550595, 0.007628603431774877, 0.007665458690954818, 0.00770191366596905, 0.0077379725019661085, 0.007773639305621888, 0.007808918145396664, 0.007843813051793982, 0.007878328017619035, 0.007912466998238676, 0.007946233911840718, 0.007979632639694378, 0.008012667026410536, 0.008045340880202976, 0.008077657973148479, 0.008109622041448614, 0.008141236785690516, 0.008172505871107625, 0.008203432927841038, 0.008234021551200222, 0.008264275301923777, 0.008294197706439969, 0.008323792257126723, 0.008353062412571405, 0.008382011597830955];
var equilibriumG = [0.021891631823283946, 0.02167828214308843, 0.021466814317783738, 0.02125711905052249, 0.02104915962219142, 0.020842920379029815, 0.02063839147544801, 0.02043556447602111, 0.020234431156270053, 0.020034983215817082, 0.01983721223487202, 0.019641109685744704, 0.019446666950631887, 0.01925387533557026, 0.01906272608007695, 0.018873210363750892, 0.01868531931100132, 0.018499043994679026, 0.018314375439079718, 0.01813130462258678, 0.017949822480102615, 0.017769919905353326, 0.017591587753110323, 0.017414816841354333, 0.01723959795339607, 0.017065921839958857, 0.016893779221229293, 0.01672316078887624, 0.016554057208040065, 0.016386459119292388, 0.01622035714056719, 0.01605574186906195, 0.015892603883110226, 0.015730933744025205, 0.015570721997913855, 0.0154119591774619, 0.015254635803690061, 0.015098742387680499, 0.014944269432274797, 0.01479120743374228, 0.014639546883419157, 0.014489278269319237, 0.014340392077714845, 0.014192878794689388, 0.014046728907660084, 0.0139019329068739, 0.01375848128687237, 0.013616364547929725, 0.013475573197461356, 0.013336097751405058, 0.0131979287355732, 0.013061056686977263, 0.01292547215512474, 0.012791165703288086, 0.01265812790974602, 0.01252634936899796, 0.012395820692951233, 0.012266532512081305, 0.012138475476565078, 0.012011640257388316, 0.011886017547425916, 0.011761598062497183, 0.011638372542394661, 0.011516331751887666, 0.011395466481700532, 0.01127576754946531, 0.011157225800650395, 0.011039832109464236, 0.010923577379735093, 0.010808452545765977, 0.010694448573166858, 0.010581556459662841, 0.010469767235879179, 0.01035907196610382, 0.010249461749026714, 0.010140927718456835, 0.010033461044018008, 0.009927052931821771, 0.009821694625119845, 0.00971737740493434, 0.009614092590668123, 0.00951183154069414, 0.009410585652924098, 0.009310346365357608, 0.009211105156611582, 0.009112853546430176, 0.009015583096175124, 0.008919285409298174, 0.008823952131794226, 0.008729574952636487, 0.00863614560419428, 0.0085436558626318, 0.008452097548291097, 0.00836146252605691, 0.008271742705705203, 0.008182930042235406, 0.008095016536185815, 0.008007994233933894, 0.0079218552279804, 0.007836591657218386, 0.007752195707187239, 0.007668659610311975, 0.007585975646127443, 0.007504136141489621, 0.007423133470771817, 0.007342960056047668, 0.007263608367260678, 0.007185070922381123, 0.007107340287548876, 0.0070304090772054855, 0.006954269954212058, 0.006878915629956498, 0.006804338864448361, 0.006730532466402153, 0.006657489293309486, 0.006585202251499917, 0.00651366429619165, 0.006442868431530661, 0.0063728077106206486, 0.0063034752355422465, 0.006234864157362298, 0.006166967676134226, 0.006099779040888137, 0.006033291549612335, 0.005967498549225989, 0.005902393435542954, 0.005837969653226762, 0.005774220695737856, 0.005711140105272964, 0.0056487214726958996, 0.005586958437460878, 0.005525844687529122, 0.005465373959277411, 0.005405540037400084, 0.005346336754803914, 0.005287757992496801, 0.005229797679469218, 0.005172449792570248, 0.005115708356376642, 0.005059567443057208, 0.005004021172229973, 0.004949063710815097, 0.004894689272881304, 0.004840892119488342, 0.004787666558522781, 0.004735006944530723, 0.004682907678544524, 0.00463136320790479, 0.004580368026079365, 0.004529916672476423, 0.004480003732254671, 0.004430623836128611, 0.004381771660170991, 0.004333441925610331, 0.004285629398626343, 0.004238328890140519, 0.004191535255604339, 0.004145243394784298, 0.004099448251543401, 0.004054144813619808, 0.0040093281124036, 0.003964993222709708, 0.003921135262548724, 0.003877749392895931, 0.0038348308174568596, 0.0037923747824314983, 0.0037503765762761376, 0.003708831529463288, 0.003667735014239367, 0.003627082444381404, 0.0035868692749509035, 0.0035470910020473836, 0.0035077431625592246, 0.0034688213339140357, 0.003430321133827251, 0.0033922382200496978, 0.0033545682901138622, 0.003317307081078892, 0.0032804503692753467, 0.0032439939700482593, 0.0032079337375000893, 0.0031722655642320544, 0.003136985381085973, 0.003102089156884297, 0.003067572898170701, 0.0030334326489491166, 0.002999664490423481, 0.0029662645407364445, 0.002933228954708266, 0.0029005539235747776, 0.002868235674726545, 0.002836270471446358, 0.002804654612647777, 0.0027733844326137307, 0.002742456300734566, 0.002711866621246729, 0.00268161183297145, 0.002651688409053677, 0.0026220928567015586, 0.0025928217169261898, 0.0025638715642810144];
var theoremEnvelope = times.map(() => 0.02);
var criticalCutoffDepths = ["2", "4", "6", "8"];
var criticalKAlpha05 = [
  1.1727735728230324,
  1.6451641432631638,
  1.7945486507244532,
  1.8417882109301968
];
var criticalKAlpha1 = [
  2.5760104874930456,
  5.576151606977197,
  8.57628190221513,
  11.576412196367531
];
var criticalKAlpha2 = [
  13.130063940849073,
  149.39623017105203,
  1511.8894951535653,
  15136.805284373851
];
var cuspRatioAlpha05 = [
  0.9413935628674814,
  0.9427948993201681,
  0.9428089001606945,
  0.9428090401678498
];
var cuspRatioAlpha1 = [
  0.9966666666666667,
  0.9999666666666667,
  0.9999996666666666,
  0.9999999966666666
];
var cuspRatioAlpha2 = [
  1.3233533333333334,
  1.3332333353333334,
  1.3333323333335334,
  1.3333333233333333
];
var twoBarrierHorizons = ["0", "0.25", "1", "4", "16", "64", "256"];
var twoBarrierRmsX0 = [
  0,
  39716783415984393e-20,
  0.002203031202009768,
  0.004179564524291642,
  0.010253539797496892,
  0.005207344790732692,
  0.00388407979942406
];
var twoBarrierRmsXPi2 = [
  0,
  0.00216515922418698,
  0.004378670881220735,
  0.003369637444526398,
  0.005127392329648042,
  0.001906952340139489,
  0.0015227722738745517
];
var twoBarrierRmsXPi = [
  0,
  588789955955046e-18,
  0.0017596396175536943,
  0.0023989368070094492,
  0.007902366711021114,
  0.0023401071601213273,
  0.004990921616023957
];
var reportPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/07-report.md";
var artifactAuditPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T14-artifact-summary.md";
var noncompactAuditPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T15-noncompact-quadratic-audit.md";
var relativeCostAuditPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T20-relative-cost-audit.md";
var summaryPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/numerics/summary_dynamic.json";
var criticalChecksPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/numerics/critical_frontier_checks.json";
var criticalAuditPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T25-critical-frontier-checks.md";
var twoBarrierFigurePath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/two-barrier-results-v2.png";
var twoBarrierDerivedPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/artifacts/two-barrier/audit-v1/derived_tables.json";
var twoBarrierAuditSummaryPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/artifacts/two-barrier/audit-v1/audit_summary.json";
var twoBarrierAuditPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T38-two-barrier-audit.md";
var twoBarrierImplementationPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T35-two-barrier-implementation.md";
var claimsPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/03-claims.md";
var d22Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/04o-unstable-phase-query-lower-bound.md";
var d23Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/04p-fixed-zero-query-lower-bound.md";
var d24Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/04q-matching-positive-query-complexity.md";
var d25Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/04r-signed-many-bump-complexity.md";
var d26Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/04s-general-reaction-query-complexity.md";
var t42Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/06g-query-information-lean.md";
var t43Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/06h-oracle-transcript-lean.md";
var t51Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/06i-positive-sigmoid-lean.md";
var t52Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/06j-positive-sample-mean-lean.md";
var t42t43RootPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T42-T43-root-correspondence.json";
var t51RootPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T51-root-correspondence.json";
var t52RootPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T52-root-correspondence.json";
var e3ResultPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/artifacts/query-information/checks-v1/check_result.json";
var e3ManifestPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/artifacts/query-information/checks-v1/execution_manifest.json";
var e3ReportPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T49-query-information-implementation.md";
var e3RootAuditPath = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T49-root-output-audit.json";
var d27Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/04t-matching-signed-query-complexity.md";
var t59Path = "/Users/michael/Desktop/NTU/fyp/parabolab/docs/research/runs/2026-09-28-dynamic-continuation/reviews/T59-signed-upper-independent-audit.md";
function DynamicContinuationEvidence() {
  const theme = useHostTheme();
  return /* @__PURE__ */ jsxs(
    Stack,
    {
      gap: 20,
      style: {
        minHeight: "100vh",
        maxWidth: 1180,
        margin: "0 auto",
        padding: 24,
        background: theme.bg.editor,
        color: theme.text.primary
      },
      children: [
        /* @__PURE__ */ jsxs(Stack, { gap: 8, children: [
          /* @__PURE__ */ jsxs(Row, { gap: 10, align: "center", wrap: true, children: [
            /* @__PURE__ */ jsx(Pill, { active: true, children: "\u72EC\u7ACB\u5BA1\u8BA1\u901A\u8FC7" }),
            /* @__PURE__ */ jsx(Pill, { size: "sm", children: "T \u2208 [0, 16] \xB7 201 \u4E2A\u65F6\u70B9" }),
            /* @__PURE__ */ jsx(Pill, { size: "sm", children: "D22\u2013D27 \xB7 \u7CBE\u786E\u70B9\u67E5\u8BE2\u590D\u6742\u5EA6" }),
            /* @__PURE__ */ jsx(Pill, { size: "sm", children: "Lean \xB7 T42 / T43 / T51 / T52" })
          ] }),
          /* @__PURE__ */ jsx(H1, { children: "\u52A8\u6001\u5EF6\u62D3\uFF1A\u8BC1\u636E\u3001\u57FA\u7EBF\u4E0E\u9002\u7528\u8303\u56F4" }),
          /* @__PURE__ */ jsx(Text, { tone: "secondary", children: "\u5DF2\u5BA1\u8BA1\u6570\u503C\u8BC1\u636E\u3001\u67E5\u8BE2\u590D\u6742\u5EA6\u7ED3\u8BBA\u4E0E\u5B9E\u9645\u5F62\u5F0F\u5316\u8986\u76D6\uFF1B\u6BCF\u4E00\u5C42\u7684\u91CF\u8BCD\u548C\u672A\u8986\u76D6\u6865\u63A5\u5747\u5355\u72EC\u6807\u660E\u3002" })
        ] }),
        /* @__PURE__ */ jsx(Callout, { tone: "warning", title: "\u5148\u8BFB\u8D1F\u9762\u7ED3\u679C", children: "\u56FA\u5B9A\u4E2D\u70B9 0.95g \u7684\u5168\u533A\u95F4\u6700\u5927\u8BEF\u5DEE\u5DF2\u662F 0.0109458\uFF0C\u4F4E\u4E8E 0.02 \u76EE\u6807\u3002\u5EF6\u62D3\u8DEF\u5F84\u867D\u7136\u66F4\u7CBE\u786E\uFF0C\u4F46\u8BE5\u76EE\u6807\u672C\u8EAB\u4E0D\u80FD\u8BC1\u660E\u76F8\u5BF9\u7B80\u5355\u57FA\u7EBF\u7684\u7ADE\u4E89\u4F18\u52BF\uFF1B\u5728\u8FD9\u4E2A\u5149\u6ED1\u4E00\u7EF4\u7B97\u4F8B\u4E0A\uFF0C \u6BCF\u6761 Monte Carlo \u8DEF\u5F84\u8017\u65F6\u662F\u4E00\u6B21\u4E25\u683C\u786E\u5B9A\u6027\u6C42\u89E3\u7684 26.6\u201327.7 \u500D\u3002" }),
        /* @__PURE__ */ jsxs(Grid, { columns: "minmax(0, 1.55fr) minmax(250px, 0.45fr)", gap: 18, align: "start", children: [
          /* @__PURE__ */ jsxs(Card, { size: "lg", children: [
            /* @__PURE__ */ jsx(CardHeader, { trailing: "201 / 201", children: "\u5F52\u4E00\u5316\u7A7A\u95F4 L\xB2 \u8BEF\u5DEE\u968F\u7EC8\u70B9 T \u53D8\u5316" }),
            /* @__PURE__ */ jsx(CardBody, { children: /* @__PURE__ */ jsxs(Stack, { gap: 8, children: [
              /* @__PURE__ */ jsx(Text, { size: "small", tone: "tertiary", children: "\u7EB5\u8F74\uFF1A\u5F52\u4E00\u5316\u7A7A\u95F4 L\xB2 \u8BEF\u5DEE" }),
              /* @__PURE__ */ jsx(
                LineChart,
                {
                  categories: times.map((value) => value.toFixed(2)),
                  series: [
                    {
                      name: "3 \u79CD\u5B50\u7ECF\u9A8C RMS",
                      data: empiricalRms,
                      tone: "info"
                    },
                    {
                      name: "\u56FA\u5B9A 0.95g",
                      data: midpoint095g,
                      tone: "success"
                    },
                    {
                      name: "\u56FA\u5B9A g",
                      data: equilibriumG,
                      tone: "warning"
                    },
                    {
                      name: "\u7406\u8BBA\u5305\u7EDC 0.02\uFF08\u9010\u7EC8\u70B9\u603B\u4F53\uFF09",
                      data: theoremEnvelope,
                      tone: "danger"
                    }
                  ],
                  height: 360,
                  yMin: 0,
                  yMax: 0.023,
                  showHoverGuide: true
                }
              ),
              /* @__PURE__ */ jsx(
                Text,
                {
                  size: "small",
                  tone: "tertiary",
                  style: { textAlign: "center" },
                  children: "\u6A2A\u8F74\uFF1A\u7EC8\u70B9 T"
                }
              ),
              /* @__PURE__ */ jsxs(Text, { size: "small", tone: "tertiary", children: [
                "\u6765\u6E90\uFF1A",
                /* @__PURE__ */ jsx(Link, { href: summaryPath, children: "summary_dynamic.json" }),
                "\uFF0C\u5B8C\u6574 201 \u65F6\u70B9\uFF082026-09-28\uFF09\u3002\u4E09\u79CD\u5B50 RMS \u4EC5\u4F5C\u63CF\u8FF0\uFF0C\u65E0\u7F6E\u4FE1\u533A\u95F4\uFF1B 0.02 \u662F\u9010\u7EC8\u70B9\u7684\u603B\u4F53\u5F52\u4E00\u5316\u7A7A\u95F4 RMS \u5B9A\u7406\u5305\u7EDC\uFF0C\u4E0D\u662F\u6574\u6761\u8DEF\u5F84\u7684\u540C\u65F6\u6982\u7387\u4FDD\u8BC1\u3002"
              ] })
            ] }) })
          ] }),
          /* @__PURE__ */ jsxs(Stack, { gap: 12, children: [
            /* @__PURE__ */ jsx(H2, { children: "\u89C4\u6A21\u4E0E\u7EC8\u70B9" }),
            /* @__PURE__ */ jsxs(Grid, { columns: 2, gap: 12, children: [
              /* @__PURE__ */ jsx(Stat, { value: "60M", label: "\u603B\u6839\u6570" }),
              /* @__PURE__ */ jsx(Stat, { value: "70,801,171", label: "\u8BBF\u95EE\u8282\u70B9" }),
              /* @__PURE__ */ jsx(Stat, { value: "201", label: "\u7EC8\u70B9\u6570\uFF08\u542B T=0\uFF09" }),
              /* @__PURE__ */ jsx(Stat, { value: "0.00353962", label: "T=16 \u7ECF\u9A8C RMS", tone: "success" })
            ] }),
            /* @__PURE__ */ jsxs(Callout, { tone: "neutral", title: "\u6BD4\u8F83\u951A\u70B9", children: [
              /* @__PURE__ */ jsx(Text, { size: "small", children: "0.95g \u5168\u533A\u95F4\u6700\u5927\u503C\uFF1A0.0109458" }),
              /* @__PURE__ */ jsx(Text, { size: "small", children: "\u6700\u5927\u4E09\u79CD\u5B50\u7ECF\u9A8C RMS\uFF1A0.00468048\uFF08T=12.72\uFF09" }),
              /* @__PURE__ */ jsx(Text, { size: "small", children: "\u7ED3\u8BBA\uFF1A\u8BEF\u5DEE\u76EE\u6807\u5DF2\u88AB\u7B80\u5355\u56FA\u5B9A\u4E2D\u70B9\u6EE1\u8DB3\uFF0C\u786E\u5B9A\u6027\u8C31\u6CD5\u4E5F\u66F4\u5FEB\u3002" })
            ] })
          ] })
        ] }),
        /* @__PURE__ */ jsxs(Stack, { gap: 12, children: [
          /* @__PURE__ */ jsxs(Row, { justify: "space-between", align: "end", gap: 16, wrap: true, children: [
            /* @__PURE__ */ jsxs(Stack, { gap: 4, children: [
              /* @__PURE__ */ jsx(H2, { children: "\u4E34\u754C\u7AEF\u70B9\u524D\u6CBF \xB7 p = 2" }),
              /* @__PURE__ */ jsxs(Text, { tone: "secondary", children: [
                "\u56FA\u5B9A \u03B1 \u2208 ",
                "{0.5, 1, 2}",
                "\uFF0C\u6BD4\u8F83 \u03B4 = 10\u207B\xB2\u300110\u207B\u2074\u300110\u207B\u2076\u300110\u207B\u2078 \u4E0B\u7684\u622A\u65AD\u7AEF\u70B9\u8D21\u732E\u4E0E\u5C16\u70B9\u6BD4\u503C\u3002"
              ] })
            ] }),
            /* @__PURE__ */ jsxs(Row, { gap: 8, wrap: true, children: [
              /* @__PURE__ */ jsx(Pill, { active: true, children: "54 / 54 \u7CBE\u786E\u68C0\u67E5\u901A\u8FC7" }),
              /* @__PURE__ */ jsx(Pill, { size: "sm", children: "80 \u4F4D\u5341\u8FDB\u5236\u7CBE\u5EA6" })
            ] })
          ] }),
          /* @__PURE__ */ jsxs(Grid, { columns: 4, gap: 12, children: [
            /* @__PURE__ */ jsx(Stat, { value: "54 / 54", label: "\u7CBE\u786E\u6052\u7B49\u5F0F\u68C0\u67E5", tone: "success" }),
            /* @__PURE__ */ jsx(Stat, { value: "1.0542\xD710\u207B\u2078\xB9", label: "\u6700\u5927\u6052\u7B49\u5F0F\u6B8B\u5DEE", tone: "success" }),
            /* @__PURE__ */ jsx(Stat, { value: "2.87546 s", label: "\u56FA\u5B9A\u534F\u8BAE\u8FD0\u884C\u65F6\u95F4" }),
            /* @__PURE__ */ jsx(Stat, { value: "12 / 12", label: "K \u6B63\u503C\u4E14\u968F\u622A\u65AD\u6DF1\u5EA6\u5355\u8C03", tone: "success" })
          ] }),
          /* @__PURE__ */ jsxs(Grid, { columns: "1fr 1fr", gap: 14, children: [
            /* @__PURE__ */ jsxs(Card, { children: [
              /* @__PURE__ */ jsx(CardHeader, { trailing: "\u03B4 = 10\u207B\xB2\u202610\u207B\u2078", children: "\u622A\u65AD\u7AEF\u70B9\u8D21\u732E K(\u03B4)" }),
              /* @__PURE__ */ jsx(CardBody, { children: /* @__PURE__ */ jsxs(Stack, { gap: 8, children: [
                /* @__PURE__ */ jsx(Text, { size: "small", tone: "secondary", children: "\u7EB5\u8F74\uFF1Alog\u2081\u2080 K(\u03B4)\uFF1B\u6570\u503C\u53D8\u6362\u4EC5\u7528\u4E8E\u540C\u65F6\u663E\u793A\u6709\u9650\u3001\u5BF9\u6570\u4E0E\u5E42\u5F8B\u589E\u957F\u3002" }),
                /* @__PURE__ */ jsx(
                  LineChart,
                  {
                    categories: criticalCutoffDepths,
                    series: [
                      {
                        name: "\u03B1=0.5 \xB7 \u7406\u8BBA\uFF1A\u6709\u9650\u6781\u9650",
                        data: criticalKAlpha05.map(Math.log10),
                        tone: "info"
                      },
                      {
                        name: "\u03B1=1 \xB7 \u7406\u8BBA\uFF1A\u5BF9\u6570\u53D1\u6563",
                        data: criticalKAlpha1.map(Math.log10),
                        tone: "warning"
                      },
                      {
                        name: "\u03B1=2 \xB7 \u7406\u8BBA\uFF1A\u5E42\u5F8B\u53D1\u6563",
                        data: criticalKAlpha2.map(Math.log10),
                        tone: "danger"
                      }
                    ],
                    height: 250,
                    beginAtZero: false,
                    showHoverGuide: true
                  }
                ),
                /* @__PURE__ */ jsx(Text, { size: "small", tone: "secondary", style: { textAlign: "center" }, children: "\u6A2A\u8F74\uFF1Alog\u2081\u2080(1/\u03B4) [\u65E0\u91CF\u7EB2]" })
              ] }) })
            ] }),
            /* @__PURE__ */ jsxs(Card, { children: [
              /* @__PURE__ */ jsx(CardHeader, { trailing: "\u7406\u8BBA\u6781\u9650\u4F5C\u53C2\u8003\u7EBF", children: "\u5C16\u70B9\u6BD4\u503C" }),
              /* @__PURE__ */ jsx(CardBody, { children: /* @__PURE__ */ jsxs(Stack, { gap: 8, children: [
                /* @__PURE__ */ jsx(Text, { size: "small", tone: "secondary", children: "\u7EB5\u8F74\uFF1A\u65E0\u91CF\u7EB2\u6BD4\u503C\uFF1B\u6BCF\u6761\u66F2\u7EBF\u5BF9\u5E94\u540C\u4E00\u7EC4\u56DB\u4E2A\u622A\u65AD\u6DF1\u5EA6\u3002" }),
                /* @__PURE__ */ jsx(
                  LineChart,
                  {
                    categories: criticalCutoffDepths,
                    series: [
                      { name: "\u03B1=0.5", data: cuspRatioAlpha05, tone: "info" },
                      { name: "\u03B1=1", data: cuspRatioAlpha1, tone: "warning" },
                      { name: "\u03B1=2", data: cuspRatioAlpha2, tone: "danger" }
                    ],
                    referenceLines: [
                      { value: 0.9428090415820634, label: "\u03B1=0.5 \u6781\u9650", tone: "info" },
                      { value: 1, label: "\u03B1=1 \u6781\u9650", tone: "warning" },
                      { value: 1.3333333333333333, label: "\u03B1=2 \u6781\u9650", tone: "danger" }
                    ],
                    height: 250,
                    yMin: 0.92,
                    yMax: 1.35,
                    beginAtZero: false,
                    showHoverGuide: true
                  }
                ),
                /* @__PURE__ */ jsx(Text, { size: "small", tone: "secondary", style: { textAlign: "center" }, children: "\u6A2A\u8F74\uFF1Alog\u2081\u2080(1/\u03B4) [\u65E0\u91CF\u7EB2]" })
              ] }) })
            ] })
          ] }),
          /* @__PURE__ */ jsxs(Grid, { columns: "1fr 1fr", gap: 14, children: [
            /* @__PURE__ */ jsxs(Stack, { gap: 6, children: [
              /* @__PURE__ */ jsx(Text, { weight: "semibold", children: "K(\u03B4) \u539F\u59CB\u9AD8\u7CBE\u5EA6\u503C" }),
              /* @__PURE__ */ jsx(
                Table,
                {
                  headers: ["\u03B1", "\u03B4=10\u207B\xB2", "\u03B4=10\u207B\u2074", "\u03B4=10\u207B\u2076", "\u03B4=10\u207B\u2078"],
                  rows: [
                    ["0.5", "1.1727735728230323", "1.6451641432631638", "1.7945486507244532", "1.8417882109301969"],
                    ["1", "2.5760104874930458", "5.5761516069771972", "8.5762819022151310", "11.576412196367531"],
                    ["2", "13.130063940849073", "149.39623017105203", "1511.8894951535653", "15136.805284373852"]
                  ],
                  columnAlign: ["left", "right", "right", "right", "right"],
                  striped: true,
                  framed: true
                }
              )
            ] }),
            /* @__PURE__ */ jsxs(Stack, { gap: 6, children: [
              /* @__PURE__ */ jsx(Text, { weight: "semibold", children: "\u5C16\u70B9\u6BD4\u503C\u4E0E\u7406\u8BBA\u6781\u9650" }),
              /* @__PURE__ */ jsx(
                Table,
                {
                  headers: ["\u03B1", "\u03B4=10\u207B\xB2", "\u03B4=10\u207B\u2074", "\u03B4=10\u207B\u2076", "\u03B4=10\u207B\u2078", "\u7406\u8BBA\u6781\u9650"],
                  rows: [
                    ["0.5", "0.9413935628674814", "0.9427948993201681", "0.9428089001606945", "0.9428090401678498", "0.9428090415820634"],
                    ["1", "0.9966666666666667", "0.9999666666666667", "0.9999996666666666", "0.9999999966666666", "1"],
                    ["2", "1.3233533333333333", "1.3332333353333334", "1.3333323333335333", "1.3333333233333334", "1.3333333333333333"]
                  ],
                  columnAlign: ["left", "right", "right", "right", "right", "right"],
                  striped: true,
                  framed: true
                }
              )
            ] })
          ] }),
          /* @__PURE__ */ jsx(Callout, { tone: "warning", title: "\u89E3\u91CA\u8FB9\u754C", children: /* @__PURE__ */ jsx(Text, { size: "small", children: "K(\u03B4) \u662F\u622A\u65AD\u7AEF\u70B9\u8D21\u732E\uFF0C\u4E0D\u662F\u5B8C\u6574 S\u2082\u3002\u56DB\u4E2A\u622A\u65AD\u70B9\u53EA\u7528\u4E8E\u6838\u5BF9\u7406\u8BBA\u9884\u8A00\u7684\u6570\u503C\u5F62\u6001\uFF1B\u6536\u655B\u6216\u53D1\u6563\u6765\u81EA\u5DF2\u5BA1\u67E5\u7684\u7406\u8BBA\u8BBA\u8BC1\uFF0C\u4E0D\u80FD\u7531\u8FD9\u56DB\u4E2A\u70B9\u8BC1\u660E\u3002" }) }),
          /* @__PURE__ */ jsxs(Text, { size: "small", tone: "secondary", children: [
            "\u6765\u6E90\uFF1A\u56FA\u5B9A T25 \u534F\u8BAE\u8F93\u51FA ",
            /* @__PURE__ */ jsx(Link, { href: criticalChecksPath, children: "critical_frontier_checks.json" }),
            "\uFF1B\u89E3\u91CA\u4E0E\u590D\u6838\u89C1 ",
            /* @__PURE__ */ jsx(Link, { href: criticalAuditPath, children: "T25 \u5BA1\u8BA1" }),
            "\u3002"
          ] })
        ] }),
        /* @__PURE__ */ jsxs(Stack, { gap: 12, children: [
          /* @__PURE__ */ jsxs(Row, { justify: "space-between", align: "end", gap: 16, wrap: true, children: [
            /* @__PURE__ */ jsxs(Stack, { gap: 4, children: [
              /* @__PURE__ */ jsx(H2, { children: "E2 \xB7 \u53CC\u79FB\u52A8\u5C4F\u969C\u7684\u6709\u9650\u8BC1\u636E" }),
              /* @__PURE__ */ jsx(Text, { tone: "secondary", children: "\u56FA\u5B9A\u4E00\u7EF4 2\u03C0 \u5468\u671F\u6570\u636E v(x)=5/8+(1/8)cos(x)\uFF1B63 \u4E2A\u5355\u5143\u3001630,000 \u4E2A\u4E3B\u5B9E\u9A8C\u6839\uFF0C\u6BCF\u5355\u5143 N=10,000\uFF0C\u56FA\u5B9A\u7EC8\u70B9 T\u2264256\u3002" })
            ] }),
            /* @__PURE__ */ jsxs(Row, { gap: 8, wrap: true, children: [
              /* @__PURE__ */ jsx(Pill, { active: true, children: "T38 \u72EC\u7ACB\u5BA1\u8BA1 992 / 992" }),
              /* @__PURE__ */ jsx(Pill, { size: "sm", children: "dtype \u8865\u5145\u68C0\u67E5\u901A\u8FC7" })
            ] })
          ] }),
          /* @__PURE__ */ jsxs(Grid, { columns: 4, gap: 12, children: [
            /* @__PURE__ */ jsx(Stat, { value: "630,000", label: "\u4E3B\u5B9E\u9A8C\u6839" }),
            /* @__PURE__ */ jsx(Stat, { value: "63", label: "\u56FA\u5B9A\u5355\u5143" }),
            /* @__PURE__ */ jsx(Stat, { value: "10,000", label: "\u6BCF\u5355\u5143\u6839\u6570" }),
            /* @__PURE__ */ jsx(Stat, { value: "256", label: "\u6700\u5927\u6709\u9650\u7EC8\u70B9 T" })
          ] }),
          /* @__PURE__ */ jsxs(Card, { size: "lg", children: [
            /* @__PURE__ */ jsx(CardHeader, { trailing: "3 \u4E2A\u67E5\u8BE2\u70B9 \xD7 7 \u4E2A\u7EC8\u70B9", children: "\u4E09\u79CD\u5B50\u76F8\u5BF9\u8BEF\u5DEE RMS" }),
            /* @__PURE__ */ jsx(CardBody, { children: /* @__PURE__ */ jsxs(Stack, { gap: 8, children: [
              /* @__PURE__ */ jsx(Text, { size: "small", tone: "secondary", children: "\u7EB5\u8F74\uFF1A\u76F8\u5BF9 RMS [%]\uFF1B1% \u7EBF\u662F\u7406\u60F3\u91CD\u590D\u96C6\u5408\u7684\u53C2\u8003\u76EE\u6807\uFF0C\u4E0D\u662F\u6BCF\u4E2A\u6709\u9650\u5B9E\u73B0\u7684\u9A8C\u6536\u4E0A\u754C\u3002" }),
              /* @__PURE__ */ jsx(
                LineChart,
                {
                  categories: twoBarrierHorizons,
                  series: [
                    { name: "x=0", data: twoBarrierRmsX0.map((value) => 100 * value), tone: "info" },
                    { name: "x=\u03C0/2", data: twoBarrierRmsXPi2.map((value) => 100 * value), tone: "success" },
                    { name: "x=\u03C0", data: twoBarrierRmsXPi.map((value) => 100 * value), tone: "warning" }
                  ],
                  referenceLines: [{ value: 1, label: "1% \u7406\u60F3\u96C6\u5408 RMS \u53C2\u7167", tone: "danger" }],
                  height: 270,
                  beginAtZero: true,
                  yMax: 1.1,
                  valueSuffix: "%",
                  showHoverGuide: true
                }
              ),
              /* @__PURE__ */ jsx(Text, { size: "small", tone: "secondary", style: { textAlign: "center" }, children: "\u6A2A\u8F74\uFF1A\u4E03\u4E2A\u56FA\u5B9A\u7EC8\u70B9 T\uFF08\u5206\u7C7B\u8F74\uFF0C\u4E0D\u8868\u793A\u7B49\u6BD4\u4F8B\u65F6\u95F4\u95F4\u9694\uFF09" })
            ] }) })
          ] }),
          /* @__PURE__ */ jsxs(Stack, { gap: 6, children: [
            /* @__PURE__ */ jsx(Text, { weight: "semibold", children: "\u5168\u90E8 21 \u4E2A\u67E5\u8BE2 RMS" }),
            /* @__PURE__ */ jsx(
              Table,
              {
                headers: ["\u67E5\u8BE2\u70B9", "T=0", "T=0.25", "T=1", "T=4", "T=16", "T=64", "T=256"],
                rows: [
                  ["x=0", ...twoBarrierRmsX0.map((value) => `${(100 * value).toFixed(6)}%`)],
                  ["x=\u03C0/2", ...twoBarrierRmsXPi2.map((value) => `${(100 * value).toFixed(6)}%`)],
                  ["x=\u03C0", ...twoBarrierRmsXPi.map((value) => `${(100 * value).toFixed(6)}%`)]
                ],
                columnAlign: ["left", "right", "right", "right", "right", "right", "right", "right"],
                striped: true,
                framed: true
              }
            )
          ] }),
          /* @__PURE__ */ jsx(Callout, { tone: "warning", title: "\u6709\u9650\u6837\u672C\u7ED3\u8BBA", children: /* @__PURE__ */ jsx(Text, { size: "small", children: "\u6700\u5927 RMS \u4E3A 1.02535%\uFF0C\u51FA\u73B0\u5728 T=16\u3001x=0\uFF1B\u56E0\u6B64\u4E0D\u80FD\u5199\u6210\u201C\u6240\u6709\u70B9\u90FD\u4F4E\u4E8E 1%\u201D\u3002\u8FD9\u662F\u4E09\u79CD\u5B50\u6709\u9650\u5B9E\u73B0\u7684\u8BCA\u65AD\u503C\uFF0C\u4E0D\u8FDD\u53CD\u7406\u60F3\u91CD\u590D\u96C6\u5408\u7684 RMS \u754C\u3002" }) }),
          /* @__PURE__ */ jsxs(Grid, { columns: "1fr 1fr", gap: 14, children: [
            /* @__PURE__ */ jsxs(Stack, { gap: 6, children: [
              /* @__PURE__ */ jsx(Text, { weight: "semibold", children: "\u56FA\u5B9A\u8BA1\u65F6\u8303\u56F4" }),
              /* @__PURE__ */ jsx(
                Table,
                {
                  headers: ["\u4EFB\u52A1", "\u8017\u65F6"],
                  rows: [
                    ["\u79CD\u5B50 2026092831 \xB7 21 \u67E5\u8BE2\u91C7\u6837", "2.12709 s"],
                    ["\u79CD\u5B50 2026092832 \xB7 21 \u67E5\u8BE2\u91C7\u6837", "1.89072 s"],
                    ["\u79CD\u5B50 2026092833 \xB7 21 \u67E5\u8BE2\u91C7\u6837", "1.76424 s"],
                    ["\u56FA\u5B9A 16 \u6A21\u5F0F \xB7 \u4E00\u6B21\u6C42\u89E3 + 21 \u67E5\u8BE2", "0.0969848 s"],
                    ["\u516D\u6B21\u53C2\u8003\u7EC6\u5316 \xB7 \u6C42\u89E3 + \u67E5\u8BE2\u5408\u8BA1", "2.12111 s"]
                  ],
                  columnAlign: ["left", "right"],
                  striped: true,
                  framed: true
                }
              ),
              /* @__PURE__ */ jsx(Text, { size: "small", tone: "tertiary", children: "16 \u6A21\u5F0F\u6BD4\u8F83\u65F6\u95F4\u4E0D\u542B\u57FA\u51FD\u6570\u4E0E\u7CFB\u7EDF\u6784\u9020\uFF1B\u516D\u6B21\u7EC6\u5316\u9A8C\u8BC1\u6210\u672C\u5355\u5217\u3002\u8FD9\u91CC\u53EA\u62A5\u544A\u56FA\u5B9A\u5B9E\u73B0\u7684\u6D4B\u91CF\uFF0C\u4E0D\u4F5C\u7B49\u7CBE\u5EA6\u4F18\u5316\u6216\u52A0\u901F\u7ED3\u8BBA\u3002" })
            ] }),
            /* @__PURE__ */ jsxs(Stack, { gap: 6, children: [
              /* @__PURE__ */ jsx(Text, { weight: "semibold", children: "T=256 \u7684\u8BEF\u5DEE\u5BF9\u7167" }),
              /* @__PURE__ */ jsx(
                Table,
                {
                  headers: ["\u91CF", "x=0", "x=\u03C0/2", "x=\u03C0"],
                  rows: [
                    ["\u4E09\u79CD\u5B50 RMS", "0.3884%", "0.1523%", "0.4991%"],
                    ["\u8C03\u548C\u4E2D\u5FC3 \xB7 \u7EDD\u5BF9\u76F8\u5BF9\u8BEF\u5DEE", "24.8573%", "24.8573%", "24.8573%"],
                    ["\u7A7A\u95F4\u5747\u503C ODE \xB7 \u7EDD\u5BF9\u76F8\u5BF9\u8BEF\u5DEE", "5.1055%", "5.1055%", "5.1055%"]
                  ],
                  columnAlign: ["left", "right", "right", "right"],
                  striped: true,
                  framed: true
                }
              )
            ] })
          ] }),
          /* @__PURE__ */ jsx(Callout, { tone: "neutral", title: "\u5DE5\u4F5C\u91CF\u8BC1\u636E\u7684\u8FB9\u754C", children: /* @__PURE__ */ jsx(Text, { size: "small", children: "\u7406\u8BBA\u91CF E[N]\u22642.82733 \u4E0E E[\u63D0\u6848\u6570]\u22645.30124 \u662F\u671F\u671B\u4E0A\u754C\uFF0C\u4E0D\u662F\u5355\u6839\u6216\u6709\u9650\u6837\u672C\u4E0A\u754C\u3002\u6700\u5927\u5355\u5143\u7ECF\u9A8C\u5E73\u5747\u8282\u70B9\u6570\u4E3A 2.8354\uFF1B\u8FD9\u79CD\u6709\u9650\u6CE2\u52A8\u4E0D\u662F\u7406\u8BBA\u8FDD\u4F8B\uFF0C\u7ECF\u9A8C\u66F2\u7EBF\u4E5F\u4E0D\u80FD\u8BC1\u660E\u671F\u671B\u754C\u3002" }) }),
          /* @__PURE__ */ jsxs(Text, { size: "small", tone: "secondary", children: [
            "\u6765\u6E90\uFF1A",
            /* @__PURE__ */ jsx(Link, { href: twoBarrierDerivedPath, children: "\u5BA1\u8BA1\u6D3E\u751F\u8868" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: twoBarrierAuditSummaryPath, children: "992 / 992 \u539F\u59CB\u8BC1\u636E\u5BA1\u8BA1" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: twoBarrierAuditPath, children: "T38 \u5BA1\u8BA1\u62A5\u544A" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: twoBarrierImplementationPath, children: "T35 \u5B9E\u73B0\u62A5\u544A" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: twoBarrierFigurePath, children: "v2 \u79D1\u5B66\u56FE" }),
            "\u3002"
          ] })
        ] }),
        /* @__PURE__ */ jsxs(Stack, { gap: 12, children: [
          /* @__PURE__ */ jsxs(Row, { justify: "space-between", align: "end", gap: 16, wrap: true, children: [
            /* @__PURE__ */ jsxs(Stack, { gap: 4, children: [
              /* @__PURE__ */ jsx(H2, { children: "D22\u2013D27 \xB7 \u7CBE\u786E\u70B9\u67E5\u8BE2\u590D\u6742\u5EA6\u5730\u56FE" }),
              /* @__PURE__ */ jsx(Text, { tone: "secondary", children: "\u56FA\u5B9A\u7EF4\u6570 d\u3001\u5149\u6ED1\u9636\u6570 s \u4E0E\u56FA\u5B9A\u7EDD\u5BF9\u7CBE\u5EA6\uFF1B\u4E0B\u8868\u4E2D\u7684\u6307\u6570\u662F\u968F\u5927\u7EC8\u70B9 T \u7684\u67E5\u8BE2\u9636\u3002" })
            ] }),
            /* @__PURE__ */ jsx(Pill, { active: true, children: "\u5E38\u89C4\u8BC1\u660E + \u72EC\u7ACB\u5BA1\u67E5" })
          ] }),
          /* @__PURE__ */ jsxs(Card, { size: "lg", children: [
            /* @__PURE__ */ jsx(CardHeader, { trailing: "\u4E0D\u540C\u8F93\u5165\u7C7B\u4E0E\u4E0D\u540C\u91CF\u8BCD\u4E0D\u53EF\u6DF7\u7528", children: "\u6B63\u7C7B\u3001\u53D8\u53F7\u7C7B\u4E0E\u4E00\u822C\u53CD\u5E94" }),
            /* @__PURE__ */ jsx(CardBody, { children: /* @__PURE__ */ jsx(
              Table,
              {
                headers: ["\u7ED3\u8BBA", "\u8F93\u5165\u7C7B / \u7CBE\u5EA6", "\u5DF2\u5EFA\u7ACB\u7684\u67E5\u8BE2\u9636", "\u91CF\u8BCD\u4E0E\u4FDD\u7559\u8FB9\u754C"],
                rows: [
                  [
                    "D22 \xB7 \u53D8\u53F7\u4E0B\u754C",
                    "Allen\u2013Cahn\uFF1B\u56FA\u5B9A\u53D8\u53F7 C\u02E2 \u7C7B\uFF1BMSE\u22641/16",
                    "\u03A9(exp(dT/(s+d)))",
                    "\u6BCF\u4E2A T \u6709\u663E\u5F0F\u57FA\u7EBF g_T\uFF1B\u57FA\u7EBF\u968F T \u53D8\u3002\u7B97\u6CD5\u53EF\u4F9D\u8D56 T\u3001\u53EF\u81EA\u9002\u5E94\u3001\u53EF\u6709\u504F\uFF1B\u672A\u58F0\u79F0\u6700\u4F18\u6307\u6570\u3002"
                  ],
                  [
                    "D23 \xB7 \u975E\u8D1F\u7C7B\u96F6\u57FA\u7EBF\u4E0B\u754C",
                    "Allen\u2013Cahn\uFF1B\u56FA\u5B9A\u975E\u8D1F C\u02E2 \u7C7B\uFF1BRMS\u22641/4",
                    "\u03A9(exp(dT/(s+d)))",
                    "\u6602\u8D35\u8F93\u5165\u662F\u540C\u4E00\u4E2A\u96F6\u51FD\u6570\uFF1B\u9690\u85CF\u66FF\u4EE3\u968F T \u53D8\u3002\u82E5\u8F93\u5165\u4EE5\u5DF2\u77E5\u96F6\u516C\u5F0F\u7ED9\u51FA\uFF0C\u5219\u4E0D\u9002\u7528\u3002"
                  ],
                  [
                    "D24 \xB7 \u975E\u8D1F\u7C7B\u5339\u914D\u9636",
                    "\u4E0E D23 \u5B8C\u5168\u76F8\u540C\u7684\u7C7B\uFF1B\u56FA\u5B9A d,s \u4E0E\u56FA\u5B9A RMS\u22641/4",
                    "\u0398(exp(dT/(s+d)))",
                    "\u6BCF\u4E2A\u5145\u5206\u5927 T\uFF1B\u4E0A\u754C\u7528\u72EC\u7ACB\u5747\u5300\u70B9\u6837\u672C\u4E0E\u6709\u504F \u03A8(exp(T)m\u0302)\uFF0C\u7EDF\u4E00 RMS\u22645/32\u3002"
                  ],
                  [
                    "D25 \xB7 \u53D8\u53F7\u5F3A\u5316\u4E0B\u754C",
                    "\u4E0E D22 \u76F8\u540C\u7684\u7C7B\uFF1B1\u2264d\u22644s\uFF1BRMS\u22641/4",
                    "\u03A9(exp(2dT/(2s+d)))",
                    "\u6709\u9650\u5148\u9A8C\u7ED9\u6700\u574F\u8F93\u5165\uFF1B\u6602\u8D35\u6210\u5458\u53EF\u4F9D\u8D56 T \u548C\u7B97\u6CD5\u3002D27\u73B0\u5DF2\u5339\u914D\u4E0A\u754C\uFF1Bd>4s\u5C1A\u672A\u5217\u4E3A\u5DF2\u8BC1\u7ED3\u8BBA\u3002"
                  ],
                  [
                    "D26 \xB7 \u4E00\u822C C\xB2 \u6B63\u7C7B",
                    "0\u2264v\u2264b/2\u3001C\u02E2 \u8303\u6570\u2264R\uFF0CR>0\uFF1B\u56FA\u5B9A \u03B5\u2208(0,b/2)",
                    "\u0398(exp(\u03BBdT/(s+d)))",
                    "\u6BCF\u4E2A\u7EC8\u70B9\u53EF\u7528\u4F9D\u8D56\u516C\u5F00 f\u3001\u53C2\u6570\u4E0E T \u7684\u6709\u9650\u53C2\u6570\uFF1B\u4E0D\u4F9D\u8D56\u672A\u77E5 v\u3002\u53EA\u8BC1\u660E\u975E\u7EDF\u4E00\u7684\u9010\u7EC8\u70B9\u67E5\u8BE2\u590D\u6742\u5EA6\u3002\u4E00\u822C C\xB2 \u5C42\u5C1A\u672A Lean \u5F62\u5F0F\u5316\u3002"
                  ],
                  [
                    "D27 \xB7 \u53D8\u53F7\u7C7B\u5339\u914D\u9636",
                    "\u4E0E D25 \u5B8C\u5168\u76F8\u540C\u7684\u7C7B\uFF1B1\u2264d\u22644s\uFF1BRMS\u22641/4",
                    "\u0398(exp(2dT/(2s+d)))",
                    "\u7C97\u7F51\u683C\u63D2\u503C\u4E0E\u7EBF\u6027/\u4E8C\u6B21\u968F\u673A\u4FEE\u6B63\u4F30\u8BA1\u975E\u7EBF\u6027\u76F8\u4F4D\u3002\u67E5\u8BE2\u6570\u6709\u786E\u5B9A\u4E0A\u9650\uFF1B\u5DF2\u4ED8\u8D39\u6837\u672C\u540E\u7684\u6709\u9650\u8F85\u52A9\u8BA1\u7B97\u53EF\u80FD\u6781\u5927\uFF0C\u6CA1\u6709\u8FD0\u884C\u65F6\u95F4\u4E0A\u754C\u3002"
                  ]
                ],
                columnAlign: ["left", "left", "left", "left"],
                striped: true,
                framed: true
              }
            ) })
          ] }),
          /* @__PURE__ */ jsxs(Grid, { columns: "1fr 1fr", gap: 14, children: [
            /* @__PURE__ */ jsx(Callout, { tone: "neutral", title: "\u8FDC\u79BB\u4E0D\u7A33\u5B9A\u96F6\u76F8\u65F6\u53EF\u6709\u7EDF\u4E00\u5DE5\u4F5C\u91CF", children: /* @__PURE__ */ jsxs(Text, { size: "small", children: [
              "D17\u2013D19 \u5728",
              "0 < m \u2264 v \u2264 M < 1",
              "\u3001m\u4E0EM\u56FA\u5B9A\u7B49\u76F8\u5E94\u6761\u4EF6\u4E0B\uFF0C\u7ED9\u51FA\u7406\u60F3\u6811\u8868\u793A\u5BF9\u7EC8\u70B9T\u4E00\u81F4\u7684\u671F\u671B\u8282\u70B9\u754C\u3002 D22\u2013D27 \u5141\u8BB8\u6570\u636E\u903C\u8FD1\u4E0D\u7A33\u5B9A\u96F6\u76F8\u6216\u8003\u5BDF\u5B8C\u6574\u56FA\u5B9A\u975E\u8D1F\u7C7B\uFF0C\u91CF\u8BCD\u548C\u4FE1\u606F\u6A21\u578B\u4E0D\u540C\uFF0C\u56E0\u6B64\u5E76\u4E0D\u77DB\u76FE\u3002"
            ] }) }),
            /* @__PURE__ */ jsx(Callout, { tone: "warning", title: "\u57FA\u7EBF\u91CF\u8BCD\u5FC5\u987B\u533A\u5206", children: /* @__PURE__ */ jsx(Text, { size: "small", children: "D22 \u7684\u516C\u5F00\u57FA\u7EBF g_T \u968F T \u53D8\u5316\uFF1BD23 \u5728\u6240\u6709\u7EC8\u70B9\u4F7F\u7528\u540C\u4E00\u4E2A\u96F6\u8F93\u5165\uFF1BD25 \u53EA\u4FDD\u8BC1\u6709\u9650\u5148\u9A8C\u5E73\u5747\u6602\u8D35\uFF0C \u5177\u4F53\u6602\u8D35\u6210\u5458\u53EF\u968F T \u548C\u7B97\u6CD5\u53D8\u5316\u3002D23 \u7684\u56FA\u5B9A\u96F6\u8F93\u5165\u7ED3\u8BBA\u4F9D\u8D56\u6574\u4E2A\u975E\u8D1F\u7C7B\u7684\u7EDF\u4E00\u7CBE\u5EA6\u8981\u6C42\uFF0C\u4E0D\u80FD\u636E\u6B64\u65AD\u8A00\u6BCF\u4E2A\u56FA\u5B9A\u5256\u9762\u90FD\u540C\u6837\u56F0\u96BE\u3002" }) })
          ] }),
          /* @__PURE__ */ jsxs(Callout, { tone: "warning", title: "\u4FE1\u606F\u6A21\u578B\u8303\u56F4", children: [
            "\u8FD9\u4E9B\u7ED3\u8BBA\u8BA1\u6570\u7684\u662F\u672A\u77E5\u521D\u503C\u7684",
            /* @__PURE__ */ jsx("strong", { children: "\u7CBE\u786E\u5B9E\u6570\u70B9\u67E5\u8BE2" }),
            "\u3002\u4E0D\u63D0\u4F9B\u672A\u77E5\u521D\u503C\u7684\u516C\u5F0F\u3001\u79EF\u5206\u3001\u5BFC\u6570\u6216\u6F14\u5316\u503C\u3002\u989D\u5916\u53D6\u5F97\u521D\u503C\u4FE1\u606F\u7684\u9884\u5904\u7406\u4E5F\u987B\u8BA1\u5165\u67E5\u8BE2\uFF0C\u5DF2\u6709\u6837\u672C\u7684\u7B97\u672F\u5904\u7406\u4E0D\u8BA1\u67E5\u8BE2\u8D39\uFF1B \u540C\u65F6\u4E5F\u6CA1\u6709\u968F\u673A\u6BD4\u7279\u3001\u6709\u9650\u7CBE\u5EA6\u3001\u7B97\u672F\u590D\u6742\u5EA6\u3001\u5185\u5B58\u3001\u5B9E\u9645\u8FD0\u884C\u65F6\u95F4\u6216\u5DE5\u7A0B\u52A0\u901F\u7ED3\u8BBA\u3002"
          ] }),
          /* @__PURE__ */ jsxs(Callout, { tone: "neutral", title: "\u53D8\u53F7\u65F6\uFF0C\u603B\u8D28\u91CF\u4E0D\u8DB3\u4EE5\u51B3\u5B9A\u957F\u671F\u7ED3\u679C", children: [
            "\u56FA\u5B9A\u7684\u4E24\u4E2A\u5149\u6ED1\u521D\u503C\u53EF\u4EE5\u5177\u6709\u76F8\u540C\u7684\u96F6\u603B\u8D28\u91CF\uFF0C\u5374\u5206\u522B\u8D8B\u5411\u6B63\u3001\u8D1F\u5E73\u8861\u6001\u3002 D27\u56E0\u6B64\u4F30\u8BA1\u5B9E\u9645PDE\u5B9A\u4E49\u7684\u975E\u7EBF\u6027\u76F8\u4F4DA(v)\uFF0C\u5E76\u7528\u6709\u9650\u8BA1\u7B97\u6784\u9020\u4FEE\u6B63\u7CFB\u6570\uFF1B\u5B83\u6CA1\u6709\u8C03\u7528\u514D\u8D39\u7684\u76F8\u4F4D\u6216PDE\u89E3\u9884\u8A00\u673A\u3002 \u5355\u4F4D\u73AF\u9762\u7684\u5F3A\u6269\u6563\u6DF7\u5408\u662F\u8BC1\u660E\u6761\u4EF6\uFF0C\u4E0D\u80FD\u76F4\u63A5\u63A8\u5E7F\u5230\u5927\u533A\u57DF\u6216\u5F31\u6269\u6563\u3002",
            /* @__PURE__ */ jsx(Text, { size: "small", children: "\u5E38\u89C4\u8BC1\u660E\u4E0E\u72EC\u7ACB\u5BA1\u67E5\u5DF2\u901A\u8FC7\uFF1B\u53D8\u53F7\u7B97\u6CD5\u5C1A\u65E0Lean\u6216\u6570\u503C\u8BC1\u636E\u3002\u53BB\u9664\u7EF4\u6570\u9650\u5236\u4ECD\u5728\u7814\u7A76\u3002" })
          ] }),
          /* @__PURE__ */ jsxs(Text, { size: "small", tone: "secondary", children: [
            "D22\u2013D27 \u5747\u5728\u5355\u4F4D\u73AF\u9762\u4E0A\u3002D26 \u8FD8\u8981\u6C42 f(0)=f(b)=0\u3001f \u5728(0,b)\u5185\u4E3A\u6B63\u3001f'(0)=\u03BB \u4E3A\u6B63\uFF1Bb\u5904\u53EF\u9000\u5316\u3002 \u7406\u8BBA\u6765\u6E90\uFF1A",
            /* @__PURE__ */ jsx(Link, { href: d22Path, children: "D22" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: d23Path, children: "D23" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: d24Path, children: "D24" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: d25Path, children: "D25" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: d26Path, children: "D26" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: d27Path, children: "D27" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: t59Path, children: "T59\u72EC\u7ACB\u5BA1\u67E5" }),
            "\u3002"
          ] })
        ] }),
        /* @__PURE__ */ jsxs(Stack, { gap: 12, children: [
          /* @__PURE__ */ jsxs(Row, { justify: "space-between", align: "end", gap: 16, wrap: true, children: [
            /* @__PURE__ */ jsxs(Stack, { gap: 4, children: [
              /* @__PURE__ */ jsx(H2, { children: "Lean \u5B9E\u9645\u8986\u76D6 \xB7 \u4FE1\u606F\u6838\u4E0E\u6B63\u7C7B\u98CE\u9669" }),
              /* @__PURE__ */ jsx(Text, { tone: "secondary", children: "\u4EE5\u4E0B\u56DB\u4E2A\u6A21\u5757\u5206\u522B\u8986\u76D6\u6982\u7387\u79EF\u5206\u3001\u6709\u9650\u81EA\u9002\u5E94\u6C42\u503C\u5668\u53CA\u7EDF\u8BA1\u8BEF\u5DEE\uFF1BPDE \u504F\u5DEE\u4ECD\u662F\u663E\u5F0F\u7684\u5916\u90E8\u6570\u5B66\u8F93\u5165\u3002" })
            ] }),
            /* @__PURE__ */ jsx(Pill, { active: true, children: "\u4E3B\u4EFB\u52A1\u5BF9\u5E94\u5BA1\u67E5\u901A\u8FC7" })
          ] }),
          /* @__PURE__ */ jsx(
            Table,
            {
              headers: ["\u6A21\u5757", "Lean \u4E2D\u5B9E\u9645\u8BC1\u660E", "\u4ECD\u5C5E\u5E38\u89C4\u8BBA\u8BC1 / \u672A\u8986\u76D6"],
              rows: [
                [
                  "T42 \xB7 \u67E5\u8BE2\u4FE1\u606F\u79EF\u5206",
                  "\u4EFB\u610F\u6982\u7387\u7A7A\u95F4\u4E0A\u7684\u914D\u5BF9\u5E73\u65B9\u635F\u5931\u4E0E\u671F\u671B\u67E5\u8BE2\u4E0B\u754C\uFF1B\u4E0D\u8981\u6C42\u8F93\u51FA\u6709\u754C\u6216\u65E0\u504F\uFF0C\u8BBF\u95EE\u96C6\u5408\u5148\u4F5C\u9010\u70B9\u4F30\u8BA1\uFF0C\u518D\u5BF9\u635F\u5931\u79EF\u5206\u3002",
                  "PDE\u3001\u70ED\u6838\u3001\u5E73\u6ED1 bump\u3001\u4E00\u822C\u968F\u673A\u7B97\u6CD5\u5D4C\u5165\u3002"
                ],
                [
                  "T43 \xB7 \u81EA\u9002\u5E94\u6C42\u503C\u5668",
                  "\u771F\u5B9E fuel \u6709\u9650\u6C42\u503C\u5668\u7684\u8F68\u8FF9\u5F52\u7EB3\u3001no-hit \u540C\u8F68\u8FF9\u540C\u8F93\u51FA\u3001\u8BBF\u95EE\u5355\u5143\u6570\u2264\u67E5\u8BE2\u6570\u3002",
                  "\u65E0\u9650\u79CD\u5B50\u7A7A\u95F4\u7684\u53EF\u6D4B\u7F16\u7801\u4E0E\u9010\u79CD\u5B50\u975E\u7EDF\u4E00\u505C\u673A\u6865\u63A5\u3002"
                ],
                [
                  "T51 \xB7 \u03A8 \u53D8\u6362",
                  "\u4ECE \u03A8(z)=z/\u221A(1+z\xB2) \u63A8\u5BFC\u951A\u5B9A\u4E0D\u7B49\u5F0F\u3001\u5B9E\u9645\u79EF\u5206\u635F\u5931\u754C\u4E0E\u7CBE\u786E 25/1024 \u504F\u5DEE\u5408\u6210\u3002",
                  "PDE \u8FD1\u4F3C\u3001\u8D28\u91CF\u63D2\u503C\u3001\u5747\u5300\u504F\u5DEE\u22641/32\u3002"
                ],
                [
                  "T52 \xB7 \u72EC\u7ACB\u6837\u672C\u5747\u503C",
                  "\u4ECE\u53EF\u6D4B Pairwise IndepFun \u4E0E 0\u2264Y\u1D62\u2264A \u63A8\u5BFC L\xB2\u3001\u65E0\u504F\u3001MSE\u2264Am/n\u3001rpow \u7F29\u653E\u4E0E\u603B MSE<1/16\u3002",
                  "iid \u5747\u5300\u70B9\u6837\u672C\u7684\u5B9E\u73B0\u6865\uFF1B\u4E00\u822C C\xB2 \u7684 \u03A6 \u5750\u6807\u4E0E\u6709\u9650\u8868\u3002"
                ]
              ],
              columnAlign: ["left", "left", "left"],
              striped: true,
              framed: true
            }
          ),
          /* @__PURE__ */ jsx(Callout, { tone: "warning", title: "T51/T52 \u4E0D\u662F\u7AEF\u5230\u7AEF PDE \u5F62\u5F0F\u5316", children: "\u5373\u4F7F T51/T52 \u5DF2\u901A\u8FC7\uFF0CD24 \u7684\u9AD8\u5EA6\u2014\u8D28\u91CF\u63D2\u503C\u3001\u70ED\u6DF7\u5408\u3001\u975E\u7EBF\u6027 PDE \u6BD4\u8F83\u3001\u7EDF\u4E00\u504F\u5DEE\u4EE5\u53CA iid \u521D\u503C\u67E5\u8BE2\u5B9E\u73B0\u4ECD\u662F\u5E38\u89C4\u6570\u5B66\u8F93\u5165\u3002 D26 \u7684\u4E00\u822C C\xB2 \u6807\u91CF\u5750\u6807\u3001\u6709\u9650\u516C\u5F00\u8868\u4E0E PDE \u7EA6\u5316\u6CA1\u6709 Lean \u8986\u76D6\u3002D25/D27\u7684urn\u4FE1\u606F\u8BBA\u8BC1\u3001\u76F8\u4F4D\u4E0E\u5BFC\u6570\u6D4B\u5EA6\u4E5F\u672A\u56E0\u6B64\u5F62\u5F0F\u5316\u3002" }),
          /* @__PURE__ */ jsxs(Text, { size: "small", tone: "secondary", children: [
            "\u5F62\u5F0F\u5316\u62A5\u544A\uFF1A",
            /* @__PURE__ */ jsx(Link, { href: t42Path, children: "T42" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: t43Path, children: "T43" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: t51Path, children: "T51" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: t52Path, children: "T52" }),
            "\uFF1B\u4E3B\u4EFB\u52A1\u5BF9\u5E94\u5BA1\u67E5\uFF1A",
            /* @__PURE__ */ jsx(Link, { href: t42t43RootPath, children: "T42/T43" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: t51RootPath, children: "T51" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: t52RootPath, children: "T52" }),
            "\u3002"
          ] })
        ] }),
        /* @__PURE__ */ jsxs(Stack, { gap: 12, children: [
          /* @__PURE__ */ jsxs(Row, { justify: "space-between", align: "end", gap: 16, wrap: true, children: [
            /* @__PURE__ */ jsxs(Stack, { gap: 4, children: [
              /* @__PURE__ */ jsx(H2, { children: "E3 \xB7 \u67E5\u8BE2\u4FE1\u606F\u6838\u7684\u6709\u9650\u7CBE\u786E\u68C0\u67E5" }),
              /* @__PURE__ */ jsx(Text, { tone: "secondary", children: "\u4E00\u6B21\u51BB\u7ED3\u8FD0\u884C\uFF1BFraction \u7A77\u4E3E\u52A0\u4E24\u79CD\u9AD8\u7CBE\u5EA6\u79EF\u5206\u516C\u5F0F\uFF0C\u53EA\u68C0\u67E5 D22 \u4FE1\u606F\u6838\u4E0E\u6807\u91CF\u516C\u5F0F\u7684\u6709\u9650\u5B9E\u4F8B\u3002" })
            ] }),
            /* @__PURE__ */ jsx(Pill, { active: true, children: "\u56FA\u5B9A\u8303\u56F4 PASS" })
          ] }),
          /* @__PURE__ */ jsxs(Grid, { columns: 4, gap: 12, children: [
            /* @__PURE__ */ jsx(Stat, { value: "25,960", label: "\u7CBE\u786E\u914D\u7F6E" }),
            /* @__PURE__ */ jsx(Stat, { value: "334,020", label: "\u6C42\u503C\u5668\u8FD0\u884C" }),
            /* @__PURE__ */ jsx(Stat, { value: "154,030", label: "no-hit \u66FF\u4EE3\u8FD0\u884C" }),
            /* @__PURE__ */ jsx(Stat, { value: "105 + 5", label: "\u4E3B\u8868 + \u6DF7\u5408\u8868\u884C" })
          ] }),
          /* @__PURE__ */ jsxs(Grid, { columns: "1fr 1fr", gap: 14, children: [
            /* @__PURE__ */ jsxs(Card, { children: [
              /* @__PURE__ */ jsx(CardHeader, { trailing: "\u4E00\u6B21\u5B98\u65B9\u8FD0\u884C \xB7 11.332 s", children: "\u68C0\u67E5\u4E86\u4EC0\u4E48" }),
              /* @__PURE__ */ jsx(CardBody, { children: /* @__PURE__ */ jsxs(Stack, { gap: 6, children: [
                /* @__PURE__ */ jsx(Text, { size: "small", children: "\u5168\u90E8 no-hit \u8FD0\u884C\u4FDD\u6301\u8F93\u51FA\u4E0E\u5B8C\u6574\u6709\u5E8F\u8F68\u8FF9\u4E00\u81F4\u3002" }),
                /* @__PURE__ */ jsx(Text, { size: "small", children: "\u8BBF\u95EE\u5355\u5143\u6570\u4E0D\u8D85\u8FC7\u67E5\u8BE2\u6570\uFF1B25,960 \u4E2A\u914D\u5BF9\u635F\u5931\u68C0\u67E5\u5168\u90E8\u7CBE\u786E\u901A\u8FC7\u3002" }),
                /* @__PURE__ */ jsx(Text, { size: "small", children: "105 \u4E2A\u4E3B\u6C47\u603B\u884C\u3001820 \u4E2A\u56FA\u5B9A\u66FF\u4EE3\u98CE\u9669\u548C 5 \u4E2A\u9884\u7B97\u6DF7\u5408\u884C\u7531\u4E3B\u4EFB\u52A1\u5BA1\u67E5\u91CD\u65B0\u8BA1\u7B97\u3002" }),
                /* @__PURE__ */ jsx(Text, { size: "small", children: "\u4E24\u79CD\u79EF\u5206\u7ED3\u679C\u76F8\u5DEE\u7EA6 4.63\xD710\u207B\u2078\xB3\uFF0C\u4F4E\u4E8E\u56FA\u5B9A 10\u207B\u2077\u2070 \u6BD4\u8F83\u9608\u503C\uFF1B\u8FD9\u4E0D\u662F\u4E25\u683C\u79EF\u5206\u5305\u7EDC\u3002" })
              ] }) })
            ] }),
            /* @__PURE__ */ jsx(Callout, { tone: "warning", title: "E3 \u7684\u6709\u9650\u89D2\u8272", children: "E3 \u4F7F\u7528\u62BD\u8C61\u5206\u914D\u76EE\u6807\uFF0C\u65E2\u4E0D\u662F PDE \u6C42\u89E3\uFF0C\u4E5F\u4E0D\u662F D24 \u4E0A\u754C\u7B97\u6CD5\u7684\u6570\u503C\u9A8C\u8BC1\uFF1B\u5B83\u4E0D\u80FD\u7ECF\u9A8C\u6027\u8BC1\u660E\u5BF9\u6240\u6709\u53EF\u6D4B\u968F\u673A\u7B97\u6CD5\u7684\u666E\u904D\u91CF\u8BCD\u3002 \u4E3B\u4EFB\u52A1\u5BA1\u67E5\u91CD\u65B0\u8BA1\u7B97\u4E86\u5B58\u50A8\u6C47\u603B\uFF0C\u4F46\u6CA1\u6709\u91CD\u653E\u5B8C\u6574\u6C42\u503C\u5668\uFF0C\u4E5F\u6CA1\u6709\u91CD\u65B0\u6267\u884C\u9AD8\u7CBE\u5EA6\u79EF\u5206\u3002" })
          ] }),
          /* @__PURE__ */ jsxs(Text, { size: "small", tone: "secondary", children: [
            "\u51BB\u7ED3\u8BC1\u636E\uFF1A",
            /* @__PURE__ */ jsx(Link, { href: e3ResultPath, children: "check_result.json" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: e3ManifestPath, children: "execution_manifest.json" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: e3ReportPath, children: "T49 \u62A5\u544A" }),
            " \xB7 ",
            /* @__PURE__ */ jsx(Link, { href: e3RootAuditPath, children: "\u4E3B\u4EFB\u52A1\u8F93\u51FA\u5BA1\u67E5" }),
            "\u3002"
          ] })
        ] }),
        /* @__PURE__ */ jsxs(Stack, { gap: 10, children: [
          /* @__PURE__ */ jsx(H2, { children: "\u65E9\u671F\u7406\u8BBA\u9002\u7528\u8303\u56F4" }),
          /* @__PURE__ */ jsx(
            Table,
            {
              headers: ["\u573A\u666F", "\u5DF2\u5EFA\u7ACB\u7684\u7ED3\u8BBA", "\u5FC5\u987B\u4FDD\u7559\u7684\u8FB9\u754C"],
              rows: [
                [
                  "\u7D27\u81F4\u60C5\u5F62 \xB7 \u539F\u59CB\u7F16\u7801",
                  "\u82E5 f(v) \u4E0D\u6052\u4E3A\u96F6\uFF0C\u4E14\u67D0\u4E2A\u9AD8\u9636\u5BFC\u6570 f^(p)(v)\uFF08p\u22652\uFF09\u4E0D\u6052\u4E3A\u96F6\uFF0C\u5219\u5728\u67D0\u4E2A\u6709\u9650 T \u540E\u4E0D\u518D\u7EDD\u5BF9\u53EF\u79EF\u3002",
                  "\u8FDE\u901A\u5E73\u5766\u73AF\u9762\u4E0A\u7684\u539F\u59CB\u5355\u6811\u8868\u793A\uFF1B\u8981\u6C42\u652F\u6301\u6240\u6709\u975E\u96F6\u9879\u3001\u7CBE\u786E\u4F3C\u7136\u6743\u91CD\u4E14\u51E0\u4E4E\u5FC5\u7136\u5B8C\u6210\u3002\u53CD\u5E94\u96F6\u70B9\u53CA\u4EFF\u5C04\u7EC8\u7AEF\u5BFC\u6570\u65CF\u662F\u4F8B\u5916\u3002"
                ],
                [
                  "\u975E\u7D27\u81F4\u9AD8\u65AF \xB7 f = \u2212u\xB2",
                  "\u82E5 0 < \u03B5 \u2264 1/32\uFF0C\u5219\u539F\u59CB\u8868\u793A\u4E00\u9636\u7EDD\u5BF9\u77E9\u5728\u6240\u6709\u6709\u9650\u65F6\u57DF\u53EF\u79EF\uFF0C\u5F53\u4E14\u4EC5\u5F53 d \u2265 5\u3002",
                  "\u4EC5\u9488\u5BF9\u6307\u5B9A\u9AD8\u65AF\u6570\u636E\u65CF\u4E0E\u539F\u59CB\u8868\u793A\uFF1B\u89C1 T15\u3002"
                ],
                [
                  "\u540C\u4E00\u89C4\u8303\u7EDD\u5BF9\u8D28\u91CF \xB7 i.i.d. \u6839",
                  "\u540C\u4E00\u5C0F\u9AD8\u65AF\u6570\u636E\u65CF\u4E2D\uFF0C\u56FA\u5B9A d\u22655\u3001x=0\uFF0C\u4EE5\u9884\u5B9A\u6570\u91CF\u7684\u72EC\u7ACB\u540C\u5206\u5E03\u65E0\u504F\u6839\u53D6\u5E73\u5747\uFF0C\u56FA\u5B9A\u76F8\u5BF9\u7CBE\u5EA6\u9700\u8981 \u03A9(T\xB2) \u4E2A\u6839\u3002",
                  "\u5339\u914D\u9AD8\u65AF\u7684\u6807\u51C6\u4E8C\u53C9\u8868\u793A\u5728 T \u4E0A\u6709\u4E00\u81F4\u7684\u76F8\u5BF9\u65B9\u5DEE\u754C\uFF1B\u4EC5\u4E3A\u7406\u60F3\u5B9E\u6570\u3001\u8282\u70B9\u8BA1\u6570\u5C42\u9762\u7684\u6BD4\u8F83\uFF0C\u89C1 T20\u3002"
                ]
              ],
              columnAlign: ["left", "left", "left"],
              rowTone: ["neutral", "info", "warning"],
              striped: true
            }
          )
        ] }),
        /* @__PURE__ */ jsxs(Stack, { gap: 8, children: [
          /* @__PURE__ */ jsx(H2, { children: "\u672C\u5730\u8BC1\u636E\u94FE" }),
          /* @__PURE__ */ jsxs(Row, { gap: 14, wrap: true, children: [
            /* @__PURE__ */ jsx(Link, { href: reportPath, children: "\u7EFC\u5408\u62A5\u544A" }),
            /* @__PURE__ */ jsx(Link, { href: claimsPath, children: "D1\u2013D27 \u58F0\u660E\u8D26\u672C" }),
            /* @__PURE__ */ jsx(Link, { href: artifactAuditPath, children: "T14 \u6570\u503C\u4E0E\u5236\u54C1\u5BA1\u8BA1" }),
            /* @__PURE__ */ jsx(Link, { href: noncompactAuditPath, children: "T15 \u975E\u7D27\u81F4\u4E8C\u6B21\u578B\u5BA1\u8BA1" }),
            /* @__PURE__ */ jsx(Link, { href: relativeCostAuditPath, children: "T20 \u76F8\u5BF9\u4EE3\u4EF7\u5BA1\u8BA1" })
          ] }),
          /* @__PURE__ */ jsx(Text, { size: "small", tone: "tertiary", children: "\u5C55\u793A\u503C\u76F4\u63A5\u6765\u81EA\u5DF2\u5BA1\u8BA1\u6458\u8981\uFF1B\u672C\u9875\u4E0D\u589E\u52A0\u65B0\u6570\u503C\uFF0C\u4E5F\u4E0D\u4F5C\u65B0\u9896\u6027\u4E3B\u5F20\u3002" })
        ] })
      ]
    }
  );
}
export {
  DynamicContinuationEvidence as default
};
