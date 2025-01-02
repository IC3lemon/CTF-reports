from Crypto.Util.number import *

n = 17628634994164171248706381420942615651173281189175992058302939438016374807776451573422125283240280011455471762806095247762996713737011864552809727131586433503509747587268723462088098068964590547604908612126866710785327643821535702456610008348114529563289511953385391924086192250610181275567143135444800219435040532641299964377041213388422136136099433489662449931021690446786213476004562062296148232117397826761739334549260214913794841677666811344226662292741290745244898152291781880846509885758289790656199049487897330196728755690236887574730924305303171939152830458235802220367796833434028751192855537534963085150323
c = 10155852720057982164373202064751526191451109176158214506377608444273503052750128711972976192671856321759037711887148652303345941552656324492833922557061646822387554917110000324627580287791931926770717577929929461902841204389274988454541797923947564735645839877806776414746987410460480042441128984475052834280784337797088882169669793518253934605055119743337237295738281796295979268289416817307421447724411367202284096562481832857631996614862114974916769058928196199348844406818280961799985455109171709429411628156903472192932693281646361706664393719981001244573382830081536162471368300625573155553910039945833436313536
hints = [186328507787082442465847881685302559236598165995079010532177301149220383721452843826987137971842083996156825065576143662081361859795100788347926164595279771943972332564309981240998579222453176724055609267774649982052748765528046168222051953280418084665987746995914578501336533045628622336551503587252504491620500935888276448861713122620762609300458776641774277288788714925890549727202463796260359066130, 591961902603046804828599763329368606539855766800458166654904604477898572573283840513704936482628981649119430534616535204808185556715837045278876202861029483690409064069175798403627700222407918085572951459925700128177551106937720449042489408890650765833857397204195940246251316538885609229873226566043928113466677019916102180438118046118057834950645378996880115866308297458116367271964721091249552832519]
h1, h2 = hints
# h1 = a1*p + b1*q
# h2 = a2*p + b2*q

# a1, a2 are small, in range 2**12 i.e. 4096
# a2*h1 = a1*a2*p + b1*a2*q ---- 1
# a1*h2 = a1*a2*p + b2*a1*q ---- 2
# eqn 1 - eqn 2 
# a2*h1 - a1*h2 = b1*a2*q - b2*a1*q
# a2*h1 - a1*h2 = 0 (mod q)

# thus brute a2, a1, gcd(a2*h1 - a1*h2, n) to get q

found_q = False
for a1 in range(2**12):
    for a2 in range(2**12):
        q = GCD(a2*h1 - a1*h2, n)
        if q != 1 and q < n:
            found_q = True
            break
    if found_q:
        # print(q, isPrime(q))
        break

p = n // q
e = 0x10001
d = inverse(e, (p-1)*(q-1))
print(long_to_bytes(pow(c, d, n))) # DUCTF{gcd_1s_a_g00d_alg0r1thm_f0r_th3_t00lbox}

