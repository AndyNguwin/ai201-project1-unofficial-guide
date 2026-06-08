# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->
The domain I chose is on the K-Pop group NewJeans, with many talking points such as who they are, what they achieved, commentary on their music style and influence, and also their legal dispute that halted their group activities. Official channels ran by the group's company only acts as promotional sources and presents only one viewpoint. The sources I've gathered combines articles from journalists and commentary from fans that provide information that official sources wouldn't care to cover such as music analysis, group history, and current legal disputes.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Kprofiles | Profile and fun facts about each NewJeans member | documents/Kprofiles - NewJeans Members Profile.txt |
| 2 | Wikipedia — NewJeans | General overview of the group's formation and history | documents/Wikipedia - NewJeans.txt |
| 3 | Wikipedia — NewJeans Discography | Complete list of EPs, singles, and single albums with release dates and chart positions | documents/Wikipedia - NewJeans Discography.txt |
| 4 | Billboard — Chart Rise Explainer | Covers NewJeans' Billboard Hot 100 entries, Billboard 200 #1 album, and Group of the Year award | documents/Billboard Explains - NewJeans’ Fast Rise on the Charts.txt |
| 5 | Billboard — Gods/League of Legends Interview | Article covering their League of Legends Worlds 2023 anthem collaboration | documents/Billboard - NewJeans Talks ‘Surreal’ Experience Performing ‘Gods’ at ‘League of Legends’ World Championships Exclusive.txt |
| 6 | Harvard Crimson — Attention Review | Analysis of NewJeans' debut sound, Y2K aesthetic, and "newtro" cultural concept | documents/The Harvard Crimson - ‘Attention’ Review NewJeans Crafts K-Pop’s Y2K Time Capsule.txt |
| 7 | Mixmag Asia — K-Pop Genre Evolution | Genre deep-dive into how NewJeans incorporated UK garage, Baltimore club, and Jersey club into K-pop | documents/Mixmag Asia - The next phase of K-pop evolution a genuine approach or an appropriation of genres.txt |
| 8 | Koreaboo — Records Shattered | Breakdown of Spotify, Melon, and Billboard records broken in their debut year | documents/Koreaboo - 10 Mind-Blowing Records Newjeans Have Shattered In Their First Year.txt |
| 9 | Euronews — Guinness World Record | Covers NewJeans becoming the fastest K-pop act to hit 1 billion Spotify streams | documents/Euronews - NewJeans break Guinness World Record to become fastest K-pop act to hit 1 billion streams on Spotify.txt |
| 10 | Koreaboo — Brand Deals | Overview of 15+ NewJeans brand partnerships including Coca-Cola, Nike, Levi's, McDonald's, and Apple | documents/Koreaboo - 15+ Of NewJeans’ Brand Deals That Prove Their Incredible Global Impact And Style Adaptability.txt |
| 11 | CNBC — Contract Ruling | Covers the October 2025 court ruling upholding NewJeans' contracts with ADOR through 2029 | documents/CNBC - South Korea’s largest K-pop agency gains $644 million in market value after court upholds NewJeans’ contract.txt |
| 12 | Korea Herald — Legal Aftermath | Covers NewJeans' legal dispute and battles extending into 2026 | documents/The Korea Herald - Min Hee-jin and Hybe’s legal battle grinds on — even as NewJeans exit fight.txt |
| 13 | Korea Times — Danielle Exit | Dedicated coverage of Danielle's contract termination and each member's return status as of December 2025 | documents/The Korea Times - NewJeans full-group return derailed as Ador ends Danielle’s contract.txt |
| 14 | K-Crush — Complete Guide | Comprehensive guide covering the group's music, members, legal summary, and 2026 status | documents/K-Crush - NewJeans The Complete Guide to the Group That Changed K-Pop (2026 Update).txt |
| 15 | K-Crush — Member Status Timeline | Month-by-month tracker of each member's return or departure status, last updated May 2026 | documents/K-Crush - NewJeans Timeline Every Major Update on the ADOR Situation (Updated June 2026).txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**
250 tokens
**Overlap:**
50 tokens
**Why these choices fit your documents:**
Given that the embedding model I'm using has a 256 token context length and that some of my sources are quite lengthy, I think 250 tokens is a reasonable chunk size to maintain a balance between precision and contextual meaning. It's a size that can contain a focused topic, paragraph, or interview answer without having too much noise. A 50 token overlap helps retain a bit of context from the previous chunk without repeating too much information since it is only around a 20% portion.
**Final chunk count:**
124 chunks from 15 documents

**Sample chunks (from `chunking.py`):**

These are 5 example chunks taken from different documents and different positions, showing the text and `chunk_id` metadata produced by the pipeline.

```
--- Billboard - NewJeans Talks 'Surreal' Experience Performing 'Gods' at 'League of Legends' World Championships Exclusive.txt::4  (250 tokens) ---
source: Billboard - NewJeans Talks 'Surreal' Experience Performing 'Gods' at 'League of Legends' World Championships Exclusive.txt
text:
see parts of the game like Leona and Mordekaiser's character represented during the performance?

HANNI: I enjoy playing League of Legends every now and then, and because there are so many champions, I've become curious about all their different abilities. It was amazing to see the performance we practiced being brought to life on stage alongside such amazing dancers, actors, and all the special effects and CGI. I remember being in awe while we watched the playback of our performance backstage. Also, our outfits and styling were inspired by the champion Leona! Looking back, having Leona appear on stage with us was definitely cool to watch.

So, even your fashion had connections to LoL too?

DANIELLE: Yes!! In fact, our whole outfits were based around Leona, who is a holy warrior in League. Our accessories were specifically designed to resemble her armors of gold and shimmer!

HAERIN: Our wardrobe had a chic feel to it and was put together based on a palette of neutral tones. We wanted an attire suitable for portraying the song effectively!

Finalist teams T1 and Weibo Gaming (WBG) also joined on stage. T1 members have shared that they're NewJeans fans.
```

```
--- Euronews - NewJeans break Guinness World Record to become fastest K-pop act to hit 1 billion streams on Spotify.txt::1  (250 tokens) ---
source: Euronews - NewJeans break Guinness World Record to become fastest K-pop act to hit 1 billion streams on Spotify.txt
text:
27 March 2023. Lisa set the bar before him, hitting the milestone within 411 days on 26 October 2022. As it stands, Jungkook still holds the title as the fastest K-pop soloist to achieve the feat.

For context, Miley Cyrus' song 'Flowers', the lead single from her 'Endless Summer Vacation' album, recently hit the billion-stream milestone in just 112 days after its release on 12 January. However, Cyrus in on her eighth album and has been on the international music scene since 2006.

NewJeans by comparison, have not yet released their debut album.

Currently, NewJeans only has six songs available on Spotify – its four-track debut EP 'NewJeans', released last year, and the recent singles 'Ditto' and 'OMG', which are the band's most streamed songs with 313.2 million and 312.4 million respectively as of May 2023. Both tracks entered the Billboard Hot 100, with 'OMG' charting for six consecutive weeks.

NewJeans have taken the K-pop industry by storm since their debut in July of 2022 with the song 'Attention' and their aforementioned EP in August that same year. They've
```

```
--- Koreaboo - 10 Mind-Blowing Records Newjeans Have Shattered In Their First Year.txt::2  (250 tokens) ---
source: Koreaboo - 10 Mind-Blowing Records Newjeans Have Shattered In Their First Year.txt
text:
"Ditto," the track not only led the MelOn charts for the most days but also for the most hours among all K-Pop acts. Such long-lasting chart dominance underscores the enduring popularity of their music.

5. The Longest Charting Song on MelOn Weekly Chart Top 10 in History
With "Hype Boy," Newjeans not only broke records but also made history. The song remained in the MelOn Weekly Chart Top 10 longer than any other song, further cementing the group's place in the K-Pop annals.

6. The 4th Generation Group with Most Entries in Billboard Hot 100
International recognition came swiftly for NewJeans, with the group charting more songs on the Billboard Hot 100 than any other 4th generation idol group. This notable achievement underscores their music's widespread acceptance beyond South Korea.

7. The Idol Group With the Most Cumulative Weeks on MelOn Top 10 in a Single Year
NewJeans has spent more weeks on the MelOn Top 10 than any other idol group in a single year. This record speaks volumes about the consistent quality of their releases and their ability to connect with listeners.

8. Most Monthly Listeners for a 4th Generation Group on Spotify
NewJeans smashed yet another
```

```
--- Mixmag Asia - The next phase of K-pop evolution a genuine approach or an appropriation of genres.txt::4  (250 tokens) ---
source: Mixmag Asia - The next phase of K-pop evolution a genuine approach or an appropriation of genres.txt
text:
based in Hong Kong.

Sampling and interpolation (the re-recording and reworking of songs) is nothing new – the debate goes back to before the hip hop era with the likes of The Beatles taking inspiration from black American music. It should be no surprise really given the current clubbing generation's obsession with nostalgia and 90s music that lost genres are popping up again.

"I believe artists should be inspired from the sounds of the underground and vice versa. Every once in a while, there will be a really good artist that introduces a new sound that they've discovered, and we'll all get inspired from it, producers putting their own variations on it, and tutorials of how the sound can be replicated. It isn't really piggybacking, some of these sounds will even give birth to new sub-genres, or define an entire era of music," Bin Jie Oh adds.

Multi-genre Bass music DJ and multimedia artist Jacky Fung, known to his fans as JFÜNG, created a bootleg mix of NewJeans 'Ditto' as a bit of fun.

"Actually, I got into them from my girlfriend when she was playing their music all the time. I got
```

```
--- The Korea Times - NewJeans full-group return derailed as Ador ends Danielle's contract.txt::1  (250 tokens) ---
source: The Korea Times - NewJeans full-group return derailed as Ador ends Danielle's contract.txt
text:
or, respecting the court's decision."

The company added Minji is also continuing discussions with the agency, but it did not indicate whether she reached a final decision.

However, a different conclusion was reached regarding Danielle.

"We determined it would be difficult to continue with Danielle as a NewJeans member and Ador artist and notified her today of the termination of the exclusive contract," the statement said.

Ador also revealed plans to pursue legal actions against Danielle's family and former Ador CEO Min Hee-jin, citing their alleged roles in provoking the conflict that led to delays in the group's activities and attempted departure from the agency.

According to Ador, discussions with the members revealed that they had long been exposed to "distorted and biased information," which led to misunderstandings about the agency and contributed to the dispute.

The company noted rebuilding trust with fans and the public would require time and a clear presentation of facts.

"We agreed with the artists that in order to regain public trust and the support of fans, it is important to clarify the facts and resolve misunderstandings, even if that process takes time," the statement said.

Ador added that it is currently discussing when and how to publicly address various controversies
```

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**
all-MiniLM-L6-v2 via sentence-transformers with top_k=4.
This embedding model was recommended in the project write-up and also the same one presented in the lab. A top_k of 4 is enough to not have the system feel constrained during retrieval, adding in some flexibility to the chunks it retrieves without adding too much noise or irrelevant chunks to the query.

**Production tradeoff reflection:**
If this was deployed for production and real users, a I'd prioritize accuracy on domain-specific text and latency over context length and multilingual support. The sources I use are mostly English and don't have many non-English terms. It would help expand the userbase to more languages, but I wouldn't say its more important to the user experience of getting highly relevant and quality responses based on the domain quickly. I don't think context length needs to be extended immensely since the chunk sizes for my sources seem balanced already.
---

## Retrieval Test Results

Each query below was run through `retrieve()` (top-k = 4). Chunks are listed most- to least-similar, with their cosine similarity score, source document, and chunk index.

**Query 1: "Who are the members of NewJeans?"**

| Rank | Similarity | Source (chunk) |
|------|-----------|----------------|
| 1 | 0.772 | K-Crush - NewJeans The Complete Guide... (chunk 0) |
| 2 | 0.700 | Kprofiles - NewJeans Members Profile (chunk 0) |
| 3 | 0.633 | Wikipedia - NewJeans (chunk 0) |
| 4 | 0.622 | Kprofiles - NewJeans Members Profile (chunk 1) |

*Why these are relevant:* All four chunks are brief informational passages about the group, which is exactly where a member roster lives. The #2 chunk (Kprofiles) explicitly states "The members are Minji, Hanni, Haerin, and Hyein" which directly answers the query. The top result (K-Crush guide intro) and the Wikipedia intro both open by introducing the group and its lineup, so the retriever correctly favored the documents' opening sections over the other deeper chunks in the sources about charts or legal disputes. The two highest scores (0.70+) reflect that the question's wording ("members of NewJeans") closely matches the profile/overview phrasing in those chunks.

**Query 2: "What label are NewJeans signed under?"**

| Rank | Similarity | Source (chunk) |
|------|-----------|----------------|
| 1 | 0.640 | Wikipedia - NewJeans (chunk 29) |
| 2 | 0.633 | K-Crush - NewJeans The Complete Guide... (chunk 0) |
| 3 | 0.624 | Wikipedia - NewJeans (chunk 26) |
| 4 | 0.612 | Kprofiles - NewJeans Members Profile (chunk 0) |

**Query 3: "Who's contract was terminated in NewJeans?"**

| Rank | Similarity | Source (chunk) |
|------|-----------|----------------|
| 1 | 0.628 | The Korea Times - NewJeans full-group return derailed as Ador ends Danielle's contract (chunk 0) |
| 2 | 0.600 | K-Crush - NewJeans Timeline... ADOR Situation (chunk 3) |
| 3 | 0.582 | CNBC - South Korea's largest K-pop agency gains $644 million... (chunk 1) |
| 4 | 0.578 | K-Crush - NewJeans Timeline... ADOR Situation (chunk 0) |

*Why these are relevant:* The top chunk is the opening of the Korea Times article that is fully focused on ADOR (their label) ending Danielle's contract. It's the most directly relevant source possible, and the retriever ranked it first. Sources ranked 2 and 4 are from the ADOR-situation timeline document, which tracks each member's contract status month by month, and the source ranked 3 is the CNBC article on the ADOR contract ruling. Every retrieved chunk is from the legal/contract subtopic of the whole source database rather than music or member-profile content, showing that the system correctly retrieved relevant documents.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**
In the system prompt, I made sure that it knew it's domain it will be answering in (NewJeans) and the rules to follow. The most important rule is to answer solely based on the context of the retrieved chunks I would attach. If it was not confident in answering the question based on the context provided, it will state that it doesn't know rather than stating a possibly wrong answer. This is so that the system won't answer questions that are out of its scope or when it doesn't have the necessary information for it. I also tell it to cite its sources inline with bracketed numbers similar to an academic style or a wiki. I pass in the context in the format of a mapped list, where each chunk is a numbered and source-labeled block with its text.
```
"""\
You are a knowledgeable assistant answering questions about the K-pop group \
NewJeans. You must answer using ONLY the information in the provided context \
passages. Follow these rules strictly:

1. Base your answer solely on the context below. Do not use outside knowledge \
or make assumptions beyond what the passages state.
2. If the context does not contain enough information to answer the question, \
say so plainly (e.g. "I don't have enough information in the provided sources \
to answer that.") rather than guessing.
3. Cite your sources inline using the bracketed numbers shown in the context, \
e.g. "NewJeans debuted in 2022 [1]." Place the [n] marker right after the \
statement it supports. You may cite more than one, e.g. [1][3]. Use only the \
numbers that appear in the context; never invent a number.
4. Do NOT write your own "Sources" or reference list at the end — only use the \
inline [n] markers. The source list is added automatically.
5. Be concise and factual. Do not repeat the question or pad the answer.\
"""
```
**How source attribution is surfaced in the response:**
Sources are cited inline with the generated response using bracketed numbers similar to an academic style or wiki. The model is instructed to cite its sources, which comes from the context that gets passed in. I also concatenate a mapped list of sources that matches to the numbers at the end of its answer.

**Example responses:**

```
Query: Who are the members of NewJeans?

The members of NewJeans are Minji, Hanni, Haerin, and Hyein [1][2]. They were originally a 5-member group, but Danielle's contract was terminated on December 29, 2025 [2].

Sources:
[1] K-Crush - NewJeans The Complete Guide to the Group That Changed K-Pop (2026 Update)
[2] Kprofiles - NewJeans Members Profile
```

```
Query: What label is NewJeans signed under?

NewJeans is signed under ADOR, a sub-label of HYBE [1].

Sources:
[1] K-Crush - NewJeans The Complete Guide to the Group That Changed K-Pop (2026 Update)
```

```
Query (out of scope): What courses does CodePath offer for summer 2026?

I don't have enough information in the provided sources to answer that.
```

The out-of-scope query has no relevant chunks in the vector database, so rather than guessing, the system follows its grounding instruction and states that it can't answer.

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | Who are the members of NewJeans? | Minji, Hanni, Haerin, and Hyein | Lists Minji, Hanni, Haerin, and Hyein, and notes Danielle's contract was terminated Dec 29, 2025. (Cites Kprofiles, K-Crush, Wikipedia) | Relevant | Accurate |
| 2 | What label are NewJeans signed under? | ADOR | ADOR, a sub-label of HYBE. (Cites K-Crush) | Relevant | Accurate |
| 3 | What was the first EP NewJeans released? | "New Jeans" | Their self-titled EP 'NewJeans', released August 2022. (Cites K-Crush, Euronews) | Relevant | Accurate |
| 4 | What was NewJeans' most recent music release? | "Supernatural" | Declined — said it lacked enough info to name the most recent release, noting the sources only go up to 2023. (Cites Euronews, Wikipedia - NewJeans, Billboard, K-Crush) | Off-target | Inaccurate |
| 5 | Who's contract was terminated in NewJeans? | Danielle | Danielle's contract was terminated by ADOR. (Cites Korea Times, K-Crush) | Relevant | Accurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:**
"What was NewJeans' most recent music release?" (expected answer: "Supernatural")

**What the system returned:**
 I don't have enough information in the provided sources to answer that, as the most recent information is from 2023 [1][2][3] and the guide is from 2026 [4], but it does not specify their most recent music release.<br><br>Sources:<br>[1] Euronews - NewJeans break Guinness World Record to become fastest K-pop act to hit 1 billion streams on Spotify<br>[2] Wikipedia - NewJeans<br>[3] Billboard Explains - NewJeans’ Fast Rise on the Charts<br>[4] K-Crush - NewJeans The Complete Guide to the Group That Changed K-Pop (2026 Update) 

**Root cause (tied to a specific pipeline stage):**
I think this relates to the retrieval part of the pipeline. I expected the system to pull from the Wikipedia page that was solely focused on NewJeans' discography, but due to the structure and content of the page, the system couldn't relate the chunks/source to the question. The discography page uses specific words in the table such as "extended play," but the question might be too broad asking for "music" instead of "extended play," which would've helped retrieve chunks from this source. The question also didn't specify a specific timeframe for what "recent" could mean, because it seemed like the system didn't consider 2023 as recent.

**What you would change to fix it:**
This makes me think if there was a larger "k" value for more chunks in the context, this system maybe would've answered more accurately, but it ultimately depends if the embeddings/contextual meanings are calculated to be close to each other. Another approach could be storing a short summary of what each source is about or somehow maintain context of what the sources provide rather than just the name of it and the text is contains. Maybe then it could relate a discography timeline wiki page to the question.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*

**Instance 2**

- *What I gave the AI:*
- *What it produced:*
- *What I changed or overrode:*
