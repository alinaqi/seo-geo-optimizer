# Measurement and prompt-set design

| Element | Guidance |
|---|---|
| Design | Minimum viable set: 30 prompts per vertical x 3 engines (ChatGPT, Google AI Mode/AIO, Perplexity), plus Gemini, Claude and Copilot where relevant; sampled weekly with 3 runs per prompt. |
| Themes | Group prompts into themes: category definition, 'best X for Y', 'X vs Y', pricing/cost, how-to, troubleshooting, 'is X worth it', local/near me, brand facts ('what is <brand>'). |
| Variants | Write 3-5 natural-language variants per theme (23-word average prompts, personas, constraints) to absorb prompt fragility. |
| Sources of prompts | Sales call questions, support tickets, People Also Ask, Reddit threads, ChatGPT follow-up suggestions, GSC question queries, AI tool 'related prompts'. |
| Collection | OpenAI Responses API with web_search (record sources list), Perplexity Sonar (search_results), Gemini grounding (groundingChunks), Claude web search; consumer-app spot checks monthly for 10 prompts. |
| Labelling | LLM judge extracts: brand mentioned (y/n), owned URL cited (y/n), position, sentiment, competitor set; 5% human audit; agreement >=90%. |
| Variance | Report min/median/max across runs; alert only on theme-level change >20% sustained 2 weeks; annotate engine updates and Google spam/core updates. |
| Memory vs search | Tag citations as 'memory' (no live source) or 'search' (live URL); memory gaps need PR/entity work, search gaps need technical/content fixes. |
| Competitor set | Fix 3-5 competitors per theme; compute share of voice = brand mentions / total brand mentions in set. |
| Compliance | Respect API terms (Gemini grounding ToS limits competitive tracking); never scrape consumer apps; store raw answers for audit. |

## Timeline Aug-Oct 2026

| Date | Event | Implication | Sources |
|---|---|---|---|
| 2026-05-21 to 06-02 | Google May 2026 core update (latest core update as of Oct 27 2026) | Scaled low-effort AI content sites among decliners | S61 |
| 2026-06-03 | Google Search Console generative-AI performance reports and site-level AI opt-out toggle announced | Measure AIO/AI Mode visibility natively; opt-out forfeits AI traffic | S48 |
| 2026-06-15 | Google 'AI features and your website' updated: llms.txt not used; preview controls apply; Google-Extended has no effect on Search/AI Mode | Stop llms.txt claims; audit snippet controls | S04 |
| 2026-06-16 | Bing AI Visibility insights: intents, topics, citation share, compare | Use for topic-level AEO measurement | S68 |
| 2026-07 | Previsible: ChatGPT 92.4% of trackable AI referrals; Claude #2 | Prioritise ChatGPT and Google; watch Claude | S32 |
| 2026-08-09 | OpenAI Atlas browser retired; agentic browsing folded into ChatGPT app and Chrome extension (per grounded research; verify) | Agent traffic arrives via ChatGPT-User fetcher | S23 |
| 2026-08-18 to 08-21 | Google August 2026 spam update | Templated/programmatic pages without value lost up to 95%; Discover/News flatlines reported | S62 |
| 2026-08 (mid) | ChatGPT changes fan-out; Reddit citation share collapses (~86% per Promptwatch, unverified); tilt to primary sources | Rebalance community strategy toward own data and YouTube for ChatGPT | S36,S37 |
| 2026-08-20 | Google releases embeddable Preferred Sources button for publishers | Deploy on articles; measure opt-ins | S29 |
| 2026-08-28 | Google changes site reputation abuse enforcement: no manual-action effect for EEA users; outside EEA unchanged | Third-party sections still risky outside EEA | S07 |
| 2026-08-31 | European Commission designates ChatGPT a Very Large Online Search Engine (DSA) | ChatGPT regulated like a search engine in the EU | S50 |
| 2026-09-24 | GSC Performance report splits Web into text and multimodal (Lens, Circle to Search) | Segment reporting | S64 |
| 2026-09-24 to 10-08 | Google September 2026 spam update (13d16h, phased; volatility spikes Sep 25-27, Sep 30, Oct 4-6) | Longest 2026 spam update; Reddit translated pages resurged | S05,S06 |
| 2026-10-01 | Google updates 'Using generative AI content': manual fact-check of all AI output including titles, meta descriptions, structured data, alt text; fabricated author profiles deceptive | Make human review a HARD_BLOCK gate | S01,S63 |
| 2026-10-02 / 10-06 | First Page Sage: schema effect negligible after authority control; agentic search 5.4% of searches; agents pick #1 only 44.6% | Invest in suitability content | S20,S21 |
| 2026-10-08 to 10-16 | ChatGPT stops appending utm_source=chatgpt.com on most links; referrer stripped (unconfirmed by OpenAI) | Expect artificial AI-referral drop; annotate GA4 | S49 |
| 2026-10-15 | SE Ranking 300k-domain llms.txt study: no correlation with citations | Drop llms.txt from AEO KPIs | S11 |
| 2026-10 (late) | No Google core update since May; next expected within weeks | Keep velocity governors armed | S61 |
