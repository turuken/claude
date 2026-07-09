# Sub-Agents and the Agent Tool

This document explains, for someone new to the idea, how Claude Code's
sub-agent feature (the `Agent` tool) works and when to reach for it.

## What is a sub-agent?

A sub-agent is a separately-invoked instance of Claude, spun up to handle one
self-contained task on the calling agent's behalf. The caller sends it a
prompt describing the job; the sub-agent runs on its own — reading files,
searching, calling tools, iterating — and when it's done, it reports back
a single result message to the caller.

The key property is isolation: everything the sub-agent does along the way
(every file it opens, every grep it runs, every dead end it explores) stays
inside the sub-agent's own context. Only its final summary crosses back into
the parent conversation. The parent's context window never sees the
intermediate noise.

## Why use them

Two main reasons:

1. **Parallelism.** If you have several independent chunks of work — e.g.
   researching three unrelated parts of a codebase, or producing several
   unrelated artifacts — you can dispatch multiple sub-agents in a single
   turn and let them run concurrently, rather than doing each one serially
   yourself.
2. **Context protection.** Exploratory work (grepping around a large repo,
   reading many files to answer one question) can generate a lot of output.
   Doing that directly in the main conversation bloats its context window
   with material that's only useful transiently. Delegating it to a
   sub-agent means the parent only pays for the final answer, not the
   search process that produced it.

## When *not* to use them

Sub-agents aren't free — spinning one up costs latency and a "cold start"
(it has no memory of the conversation so far). Skip them when:

- The task is a simple, targeted lookup — reading one known file, or a
  single grep/glob for a specific symbol. Just call `Read`, `Grep`, or
  `Glob` directly; it's faster and cheaper than delegating.
- The task requires genuine back-and-forth with the conversation's
  accumulated context — a sub-agent starts cold and only knows what you put
  in its prompt, so tasks that depend on subtle prior discussion don't fit.

## Agent types

Not all sub-agents are identical. Different agent "types" exist, each with
its own tool access and specialization — for example, a read-only "Explore"
type that can only search and read files (fast, safe for pure research), or
a general-purpose type with full tool access (able to write and edit files,
run commands, etc.). The caller picks the type that matches the task, so a
simple research question doesn't get more capability (or risk) than it
needs.

## Foreground vs. background

A sub-agent can run in the **foreground**, where the caller blocks and waits
for its result before continuing — appropriate when you need that result to
decide your next step. Or it can run in the **background**, where the
caller keeps working on other things and is notified when the sub-agent
finishes — appropriate for independent work that doesn't gate anything else
happening right now.

## Writing a good sub-agent prompt

Because a sub-agent starts with no memory of the calling conversation, its
prompt has to be self-contained: state the goal, the relevant background,
any file paths already known, and a clear description of what the
deliverable should look like. A vague instruction like "look into the bug"
produces a shallow result; a prompt with concrete context and an explicit
ask produces a useful one.

## This file is an example

This very file — along with its siblings `README.md` and `word_count.py` in
this same repository — was produced by exactly the pattern described above:
one parent turn dispatched three sub-agents in parallel, each one given a
self-contained prompt describing a single artifact to produce, and each
worked independently before reporting back a finished result for the parent
to commit.
