from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import TrendingFactModel, BenchmarkModel

def seed_database_if_empty(db: Session):
    existing_facts = db.query(TrendingFactModel).count()
    if existing_facts > 0:
        return  # Already seeded
        
    facts = [
        # --- NIGERIA (Primary Focus) ---
        TrendingFactModel(
            title="Petrol (PMS) Retail Price Benchmark",
            country="Nigeria",
            location="Lagos (Ikeja, Alausa, Ojota)",
            category="fuel_price",
            summary_en="Petrol is selling between ₦850 and ₦890 per litre across NNPC and major retail stations (Total, Conoil). Independent marketers are selling between ₦910 and ₦940. No major scarcity observed.",
            summary_pidgin="Fuel for Ikeja and Ojota dey sell between ₦850 and ₦890 for major stations like NNPC and Total. Black market no plenty, fuel dey pump normal. No need to panic buy.",
            summary_yoruba="Iroyin Epo: Epo petrol n ta laarin ₦850 si ₦890 fun lita ni awon ile-epo nla bi NNPC ati Total ni Ikeja. Ko si aini epo kankan.",
            summary_hausa="Farashin Fetur: Ana sayar da fetur tsakanin ₦850 zuwa ₦890 a manyan gidajen mai a Ikeja da Ojota. Babu dogon layi ko wahala.",
            summary_swahili="Bei ya Mafuta: Petroli inauzwa kati ya ₦850 na ₦890 kwa lita katika vituo vikuu vya mafuta.",
            summary_zulu="Intengo Kaphethiloli: Uphethiloli uthengiswa phakathi kuka-₦850 no-₦890 nge-litre eziteshini ezinkulu.",
            confidence_level="High",
            sources="42 Verified citizen reports + NMDPRA Retail Tracker + Field spot checks",
            action="Avoid roadside black market boys selling at ₦1,200. Report any station hoarding fuel above NMDPRA guidance.",
            report_count=42,
            upvotes=18,
            is_hot=True,
            updated_at=datetime.utcnow() - timedelta(minutes=24)
        ),
        TrendingFactModel(
            title="Garri (Yellow & White) Mile 12 & Bodija Market Rates",
            country="Nigeria",
            location="Lagos & Ibadan (Mile 12 & Bodija Markets)",
            category="food_staple",
            summary_en="One paint rubber of White Garri is selling at ₦2,200 - ₦2,400. Yellow Garri (Bendel) is ₦2,600 - ₦2,800. Price is stabilizing following new cassava harvests from Edo and Ogun states.",
            summary_pidgin="Paint bucket of white garri for Mile 12 dey go for ₦2,200 to ₦2,400 now. Yellow garri na around ₦2,700. Price don calm down small because new cassava don land.",
            summary_yoruba="Iye Ounje Garri: Roba garri funfun n ta fun ₦2,200 si ₦2,400. Garri pupa je ₦2,700 ni oja Mile 12. Owo ti bale die nitori isu gbaguda titun.",
            summary_hausa="Farashin Garri: Robar garri farar tana ₦2,200 zuwa ₦2,400 a kasuwar Mile 12. Farashi ya daidaita.",
            summary_swahili="Bei ya Garri: Ndoo ya Garri inauzwa kati ya ₦2,200 na ₦2,400 katika soko la Mile 12.",
            summary_zulu="Ukudla: I-Garri ithengiswa ngo-₦2,200 kuya ku-₦2,400 emakethe yase-Mile 12.",
            confidence_level="High",
            sources="31 Market women reports + Lagos State Consumer Price Index bulletin",
            action="Buy from inner market stalls rather than expressway gates to get the best wholesale rate.",
            report_count=31,
            upvotes=14,
            is_hot=True,
            updated_at=datetime.utcnow() - timedelta(hours=1, minutes=10)
        ),
        TrendingFactModel(
            title="Ikeja Electric Feeder Outage Update",
            country="Nigeria",
            location="Lagos (Oregun, Allen Avenue, Ikeja GRA)",
            category="power_status",
            summary_en="Temporary 33kV line tripping along the Maryland-Alausa injection substation. Ikeja Electric technicians are on site; power restoration expected by 4:00 PM.",
            summary_pidgin="NEPA line trip Maryland-Alausa side. Ikeja Electric people dey ground dey fix the cable. Light suppose show by 4:00 PM today.",
            summary_yoruba="Atunse Ina Monamona: Waya 33kV ja ni agbegbe Maryland-Alausa. Awon onise Ikeja Electric ti wa nibe lati tun se. Ina ma de ni ago merin irole.",
            summary_hausa="Gyaran Wutar Lantarki: Layin wuta ya katse a Maryland-Alausa. Ma'aikata suna aiki don dawo da wuta da karfe 4:00 na yamma.",
            summary_swahili="Kukatika kwa Umeme: Mafundi wanarekebisha njia ya umeme ya Maryland-Alausa. Umeme unatarajiwa kurejea saa kumi jioni.",
            summary_zulu="Ukucinywa Kukagesi: Abasebenzi balungisa izintambo zikagesi. Ugesi kulindeleke ukuthi ubuye ngo-4 ntambama.",
            confidence_level="Verified",
            sources="Ikeja Electric (IE) Customer Notice + 19 Resident confirmations",
            action="Turn off sensitive electronics before power returns to prevent surge damage.",
            report_count=19,
            upvotes=9,
            is_hot=True,
            updated_at=datetime.utcnow() - timedelta(minutes=45)
        ),
        TrendingFactModel(
            title="DEBUNKED: Rumor on Sudden Petrol Price Slash to ₦450",
            country="Nigeria",
            location="Nationwide (WhatsApp Viral Forward)",
            category="rumor_claim",
            summary_en="FALSE. A forwarded voice note claiming the Federal Government ordered an immediate reversal of petrol prices to ₦450/L is fake. NMDPRA and Ministry of Petroleum have confirmed no such circular exists.",
            summary_pidgin="FAKE NEWS: That voice note wey people dey forward say fuel don drop to ₦450 na pure lie. Government or NMDPRA no talk that kain thing. Make una warn people for family group.",
            summary_yoruba="IRO NI: Ohun igbasile ti awon eniyan n pin kakiri pe ijoba ti so pe epo petrol di ₦450 je iro funfun. Ko si iru ase bee lati odo ijoba.",
            summary_hausa="KARYA CE: Wani sautin murya da ake yadawa cewa gwamnati ta rage farashin fetur zuwa ₦450 ba gaskiya ba ne. Hukumar NMDPRA ta karyata labarin.",
            summary_swahili="HABARI ZA UONGO: Ujumbe wa sauti unaosambazwa ukidai bei ya petroli imeshuka hadi ₦450 si wa kweli. Mamlaka imekanusha madai hayo.",
            summary_zulu="AMABANGA AMANGA: Umyalezo ozwakalayo othi uhulumeni unciphise uphethiloli ube ngu-₦450 ngamanga.",
            confidence_level="Verified",
            sources="NMDPRA Official Press Statement + Premium Times FactCheck Desk",
            action="Share this debunk notice to any WhatsApp group forwarding the false voice note.",
            report_count=67,
            upvotes=45,
            is_hot=True,
            updated_at=datetime.utcnow() - timedelta(minutes=15)
        ),
        TrendingFactModel(
            title="50kg Bag of Foreign & Local Parboiled Rice",
            country="Nigeria",
            location="Abuja (Wuse & Utako Markets)",
            category="food_staple",
            summary_en="Local parboiled rice 50kg bag is averaging ₦78,000 to ₦82,000. Foreign long grain is averaging ₦88,000 to ₦94,000 across major distributors in Abuja.",
            summary_pidgin="Bag of local rice for Wuse market na between ₦78k and ₦82k. Foreign rice dey hover around ₦90k. Supply dey stable for now.",
            summary_yoruba="Iye Iresi: Apo iresi ibile 50kg wa laarin ₦78,000 si ₦82,000 ni oja Wuse ni Abuja.",
            summary_hausa="Farashin Shinkafa: Bukar shinkafar gida mai nauyin kilo 50 tana tsakanin ₦78,000 zuwa ₦82,000 a kasuwar Wuse da Utako.",
            summary_swahili="Bei ya Mchele: Mfuko wa kilo 50 wa mchele unauzwa kati ya ₦78,000 na ₦82,000 katika soko la Wuse mjini Abuja.",
            summary_zulu="Ilayisi: Isikhwama se-50kg selayisi sibiza phakathi kuka-₦78,000 no-₦82,000 e-Abuja.",
            confidence_level="High",
            sources="18 Wholesaler reports + FCT Consumer Price Monitor",
            action="Form cooperative buying groups with neighbors to purchase at distributor bulk price.",
            report_count=18,
            upvotes=11,
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=3)
        ),
        
        # --- KENYA ---
        TrendingFactModel(
            title="Super Petrol & Diesel EPRA Pump Price",
            country="Kenya",
            location="Nairobi (CBD, Westlands, Industrial Area)",
            category="fuel_price",
            summary_en="Super Petrol remains capped at KSh 188.84 per litre; Diesel at KSh 176.60 in Nairobi following EPRA's monthly pricing cycle. Rubis and Total stations adhering to official ceiling.",
            summary_pidgin="Petrol for Nairobi dey sell for KSh 188.84 per litre, diesel na KSh 176.60. All petrol stations dey follow the official government price.",
            summary_swahili="Bei Rasmi ya Mafuta: Petroli inauzwa kwa KSh 188.84 kwa lita, na Dizeli kwa KSh 176.60 jijini Nairobi kulingana na bei ya EPRA. Vituo vyote vinafuata mwongozo.",
            summary_yoruba="Owo Epo ni Kenya: Epo petrol duro ni KSh 188.84 fun lita ni ilu Nairobi gege bi ijoba EPRA se fi lele.",
            summary_hausa="Farashin Fetur a Kenya: Farashin fetur a Nairobi shine KSh 188.84 kan kowace lita karkashin ka'idar hukumar EPRA.",
            summary_zulu="Intengo Kaphethiloli e-Kenya: Uphethiloli e-Nairobi ubiza u-KSh 188.84 nge-litre ngokusho kwe-EPRA.",
            confidence_level="Verified",
            sources="EPRA Official Gazette + 28 Matatu driver reports",
            action="Report any station overcharging above EPRA maximum pump price via EPRA SMS hotline 22446.",
            report_count=28,
            upvotes=15,
            is_hot=True,
            updated_at=datetime.utcnow() - timedelta(hours=2)
        ),
        TrendingFactModel(
            title="2kg Maize Flour (Unga) Retail Rate",
            country="Kenya",
            location="Nairobi & Kisumu",
            category="food_staple",
            summary_en="A 2kg packet of premium maize meal (Jogoo, Pembe) is retailing between KSh 135 and KSh 150 across Naivas, Quickmart, and estate dukas.",
            summary_pidgin="2kg Unga (maize flour) for Nairobi supermarkets dey between KSh 135 and KSh 150. Food plenty for shelf.",
            summary_swahili="Bei ya Unga wa Mahindi: Pakiti ya kilo 2 ya unga (Jogoo, Pembe) inauzwa kati ya KSh 135 na KSh 150 katika maduka makuu kama Naivas na Quickmart.",
            summary_yoruba="Owo Ounje Unga: Apo unga 2kg n ta laarin KSh 135 si KSh 150 ni awon soobu nla ni ilu Nairobi.",
            summary_hausa="Farashin Unga: Kilo 2 na garin masara (Unga) yana tsakanin KSh 135 zuwa KSh 150 a manyan kantuna.",
            summary_zulu="Impuphu: I-Unga ye-2kg ibiza phakathi kuka-KSh 135 no-KSh 150 ezitolo ezinkulu zase-Nairobi.",
            confidence_level="High",
            sources="35 Citizen price submissions + Supermarket shelf surveys",
            action="Compare retail promotions between estate shops and supermarket chains before buying in bulk.",
            report_count=35,
            upvotes=8,
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=4)
        ),
        TrendingFactModel(
            title="Kenya Power (KPLC) Planned Maintenance Outage",
            country="Kenya",
            location="Nairobi (Kilimani, Lavington, Kileleshwa)",
            category="power_status",
            summary_en="Scheduled network maintenance ongoing until 5:00 PM. Affected areas include Dennis Pritt Rd, State House Crescent, and parts of Argwings Kodhek.",
            summary_pidgin="Kenya Power dey do maintenance work for Kilimani area till 5:00 PM today. Power go return once them finish work.",
            summary_swahili="Matengenezo ya Umeme (KPLC): Shughuli za matengenezo zinaendelea maeneo ya Kilimani na Lavington hadi saa kumi na moja jioni. Umeme utarejea punde baada ya kazi kukamilika.",
            summary_yoruba="Atunse Ina KPLC: Ile-ise ina Kenya Power n se atunse waya ni Kilimani titi di ago marun irole.",
            summary_hausa="Gyaran Wutar KPLC: Kamfanin Kenya Power yana aikin gyara a Kilimani har zuwa karfe 5:00 na yamma.",
            summary_zulu="Ukulungiswa Kukagesi: I-Kenya Power ilungisa izintambo kagesi e-Kilimani kuze kube u-5 ntambama.",
            confidence_level="Verified",
            sources="KPLC Scheduled Outage Notice + Kilimani Residents Association",
            action="Plan generator/inverter usage accordingly; KPLC helpline: 97771.",
            report_count=22,
            upvotes=12,
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=1, minutes=30)
        ),

        # --- SOUTH AFRICA ---
        TrendingFactModel(
            title="Unleaded 95 & Diesel Inland Fuel Prices",
            country="South Africa",
            location="Johannesburg & Pretoria (Gauteng Inland)",
            category="fuel_price",
            summary_en="Unleaded 95 petrol inland is R22.86 per litre; Diesel 50ppm is R21.15 per litre according to DMRE official determination. Sasol, Shell, and Engen stations standard.",
            summary_pidgin="Petrol for Joburg dey sell at R22.86 per litre, while diesel na R21.15. Price uniform across major stations.",
            summary_zulu="Intengo Kaphethiloli: Uphethiloli we-95 uthengiswa ngo-R22.86 nge-litre kanti idizili ingu-R21.15 eGoli ngokwesinqumo somnyango we-DMRE.",
            summary_swahili="Bei ya Mafuta Afrika Kusini: Petroli ya 95 inauzwa R22.86 kwa lita na dizeli ni R21.15 jijini Johannesburg.",
            summary_yoruba="Owo Epo ni South Africa: Epo petrol Unleaded 95 n ta fun R22.86 fun lita kan ni ilu Johannesburg.",
            summary_hausa="Farashin Fetur a Afirka ta Kudu: Ana sayar da fetur lita daya a kan R22.86 a Johannesburg.",
            confidence_level="Verified",
            sources="Department of Mineral Resources and Energy (DMRE) + Automobile Association (AA)",
            action="Check fuel rewards programs (e.g. FNB eBucks, Discovery Insure) to earn cash back at pumps.",
            report_count=29,
            upvotes=16,
            is_hot=True,
            updated_at=datetime.utcnow() - timedelta(hours=2, minutes=15)
        ),
        TrendingFactModel(
            title="Eskom National Grid & Load Shedding Status",
            country="South Africa",
            location="National (Eskom & City Power)",
            category="power_status",
            summary_en="Load shedding remains suspended nationwide due to sustained generation capacity. Local outages in Roodepoort are due to localized cable theft, not stage load shedding.",
            summary_pidgin="No national load shedding today! Power dey steady. Only small area for Roodepoort get issue because thiefs cut cable.",
            summary_zulu="Isimo Sikagesi (Eskom): Ukucinywa kukagesi (load shedding) kusamisiwe ezweni lonke. Ukucima kukagesi e-Roodepoort kubangelwa ukwebiwa kwezintambo.",
            summary_swahili="Hali ya Umeme Eskom: Hakuna mgao wa umeme (load shedding) kitaifa leo nchini Afrika Kusini. Umeme uko thabiti.",
            summary_yoruba="Ina Monamona ni South Africa: Ko si ikuna ina gbogbo orile-ede (load shedding) loni. Ina duro daadaa.",
            summary_hausa="Wutar Lantarki a Eskom: Babu dauke wuta a fadin kasar Afirka ta Kudu a yau.",
            confidence_level="High",
            sources="Eskom Media Briefing + City Power JHB Crisis Desk",
            action="Report cable vandalism or illegal connections to City Power Crime Stop: 0800 002 587.",
            report_count=48,
            upvotes=27,
            is_hot=True,
            updated_at=datetime.utcnow() - timedelta(minutes=50)
        ),
        TrendingFactModel(
            title="Rand Water Infrastructure Maintenance",
            country="South Africa",
            location="Johannesburg South & Soweto",
            category="water_status",
            summary_en="Water supply pressure in Crown Gardens and parts of Soweto is recovering after valve replacement at Eikenhof pump station. Full pressure expected within 12 hours.",
            summary_pidgin="Water pressure dey slowly return after repairs for Eikenhof pump station. Tap suppose dey flow normal by tonight.",
            summary_zulu="Uphiko Lwamanzi (Rand Water): Umfutho wamanzi ubuyela kancane kancane e-Crown Gardens nase-Soweto ngemuva kokulungiswa kwesiteshi se-Eikenhof.",
            summary_swahili="Ugavi wa Maji: Shinikizo la maji linarejea polepole katika maeneo ya Crown Gardens na Soweto baada ya ukarabati.",
            summary_yoruba="Iroyin Omi: Omi ti n pada bo ni sise ntele ni agbegbe Crown Gardens ati Soweto.",
            summary_hausa="Wadatar Ruwa: Ruwan famfo yana dawowa a hankali a yankunan Crown Gardens da Soweto.",
            confidence_level="Verified",
            sources="Johannesburg Water Operations + Ward 54 Councillor Bulletin",
            action="Keep emergency drinking water stored in clean closed containers.",
            report_count=17,
            upvotes=10,
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=3, minutes=20)
        )
    ]
    
    for f in facts:
        db.add(f)
        
    # Benchmarks
    benchmarks = [
        BenchmarkModel(
            country="Nigeria",
            category="fuel_price",
            item_name="Premium Motor Spirit (PMS / Petrol)",
            official_rate="₦850 - ₦900 / Litre (Major Marketers)",
            official_source="NMDPRA (Nigerian Midstream and Downstream Petroleum Regulatory Authority)",
            hotline_contact="NMDPRA Consumer Helpline: 0800-663-772 / contact@nmdpra.gov.ng"
        ),
        BenchmarkModel(
            country="Nigeria",
            category="food_staple",
            item_name="Garri (Ijebu / Yellow)",
            official_rate="₦2,200 - ₦2,600 / Paint Bucket (Lagos Markets)",
            official_source="Lagos State Bureau of Statistics Food Commodity Survey",
            hotline_contact="FCCPC Consumer Complaints: 0805-820-2020"
        ),
        BenchmarkModel(
            country="Nigeria",
            category="power_status",
            item_name="Electricity Distribution (Disco Tariff Band A-D)",
            official_rate="NERC Multi-Year Tariff Order (MYTO)",
            official_source="NERC / Disco Customer Service Desks",
            hotline_contact="NERC Complaints: complaints@nerc.gov.ng / 09-462-1400"
        ),
        BenchmarkModel(
            country="Kenya",
            category="fuel_price",
            item_name="Super Petrol & Diesel",
            official_rate="KSh 188.84 / L (Petrol), KSh 176.60 / L (Diesel)",
            official_source="EPRA (Energy and Petroleum Regulatory Authority Kenya)",
            hotline_contact="EPRA SMS Complaints: 22446"
        ),
        BenchmarkModel(
            country="South Africa",
            category="fuel_price",
            item_name="Petrol 95 Unleaded (Inland)",
            official_rate="R22.86 / Litre",
            official_source="Department of Mineral Resources and Energy (DMRE)",
            hotline_contact="DMRE Consumer Info: +27 12 406 8000"
        )
    ]
    
    for b in benchmarks:
        db.add(b)
        
    db.commit()
