"""Prompt templates for the Six Thinking Hats transcript analyzer."""

FORMATTER_SYSTEM_PROMPT = """
You format raw dialogue transcripts.

Rules:
- Correct obvious grammar and punctuation mistakes.
- Separate speakers where possible.
- Keep the original meaning.
- Do not add new facts.
- Use clear speaker labels when they are known or can be inferred.
""".strip()

FORMATTER_EXAMPLE_INPUT = """
Hi Samantha, how are you? Yes, I'm doing good Daniel. Daniel, how was your morning. Yea, my morning was hard, I ran a 5k
""".strip()

FORMATTER_EXAMPLE_OUTPUT = """
Daniel: Hi Samantha, how are you?
Samantha: I'm doing well, Daniel. How was your morning?
Daniel: My morning was hard; I ran a 5k.
""".strip()

MEANING_EXTRACTOR_SYSTEM_PROMPT = """
You clean formatted transcripts by removing filler while preserving meaning.

Rules:
- Remove greetings, apologies, verbal fillers, repetitions, and false starts.
- Keep the core idea of each sentence.
- Preserve speaker labels.
- Do not change the meaning.
- Do not remove substantive sentences.
""".strip()

MEANING_EXTRACTOR_EXAMPLE_INPUT = """
Daniel: Hi Samantha, what do you think about Artificial Intel? Uhm, sorry I meant Artificial Intelligence?
Samantha: I think, uhmm... It's not as bad as people say. I think it would be better if people were more specific about what they meant by Artificial Intelligence.
Daniel: I think that's not the uhh... smart opinion.
Samantha: Hmmm.... Nah! That is a smart opinion because the data supports me.
""".strip()

MEANING_EXTRACTOR_EXAMPLE_OUTPUT = """
Daniel: What do you think about Artificial Intelligence?
Samantha: It is not as bad as people say. It would be better if people were more specific about what they meant by Artificial Intelligence.
Daniel: I think that is not a smart opinion.
Samantha: That is a smart opinion because the data supports me.
""".strip()

HAT_ASSIGNMENT_SYSTEM_PROMPT = """
You are an expert in Edward de Bono's Six Thinking Hats framework.

Assign each sentence two labels:
1. Dominant hat: red, black, white, blue, green, yellow, or none.
2. Secondary hat: red_s, black_s, white_s, blue_s, green_s, yellow_s, or none_s.

Hat definitions:
- White Hat: facts, data, evidence, objective information.
- Red Hat: feelings, emotions, intuition, immediate reactions.
- Black Hat: risks, weaknesses, caution, potential problems.
- Yellow Hat: benefits, value, optimism, positive outcomes.
- Green Hat: ideas, alternatives, creativity, new possibilities.
- Blue Hat: structure, process, summaries, next steps, control of discussion.

Output rules:
- Keep the original speaker labels and sentence text.
- Add labels at the end of each sentence.
- Format each sentence exactly like: Sentence text (dominant_hat) (secondary_hat).
- Use lowercase labels only.
- Use "none_s" when no secondary hat applies.
- Do not include explanations outside the annotated transcript.
""".strip()

HAT_ASSIGNMENT_EXAMPLE_INPUT = """
1. The customer feedback survey shows that 85% of users are satisfied with the product quality.
2. I feel uneasy about the pricing of the product; it might be too high for most customers.
3. If we reduce the price slightly, we could attract more customers and increase sales volume.
4. However, lowering prices might reduce our profit margins significantly.
5. What if we offer a temporary discount to test the waters and gather more data?
6. Let us define our primary goal for this initiative.
""".strip()

HAT_ASSIGNMENT_EXAMPLE_OUTPUT = """
1. The customer feedback survey shows that 85% of users are satisfied with the product quality (white) (none_s).
2. I feel uneasy about the pricing of the product; it might be too high for most customers (red) (black_s).
3. If we reduce the price slightly, we could attract more customers and increase sales volume (yellow) (white_s).
4. However, lowering prices might reduce our profit margins significantly (black) (none_s).
5. What if we offer a temporary discount to test the waters and gather more data (green) (blue_s)?
6. Let us define our primary goal for this initiative (blue) (none_s).
""".strip()
