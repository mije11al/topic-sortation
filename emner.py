# -*- coding: latin-1 -*-
"""
Functions for sorting Facebook text data into topics
@Author: Michael Jensen, Louise Schi�tt
@Date:   2017-08-22
@Email:  michael@nextwork,as

"""

import pandas as pd
import os,re
import glob



#==============================================================================
import sys  

reload(sys)  
sys.setdefaultencoding('latin-1')

#==============================================================================

#wordlist used for topics
aeldre=[u"�ldrepleje", u"de �ldre", u"�ldre mennesker", "hjemmepleje", u"hjemmehj�lp", "sosu ", "plejepersonale", u"plejecenter",u"�ldrebolig","alderdom", u"varme h�nder", u"�ldreomr�de", u"�ldreminist"]
andre_trossamfund=[u"trossamfund", "trosretning", u"vielsesbemyndig", u"begravelsespladser", u"religionsfrihed", "frikirke", "katolik", "pave", "rabbiner","synagoge", "hindu", "buddhis", " munk", "scientology", " sekt "]
arbejdsloeshed=[u"arbejdsl�s", u"g� ledig", "ledighed", "langtidsledig", "lediggang", u"i besk�ftigelse", "arbejdsformidling", "jobrettet", u"jobs�gning", u"s�ge job", u"s�ge arbejde", u"arbejdss�gende", "finde arbejde", "finde et arbejde", "finde job", "finde et job", u"fleksjob", u"jobcenter", u"besk�ftigelsesindsats", u"virksomhedspraktik", u"l�ntilskud", u"ressourceforl�b", u"seniorjob", "arbejdsmarkedsparat", "aktivering", u"jobs�gningskursus", ]
arbejdsmiljoe=[u"arbejdsmilj�", u"arbejdsgl�de", "trivsel p� arbejdspladsen", u"trivselsm�ling", u"trivselsunders�gelse", "arbejdstilsyn", u"mobning p� arbejdspladsen", u"voksenmobning", u"arbejdsstilling", u"arbejdsskade", u"arbejdsulykke", u"erhvervssygdom", " APV ", "arbejdspladsvurdering", "hviletid", u"k�re hvile tid", u"k�re/hvile-tid", u"k�rehviletid", "11-timersreglen", "11 timers reglen", "11-timers reglen", "hvileperiode", u"frid�gn", u"sygefrav�r", "arbejdsforhold",]
barsel=["barsel", u"for�ldreorlov", "graviditetsorlov", u"f�dreorlov", "adoptionsorlov", u"m�dregruppe"]
boernepasning=["dagpleje", u"daginstitution", u"vuggestue", u"b�rnehave", u"skovb�rnehave", u"integreret institution", u"privat b�rnehave", u"privat vuggestue", u"pladsanvisning", u"pasningsgaranti", u"p�dagog", u"normering", "fritidshjem", u" sfo ", u"ungdomsklub"]
byggeri_bolig=[u"statslige ejendomme", u"regulering af byggebranchen", u"offentligt byggeri", u"almenbolig", u"boligselskab", u"lejeloven", u"ungdomsbolig", u"�ldrebolig", u"andelsbolig", u"ejerbolig", u"boligst�tte", "boligydelse", "boligpakke", "boliglov", u"boligomr�de", "boligforhold", "studiebolig", "boligmangel", "mangel p� boliger","bolig"," hus "]
danskhed_debat=["danskhed", "udansk", u"at v�re dansk", u"danske v�rdier", u"dansk v�rdi", u"indf�dsretspr�ve", "ikke-vestlig indflydelse", "national identitet", "islamisering", "nationalret", "national ret", "nationaldyr"]
digitalisering_off=[u"digitaliseringsstrategi", u"digital handlingsplan", u"datasikkerhed", u"it-sikkerhed", u"it-arkitektur", u"digital omstilling", u"digital signatur", u"nemid", u"nemkonto", u"nemsms", u"digital post", u"e-boks", "datafordeler"]
diskrimination=["diskrimin", "racis", "fremmedfjendsk", "fremmedhad", u"forskelsbehandling", u"institut for menneskerettigheder", u"hadforbrydelse", "sexis", "k�nsdiskrimin", "kvindeundertryk", "islamofob", u"hadpr�dikant", "homofob", "perker"]
efteruddannelse_opkvalificering=["efteruddan", u"opkvalificering", u"diplomuddannelse", u" mba ", u"mini-mba", u"veu-godtg�relse", " amu ", "voksenuddannelse", "akademiuddannelse", "realkompetencevurder", u"�bent universitet", ]
energiforsyning=[u"energiforsyn", "energiressource", "energiresurse", "energireserve", "energiudvind", u"energianl�g", u"r�stof", u"energisystem", u"elforsyning", u"elv�rk", u"elanl�g", u"gasforsyning", u"vandforsyning", u"fossile br�nds", "oliefyr", u"vedvarende energi", u"gr�n energi", u"b�redygtig energi", u"biobr�ndsel", "biogas", u"vindenergi", u"vindm�lle", u"solenergi", u"solcelle", "geotermi", "varmepumpe", "biogas", u"olieudvinding", u"boreplatform", u"gasudvinding", "elforbrug", u"str�mafbrydelse", u"str�msvigt", "bore efter olie",]
eu=[" eu ", u"europa-parlamentet", u"det europ�iske r�d", u"europa-kommissionen", u"ministerr�det", u"r�det for den europ�iske union", u"eu-domstol", u"  e�s ", u"  edps ", u"europol", u"csdp", u"f�lles m�ntfod", u"  euro ", u"retsforbehold", u"eu-kommiss�r", "kommitologi", "brexit", u"miste suver�nitet", u"mister suver�nitet", u"afgive suver�nitet", u"afgiver suver�nitet", "danske forbehold", "danmarks forbehold"]
faengsler=[u"f�ngsler", u"i f�ngsel", u"f�ngselsbetjent", "kriminalforsorg", "de indsatte", u"f�ngselscelle", u"pr�vel�sladt",]
familieliv=["familieliv", u"b�rnefamilie", "storfamilie", u"�gteskab", u"skilsmisse", u"for�ldremyndighed", u"statsamt", u"faderskab", u"adoption", u"regnbuefamilie" , u"familieform", u"v�re for�ldre", "juridisk abort", u"b�rnebidrag", "medmor", u"for�ldrelovsdirektiv", "barnets tarv", u"v�re mor", u"v�re far", "blive mor", "blive far", u"blive for�ldre",]
feminisme=["feminist", "feminisme", u"f�rsteb�lge", u"andenb�lge", u"tredjeb�lge", u"fjerdeb�lge", "kvindekamp", u"r�dstr�mpe", "international kampdag", "kvindernes internationale kampdag", "patriarkat", u"kvindebev�gelse", "kvinfo"]
fertilitet=["fertil", u" f�dsel ", u"gravid", u"pr�vention", u"barnl�s", u"s�ddonor", u"�gdonor", u"donors�d", u"donor�g", u"s�tte �g op", "insemination", "inseminere", "reagensglasbarn", "reagensglasbehandling", " IVFI ", " ICSI ", "endometriose", u"s�dkvalitet", "abort"]
film_tv=[u"filmskole", "cannes", "oscar-uddeling", "oscar uddeling", "oscars", "golden globe", "susanne bier", "von trier", "dox", "pix", "sundance", "thomas vinterberg", "filminstitut", "filmfestival", "filmkunst", "biografkultur", u"g� i biografen", "filmproduktion", "filmkultur", "filmpremiere", "biografpremiere", "spillefilm", "dokumentarfilm", "tv-program", "tv program", "se tv", "se fjernsyn", "program i fjernsynet", "flow-tv", "flow tv", "streame tv", "streame film", "streaming-tjeneste", "streaming tjeneste", "netflix", " hbo ", "viaplay", "dr tv", "tv2 play"]
finanslov=["finanslov", u"statslige udgifter", "finanspolitiske prioriteringer", "statens budget", u"statsbudget", u"�konomiaftale", "statens udgifter", "till�gsbevilling", "budgetvejledningen",]
finanssektor =["finanskrise", u"finanssektor", u"kapital", u"cashflow", u"invester", u"aktie", u"obligation", u" �op ", u" kreditvurdering ", u"nationalrente", u"renters rente", u"l�netype", u"egenkapital", u"kapitalrunde"]
flygtninge=[u"flygtning", "asyl", "flygte fra krig", "flygter fra krig", u"mennesker p� flugt", "teltlejre", "sandholmlejr", "internt fordrevn", "modtagelsescent", "udrejsecent", ]
foedevarer=[u"�kologi", u"konventionelle f�devarer", u"bur�g", u"fritg�ende", "etisk forbrug", "forbrugsetik", "bevidst forbruger", u"b�redygtige f�devarer", u"dyrevelf�rd", "fairtrade", "supermarked", "glutenfri", "laktosefri", u"k�dfri", u"mindre k�d", "vegetar", "vegan", u"f�devarepris", "madspild", "dagligvare", "egnsret", "spisevaner", "madtrend", "lokalt produceret", u"indk�bspose", u"k�be ind", "forbrugskultur", u"r�vare", ]
folkekirken_kristendom=["folkekirke", "statskirke", "kirkeminister", "gudstjeneste", "kirkelig", u"kirkeskat", u" sogn", u"barned�b", u"konfirmation", u"vielse", "kirkebryllup", u"begravelse", u"pr�st", u"biskop", "menighed", u"g� i kirke", u"g�r i kirke", "kristen", "kristne",]
folkeskole=["folkeskole", "grundskole", u"privatskole", u"friskole", u"efterskole", u"specialskole", u"kostskole", u"undervisningspligt", u"folkeskolereform", u"klassekvotient", u"pisa-test", u"skolel�rer", u"l�rermangel", "skoledag", u"lektiehj�lp", "skolebibliotek", "indskoling", "udskoling", "klassetrin", "elevplan", u"afgangspr�ve", "skolebestyrelse", "skole-hjem-samtale"]
forbrug_kemi=[u"svanem�rket", "eu-blomsten", u"milj�m�rket", "kemiindhold", "flourerede stoffer", "bisphenol", "ftalater", "phtalater", "mikroplast", "tungmetal", "skadelige stoffer", "hormonforstyrrende", u"kr�ftfremkaldende", "parabene", "parfumestof", "allergifremkaldende", u"tils�tningsstof", "konserveringsmid", "e-numre", " mi ", " pcb ", "triclosan", "kontaktallergi", "hverdagskemi"]
forskning=[" forsker ", " forskning ", u"videnskabelig unders�gelse", u"forskningskroner", u"forskningsmidler", u"forskningsbevilling", u"grundforskning", u"basisbevilling"]
forskning_sygdomme=[u"kr�ftforskning", u"hjerneforskning", "hjerneforsker", u"kr�ftforsker", "gigtforsker", "gigtforskning", "forskning i gigt", "forskning i sygdomme", "medicinsk forskning", u"forskning i m�nds helbred", u"forskning i kvinders helbred", "hjerteforsker", "hjerteforskning", "forskning i hjertekarsygdomme", "forske i sygdom", "forskning i sukkersyge", "forskning i diabetes", "forskning i psykiske lidelser", "forskning i psykiatri", "forskning i demens", "forskning i alzheimerz"]
forsvaret=[u"forsvaret", u"forsvarskommando", u"hjemmev�rn", u"beredskabsstyrelsen", u"forsvarets efterretningstjeneste", u"h�ren", "forsvarskommando", "soldater", u"flyvev�bnet", "hangarskib", u"s�v�rnet", "redningshelikopter", "kampfly", "f-16", "kaserne", "kampvogn", u"pansret k�ret�j", u"b�ltek�ret�j", u"fl�den", u"milit�r", "rullemarie", "fregat", "arktisk kommando", "forsvarsakademiet", u"st�jportal", "blive soldat", u"v�re soldat"]
fysiske_sygdomme=[u" kr�ft ", u"kr�ftpatient", u"kr�ftdiagnose", u"kr�ftsygdom", u"kr�ftramt", " cancer ", u"sklerose", u" gigt", "hjertesyg", "hjertekarsygdom", "hjerte-kar-sygdom", "hjerte kar sygdom", "muskelsvind", u"influenza", u"blodprop", u"fork�le", u"allergi", " astma ", u"hjertestop", u"kronisk syg", "kroniske smerter", "progeria", " MRSA ", "meningitis", u"k�nssygdom", "klamydia", "gonore", "HPV", " HIV ", " Aids ", " KOL ", "rygerlunger", "diabetes", "sukkersyge", "apopleksi", "leversyg", "nyresyg", "blodsyg", "infektion", "epidemi", "pandemi", "svulst", "tumor", "terminalpatient", u"migr�ne", "ondt i ryggen", "ondt i nakken", "rygsmerter", "nakkesmerte", u"piskesm�ld", "diskosprolaps"]
handelspolitik_udenrigsoekonomi=[u"handelspolitik", u"udenrigs�konomi", " ttip ", "toldbarriere", u"frihandel", u"samhandel", u"import", u"eksport", u"handelsbalance", u"protektionisme", u"handelsliberalisering", u"investeringsbeskyttelse", u"global �konomi", u"konkurrenceevne", u"verdensbanken", u"udviklingsland", u"briks", u"gr�nse�konomi"]
handicap=["handicap", "invalid", u"f�rlighed", u"bev�gelsesh�mmet", u"k�restol", "rullestol", u"funktionsneds�ttelse", u"udviklingsh�mmet", u"hjerneskade", u"specialomr�det", u"tilg�ngelighedsregler", u"tilg�ngelighedsdirektiv", " downs syndrom", "diskriminationsforbud", "nedsat syn", u"nedsat h�relse", u"h�reh�m", u"h�reneds", "spastiker", "spastisk lamme", "svagtsyn",  "blindesamfund", u"d�vstum", u"d�vblind", "ordblind", "dysleksi", "tegnsprog", ]
hospitalsvaesen=["hospital", u"sygehus", u"patient", u"privathospital", u"supersygehus", u"ambulance", u"overbel�gning", u"operation", "ligger p� gangene", "kirurg", u"overl�ge", u"narkosel�ge", u"kr�ftl�ge", "onkolog", "sygeplejerske"]
idraetsliv=[u"idr�t", u"  dgi ", " dif ", u"dgi's landsst�vne", u"skolernes motionsdag", "gymnastiktime", u"g� til gymnastik", "sportsklub", "gymnastikforening", "gymnastikforbund", "sportsklub", "fritidsaktivitet"]
integration=["integration", u"modersm�lsundervisning", u"l�re at tale dansk",  u"l�re dansk", u"mentornetv�rk", u"integrationsnetv�rk", u"indf�dsretspr�ven", "ghetto", "integrationsydelse", "integrere sig", "assimilation", "assimilere", "parallelsamfund"]
international_politik=[u"konvention", u" fn ", u"unicef", u"unhcr", u" nato ", u"europar�det", u"nordisk ministerr�d", u"nordisk r�d", u" osce ", u"verdenshandelsorganisationen", u" wto ","trump","putin","merkel","kansler",u"pr�sident","senatet",u"repr�sentanternes hus","theresa may","xi jinping","premierminister","diplomat","multilateralt samarbejde", "erdogan",]
international_sikkerhedspolitik=[u"international mission", u"konfliktforebygge", u"fredsbevarende", u" fsb ", u"masse�del�ggelsesv�ben", u"atomv�ben", u"v�benindustri", u"trafficking", u"menneskehandel", u"gr�nseoverskridende kriminalitet", u"pirateri", u"international cyberkriminalitet"]
internationalt_kultursamarbejde=[u"internationalt kultursamarbejde", u"kulturudveksling", u"det internationale kulturpanel", u"europ�isk kulturhovedstad", u"udvekslingsstud", u"kultureksport", u"interkulturel"]
islam=["islam", "koran", "allah", "profeten muhammed", "muslim", u"g� med t�rkl�de", "hijab", u"niqab", u"burka", u"fredagsb�n", "bede fem gange om dagen", " sunni", " shia", "ramadan", u"halal", "imam", "haram", " eid ", "minaret", "konvertit",]
kaeledyr=[ u"k�ledyr", "kamphund", "hundelov", "familiehund", "familie hund", "indekat", "udekat", "have hund", "have kat", "hundeejer", "katteejer", ]
klimaforandringer=[u"klimaforandring", u"co2-udledning", u"reduktionsm�l", u"drivhusgas", u"drivhuseffekt", u"ozonlag", u"energilovgivning", u"co2-kvote", u"klimaindsats", u"klimalov", u"klimar�d", "klimaaftal",]
koens_og_seksualnormer=[u"transk�n", u"homoseksuel", u"lesbisk",u"k�nsidentitet","lgbt",u"cisk�nnet","heteronormativ",u"k�nsnormativ",u"ikke-bin�r","regnbueflag",u"h�vnporno",u"n�genbillede","pride","homoparade","hate crime","hatecrime","mansplaining",u"voldt�gtskultur","sexarbejde","seksuelt samtykke","slutshaming", "slut shaming", "victimblaming","seksualiser","queer",u" b�sse", " lebbe "," svans ","ofrets skyld"]
kommuner_regioner=[" kl ", "danske regioner", "kommunal", "kommune", u"regionsloven", u"borgmester", u"regionsr�d", u"regionalt ansvarsomr�de", "praksissektor", u"regional�konomi", u"�konomi i region", u"regionernes �konomi", u"budgetsamarbejde", u"i udbud", u"konkurrenceuds�t", "udbudsomr�de", u"besk�ftigelsestilskud", "omprioriteringsbidrag"]
kongehuset=["kongehus", "kongelig", "dronning margrethe", "prins henrik", "kronprins", "kronprinsesse", "prins joachim", "prinsesse marie", "apanage", "kongeskibet", "kongepar", u"royalt bes�g", u"nyt�rstaffel", "royal begivenhed", "de royale"]
kontanthjaelp_dagpenge=[u"kontanthj�lp", "dagpenge","a-kasse", "optjeningsperiode", u"gensidig fors�rgerpligt", u"gensidig fors�rgelsespligt", u"uddannelseshj�lp", "225 timers reg", "225-timersreg", "udbetalingsseddel", "udbetalings seddel", u"underst�ttelse",]
kulturarv=[u"fredet bygning", "fredede bygninger", u"bevaringsv�rdi", "kulturarv", "kulturinstitution", "kulturkanon", "kulturhistorie", "fortidsfund", "klenodie", "verdensarv", "dansk tradition", "traditionsrig", "danske traditioner", u"ark�ologisk fund", u"folkebibliotek", u"l�ne b�ger", u" udl�n ", u"biblioteksv�sen", u"biblioteksafgift", u"centralbibliotek", u"rigsarkivet", u"stadsarkiv", u"arkivloven", u"danef�"]
kunst_museer=[u"kunstst�tte", "kunstmuseum", u"kunstfond", u"nationalmuseet", "glyptoteket", u"statens museum for kunst", u"kunststyrelsen", u"kunstr�det", u"museumsloven", "moderne kunst", u"s�rudstilling", u"museumsg�st", "kurator", "kunsthal", "installationskunst", u"kunstv�rk", "billedkunstner",]
landbrug=[u"landbrug", "landmand", u"landm�nd", u"bondemand", u"b�nder", u"ude p� marken", "konventionelt dyrk", "dyrket konventionelt", u"dyrket �kologisk", u"�kologisk dyrk", "dyrkningsmetode", u"g�dning", u"afgr�de", "bigballe", "kyllingefarm", "svinefarm", u"kv�gfarm", u"kv�gproduktion", "kostald", "malkerobot", "svineproduktion", ]
ligestilling_arbejdsmarked=[u"ligel�n", u"l�nskel", u"l�ngap", u"l�ngab", u"l�n gap", u"ligebehandlingslov", u"ligel�nslov", u"barseludligningslov", u"barsellov", u"mandejob", u"kvindejob", u"lige l�n for lige arbejde", "glasloft",]
ligestilling_repraesentation=[u"lige repr�sentation", u"underrepr�senteret", u"overrepr�senteret", u"repr�sentation af etniske minoriteter", "kvindedominere", "mandsdominere", u"kvinder i bestyrelse", u"kvinder i ledelse", "kvindelige chefer", "kvindelige topchefer", u"kvindekvote", u"k�nskvot", "kvinder i folketinget", u"kvinder i milit�ret",]
livsstil=["sund livsstil", "kostvane", u"madvane", u"overv�gtig", u"fedme", u"slankekur", u"motion", u"rygning", "cigaret", u"sm�ger", u"drikke alkohol", "alkoholforbrug", "genstande om ugen", u"euforiserende stoffer", u"narkotika", u"hash", u"alkoholmisbrug", "6 om dagen", "30 minutter om dagen", "sundhedsstyrelsen", "usund"]
medicin_bivirkninger=["medicin", "medicinsk behandling", "bivirkning", u"forebygge", u"smertestille", u"smertelindring", u"morfin", u"antibiotika", "penicillin", u"kemo", u"str�lebehandling", "immunterapi", "stamcellebehandling", u"pacemaker", u"vaccine", "vaccination", "cannabisolie", u"medicinsk cannabis", "cannabis", "dialyse", "p-pille", "transplantation", "alternativ behandling", "alternative behandlingsformer", "hpv", "akkupunktur", "zoneterapi", "hom�opati", "iboprofen", "antihistamin", "paratecemol", "panodil", " ipren", "sovepille", "lykkepille", "antidepressiv", "binyrebarkhormon", "interferon-beta", "copaxone", "eksperimentel behandling", "eksperimentelle behandlingsformer", "psykofarmaka", "hpv", u"m�sling"]
medier_sprog=[u"medielovgivning", u"trykte medier", u"digitale medier", u"public service", u"licens", u"dansk sprogn�vn","medielov","medivirksomhed","mediekoncern","mediebranche","tv-kanal","regionalprogram","nyhedskanal","nyhedsudsendelse","regionalnyhed","skrevne medier","aviser","public service","medielicens", "betale licens","licenspenge",u"dansk sprogn�vn","sprogpolitik","sprogbruger","retskrivning","retstavning",u"godkendt stavem�de","fremmedord","dialekt","nyt ord",u"l�neord","tegnsprog",u"tegns�tning","kommaregler","nyt komma"," slang ","slangord","det danske sprog","pendulord","produktionsselskab",]
meteorologi=[u"meterolog", u"vejrudsigt", " dmi ", u"vejrprognose", u"varsel om farligt vejr", u"stormvarsel", u"stormflodsvarsel", u"klimaoverv�gning", u"forskning i klimaforandringer", "byvejr","regionaludsigt","landsudsigt",u"glatf�re",u"femd�gnsprognose","vejrprognose","uv-index","uv index","uv-indeks","uv indeks"," dmi ","meteorolog", " sne ", "skybrud", "sommervejr"]
miljoe=[u"foruren", u"milj�venlig", u"t�nke p� milj�et", u"t�nk p� milj�et", u"godt for milj�et", u"passe p� milj�et", u"milj�svin", u"affaldsh�ndtering", "affaldssortering", "sortere affald", u"grundvand", "drikkevand", "spildevand", "genbrug af vand", u"luftkvalitet", u"kemikalier", u"milj�afgift", u"gr�n afgift", u"b�redygtig produktion", "jordbrugsforhold", u"vandmilj�",  u"havmilj�", u"milj�vurdering", u"milj�m�rket", u"milj�zone", u"milj�politik", u"milj�minister", u"milj�styrelse"]
musik=["symfoniorkest", "opera", " vega ", "musikskole", u"dr symfoniorkestret", u"dr big bandet", u"musikfestival", "roskilde festival", "smukfest", "northside festival", "langelandsfestival", "jazzfestival", "copenhell", "trailerpark festival", u"distortion i k�benhavn" u"musikkonservatorium",  u" koda ",  "spillested", "livemusik", "koncertsted", "spille et instrument", "spille p� et instrument", "musikundervisning", u"g� til musik", "spotify", u"h�re musik"]
national_sikkerhed=[u"politiets efterretningstjeneste", " pet ", u"national sikkerhed", "danmarks sikkerhed", "landets sikkerhed", "forsvarets efterretningstjeneste", " fe "]
natur_dyreliv=[u"naturbeskyt", "biodiversitet", "naturpakken", "danmarks naturfredningsforening", "naturindsats", "naturforvalt", "skovbrug", "skovdrift", "danmarks skove", "danmarks natur", "naturgenopretning", "skovlov", "nationalpark", "dyreliv", "beskyttede arter", "beskyttet dyr", "flora og fauna",]
offentlige_finanser=["2025-plan", u"velf�rdspulje", "helhedsplan", "investorfradrag", u"bankpakke", "su-system", " su ", u"su-l�n"]
pension=["pensionsalder", u"folkepension", u"pensionsopsparing", u"f�rtidspension", u"efterl�n", u"nedslidt", u"�ldrecheck", u"kapitalpension","pensionsselskab","pensionsregler","pensionsreform","aldersopsparing","ratepension",u"f�rtidspension",u"efterl�n","nedslidt",u"�ldrecheck","kapitalpension","forventet levetid"]
politi_kriminalitet=["betjent", "politi ", "patruljevogn", u"t�regas", u"kampkl�dt", "knippel", "narkohund", "ransag", "patruljering", "patruljevogn", u"afh�ring", u"hundef�rer", "europol", "kriminel", "gerningsmand", "indbrud", u"r�veri", "tiltalt", " efterforsk "]
politikerliv=[u"ministerpension", u"eftervederlag", "ministerbil", "ministertaburet", "personsag", "folketingskandidat", "folkevalgt", "spindoktor", "folketingsmedlem", "folketingskandidat", "politikerlede", u"l�ftebrud", ]
politisk_ideologi=[u"ideologi", u"socialist", u"kommunist", u"nationalist", "nazist", "nazisme", "socialisme", "kommunisme", "liberalisme", "konservatisme", "liberal tankegang",]
politisk_kommentator=["politisk kommentator", "politisk analyse", "hans engell", "mogensen og kristiansen", "jersild", "clement kj�rsgaard", ]
politisk_samarbejde= [u"st�tteparti", u"koalition", u"regeringssamarbejde", "regeringskrise", "intern splid", "partiformand", "statsministerkandidat", "forlig", "politisk samarbejde", "politisk alliance", "samarbejde over midten", "blokpolitik", "forligsparti", "forligskreds"]
postvaesen=[" post danmark ", " post dk ", u"postdanmark", "sender breve", u"postnord", u" porto ", u"frim�rk", u"pakkepost", u"track and trace", u"eposthuset", u"mobilporto", u"pakkeboks", u"modtagerflex", "postsektor"]
praktiserende_laeger=[u" egen l�ge ", "e-konsultation", "emailkonsultation", u"praktiserende l�ge", u"l�gepraksis", u"l�gesekret�r", u" l�geklinik", "kliniksygeplejerske", u"familiel�ge"]
privatoekonomi=[u"privat�konomi", u"kvikl�n", u"bill�n", u"sms-l�n", "skylde penge", "bruge penge", u"g�ldssanering", " rki ", " kreditkort", "f�lles�konomi", "madkonto", "inkasso", "mastercard", "dankort", u"indl�n", "opsparing", "l�n","konto"]
psykiske_lidelser=[u"spiseforstyrrelse", u"stress", u"adhd", u"autism", u"angst", u"terapi", u"psykofarmaka","psykisk lidelse","psykisk syg","sindslidelse", "sindslidende", "mental sundhed","spiseforstyrrelse", "anoreksi","bulimi","ortoreksi","overspisning","selvskade","cutter","selvmord","demens","dement","alzheimer","depression","skizofren","bipolar","manio-depressiv","depressiv","ocd","tvangstanke","tilknytningsforstyrrelse","tilpasningsforstyrrelse","posttraumatisk stress","autisme","angst","psykiatri","psykolog","psykiater","psykoterapi","samtaleterapi","skolepsykolog",u"milj�terapi","lykkepille",u"mentalunders�gelse"," ect ",u"tvangsindl�ggelse", "antidepressiv"]
retspolitik_justitsvaesen=["anklagemyn", "domstol", "byret", "strafferamme", u"h�rdere straffe", u"straffes med f�ngsel", u"f�ngselsstraf", u"b�destraf", u"id�m", "livstid", u"h�jesteret", "landsret", "bryde lov", "straffelov", "straffesag"]
scenekunst_litteratur=[u"det kongelige teater", "teaterfestival", "scenekunst", "operahus", "teaterscene", u"sk�nlitteratur", "samtidslitteratur", u"g� i teatret", "se teater", "teaterforestilling", u"l�se b�ger", u"l�ser b�ger", "arnold busck", "bog og ide", "boghandel", "bogmesse", "poesi", "bogudgivelse", "bogforlag", "gyldendal", "lindhart og ringhof", "lydbog", "e-bog", "e bog", u"e b�ger", u"e-b�ger", " kindle ",]
skatter_afgifter=["am bidrag", u"arbejdsmarkedsbidrag", u"b-indkomst", u"b-skat", u"a-indkomst", u"a-kort", u"frikort", u"restskat", u"penge tilbage i skat", u"selvangivelse", u"forskudsopg�relse", u"�rsopg�relse", u"selskabsskat", u"skattefradrag", u"boligskattefradrag", u"fradrag", u"told" ,u"moms", u"indkomstskat", u"skat p� arbejde", u"bundskat", u"topskat", u"grundskyld", "betale skat", "skat", u"boligskat", u"grundskyld", u"topskat", u"bundskat", u"moms", u"told", u"afgift", u"skattelettelse", u"skattely", " pso "]
socialt_udsatte=[u"socialt udsat", "samfundets svageste", "sociale problemer", u"udsatte b�rn", "udsatte unge", "udsatte familier", u"hjeml�s", u"leve p� gaden", u"bo p� gaden", u"g� fra hus og hjem", "misbruger","seksuelt misbrugt", "incest", "alkoholiker", u"fattige b�rn", "prostitueret", "voldsramt", u"v�rested", "herberg", "stofmisbrug", "fixerum", "sundhedsrum", "stofindtagelsesrum", "sexhandlede", "handlede kvinder", "omsorgssvigt", u"vanr�gt", u"b�rnehjem"]
sport=[" sport ", u" OL ", "olympisk", u"paralympiske lege", u" EM ", u" VM ", "doping", "matchfixing", "fodbold", u"h�ndbold", "tennis", "badminton", "gymnastik", "roning", "basketball", "volleyball", "atletik", "baseball", "ridning", " uefa ", "champions leage", "tour de france", "giro d'italia", "vuelta a espa�a", u"bjergtr�je", u"pointtr�je", u" den gule tr�je", "cykelsport", "elitesport", "team danmark", " fifa ", " uefa ", "wozniacki", "golden league", "mesterskab", "medalje", "pokal", "sportsarena", "sportshal", "squash", "nationalmelodi", " ehf ", " whf ", " wta ", "golf", "boksning"]
sundhed_etik=[u"d�dshj�lp", "organdonation", "rugemor", u"rugem�dre", "kunstig befrugtning", "cyborg", "kloning", "genteknologi", "stamcelle", "genmodificer", "surrogat", "fosterdiagnostik", u"designerb�rn", u"designer b�rn", "bioteknologi", "assisteret reproduktion", "cybergenetics", "cybergenetik", "dobbeltdonation", "embryo adoption",]
teknologi_hverdag=[u"mobilstr�ling", u"sk�rmforbrug", u"sk�rmtid", u"overv�gning", " wifi", "google maps", "tinder", " app ", " mac ", "profilbillede", u"p� nettet"]
teknologisk_udvikling=["teknologi", "algoritme",  "automatisering", "virtual reality", u"robot", u"selvk�r", u"f�rerl�s", "kunstig intelligens", "artificial intelligence", "augmented reality", "distruption", u"programm�r", "hack", "cyber security","cyber-sikkerhed","cyber-sikkerhed", "dark web", "3d-print","nanoteknologi","kvantecomputer"]
terror=[u"terror", "voldelig ekstremisme", "islamis", " isis ", "selvmords", u"bombeb�lte", "radikaliser", "ensom ulv"]
transport=[u"vejnet", u"storeb�lt", u"lilleb�lt", u"�resund", u"kollektiv trafik", u"offentlig transport", u"billetpris", u"takstzone", u"pendler", u"rejsekort", u"ungdomskort", u"  bus ", "togbus", u" tog ", u" metro ", u" taxa ", u"f�rge", u"banedanmark", " DSB ", "metroselskabet", " uber ", u"selvk�rende bil", u"storstr�msbro", "fehmern", "benzin", "diesel", " biler ", " bil ", "tankstation", "movia", "arriva"]
trepartsforhandlinger=["den danske model", "trepartsforhandlinger", u"trepartsaftale", u"dansk arbejdsgiverforening", u"fagbev�gelse", u"s�ttem�de", u"kommissorium", "septemberforlig", " LO ", "arbejdsgiverorganisation", u"l�nmodtager", "dansk arbejdsgiverforening", " DA ", u"l�nvilk�r", u"arbejdsvilk�r", ]
udenlandsk_arbejdskraft=["udenlandsk arbejdskraft", u"arbejdstilladelse", "fast-track-ordning", "greencard", "positivlisten", "au pair", "working holiday", u"�starbejd", u"gr�nseg�ng", u"�steurop�iske h�ndv�rkere", u"polske h�ndv�rkere", "social dumping", u"l�ndumping", u" uden overenskomst", u"mindstel�n", u"arbejdsmilj�lovgivning", u"udenlandske l�nmodtagere", u"indslusningsl�n", u"indslusningsl�n"]
udviklingspolitik=[u"udviklingspolitik", u"udviklingsbistand", u"udviklingssamarbejde", u"fattigdomsbek�mpelse", u"bek�mpelse af fattigdom", u"n�dhj�lp", u"humanit�r indsats", u"rettighedsbaseret arbejde", u"menneskerettigheder", "flygtningelejr", u"n�romr�de", "udviklingsprogram", "uland", "iland", "2015-m�l", "absolut fattigdom", "global ulighed", "Verdensbanken", " IBRD ", "demokratiprocesser", u"verdensm�l", "dkaid", u"st�t uland"]
ungdomsuddannelser=["ungdomsuddannelse" "gymnasial uddannelse", u"erhvervsskole", u"l�replads", "praktikplads", u"teknisk skole", u"handelsskole", u"landbrugsskole", u"social- og sundhedsuddannelse", u"sosu-uddannelse", u"produktionsskole", "stx", "htx", "hhx", " hf ", u"l�rling",]
vaekst_erhverv=[u"�konomisk v�kst", u"erhvervsliv", u"handelssektor", u" industri", u"import", u"eksport", u"turisme", u"konkurrencelovgivning", u"konkurrencedygtig", "virksomhed"]
vaernepligt=[u"v�rnepligt", u"v�rneret", u"milit�rn�gter", "indkaldelsesordre", "Forsvarets Dag", "tjenestested", "tjenestetid", "til session",]
valg_folkeafstemninger=["meningsm�ling", u"folketingsvalg", u"europaparlamentsvalg", u"kommunalvalg", u"regionsr�dsvalg", u"stemmeprocent", u"valgdeltagelse", "folkeafstemning", "valgkamp", "brevstem", "valgsted", "valgplakat", "udskrive valg", "udskriver valg", "valgtilforordnet", u"f�rstegangsv�lger", u"r�dt flertal", u"bl�t flertal", u"v�lgererkl�ring",]
videregaaende_uddannelser=[u"videreg�ende uddannelse", u"universitet", u"bacheloruddannelse", u"kandidatgrad", "kandidatuddannelse", u"masteruddannelse", u"professionsh�jskole", u"professionsbachelor", u"erhvervsakademi", u"kunstakademi", "arkitektskolen", "uddannelsesloft", u"s�ge merit", u"f� merit", "kvote 1", "kvote 2", "standby-plads", "skrive speciale", "specialekontrakt", "specialevejleder", "afhandling", " KU ", " Aau ", " dtu ", " RUC ", "campus", "akademik", "akademisk"]
yderomraader=[u"yderomr�der",u"udvikling af landdistrikter og �er","udkantsdanmark",u"byplanl�gning","udflytning af statslige arbejdspladser",u"�samfund", u"planlov","landdistrikt",u"den r�dne banan","regional udvikling","landsby",u"landomr�der",u"ude p� landet","lokalsamfund","yderkommune","udkantskommune"]

#==============================================================================
def dagsordener(self):
    self['aeldre']= self['Message'].str.contains('|'.join(map(re.escape,aeldre,)))
    self['andre_trossamfund']= self['Message'].str.contains('|'.join(map(re.escape,andre_trossamfund,)))
    self['arbejdsloeshed']= self['Message'].str.contains('|'.join(map(re.escape,arbejdsloeshed,)))
    self['arbejdsmiljoe']= self['Message'].str.contains('|'.join(map(re.escape,arbejdsmiljoe,)))
    self['barsel']= self['Message'].str.contains('|'.join(map(re.escape,barsel,)))
    self['boernepasning']= self['Message'].str.contains('|'.join(map(re.escape,boernepasning,)))
    self['byggeri_bolig']= self['Message'].str.contains('|'.join(map(re.escape,byggeri_bolig,)))
    self['danskhed_debat']= self['Message'].str.contains('|'.join(map(re.escape,danskhed_debat,)))
    self['digitalisering_off']= self['Message'].str.contains('|'.join(map(re.escape,digitalisering_off,)))
    self['diskrimination']= self['Message'].str.contains('|'.join(map(re.escape,diskrimination,)))
    self['efteruddannelse_opkvalificering']= self['Message'].str.contains('|'.join(map(re.escape,efteruddannelse_opkvalificering,)))
    self['energiforsyning']= self['Message'].str.contains('|'.join(map(re.escape,energiforsyning,)))
    self['eu']= self['Message'].str.contains('|'.join(map(re.escape,eu,)))
    self['faengsler']= self['Message'].str.contains('|'.join(map(re.escape,faengsler,)))
    self['familieliv']= self['Message'].str.contains('|'.join(map(re.escape,familieliv,)))
    self['feminisme']= self['Message'].str.contains('|'.join(map(re.escape,feminisme,)))
    self['fertilitet']= self['Message'].str.contains('|'.join(map(re.escape,fertilitet,)))
    self['film_tv']= self['Message'].str.contains('|'.join(map(re.escape,film_tv,)))
    self['finanslov']= self['Message'].str.contains('|'.join(map(re.escape,finanslov,)))
    self['finanssektor']= self['Message'].str.contains('|'.join(map(re.escape,finanssektor ,)))
    self['flygtninge']= self['Message'].str.contains('|'.join(map(re.escape,flygtninge,)))
    self['foedevarer']= self['Message'].str.contains('|'.join(map(re.escape,foedevarer,)))
    self['folkekirken_kristendom']= self['Message'].str.contains('|'.join(map(re.escape,folkekirken_kristendom,)))
    self['folkeskole']= self['Message'].str.contains('|'.join(map(re.escape,folkeskole,)))
    self['forbrug_kemi']= self['Message'].str.contains('|'.join(map(re.escape,forbrug_kemi,)))
    self['forskning']= self['Message'].str.contains('|'.join(map(re.escape,forskning,)))
    self['forskning_sygdomme']= self['Message'].str.contains('|'.join(map(re.escape,forskning_sygdomme,)))
    self['forsvaret']= self['Message'].str.contains('|'.join(map(re.escape,forsvaret,)))
    self['fysiske_sygdomme']= self['Message'].str.contains('|'.join(map(re.escape,fysiske_sygdomme,)))
    self['handelspolitik_udenrigsoekonomi']= self['Message'].str.contains('|'.join(map(re.escape,handelspolitik_udenrigsoekonomi,)))
    self['handicap']= self['Message'].str.contains('|'.join(map(re.escape,handicap,)))
    self['hospitalsvaesen']= self['Message'].str.contains('|'.join(map(re.escape,hospitalsvaesen,)))
    self['idraetsliv']= self['Message'].str.contains('|'.join(map(re.escape,idraetsliv,)))
    self['integration']= self['Message'].str.contains('|'.join(map(re.escape,integration,)))
    self['international_politik']= self['Message'].str.contains('|'.join(map(re.escape,international_politik,)))
    self['international_sikkerhedspolitik']= self['Message'].str.contains('|'.join(map(re.escape,international_sikkerhedspolitik,)))
    self['internationalt_kultursamarbejde']= self['Message'].str.contains('|'.join(map(re.escape,internationalt_kultursamarbejde,)))
    self['islam']= self['Message'].str.contains('|'.join(map(re.escape,islam,)))
    self['kaeledyr']= self['Message'].str.contains('|'.join(map(re.escape,kaeledyr,)))
    self['klimaforandringer']= self['Message'].str.contains('|'.join(map(re.escape,klimaforandringer,)))
    self['koens_og_seksualnormer']= self['Message'].str.contains('|'.join(map(re.escape,koens_og_seksualnormer,)))
    self['kommuner_regioner']= self['Message'].str.contains('|'.join(map(re.escape,kommuner_regioner,)))
    self['kongehuset']= self['Message'].str.contains('|'.join(map(re.escape,kongehuset,)))
    self['kontanthjaelp_dagpenge']= self['Message'].str.contains('|'.join(map(re.escape,kontanthjaelp_dagpenge,)))
    self['kulturarv']= self['Message'].str.contains('|'.join(map(re.escape,kulturarv,)))
    self['kunst_museer']= self['Message'].str.contains('|'.join(map(re.escape,kunst_museer,)))
    self['landbrug']= self['Message'].str.contains('|'.join(map(re.escape,landbrug,)))
    self['ligestilling_arbejdsmarked']= self['Message'].str.contains('|'.join(map(re.escape,ligestilling_arbejdsmarked,)))
    self['ligestilling_repraesentation']= self['Message'].str.contains('|'.join(map(re.escape,ligestilling_repraesentation,)))
    self['livsstil']= self['Message'].str.contains('|'.join(map(re.escape,livsstil,)))
    self['medicin_bivirkninger']= self['Message'].str.contains('|'.join(map(re.escape,medicin_bivirkninger,)))
    self['medier_sprog']= self['Message'].str.contains('|'.join(map(re.escape,medier_sprog,)))
    self['meteorologi']= self['Message'].str.contains('|'.join(map(re.escape,meteorologi,)))
    self['miljoe']= self['Message'].str.contains('|'.join(map(re.escape,miljoe,)))
    self['musik']= self['Message'].str.contains('|'.join(map(re.escape,musik,)))
    self['national_sikkerhed']= self['Message'].str.contains('|'.join(map(re.escape,national_sikkerhed,)))
    self['natur_dyreliv']= self['Message'].str.contains('|'.join(map(re.escape,natur_dyreliv,)))
    self['offentlige_finanser']= self['Message'].str.contains('|'.join(map(re.escape,offentlige_finanser,)))
    self['pension']= self['Message'].str.contains('|'.join(map(re.escape,pension,)))
    self['politi_kriminalitet']= self['Message'].str.contains('|'.join(map(re.escape,politi_kriminalitet,)))
    self['politikerliv']= self['Message'].str.contains('|'.join(map(re.escape,politikerliv,)))
    self['politisk_ideologi']= self['Message'].str.contains('|'.join(map(re.escape,politisk_ideologi,)))
    self['politisk_kommentator']= self['Message'].str.contains('|'.join(map(re.escape,politisk_kommentator,)))
    self['politisk_samarbejde']= self['Message'].str.contains('|'.join(map(re.escape,politisk_samarbejde,)))
    self['postvaesen']= self['Message'].str.contains('|'.join(map(re.escape,postvaesen,)))
    self['praktiserende_laeger']= self['Message'].str.contains('|'.join(map(re.escape,praktiserende_laeger,)))
    self['privatoekonomi']= self['Message'].str.contains('|'.join(map(re.escape,privatoekonomi,)))
    self['psykiske_lidelser']= self['Message'].str.contains('|'.join(map(re.escape,psykiske_lidelser,)))
    self['retspolitik_justitsvaesen']= self['Message'].str.contains('|'.join(map(re.escape,retspolitik_justitsvaesen,)))
    self['scenekunst_litteratur']= self['Message'].str.contains('|'.join(map(re.escape,scenekunst_litteratur,)))
    self['skatter_afgifter']= self['Message'].str.contains('|'.join(map(re.escape,skatter_afgifter,)))
    self['socialt_udsatte']= self['Message'].str.contains('|'.join(map(re.escape,socialt_udsatte,)))
    self['sport']= self['Message'].str.contains('|'.join(map(re.escape,sport,)))
    self['sundhed_etik']= self['Message'].str.contains('|'.join(map(re.escape,sundhed_etik,)))
    self['teknologi_hverdag']= self['Message'].str.contains('|'.join(map(re.escape,teknologi_hverdag,)))
    self['teknologisk_udvikling']= self['Message'].str.contains('|'.join(map(re.escape,teknologisk_udvikling,)))
    self['terror']= self['Message'].str.contains('|'.join(map(re.escape,terror,)))
    self['transport']= self['Message'].str.contains('|'.join(map(re.escape,transport,)))
    self['trepartsforhandlinger']= self['Message'].str.contains('|'.join(map(re.escape,trepartsforhandlinger,)))
    self['udenlandsk_arbejdskraft']= self['Message'].str.contains('|'.join(map(re.escape,udenlandsk_arbejdskraft,)))
    self['udviklingspolitik']= self['Message'].str.contains('|'.join(map(re.escape,udviklingspolitik,)))
    self['ungdomsuddannelser']= self['Message'].str.contains('|'.join(map(re.escape,ungdomsuddannelser,)))
    self['vaekst_erhverv']= self['Message'].str.contains('|'.join(map(re.escape,vaekst_erhverv,)))
    self['vaernepligt']= self['Message'].str.contains('|'.join(map(re.escape,vaernepligt,)))
    self['valg_folkeafstemninger']= self['Message'].str.contains('|'.join(map(re.escape,valg_folkeafstemninger,)))
    self['videregaaende_uddannelser']= self['Message'].str.contains('|'.join(map(re.escape,videregaaende_uddannelser,)))
    self['yderomraader']= self['Message'].str.contains('|'.join(map(re.escape,yderomraader,)))
#   midlertidig tilf�jelse til banker
#     self['ferie']= self['Message'].str.contains('|'.join(map(re.escape,ferie,)))
#     self['it_sikkerhed']= self['Message'].str.contains('|'.join(map(re.escape,it_sikkerhed,)))
#     self['betalingskort']= self['Message'].str.contains('|'.join(map(re.escape,betalingskort,)))
#     self['mobilepay']= self['Message'].str.contains('|'.join(map(re.escape,mobilepay,)))
#     self['konkurrence']= self['Message'].str.contains('|'.join(map(re.escape,konkurrence,)))
    return self


#==============================================================================


#Replace this with your own working directoy
path =r'/Users/nextwork/Dropbox/PycharmProjects/topics/'

##Function that outputs excel file with bool value for each row, at each label
def quant_analyzer(path):
    all_files = glob.glob\
        (os.path.join(path, "input/*.xlsx"))# advisable to use os.path.join as this makes concatenation OS independent
    for f in all_files:
        name = os.path.basename(f)
        df = pd.read_excel(f)
        dagsordener(df)
        #converts bools to numbers
        df_num=df.loc[:, 'aeldre':'yderomraader'].applymap\
            (lambda x: 1 if x else 0)
        temp = df_num.combine_first(df)
        #temp.loc['Total']= temp.sum()
        #temp=temp.dropna()
        return temp.to_excel(path + "output/out_" + name)

#Executes quant_analyzer
quant_analyzer(path)



