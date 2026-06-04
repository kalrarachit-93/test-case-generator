"""
Tools for the test case generator agent.

The agent uses these to structure its reasoning:
- extract_criteria: forces it to identify each AC explicitly
- validate_coverage: forces it to check its own work against the criteria

These are intentionally simple. The 'intelligence' lives in Claude; the tools
provide structure so Claude reasons about each criterion separately rather
than blurring them together.
"""

import re


# ============================================================
# Tool 1: extract_criteria
# ============================================================

def extract_criteria(ticket_text: str) -> list[str]:
    """
    Pulls each acceptance criterion out of a Jira-style ticket.
    Returns a list of strings, one per criterion.

    Looks for a line containing 'ACCEPTANCE CRITERIA' and then collects
    each bullet item (line starting with '-') until the next section
    (PRIORITY, COMPONENT, etc.) or end of text.
    """
    # Find the start of the AC section
    upper = ticket_text.upper()
    start_idx = upper.find("ACCEPTANCE CRITERIA")
    if start_idx == -1:
        return []

    # Look for the next section header to know where AC ends
    # Section headers we expect after AC: PRIORITY, COMPONENT, REPORTER, ASSIGNEE
    section_endings = ["PRIORITY:", "COMPONENT:", "REPORTER:", "ASSIGNEE:", "STATUS:"]
    end_idx = len(ticket_text)
    for marker in section_endings:
        idx = upper.find(marker, start_idx)
        if idx != -1 and idx < end_idx:
            end_idx = idx

    ac_block = ticket_text[start_idx:end_idx]

    # Each criterion starts with "- " at the beginning of a line.
    # Some criteria span multiple lines, so we split smartly.
    criteria = []
    current = []
    for line in ac_block.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            # New criterion - save the previous one if any
            if current:
                criteria.append(" ".join(current).strip())
                current = []
            current.append(stripped[2:])  # remove the "- " prefix
        elif stripped and current:
            # Continuation of current criterion
            current.append(stripped)

    # Don't forget the last one
    if current:
        criteria.append(" ".join(current).strip())

    return criteria


# ============================================================
# Tool 2: validate_coverage
# ============================================================

def validate_coverage(criteria: list[str], test_case_titles: list[str]) -> dict:
    """
    Checks whether each acceptance criterion appears to be covered by at
    least one test case.

    This is a simple keyword-overlap check. It's intentionally imperfect:
    the agent's job is to interpret the result and decide whether to fix gaps.

    Returns a dict with:
    - covered: list of criteria that have likely coverage
    - missing: list of criteria with no apparent coverage
    - coverage_rate: percentage of criteria covered
    """
    covered = []
    missing = []

    for criterion in criteria:
        # Pull out the meaningful keywords from the criterion
        # (skip generic words like 'given', 'when', 'then', 'the', etc.)
        skip_words = {
            "given", "when", "then", "the", "a", "an", "and", "or", "but",
            "is", "are", "be", "they", "their", "is", "on", "to", "in", "of",
            "for", "with", "user", "users", "see", "do", "does", "must",
            "should", "can", "will", "have", "has", "this", "that",
        }
        words = re.findall(r"\b\w+\b", criterion.lower())
        keywords = [w for w in words if w not in skip_words and len(w) > 3]

        # A criterion is "covered" if at least 2 of its keywords appear
        # in any test case title.
        all_titles_lower = " ".join(t.lower() for t in test_case_titles)
        matches = sum(1 for kw in keywords if kw in all_titles_lower)

        if matches >= 2:
            covered.append(criterion)
        else:
            missing.append(criterion)

    coverage_rate = (
        round(len(covered) / len(criteria) * 100, 1) if criteria else 0
    )

    return {
        "covered": covered,
        "missing": missing,
        "coverage_rate": coverage_rate,
        "total_criteria": len(criteria),
        "covered_count": len(covered),
        "missing_count": len(missing),
    }


# ============================================================
# Tool schemas (what Claude sees)
# ============================================================

TOOL_SCHEMAS = [
    {
        "name": "extract_criteria",
        "description": (
            "Parses a Jira-style ticket and extracts each acceptance criterion "
            "as a separate item. Always call this FIRST to understand what needs "
            "to be tested. Returns a list of criterion strings."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "ticket_text": {
                    "type": "string",
                    "description": "The full text of the Jira-style ticket."
                }
            },
            "required": ["ticket_text"]
        }
    },
    {
        "name": "validate_coverage",
        "description": (
            "Checks whether the generated test case titles cover each "
            "acceptance criterion. Call this AFTER generating test cases to "
            "verify no criterion is missed. If coverage_rate is below 100%, "
            "generate additional test cases for the 'missing' criteria."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "criteria": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The list of acceptance criteria (from extract_criteria)."
                },
                "test_case_titles": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "The titles of the test cases generated so far."
                }
            },
            "required": ["criteria", "test_case_titles"]
        }
    }
]


# ============================================================
# Tool executor
# ============================================================

def execute_tool(tool_name: str, tool_input: dict):
    """Routes a tool call to the right Python function and returns the result."""
    if tool_name == "extract_criteria":
        return extract_criteria(tool_input["ticket_text"])
    elif tool_name == "validate_coverage":
        return validate_coverage(
            tool_input["criteria"],
            tool_input["test_case_titles"]
        )
    return f"Unknown tool: {tool_name}"