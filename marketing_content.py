 python
    MARKETING_DB = {
        "brand": {
            "naam": "Giantpanda",
            "positionering": "AI WhatsApp Appointment Setters voor Nederlandse MKB",
            "headline": "Every Lead. Followed Up. Instantly.",
            "trefwoorden": ["afspraken", "WhatsApp", "AI-agent", "leadopvolging", "quote-automatisering", "Nederland", "MKB", "ZZP"],
            "tonality": "Alex Hormozi-stijl: direct, value-first, harde cijfers, geen fluff, ideal beliefs doorbreken",
        },
        "personas": {
            "judith": {
                "naam": "Drukke eigenaar Judith",
                "verkoopstraal": "Regionaal",
                "branche": "Bouw, Coach, Agency",
                "bedrijfsgrootte": "1-2 fte",
                "omzet": "10-50K p/m",
                "technisch": "laag",
                "pijnpunten": ["Chaos", "Geen vrije tijd", "In avond leads opvolgen", "Geen overzicht", "Niet schaalbaar"],
                "verlangens": ["Meer omzet", "Rust", "Vrijheid", "Passief inkomen", "Groeien zonder personeel"],
                "false_beliefs": ["Meer omzet betekent harder werken", "AI voelt onpersoonlijk", "Mijn klanten willen menselijk contact"],
                "cta_stijl": "laag-drempel: 'Plan gratis demo', 'Bekijk 2-min uitleg'",
            },
            "rick": {
                "naam": "Regelaar Rick",
                "verkoopstraal": "Nationaal / Interregionaal",
                "branche": "Installatietechniek, Agency, Bouwbedrijf",
                "bedrijfsgrootte": "1 fte + 3-8 zzp'ers",
                "omzet": "50K-150K p/m",
                "technisch": "gemiddeld",
                "pijnpunten": ["Kwaliteitsverlies door externen", "Communicatieruis", "Facturatie loopt achter", "doet zelf alle verkoop"],
                "verlangens": ["Systeem dat voor hem werkt", "Betrouwbaar team", "Kwaliteit borgen", "Rust in de kop"],
                "false_beliefs": ["Anderen doen het nooit zo goed als ik", "Automatisering is te rigide", "Kost te veel tijd om in te richten"],
                "cta_stijl": "direct testen: 'Start gratis', 'Bekijk voorbeeld voor installatiebedrijven'",
            },
            "alex": {
                "naam": "Ambitieuze Alex",
                "verkoopstraal": "Nationaal / Internationaal",
                "branche": "Agency, E-commerce, SaaS, Detachering",
                "bedrijfsgrootte": "10-25 fte",
                "omzet": "100K-500K p/m",
                "technisch": "hoog",
                "pijnpunten": ["Silo-vorming", "Hoge overhead", "Marketing & Sales praten niet", "Churn door trage opvolging"],
                "verlangens": ["Voorspelbare groei", "Data-driven beslissingen", "Efficiënte backoffice"],
                "false_beliefs": ["Onze processen zijn te complex", "We hebben al veel tools", "Veranderweerstand"],
                "cta_stijl": "strategisch: 'Plan strategie call', 'Bekijk integratiemogelijkheden'",
            },
            "victor": {
                "naam": "Vrijgevochten Victor",
                "verkoopstraal": "Internationaal / Grootschalig",
                "branche": "Gevestigde MKB, Productie, Vastgoedbeheer",
                "bedrijfsgrootte": "30-100 fte",
                "omzet": "500K+ p/m",
                "technisch": "laag-gemiddeld (delegeert IT)",
                "pijnpunten": ["Gebrek aan realtime inzicht", "Afhankelijkheid van key-employees", "Innovatie-schuld"],
                "verlangens": ["Passief inkomen", "Overdraagbaar bedrijf", "Impact maken"],
                "false_beliefs": ["Te groot om te veranderen", "Automatisering is voor kleine bedrijven", "Mijn personeel doet het al jaren zo"],
                "cta_stijl": "executive: 'Plan executive demo', 'Download business case'",
            },
        },
        "lp_teksten": {
            "judith": {
                "hero": {
                    "kop": "Stop met je weekends te verkopen.",
                    "subkop": "Je AI-agent reageert binnen 60 seconden op elke lead, filtert prijszoekers eruit en plant afspraken in — terwijl jij aan het werk bent. Geen extra personeel. Geen extra stress.",
                    "voordelen": [
                        "Binnen 1 minuut een reactie op elke aanvraag",
                        "Meer afspraken in je agenda, zonder dat jij hoeft te bellen",
                        "Eindelijk weer vrije avonden en rust in je hoofd",
                    ],
                    "ctas": ["Plan gratis 15-min demo", "Bekijk 2-min uitleg"],
                },
                "probleem_titel": "Je bent een eigenaar. Geen receptionist.",
                "oplossing_titel": "Stel je voor: leads worden opgevolgd terwijl jij klanten helpt.",
                "social_proof": [
                    {"naam": "Esther K.", "branche": "Schoonheidssalon", "quote": "Tijdens behandelingen miste ik de helft van mijn leads. Nu boekt de assistent 80% van de afspraken.", "metric": "+45% afspraken"},
                    {"naam": "Marco B.", "branche": "Schildersbedrijf Marco", "quote": "Ik zat tot 22:00 leads op te volgen. Nu plan ik 12 afspraken p/w zonder zelf een WhatsApp te sturen.", "metric": "12 afspraken p/w"},
                    {"naam": "Jeroen D.", "branche": "Personal Training", "quote": "Sinds de assistent direct reageert, mis ik geen enkele lead meer.", "metric": "3x hogere conversie"},
                ],
                "faq": [
                    {"vraag": "Mijn bedrijf is te klein voor dit soort tools.", "antwoord": "Daarvoor is het juist gemaakt. Binnen 2 minuten live, geen technische kennis nodig."},
                    {"vraag": "Is het nog steeds persoonlijk genoeg?", "antwoord": "De agent spreekt precies dezelfde taal als jij. Jij stelt de toon, hij volgt die exact op."},
                    {"vraag": "Heb ik tijd om het in te richten?", "antwoord": "Nee. Dat doen wij voor je. Jij geeft alleen je voorkeuren door en binnen 48 uur is het live."},
                    {"vraag": "Wat als ik geen WhatsApp Business API heb?", "antwoord": "Geen probleem. Je werkt eerst met een QR-code, geen API vereist."},
                ],
            },
            "rick": {
                "hero": {
                    "kop": "Elke Lead. Direct Opgevolgd. Zonder dat jij de tussenpersoon bent.",
                    "subkop": "Je AI-agent neemt de volledige opvolging over: van eerste reactie tot afspraak in je agenda. En je zzp'ers krijgen direct de juiste gegevens.",
                    "trust_badge": "4.9/5 — 500+ ondernemers — EU-gehost — AVG-proof",
                    "ctas": ["Start gratis", "Bekijk voorbeeld voor installatiebedrijven"],
                },
                "hoe_het_werkt_stappen": [
                    "Lead meldt zich aan via je website of formulieren",
                    "Binnen 60 seconden WhatsApp-reactie van jouw AI-agent",
                    "Agent stelt juiste vragen en geeft je team direct alle info",
                    "Afspraak staat in je agenda — zonder dat jij hoeft te plannen",
                ],
                "whatsapp_voorbeeld": {
                    "ai": "Hoi! Ik zag je aanvraag voor een cv-ketel. Heb je even tijd om 3 vragen te beantwoorden?",
                    "lead": "Ja zeker, wat wil je weten?",
                    "ai": "Top! Heb je een voorkeur voor datum en wat is je adres? Ik geef dat direct door aan onze monteur.",
                },
                "faq": [
                    {"vraag": "Werkt dit ook met mijn losse tools?", "antwoord": "Ja. 40+ integraties, waaronder WhatsApp, Excel, gedeelde agenda's en facturatiesoftware."},
                    {"vraag": "Kost het veel tijd om in te richten?", "antwoord": "Nee. Binnen 2 minuten live via QR-code. Daarna doen wij de rest."},
                    {"vraag": "Is mijn bedrijf niet te flexibel voor een vaste AI?", "antwoord": "De assistent leert jouw regels. Niet andersom."},
                ],
            },
            "alex": {
                "hero": {
                    "kop": "Meer omzet. Zelfde team. Geen payroll-explosie.",
                    "subkop": "Je leads worden binnen 60 seconden gekwalificeerd en direct in je CRM gezet. Marketing, sales en ops werken nu synchroon — zonder dat jij de tussenpersoon bent.",
                    "voordelen": [
                        "Directe opvolging van inkomende leads — altijd binnen 60 sec",
                        "Meer omzet uit dezelfde marketingbudget",
                        "Minder operationele rompslomp, meer schaalbaarheid",
                    ],
                    "ctas": ["Plan strategie call", "Bekijk integratiemogelijkheden"],
                },
                "probleem_titel": "Je hebt geen groeiprobleem. Je hebt een operatieprobleem.",
                "punten": [
                    {"kop": "CAPACITEIT", "tekst": "Marketing levert meer leads dan sales kan aan. Handmatige opvolging betekent dat 40% van je warme leads afkoelt voordat iemand reageert."},
                    {"kop": "PAYROLL", "tekst": "Iedere nieuwe groeifase dwingt je tot extra hires. Je overhead stijgt lineair, je omzet niet."},
                    {"kop": "DATA", "tekst": "CRM half gevuld. Slack, formulieren, WhatsApp — iedereen vertelt een ander verhaal."},
                    {"kop": "SNELHEID", "tekst": "Je bent te traag. De concurrent die binnen 5 minuten reageert, krijgt de deal."},
                ],
                "unit_economics": {
                    "zonder": [
                        "Lead wacht uren → waardevolle leads koelen af",
                        "CRM half gevuld → sales verspil tijd aan admin",
                        "Sales zoekt informatie → eindeloos kopiëren en plakken",
                        "Extra volume = extra personeel → overhead explodeert",
                    ],
                    "met": [
                        "Binnen 60 sec reactie → directe, gepersonaliseerde opvolging",
                        "Data automatisch compleet → elk lead-profile 100% accuraat in je CRM",
                        "Alles staat direct klaar → Agenda en CRM gevuld voordat jij het weet",
                        "Extra volume = zelfde team → schaal zonder payroll-groei",
                    ],
                },
                "social_proof": [
                    {"naam": "Wrapkampioen", "quote": "We besparen momenteel 2 fulltime medewerkers. Onze winst is met 20% gestegen.", "metrics": "-2 FTE | +20% winst"},
                    {"naam": "Uw Keuken Wrappen", "quote": "Onze tijd per offerte is verlaagd van 15 naar 2 minuten.", "metrics": "-13 min per offerte"},
                    {"naam": "Agency & Partners", "quote": "Ontvang 15% kickback op elke doorverwezen klant.", "metrics": "15% recurring kickback"},
                ],
                "faq": [
                    {"vraag": "Onze processen zijn te complex voor een out-of-the-box oplossing.", "antwoord": "De assistent leert jouw exacte workflow. Van intakevragen tot CRM-velden — alles past bij jouw proces."},
                    {"vraag": "We hebben al 7 tools. Waar zouden we nog een tool bij moeten nemen?", "antwoord": "Giantpanda vervangt niets. Het voegt een laag van conversie-automatisering toe op je bestaande stack."},
                    {"vraag": "Veranderweerstand bij mijn team?", "antwoord": "De assistent neemt het repetitieve werk over: opvolgen, boekingen, data-entry. Je team kan zich richten op wat echt waarde toevoegt."},
                ],
            },
            "victor": {
                "hero": {
                    "kop": "Bouw een bedrijf dat draait. Ook als jij er niet bent.",
                    "subkop": "Verhoog je operationele hefboomwerking, verminder afhankelijkheid van sleutelpersonen en maak je bedrijf exit-proof. Zonder 2-jaars IT-projecten.",
                    "cta": "Plan executive demo",
                    "trust_elementen": ["300+ bedrijven", "4.9/5 rating", "EU-gehost", "AVG-proof", "audit-log"],
                },
                "probleem_titel": "Wat gebeurt er als jij drie maanden weg bent?",
                "oplossing_titel": "Een organisatie die functioneert zonder constante sturing.",
                "oplossingspunten": [
                    {"titel": "Processen draaien zelfstandig", "tekst": "Dagelijkse taken worden autonoom afgehandeld, fouten met 80% terug."},
                    {"titel": "Realtime inzicht", "tekst": "Live dashboards in plaats van wachtende rapportages."},
                    {"titel": "Schalen zonder payroll", "tekst": "Verhoog volume met 40% zonder extra backoffice."},
                    {"titel": "Hogere winstgevendheid", "tekst": "Operationele hefboomwerking stijgt, marges verbeteren."},
                    {"titel": "Exit-proof", "tekst": "Een onafhankelijk draaiend bedrijf is 2-3x meer waard bij verkoop."},
                ],
                "metrics": [
                    "30-70% minder handmatige taken per medewerker",
                    "Nul kritieke processen stilvallen bij afwezigheid van sleutelpersoneel",
                    "+40% capaciteit zonder extra FTE",
                    "100% inzicht in de volledige operatie via live dashboard",
                ],
                "faq": [
                    {"vraag": "Is onze procesvoering niet te specifiek?", "antwoord": "Onze assistenten trainen we op jouw exacte bedrijfsregels, protocollen en uitzonderingen."},
                    {"vraag": "Veroorzaakt dit downtime?", "antwoord": "Nul downtime. Implementatie gebeurt parallel aan je huidige processen."},
                    {"vraag": "Zit er vertrouwen in een AI bij onze klanten?", "antwoord": "De AI communiceert in jouw merk- en toon. Klanten merken geen verschil — alleen snellere responstijden."},
                    {"vraag": "Wat als het niet levert?", "antwoord": "Geen meetbare verbetering in 90 dagen? Dan terugbetaling van de eerste 3 maanden."},
                ],
            },
        },
        "hooks": {
            "judith": [
                "Stop met je weekends te verkopen.",
                "Je AI-agent werkt ook als jij slaapt.",
                "Meer afspraken. Minder werk. Meer vrije tijd.",
                "Elke lead verdient een antwoord binnen 60 seconden.",
            ],
            "rick": [
                "Elke Lead. Direct Opgevolgd. Zonder dat jij de tussenpersoon bent.",
                "Stop met informatie door te geven. Laat de software het doen.",
                "Je zzp'ers krijgen direct de juiste gegevens. Jij ook.",
                "Binnen 2 minuten live. Zonder ingewikkelde setup.",
            ],
            "alex": [
                "Meer omzet. Zelfde team. Geen payroll-explosie.",
                "Je hebt geen groeiprobleem. Je hebt een operatieprobleem.",
                "Marketing levert leads. Sales mist ze. Stop dat.",
                "Schaal zonder te huren. Automatiseer wat repetitief is.",
            ],
            "victor": [
                "Bouw een bedrijf dat draait. Ook als jij er niet bent.",
                "Wat gebeurt er als jij drie maanden weg bent?",
                "Je bedrijf is pas echt waardevol als het zonder jou draait.",
                "Operationele hefboomwerking > meer mensen.",
            ],
        },
        "faq_generiek": [
            {"vraag": "Hoe werkt het?", "antwoord": "Je beschrijft je bedrijf, wij bouwen je AI-agent, jij scant een QR-code en bent binnen 2 minuten live."},
            {"vraag": "Heb ik WhatsApp Business API nodig?", "antwoord": "Nee. Je kunt starten met een QR-code, geen API vereist."},
            {"vraag": "Hoeveel integraties hebben jullie?", "antwoord": "40+ integraties, waaronder HubSpot, Salesforce, Google Sheets, Zapier, Calendly en Stripe."},
            {"vraag": "Kan ik de gesprekken aanpassen?", "antwoord": "Ja. Je agent spreekt precies dezelfde taal als jij. Jij stelt de toon, wij bouwen hem in."},
            {"vraag": "Is support inbegrepen?", "antwoord": "Ja. Elke klant heeft een vaste contactpersoon. Geen chatbots als support."},
        ],
    }
    
    def get_marketing_content(section, key=None):
        if section == "all":
            return MARKETING_DB
        if section in MARKETING_DB:
            data = MARKETING_DB[section]
            if key and key in data:
                return data[key]
            return data
        return None
    
    
