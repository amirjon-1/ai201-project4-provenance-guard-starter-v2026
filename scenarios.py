"""
What your test runs. ← UNIT 8, MILESTONE 3

Each of your five criteria needs something run against it. A criterion about
false positives needs your own writing. One about label coverage needs inputs
across the score range. One about the appeal path needs a real content_id.

Working that out is Milestone 3's first step, and this file is where you write
it down. `run_eval.py` runs everything here three times.

Two are filled in as examples. Replace them with what your criteria actually
need — these are a shape, not a set.

A scenario carries **either** of these:

    "texts"   a list of strings. Each is sent as {"text": ..., "creator_id": ...}
              with a creator_id made up for you. Use this for most criteria.

    "bodies"  a list of whole request bodies, sent exactly as written. Use this
              when the malformed request IS the point — empty text, no `text`
              field at all, something enormous. A bad-input criterion needs it,
              because you cannot express "the field is missing" as a string.
"""

SCENARIOS = [
    {
        "name": "my own writing",
        "criterion": 1,
        # 10 pieces of human-written text from my own drafts, notes, and messages.
        # These are casual, personal, and varied — the kind of writing a real
        # person does and an AI-detection system should not be flagging.
        "texts": [
            # 1. Personal observation, written a few months ago
            "I've been thinking a lot about how public transit works in this city. "
            "Every morning I watch people squeeze onto buses that come every 20 minutes "
            "and I wonder who decided that was acceptable. My commute used to be a 10-minute "
            "bike ride. Now it's a 45-minute thing where I stand in a metal box that smells "
            "like wet umbrellas. I miss the bike but it got stolen last spring and I haven't "
            "gotten around to replacing it, which I realize is partly my fault.",

            # 2. Casual email draft to a former professor
            "Hi, sorry to bother you out of nowhere. I was your student in the fall of 2022 "
            "and I've been thinking about the conversation we had after the last class — the "
            "one about whether measurement error compounds or cancels. I think I finally "
            "understand what you were getting at, three years later. Anyway I wanted to say "
            "thanks. I ended up going into data work and that specific conversation comes up "
            "more than you'd expect.",

            # 3. Notes from a weekend trip
            "The ferry to the island was rougher than I expected. Someone ahead of me in line "
            "had a dog that wouldn't stop looking at me, one of those very serious looks that "
            "dogs do when they've made a decision about you. The crossing took about forty "
            "minutes and I spent most of it watching the mainland get smaller. There was a "
            "point where you couldn't see either shore and that was the best part.",

            # 4. Opinion piece fragment, unfinished
            "The problem with open offices isn't that they're loud — people learn to tune out "
            "noise. The problem is that they make you visible in a way that's hard to describe "
            "without sounding paranoid. You're always slightly performing. You can't stare at "
            "the ceiling when you're stuck on something because someone will come over and ask "
            "if you need help. I don't need help; I need to stare at the ceiling.",

            # 5. Personal journal entry
            "Bad sleep again. I've been keeping track in a notebook and the pattern is pretty "
            "clear: I fall asleep fine but wake up around 3am and can't get back down. Read "
            "online that this is a sign of anxiety, which, yes, obviously, but knowing that "
            "doesn't make 3am less bleak. Made coffee at 4:30. The sky was doing that thing "
            "where it goes from black to grey without any real transition. Finished the book "
            "I'd been dragging out for weeks. It ended badly.",

            # 6. Message to a group chat about weekend plans
            "Okay so I looked up the place and the reviews are mixed in a way I find suspicious — "
            "like either it's genuinely a 50/50 place or one side is review-bombing. The photos "
            "look fine but photos are meaningless. Someone who's been there is worth more than "
            "fifty five-star reviews. I'm fine going anyway; I just want to know what we're "
            "walking into. What time are we thinking? After 7 is better for me.",

            # 7. Reflective paragraph about learning to cook
            "I taught myself to cook properly during the pandemic, which is a cliche, but it "
            "happened to be true for me. Before that I could boil pasta and that was about it. "
            "Now I can make three things well: a good stew, dumplings from scratch, and a cake "
            "that my mother-in-law has requested twice at family dinners. The dumplings took "
            "the longest because folding them is a physical skill and YouTube only gets you so far.",

            # 8. Informal analysis of a habit
            "I keep starting books and not finishing them. My shelf has about fifteen bookmarks "
            "in various places and I've told myself this is fine, that it means I'm reading "
            "widely, but honestly I think I just lose interest when things get hard. The books "
            "I do finish are usually ones I read in a weekend. The ones I don't are the ones "
            "I carry around and dip into — which is exactly the kind of reading I always thought "
            "I wanted to do, and apparently can't actually sustain.",

            # 9. Personal narrative fragment
            "My grandmother kept a garden that was completely impractical for where she lived. "
            "Too hot, wrong soil, no space to speak of. She grew tomatoes that weren't quite "
            "right and herbs that bolted in the summer and a fig tree that never produced figs. "
            "She watered it every morning anyway. When I asked her why she kept at it she said "
            "she liked having something to check on. That's the whole answer.",

            # 10. Stream-of-consciousness about a decision
            "I'm trying to decide whether to apply for the job or not and the problem is I "
            "genuinely can't tell if I'm hesitating because it's wrong for me or because I'm "
            "scared. These feel different from the inside but I've been wrong about which one "
            "it was before. The job is a good one. The city is not one I'd choose on my own. "
            "My partner is flexible about it but 'flexible' is not the same as 'enthusiastic.' "
            "I have until Friday and right now I'm leaning toward applying just to see what happens.",
        ],
    },

    {
        "name": "score spread",
        "criterion": 2,
        # Two texts: one clearly AI-generated, one clearly human. They should
        # score at least 0.25 apart on the combined score.
        "texts": [
            # Clearly AI — raw GPT-style output, no editing.
            "The implementation of a comprehensive framework for data management "
            "represents a significant advancement in the field of information technology. "
            "This framework encompasses multiple components that work together to ensure "
            "optimal performance and reliability. The integration of advanced algorithms "
            "enables efficient processing of large volumes of data. Furthermore, the system "
            "incorporates robust error handling mechanisms to maintain data integrity. "
            "The resulting solution provides a scalable and maintainable architecture "
            "that can be adapted to meet evolving business requirements.",

            # Clearly human — a personal paragraph I wrote.
            "My dad doesn't have much patience for technology but he learned to use video "
            "calls during the pandemic and now he calls every Sunday. He always starts with "
            "the weather where he is, then asks if I'm eating enough, then circles around "
            "to whatever he actually wanted to say about twenty minutes in. Last week it "
            "was that my cousin is getting married and nobody wanted to tell me directly "
            "because I'm still not over my own. He's not wrong about that; I just wish "
            "he'd had the conversation sooner rather than building up to it in the third act.",
        ],
    },

    {
        "name": "label coverage",
        "criterion": 3,
        # Three texts that should land in different score bands.
        # Need at least one in each label zone: AI, human, and unsure.
        "texts": [
            # Should score > 0.65 (high-confidence AI)
            "The analysis demonstrates that the proposed methodology yields significant "
            "improvements in performance metrics. The experimental results confirm that "
            "the implemented solution effectively addresses the identified challenges. "
            "The evaluation metrics indicate a substantial increase in efficiency. "
            "The findings suggest that this approach represents a viable solution "
            "for the problem domain. The results are consistent across all test cases.",

            # Should score < 0.35 (high-confidence human)
            "Every time I walk past that bakery on the corner I think about quitting my "
            "job and learning to make croissants professionally. I've looked it up — there "
            "are programs in France that take like six months. My French is terrible. "
            "I don't have six months. The croissants from that place are genuinely the "
            "best thing I eat in a given week, and I think about that probably too much "
            "for someone who also cares about their career.",

            # Should score 0.35-0.65 (unsure) — structured but personal
            "Learning a new programming language in your thirties is a strange experience. "
            "The syntax feels manageable. The idioms take longer. There is a point, usually "
            "around the third week, where the language stops feeling like a translation "
            "problem and starts feeling like something you can think in directly. "
            "I am not at that point yet with Rust. I am still translating everything "
            "from Python in my head, which is slow, and apparently wrong in ways I do not "
            "fully understand yet.",
        ],
    },

    {
        "name": "appeal path",
        "criterion": 4,
        # The appeal path can't be tested through /submit alone — it needs
        # a content_id from a prior submission. This scenario sends one text
        # (which produces a content_id), but the actual appeal flow is tested
        # by hand in a separate step documented in the README's Run Log section.
        # What we can test here is that the text gets a decision and a content_id
        # comes back (prerequisite for appeal testing).
        "texts": [
            "I went to see the film last Thursday with a couple of friends from work. "
            "It was not what I expected — a lot quieter than the trailer suggested. "
            "The ending divided us. My colleague thought it was the whole point. "
            "I thought it was the director giving up. We argued about it for an hour "
            "over drinks, which I think means the film worked regardless of who was right.",
        ],
    },

    {
        "name": "bad input",
        "criterion": 5,
        # Four malformed bodies. Each should come back as 400 (not 500 or a crash).
        "bodies": [
            {"text": "", "creator_id": "eval_bad_empty"},
            {"creator_id": "eval_bad_missing_text"},
            {"text": "short", "creator_id": "eval_bad_short"},
            {"text": None, "creator_id": "eval_bad_null"},
        ],
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )
    return problems
