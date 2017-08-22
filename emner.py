# -*- coding: latin-1 -*-
"""
Functions for sorting Facebook text data into topics
@Author: Michael Jensen, Louise Schiøtt
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
aeldre=[u"ældrepleje", u"de ældre", u"ældre mennesker", "hjemmepleje", u"hjemmehjælp", "sosu ", "plejepersonale", u"plejecenter",u"ældrebolig","alderdom", u"varme hænder", u"ældreområde", u"ældreminist"]
andre_trossamfund=[u"trossamfund", "trosretning", u"vielsesbemyndig", u"begravelsespladser", u"religionsfrihed", "frikirke", "katolik", "pave", "rabbiner","synagoge", "hindu", "buddhis", " munk", "scientology", " sekt "]
arbejdsloeshed=[u"arbejdsløs", u"gå ledig", "ledighed", "langtidsledig", "lediggang", u"i beskæftigelse", "arbejdsformidling", "jobrettet", u"jobsøgning", u"søge job", u"søge arbejde", u"arbejdssøgende", "finde arbejde", "finde et arbejde", "finde job", "finde et job", u"fleksjob", u"jobcenter", u"beskæftigelsesindsats", u"virksomhedspraktik", u"løntilskud", u"ressourceforløb", u"seniorjob", "arbejdsmarkedsparat", "aktivering", u"jobsøgningskursus", ]
arbejdsmiljoe=[u"arbejdsmiljø", u"arbejdsglæde", "trivsel på arbejdspladsen", u"trivselsmåling", u"trivselsundersøgelse", "arbejdstilsyn", u"mobning på arbejdspladsen", u"voksenmobning", u"arbejdsstilling", u"arbejdsskade", u"arbejdsulykke", u"erhvervssygdom", " APV ", "arbejdspladsvurdering", "hviletid", u"køre hvile tid", u"køre/hvile-tid", u"kørehviletid", "11-timersreglen", "11 timers reglen", "11-timers reglen", "hvileperiode", u"fridøgn", u"sygefravær", "arbejdsforhold",]
barsel=["barsel", u"forældreorlov", "graviditetsorlov", u"fædreorlov", "adoptionsorlov", u"mødregruppe"]
boernepasning=["dagpleje", u"daginstitution", u"vuggestue", u"børnehave", u"skovbørnehave", u"integreret institution", u"privat børnehave", u"privat vuggestue", u"pladsanvisning", u"pasningsgaranti", u"pædagog", u"normering", "fritidshjem", u" sfo ", u"ungdomsklub"]
byggeri_bolig=[u"statslige ejendomme", u"regulering af byggebranchen", u"offentligt byggeri", u"almenbolig", u"boligselskab", u"lejeloven", u"ungdomsbolig", u"ældrebolig", u"andelsbolig", u"ejerbolig", u"boligstøtte", "boligydelse", "boligpakke", "boliglov", u"boligområde", "boligforhold", "studiebolig", "boligmangel", "mangel på boliger","bolig"," hus "]
danskhed_debat=["danskhed", "udansk", u"at være dansk", u"danske værdier", u"dansk værdi", u"indfødsretsprøve", "ikke-vestlig indflydelse", "national identitet", "islamisering", "nationalret", "national ret", "nationaldyr"]
digitalisering_off=[u"digitaliseringsstrategi", u"digital handlingsplan", u"datasikkerhed", u"it-sikkerhed", u"it-arkitektur", u"digital omstilling", u"digital signatur", u"nemid", u"nemkonto", u"nemsms", u"digital post", u"e-boks", "datafordeler"]
diskrimination=["diskrimin", "racis", "fremmedfjendsk", "fremmedhad", u"forskelsbehandling", u"institut for menneskerettigheder", u"hadforbrydelse", "sexis", "kønsdiskrimin", "kvindeundertryk", "islamofob", u"hadprædikant", "homofob", "perker"]
efteruddannelse_opkvalificering=["efteruddan", u"opkvalificering", u"diplomuddannelse", u" mba ", u"mini-mba", u"veu-godtgørelse", " amu ", "voksenuddannelse", "akademiuddannelse", "realkompetencevurder", u"åbent universitet", ]
energiforsyning=[u"energiforsyn", "energiressource", "energiresurse", "energireserve", "energiudvind", u"energianlæg", u"råstof", u"energisystem", u"elforsyning", u"elværk", u"elanlæg", u"gasforsyning", u"vandforsyning", u"fossile brænds", "oliefyr", u"vedvarende energi", u"grøn energi", u"bæredygtig energi", u"biobrændsel", "biogas", u"vindenergi", u"vindmølle", u"solenergi", u"solcelle", "geotermi", "varmepumpe", "biogas", u"olieudvinding", u"boreplatform", u"gasudvinding", "elforbrug", u"strømafbrydelse", u"strømsvigt", "bore efter olie",]
eu=[" eu ", u"europa-parlamentet", u"det europæiske råd", u"europa-kommissionen", u"ministerrådet", u"rådet for den europæiske union", u"eu-domstol", u"  eøs ", u"  edps ", u"europol", u"csdp", u"fælles møntfod", u"  euro ", u"retsforbehold", u"eu-kommissær", "kommitologi", "brexit", u"miste suverænitet", u"mister suverænitet", u"afgive suverænitet", u"afgiver suverænitet", "danske forbehold", "danmarks forbehold"]
faengsler=[u"fængsler", u"i fængsel", u"fængselsbetjent", "kriminalforsorg", "de indsatte", u"fængselscelle", u"prøveløsladt",]
familieliv=["familieliv", u"børnefamilie", "storfamilie", u"ægteskab", u"skilsmisse", u"forældremyndighed", u"statsamt", u"faderskab", u"adoption", u"regnbuefamilie" , u"familieform", u"være forældre", "juridisk abort", u"børnebidrag", "medmor", u"forældrelovsdirektiv", "barnets tarv", u"være mor", u"være far", "blive mor", "blive far", u"blive forældre",]
feminisme=["feminist", "feminisme", u"førstebølge", u"andenbølge", u"tredjebølge", u"fjerdebølge", "kvindekamp", u"rødstrømpe", "international kampdag", "kvindernes internationale kampdag", "patriarkat", u"kvindebevægelse", "kvinfo"]
fertilitet=["fertil", u" fødsel ", u"gravid", u"prævention", u"barnløs", u"sæddonor", u"ægdonor", u"donorsæd", u"donoræg", u"sætte æg op", "insemination", "inseminere", "reagensglasbarn", "reagensglasbehandling", " IVFI ", " ICSI ", "endometriose", u"sædkvalitet", "abort"]
film_tv=[u"filmskole", "cannes", "oscar-uddeling", "oscar uddeling", "oscars", "golden globe", "susanne bier", "von trier", "dox", "pix", "sundance", "thomas vinterberg", "filminstitut", "filmfestival", "filmkunst", "biografkultur", u"gå i biografen", "filmproduktion", "filmkultur", "filmpremiere", "biografpremiere", "spillefilm", "dokumentarfilm", "tv-program", "tv program", "se tv", "se fjernsyn", "program i fjernsynet", "flow-tv", "flow tv", "streame tv", "streame film", "streaming-tjeneste", "streaming tjeneste", "netflix", " hbo ", "viaplay", "dr tv", "tv2 play"]
finanslov=["finanslov", u"statslige udgifter", "finanspolitiske prioriteringer", "statens budget", u"statsbudget", u"økonomiaftale", "statens udgifter", "tillægsbevilling", "budgetvejledningen",]
finanssektor =["finanskrise", u"finanssektor", u"kapital", u"cashflow", u"invester", u"aktie", u"obligation", u" åop ", u" kreditvurdering ", u"nationalrente", u"renters rente", u"lånetype", u"egenkapital", u"kapitalrunde"]
flygtninge=[u"flygtning", "asyl", "flygte fra krig", "flygter fra krig", u"mennesker på flugt", "teltlejre", "sandholmlejr", "internt fordrevn", "modtagelsescent", "udrejsecent", ]
foedevarer=[u"økologi", u"konventionelle fødevarer", u"buræg", u"fritgående", "etisk forbrug", "forbrugsetik", "bevidst forbruger", u"bæredygtige fødevarer", u"dyrevelfærd", "fairtrade", "supermarked", "glutenfri", "laktosefri", u"kødfri", u"mindre kød", "vegetar", "vegan", u"fødevarepris", "madspild", "dagligvare", "egnsret", "spisevaner", "madtrend", "lokalt produceret", u"indkøbspose", u"købe ind", "forbrugskultur", u"råvare", ]
folkekirken_kristendom=["folkekirke", "statskirke", "kirkeminister", "gudstjeneste", "kirkelig", u"kirkeskat", u" sogn", u"barnedåb", u"konfirmation", u"vielse", "kirkebryllup", u"begravelse", u"præst", u"biskop", "menighed", u"gå i kirke", u"går i kirke", "kristen", "kristne",]
folkeskole=["folkeskole", "grundskole", u"privatskole", u"friskole", u"efterskole", u"specialskole", u"kostskole", u"undervisningspligt", u"folkeskolereform", u"klassekvotient", u"pisa-test", u"skolelærer", u"lærermangel", "skoledag", u"lektiehjælp", "skolebibliotek", "indskoling", "udskoling", "klassetrin", "elevplan", u"afgangsprøve", "skolebestyrelse", "skole-hjem-samtale"]
forbrug_kemi=[u"svanemærket", "eu-blomsten", u"miljømærket", "kemiindhold", "flourerede stoffer", "bisphenol", "ftalater", "phtalater", "mikroplast", "tungmetal", "skadelige stoffer", "hormonforstyrrende", u"kræftfremkaldende", "parabene", "parfumestof", "allergifremkaldende", u"tilsætningsstof", "konserveringsmid", "e-numre", " mi ", " pcb ", "triclosan", "kontaktallergi", "hverdagskemi"]
forskning=[" forsker ", " forskning ", u"videnskabelig undersøgelse", u"forskningskroner", u"forskningsmidler", u"forskningsbevilling", u"grundforskning", u"basisbevilling"]
forskning_sygdomme=[u"kræftforskning", u"hjerneforskning", "hjerneforsker", u"kræftforsker", "gigtforsker", "gigtforskning", "forskning i gigt", "forskning i sygdomme", "medicinsk forskning", u"forskning i mænds helbred", u"forskning i kvinders helbred", "hjerteforsker", "hjerteforskning", "forskning i hjertekarsygdomme", "forske i sygdom", "forskning i sukkersyge", "forskning i diabetes", "forskning i psykiske lidelser", "forskning i psykiatri", "forskning i demens", "forskning i alzheimerz"]
forsvaret=[u"forsvaret", u"forsvarskommando", u"hjemmeværn", u"beredskabsstyrelsen", u"forsvarets efterretningstjeneste", u"hæren", "forsvarskommando", "soldater", u"flyvevåbnet", "hangarskib", u"søværnet", "redningshelikopter", "kampfly", "f-16", "kaserne", "kampvogn", u"pansret køretøj", u"bæltekøretøj", u"flåden", u"militær", "rullemarie", "fregat", "arktisk kommando", "forsvarsakademiet", u"støjportal", "blive soldat", u"være soldat"]
fysiske_sygdomme=[u" kræft ", u"kræftpatient", u"kræftdiagnose", u"kræftsygdom", u"kræftramt", " cancer ", u"sklerose", u" gigt", "hjertesyg", "hjertekarsygdom", "hjerte-kar-sygdom", "hjerte kar sygdom", "muskelsvind", u"influenza", u"blodprop", u"forkøle", u"allergi", " astma ", u"hjertestop", u"kronisk syg", "kroniske smerter", "progeria", " MRSA ", "meningitis", u"kønssygdom", "klamydia", "gonore", "HPV", " HIV ", " Aids ", " KOL ", "rygerlunger", "diabetes", "sukkersyge", "apopleksi", "leversyg", "nyresyg", "blodsyg", "infektion", "epidemi", "pandemi", "svulst", "tumor", "terminalpatient", u"migræne", "ondt i ryggen", "ondt i nakken", "rygsmerter", "nakkesmerte", u"piskesmæld", "diskosprolaps"]
handelspolitik_udenrigsoekonomi=[u"handelspolitik", u"udenrigsøkonomi", " ttip ", "toldbarriere", u"frihandel", u"samhandel", u"import", u"eksport", u"handelsbalance", u"protektionisme", u"handelsliberalisering", u"investeringsbeskyttelse", u"global økonomi", u"konkurrenceevne", u"verdensbanken", u"udviklingsland", u"briks", u"grænseøkonomi"]
handicap=["handicap", "invalid", u"førlighed", u"bevægelseshæmmet", u"kørestol", "rullestol", u"funktionsnedsættelse", u"udviklingshæmmet", u"hjerneskade", u"specialområdet", u"tilgængelighedsregler", u"tilgængelighedsdirektiv", " downs syndrom", "diskriminationsforbud", "nedsat syn", u"nedsat hørelse", u"hørehæm", u"høreneds", "spastiker", "spastisk lamme", "svagtsyn",  "blindesamfund", u"døvstum", u"døvblind", "ordblind", "dysleksi", "tegnsprog", ]
hospitalsvaesen=["hospital", u"sygehus", u"patient", u"privathospital", u"supersygehus", u"ambulance", u"overbelægning", u"operation", "ligger på gangene", "kirurg", u"overlæge", u"narkoselæge", u"kræftlæge", "onkolog", "sygeplejerske"]
idraetsliv=[u"idræt", u"  dgi ", " dif ", u"dgi's landsstævne", u"skolernes motionsdag", "gymnastiktime", u"gå til gymnastik", "sportsklub", "gymnastikforening", "gymnastikforbund", "sportsklub", "fritidsaktivitet"]
integration=["integration", u"modersmålsundervisning", u"lære at tale dansk",  u"lære dansk", u"mentornetværk", u"integrationsnetværk", u"indfødsretsprøven", "ghetto", "integrationsydelse", "integrere sig", "assimilation", "assimilere", "parallelsamfund"]
international_politik=[u"konvention", u" fn ", u"unicef", u"unhcr", u" nato ", u"europarådet", u"nordisk ministerråd", u"nordisk råd", u" osce ", u"verdenshandelsorganisationen", u" wto ","trump","putin","merkel","kansler",u"præsident","senatet",u"repræsentanternes hus","theresa may","xi jinping","premierminister","diplomat","multilateralt samarbejde", "erdogan",]
international_sikkerhedspolitik=[u"international mission", u"konfliktforebygge", u"fredsbevarende", u" fsb ", u"masseødelæggelsesvåben", u"atomvåben", u"våbenindustri", u"trafficking", u"menneskehandel", u"grænseoverskridende kriminalitet", u"pirateri", u"international cyberkriminalitet"]
internationalt_kultursamarbejde=[u"internationalt kultursamarbejde", u"kulturudveksling", u"det internationale kulturpanel", u"europæisk kulturhovedstad", u"udvekslingsstud", u"kultureksport", u"interkulturel"]
islam=["islam", "koran", "allah", "profeten muhammed", "muslim", u"gå med tørklæde", "hijab", u"niqab", u"burka", u"fredagsbøn", "bede fem gange om dagen", " sunni", " shia", "ramadan", u"halal", "imam", "haram", " eid ", "minaret", "konvertit",]
kaeledyr=[ u"kæledyr", "kamphund", "hundelov", "familiehund", "familie hund", "indekat", "udekat", "have hund", "have kat", "hundeejer", "katteejer", ]
klimaforandringer=[u"klimaforandring", u"co2-udledning", u"reduktionsmål", u"drivhusgas", u"drivhuseffekt", u"ozonlag", u"energilovgivning", u"co2-kvote", u"klimaindsats", u"klimalov", u"klimaråd", "klimaaftal",]
koens_og_seksualnormer=[u"transkøn", u"homoseksuel", u"lesbisk",u"kønsidentitet","lgbt",u"ciskønnet","heteronormativ",u"kønsnormativ",u"ikke-binær","regnbueflag",u"hævnporno",u"nøgenbillede","pride","homoparade","hate crime","hatecrime","mansplaining",u"voldtægtskultur","sexarbejde","seksuelt samtykke","slutshaming", "slut shaming", "victimblaming","seksualiser","queer",u" bøsse", " lebbe "," svans ","ofrets skyld"]
kommuner_regioner=[" kl ", "danske regioner", "kommunal", "kommune", u"regionsloven", u"borgmester", u"regionsråd", u"regionalt ansvarsområde", "praksissektor", u"regionaløkonomi", u"økonomi i region", u"regionernes økonomi", u"budgetsamarbejde", u"i udbud", u"konkurrenceudsæt", "udbudsområde", u"beskæftigelsestilskud", "omprioriteringsbidrag"]
kongehuset=["kongehus", "kongelig", "dronning margrethe", "prins henrik", "kronprins", "kronprinsesse", "prins joachim", "prinsesse marie", "apanage", "kongeskibet", "kongepar", u"royalt besøg", u"nytårstaffel", "royal begivenhed", "de royale"]
kontanthjaelp_dagpenge=[u"kontanthjælp", "dagpenge","a-kasse", "optjeningsperiode", u"gensidig forsørgerpligt", u"gensidig forsørgelsespligt", u"uddannelseshjælp", "225 timers reg", "225-timersreg", "udbetalingsseddel", "udbetalings seddel", u"understøttelse",]
kulturarv=[u"fredet bygning", "fredede bygninger", u"bevaringsværdi", "kulturarv", "kulturinstitution", "kulturkanon", "kulturhistorie", "fortidsfund", "klenodie", "verdensarv", "dansk tradition", "traditionsrig", "danske traditioner", u"arkæologisk fund", u"folkebibliotek", u"låne bøger", u" udlån ", u"biblioteksvæsen", u"biblioteksafgift", u"centralbibliotek", u"rigsarkivet", u"stadsarkiv", u"arkivloven", u"danefæ"]
kunst_museer=[u"kunststøtte", "kunstmuseum", u"kunstfond", u"nationalmuseet", "glyptoteket", u"statens museum for kunst", u"kunststyrelsen", u"kunstrådet", u"museumsloven", "moderne kunst", u"særudstilling", u"museumsgæst", "kurator", "kunsthal", "installationskunst", u"kunstværk", "billedkunstner",]
landbrug=[u"landbrug", "landmand", u"landmænd", u"bondemand", u"bønder", u"ude på marken", "konventionelt dyrk", "dyrket konventionelt", u"dyrket økologisk", u"økologisk dyrk", "dyrkningsmetode", u"gødning", u"afgrøde", "bigballe", "kyllingefarm", "svinefarm", u"kvægfarm", u"kvægproduktion", "kostald", "malkerobot", "svineproduktion", ]
ligestilling_arbejdsmarked=[u"ligeløn", u"lønskel", u"løngap", u"løngab", u"løn gap", u"ligebehandlingslov", u"ligelønslov", u"barseludligningslov", u"barsellov", u"mandejob", u"kvindejob", u"lige løn for lige arbejde", "glasloft",]
ligestilling_repraesentation=[u"lige repræsentation", u"underrepræsenteret", u"overrepræsenteret", u"repræsentation af etniske minoriteter", "kvindedominere", "mandsdominere", u"kvinder i bestyrelse", u"kvinder i ledelse", "kvindelige chefer", "kvindelige topchefer", u"kvindekvote", u"kønskvot", "kvinder i folketinget", u"kvinder i militæret",]
livsstil=["sund livsstil", "kostvane", u"madvane", u"overvægtig", u"fedme", u"slankekur", u"motion", u"rygning", "cigaret", u"smøger", u"drikke alkohol", "alkoholforbrug", "genstande om ugen", u"euforiserende stoffer", u"narkotika", u"hash", u"alkoholmisbrug", "6 om dagen", "30 minutter om dagen", "sundhedsstyrelsen", "usund"]
medicin_bivirkninger=["medicin", "medicinsk behandling", "bivirkning", u"forebygge", u"smertestille", u"smertelindring", u"morfin", u"antibiotika", "penicillin", u"kemo", u"strålebehandling", "immunterapi", "stamcellebehandling", u"pacemaker", u"vaccine", "vaccination", "cannabisolie", u"medicinsk cannabis", "cannabis", "dialyse", "p-pille", "transplantation", "alternativ behandling", "alternative behandlingsformer", "hpv", "akkupunktur", "zoneterapi", "homøopati", "iboprofen", "antihistamin", "paratecemol", "panodil", " ipren", "sovepille", "lykkepille", "antidepressiv", "binyrebarkhormon", "interferon-beta", "copaxone", "eksperimentel behandling", "eksperimentelle behandlingsformer", "psykofarmaka", "hpv", u"mæsling"]
medier_sprog=[u"medielovgivning", u"trykte medier", u"digitale medier", u"public service", u"licens", u"dansk sprognævn","medielov","medivirksomhed","mediekoncern","mediebranche","tv-kanal","regionalprogram","nyhedskanal","nyhedsudsendelse","regionalnyhed","skrevne medier","aviser","public service","medielicens", "betale licens","licenspenge",u"dansk sprognævn","sprogpolitik","sprogbruger","retskrivning","retstavning",u"godkendt stavemåde","fremmedord","dialekt","nyt ord",u"låneord","tegnsprog",u"tegnsætning","kommaregler","nyt komma"," slang ","slangord","det danske sprog","pendulord","produktionsselskab",]
meteorologi=[u"meterolog", u"vejrudsigt", " dmi ", u"vejrprognose", u"varsel om farligt vejr", u"stormvarsel", u"stormflodsvarsel", u"klimaovervågning", u"forskning i klimaforandringer", "byvejr","regionaludsigt","landsudsigt",u"glatføre",u"femdøgnsprognose","vejrprognose","uv-index","uv index","uv-indeks","uv indeks"," dmi ","meteorolog", " sne ", "skybrud", "sommervejr"]
miljoe=[u"foruren", u"miljøvenlig", u"tænke på miljøet", u"tænk på miljøet", u"godt for miljøet", u"passe på miljøet", u"miljøsvin", u"affaldshåndtering", "affaldssortering", "sortere affald", u"grundvand", "drikkevand", "spildevand", "genbrug af vand", u"luftkvalitet", u"kemikalier", u"miljøafgift", u"grøn afgift", u"bæredygtig produktion", "jordbrugsforhold", u"vandmiljø",  u"havmiljø", u"miljøvurdering", u"miljømærket", u"miljøzone", u"miljøpolitik", u"miljøminister", u"miljøstyrelse"]
musik=["symfoniorkest", "opera", " vega ", "musikskole", u"dr symfoniorkestret", u"dr big bandet", u"musikfestival", "roskilde festival", "smukfest", "northside festival", "langelandsfestival", "jazzfestival", "copenhell", "trailerpark festival", u"distortion i københavn" u"musikkonservatorium",  u" koda ",  "spillested", "livemusik", "koncertsted", "spille et instrument", "spille på et instrument", "musikundervisning", u"gå til musik", "spotify", u"høre musik"]
national_sikkerhed=[u"politiets efterretningstjeneste", " pet ", u"national sikkerhed", "danmarks sikkerhed", "landets sikkerhed", "forsvarets efterretningstjeneste", " fe "]
natur_dyreliv=[u"naturbeskyt", "biodiversitet", "naturpakken", "danmarks naturfredningsforening", "naturindsats", "naturforvalt", "skovbrug", "skovdrift", "danmarks skove", "danmarks natur", "naturgenopretning", "skovlov", "nationalpark", "dyreliv", "beskyttede arter", "beskyttet dyr", "flora og fauna",]
offentlige_finanser=["2025-plan", u"velfærdspulje", "helhedsplan", "investorfradrag", u"bankpakke", "su-system", " su ", u"su-lån"]
pension=["pensionsalder", u"folkepension", u"pensionsopsparing", u"førtidspension", u"efterløn", u"nedslidt", u"ældrecheck", u"kapitalpension","pensionsselskab","pensionsregler","pensionsreform","aldersopsparing","ratepension",u"førtidspension",u"efterløn","nedslidt",u"ældrecheck","kapitalpension","forventet levetid"]
politi_kriminalitet=["betjent", "politi ", "patruljevogn", u"tåregas", u"kampklædt", "knippel", "narkohund", "ransag", "patruljering", "patruljevogn", u"afhøring", u"hundefører", "europol", "kriminel", "gerningsmand", "indbrud", u"røveri", "tiltalt", " efterforsk "]
politikerliv=[u"ministerpension", u"eftervederlag", "ministerbil", "ministertaburet", "personsag", "folketingskandidat", "folkevalgt", "spindoktor", "folketingsmedlem", "folketingskandidat", "politikerlede", u"løftebrud", ]
politisk_ideologi=[u"ideologi", u"socialist", u"kommunist", u"nationalist", "nazist", "nazisme", "socialisme", "kommunisme", "liberalisme", "konservatisme", "liberal tankegang",]
politisk_kommentator=["politisk kommentator", "politisk analyse", "hans engell", "mogensen og kristiansen", "jersild", "clement kjærsgaard", ]
politisk_samarbejde= [u"støtteparti", u"koalition", u"regeringssamarbejde", "regeringskrise", "intern splid", "partiformand", "statsministerkandidat", "forlig", "politisk samarbejde", "politisk alliance", "samarbejde over midten", "blokpolitik", "forligsparti", "forligskreds"]
postvaesen=[" post danmark ", " post dk ", u"postdanmark", "sender breve", u"postnord", u" porto ", u"frimærk", u"pakkepost", u"track and trace", u"eposthuset", u"mobilporto", u"pakkeboks", u"modtagerflex", "postsektor"]
praktiserende_laeger=[u" egen læge ", "e-konsultation", "emailkonsultation", u"praktiserende læge", u"lægepraksis", u"lægesekretær", u" lægeklinik", "kliniksygeplejerske", u"familielæge"]
privatoekonomi=[u"privatøkonomi", u"kviklån", u"billån", u"sms-lån", "skylde penge", "bruge penge", u"gældssanering", " rki ", " kreditkort", "fællesøkonomi", "madkonto", "inkasso", "mastercard", "dankort", u"indlån", "opsparing", "lån","konto"]
psykiske_lidelser=[u"spiseforstyrrelse", u"stress", u"adhd", u"autism", u"angst", u"terapi", u"psykofarmaka","psykisk lidelse","psykisk syg","sindslidelse", "sindslidende", "mental sundhed","spiseforstyrrelse", "anoreksi","bulimi","ortoreksi","overspisning","selvskade","cutter","selvmord","demens","dement","alzheimer","depression","skizofren","bipolar","manio-depressiv","depressiv","ocd","tvangstanke","tilknytningsforstyrrelse","tilpasningsforstyrrelse","posttraumatisk stress","autisme","angst","psykiatri","psykolog","psykiater","psykoterapi","samtaleterapi","skolepsykolog",u"miljøterapi","lykkepille",u"mentalundersøgelse"," ect ",u"tvangsindlæggelse", "antidepressiv"]
retspolitik_justitsvaesen=["anklagemyn", "domstol", "byret", "strafferamme", u"hårdere straffe", u"straffes med fængsel", u"fængselsstraf", u"bødestraf", u"idøm", "livstid", u"højesteret", "landsret", "bryde lov", "straffelov", "straffesag"]
scenekunst_litteratur=[u"det kongelige teater", "teaterfestival", "scenekunst", "operahus", "teaterscene", u"skønlitteratur", "samtidslitteratur", u"gå i teatret", "se teater", "teaterforestilling", u"læse bøger", u"læser bøger", "arnold busck", "bog og ide", "boghandel", "bogmesse", "poesi", "bogudgivelse", "bogforlag", "gyldendal", "lindhart og ringhof", "lydbog", "e-bog", "e bog", u"e bøger", u"e-bøger", " kindle ",]
skatter_afgifter=["am bidrag", u"arbejdsmarkedsbidrag", u"b-indkomst", u"b-skat", u"a-indkomst", u"a-kort", u"frikort", u"restskat", u"penge tilbage i skat", u"selvangivelse", u"forskudsopgørelse", u"årsopgørelse", u"selskabsskat", u"skattefradrag", u"boligskattefradrag", u"fradrag", u"told" ,u"moms", u"indkomstskat", u"skat på arbejde", u"bundskat", u"topskat", u"grundskyld", "betale skat", "skat", u"boligskat", u"grundskyld", u"topskat", u"bundskat", u"moms", u"told", u"afgift", u"skattelettelse", u"skattely", " pso "]
socialt_udsatte=[u"socialt udsat", "samfundets svageste", "sociale problemer", u"udsatte børn", "udsatte unge", "udsatte familier", u"hjemløs", u"leve på gaden", u"bo på gaden", u"gå fra hus og hjem", "misbruger","seksuelt misbrugt", "incest", "alkoholiker", u"fattige børn", "prostitueret", "voldsramt", u"værested", "herberg", "stofmisbrug", "fixerum", "sundhedsrum", "stofindtagelsesrum", "sexhandlede", "handlede kvinder", "omsorgssvigt", u"vanrøgt", u"børnehjem"]
sport=[" sport ", u" OL ", "olympisk", u"paralympiske lege", u" EM ", u" VM ", "doping", "matchfixing", "fodbold", u"håndbold", "tennis", "badminton", "gymnastik", "roning", "basketball", "volleyball", "atletik", "baseball", "ridning", " uefa ", "champions leage", "tour de france", "giro d'italia", "vuelta a españa", u"bjergtrøje", u"pointtrøje", u" den gule trøje", "cykelsport", "elitesport", "team danmark", " fifa ", " uefa ", "wozniacki", "golden league", "mesterskab", "medalje", "pokal", "sportsarena", "sportshal", "squash", "nationalmelodi", " ehf ", " whf ", " wta ", "golf", "boksning"]
sundhed_etik=[u"dødshjælp", "organdonation", "rugemor", u"rugemødre", "kunstig befrugtning", "cyborg", "kloning", "genteknologi", "stamcelle", "genmodificer", "surrogat", "fosterdiagnostik", u"designerbørn", u"designer børn", "bioteknologi", "assisteret reproduktion", "cybergenetics", "cybergenetik", "dobbeltdonation", "embryo adoption",]
teknologi_hverdag=[u"mobilstråling", u"skærmforbrug", u"skærmtid", u"overvågning", " wifi", "google maps", "tinder", " app ", " mac ", "profilbillede", u"på nettet"]
teknologisk_udvikling=["teknologi", "algoritme",  "automatisering", "virtual reality", u"robot", u"selvkør", u"førerløs", "kunstig intelligens", "artificial intelligence", "augmented reality", "distruption", u"programmør", "hack", "cyber security","cyber-sikkerhed","cyber-sikkerhed", "dark web", "3d-print","nanoteknologi","kvantecomputer"]
terror=[u"terror", "voldelig ekstremisme", "islamis", " isis ", "selvmords", u"bombebælte", "radikaliser", "ensom ulv"]
transport=[u"vejnet", u"storebælt", u"lillebælt", u"øresund", u"kollektiv trafik", u"offentlig transport", u"billetpris", u"takstzone", u"pendler", u"rejsekort", u"ungdomskort", u"  bus ", "togbus", u" tog ", u" metro ", u" taxa ", u"færge", u"banedanmark", " DSB ", "metroselskabet", " uber ", u"selvkørende bil", u"storstrømsbro", "fehmern", "benzin", "diesel", " biler ", " bil ", "tankstation", "movia", "arriva"]
trepartsforhandlinger=["den danske model", "trepartsforhandlinger", u"trepartsaftale", u"dansk arbejdsgiverforening", u"fagbevægelse", u"sættemøde", u"kommissorium", "septemberforlig", " LO ", "arbejdsgiverorganisation", u"lønmodtager", "dansk arbejdsgiverforening", " DA ", u"lønvilkår", u"arbejdsvilkår", ]
udenlandsk_arbejdskraft=["udenlandsk arbejdskraft", u"arbejdstilladelse", "fast-track-ordning", "greencard", "positivlisten", "au pair", "working holiday", u"østarbejd", u"grænsegæng", u"østeuropæiske håndværkere", u"polske håndværkere", "social dumping", u"løndumping", u" uden overenskomst", u"mindsteløn", u"arbejdsmiljølovgivning", u"udenlandske lønmodtagere", u"indslusningsløn", u"indslusningsløn"]
udviklingspolitik=[u"udviklingspolitik", u"udviklingsbistand", u"udviklingssamarbejde", u"fattigdomsbekæmpelse", u"bekæmpelse af fattigdom", u"nødhjælp", u"humanitær indsats", u"rettighedsbaseret arbejde", u"menneskerettigheder", "flygtningelejr", u"nærområde", "udviklingsprogram", "uland", "iland", "2015-mål", "absolut fattigdom", "global ulighed", "Verdensbanken", " IBRD ", "demokratiprocesser", u"verdensmål", "dkaid", u"støt uland"]
ungdomsuddannelser=["ungdomsuddannelse" "gymnasial uddannelse", u"erhvervsskole", u"læreplads", "praktikplads", u"teknisk skole", u"handelsskole", u"landbrugsskole", u"social- og sundhedsuddannelse", u"sosu-uddannelse", u"produktionsskole", "stx", "htx", "hhx", " hf ", u"lærling",]
vaekst_erhverv=[u"økonomisk vækst", u"erhvervsliv", u"handelssektor", u" industri", u"import", u"eksport", u"turisme", u"konkurrencelovgivning", u"konkurrencedygtig", "virksomhed"]
vaernepligt=[u"værnepligt", u"værneret", u"militærnægter", "indkaldelsesordre", "Forsvarets Dag", "tjenestested", "tjenestetid", "til session",]
valg_folkeafstemninger=["meningsmåling", u"folketingsvalg", u"europaparlamentsvalg", u"kommunalvalg", u"regionsrådsvalg", u"stemmeprocent", u"valgdeltagelse", "folkeafstemning", "valgkamp", "brevstem", "valgsted", "valgplakat", "udskrive valg", "udskriver valg", "valgtilforordnet", u"førstegangsvælger", u"rødt flertal", u"blåt flertal", u"vælgererklæring",]
videregaaende_uddannelser=[u"videregående uddannelse", u"universitet", u"bacheloruddannelse", u"kandidatgrad", "kandidatuddannelse", u"masteruddannelse", u"professionshøjskole", u"professionsbachelor", u"erhvervsakademi", u"kunstakademi", "arkitektskolen", "uddannelsesloft", u"søge merit", u"få merit", "kvote 1", "kvote 2", "standby-plads", "skrive speciale", "specialekontrakt", "specialevejleder", "afhandling", " KU ", " Aau ", " dtu ", " RUC ", "campus", "akademik", "akademisk"]
yderomraader=[u"yderområder",u"udvikling af landdistrikter og øer","udkantsdanmark",u"byplanlægning","udflytning af statslige arbejdspladser",u"øsamfund", u"planlov","landdistrikt",u"den rådne banan","regional udvikling","landsby",u"landområder",u"ude på landet","lokalsamfund","yderkommune","udkantskommune"]

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
#   midlertidig tilføjelse til banker
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



