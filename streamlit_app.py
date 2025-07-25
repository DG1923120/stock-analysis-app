# app.py

# STEP 1: Import all libraries
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import logging
from scipy.signal import argrelextrema

# --- PAGE CONFIG ---
st.set_page_config(layout="wide", page_title="Stock Analysis Tool")

# --- SUPPRESS YFINANCE ERROR LOGS ---
logging.getLogger('yfinance').setLevel(logging.CRITICAL)

# --- CONFIGURATION (Keep it accessible) ---
CONFIG = {
    "STOCKS": [
    "RELIANCE","HDFCBANK","TCS","BHARTIARTL","ICICIBANK","SBIN","INFY","BAJFINANCE","LICI","HINDUNILVR","ITC","LT","KOTAKBANK","HCLTECH","M&M","SUNPHARMA","MARUTI","ULTRACEMCO","AXISBANK",
        "NTPC","BAJAJFINSV","HAL","ONGC","TITAN","ADANIPORTS","ADANIENT","BEL","ETERNAL","POWERGRID","WIPRO","DMART","TATAMOTORS","JSWSTEEL","COALINDIA","NESTLEIND","BAJAJ-AUTO","ASIANPAINT",
        "INDIGO","ADANIPOWER","IOC","DLF","TATASTEEL","JIOFIN","TRENT","HINDZINC","GRASIM","SBILIFE","VEDL","IRFC","DIVISLAB","HYUNDAI","VBL","HDFCLIFE","ADANIGREEN","LTIM","HINDALCO","BAJAJHLDNG",
        "AMBUJACEM","TECHM","BPCL","EICHERMOT","PIDILITIND","PFC","BRITANNIA","SOLARINDS","TVSMOTOR","LODHA","CHOLAFIN","TATAPOWER","GODREJCP","PNB","BANKBARODA","SHRIRAMFIN","GAIL","MAXHEALTH",
        "ABB","TORNTPHARM","HDFCAMC","CIPLA","MAZDOCK","SHREECEM","BOSCHLTD","SIEMENS","UNIONBANK","MANKIND","MUTHOOTFIN","CGPOWER","INDHOTEL","INDUSTOWER","ENRIN","APOLLOHOSP","RECLTD","TATACONSUM",
        "IDBI","MOTHERSON","SWIGGY","DRREDDY","BSE","ADANIENSOL","POLYCAB","BAJAJHFL","DIXON","CUMMINSIND","JINDALSTEL","HAVELLS","CANBK","UNITDSPR","ZYDUSLIFE","ICICIGI","GMRAIRPORT","NAUKRI","SRF",
        "JSWENERGY","MARICO","HINDPETRO","WAAREEENER","ICICIPRULI","DABUR","NTPCGREEN","BHARTIHEXA","SUZLON","POWERINDIA","PERSISTENT","LUPIN","HEROMOTOCO","BHEL","NHPC","SBICARD","INDIANB",
        "POLICYBZR","IDEA","LLOYDSME","RVNL","OFSS","IOB","PRESTIGE","ABBOTINDIA","OIL","ASHOKLEY","ATGL","PATANJALI","ABCAPITAL","GODREJPROP","COROMANDEL","TORNTPOWER","PAYTM","JSWINFRA",
        "BERGEPAINT","GICRE","HDBFS","INDUSINDBK","SCHAEFFLER","VMM","OBEROIRLTY","AUROPHARMA","NMDC","GVT&D","MRF","KALYANKJIL","FORTIS","NYKAA","BDL","YESBANK","COLPAL","COFORGE","PIIND",
        "UNOMINDA","FACT","IRCTC","GLENMARK","ALKEM","BHARATFORG","SUNDARMFIN","TIINDIA","LINDEINDIA","MOTILALOFS","JSL","SAIL","AUBANK","UPL","NAM-INDIA","MFSL","UBL","LTF","IDFCFIRSTB",
        "BIOCON","GLAXO","BALKRISIND","PAGEIND","SUPREMEIND","HEXT","FEDERALBNK","PHOENIXLTD","MPHASIS","BANKINDIA","JKCEMENT","ITCHOTELS","TATACOMM","COCHINSHIP","PREMIERENE","AIIL","GODFRYPHLP",
        "APLAPOLLO","CONCOR","THERMAX","PETRONET","LTTS","360ONE","VOLTAS","HUDCO","LAURUSLABS","IREDA","JUBLFOOD","MAHABANK","CRISIL","ANTHEM","DALBHARAT","PGHH","KPRMILL","MCX","NH","COHANCE",
        "ASTRAL","FLUOROCHEM","CHOLAHLDNG","ESCORTS","UCOBANK","SJVN","TATAELXSI","KAYNES","GODREJIND","KEI","IPCALAB","ENDURANCE","RADICO","APARINDS","ACC","GILLETTE","NATIONALUM","AWL","M&MFIN",
        "BLUESTARCO","HONAUT","3MINDIA","CDSL","MEDANTA","KPITTECH","POONAWALLA","TATAINVEST","CENTRALBK","LICHSGFIN","AJANTPHARM","NLCINDIA","GLAND","EXIDEIND","GODIGIT","METROBRAND","DELHIVERY",
        "GUJGASLTD","BAYERCROP","AIAENG","ASTERDM","NBCC","AEGISVOPAK","KIMS","NIACL","SONACOMS","ITI","GRSE","PEL","IGL","SUMICHEM","IRB","BANDHANBNK","APOLLOTYRE","TATATECH","RAMCOCEM","WOCKPHARMA",
        "NUVAMA","PNBHOUSING","IKS","MSUMI","PPLPHARMA","MRPL","INOXWIND","EMCURE","SYNGENE","HINDCOPPER","TIMKEN","AEGISLOG","AFFLE","JBCHEPHARM","DEEPAKNTR","STARHEALTH","SHYAMMETL","NAVINFLUOR",
        "BRIGADE","ANGELONE","ZFCVINDIA","HSCL","ABSLAMC","EMAMILTD","LALPATHLAB","TVSHLTD","TATACHEM","AMBER","SKFINDIA","REDINGTON","FSL","PFIZER","WELCORP","ERIS","EIHOTEL","CESC","JYOTICNC",
        "SUNTV","MANAPPURAM","KEC","ONESOURCE","IIFL","DCMSHRIRAM","CASTROLIND","ABREL","PGEL","FORCEMOT","CHAMBLFERT","ASTRAZEN","AADHARHFC","ANANDRATHI","KIOCL","PSB","BASF","CROMPTON","KARURVYSYA",
        "KFINTECH","HATSUN","DEVYANI","CREDITACC","PTCIL","FIVESTAR","SUNDRMFAST","POLYMED","SAGILITY","EIDPARRY","CAMS","ASAHIINDIA","CHALET","CONCORDBIO","KPIL","DEEPAKFERT","VINATIORGA",
        "TRITURBINE","APLLTD","KANSAINER","BIKAJI","ATUL","GRINDWELL","RATNAMANI","KAJARIACER","ANANTRAJ","VENTIVE","MANYAVAR","JUBLPHARMA","FIRSTCRY","OLAELEC","UTIAMC","GSPL","ELGIEQUIP",
        "CARBORUNIV","ZENSARTECH","NATCOPHARM","ARE&M","ABLBL","WHIRLPOOL","NAVA","BEML","VGUARD","IRCON","SOBHA","NEULANDLAB","IGIL","ECLERX","CGCL","APTUS","ACMESOLAR","TECHNOE","AKZOINDIA",
        "SIGNATURE","ZENTEC","JMFINANCIL","LTFOODS","LMW","MAHSCOOTER","SAILIFE","IEX","INTELLECT","IFCI","RRKABEL","KIRLOSBROS","FINEORG","PARADEEP","GODREJAGRO","ICICIB22","EMBDL","HBLENGINE",
        "CENTURYPLY","BLUEDART","SWANENERGY","NIVABUPA","CAPLIPOINT","CIEINDIA","SARDAEN","CUB","TRIDENT","RBLBANK","INDIAMART","AFCONS","RAINBOW","TBOTEK","DATAPATTNS","THELEELA","AARTIIND",
        "BATAINDIA","KSB","SPLPETRO","TRAVELFOOD","JWL","PCBL","CRAFTSMAN","JBMA","CHOICEIN","BLS","TARIL","GALLANTT","AAVAS","JPPOWER","MGL","NUVOCO","HOMEFIRST","JINDALSAW","GMDCLTD","GABRIEL",
        "DOMS","AGARWALEYE","CYIENT","GESHIP","BLUEJET","CEATLTD","NCC","FINCABLES","VTL","CLEAN","ITDCEM","BBTC","SANOFI","ACE","ENGINERSIN","INDGN","CELLO","ELECON","KIRLOSENG","ABDL","ZYDUSWELL",
        "WELSPUNLIV","RITES","TEGA","RAILTEL","SBFC","GPIL","FINPIPE","INGERRAND","JUBLINGREA","GRAVITA","ANURAS","ALIVUS","ATHERENERG","NEWGEN","JYOTHYLAB","LEMONTREE","TITAGARH","SYRMA","NAZARA",
        "RELAXO","ZEEL","PRUDENT","MINDACORP","J&KBANK","GRINFRA","BALRAMCHIN","WESTLIFE","SONATSOFTW","SANOFICONR","JKLAKSHMI","WAAREERTL","HFCL","BELRISE","USHAMART","GRANULES","CHENNPETRO",
        "NSLNISP","CCL","ALKYLAMINE","RKFORGE","GENUSPOWER","SHAKTIPUMP","SUNDARMHLD","INDIACEM","GRAPHITE","BSOFT","BIRLACORPN","VESUVIUS","INOXINDIA","SAMMAANCAP","NETWEB","OLECTRA","TEJASNET",
        "SAPPHIRE","RHIM","EUREKAFORB","MARKSANS","JAIBALAJI","AETHER","EDELWEISS","MEDPLUS","TIMETECHNO","SHRIPISTON","KPIGREEN","CANFINHOME","SAFARI","VIJAYA","SCI","LLOYDSENT","HEG","METROPOLIS",
        "INDIASHLTR","MMTC","AZAD","AVANTIFEED","ASKAUTOLTD","ALOKINDS","POWERMECH","PCJEWELLER","IIFLCAPS","MON100","PVRINOX","HDFCGOLD","WABAG","MAHSEAMLES","MAPMYINDIA","PGHL","ACUTAAS","STARCEMENT",
        "JKTYRE","SUDARSCHEM","TRANSRAILL","RELIGARE","JLHL","PRIVISCL","BECTORFOOD","SAREGAMA","TCI","MANORAMA","KRBL","VOLTAMP","ASTRAMICRO","HAPPSTMNDS","NETWORK18","CARTRADE","GARFIBRES",
        "LATENTVIEW","ABFRL","BANCOINDIA","HAPPYFORGE","GALAXYSURF","LLOYDSENGG","TANLA","UJJIVANSFB","TI","PRAJIND","NESCO","HONASA","ESABINDIA","DIACABS","ARVIND","CAMPUS","OSWALPUMPS",
        "MAXESTATES","CERA","TTKPRESTIG","THOMASCOOK","KALPATARU","IXIGO","AARTIPHARM","ACI","KIRLPNU","GRWRHITECH","AKUMS","RCF","VARROC","STAR","SANSERA","ISGEC","BORORENEW","GMRP&UI","RTNINDIA",
        "CMSINFO","GSFC","PNCINFRA","PNGJL","GNFC","TRIVENI","PRSMJOHNSN","DODLA","MAHLIFE","BLACKBUCK","MOIL","AURIONPRO","ELLEN","FDC","TIPSMUSIC","SHARDACROP","AJAXENGG","HCG","MASTEK","RUSTOMJEE",
        "MIDHANI","GPPL","LUMAXTECH","SYMPHONY","EPIGRAL","SANDUMA","DHANUKA","SOUTHBANK","ETHOSLTD","RTNPOWER","TDPOWERSYS","BAJAJELEC","SHAILY","TIIL","GANESHHOUC","EPL","CSBBANK","SURYAROSNI",
        "MHRIL","JUSTDIAL","CHEMPLASTS","TMB","SFL","AHLUCONT","REDTAPE","EQUITASBNK","IONEXCHANG","KTKBANK","JUNIPER","SWSOLAR","WELENT","ELECTCAST","HGINFRA","DBL","RALLIS","GOLD1","PGIL",
        "MANINFRA","EMUDHRA","RAYMONDLSL","PURVA","RENUKA","QPOWER","ARVINDFASN","GOKEX","HNDFDS","SHARDAMOTR","ICRA","V2RETAIL","VIPIND","JKPAPER","PARAS","RESPONIND","SUNTECK","THYROCARE",
        "TEXRAIL","GREENLAM","KNRCON","FISCHER","AGI","SUPRAJIT","BANSALWIRE","YATHARTH","VMART","GULFOILLUB","MASFIN","WEBELSOLAR","CRIZAC","GHCL","SHOPERSTOP","RAJESHEXPO","ROUTE","THANGAMAYL",
        "SMLISUZU","ICIL","PILANIINVS","GMMPFAUDLR","TVSSCS","AVALON","KSCL","TARC","SENCO","STLTECH","PICCADIL","INDIGOPNTS","ASHOKA","SUBROS","LXCHEM","HDFCNIFBAN","SUPRIYA","PTC","BALAMINES",
        "STYRENIX","CARERATING","JKIL","APOLLO","ZAGGLE","INDIAGLYCO","ANUP","IFBIND","BANKNIFTY1","ASHAPURMIN","REFEX","VRLLOG","SWARAJENG","SIS","RATEGAIN","KRN","SKIPPER","SAMHI","PDSL",
        "SUNFLAG","PRICOLLTD","FIEMIND","ORIENTCEM","RAIN","RSYSTEMS","ENTERO","EMIL","ITDC","INNOVACAP","OPTIEMUS","SINDHUTRAD","GAEL","RAYMONDREL","AVL","SPARC","DBCORP","DATAMATICS","PFOCUS",
        "63MOONS","LIQUIDCASE","MCLOUD","HEIDELBERG","RBA","AARTIDRUGS","EIEL","VSTIND","DYNAMATECH","CIGNITITEC","JSFB","MARATHON","SMARTWORKS","NFL","GREAVESCOT","SKYGOLD","RAYMOND","JCHAC",
        "E2E","GOCOLORS","BANARISUG","GOKULAGRO","MTARTECH","SEQUENT","ORIENTELEC","KIRLOSIND","CEIGALL","BHARATRAS","QUESS","FEDFINA","INFIBEAM","SANATHAN","NIITMTS","AWFIS","UNICHEMLAB",
        "DCBBANK","SHANTIGEAR","GOPAL","HDFCNIFTY","KINGFA","HERITGFOOD","GUJALKALI","SUNCLAY","UFLEX","INDRAMEDCO","LUXIND","NORTHARC","GREENPLY","HIKAL","WONDERLA","JAYNECOIND","INDOSTAR",
        "RPGLIFE","VSTTILLERS","MPSLTD","JINDWORLD","NEOGEN","LGBBROSLTD","IMFA","ROLEXRINGS","SAMBHV","RAMKY","VADILALIND","GUJTHEM","HUBTOWN","VAIBHAVGBL","BOROLTD","KSL","ROSSARI","BHAGCHEM",
        "SJS","CUPID","DIGITIDE","PRINCEPIPE","GREENPANEL","DHANI","SSWL","GUFICBIO","ARKADE","SHAREINDIA","BOMDYEING","AVANTEL","PRABHA","JAMNAAUTO","MEDIASSIST","MANGCHEFER","HEMIPROP","MAFANG",
        "JASH","IMAGICAA","DPABHUSHAN","BALMLAWRIE","GOLDIAM","GANECOS","HPL","ADVENZYMES","CYIENTDLM","MBAPL","HARSHA","EASEMYTRIP","JTEKTINDIA","JISLJALEQS","NSIL","GOODLUCK","WSTCSTPAPR","SHK",
        "ORCHPHARMA","NPST","PITTIENG","MSTCLTD","LUMAXIND","KPEL","POLYPLEX","ALLCARGO","AJMERA","SUNDROP","ZOTA","EMSLIMITED","KKCL","BBL","NAVNETEDUL","KDDL","EPACK","CENTUM","MAITHANALL",
        "KOLTEPATIL","FLAIR","PENIND","TCPLPACK","PRECWIRE","PROTEAN","MOREPENLAB","DDEVPLSTIK","VISHNU","ARTEMISMED","PARKHOTELS","SAGCEM","BAJAJHIND","BAJAJCON","FMGOETZE","PATELENG","NIFTY1",
        "PSPPROJECT","MOSCHIP","GLOBUSSPR","GATEWAY","ASHIANA","NITCO","PRAKASH","SIYSIL","NOCIL","TEAMLEASE","VENUSPIPES","SBCL","POKARNA","GIPCL","SERVOTECH","RPSGVENT","KIRIINDUS","STYLAMIND",
        "DALMIASUG","FCL","SDBL","RAMRAT","ORISSAMINE","FOSECOIND","RPEL","TIRUMALCHM","JUBLCPL","ALEMBICLTD","EVEREADY","KRISHANA","LAOPALA","DEEPINDS","DCXINDIA","BSLNIFTY","PARAGMILK","MONARCH",
        "JTLIND","ADFFOODS","BFUTILITIE","SAKSOFT","NRBBEARING","MUTHOOTMF","WINDMACHIN","SANDHAR","HONDAPOWER","PAISALO","MANINDS","VEEDOL","FUSION","BCG","NUCLEUS","IOLCP","COSMOFIRST","INSECTICID",
        "INDOCO","ARVSMART","KCP","SENORES","SOTL","BEPL","TCIEXP","HGS","TASTYBITE","CARRARO","HATHWAY","AEROFLEX","KRSNAA","HLEGLAS","CAPACITE","REPCOHOME","PREMEXPLN","KALAMANDIR","POCL",
        "XPROINDIA","AUTOAXLES","TAJGVK","ORIENTHOT","PANACEABIO","UNIVCABLES","JINDALPOLY","NILKAMAL","PFS","MAYURUNIQ","NDRAUTO","TFCILTD","CARYSIL","LAXMIDENTL","FILATEX","GENESYS","MAHLOG",
        "AGIIL","SULA","IPL","UTKARSHBNK","RAMCOIND","MOL","SHANKARA","RML","MOLDTKPAC","STEELCAS","SEPC","DIAMONDYD","SCILAL","SOLARA","THEJO","DELTACORP","SIMPLEXINF","EIHAHOTELS","NIBE","YASHO",
        "TVSSRICHAK","TATVA","FINOPB","SPECTRUM","SOMANYCERA","SANGHVIMOV","SANGAMIND","SUMMITSEC","ROSSTECH","CANTABIL","VIMTALABS","SIRCA","INDIANHUME","WEL","GRMOVER","RANEHOLDIN","SASKEN","SHALBY",
        "HINDOILEXP","MOTISONS","NITINSPIN","DOLLAR","HINDWAREAP","VENKEYS","KICL","SPANDANA","PANAMAPET","DCW","VSSL","IDEAFORGE","DYCL","SEAMECLTD","HIRECT","SMSPHARMA","LIQUIDADD","LANDMARK","VPRPL",
        "ECOSMOBLTY","JYOTISTRUC","ACCELYA","PIXTRANS","SPMLINFRA","GEOJITFSL","SPAL","WENDT","GOLDSHARE","UDAICEMENT","RAJOOENG","DEEDEV","RAJRATAN","APCOTEXIND","EXICOM","STYLEBAAZA","VIDHIING",
        "TARSONS","MOBIKWIK","ASALCBR","RPTECH","UGROCAP","WHEELS","AMRUTANJAN","DREDGECORP","GEPIL","STOVEKRAFT","MANGLMCEM","DIVGIITTS","VINDHYATEL","UTINEXT50","INDOTECH","NAVKARCORP","NELCO",
        "STANLEY","AXISGOLD","HIMATSEIDE","MUKANDLTD","WINDLAS","HITECH","GOCLCORP","JGCHEM","PNBGILTS","VINCOFE","TTKHLTCARE","MSPL","UDS","KMEW","EXPLEOSOL","VERANDA","QUADFUTURE","JNKINDIA",
        "IFGLEXPOR","JAICORPLTD","ADOR","APOLLOPIPE","PRECAM","DEN","IGARASHI","JINDRILL","ARIHANTSUP","BFINVEST","DLINKINDIA","QUICKHEAL","OMAXE","INDNIPPON","DOLPHIN","SPIC","CONFIPET","RAMASTEEL",
        "AWHCL","BIRLANU","SANGHIIND","JAGSNPHARM","ARMANFIN","TALBROAUTO","ASTEC","SESHAPAPER","DAMCAPITAL","SATIN","MMFL","GARUDA","RUPA","EXCELINDUS","PARACABLES","FAZE3Q","UNIPARTS","SHRIRAMPPS",
        "MASTERTR","PLATIND","GREENPOWER","GPTINFRA","ROTO","SANSTAR","HUHTAMAKI","ESAFSFB","LGHL","TINNARUBR","CLSEL","DOLATALGO","NIITLTD","GMBREW","BLISSGVS","SPORTKING","GANDHAR","BAJAJHCARE",
        "PSUBANK","IKIO","JAGRAN","SURAKSHA","BLKASHYAP","ALICON","SMCGLOBAL","BOROSCI","PUNJABCHEM","HESTERBIO","EKC","ANDHRAPAP","SURAJEST","SIGACHI","HMAAGRO","DCMSRIND","IGPL","HARIOMPIPE","CIFL",
        "DECCANCE","AURUM","YUKEN","SURYODAY","MUFIN","ALLDIGI","SALZERELEC","HERANBA","SILVER1","MANAKCOAT","GNA","CAPITALSFB","BSHSL","AGARIND","MADRASFERT","NELCAST","BHARATWIRE","RIIL","BAJAJINDEF",
        "YATRA","GTPL","ORIENTTECH","LIQUID1","KELLTONTEC","MTNL","BUTTERFLY","OAL","HEUBACHIND","GPTHEALTH","IMPAL","ELECTHERM","STERTOOLS","GRPLTD","BCLIND","SHREDIGCEM","HDFCSML250","BLUSPRING",
        "EIMCOELECO","AYMSYNTEX","TBZ","MICEL","DSSL","PENINLAND","INFOBEAN","PROSTARM","CEWATER","WEALTH","MANALIPETC","ASIANENE","VHL","AMNPLST","UNIECOM","SALASAR","DPSCLTD","TEXINFRA","ICEMAKE",
        "SIGNPOST","VASCONEQ","DVL","BIL","ATULAUTO","MONTECARLO","RGL","DIFFNKG","STEELXIND","BARBEQUE","5PAISA","IRMENERGY","FAIRCHEMOR","RADHIKAJWE","KROSS","SCODATUBES","MAMATA","OMINFRAL",
        "AEROENTER","CONTROLPR","RACLGEAR","SAURASHCEM","SHREEPUSHK","ROHLTD","ESTER","ARISINFRA","TNPL","SBISILVER","INNOVANA","WCIL","KUANTUM","KOKUYOCMLN","PDMJEPAPER","MAXIND","INDOAMIN",
        "OSWALGREEN","CENTENKA","SRHHYPOLTD","AVTNPL","DHANBANK","AFSL","UNIENTER","ANDHRSUGAR","MATRIMONY","CHEMFAB","BESTAGRO","THEMISMED","HDFCSILVER","GALAPREC","RISHABH","OSWALAGRO","SRM",
        "PASHUPATI","LIKHITHA","LINCOLN","CREST","GULPOLY","MVGJL","MUFTI","ARIHANTCAP","GKWLIMITED","UTTAMSUGAR","DISHTV","KABRAEXTRU","HDFCSENSEX","XCHANGING","GICHSGFIN","TVTODAY","ACLGATI",
        "NCLIND","HEXATRADEX","INDOFARM","SWELECTES","KOTHARIPET","AXISNIFTY","RICOAUTO","BIRLAMONEY","ANUHPHR","MASPTOP50","ADSL","20MICRONS","CREATIVE","SNOWMAN","SILVERTUC","PRIMESECU","SILVER",
        "DENTA","SELAN","BODALCHEM","AVADHSUGAR","GANDHITUBE","NAHARSPING","DHAMPURSUG","ASAL","PAKKA","PVSL","DHUNINV","STALLION","AMBIKCO","PPL","JITFINFRA","SASTASUNDR","ZUARI","KECL","SANDESH",
        "SILVERADD","GHCLTEXTIL","THEINVEST","SHIVALIK","RKSWAMY","MUKKA","BLAL","BIGBLOC","SATIA","SGIL","HLVLTD","BHAGERIA","RITCO","ZEEMEDIA","MSCIINDIA","NBIFIN","TREL","KOPRAN","TATAGOLD",
        "JPOLYINVST","DWARKESH","NINSYS","KAMDHENU","MAGADSUGAR","ATL","MALLCOM","VLSFINANCE","VERTOZ","KSOLVES","SBC","JAYBARMARU","RATNAVEER","SCHAND","ZUARIIND","RUBYMILLS","CHEMCON","RUSHIL",
        "JAYAGROGN","NGLFINE","DMCC","GEECEE","SARVESHWAR","COFFEEDAY","REPRO","SHALPAINTS","INDOBORAX","MUNJALAU","URJA","APEX","RSWM","STEL","CCCL","LICNFNHGP","NEXT50","CSLFINANCE","ELDEHSG",
        "HINDCOMPOS","IGCL","LICNMID100","GLOSTERLTD","TOP10ADD","MMP","HDFCPVTBAN","KAMATHOTEL","ORICONENT","GFLLIMITED","ALPHA","MENONBE","MOM100","SUTLEJTEX","ENIL","GANESHBE","PRIMO","MANBA",
        "CHEVIOT","SMALLCAP","KRONOX","SURAJLTD","SPECIALITY","EMKAY","HMVL","DBEIL","RPPINFRA","CONSOFINVT","TOLINS","SILINV","TRACXN","DBOL","PYRAMID","ACL","IZMO","RADIANTCMS","TPLPLASTEH",
        "PROZONER","ORIENTPPR","MAZDA","MODISONLTD","TRANSWORLD","EMAMIPAP","BORANA","EQUAL50ADD","MUNJALSHOW","INTLCONV","TARACHAND","ARFIN","ZIMLAB","BELLACASA","ONMOBILE","PAVNAIND","NILASPACES",
        "DICIND","ADVANIHOTR","MUTHOOTCAP","SREEL","VRAJ","LORDSCHLO","PVP","SHREERAMA","RBZJEWEL","MODEFENCE","PREMIERPOL","MGEL","SINCLAIR","NOVAAGRI","SPENCERS","GUJAPOLLO","DONEAR","KRITINUT",
        "GLOBECIVIL","MANAKSIA","SUKHJITS","LIQUID","MBLINFRA","ORIENTCER","KHADIM","SOFTTECH","PTL","MEDICAMEQ","UNITEDPOLY","GSLSU","ALBERTDAVD","UGARSUGAR","DIGISPICE","PLASTIBLEN","SRD","AVONMORE",
        "COMSYN","CLEDUCATE","VARDMNPOLY","DENORA","RHL","SBIBPB","SRGHFL","KAPSTON","GENUSPAPER","KOTHARIPRO","AFFORDABLE","BANSWRAS","ARIES","BEDMUTHA","OILCOUNTUB","HPAL","NILAINFRA","RUBFILA",
        "MAHKTECH","ORIENTBELL","MCLEODRUSS","REMSONSIND","PASUPTAC","UNIDT","MOLDTECH","XTGLOBAL","MIRZAINT","GOACARBON","DYNPRO","GOKUL","BFSI","NDGL","PVTBANKADD","AVG","BPL","RACE","AARON",
        "ALANKIT","ROSSELLIND","VALIANTLAB","SHIVAMAUTO","ASMS","SUMIT","MIRCELECTR","MAHEPC","TRF","RUCHIRA","3IINFOLTD","VARDHACRLC","LOKESHMACH","LYKALABS","HARRMALAYA","LICMFGOLD","KCPSUGIND",
        "KANORICHEM","SSDL","MAWANASUG","MANCREDIT","DIAMINESQ","BALAJEE","DCI","NAGAFERT","GOLDTECH","BCONCEPTS","GEEKAYWIRE","ALMONDZ","SUNDRMBRAK","APOLSINHOT","DJML","VIPCLOTHNG","MIDSMALL",
        "BBTCL","UYFINCORP","SINTERCOM","SMSLIFE","GOLDCASE","QGOLDHALF","NIPPOBATRY","INDOUS","AIRAN","DCMNVL","DPWIRES","AXISILVER","IT","HITECHCORP","SHRADHA","BHAGYANGR","SAHYADRI","AUTOIND",
        "UCAL","TREJHARA","VSTL","UNIVASTU","REPL","JAYSREETEA","GLOBALVECT","MEDICO","AXITA","PODDARMENT","AFIL","SCPL","RADIOCITY","MEGASTAR","CINELINE","STARTECK","CPCAP","PRITIKAUTO","MARALOVER",
        "KOTARISUG","IVZINGOLD","VIRINCHI","SAKHTISUG","CCHHL","MANOMAY","ABAN","TATSILV","UFO","AHLEAST","LIQUIDPLUS","STARPAPER","SUPREME","ZODIACLOTH","IVC","ATLANTAA","GILLANDERS","NIRAJ","RVHL",
        "MURUDCERA","ANIKINDS","WORTH","PONNIERODE","GROWWEV","PLAZACABLE","BALAXI","KALYANIFRG","SHIVATEX","CORDSCABLE","DEVIT","SURANAT&P","KMSUGAR","KRITIKA","BASML","AMJLAND","TRIGYN","NURECA",
        "COASTCORP","INDOWIND","VETO","MHLXMIRU","ESILVER","AKSHARCHEM","ASPINWALL","RANASUG","UNITEDTEA","NDLVENTURE","TIPSFILMS","EGOLD","GULFPETRO","OMAXAUTO","AONELIQUID","NATCAPSUQ","SADBHAV",
        "TAINWALCHM","AARTECH","MOMENTUM50","NECCLTD","ALPA","MANAKALUCO","SONAMLTD","MAKEINDIA","GROWWDEFNC","DCM","BAFNAPH","NITIRAJ","JMA","DTIL","VISHWARAJ","EMMBI","INTENTECH","ARCHIDPLY","USK",
        "CORALFINAC","AVROIND","DUCON","IVP","MUKTAARTS","RPPL","INDTERRAIN","CENTEXT","ARVEE","WEIZMANIND","INDIANCARD","SUPERHOUSE","CROWN","SOMICONVEY","TEXMOPIPES","BRNL","LAGNAM","ALPHAGEO",
        "HINDCON","MAHESHWARI","EVINDIA","LOWVOL1","AIROLAM","COMPUSOFT","ISFT","MODTHREAD","SIKKO","TIMESGTY","GANGESSECU","GVPTECH","RKEC","LANCORHOL","SMLT","STEELCITY","SURANASOL","MAGNUM","HPIL",
        "RAJSREESUG","GTL","AARVI","BAIDFIN","BALPHARMA","NIFTY50ADD","MAHAPEXLTD","LOTUSEYE","SMARTLINK","UMIYA-MRO","INDBANK","BTML","MANGALAM","PRUDMOULI","JOCIL","PRAENG","BHARATGEAR","UNIONGOLD",
        "LOVABLE","FIBERWEB","LAMBODHARA","TARMAT","SAMBHAAV","RELCHEMQ","ABSLNN50ET","BAGFILMS","HDFCNEXT50","AKSHOPTFBR","MONIFTY500","SURYALAXMI","SALSTEEL","HDFCMID150","REGENCERAM","MCL","XELPMOC",
        "WIPL","BHANDARI","VAISHALI","KAKATCEM","AXSENSEX","SALONA","SAMPANN","HDFCMOMENT","MOMOMENTUM","KOHINOOR","SIL","PIONEEREMB","MOVALUE","PALASHSECU","LATTEYS","TOTAL","ZENITHEXPO","BBNPPGOLD",
        "BEARDSELL","PATINTLOG","MOSMALL250","ESG","PRITI","SHAHALLOYS","OSWALSEEDS","MOGSEC","TOKYOPLAST","AAATECH","NV20","ATAM","DIGIDRIVE","MOKSH","OBCL","ACCURACY","TOUCHWOOD","HDFCNIFIT","LPDC",
        "HISARMETAL","GOYALALUM","GROWWGOLD","MOTOGENFIN","JHS","MITCON","MIDQ50ADD","PRAKASHSTL","BVCL","MOREALTY","DBSTOCKBRO","BANKA","ALKALI","MID150CASE","INDSWFTLTD","AJOONI","IVZINNIFTY",
        "AMDIND","PSUBANKADD","ANMOL","GSEC10YEAR","GSEC10ABSL","AGRITECH","DAMODARIND","MOLOWVOL","ORIENTLTD","MONQ50","AHLADA","3PLAND","NARMADA","GSS","NAGREEKEXP","CELEBRITY","BANARBEADS","SECURKLOUD",
        "BLBLIMITED","BANG","RELIABLE","ASTRON","AGROPHOS","QNIFTY","JAIPURKURT","MIDCAP","RKDL","MALUPAPER","SHIVAMILLS","BALKRISHNA","HDFCNIF100","GROWWRAIL","SILVERCASE","LFIC","MOCAPITAL",
        "21STCENMGM","JISLDVREQS","ADROITINFO","AROGRANITE","GROWWLIQID","DNAMEDIA","MOM50","SUPERSPIN","NGIL","PEARLPOLY","AMBICAAGAR","WEWIN","SAGARDEEP","MULTICAP","MOMENTUM","LAXMICOT","AKASH",
        "ABSLLIQUID","BOHRAIND","ABGSEC","MOHITIND","LIQUIDSBI","LOWVOL","NEXTMEDIA","HDFCLIQUID","ASHOKAMET","BANKPSU","KHANDSE","AKG","MADHAV","METAL","WILLAMAGOR","HDFCLOWVOL","TGBHOTELS","MNC",
        "HEALTHY","HDFCVALUE","LIBAS","EQUAL50","LIQUIDSHRI","NAGREEKCAP","TECH","ABSLPSE","MOHEALTH","GROWWSLVR","KAUSHALYA","EMULTIMQ","CYBERMEDIA","CONSUMER","HDFCPSUBK","NEXT30ADD","NIFTYQLITY",
        "ACEINTEG","UTISXN50","SANGINITA","AONETOTAL","MON50EQUAL","RETAIL","HDFCGROWTH","HDFCQUAL","HEADSUP","GUJRAFFIA","MOQUALITY","SILLYMONKS","GROWWMOM50","ECAPINSURE","HDFCBSE500","GOLD360",
        "SELECTIPO","UMESLTD","GROWWN200","EUROTEXIND","EQUAL200","AONENIFTY","NPBET","INTERNET","AXISVALUE","HEALTHADD","NIFMID150","SILVER360","ORTINGLOBE",

    ],
    "DATA_PERIOD": "5y", "PLOT_DAYS": 500, "TABLE_DAYS": 15, "UT_SENSITIVITY": 1, "UT_ATR_PERIOD": 10,
    "HMA_PERIOD": 55, "EMA_SHORT": 9, "EMA_MEDIUM": 21, "BB_PERIOD": 20, "BB_STD_DEV": 2.0, "RSI_PERIOD": 14,
    "RSI_EMA_PERIOD": 20, "MACD_FAST": 12, "MACD_SLOW": 26, "MACD_SIGNAL": 9, "SR_WINDOW": 15, "BACKTEST_CAPITAL": 100000,
}

# --- HELPER & ANALYSIS FUNCTIONS ---
def clean_data(df):
    if df.empty: return df
    df = df[df.index <= pd.to_datetime('today').normalize()]
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
    df = df.loc[:,~df.columns.duplicated()]; ohlcv = ['Open', 'High', 'Low', 'Close', 'Volume']
    for col in ohlcv:
        if col in df.columns: df[col] = pd.to_numeric(df[col], errors='coerce')
    df.dropna(subset=ohlcv, inplace=True); return df

def compute_atr(high, low, close, period):
    tr = pd.concat([high - low, abs(high - close.shift(1)), abs(low - close.shift(1))], axis=1).max(axis=1)
    return tr.ewm(alpha=1/period, adjust=False).mean()

def find_support_resistance(df, window):
    highs = argrelextrema(df['High'].values, np.greater_equal, order=window)[0]
    lows = argrelextrema(df['Low'].values, np.less_equal, order=window)[0]
    return df.iloc[highs]['High'], df.iloc[lows]['Low']

def add_all_indicators(df_orig):
    df = df_orig.copy()
    df['Change'] = df['Close'].diff(); df['Change %'] = df['Close'].pct_change() * 100
    df['EMA9'] = df['Close'].ewm(span=CONFIG['EMA_SHORT'], adjust=False).mean()
    df['EMA21'] = df['Close'].ewm(span=CONFIG['EMA_MEDIUM'], adjust=False).mean()
    delta = df['Close'].diff(1); gain = delta.where(delta > 0, 0); loss = -delta.where(delta < 0, 0)
    avg_gain = gain.ewm(com=CONFIG['RSI_PERIOD'] - 1, min_periods=CONFIG['RSI_PERIOD']).mean();
    avg_loss = loss.ewm(com=CONFIG['RSI_PERIOD'] - 1, min_periods=CONFIG['RSI_PERIOD']).mean()
    rs = avg_gain / avg_loss; df['RSI14'] = 100 - (100 / (1 + rs))
    df['RSI_EMA20'] = df['RSI14'].ewm(span=CONFIG["RSI_EMA_PERIOD"], adjust=False).mean()
    exp1 = df['Close'].ewm(span=CONFIG['MACD_FAST'], adjust=False).mean(); exp2 = df['Close'].ewm(span=CONFIG['MACD_SLOW'], adjust=False).mean()
    df['MACD'] = exp1 - exp2; df['MACD_Signal'] = df['MACD'].ewm(span=CONFIG['MACD_SIGNAL'], adjust=False).mean(); df['MACD_Hist'] = df['MACD'] - df['MACD_Signal']
    atr = compute_atr(df['High'], df['Low'], df['Close'], period=CONFIG['UT_ATR_PERIOD'])
    n_loss = CONFIG['UT_SENSITIVITY'] * atr; atr_ts = pd.Series(np.nan, index=df.index); atr_ts.iloc[0] = 0
    for i in range(1, len(df)):
        cl,prev_cl,prev_ts=df['Close'].iloc[i],df['Close'].iloc[i-1],atr_ts.iloc[i-1]
        if cl>prev_ts and prev_cl>prev_ts: atr_ts.iloc[i]=max(prev_ts,cl-n_loss.iloc[i])
        elif cl<prev_ts and prev_cl<prev_ts: atr_ts.iloc[i]=min(prev_ts,cl+n_loss.iloc[i])
        elif cl>prev_ts: atr_ts.iloc[i]=cl-n_loss.iloc[i]
        else: atr_ts.iloc[i]=cl+n_loss.iloc[i]
    df['ATR_Stop'] = atr_ts; df['UT_Trend'] = np.where(df['Close'] > df['ATR_Stop'], 1, -1)
    half_len = int(CONFIG['HMA_PERIOD'] / 2); sqrt_len = int(np.sqrt(CONFIG['HMA_PERIOD']))
    wma_half = df['Close'].rolling(half_len).apply(lambda x: np.dot(x, np.arange(1, half_len + 1)) / np.arange(1, half_len + 1).sum(), raw=True)
    wma_full = df['Close'].rolling(CONFIG['HMA_PERIOD']).apply(lambda x: np.dot(x, np.arange(1, CONFIG['HMA_PERIOD'] + 1)) / np.arange(1, CONFIG['HMA_PERIOD'] + 1).sum(), raw=True)
    df['HMA'] = (2 * wma_half - wma_full).rolling(sqrt_len).apply(lambda x: np.dot(x, np.arange(1, sqrt_len + 1)) / np.arange(1, sqrt_len + 1).sum(), raw=True)
    bb_basis = df['Close'].rolling(window=CONFIG['BB_PERIOD']).mean(); bb_std = df['Close'].rolling(window=CONFIG['BB_PERIOD']).std()
    df['BB_Upper'] = bb_basis + (CONFIG['BB_STD_DEV']*bb_std); df['BB_Lower'] = bb_basis - (CONFIG['BB_STD_DEV']*bb_std)
    return df

def apply_trading_logic(df_orig):
    df = df_orig.copy()
    ema_golden_cross = (df['EMA9'] > df['EMA21']) & (df['EMA9'].shift(1) <= df['EMA21'].shift(1))
    buy_signal = (df['UT_Trend'] == 1) & (df['Close'] > df['HMA']) & ema_golden_cross
    df['Signal'] = np.where(buy_signal, "BUY", "-"); df['Buy_Marker'] = np.where(buy_signal, df['Low']*0.985, np.nan)
    return df

def run_advanced_backtest(_df, initial_capital=100000):
    df = _df.copy()
    df_bt = df.copy().dropna(subset=['ATR_Stop', 'Signal'])
    if df_bt.empty: return "Not enough data for backtest.", None
    capital = initial_capital; equity_curve = [initial_capital]; position = 0; trades = []
    for i in range(1, len(df_bt)):
        current_capital = equity_curve[-1]
        if position == 0 and df_bt['Signal'].iloc[i] == 'BUY':
            entry_price = df_bt['Close'].iloc[i]; entry_date = df_bt.index[i]; position = 1
            shares = current_capital / entry_price
        elif position == 1 and df_bt['Close'].iloc[i] < df_bt['ATR_Stop'].iloc[i]:
            exit_price = df_bt['Close'].iloc[i]; exit_date = df_bt.index[i]; position = 0
            pnl = (exit_price - entry_price) * shares; capital += pnl; equity_curve.append(capital)
            trades.append({"EntryDate": entry_date.strftime('%Y-%m-%d'), "ExitDate": exit_date.strftime('%Y-%m-%d'), "PnL": pnl, "PnL %": (exit_price/entry_price - 1) * 100})
    if not trades: return "No trades were executed.", None
    results_df = pd.DataFrame(trades); total_pnl = results_df['PnL'].sum()
    gross_profit = results_df[results_df['PnL'] > 0]['PnL'].sum(); gross_loss = abs(results_df[results_df['PnL'] < 0]['PnL'].sum())
    win_count = (results_df['PnL'] > 0).sum(); loss_count = len(results_df) - win_count
    equity_series = pd.Series(equity_curve); running_max = equity_series.cummax(); drawdown = (equity_series - running_max) / running_max
    max_drawdown = drawdown.min() * 100 if not drawdown.empty else 0
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
    avg_win = gross_profit / win_count if win_count > 0 else 0; avg_loss = abs(gross_loss / loss_count) if loss_count > 0 else 0
    win_rate = (win_count / len(results_df)) * 100 if len(results_df) > 0 else 0
    summary = (f"Data Period: {df.index.min().strftime('%Y-%m-%d')} to {df.index.max().strftime('%Y-%m-%d')}\n"
               f"Initial Capital: ₹{initial_capital:,.2f}\n"
               f"Final Capital:   ₹{capital:,.2f} ({total_pnl/initial_capital*100:+.2f}%)\n"
               f"Profit Factor:   {profit_factor:.2f}\n"
               f"Max Drawdown:    {max_drawdown:.2f}%\n"
               f"Win Rate:        {win_rate:.2f}% ({win_count}/{win_count+loss_count})\n"
               f"Avg Win / Loss:  ₹{avg_win:,.2f} / ₹{avg_loss:,.2f}")
    return summary, results_df

def check_scanner_conditions(df):
    if len(df) < 2: return False
    try:
        latest=df.iloc[-1]; previous=df.iloc[-2]
        cond1 = latest['Close']>latest['EMA9'] and previous['Close']<=previous['EMA9']
        cond2 = latest['Volume']>100000 and latest['Close']>60 and latest['Change %']<10
        cond3 = latest['RSI14']>latest['RSI_EMA20']; cond4 = latest['MACD_Hist']>0
        return cond1 and cond2 and cond3 and cond4
    except Exception: return False

@st.cache_data
def get_stock_data_and_process(symbol):
    ticker_symbol = f"{symbol.upper()}.NS"
    df_raw = yf.download(ticker_symbol, period="2y", interval="1d", auto_adjust=False, progress=False)
    if df_raw.empty: return None
    df = clean_data(df_raw)
    if len(df) < 250: return None
    df = add_all_indicators(df)
    df = apply_trading_logic(df)
    return df

def display_analysis(symbol, df, reason=""):
    summary, backtest_df = run_advanced_backtest(df, CONFIG["BACKTEST_CAPITAL"])
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.subheader(f"Recent Data for {symbol}")
        table_df = df.tail(CONFIG['TABLE_DAYS']).sort_index(ascending=False)
        table_df.index = table_df.index.strftime('%d-%m-%Y')
        st.dataframe(table_df[['Open','High','Low','Close','Change','Change %','Volume','RSI14','Signal']].style.format(precision=2))
    with col2:
        st.subheader("Backtest Results")
        st.code(summary, language=None)
        if backtest_df is not None:
            st.dataframe(backtest_df.style.format(precision=2))
    plot_df = df.tail(CONFIG['PLOT_DAYS']); latest = df.iloc[-1]
    ohlcv_text=(f"<b>{symbol.upper()}</b> {reason} O:<span style='color:#333;'>{latest['Open']:.2f}</span> H:<span style='color:#333;'>{latest['High']:.2f}</span> L:<span style='color:#333;'>{latest['Low']:.2f}</span> C:<span style='color:#333;'>{latest['Close']:.2f}</span> V:<span style='color:#333;'>{latest['Volume']/1e6:.2f}M</span>")
    vol_text=f"Volume: {latest['Volume']/1e6:.2f}M"; rsi_text=f"RSI({CONFIG['RSI_PERIOD']}): {latest['RSI14']:.2f}"
    macd_hist_color='green' if latest['MACD_Hist']>=0 else 'red'
    macd_text=(f"<b>MACD</b>({CONFIG['MACD_FAST']},{CONFIG['MACD_SLOW']},{CONFIG['MACD_SIGNAL']}) <span style='color:blue;'>{latest['MACD']:.2f}</span> <span style='color:orange;'>{latest['MACD_Signal']:.2f}</span> <span style='color:{macd_hist_color};'>{latest['MACD_Hist']:.2f}</span>")
    fig = make_subplots(rows=4, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=[0.60, 0.13, 0.13, 0.14])
    resistance_levels, support_levels = find_support_resistance(plot_df, CONFIG['SR_WINDOW'])
    for r in resistance_levels: fig.add_hline(y=r, line_width=1, line_dash="dash", line_color="rgba(255, 82, 82, 0.5)")
    for s in support_levels: fig.add_hline(y=s, line_width=1, line_dash="dash", line_color="rgba(0, 176, 240, 0.5)")
    fig.add_trace(go.Scatter(x=list(plot_df.index)+list(plot_df.index[::-1]),y=list(plot_df['BB_Upper'])+list(plot_df['BB_Lower'][::-1]),fill='toself',fillcolor='rgba(0,176,240,0.08)',line=dict(color='rgba(255,255,255,0)'),showlegend=False),row=1,col=1)
    fig.add_trace(go.Candlestick(x=plot_df.index,open=plot_df['Open'],high=plot_df['High'],low=plot_df['Low'],close=plot_df['Close'],showlegend=False),row=1,col=1)
    fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['EMA9'], mode='lines', name=f'EMA {CONFIG["EMA_SHORT"]}', line=dict(color='green',width=1)),row=1,col=1)
    fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['EMA21'], mode='lines', name=f'EMA {CONFIG["EMA_MEDIUM"]}', line=dict(color='red',width=1)),row=1,col=1)
    fig.add_trace(go.Scatter(x=plot_df.index, y=plot_df['Buy_Marker'], mode='markers', name='Buy Signal', marker=dict(color='lime',size=12,symbol='triangle-up')),row=1,col=1)
    vol_colors=['green' if r['Close']>=r['Open'] else 'red' for _,r in plot_df.iterrows()]; fig.add_trace(go.Bar(x=plot_df.index,y=plot_df['Volume'],marker_color=vol_colors,showlegend=False),row=2,col=1)
    fig.add_trace(go.Scatter(x=plot_df.index,y=plot_df['RSI14'],mode='lines',name='RSI',line=dict(color='green')),row=3,col=1); fig.add_trace(go.Scatter(x=plot_df.index,y=plot_df['RSI_EMA20'],mode='lines',name='RSI EMA',line=dict(color='fuchsia')),row=3,col=1)
    macd_colors=['green' if v>=0 else 'red' for v in plot_df['MACD_Hist']]; fig.add_trace(go.Bar(x=plot_df.index,y=plot_df['MACD_Hist'],marker_color=macd_colors,showlegend=False),row=4,col=1)
    fig.add_trace(go.Scatter(x=plot_df.index,y=plot_df['MACD'],mode='lines',name='MACD',line=dict(color='blue')),row=4,col=1); fig.add_trace(go.Scatter(x=plot_df.index,y=plot_df['MACD_Signal'],mode='lines',name='Signal',line=dict(color='orange')),row=4,col=1)
    annotations = [dict(text=ohlcv_text,align='left',showarrow=False,xref='paper',yref='paper',x=0.01,y=1.07)]
    annotations.extend([dict(xref='paper',yref='y2',x=0.01,y=plot_df['Volume'].max()*0.95,text=vol_text,showarrow=False,font=dict(color='black',size=12),xanchor='left'),
                        dict(xref='paper',yref='y3',x=0.01,y=95,text=rsi_text,showarrow=False,font=dict(color='black',size=12),xanchor='left'),
                        dict(xref='paper',yref='y4',x=0.01,y=plot_df['MACD'].abs().max()*0.95,text=macd_text,showarrow=False,font=dict(color='black',size=12),xanchor='left')])
    fig.update_layout(height=800,template='plotly_white',xaxis_rangeslider_visible=False,showlegend=True,legend=dict(orientation="h",yanchor="bottom",y=1.02,xanchor="right",x=1),yaxis_side='right',hovermode='x unified',annotations=annotations)
    fig.update_yaxes(side='right',showticklabels=True,row=2,col=1);fig.update_yaxes(side='right',showticklabels=True,row=3,col=1);fig.update_yaxes(side='right',showticklabels=True,row=4,col=1)
    st.plotly_chart(fig, use_container_width=True)

# --- STREAMLIT APP LAYOUT & LOGIC ---

# --- STREAMLIT APP LAYOUT & LOGIC (SYNTAX ERROR FIXED) ---

st.title("📈 DG Professional Stock Tool")

if 'found_stocks' not in st.session_state:
    st.session_state.found_stocks = []
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0

st.sidebar.header("Controls")
analysis_mode = st.sidebar.radio("Choose Analysis Mode", ["Screener", "Single Stock"])

if analysis_mode == "Screener":
    if st.sidebar.button("▶️ Run Full Screener"):
        st.session_state.found_stocks = []
        st.session_state.current_index = 0
        passing_stocks = []
        progress_bar = st.sidebar.progress(0)
        status_text = st.sidebar.empty()
        
        for i, symbol in enumerate(CONFIG['STOCKS']):
            status_text.text(f"Scanning: {symbol}")
            progress_bar.progress((i + 1) / len(CONFIG['STOCKS']))
            df_screener = get_stock_data_and_process(symbol)
            if df_screener is not None and check_scanner_conditions(df_screener):
                passing_stocks.append(symbol)
        
        status_text.success("Scan complete!")
        st.session_state.found_stocks = passing_stocks
        st.rerun()

else:  # Single Stock Mode
    selected_stock = st.sidebar.selectbox("Select a Stock", sorted(CONFIG['STOCKS']))
    if st.sidebar.button("🔎 Analyze Selected Stock"):
        st.session_state.found_stocks = [selected_stock]
        st.session_state.current_index = 0
        st.rerun()

if not st.session_state.found_stocks:
    st.info("Run the screener or select a single stock to begin analysis.")
else:
    # --- THIS IS THE CORRECTED LINE ---
    total_stocks = len(st.session_state.found_stocks)
    # --- END OF CORRECTION ---
    
    st.header(f"Analysis Results ({st.session_state.current_index + 1} of {total_stocks})")

    col1, _, col2 = st.columns([1, 8, 1])
    if col1.button("⬅️ Previous", disabled=(st.session_state.current_index <= 0)):
        st.session_state.current_index -= 1
        st.rerun()
    if col2.button("Next ➡️", disabled=(st.session_state.current_index >= total_stocks - 1)):
        st.session_state.current_index += 1
        st.rerun()

    # Ensure index is within bounds before accessing
    if 0 <= st.session_state.current_index < len(st.session_state.found_stocks):
        current_stock_symbol = st.session_state.found_stocks[st.session_state.current_index]
        with st.spinner(f"Loading data for {current_stock_symbol}..."):
            df_analysis = get_stock_data_and_process(current_stock_symbol)
            if df_analysis is not None:
                display_analysis(current_stock_symbol, df_analysis, reason="[Screener Match]")
            else:
                st.error(f"Could not load data for {current_stock_symbol}.")
    else:
        st.warning("No stock selected or index is out of bounds. Please run the screener again.")
