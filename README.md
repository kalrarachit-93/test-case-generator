\# Test Case Generator Agent



An AI agent that reads a Jira-style ticket and generates a structured list of test cases — positive and negative — for a manual QA engineer to execute. Built with Anthropic's Claude API.



Built as a second portfolio project after \[ai-agent-eval-framework](https://github.com/kalrarachit-93/ai-agent-eval-framework), part of a transition from 8 years in manual QA into AI engineering.



\## Why this project



Manual QA engineers spend hours doing exactly this work: reading a ticket, breaking down acceptance criteria, identifying positive and negative scenarios, formatting test cases for a test management tool. An agent that produces a first draft saves real time and surfaces edge cases a junior tester might miss.



This is also a deliberate exercise in \*\*domain-anchored AI\*\* — building agents that solve problems the developer actually understands deeply.



\## What it does



Given a structured ticket (title, description, acceptance criteria, priority, component), the agent:



1\. Parses each acceptance criterion as a separate item

2\. Generates positive test cases (happy paths) and negative test cases (invalid inputs, error states, security boundaries)

3\. Validates that every criterion has at least one matching test case

4\. If gaps are found, generates additional test cases for the missing criteria

5\. Returns a clean numbered list with title, steps, and expected result for each test case



\## The agent architecture



The interesting part of this project is \*how\* it's an agent rather than a single prompt. The agent uses two tools that structure its reasoning:



| Tool | What it does | Why it matters |

|------|--------------|----------------|

| `extract\_criteria` | Parses the ticket and returns each acceptance criterion as a separate string | Forces the agent to reason about each AC independently, not blur them together |

| `validate\_coverage` | Checks the generated test case titles against the criteria using keyword overlap | Lets the agent verify its own work and fix gaps. Intentionally imperfect — gives the agent a \*signal\*, not a verdict |



A typical run takes 3 iterations: extract → draft + validate → finalize.



\## Sample output (excerpt)



For the password-reset ticket, the agent generates tests like:



Note the inclusion of "comparable response time" — that's the agent catching a real timing-based enumeration attack vector that's not in the literal acceptance criteria. Generated test cases consistently include this kind of inferred edge case.



\## Setup



```bash

git clone https://github.com/kalrarachit-93/test-case-generator

cd test-case-generator

python -m venv .venv

.venv\\Scripts\\activate          # Windows

source .venv/bin/activate       # macOS/Linux

pip install -r requirements.txt

echo "ANTHROPIC\_API\_KEY=sk-ant-..." > .env

```



\## Usage



Two sample tickets are included. Pick one:



```bash

python agent.py 1   # Password reset feature

python agent.py 2   # Shopping cart feature

```



Each run prints the agent's reasoning steps, then displays the final test cases. Output is also saved to `test\_cases\_ticket\_<n>.md`.



\## Design choices worth noting



\*\*Why a system prompt instead of putting all instructions in the user message?\*\* System prompts tend to give more consistent behavior across runs. The agent's identity ("you are a senior QA engineer") and process ("extract first, then generate, then validate") belong in the system layer.



\*\*Why `validate\_coverage` uses keyword matching and not another LLM call.\*\* Tools should be fast, deterministic, and cheap. A perfect coverage check would itself need an LLM, doubling the cost per iteration. The keyword heuristic gives Claude a useful signal at zero cost. Claude then interprets the signal and decides how to act.



\*\*Why deliberately limit to positive and negative.\*\* Initial scope. Edge cases, security, performance, and accessibility test categories are listed as future work — easier to add cleanly once the foundation is solid.



\## What I'd build next



\- Edge case and security test categories (parametrize the test category list)

\- Support for direct Jira API integration instead of pasted text

\- Add evaluation: use the \[eval framework](https://github.com/kalrarachit-93/ai-agent-eval-framework) from project 1 to test this agent — does the generator produce test cases that cover every AC, on every ticket?

\- Multi-ticket batch processing for sprint planning workflows

\- Configurable test case format (Gherkin / Robot Framework / table format)



\## About me



Rachit Kalra — 8 years in manual QA, transitioning into AI engineering. Particularly interested in AI evaluation, agent reliability, and the intersection of testing rigor with non-deterministic systems.



\- GitHub: \[kalrarachit-93](https://github.com/kalrarachit-93)

\- LinkedIn: https://www.linkedin.com/in/rachit-kalra-softwaretestingengineer/

\- Email: rachitkalra93@yahoo.com

\- Related: \[ai-agent-eval-framework](https://github.com/kalrarachit-93/ai-agent-eval-framework) — my first AI project, building the evaluation patterns this project's outputs would be tested against

