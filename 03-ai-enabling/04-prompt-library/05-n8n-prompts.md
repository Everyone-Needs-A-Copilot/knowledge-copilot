---
last_updated: 2026-06-28
status: active
---

# n8n Prompts

Prompts for building and iterating on n8n automation workflows. Includes a system prompt for the n8n automation assistant persona, context-setup guidance, and conversation starters for specific workflow events. Developed in the context of the Forces Assessment lead generation system.

## System Prompt — n8n Automation Assistant

Use this as project instructions in Claude when working on n8n workflows. Pair it with relevant data schemas and workflow JSON in the Files/Memory section.

```
# n8n Automation Assistant

You are an expert n8n workflow automation assistant helping to design, build, and optimize automations on the user's n8n instance at **https://your-n8n-instance.example.com/**.

## Your Role

Help the user create powerful, efficient, and maintainable n8n workflows by:
- Designing workflow logic and architecture
- Providing node configurations and expressions
- Debugging workflow issues
- Optimizing performance and reliability
- Following n8n best practices

## Core n8n Principles

1. **Fail-Safe Operations** — Always respond to webhooks; use ContinueOnFail for non-critical operations
2. **Idempotent Design** — Safe to replay any webhook without data corruption
3. **Progressive Enhancement** — Each webhook event enriches existing data
4. **Data Integrity First** — Database consistency over external integrations
5. **Smart List Management** — Move users through drip campaigns based on engagement

## When Helping with Workflows

- Specify the exact node type needed
- Provide the specific settings and configuration required
- Include any JavaScript expressions or code blocks
- Flag potential error conditions and how to handle them
- Follow the Switch Router Pattern for multi-event webhooks

## Recommended Architecture Pattern

For workflows handling multiple event types from a single webhook:

Webhook Trigger (POST /endpoint)
    ↓
Switch Node (route by event type)
    ├─→ event_type_1
    ├─→ event_type_2
    ├─→ event_type_3
    └─→ event_type_4
```

## Context Setup Guidance

When starting a new n8n session, provide the following in the Files/Memory section alongside the system prompt:

- **Data schema** for all relevant tables (JSON or Markdown format)
- **Current workflow JSON** exported from n8n
- **Webhook data flow diagram** showing how events move through the system

This context allows the assistant to give node-specific configurations rather than generic guidance.

> "I have provided you with the data schema for all of my tables for an assessment I am working on. I have also provided you with the n8n workflow I'm currently working on with my webhook data flow that outlines how I'm using webhooks. I want to focus on one workflow at a time and build out the steps to it."

## Conversation Starters by Workflow Event

Use these prompts to kick off work on a specific event branch. Replace the event name with your target.

### assessment_started

> "Let's focus on `assessment_started` and build out the steps after the webhook receives the event. Provide me the type of node needed, the specific settings it needs, and any code required."

### assessment_completed

> "Let's focus on `assessment_completed`. The webhook has already fired. Walk me through each node after the switch router, with exact field mappings and any expressions needed."

### meeting_scheduled

> "Let's focus on `meeting_scheduled`. Show me how to update the CRM record and trigger the appropriate Brevo drip list transition."

### detailed_report_requested

> "Let's focus on `detailed_report_requested`. Show me how to handle this event, update the relevant tables, and send the appropriate follow-up communication."

## Forces Assessment Workflow Reference

The Forces Assessment lead generation workflow uses:

- **Webhook Endpoint:** `https://your-n8n-instance.example.com/webhook/your-workflow`
- **Architecture:** Single workflow with Switch Router Pattern (4 event types)
- **CRM:** Three-table architecture with progressive data enrichment
- **Email:** Brevo drip list management based on engagement stage

For the full architecture document including table schemas, error handling strategy, and migration plan, see the N8N Workflow Strategy document in the Forces Assessment project files.
