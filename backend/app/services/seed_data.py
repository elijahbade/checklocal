from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models import TrendingFactModel, BenchmarkModel

def seed_database_if_empty(db: Session, force_refresh: bool = False):
    existing_facts = db.query(TrendingFactModel).count()
    
    # Check if PowerWatch feeders already exist
    power_facts = db.query(TrendingFactModel).filter(TrendingFactModel.feeder_name.isnot(None)).count()
    if existing_facts > 0 and power_facts >= 3 and not force_refresh:
        return  # Already seeded with powerwatch data
        
    if force_refresh or power_facts < 3:
        # Clear existing to ensure clean consistent schema
        db.query(TrendingFactModel).delete()
        db.query(BenchmarkModel).delete()
        db.commit()
        
    facts = [
        # --- POWERWATCH: NIGERIA FEEDER AUDITS (Primary Focus) ---
        TrendingFactModel(
            title="Magodo Phase 2 33kV Feeder: Band A Tariff Under-Delivery Audit",
            country="Nigeria",
            location="Lagos (Magodo Phase 2, Shangisha, CMD Road)",
            category="power_status",
            summary_en="DisCo (Ikeja Electric) is billing connected consumers at Band A rates (₦206.80/kWh) requiring ≥ 20.0 hrs/day. Crowdsourced meter telemetry across 48 verified accounts corroborates an actual 14-day average of only 6.8 hrs/day (13.2-hr daily deficit). Formal NERC Dispute Docket generated demanding SCADA subpoena and tariff downgrade.",
            summary_pidgin="Ikeja Electric dey charge Magodo Phase 2 people Band A rate of ₦206.80/kWh wey suppose get 20 hours light every day, but community light average na only 6.8 hours. Overbilling dispute petition don ready for NERC Forum Office.",
            summary_yoruba="Iroyin Ina Magodo: Ile-ise Ikeja Electric n gba owo Band A (₦206.80/kWh) ti o ye ki o fun ni wakati ogun (20h), sugbon wakati mefa pere (6.8h) ni ina n de. A ti ko iwe ejo si NERC.",
            summary_hausa="Binciken Wutar Magodo: Kamfanin Ikeja Electric yana cajin kudin Band A na ₦206.80/kWh wanda ya kamata a ba da wuta ta awa 20 a rana, amma awa 6.8 kacal ake samu. An shirya takardar korafi zuwa NERC.",
            summary_swahili="Uchunguzi wa Umeme Magodo: Kampuni ya umeme inatoza viwango vya juu vya Band A kwa ahadi ya masaa 20 ya umeme, lakini inatoa masaa 6.8 pekee kwa siku.",
            summary_zulu="Ukucwaningwa Kukagesi: Inkampani kagesi ibiza intengo ephezulu ye-Band A ngesithembiso samahora angama-20, kodwa inikeza amahora angama-6.8 kuphela.",
            confidence_level="Verified",
            sources="48 Corroborated Smart Meters + Feeder Substation Telemetry Audit + NERC MYTO Baseline",
            action="Download official NERC Dispute Docket #PW-NERC-2026-IKEDC-042 to join the collective tariff refund petition.",
            report_count=48,
            upvotes=34,
            is_hot=True,
            # PowerWatch Feeder Attributes
            feeder_name="Magodo Phase 2 33kV Feeder",
            disco_name="Ikeja Electric Plc",
            tariff_band="Band A (Statutory ≥ 20.0 hrs/day)",
            promised_hours="20.0",
            actual_hours_avg="6.8",
            overbilling_differential="₦138.80 / kWh overcharge",
            docket_ready=True,
            docket_number="PW-NERC-2026-IKEDC-042",
            updated_at=datetime.utcnow() - timedelta(minutes=18)
        ),
        TrendingFactModel(
            title="Gwarinpa 11kV Feeder: AEDC Band A Tariff Breach & Refund Demand",
            country="Nigeria",
            location="Abuja FCT (Gwarinpa Estate, 1st - 7th Avenues)",
            category="power_status",
            summary_en="AEDC is billing Gwarinpa residents at Band A (₦209.50/kWh) while delivering an average of 5.2 hrs/day across 64 monitored meters. Precedent: NERC previously fined AEDC ₦200M for overbilling non-qualifying feeders. Collective docket ready for submission to NERC Abuja Forum Office.",
            summary_pidgin="AEDC dey bill Gwarinpa at Band A (₦209.50/kWh) but light average na only 5.2 hours daily. Remember say NERC don fine AEDC ₦200 million before for this same overbilling. Download petition to demand your token refund.",
            summary_yoruba="Iroyin Ina Abuja Gwarinpa: AEDC n gba owo Band A ₦209.50/kWh sugbon wakati marun (5.2h) pere ni ina n wa. NERC ti gba itanran ₦200m lowo AEDC ri lori iru e.",
            summary_hausa="Hukuncin Wutar Gwarinpa: AEDC na cajin kudin Band A na ₦209.50/kWh alhali wuta awa 5.2 kacal take zuwa a rana. An shirya takardar shigar da kara ga NERC.",
            summary_swahili="Mgogoro wa Ushuru wa Umeme Abuja: AEDC inatoza kiwango cha juu cha Band A wakati umeme unapatikana kwa masaa 5.2 tu kwa siku.",
            summary_zulu="Ukubizwa Kwezindleko Ezingekho Emthethweni: I-AEDC ibiza intengo ephezulu kanti ugesi ufika amahora ama-5.2 kuphela ngosuku.",
            confidence_level="Verified",
            sources="64 Corroborated Resident Meters + NERC Enforcement Records + Estate HOA Log",
            action="Generate NERC Regulatory Petition #PW-NERC-2026-AEDC-019 to compel AEDC to refund overbilled token units.",
            report_count=64,
            upvotes=51,
            is_hot=True,
            # PowerWatch Feeder Attributes
            feeder_name="Gwarinpa 11kV Radial Feeder",
            disco_name="Abuja Electricity Distribution Company (AEDC)",
            tariff_band="Band A (Statutory ≥ 20.0 hrs/day)",
            promised_hours="20.0",
            actual_hours_avg="5.2",
            overbilling_differential="₦141.50 / kWh overcharge",
            docket_ready=True,
            docket_number="PW-NERC-2026-AEDC-019",
            updated_at=datetime.utcnow() - timedelta(minutes=42)
        ),
        TrendingFactModel(
            title="Lekki Phase 1 Express 33kV Feeder: Band A Supply Deficit",
            country="Nigeria",
            location="Lagos (Lekki Phase 1, Admiralty Way)",
            category="power_status",
            summary_en="Eko DisCo (EKEDC) Lekki Phase 1 feeder recorded 8.5 hrs/day average over 30 days against statutory 20-hour Band A threshold. Community audit of 52 verified meters shows 57.5% supply shortfall. Petition requests immediate reclassification to Band C.",
            summary_pidgin="EKEDC Lekki Phase 1 feeder dey give 8.5 hours instead of 20 hours Band A entitlement. Overbilling differential na ₦138.80 per kWh. Legal docket ready for NERC Lagos Forum.",
            summary_yoruba="Iroyin Ina Lekki: Ile-ise EKEDC n fun Lekki Phase 1 ni wakati 8.5 pere dipo wakati 20 ti won gba owo le lori. Iwe ejo ti se tan.",
            summary_hausa="Wutar Lekki Phase 1: Kamfanin EKEDC yana ba da wuta ta awa 8.5 a maimakon awa 20. An fara binciken doka.",
            summary_swahili="Uchunguzi wa Umeme Lekki: Usambazaji wa umeme ni masaa 8.5 badala ya masaa 20 yaliyoahidiwa chini ya Band A.",
            summary_zulu="Ukushoda Kukagesi: Abathengi bathola amahora ayi-8.5 esikhundleni samahora angama-20 ngaphansi kwe-Band A.",
            confidence_level="High",
            sources="52 Verified Prepaid Meters + Admiralty Ratepayers Outage Registry",
            action="Join Lekki Ratepayers Coalition on Docket #PW-NERC-2026-EKEDC-077 to enforce Band C reclassification.",
            report_count=52,
            upvotes=39,
            is_hot=True,
            feeder_name="Lekki Phase 1 Express 33kV Feeder",
            disco_name="Eko Electricity Distribution Company (EKEDC)",
            tariff_band="Band A (Statutory ≥ 20.0 hrs/day)",
            promised_hours="20.0",
            actual_hours_avg="8.5",
            overbilling_differential="₦138.80 / kWh overcharge",
            docket_ready=True,
            docket_number="PW-NERC-2026-EKEDC-077",
            updated_at=datetime.utcnow() - timedelta(hours=1, minutes=15)
        ),

        # --- POWERWATCH: SOUTH AFRICA MUNICIPAL TARIFF AUDIT ---
        TrendingFactModel(
            title="City Power JHB: Alexandra Grid Load Reduction & Unlawful Surcharge",
            country="South Africa",
            location="Johannesburg (Alexandra & Sandton Border)",
            category="power_status",
            summary_en="City Power is subjecting township consumers to unnotified 8-hour daily load reduction alongside an unapproved municipal surcharge. Precedent: Pretoria High Court (AfriForum v NERSA) ruled municipal tariff approvals without compliant Cost-of-Supply studies unconstitutional. NERSA dispute docket active.",
            summary_pidgin="City Power for Joburg dey cut light 8 hours daily for Alexandra and dey charge extra municipal fee wey Pretoria High Court talk say illegal because no Cost-of-Supply study. Dispute docket ready for NERSA.",
            summary_zulu="Isinqumo Senkantolo: Inkantolo Ephakeme yase-Pretoria (AfriForum v NERSA) inqume ukuthi izindleko zikagesi zikamasipala ezingenazo izifundo ze-Cost-of-Supply azikho emthethweni. Ugesi ucinywa amahora ayisi-8 e-Alexandra.",
            summary_swahili="Mgogoro wa Umeme Johannesburg: Mahakama Kuu ya Pretoria iliamua kuwa viwango vya umeme vya manispaa bila utafiti wa gharama si halali.",
            summary_yoruba="Iroyin Ina South Africa: Ile-ejo giga Pretoria ti pase pe owo ina afikun ti ijoba ibile gba lai se iwadi je arufin.",
            summary_hausa="Wutar Afirka ta Kudu: Kotun Pretoria ta yanke hukuncin cewa karin kudin wutar lantarki ba tare da cikakken bincike ba haramun ne.",
            confidence_level="Verified",
            sources="38 Corroborated Meters + Pretoria High Court Ruling (AfriForum v NERSA) + City Power Switching Logs",
            action="Lodge objection with NERSA via Docket #PW-NERSA-2026-JHB-008 to challenge unlawful municipal surcharge.",
            report_count=38,
            upvotes=26,
            is_hot=True,
            feeder_name="Alexandra Municipal Distribution Network",
            disco_name="City Power Johannesburg / Eskom",
            tariff_band="Municipal Domestic Surcharge",
            promised_hours="24.0",
            actual_hours_avg="16.0",
            overbilling_differential="R200 / month unlawful surcharge",
            docket_ready=True,
            docket_number="PW-NERSA-2026-JHB-008",
            updated_at=datetime.utcnow() - timedelta(hours=2)
        ),

        # --- VERIFIED CIVIC BENCHMARKS (Nigeria & Regional) ---
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
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=2, minutes=24)
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
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=3, minutes=10)
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
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=4)
        ),
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
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=5)
        ),
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
            is_hot=False,
            updated_at=datetime.utcnow() - timedelta(hours=6)
        )
    ]
    
    for f in facts:
        db.add(f)
        
    # Benchmarks
    benchmarks = [
        BenchmarkModel(
            country="Nigeria",
            category="power_status",
            item_name="NERC Band A Electricity Tariff Statutory Minimum",
            official_rate="20.0 Hours/Day Mandatory Minimum (Tariff: ₦206.80 – ₦209.50/kWh)",
            official_source="NERC Supplementary Order to MYTO & Section 63 Electricity Act 2023",
            hotline_contact="NERC Complaints: complaints@nerc.gov.ng / 09-462-1400"
        ),
        BenchmarkModel(
            country="South Africa",
            category="power_status",
            item_name="Municipal Electricity Tariff & Cost-of-Supply Mandate",
            official_rate="Cost-of-Supply (CoS) Study Approval Required by High Court",
            official_source="Pretoria High Court Ruling (AfriForum v NERSA) & Electricity Regulation Act",
            hotline_contact="NERSA Compliance: +27 12 401 4600 / complaints@nersa.org.za"
        ),
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
