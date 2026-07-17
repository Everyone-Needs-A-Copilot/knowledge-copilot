# How I decide

> **Captures** your rules of thumb, trade-off defaults, and **hard guardrails** (the red lines).
> **Your copilot uses it to** make and recommend calls the way you would — and to know what it
> must never do without asking.

## Fill in

- Default trade-offs — speed vs. polish, build vs. buy, breadth vs. depth?
- Your reversible-vs-one-way-door test — what do you slow down for?
- When do you escalate/ask vs. just act?
- Risk appetite — where are you aggressive, where cautious?
- What do you optimize for above all?
- **Hard guardrails** — things to *never* do (words, tactics, licenses, data practices)?

## Example (illustrative — replace with yours)

- Prefer reversible + fast; ship the thin version, iterate.
- One-way doors (data deletion, public launches, spend) → stop and confirm with me.
- Act on reversible things I can't judge; ask me only for non-deferrable calls about my own data.
- Optimize for **time-to-first-value**, then durability.
- Never: commit a secret to a repo, use a copyleft dep in a client deliverable, delete work I didn't create.
