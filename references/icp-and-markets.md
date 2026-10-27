# ICP discovery, markets and content strategy (from August 2026)

Read this at SKILL.md step 1b (ICP and market discovery) and step 4b (content strategy). Figures below come from vendor and analyst reports graded C unless marked; treat them as directional and re-verify before quoting.

## Why ICP comes before content

- 51% of B2B software buyers now start vendor research in an AI chatbot, and chatbots are the top influence on shortlists (G2, Mar 2026, S76). 45% of B2B buyers use generative AI for vendor information and 69% then validate with a human rep (Gartner, May 2026, S77).
- 89% of citations for unbranded B2B questions come from third-party sources, not vendor sites (Bain, Oct 2026, S78). Your ICP decides which third parties matter.
- Recommendation prompts are persona-shaped ("best X for a 300-person HR team in Germany"). Content that names the segment and its fit is retrieved for that segment; generic category pages are not (First Page Sage, S20).

## ICP sheet (one row per segment)

| Field | What to write | Evidence rule |
|---|---|---|
| Segment name | Role + size + industry + market, e.g. "HR leaders, mid-market, DACH" | from site, pricing, case studies, reviews, job posts |
| Roles | Buyer, champion, user | quote the page or review that names them |
| Company size | smb / mid-market / enterprise | quote employee ranges or plan names |
| Industries | named verticals | nav, solution pages, case studies |
| Markets and languages | countries, languages served, currency | market_detect.py output |
| Buying triggers and objections | why now, what blocks | reviews, FAQ, sales notes |
| Engines to sample | from the market table below | per market |
| Prompts | 5-10 natural-language prompts this persona types | mined from calls, tickets, Reddit, PAA |
| Competitors in answers | 3-5 per segment | first sampling run |
| Confidence | high / medium / low; UNKNOWN fields stay UNKNOWN | never invent |

`scripts/icp_signals.py` extracts roles, industries, size band, pricing model, review platforms and proof quotes with evidence; `scripts/market_detect.py` detects languages, hreflang, JavaScript language swaps, currencies and geographies and returns the market profile. Both feed the sheet; the agent adds judgment and the owner confirms.

## Market table (engine mix and citation pools, Oct 2026)

| Market | Engines to sample (priority order) | Third-party citation pools | Notes |
|---|---|---|---|
| US | ChatGPT, Google AI Mode, Perplexity, Claude, Copilot | G2, Capterra, Trustpilot, Yelp (local), Reddit, YouTube | ChatGPT ~56-61% of AI chatbot visits; AIO on ~half of US queries; Preferred Sources live (S84, S85) |
| UK | Google AI Mode, ChatGPT, Perplexity, Copilot | Trustpilot (cited in ~49% of AI Mode consumer answers, S80), G2, Capterra UK | CMA proposed publisher opt-out rights for AIO (S87) |
| DACH | Google AI Mode, ChatGPT, Perplexity, Copilot | OMR Reviews, Capterra DE, G2, Trusted Shops, Provenexpert | EEA: site-reputation manual actions do not apply for EEA users since Aug 2026; GDPR hosting is a frequent prompt |
| France | Google AI Mode, ChatGPT, Mistral Le Chat, Perplexity | Trustpilot FR, Capterra FR, Avis Vérifiés | Le Chat has a domestic following |
| Spain / LatAm | Google AI Mode, ChatGPT, Perplexity | Capterra ES, G2, Trustpilot | Spanish AIO live |
| Brazil | Google AI Mode, ChatGPT, Perplexity | Reclame Aqui, Capterra BR, G2 | Portuguese AIO live |
| Japan | Google AI Mode, ChatGPT, Copilot, Perplexity | ITreview, BOXIL | Japanese AIO live |
| Korea | Naver AI Briefing, ChatGPT, Google AI Mode | Naver Blog, Naver Cafe, Kakao | Naver contests Google for #1; Naver content is the citation pool |
| China | Baidu/Ernie, DeepSeek, Doubao, Kimi | Zhihu, Baidu Baike, WeChat | Western engines unavailable; DeepSeek 3.4% of global chatbot visits |
| India | Google AI Mode, ChatGPT, Perplexity | G2, Capterra, SoftwareSuggest | English and Hindi AIO live |
| Middle East | Google AI Mode, ChatGPT, Perplexity | G2, Google Business Profile | Arabic AIO live; English B2B prompts common |
| Russia / CIS | Yandex Alice, ChatGPT where reachable | Yandex Zen, Otzovik | Yandex leads |
| Czechia | Google AI Mode, Seznam, ChatGPT | Heureka | Seznam keeps double-digit share |

Cross-market facts: AI Overviews exist in 200+ countries and 40+ languages (S84). AI Mode answers are 4x longer than AIO and share only 13.7% of cited URLs with AIO for the same query, so track them separately (S83, Ahrefs Oct 2026).

## Language rules that changed in 2026

- Engines ignore hreflang when composing answers (S82, grade D) and run 43% of sub-searches for non-English prompts in English (Peec AI, S81). A JavaScript language toggle or a thin translated subfolder is invisible to retrieval.
- What works: each language at its own URL, the answer in the opening paragraph written by a native speaker, local third-party mentions and reviews, a per-market prompt set in the local language, and English versions of your strongest pages because English sub-searches still dominate.
- Never ship literal machine translation; engines filter content that lacks local expertise.

## Content brief (required fields)

| Field | Rule |
|---|---|
| Segment and market | one segment, one market, one language |
| Theme | definition, best_for, comparison, pricing, how_to, proof |
| Intent sentence | the question the page answers, in the persona's words |
| Sub-questions | from fan-out (ST09), each gets a self-contained passage |
| Information gain | the specific data, experience or expert input this page adds; no brief without it |
| Author | named human with bio; reviewer for YMYL |
| Sources | primary sources with retrieval dates (claim ledger) |
| Gate | who approves before publish (comparison: product marketing + legal; proof: customer approval) |
| Prompts | the measurement rows that will show whether the page is retrieved |

`scripts/strategy_plan.py --icp icp.json --outdir strategy/` writes `strategy.md` and `calendar.csv` with these fields, under the velocity cap.

## Demographics and consumer markets

For consumer sites use the same sheet with demographic fields (age band, household, location, device, price sensitivity) drawn from reviews, analytics and surveys, never guessed. Consumer AI discovery now rivals search (44% of users put AI search first for discovery; McKinsey, S86), and consumer answers lean on Trustpilot, Yelp, Reddit and YouTube, so review presence and video outrank most on-site work.
