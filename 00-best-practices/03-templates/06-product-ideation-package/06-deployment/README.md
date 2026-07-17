---
last_updated: 2026-06-27
status: active
---

# Deployment Guide

> **Status:** STUB — filled before Gate G9 (release candidate approved).
>
> This document covers environments, CI/CD pipeline, deploy process,
> and rollback procedures for {{PRODUCT_NAME}}.

---

## When this gets filled

Gate G9 is the release candidate gate. Deployment documentation must be complete
and verified before that gate passes. It should be drafted during the engineering
phase (post-G8) and confirmed working by QA before G9.

## What this will cover

- Environment overview (local, staging, production — URLs, purposes, access)
- Environment variables required per environment
- CI/CD pipeline (what triggers a build, what gates must pass, how to monitor)
- Manual deploy steps (for cases where automation is not available)
- Database migrations: how they run, how to verify, how to roll back
- Rollback procedure: how to revert a bad release
- Post-deploy verification checklist

---

*Do not fill this stub until the CI/CD pipeline is configured and at least one
successful deploy to staging has been completed.*
