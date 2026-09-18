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
