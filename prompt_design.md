# Prompt Design Documentation

## Overview

This project implements a multi-stage AI-powered customer support workflow for Bloom Aesthetics Clinic using an OpenAI-compatible LLM architecture.

The workflow includes:
1. FAQ Answering
2. Lead Qualification
3. Escalation Detection
4. Conversation Summary Generation

The prompts were designed to prioritize:
- SOP grounding
- hallucination prevention
- safe escalation
- structured outputs
- conversational reliability

---

# System Prompt Design

The FAQ agent system prompt was designed to ensure the AI answers ONLY from the provided SOP information.

Key instructions included:
- never hallucinate information
- never assume unsupported details
- refuse unsupported questions safely
- return structured JSON outputs

Core instruction:

```text
ONLY use information explicitly available in the SOP.
````

This reduces the likelihood of fabricated services, pricing, or medical advice.

The model is also instructed to:

* escalate unsupported queries
* maintain professional SMB-friendly tone
* support semantic understanding of customer wording

---

# Hallucination Prevention

Hallucination prevention was treated as a primary requirement.

The workflow prevents hallucinations through:

1. SOP-grounded prompting
2. explicit refusal instructions
3. confidence-based escalation
4. structured JSON outputs

If information is unavailable in the SOP:

* the AI clearly states the limitation
* avoids generating fake details
* recommends escalation when appropriate

Example:

```text
I do not have information about hair transplant surgery in the SOP.
```


# Confidence-Based Escalation

The FAQ workflow returns structured confidence scores:

```json id="y1p8m4"
{
  "confidence": 0.95
}
```

If confidence falls below a threshold:

* escalation is triggered
* the response is treated as unreliable
* unsupported requests are safely handled

This prevents low-confidence hallucinated answers.

# Escalation Logic

The escalation system uses a hybrid approach:

* rule-based escalation
* LLM-based sentiment detection

Rule-based escalation handles:

* complaints
* frustration
* medical questions
* pricing negotiation
* explicit human requests

Example escalation triggers:

* "I’m very frustrated"
* "Are Botox side effects dangerous?"
* "I want to speak to a human"

Escalation events are logged with reasons for observability and debugging.

# Lead Qualification Workflow

The qualification workflow collects:

* business type
* team size
* current customer support tools

Qualification was separated into its own workflow stage to prevent qualification answers from being incorrectly interpreted as FAQ queries.

A shared conversation state object manages:

* workflow stage
* escalation state
* lead data
* SOP gaps
* conversation history

# Tone and Persona

The assistant was designed for SMB customer-support use cases.

Target tone:

* professional
* concise
* polite
* operationally clear

The AI avoids:

* excessive verbosity
* aggressive sales language
* unsupported medical guidance

# Architectural Tradeoffs

## Why Modular Agents?

The system was separated into:

* FAQ agent
* escalation agent
* qualification agent
* summary agent

This improves:

* maintainability
* debugging
* workflow orchestration


## Why No Vector Database / RAG?

The SOP dataset is intentionally small and deterministic.

Using embeddings or vector databases would add unnecessary complexity for this assignment scope.

Direct SOP grounding was therefore selected as the simpler and more reliable approach.



# Reliability and Safety

The workflow includes:

* hallucination prevention
* escalation handling
* low-confidence routing
* graceful failure behavior
* structured outputs

These behaviors were prioritized to create safer SMB customer interactions.

# UI and Workflow Visualization

A lightweight Streamlit dashboard was added to improve workflow observability and demonstrate orchestration behavior visually.

The dashboard displays:
- live workflow stages
- escalation state
- qualification data
- SOP gaps
- structured summaries

The UI layer was intentionally kept lightweight to focus development effort on orchestration logic and AI workflow reliability rather than frontend complexity.

# Known Limitations

Current limitations:

* no persistent database
* no CRM integration
* no long-term memory across sessions

These tradeoffs were intentionally accepted to focus on workflow orchestration and AI reliability.



