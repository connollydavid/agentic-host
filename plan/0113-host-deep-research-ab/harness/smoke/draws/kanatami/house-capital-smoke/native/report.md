# The Capital of France and the River That Runs Through It
### Final Deep-Research Report — web-search-deep protocol

**Question:** *What is the capital of France, and which river runs through it?*
**Date of research:** 2026-11-28 · **Cycles:** Phase 2 (5 parallel queries) + Phase 4 feedback loops 1–5 (8 workers) · **Distinct sources consulted:** ≈95 (≈55 fetched or verbatim-captured)
**Corpus:** `research/01-plan.md`, `research/02-raw/*` (9 worker dumps), `research/03-intermediate.md`, `research/04-loops/loop-01…05.md`

---

## 1. Executive Summary (TL;DR)

**The capital of France is Paris, and the river that runs through it is the Seine (la Seine).** Across five research cycles and roughly 95 sources — including the European Union's official country page, the French government's terminology decree of 4 November 1993, the official City of Paris dossier on the Seine, the Sandre national hydrography registry, and UNESCO's World Heritage documentation — the answer was unanimous and uncontested. Paris, population 2.05 million in the city proper and 13.3 million in its metropolitan area, has been France's capital since at latest the 12th century; the Seine, 775–777 km long, rises in the Langres plateau, divides Paris into its famous Left and Right Banks over 13 intra-muros kilometres spanned by 37 bridges, and empties into the English Channel at Le Havre–Honfleur. The research also stress-tested the answer against every plausible complication — the buried Bièvre, the tributary Marne, Versailles and Vichy as rival seats of government, constitutional silence on capitals, and conflicting river statistics — and each was resolved without shaking the core result.

---

## 2. Background / Context

The question joins two elementary geographical facts, but elementary facts deserve verification, and their full answers carry genuine subtlety:

1. **"Capital" is not constitutionally defined in France.** The Fifth Republic's constitution (4 October 1958) names no capital; no French constitution since 1791 has done so (Delledonne 2024; Council of Europe report CPL(14)4REP). Paris's status rests on a stack of statutory, terminological, historical and conventional foundations — which the protocol's loops were designed to map.
2. **"The river of Paris" invites disambiguation.** The Seine's two largest tributaries touch the city's thresholds (Marne) or historically ran inside it (Bièvre, now subterranean), and open-data datasets can mislabel arrondissement centroids as riverside towns. A rigorous answer must show the Seine is the *unique* correct reading.

Methodology per the web-search-deep protocol: Phase 1 planning (5 must-have queries, gap-driven nice-to-haves); Phase 2 parallel search by 5 `web-search-worker` subagents; Phase 3 intermediate synthesis with contradiction ledger (C1–C9) and gap list (G1–G7); Phase 4 five feedback loops (official capital sources, Sandre registry, river ranking, edge-case rivers, historical intermezzos, UNESCO/current-status closure); Phase 5 this synthesis. Stated deviation: the English report target of 7,000 words is disproportionate to a two-fact question; per the plan's documented assumption, the deliverable meets the ≥10,000-character floor at full evidentiary density instead of filler.

---

## 3. Key Findings (with evidence mapping)

**KF-1. Paris is the capital of France. — Confidence: Very High (unanimous; ≥7 independent source classes).**
Evidence: EU official country page, "Capital: Paris" (updated 16 Oct 2026) [P2-Q1.1]; EN Wikipedia, "Paris is the capital and largest city of France… 2,047,602 (Jan 2026)… metro 13.32 million (2023)" [P2-Q1.2]; French State — *arrêté du 4 novembre 1993* annex, column "CAPITALE ou siège du gouvernement": "France (la) … **Paris**" [L1a.1–5]; Ministère de l'Intérieur civic-training dossier: "Paris est la capitale de la France" [L1a.7]; Île-de-France prefecture dossier [L1a.8]; Sénat, minister 2016: "ville-capitale, siège des institutions de la République" [L1a.12]; MEAE/CILF toponym recommendation, JO 2008 & 2019 [L1a.6]; WorldAtlas [P2-Q1.4]; National Geographic [P2-Q1.5]. Contradictions found: **zero.**

**KF-2. The Seine is the river that runs through Paris. — Confidence: Very High (unanimous).**
Evidence is anchored by the City of Paris itself: "la Seine… fait vibrer **la capitale** le long de ses **37 ponts** répartis sur les **13 kilomètres** qu'elle parcourt intra-muros" [P2-Q2.1]. Corroborated by EN/FR Wikipedia [P2-Q2.2, L1b.5], Larousse [P2-Q3.3], ESA satellite imagery ("the most defining geographical feature is the Seine River… winds through the centre") [P2-Q2.5], UNESCO SOUV ("The city of Paris is built along a bend in the River Seine") [P2-Q5.1], Ministère de l'Intérieur ("grandes villes traversées : Troyes, **Paris**, Rouen et Le Havre") [P2-Q3.7]. The Marne joins only at Charenton/Alfortville, outside city limits [L3b]; the Bièvre has been buried since 1912 [L3a]; no source anywhere in the corpus dissents.

**KF-3. The Seine in Paris — key verified parameters.**
13 km intra-muros; width 30 m (quai Montebello) to 200 m (pont de Grenelle); depth 3.40–5.70 m; 37 bridges; normal discharge ≈330 m³/s (HydroPortail interannual 309–317 m³/s); normal gauge height at Austerlitz 1–2 m; record modern flood 8.62 m (28 Jan 1910; peak discharge ~2,400–2,650 m³/s) [P2-Q2.1, L2a]. The widely repeated "average depth 9.5 m" is a low-authority outlier (en.wikipedia→Britannica chain, amplified only by content aggregators) — **rejected in favour of the official 3.40–5.70 m band.**

**KF-4. The Seine overall — key verified parameters.**
Length 775–777 km (Sandre registry fiche "----0010": 775 km / 774.76 km depending on vintage; commonly cited 777); source at Source-Seine, Côte-d'Or, Langres plateau (~446–471 m, sources vary); mouth in the English Channel between Le Havre and Honfleur; basin ≈75,000–79,000 km²; main stem crosses 12–13 départements and 4 regions; navigable by ocean vessels to Rouen, by barge from Marcilly-sur-Seine; principal tributaries Yonne, **Marne** (longest, 514.26 km, supplying ~⅓ of the Seine's flow at Paris), **Oise**, Aube, Loing, Eure; name from Gaulish *Sēquana*, the Celtic river goddess whose statues were found at the source [P2-Q2.2, P2-Q3.1/3.2, L1b, L2b, L3b].

**KF-5. Paris's capital status: three complementary senses, all pointing to Paris.**
(i) *Popular/historical*: capital from Clovis (508), with prior Frankish seats Tournai and Soissons acknowledged; (ii) *Scholarly/administrative*: capital "incontestably since the 12th century", crystallising under Philippe Auguste (Louvre, royal archives fixed at the Palais de la Cité, sedentarised *Curia regis*); first use *caput regni* (Rigord; Guillaume le Breton, 1224); (iii) *Legal*: constitution silent, but ordonnance n° 58-1100 art. 1er fixes both chambers in Paris, the 1993 arrêté recommends "Paris" as France's capital, and government may transfer the *seat of public powers* in emergencies "without that necessarily constituting a change of capital" [P2-Q1.3, P2-Q4.1–5, L1a, L4b].

**KF-6. Historical seat-of-government shifts never displaced Paris's capital status.**
Versailles was the seat of government 1682–1715, 1722–1789 and again 1871–1879 — "sans que Paris ne perde son titre de capitale" (Château de Versailles, official) — and the 1875 constitutional law even fixed the seat at Versailles until abrogated in 1879, the return justified as "rendre à la France **sa capitale séculaire, sa capitale nécessaire**" (Assemblée nationale, rapport 2226). Wartime withdrawals (Tours/Bordeaux 1870, 1914, 1940; Vichy 1940–44 "capitale de facto… Paris reste toujours capitale de jure"; Free France's Brazzaville/Alger; Bayeux 1944) likewise left the capital untouched; the GPRF returned definitively on 31 August 1944 [L4a, L4b].

**KF-7. The Seine defines Paris physically and legally — UNESCO "Paris, Banks of the Seine".**
Inscribed 1991 under criteria (i)(ii)(iv); the 2024 minor boundary modification (Decision **46 COM 8B.39**, New Delhi) expanded the property from 365 ha to 531 ha (538 ha as recorded on the List page), now running from the viaduc d'Austerlitz to the pont de Bir-Hakeim and including the Île aux Cygnes, with a 3,194 ha buffer zone following roughly the Wall of the Ferme Générale; a dedicated management plan remains a standing Committee demand [P2-Q5.1–2, L5a].

**KF-8. The Seine today: post-Olympic renaissance.**
Swimming — banned since 1923 — reopened in Paris on 5 July 2025 at Bercy, Grenelle and the Bras Marie; 2026 saw eight permanent sites across Île-de-France, ≈260,000 swimmers in natural zones (116,000–120,000 in Paris, +20%), the Plan Baignade at €1.1–1.4 billion invested since 2016, and a new €850 M downstream programme to 2040; ecological recovery: 36 fish species vs 14 in 1990 [P2-Q2.1, L5b].

---

## 4. Detailed Analysis by Sub-topic

### 4.1 Paris as capital — identity and institutions
Paris is the capital and largest city of France (2,047,602 inhabitants, 1 January 2026, in 105.4 km²; urban 11.0 M; metropolitan 13.3 M — 1st in France, 9th in Europe), prefecture of the Île-de-France region, a unique combined commune-département split into 20 arrondissements. The president (Élysée), prime minister (Matignon), both parliamentary chambers (Bourbon, Luxembourg) and international bodies (UNESCO, OECD, BIPM, IEA, OIF, ESA, EBA, ESMA) sit there. Its capital trajectory runs: Parisii settlement on the Seine c. 250–225 BC → Roman Lutetia (defeated 52 BC by Labienus; *Civitas Parisiorum* by 305 AD; briefly a western-imperial seat under Julian 360) → Clovis makes it the Frankish capital (508; buried there 511; kept as undivided dynastic symbol by his successors) → Carolingian neglect (Aachen) → Capetian recovery (987), decisive under **Philippe Auguste** (1180–1223) → English occupation and Loire-valley absence, restored by **François I (1528)** → Versailles shadow (1682–1789) → revolutionary return (October 1789) → revolutionary/republican convulsions (Commune 1871; Versailles interlude to 1879) → unambiguous national capital from 1944–58 onward, formally *not* a capital of the "V Republic" any more or less than of any regime — "the only capital of France since 1944: Paris", as the French wiki chronology puts it, with Vichy dismissed as never legally capital.

Legally, France is the archetype of the "conventional capital" (Council of Europe phrasing): silent constitutions + statutory seat (art. 1, ord. 58-1100) + terminological designation (arrêté 1993 "recommandée", carried forward by CILF lists of 2008/2019) + administrative usage (Ministère de l'Intérieur civic teaching materials) + universal international recognition (UN, EU). Emergency transfer of the *siège des pouvoirs publics* is constitutionally anticipated (via that ordonnance and art. 16 practice) yet never invoked under the Fifth Republic — no historical case was found.

### 4.2 The Seine — hydrography of "la Traversée de Paris"
The Seine is a northern-French river rising in the commune of Source-Seine (Côte-d'Or), ~30 km NW of Dijon, on the Langres plateau (grotto laid out over the spring; property of the City of Paris since 1864; Gallo-Roman sanctuary of *dea Sequana*). The registry lineage (Sandre code ----0010, spanning two hydrographic regions, hence the "----" prefix) records ~775 km; guidebooks and older encyclopedias give up to 781 km. The river's course is conventionally five-part: Petite Seine, Haute Seine (Montereau→Paris), **Traversée de Paris**, Basse Seine (Paris→Rouen), Seine maritime (Rouen→estuary). Within Paris the Seine's gentle gradient (only ~24 m above sea level even 446 km inland) produces the slow, tamed, lock-regulated reach the city built its identity on: 13 km, 30–200 m wide, 3.40–5.70 m deep, ~330 m³/s, regime oceanic-pluvial (winter highs, summer lows; reservoirs of the Seine Grands Lacs maintain ≥~60 m³/s in drought). Flood memory: 1910 (8.62 m at Austerlitz, the *crue de référence*/PHEC), 1924 (7.32 m), 1945, 1955, 1982, 2016 (6.10 m), 2018 (5.88 m); July 2026 marked the lowest monthly flow since 1900 (69 m³/s). The river divides into Rive Droite (north — historically commerce and institutions) and Rive Gauche (south — the Latin Quarter, universities, artists), linked by 37 bridges from the medieval Pont Neuf (completed 1607) to the Simone-de-Beauvoir footbridge (2006), and punctuated by three islands: the Île de la Cité (cradle of Paris — Notre-Dame, Sainte-Chapelle), the Île Saint-Louis, and the artificial Île aux Cygnes.

Navigational and economic weight: ocean-going ships reach Rouen (123 km of Seine maritime); barges ply from Marcilly; the Port of Paris handles ~20 Mt; the estuary between Le Havre and Honfleur (Pont de Normandie) carries a quarter of French maritime traffic. Ecologically, the Seine–Normandie water agency district covers 94,500 km² (18% of national territory) and 18.9 M inhabitants; the Seine watershed alone ~75–79,000 km².

### 4.3 Disambiguation — why no other river answers the question
- **Marne** (514.26 km, longest tributary; ~⅓ of the Seine's Paris flow): joins at Charenton-le-Pont/Alfortville, entirely outside the commune of Paris, immediately upstream ("just upstream from Paris" — en.wikipedia; Larousse: "dans la banlieue de Paris"). A single open-data atlas lists "Paris 12e" among its bank towns — an artifact of arrondissement-centroid proximity (the Bois de Vincennes borders the lower Marne); flagged and rejected against eight institutional sources.
- **Bièvre** (34.6–36 km): the only natural tributary ever to join the Seine *within* Paris (5 km across the 5e/13e, outfall at today's place Valhubert near Gare d'Austerlitz — "seul affluent naturel de la Seine dans Paris", Paris & Métropole Aménagement). progressively culverted from the 1820s and fully buried intra-muros by 1912; its waters now run to the Achères treatment plant via the sewer system. Present-tense answers exclude it; historically it was "Paris's second river", and partial daylighting is under active study (parc Kellermann feasibility programme; SMBVB Contrat 2026–2030).
- **Oise, Essonne, Epte, Seine tributaries beyond the city**: meet the Seine strictly outside Paris.
Verdict: "the Seine" is the only correct answer, with the Bièvre a footnote and the Marne an at-threshold neighbour.

### 4.4 The river as patrimonial and civic spine
UNESCO's OUV frames Paris as "a river city" — since prehistoric settlements and the Parisii, "the Seine has played both a defensive and an economic role"; the inscribed ensemble (bridges, quays, banks, two islands, now 531/538 ha, buffer 3,194 ha) is "an outstanding urban architectural ensemble, united by a grandiose river landscape… illustrating most of the styles… employed over nearly eight centuries" — Notre-Dame and the Sainte-Chapelle (Gothic diffusion), Pont Neuf (Renaissance), classical Louvre–Invalides–École militaire axis, Haussmann boulevards that "inspired the construction of the great cities of the New World", and the Eiffel Tower ("a universally recognized icon"). Management instruments: the 1999 *Cahier des prescriptions* for the banks, seasonal-use specifications (2015), and the definitive closure of the lower quays to cars (Left Bank 2014, Right Bank 2016) that created the Parc Rives de Seine. The bouquinistes green boxes — "a living cultural corridor" — and, since summer 2025, legalized public swimming (post-2024-Olympics flagship: 3 Paris sites, €1.1–1.4 Md Plan Baignade, daily ColiMinder water surveillance, €68 fine for out-of-zone swimming since Aug 2026, €850 M downstream extension decided Nov 2026) complete the picture of a river that remains the capital's beating heart — literally "cœur battant", as the Ville de Paris dossier titled it.

---

## 5. Comparison / Evaluation Matrices

**5.1 Candidate rivers for "runs through Paris"**

| River | Touches Paris city? | Joins Seine where | Surface water in Paris today? | Verdict |
|---|---|---|---|---|
| **Seine** | Yes — 13 km intra-muros | — (is the river) | Yes | **THE answer** |
| Bièvre | Yes (historically, 5 km) | Place Valhubert (5e/13e) | No — culverted 1912 | Historical footnote only |
| Marne | No (limitrophe, upstream) | Charenton–Alfortville (Val-de-Marne) | No | Ruling-out evidence |
| Oise / Essonne / Epte | No | Conflans / Seine-Amont / near Gisors | No | Not applicable |

**5.2 "Capital" senses (all satisfied by Paris; none by any alternative city)**

| Sense | Basis | Paris? | Contenders? |
|---|---|---|---|
| Constitutional text | None exists (Vth Rep; all const. since 1791) | n/a | none |
| Statutory seat | Ord. 58-1100 art. 1er (1958) | Yes | Versailles 1871–79 (law then said seat there) — abrogated |
| Terminology (State) | Arrêté 4 Nov 1993 + CILF JO 2008/2019 | Yes ("Paris") | none |
| Institutional presence | Presidency, PM, both chambers, ministries | Yes | Vichy 1940–44 (de facto, never de jure) |
| International recognition | UN, EU, Council of Europe lists | Yes | none |
| Historical/cultural | "caput regni" since 12th c. | Yes | Clovis-era Tournai/Soissons (predecessor seats) |

**5.3 Seine statistics — spread and adopted values**

| Parameter | Spread observed | Adopted (rationale) |
|---|---|---|
| Total length | 773 / 774.76 / 775 / 776 / 776.6 / 777 / 781 km | **≈775–777 km** (Sandre registry lineage vs common citation) |
| Rank among French rivers | 2nd (length on metropolitan soil) / 5th (total lengths incl. Rhine, Meuse…) | **2nd after the Loire**, convention-dependent (overseas rivers never displace it) |
| Length in Paris | 8 mi = 13 km (multiple) | **13 km** |
| Width in Paris | 30–200 m | **30–200 m** |
| Depth in Paris | 3.40–5.70 m vs 9.5 m | **3.40–5.70 m** (official consensus; 9.5 m = documented outlier) |
| Discharge at Paris | 300–336 m³/s; QJ0.5 ≈ 228 | **~330 m³/s normal** |
| 1910 flood | 8.62 m; 2,400–2,650 m³/s | **8.62 m / ~2,400–2,650 m³/s** |
| Departments (main stem) | 12 / 13 (Marne-edge; Calvados "longé") | **12–13** |
| Basin | 75,000–79,000 km² (94,500 = agency district) | **≈78,000 km² (watershed)** |
| UNESCO property | 365→531 ha (ICOMOS) / 538 ha (List page); buffer 3,157 (proposed) → 3,194 ha (approved) | **531 (or 538) ha, buffer 3,194 ha, per Decision 46 COM 8B.39** |

---

## 6. Gaps and Limitations

1. **Fetch-blocking artefacts:** legifrance.gouv.fr, Britannica, culture.gouv.fr PDFs, Le Parisien and some .gouv.fr pages return 403 to non-browser clients; canonical texts (the 1993 annex row; ord. 58-1100 art. 1) were verified through official mirrors (Université Laval; senat.fr) and verbatim search-index captures of the blocked pages. PDF content types (ICOMOS evaluations, Sandre metadata) were captured via search index, not parsed natively.
2. **Live Sandre UI** is a JS SPA; the registry record came from a 2021 Wayback capture plus a 2026 BD-TOPAGE-derived secondary — authoritative but not same-day. The exact "776.6 vs 774.76 vs 775" cannot be pinned without the current downloadable geodata.
3. **Minor unresolved numerical variances**, all immaterial to the answer: 531 vs 538 ha property area; 116k vs 120k 2026 Paris swimmers (DRIEAT vs Ville/Apur); source-elevation spread (446–471 m); a blog's "October 2024" for a July 2024 decision.
4. **The 1877 "seize de Mai" relocation rumour** investigated and *not* evidenced (documented negative finding).
5. **Scope limits:** metropolitan France assumed (per plan); "runs through" read as municipal boundary, not metro area; complete 37-bridge inventory, 2026 Kellermann daylighting construction status, and Free-France ordonnance primaries were left as acknowledged, non-material gaps.

---

## 7. Recommendations / Future Directions

- **For answering this question directly:** "The capital of France is **Paris**, and the river that runs through it is the **Seine**" — optionally enriched: 13 km/37 bridges intra-muros; 775+ km to the English Channel.
- **For citation hygiene:** prefer Sandre/BD-TOPAGE, Ville de Paris, DRIEAT/préfecture, UNESCO SOUV over travel-aggregator echo chambers (the 9.5 m depth and "fifth longest" figures propagate almost exclusively through them).
- **If extended later:** monitor (a) the Seine–Banks management plan now due to WHC (updated SOC report by 1 Feb 2027, 49th session), (b) the downstream baignade programme (€850 M, new sites ~2030), (c) any Bièvre daylighting ground-breaking at parc Kellermann, and (d) Le Monde's reported 2026 initiative to *reduce* the heritage perimeter — the only live pressure found on any fact in this report.

---

## 8. Complete Source List

**Official / institutional (EU, French State, City, UNESCO, agencies):**
1. european-union.europa.eu — France country page — https://european-union.europa.eu/principles-countries-history/eu-countries/france_en
2. Ville de Paris — "La Seine, cœur battant de Paris" — https://www.paris.fr/dossiers/la-seine-coeur-battant-de-paris-216
3. Ville de Paris — "Les secrets enfouis de la Bièvre" — https://www.paris.fr/pages/les-secrets-enfouis-de-la-bievre-riviere-parisienne-16900
4. Ville de Paris — Baignade FAQ — https://www.paris.fr/pages/baignade-en-seine-toutes-les-questions-que-vous-vous-posez-31533
5. presse.paris.fr — "8 sites ouverts pour la saison 2026" — https://presse.paris.fr/communiques/reouverture-des-sites-de-baignade-en-ile-de-france-8-sites-ouverts-pour-la-saison-2026
6. Légifrance — Arrêté du 4 novembre 1993 — https://www.legifrance.gouv.fr/jorf/id/JORFTEXT000000181509/ ; https://www.legifrance.gouv.fr/loda/id/LEGITEXT000005615170/ ; art. 2 — https://www.legifrance.gouv.fr/loda/article_lc/LEGIARTI000006546206
7. Université Laval/AXL — Arrêté 1993 + annexe (France→Paris) — https://www.axl-cefan.cstip.ulaval.ca/europe/france_arrete-1993.htm (+ liste annexée page)
8. culture.gouv.fr — Recommandation de toponymie MEAE/CILF (JO 2008/2019) — https://www.culture.gouv.fr/Media/Thematiques/Langue-francaise-et-langues-de-France/Infolettres/JUILLET-2019/Liste-complete-des-toponymes
9. formation-civique.interieur.gouv.fr — "Les fleuves français" — https://formation-civique.interieur.gouv.fr/fiches-par-thematiques/histoire-geographie-et-culture/atlas-de-la-france/les-fleuves-français/
10. bouches-du-rhone.gouv.fr — Formation civique module 1 (PDF) — https://www.bouches-du-rhone.gouv.fr/content/download/22931/139092/file/module%201_Valeurs-et-institutions.pdf
11. prefectures-regions.gouv.fr — Île-de-France dossier — https://www.prefectures-regions.gouv.fr/ile-de-france/layout/set/print/Region-et-institutions/Portrait-de-la-region/Histoire/L-Ile-de-France ; post-JOP Plan Baignade — …/Le-Plan-Baignade-poursuit-sa-dynamique-post-JOP-2024-vers-une-Seine-et-une-Marne-baignables
12. sénat.fr — Règlement → Ordonnance n° 58-1100, art. 1er — https://www.senat.fr/reglement/reglement142.html ; séance 7 nov 2016 — https://www.senat.fr/seances/s201611/s20161107/s20161107006.html
13. info.gouv.fr — Le Premier ministre — https://www.info.gouv.fr/le-premier-ministre ; vie-publique.fr — présidence — https://www.vie-publique.fr/fiches/19414-…
14. whc.unesco.org — Paris, Banks of the Seine — https://whc.unesco.org/en/list/600/ ; maps — /en/list/600/maps/ ; Urban Heritage Atlas — /en/urban-heritage-atlas/Paris/ ; Decision 46 COM 8B.39 — /en/decisions/8631/ ; ICOMOS eval WHC/24/46.COM/INF.8B1.Add — /document/208527 ; 8B.Add — /document/206974 ; 46 COM 7B.7 — /en/decisions/8533/
15. Sandre (Office français de la biodiversité network) — fiche cours d'eau "La Seine" ----0010 — live: https://www.sandre.eaufrance.fr/geo/CoursEau/----0010 ; capture: https://web.archive.org/web/20210123171121/http:/www.sandre.eaufrance.fr/geo/CoursEau/----0010 ; OIEau code-method PDF — https://www.sandre.eaufrance.fr/sites/default/files/IMG/pdf/Point_CodeHydrographique.pdf
16. eaufrance.fr — "Les rivières" — https://www.eaufrance.fr/les-rivieres
17. Agence de l'Eau Seine-Normandie — "Le bassin de la Seine" — https://www.eau-seine-normandie.fr/agence-de-leau/le-bassin-de-la-seine
18. HydroPortail/Vigicrues — station F700000103 La Seine à Paris-Austerlitz — https://www.hydro.eaufrance.fr/stationhydro/F700000103/fiche
19. VNF — crue guide (PDF) — https://www.vnf.fr/vnf/app/uploads/2020/03/Guide-information-recommandations-en-cas-de-crue.pdf
20. DRIEAT Île-de-France — 1910 bilan (PDF) — https://www.drieat.ile-de-france.developpement-durable.gouv.fr/IMG/pdf/bilan_1910_cle7c8919.pdf ; baignade 2026 bilan — https://www.drieat.ile-de-france.developpement-durable.gouv.fr/qualite-de-l-eau-de-la-seine-et-de-la-marne-bilan-a13652.html ; method page — /baignade-dans-la-seine-et-dans-la-marne-a13617.html
21. ARS Île-de-France — eaux de baignade — https://www.iledefrance.ars.sante.fr/la-qualite-des-eaux-de-baignade-en-ile-de-france
22. Château de Versailles — "Versailles, capitale du royaume" — https://www.chateauversailles.fr/decouvrir/histoire/grandes-dates/versailles-capitale-royaume ; "Histoire de la République à Versailles" — …/histoire-republique-versailles ; IIIe Rép. — …/iiie-republique-versailles
23. Assemblée nationale — crise du 16 mai 1877 — https://www.assemblee-nationale.fr/dyn/histoire-et-patrimoine/troisieme-republique/la-crise-du-16-mai-1877 ; rapport n° 2226 — https://www.assemblee-nationale.fr/12/rapports/r2226.asp
24. Musée Carnavalet — "The Seine, from 1977 to the present days" — https://carnavalet.paris.fr/en/exhibitions/seine-1977-present-days
25. BnF Essentiels — "De Lutèce à la capitale" — https://essentiels.bnf.fr/fr/histoire/moyen-age/99f01b1e-76a4-42f6-bfd0-1700e9ebbf99-ville-moyen-age/article/3835a75d-9077-4cd1-95a1-11d9446dcd33-lutece-la-capitale ; Gallica feature — https://gallica.bnf.fr/accueil/fr/html/lhistoire-tourmentee-dune-riviere-quand-la-bievre-disparait
26. archeologie.culture.gouv.fr — "La Bièvre" / "The Gallic Lutetia" — https://archeologie.culture.gouv.fr/paris/fr/la-bievre
27. SMBVB — Historique Bièvre — https://www.smbvb.fr/la-bievre/historique/ ; Paris & Métropole Aménagement — https://www.parisetmetropole-amenagement.fr/fr/bievre-paris-13e ; APUR (2001 PDF) — https://www.apur.org/sites/default/files/documents/40.pdf
28. SAGE Marne Confluence — https://www.sage-marne-confluence.fr/le-territoire-du-sage-et-ses-enjeux/caracteristiques-du-territoire/ ; eau.seine-et-marne.fr ; Val-de-Marne Tourisme — La Marne
29. archives.allier.fr — "Vichy capitale" ; ESA — SPOT-7 Paris image — https://earth.esa.int/eogateway/gallery/paris-france-as-seen-by-spot-7
30. seinegrandslacs.fr — EPTB presentation — https://www.seinegrandslacs.fr/seine-grands-lacs

**Reference / encyclopedic:**
31. en.wikipedia.org — Paris · Seine · History of Paris · Lutetia · Marne (river) · Seine River (Britannica-cited depth claim)
32. fr.wikipedia.org — Capitale de la France · Seine · Marne (rivière) · Bièvre (affluent de la Seine) · Crue de la Seine de 1910 · Charenton-le-Pont · Versailles · Rives de la Seine à Paris · Liste des cours d'eau de France par longueur · Liste de fleuves de France · Régime de Vichy
33. Larousse en ligne — la Seine · Versailles · Marne — https://www.larousse.fr/encyclopedie/riviere-lac/la_Seine/143800 etc.
34. Britannica Kids/Students (snippets; fetch 403) — kids.britannica.com ; main article britannica.com/place/Seine-River (blocked)
35. Council of Europe — "Status of capital cities" CPL(14)4REP (2007) — rm.coe.int ; Delledonne, *Perspectives on Federalism* (2024) — iris.sssup.it ; Lefèvre, *Social, economic and spatial history of the Île-de-France metropolis* (Cambridge Core)

**Media / community / commercial (used for corroboration or flagged):**
36. WorldAtlas — What is the Capital of France? / Which River Runs Through Paris?
37. National Geographic Kids — France profile
38. French Moments — Top 10 bridges — https://frenchmoments.eu/top-10-most-beautiful-bridges-of-paris/
39. Paris Perfect — Seine guide ; Rick Steves/PBS (snippet)
40. Paris je t'aime (tourism; 403) — bridges & Rives de Seine articles (snippets)
41. EuroCanals — https://www.eurocanals.com/Rivers/seine-river-france.html
42. carnetsdici.fr ; fleuves.org (×2) ; OSM wiki France/Cours d'eau ; riveryas.com (flagged artifact)
43. Initiatives Rivers/AFSU Seine synopsis PDF (snippet)
44. lemondefou.fr ; caminteresse.fr ; geogir.fr (rankings, snippet)
45. info-paris.fr — crues table ; meteo-npdc.fr (Hub'Eau mirror)
46. Le Point du Jour — baignade bilan (07/10/2026) — https://lepointdujour.fr/energie-environnement/8301-baignade-seine-bilan-saisons/
47. Le Parisien — €850 M aval (05/11/2026, paywalled snippet) ; Les Echos — Versailles 1871 ; Revue des Deux Mondes (snippet) ; paris-historique.org ; edgepedia.org ; parisjetaime snippets
48. paris-city.fr (flagged low-authority, anachronisms) ; various Légifrance mirrors (Jurisfac/Juriblio/LibreJustice, Portail législatif)

---

## 9. Appendix — Raw Search Queries per Cycle

| Cycle | Worker | Query |
|---|---|---|
| Phase 2 | Q1 | capital of France |
| Phase 2 | Q2 | river that runs through Paris France |
| Phase 2 | Q3 | Seine River length source mouth geography France |
| Phase 2 | Q4 | Paris history capital of France Lutetia Clovis |
| Phase 2 | Q5 | Seine River Paris bridges Left Bank Right Bank UNESCO World Heritage banks of the Seine |
| Loop 1 | L1a | arrêté du 4 novembre 1993 relatif à la terminologie des noms d'États et de capitales legifrance Paris; site:gouvernement.fr Paris capitale de la France; fallback vie-publique query (+2 supplementary) |
| Loop 1 | L1b | Sandre fiche cours d'eau La Seine 0----0010 longueur; La Seine fleuve 776,6 km source embouchure départements traversés (+site-restricted) |
| Loop 2 | L2a | profondeur moyenne de la Seine à Paris mètres étiage crue (+EN & Vigicrues variants) |
| Loop 2 | L2b | le plus long fleuve de France classement Loire Seine Maroni Rhin kilomètres |
| Loop 3 | L3a | Bièvre rivière Paris souterraine affluent de la Seine histoire |
| Loop 3 | L3b | la Marne fleuve confluent Seine Paris Charenton bois de Vincennes traverse (+EN variant) |
| Loop 4 | L4a | Versailles siège du gouvernement 1682 1789 1871 1879 Paris capitale (+seize de Mai follow-up) |
| Loop 4 | L4b | régime de Vichy 1940 capitale de facto Vichy Paris capitale de jure; ordonnance n° 58-1100 du 17 novembre 1958 article 1er Parlement siège Paris transfert siège des pouvoirs publics |
| Loop 5 | L5a | "Paris Banks of the Seine" UNESCO 2024 minor boundary modification decision buffer zone World Heritage (+FR variants) |
| Loop 5 | L5b | baignade Seine Paris 2026 qualité eau projets Bras marie Hélie Saint-Léger milliards |

**Protocol compliance:** Phase 1 plan ✓ · Phase 2 five parallel workers ✓ · Phase 3 intermediate synthesis + gap ledger ✓ · Phase 4 five loops ≥ minimum, decision per cycle recorded in `04-loops/` ✓ · Phase 5 report ≥10,000 characters with all nine required sections ✓ (7,000-word English variant explicitly deviated from, as stated in §2).

---

*Prepared 2026-11-28. Answer in one line: **Paris — the Seine.***
