# Strategies and agent execution (from SEO_AEO_Agentic_Playbook_2026.xlsx)

Win probability = estimated chance of a measurable KPI gain in 90-180 days; priority = win x impact x (4 - risk) / effort.

## ST01 AI-crawler access and server-rendered HTML (win 90%, grade A, risk 1/3)

**What:** Allow the search/retrieval bots you want citations from (Googlebot, Bingbot, OAI-SearchBot, Claude-SearchBot, PerplexityBot, user fetchers) at robots.txt AND at the CDN/WAF; decide training bots (GPTBot, ClaudeBot, Google-Extended, CCBot) separately; serve full HTML server-side because OpenAI, Anthropic and Perplexity bots do not execute JavaScript.

**Why:** Retrieval-augmented engines can only cite what their own crawler fetched. OpenAI, Anthropic and Perplexity run their own indexes; blocking OAI-SearchBot removes you from ChatGPT search. AI bots read static HTML only (Vercel/MERJ, RESONEO 2026). Google-Extended has no effect on AI Overviews/AI Mode.

**Evidence:** Official crawler docs (OpenAI, Anthropic, Perplexity, Google); Vercel/MERJ log study; Cloudflare default-block behaviour; 2026 practitioner reports of brands that blocked OAI-SearchBot by mistake and vanished from ChatGPT answers. Sources: S04,S23,S24,S25,S26,S27,S70

**Agent:** Technical SEO agent | autonomy PROPOSE (robots/WAF changes), AUTO (monitoring) | trigger Weekly + on deploy

**Steps:** 1 Fetch robots.txt and parse per UA (Googlebot, Bingbot, OAI-SearchBot, ChatGPT-User, Claude-SearchBot, Claude-User, PerplexityBot, Perplexity-User). 2 Request 20 sample URLs per template with each UA and from verified bot IPs; record status codes. 3 Diff raw HTML vs rendered DOM for main content; flag JS-only content. 4 Propose minimal robots/WAF allow-list diff plus SSR/prerender fix list. 5 After approval, re-test and record evidence.

**Checks:** All sample URLs return 200 for allowed UAs; main text present in raw HTML (>=90% of rendered text); no 403/429 from WAF for verified bot IPs; training-bot policy documented separately.

**Gate:** Security/infra owner approves any WAF or robots change (HARD_BLOCK). **Guardrails:** Never weaken auth or expose private paths; change only scoped rules; keep a rollback.

## ST16 Agent-driven internal linking and orphan repair (win 65%, grade B, risk 1/3)

**What:** Crawl the site, find orphan and deep pages, propose contextual links with descriptive anchors from relevant high-authority pages, batch-apply after review.

**Why:** Internal links remain a primary crawl, context and authority pathway; Google recommends findable internal links for AI features too. Low-risk, high-coverage automation.

**Evidence:** Google guidance (A); Arvow refresh case (27 link suggestions auto-queued) (C). Sources: S03,S41,S72

**Agent:** Internal linking agent | autonomy PROPOSE, AUTO for approved patterns | trigger Weekly crawl

**Steps:** 1 Crawl; list orphan pages, pages with crawl depth >3, and high-authority pages with few outlinks. 2 Compute semantic similarity to propose source-target pairs with anchor text drawn from the target's H1/entity. 3 Queue suggestions; batch apply after approval; AUTO for pre-approved template-level rules.

**Checks:** No link to noindex/redirect targets; anchor text descriptive (not 'click here'); max 3 new links per source page per pass.

**Gate:** Editor bulk-approves queue (ADVISORY). **Guardrails:** Cap links per page; do not create nav-like link blocks.

## ST08 Entity consistency and knowledge-graph hygiene (win 60%, grade C, risk 1/3)

**What:** One canonical description of the company, products, founders, pricing and category used identically on site, LinkedIn, Crunchbase, Wikidata, GBP, app stores and press kit; Organization schema with sameAs; fix contradictions between sources.

**Why:** Models recommend brands whose core facts are consistent across third-party sources (First Page Sage); engines reason over entities; 'memory' citations (training data) depend on cross-web consistency, 'search' citations on live pages.

**Evidence:** First Page Sage Oct 2026; Kalicube entity practice; Google structured data must match visible text. Sources: S21,S04,S63

**Agent:** Entity consistency agent | autonomy PROPOSE | trigger Monthly + on fact change (pricing, leadership, product names)

**Steps:** 1 Crawl all owned and third-party profiles; extract facts. 2 Diff against canonical record; list contradictions. 3 Sample AI answers for 'what is <brand>' prompts per engine; score factual accuracy. 4 Propose corrections per profile and Organization schema update with sameAs. 5 Re-sample after 4 weeks.

**Checks:** Contradiction count trending to 0; schema matches visible text; AI answer accuracy score >=90% on sampled prompts.

**Gate:** Brand owner approves canonical record changes. **Guardrails:** Do not edit Wikipedia for pay; never assert unverifiable claims.

## ST10 Machine-readable E-E-A-T: real authors, reviewers, dates (win 60%, grade A, risk 1/3)

**What:** Named real authors with bios, credentials and sameAs links; reviewer line for YMYL; visible published/updated dates matching schema; 'how we tested' sections; no fabricated authors or AI headshots.

**Why:** Google's Oct 2026 guidance classifies fabricated author profiles as deceptive and demands human fact-check of all AI output; YMYL citations skew to institutional/expert sources.

**Evidence:** Google gen-AI content guidance (A); citation studies showing .gov/.org dominance in health/finance (B). Sources: S01,S63,S73

**Agent:** E-E-A-T compliance agent | autonomy AUTO (checks), PROPOSE (fixes) | trigger Pre-publish; quarterly audit

**Steps:** 1 Verify author exists in registry and bio page is live. 2 Check visible dates match schema datePublished/dateModified. 3 For YMYL, require reviewer field and >=2 authoritative citations. 4 Flag any AI-generated headshots or placeholder bios. 5 Propose fixes.

**Checks:** Author registry match 100%; date consistency 100%; YMYL reviewer present; zero fabricated profiles.

**Gate:** Publish blocked until checks pass (HARD_BLOCK for YMYL). **Guardrails:** Never generate author personas; humans own bylines.

## ST23 Outbound citation and source hygiene (win 60%, grade A, risk 1/3)

**What:** Cite authoritative primary sources inline, quote named experts, link to standards and datasets; add a references section.

**Why:** 'Cite sources' and 'quotation addition' were among the top GEO methods (+30-40%); engines favour evidence-backed passages; Bing recommends supporting claims with data and cited sources.

**Evidence:** Princeton GEO (A); Bing guidance (A). Sources: S13,S67

**Agent:** Citation hygiene agent | autonomy AUTO (checks), PROPOSE (fixes) | trigger Pre-publish

**Steps:** 1 Extract factual claims. 2 Require a primary or authoritative source per claim; flag vendor blogs for secondary-only status. 3 Verify URLs resolve and support the claim (LLM check plus human spot check). 4 Insert inline citations and references section.

**Checks:** Claim coverage 100%; dead links 0; source grade recorded.

**Gate:** Editor approves flagged claims. **Guardrails:** Never cite sources that do not contain the claim.

## ST02 Content refresh and decay program (win 75%, grade B, risk 1/3)

**What:** Continuously identify pages losing clicks/citations or with stale facts, make substantive updates (new data, new sections, corrected claims), expose real dateModified, keep a changelog, update sitemap lastmod only on material change, ping IndexNow.

**Why:** AI-cited URLs are ~26% fresher than organic results on the same queries; recently updated pages average 6 citations vs 3.6 for outdated ones; 88% of cited pages were updated within 2 years. Freshness is partly manufactured by updates, so refresh beats net-new for established sites.

**Evidence:** Ahrefs 17M-citation study; Seer last-updated analysis; HubSpot historical optimization (+106% on refreshed cohort); Bing lastmod guidance. Causal before/after measurement is still thin. Sources: S16,S17,S58,S69,S43

**Agent:** Refresh agent | autonomy PROPOSE | trigger Weekly cohort selection; per-page on decay alert

**Steps:** 1 Score pages: decay (clicks -20% QoQ), opportunity (positions 4-15), staleness (facts older than SLA), citation loss. 2 For top 10/week, extract claims and check each against current primary sources (claim ledger). 3 Draft a targeted update: corrected facts, new data block, new sub-question sections, updated TL;DR; keep URL. 4 Generate change summary and visible changelog entry. 5 On approval publish, set dateModified, sitemap lastmod, IndexNow ping; schedule 4- and 8-week measurement.

**Checks:** Every changed claim has a source URL and retrieval date; diff shows substantive change (>15% content delta or >=1 new data block); no date bump without content change; schema dateModified equals visible date; internal links intact.

**Gate:** Editor approves diff; SME approves YMYL pages (REVIEW_REQUIRED). **Guardrails:** Max 10 refreshes/week per editor; no mass date changes; preserve author attribution.

## ST18 Bing and Copilot grounding readiness (win 55%, grade A, risk 1/3)

**What:** Verify Bing Webmaster Tools, submit sitemaps with accurate lastmod, stream IndexNow on every publish/update/removal, avoid NOCACHE/NOARCHIVE on citable pages, read the AI Performance report (citations, grounding queries, citation share).

**Why:** Bing's rewritten guidelines define GEO eligibility; NOCACHE restricts Copilot to URL/title/snippet; Bing is the only engine exposing native citation analytics.

**Evidence:** Bing Webmaster Guidelines and AI Performance docs (A). Sources: S22,S66,S67,S68,S69

**Agent:** Bing/IndexNow agent | autonomy AUTO | trigger On publish/update/delete; weekly report

**Steps:** 1 On content change, submit URL via IndexNow (stream, not batch). 2 Regenerate sitemap with content-derived lastmod. 3 Weekly: pull AI Performance (citations, cited pages, grounding queries, citation share). 4 Flag pages with NOCACHE/NOARCHIVE that should be citable.

**Checks:** IndexNow 200/202 responses; lastmod equals content change time; no NOCACHE on citable templates.

**Gate:** None for submission; content lead reviews directive changes. **Guardrails:** Do not ping unchanged URLs.

## ST03 Answer-first passage architecture (win 70%, grade B, risk 1/3)

**What:** Open every section with a direct 40-60 word answer; make 100-300 word self-contained chunks with descriptive, question-shaped H2/H3; put the most citable facts in the first 30% of the page; use entity-clean language (canonical names, no dangling pronouns); add tables and 'key numbers' blocks.

**Why:** Engines retrieve passages, not pages (query fan-out). 44.2% of ChatGPT citations come from the first 30% of the source article. First Page Sage: clarity of offering doubled recommendation rate, schema did not.

**Evidence:** Growth Memo 1.2M-answer analysis; Digiday/Google explanation of fan-out; First Page Sage 4,213-prompt study; Bing guidance on headings/tables/FAQ. Sources: S12,S21,S57,S67,S14

**Agent:** Passage-structure agent | autonomy PROPOSE | trigger Pre-publish and during refresh

**Steps:** 1 Parse headings; map each H2/H3 to a sub-question. 2 Check each section opens with a direct answer (<=60 words) and is self-contained (100-300 words). 3 Replace pronouns/ambiguous references with canonical entity names. 4 Add key-numbers table where >=3 figures exist. 5 Move highest-value facts above the 30% mark. 6 Output rewritten draft plus structure report.

**Checks:** Section-level answer-first score >=0.8; no section >350 words without a sub-heading; entity ambiguity count 0; readability unchanged or better; facts unchanged (claim diff empty).

**Gate:** Editor approves (ADVISORY for blogs, REVIEW_REQUIRED for product/YMYL). **Guardrails:** Structure edits must not alter facts; keep brand voice checks.

## ST13 Preferred Sources button and audience loyalty (win 50%, grade B, risk 1/3)

**What:** Embed Google's Preferred Sources button (Aug 20 2026) on articles, ask newsletter and app audiences to opt in; sites marked preferred get a badge in AI Overviews/AI Mode and are shown more often to that user.

**Why:** Personalised ranking signal inside AI answers; Google says users are 2x more likely to click a 'Preferred' badge.

**Evidence:** Google Preferred Sources documentation and Aug 2026 launch coverage (B). No independent lift studies yet. Sources: S29

**Agent:** Audience loyalty agent | autonomy PROPOSE | trigger One-time setup; monthly review

**Steps:** 1 Insert Preferred Sources button component on article templates per Google docs. 2 Draft newsletter/app prompts asking readers to opt in. 3 Measure AIO/AI Mode clicks from returning users in GSC generative-AI report.

**Checks:** Button renders and links correctly; no dark patterns; opt-in copy honest.

**Gate:** Product/design approval. **Guardrails:** No incentives for opt-in that violate Google policy.

## ST12 Agentic shopping readiness (win 60%, grade B, risk 1/3)

**What:** Clean product feeds in Merchant Center, live price/stock, Product+Offer schema, support Google Universal Commerce Protocol and OpenAI Agentic Commerce Protocol where available, trust signals (returns, reviews, shipping), machine-readable specs.

**Why:** AI shopping agents shortlist from structured merchant data and verified live price/stock; brands without agent-readable catalogs do not make the shortlist.

**Evidence:** Google Universal Cart/UCP announcements; OpenAI ACP docs; practitioner reports (C). Sources: S58,S59,S75

**Agent:** Commerce feed agent | autonomy AUTO (feed sync), PROPOSE (catalog content) | trigger Hourly feed sync; daily diagnostics

**Steps:** 1 Sync price/stock to Merchant Center and on-page schema from one source of truth. 2 Run Merchant Center diagnostics; fix disapprovals. 3 Enrich product pages with specs, use cases, comparison tables. 4 Expose ACP/UCP product endpoints where supported. 5 Monitor AI shopping inclusion via prompt set.

**Checks:** Feed and page price/stock match 100%; disapproval rate <1%; schema valid; return/shipping policies machine-readable.

**Gate:** Merchandising approves content enrichment; engineering approves protocol endpoints. **Guardrails:** Never show different prices to bots and users (cloaking).

## ST14 Suitability and comparison content ('best for whom') (win 60%, grade C, risk 1/3)

**What:** Pages that state explicitly who the product fits and does not fit, pricing, limits, integrations, migration paths; honest comparison tables with sourced cells; 'alternatives' pages.

**Why:** Agents chose the #1 ranked result only 44.6% of the time and picked sites with dedicated suitability content 2.7x more often; comparison prompts are the highest-value AEO surface.

**Evidence:** First Page Sage Oct 2026 agentic-search study (C); HubSpot AEO template guidance (C). Sources: S20,S21

**Agent:** Comparison content agent | autonomy PROPOSE | trigger Quarterly competitor refresh; on pricing changes

**Steps:** 1 Build comparison matrix from sourced cells (URL + retrieval date per cell). 2 Draft 'best for / not for' statements grounded in win/loss data. 3 Draft alternatives page with fair treatment. 4 Legal check for claims about competitors. 5 Schedule quarterly re-verification of every cell.

**Checks:** Every competitor claim has source and date; no superlatives without evidence; brand not auto-ranked #1 in every table.

**Gate:** Product marketing and legal approve (REVIEW_REQUIRED). **Guardrails:** No disparagement; no outdated competitor pricing; update or remove when sources change.

## ST20 AI visibility measurement program (win 85%, grade B, risk 1/3)

**What:** Build a prompt set (>=30 prompts per vertical x 3+ engines, sampled weekly via official APIs plus consumer-app spot checks), track mention, citation, position-in-answer and sentiment; add GA4 AI Assistant channel with custom rules for claude.ai/perplexity.ai; use GSC generative-AI report and Bing AI Performance.

**Why:** You cannot optimise what you do not sample; engines disagree 62% of the time and API answers differ from app answers, so trend lines over themed prompt groups are the only stable signal.

**Evidence:** BrightEdge disagreement study (C); vendor API docs (A); GA4/GSC 2026 reporting changes (B). Sources: S38,S47,S48,S51,S52,S53,S54,S66

**Agent:** Measurement agent | autonomy AUTO | trigger Weekly sampling; daily referral pull

**Steps:** 1 Run each prompt 3x per engine per week (temperature default), store full answer, sources, position. 2 Classify mention/citation/sentiment with an LLM judge plus 5% human audit. 3 Aggregate by theme, engine, week; compute share of voice vs competitor set. 4 Pull GA4 AI Assistant channel plus custom claude.ai/perplexity.ai rule; pull GSC generative-AI report; 5 Alert on >20% week-over-week drop by theme; annotate with spam/core updates from the Google status dashboard.

**Checks:** Judge agreement with human audit >=90%; sampling variance reported (3 runs); API vs consumer-app spot check monthly; respect provider ToS.

**Gate:** None (read-only). **Guardrails:** Do not scrape consumer apps against ToS; label API-based numbers as proxies.

## ST04 Information gain: original data, experience and quotable statistics (win 70%, grade A, risk 1/3)

**What:** Publish first-party data (surveys, benchmarks, product telemetry, experiments), named-expert quotes with credentials, and concrete worked examples. Add a 'Statistics' or 'Key findings' block with sourced numbers and a methodology note.

**Why:** The only peer-reviewed GEO study found 'statistics addition', 'quotation addition' and 'cite sources' lift generative-engine visibility 30-40%; agents that only summarise the SERP consensus fail to be cited ('synthetic echo chamber'). Google's Oct 2026 guidance quotes the rater guidelines: little effort/originality/added value = lowest quality.

**Evidence:** Princeton GEO (KDD 2024); GEO survey 2026; Google gen-AI content guidance Oct 2026; Ahrefs/ChatGPT tilt to primary sources Oct 2026. Sources: S13,S14,S01,S37,S73

**Agent:** Research and data agent | autonomy ASSIST (data analysis), PROPOSE (draft) | trigger Monthly data-story cycle

**Steps:** 1 Propose 3 data stories per month from first-party data with a hypothesis each. 2 Run analysis with reproducible notebook; produce charts and methodology note. 3 Draft article with statistics block, named-expert quotes (collected by humans), limitations section. 4 Build a press-ready summary for the PR agent (ST05). 5 Publish after review; register dataset page for reuse.

**Checks:** Every statistic traces to a query/notebook; sample sizes and dates stated; no numbers invented by the model (ledger cross-check); quotes verified with the quoted person.

**Gate:** Data owner signs off on analysis; legal/privacy check on data release (HARD_BLOCK). **Guardrails:** Never fabricate statistics or quotes; anonymise user data; label estimates.

## ST05 Earned brand mentions and digital PR (win 65%, grade B, risk 1/3)

**What:** Run a mention program: data-led PR, expert commentary (Qwoted, Featured, Source of Sources), podcast/YouTube guest appearances, LinkedIn thought leadership, partner co-marketing. Target consistent brand+category co-occurrence on third-party sites, not links.

**Why:** Branded web mentions correlate 0.664 with AI Overview visibility (YouTube mentions 0.737) vs 0.218 for backlinks; nofollow and follow links correlate identically. Seer: citation rate 53% when brand is already mentioned vs 11% when not. Earned media is often the sole source of a brand's AI visibility.

**Evidence:** Ahrefs 75k-brand study; Seer 541k responses; multiple vendor replications. Correlational, not causal. Sources: S09,S17,S18,S33

**Agent:** Digital PR agent | autonomy PROPOSE (pitches), ASSIST (relationships) | trigger Daily query monitoring; weekly pitch batch

**Steps:** 1 Monitor queries and news hooks matching expertise map. 2 Draft pitch with a concrete data point or expert view; attach approved bio. 3 Human sends from personal account. 4 Track placements, mentions, and brand+category co-occurrence. 5 Feed new mentions to entity-consistency agent for fact checks.

**Checks:** No pitch without a verifiable fact or named human spokesperson; no paid-link offers; all placements logged with URL and date.

**Gate:** Spokesperson approves every quote; comms lead approves outlets (REVIEW_REQUIRED). **Guardrails:** No link schemes, no sponsored posts disguised as editorial, no mass templated outreach.

## ST09 Topic clusters built for query fan-out (win 65%, grade B, risk 1/3)

**What:** Map each target topic into the sub-questions an engine fans out to (definitions, how-to, cost, comparison, alternatives, pitfalls, for-whom); build a hub plus spokes with explicit internal links; make sure each sub-question has a self-contained passage somewhere.

**Why:** AI Mode and ChatGPT issue multiple sub-queries and fuse passages; a lower-ranking page with the best passage for a sub-query can win. Only ~38-40% of AI-cited pages rank in the organic top 10.

**Evidence:** Google/Digiday fan-out explanation; Ahrefs/BrightEdge overlap studies; practitioner consensus. Sources: S57,S42,S14

**Agent:** Topic cluster planner | autonomy PROPOSE | trigger Quarterly planning; weekly gap scan

**Steps:** 1 For each hub topic, generate the fan-out sub-questions (use 3 engines' 'related questions' plus LLM simulation). 2 Map existing pages/passages to sub-questions; mark gaps and overlaps. 3 Propose briefs for gaps with the owning page and internal-link plan. 4 Enforce one page per intent; merge overlaps. 5 Track sub-question citation coverage.

**Checks:** Each sub-question has exactly one owning passage; hub links to all spokes and back; no cannibalisation (two pages for one intent).

**Gate:** Content lead approves cluster plan. **Guardrails:** Briefs must specify information gain; no 'summarise top 10' briefs.

## ST07 Third-party review and independent listicle presence (win 60%, grade C, risk 1/3)

**What:** Get listed and well-reviewed on G2, Capterra, Trustpilot, Yelp, industry directories; pitch inclusion in independent 'best X' roundups and comparison articles. Do not mass-publish self-ranked listicles on your own domain.

**Why:** Review platforms are heavy sources for recommendation prompts; self-promotional listicles were linked to visibility losses and the self-ranked brand is absent from the answer in 83% of sampled cases.

**Evidence:** Peec AI review-platform finding; Nilink listicle analysis (C); Perplexity source mix (G2 top-5). Sources: S18,S30

**Agent:** Reviews and listings agent | autonomy PROPOSE | trigger Monthly audit; daily review alerts

**Steps:** 1 Audit presence and consistency on G2/Capterra/Trustpilot/Yelp/industry directories. 2 Identify independent roundups where the brand is absent; draft outreach with evidence of fit. 3 Draft review-request campaigns to recent happy customers (opt-in, no incentives that violate platform rules). 4 Draft responses to reviews for human send.

**Checks:** Profile facts match entity record; review requests follow platform policy; no fake or incentivised reviews.

**Gate:** CS lead approves outreach and responses. **Guardrails:** No review gating, no self-ranked listicles at scale, no fake reviews (FTC rule).

## ST11 Structured data hygiene (rich results and shopping, not a citation lever) (win 55%, grade B, risk 1/3)

**What:** Maintain accurate Organization, Product/Offer, Article, BreadcrumbList, FAQ (where shown) markup that matches visible text; validate with Rich Results Test and schema.org validator; keep it out of the 'AI citation' KPI.

**Why:** Ahrefs tracked 1,885 pages adding schema: AI Mode/ChatGPT effect indistinguishable from noise, AIO citations fell slightly. Schema still drives rich results and feeds shopping agents via Merchant Center.

**Evidence:** Ahrefs May 2026 (B); First Page Sage effect 0.4 pts (C); Google: structured data must match content (A). Sources: S08,S21,S04,S31

**Agent:** Structured data agent | autonomy PROPOSE | trigger On template change; monthly validation

**Steps:** 1 Generate JSON-LD from the same data source as visible content. 2 Validate with Rich Results Test and schema.org validator. 3 Diff schema values against rendered text (price, availability, dates, names). 4 Remove unsupported or decorative types. 5 Report rich-result eligibility.

**Checks:** 0 validation errors; 0 content/schema mismatches; only Google-supported types for rich results.

**Gate:** Developer review on template PR (REVIEW_REQUIRED). **Guardrails:** No markup for content not visible on the page; no fake ratings/FAQ.

## ST22 Conversational long-tail and FAQ coverage (win 55%, grade C, risk 1/3)

**What:** Mine real questions (sales calls, support tickets, People Also Ask, Reddit, AI tools' follow-up suggestions); answer them in natural-language Q&A blocks on the relevant page; keep answers durable and specific.

**Why:** AI prompts average ~23 words vs ~4 for Google; engines fan out into question-shaped sub-queries; FAQ blocks give retrievable passages (the FAQ schema itself is not the lever).

**Evidence:** HubSpot AEO guide (C); fan-out mechanism (B). Sources: S57,S14

**Agent:** Question mining agent | autonomy PROPOSE | trigger Monthly

**Steps:** 1 Cluster questions by intent and page. 2 Draft durable answers (no time-bound phrasing) with sources. 3 Place Q&A block on the owning page; avoid duplicate FAQ pages. 4 Track citation of each answer.

**Checks:** Each question maps to one page; answers <=120 words; sourced; no PII from tickets.

**Gate:** Editor approves. **Guardrails:** Strip customer data; do not create FAQ pages that duplicate existing content.

## ST21 Content pruning and consolidation (win 60%, grade B, risk 2/3)

**What:** Identify thin, duplicate, outdated or cannibalising pages; merge, redirect, update or noindex; keep the inventory of indexable pages lean and intentional.

**Why:** March-May 2026 core updates shifted visibility from aggregators and thin templated pages to original sources; site-wide quality signals matter more than page count.

**Evidence:** Core-update analyses (C); Google quality guidance (A). Sources: S60,S61,S73

**Agent:** Content pruning agent | autonomy PROPOSE | trigger Quarterly

**Steps:** 1 Flag pages with zero clicks and zero citations in 12 months, near-duplicate clusters (cosine >0.9), outdated topics. 2 Recommend action per page: update, merge+301, noindex, delete+410. 3 Preserve pages with links or conversions. 4 Execute after approval in batches; monitor.

**Checks:** No page with backlinks or conversions deleted; redirects map to closest topic; no redirect chains.

**Gate:** SEO lead approves batch (REVIEW_REQUIRED). **Guardrails:** Max 5% of inventory per batch; wait 4 weeks between batches.

## ST19 Multimodal assets: video, images, transcripts (win 55%, grade B, risk 1/3)

**What:** Publish explainer videos on YouTube with full transcripts, chapters and descriptions mirroring page facts; descriptive alt text; original diagrams and charts with captions.

**Why:** YouTube is the single most-cited domain in AI Overviews; Google explicitly recommends high-quality images and video; AI agents parse transcripts and chapters.

**Evidence:** Ahrefs citation share (B); Google guidance (A); Ahrefs YouTube-mention correlation 0.737 (B). Sources: S19,S03,S09

**Agent:** Multimodal asset agent | autonomy PROPOSE | trigger Per content brief

**Steps:** 1 Propose video outline and chapter list mirroring page sub-questions. 2 After human recording, generate transcript, chapters, description with canonical entity names and page link. 3 Generate charts from data notebook with alt text and captions. 4 Verify text facts and video facts match.

**Checks:** Transcript accuracy >=98% on spot check; alt text descriptive; facts consistent across formats.

**Gate:** Marketing approves publish. **Guardrails:** No synthetic presenters claiming to be real staff without disclosure.

## ST06 Community presence: Reddit and YouTube (win 55%, grade C, risk 2/3)

**What:** Maintain authentic, non-promotional Reddit participation in relevant subreddits (expert answers, AMAs, disclosure) and a YouTube channel with transcripts, chapters and topical depth. Never drop links from new accounts; never use bots to post.

**Why:** Reddit and YouTube are the most-cited domains across engines (Peec 30M sources; Ahrefs AIO 21% YouTube, 18.5% Reddit). But ChatGPT cut Reddit's citation share sharply in Aug 2026 and tilted to primary sources, so weight YouTube and own-site data higher for ChatGPT.

**Evidence:** Peec AI, Ahrefs, SE Ranking citation-share studies (B); Promptwatch Reddit collapse (D); Sprout Social mattress-brand karma case (C). Sources: S18,S19,S36,S55,S37

**Agent:** Community listening agent | autonomy ASSIST only (humans post) | trigger Daily

**Steps:** 1 Surface threads where the brand or category is discussed and a helpful expert answer is possible. 2 Draft a suggested answer with sources and a disclosure line. 3 A named employee edits and posts from their own account. 4 Log thread, answer, and later citations. 5 For YouTube: propose video topics from unanswered questions; produce transcript and chapters after recording.

**Checks:** Disclosure present; no link in first 10 contributions per subreddit; answer adds information not in thread; subreddit rules checked.

**Gate:** Human posts every message (HARD_BLOCK on automated posting). **Guardrails:** No vote manipulation, no sockpuppets, no automated accounts; respect bans and rate limits; Reddit terms prohibit bot posting.

## ST17 Page experience and Core Web Vitals (win 45%, grade A, risk 1/3)

**What:** Keep field p75 LCP <=2.5s, INP <=200ms, CLS <=0.1 on important templates; fast, text-first pages for bots and users.

**Why:** Google lists page experience among the ways to succeed in AI search; 81% of AIO traffic is mobile. Direct ranking effect is small but it gates crawl efficiency and conversion.

**Evidence:** Google guidance (A); web.dev thresholds (A). Sources: S03,S28

**Agent:** Performance agent | autonomy AUTO (monitoring), PROPOSE (fixes) | trigger Weekly CrUX pull; on deploy (Lighthouse CI)

**Steps:** 1 Pull p75 CWV by template. 2 Diagnose regressions (LCP element, INP handlers, CLS sources). 3 Propose fixes as PRs with before/after lab numbers. 4 Verify field metrics after 28 days.

**Checks:** Field p75 thresholds met; no regression >10% on deploy.

**Gate:** Engineering review on PR. **Guardrails:** No lab-only success claims.

## ST24 Wikipedia and Wikidata presence (win 35%, grade C, risk 2/3)

**What:** Where the organisation is notable, ensure an accurate, neutral Wikipedia article and Wikidata item maintained per community rules (no paid editing without disclosure).

**Why:** Wikipedia dominates ChatGPT's top-ten citations and AI Mode's source mix; it anchors 'memory' citations.

**Evidence:** Citation-share studies (B/C). Achievability is low for non-notable brands and policy risk is real. Sources: S18,S19

**Agent:** Knowledge-base presence agent | autonomy ASSIST | trigger Quarterly

**Steps:** 1 Assess notability against Wikipedia guidelines. 2 Compile independent sources. 3 Draft neutral article text for a disclosed editor or request via Articles for Creation; maintain Wikidata item with references.

**Checks:** Only independent reliable sources; conflict-of-interest disclosed.

**Gate:** Comms lead and a disclosed human editor. **Guardrails:** No undisclosed paid editing; accept community decisions.

## ST15 Programmatic SEO with value gates and velocity caps (win 40%, grade C, risk 3/3)

**What:** Generate template pages only where each page carries unique, sourced, useful data; run a 5-page pilot, wait 4 weeks for indexation/engagement, then scale in waves under a weekly publishing cap tied to human review capacity.

**Why:** Scaled content abuse is judged on value and purpose, not authorship; Aug/Sep 2026 spam updates hit templated pages lacking unique value (40-95% losses reported). One new-domain case with research-then-write agent waves reached 479k impressions in 6 months.

**Evidence:** Google spam policy (A); spam-update reporting (B); agency and Reddit case studies (C/D). Sources: S02,S05,S06,S43,S44

**Agent:** Programmatic page agent | autonomy PROPOSE with velocity governor | trigger Wave-based (research wave, write wave, QA wave)

**Steps:** 1 Define value test: what unique sourced data each page adds. 2 Pilot 5 pages; wait 4 weeks; check indexation, impressions, engagement vs site median. 3 If pilot passes, publish in waves under a weekly cap (default 25 pages/week) that never exceeds human review capacity. 4 Auto-noindex pages whose data completeness <70%. 5 Monthly: prune pages with zero impressions after 90 days.

**Checks:** Per-page uniqueness score (non-boilerplate text share >=40%); data completeness; duplicate-title rate 0; sampled human review of 10% of each wave.

**Gate:** Pilot results reviewed by SEO lead before scaling (HARD_BLOCK). **Guardrails:** Hard publishing cap; no scaling on new domains before pilot evidence; stop on spam-update volatility.

