# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
The domain I chose is on the K-Pop group NewJeans, with many talking points such as who they are, what they achieved, commentary on their music style and influence, and also their legal dispute that halted their group activities. Official channels ran by the group's company only acts as promotional sources and presents only one viewpoint. The sources I've gathered combines articles from journalists and commentary from fans that provide information that official sources wouldn't care to cover.
---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source | Description | URL or location |
|---|--------|-------------|-----------------|
| 1 | Kprofiles | Profile and fun facts about each NewJeans member | https://kprofiles.com/newjeans-members-profile/ |
| 2 | Wikipedia — NewJeans | General overview of the group's formation and history | https://en.wikipedia.org/wiki/NewJeans |
| 3 | Wikipedia — NewJeans Discography | Complete list of EPs, singles, and single albums with release dates and chart positions | https://en.wikipedia.org/wiki/NewJeans_discography |
| 4 | Wikipedia — New Jeans EP | Breakdown of their debut EP including themes, sound, and chart performance | https://en.wikipedia.org/wiki/New_Jeans_(EP) |
| 5 | Wikipedia — OMG EP | Breakdown of their second release including themes, sound, and chart performance | https://en.wikipedia.org/wiki/OMG_(NewJeans_EP) |
| 6 | Wikipedia — Get Up EP | Breakdown of their most commercially successful EP including critical reception | https://en.wikipedia.org/wiki/Get_Up_(NewJeans_EP) |
| 7 | Billboard — Chart Rise Explainer | Covers NewJeans' Billboard Hot 100 entries, Billboard 200 #1 album, and Group of the Year award | https://www.billboard.com/music/chart-beat/billboard-explains-newjeans-rise-on-charts-1235611739/ |
| 8 | Billboard — Gods/League of Legends Interview | Article covering their League of Legends Worlds 2023 anthem collaboration | https://www.billboard.com/music/pop/newjeans-interview-gods-league-of-legends-world-championships-2023-exclusive-1235519282/ |
| 9 | Harvard Crimson — Attention Review | Analysis of NewJeans' debut sound, Y2K aesthetic, and "newtro" cultural concept | https://www.thecrimson.com/article/2022/9/20/newjeans-kpop-girlgroup-hybe-attention-debut-single/ |
| 10 | Mixmag Asia — K-Pop Genre Evolution | Genre deep-dive into how NewJeans incorporated UK garage, Baltimore club, and Jersey club into K-pop | https://mixmag.asia/feature/new-jeans-k-pop-evolution-aesthetic-dance-music-genres-breaks-bass |
| 11 | Koreaboo — Records Shattered | Breakdown of Spotify, Melon, and Billboard records broken in their debut year | https://www.koreaboo.com/lists/records-newjeans-shattered-in-first-year/ |
| 12 | Euronews — Guinness World Record | Covers NewJeans becoming the fastest K-pop act to hit 1 billion Spotify streams | https://www.euronews.com/culture/2023/05/09/newjeans-break-guinness-world-record-to-become-fastest-k-pop-act-to-hit-1-billion-streams- |
| 13 | Koreaboo — Brand Deals | Overview of 15+ NewJeans brand partnerships including Coca-Cola, Nike, Levi's, McDonald's, and Apple | https://www.koreaboo.com/lists/newjeans-brand-ambassador-deals-global-impact-style-adaptability/ |
| 14 | CNBC — Contract Ruling | Covers the October 2025 court ruling upholding NewJeans' contracts with ADOR through 2029 | https://www.cnbc.com/2025/10/30/newjeans-contract-ruling-valid-hybe-gains-almost-630-million-.html |
| 15 | Korea Herald — Legal Aftermath | Covers NewJeans' legal dispute and battles extending into 2026 | https://www.koreaherald.com/article/10640428 |
| 16 | Korea Times — Danielle Exit | Dedicated coverage of Danielle's contract termination and each member's return status as of December 2025 | https://www.koreatimes.co.kr/entertainment/k-pop/20251229/newjeans-full-group-return-derailed-as-ador-ends-danielles-contract |
| 17 | K-Crush — Complete Guide | Comprehensive guide covering the group's music, members, legal summary, and 2026 status | https://k-crush.com/newjeans-complete-guide-2026/ |
| 18 | K-Crush — Member Status Timeline | Month-by-month tracker of each member's return or departure status, last updated May 2026 | https://k-crush.com/newjeans-timeline-2026-updates/ |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | | |
| 2 | | |
| 3 | | |
| 4 | | |
| 5 | | |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
