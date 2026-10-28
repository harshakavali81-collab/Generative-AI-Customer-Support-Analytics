# Retrieval and generation model card

**Default:** locally computed sparse normalized TF-IDF vectors + cosine search and rule-guided extractive response. Not a generative model despite the optional LLM integration; no training and no network access are needed in offline mode.

**Optional:** external OpenAI chat completion if `ENABLE_REMOTE_LLM=true` and `OPENAI_API_KEY` set. Requires provider access, budget and documented data handling.

**Intended use:** educational demo QA for six fictional customer policies. **Not for:** real merchant support, legal advice, financial decisions, live refund authorization, medical or emergency assistance.

**Known risks:** lexical query mismatch, ambiguous terms, duplicate chunks, unsupported facts that overlap by token, prompt injection, invalid citations, API outages and language mismatch. If no sufficiently matched answer is found, a human support fallback appears.

**Evaluation:** fixture-based top-3 source retrieval and manual checks only; no external benchmark verified. See EVALUATION.md.
