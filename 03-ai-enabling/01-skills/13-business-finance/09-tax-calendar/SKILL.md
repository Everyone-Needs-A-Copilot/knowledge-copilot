---
last_updated: 2026-02-25
status: active
name: tax-calendar
description: Manage tax deadlines, estimated payment dates, and filing requirements with proactive reminders. Use when planning tax-related actions, setting up reminders, or checking upcoming obligations.
triggers:
  files: ["**/finance/**", "**/tax/**", "**/calendar/**"]
  keywords: ["tax calendar", "deadlines", "estimated payments", "filing dates", "extensions", "reminders", "quarterly"]
allowed-tools: Read, Write, Edit
---

# Tax Calendar

Missing a tax deadline is one of the most expensive administrative failures. Late filing penalties, late payment penalties, and underpayment interest compound quickly and are entirely avoidable. The IRS and state agencies do not send advance reminders for estimated payments. The burden is on you to know the dates, prepare in advance, and act on time.

A tax calendar is not just a list of due dates -- it is a preparation timeline. Each deadline has a preparation window: the work that must happen before the deadline to ensure timely, accurate compliance. A payment due on April 15 requires income aggregation, deduction calculation, and payment scheduling well before that date. This skill provides both the deadlines and the preparation cadence to ensure nothing is missed.

---

## Framework

### Annual Federal Tax Calendar

**Q1: January - March**

| Date | Obligation | Who | Preparation Window |
|------|-----------|-----|--------------------|
| Jan 15 | Q4 estimated tax payment due | Self-employed, investors | Calculate by Jan 1 |
| Jan 31 | W-2s due to employees | Employers | Prepare by Jan 15 |
| Jan 31 | 1099-NEC due to contractors and IRS | Businesses paying contractors | Gather data by Jan 15 |
| Jan 31 | 1099-MISC due (certain types) | Businesses | Gather data by Jan 15 |
| Feb 15 | 1099-INT, 1099-DIV, 1099-B due to recipients | Financial institutions | Usually auto-generated |
| Mar 15 | S-corp (1120-S) and Partnership (1065) returns due | S-corps, partnerships | Begin preparation Feb 1 |
| Mar 15 | S-corp/Partnership extension (Form 7004) due if extending | S-corps, partnerships | Decide by Mar 1 |

**Q2: April - June**

| Date | Obligation | Who | Preparation Window |
|------|-----------|-----|--------------------|
| Apr 15 | Individual return (1040) due | All individuals | Begin preparation Mar 1 |
| Apr 15 | Q1 estimated tax payment due | Self-employed, investors | Calculate by Apr 1 |
| Apr 15 | Individual extension (Form 4868) due if extending | Individuals needing more time | Decide by Apr 1 |
| Apr 15 | IRA and HSA contribution deadline for prior year | Account holders | Fund by Apr 14 |
| Apr 15 | C-corp return (1120) due | C-corporations | Begin preparation Feb 15 |
| Jun 15 | Q2 estimated tax payment due | Self-employed, investors | Calculate by Jun 1 |

**Q3: July - September**

| Date | Obligation | Who | Preparation Window |
|------|-----------|-----|--------------------|
| Sep 15 | Q3 estimated tax payment due | Self-employed, investors | Calculate by Sep 1 |
| Sep 15 | Extended S-corp/Partnership returns due | Extended S-corps, partnerships | Finalize by Sep 1 |

**Q4: October - December**

| Date | Obligation | Who | Preparation Window |
|------|-----------|-----|--------------------|
| Oct 15 | Extended individual returns (1040) due | Individuals who filed extension | Finalize by Oct 1 |
| Oct 15 | Extended C-corp returns due | C-corps who filed extension | Finalize by Oct 1 |
| Dec 31 | Solo 401(k) employee contribution deadline | Solo 401(k) participants | Verify by Dec 15 |
| Dec 31 | Roth conversion deadline | Anyone converting | Execute by Dec 30 |
| Dec 31 | Charitable contribution deadline | Itemizers | Complete by Dec 30 |
| Dec 31 | Required Minimum Distribution (RMD) deadline | Account holders 73+ | Calculate by Dec 1 |

### State Tax Calendar Considerations

| Factor | Impact | Action |
|--------|--------|--------|
| State income tax filing deadline | Most align with federal; some differ (e.g., some states have different dates) | Verify your state's specific dates |
| State estimated payment schedule | Most align with federal; some have different schedules | Verify your state's specific schedule |
| State extension rules | Some auto-extend with federal; some require separate extension | Check if state requires its own extension filing |
| Multi-state filing | Each state has its own deadlines | Track all applicable state deadlines separately |
| State-specific obligations | Local taxes, city taxes, franchise taxes | Identify all state/local obligations |

### Extension Management

**What an extension does and does not do:**

| Extension Provides | Extension Does NOT Provide |
|-------------------|---------------------------|
| Additional time to file the return | Additional time to pay the tax |
| Protection from late-filing penalty | Protection from late-payment penalty |
| Up to 6 months additional time | Any change to estimated payment schedule |

**Extension Decision Matrix:**

| Situation | Extension? | Required Action |
|-----------|-----------|----------------|
| Missing documents (K-1, corrected 1099) | Yes | File extension, pay estimated tax due |
| Complex situation needs more time | Yes | File extension, pay estimated tax due |
| Owe money but cannot pay | File on time anyway | File return, set up payment plan |
| Expecting a refund | Optional (no penalty for late refund claims) | File when ready, within 3 years |
| Need to fund IRA/HSA for prior year | Does not help (deadline is Apr 15 regardless) | Fund accounts by Apr 15 |

**Extension Payment Estimate:**

When filing an extension, you must still estimate and pay taxes owed by the original deadline.

```
Estimated tax due with extension =
  Projected total tax liability
  - Withholding (W-2, backup)
  - Estimated payments already made
  - Credits
  = Amount to pay with extension
```

### Document Gathering Timeline

**By January 31:**
- [ ] Prior year return (for reference and safe harbor calculation)
- [ ] W-2 forms from all employers
- [ ] Final pay stubs (verify against W-2)

**By February 28:**
- [ ] 1099-NEC (contractor income)
- [ ] 1099-MISC (other income)
- [ ] 1099-INT (interest income)
- [ ] 1099-DIV (dividend income)
- [ ] 1099-B (brokerage/investment sales)
- [ ] 1099-R (retirement distributions)
- [ ] 1099-G (government payments, state refund)
- [ ] 1099-SA (HSA distributions)
- [ ] 1098 (mortgage interest)
- [ ] 1098-T (tuition)
- [ ] 1098-E (student loan interest)
- [ ] K-1 forms (partnership/S-corp/trust income)

**By March 15:**
- [ ] Charitable contribution receipts and acknowledgment letters
- [ ] Medical expense records (if itemizing)
- [ ] Business expense records and receipts
- [ ] Home office measurements and expense records
- [ ] Vehicle mileage log
- [ ] Estimated payment records (federal and state)
- [ ] HSA contribution records (Form 5498-SA)
- [ ] IRA contribution records (Form 5498)
- [ ] Property tax records
- [ ] Childcare expense records (if claiming credit)

**Note:** K-1 forms are frequently late. If expected K-1 has not arrived by March 15, plan to file an extension.

### Reminder Cadence System

| Days Before Deadline | Reminder Type | Action |
|---------------------|---------------|--------|
| 30 days | Early warning | Begin preparation, gather documents |
| 14 days | Preparation checkpoint | All documents gathered, calculations started |
| 7 days | Action deadline | Finalize calculations, prepare payment |
| 3 days | Final reminder | Submit payment, file return/extension |
| Day of | Confirmation | Verify submission received, save confirmation |

### Penalty Reference

| Penalty Type | Rate | Applies When |
|-------------|------|-------------|
| Failure to file | 5% of unpaid tax per month, max 25% | Return not filed by deadline (including extension) |
| Failure to pay | 0.5% of unpaid tax per month, max 25% | Tax not paid by original deadline |
| Underpayment of estimated tax | IRS interest rate (changes quarterly) | Did not meet safe harbor and owed > $1,000 |
| Combined maximum | 47.5% of unpaid tax (25% file + 22.5% pay) | Both file and pay penalties applied |
| Minimum late-filing penalty | Lesser of $510 or 100% of tax due | Return filed > 60 days late |

**Penalty avoidance priority:**
1. Always file on time (or file extension) -- filing penalty is 10x payment penalty
2. Pay as much as possible by original deadline
3. Meet safe harbor for estimated payments
4. If you cannot pay, file anyway and request a payment plan

---


## Define Done

- [ ] Financial data gathered and categorized accurately
- [ ] Analysis based on actual numbers, not estimates
- [ ] Recommendations account for tax implications and time horizon
- [ ] Action steps are specific and prioritized

## Application

### Setting Up Your Tax Calendar

**Step 1: Identify all applicable obligations**

| Obligation | Applies to Me? | Deadline |
|-----------|----------------|----------|
| Individual return (1040) | Yes (everyone) | Apr 15 |
| Estimated payments (federal) | If self-employed or investment income | Apr 15, Jun 15, Sep 15, Jan 15 |
| Estimated payments (state) | Check state requirements | Varies |
| S-corp return (1120-S) | If S-corp owner | Mar 15 |
| 1099-NEC issuance | If paying contractors > $600 | Jan 31 |
| State returns | Check all applicable states | Varies |
| Local/city returns | Check local requirements | Varies |
| Retirement contribution deadlines | If applicable | Varies by account type |

**Step 2: Set up reminders for each obligation**

For each deadline, create reminders at 30, 14, 7, and 3 days before.

**Step 3: Block preparation time**

For each deadline, block calendar time in the preparation window (typically 2-4 weeks before the deadline).

### Quarterly Payment Tracking Sheet

| Payment | Due Date | Amount Due | Date Paid | Confirmation # | Method |
|---------|----------|-----------|-----------|----------------|--------|
| Federal Q1 | Apr 15 | $X | | | EFTPS / Direct Pay |
| Federal Q2 | Jun 15 | $X | | | EFTPS / Direct Pay |
| Federal Q3 | Sep 15 | $X | | | EFTPS / Direct Pay |
| Federal Q4 | Jan 15 | $X | | | EFTPS / Direct Pay |
| State Q1 | [date] | $X | | | [state system] |
| State Q2 | [date] | $X | | | [state system] |
| State Q3 | [date] | $X | | | [state system] |
| State Q4 | [date] | $X | | | [state system] |

### Weekend/Holiday Adjustment Rule

When a tax deadline falls on a weekend or federal holiday, the deadline moves to the next business day. Always verify the actual due date for the current year, as it shifts annually.

| Standard Date | If Falls On | Moves To |
|--------------|-------------|----------|
| Apr 15 | Saturday | Monday Apr 17 |
| Apr 15 | Sunday | Monday Apr 16 |
| Apr 15 | Emancipation Day (DC holiday) | Next business day |
| Jun 15 | Weekend | Next Monday |
| Sep 15 | Weekend | Next Monday |
| Jan 15 | Weekend or MLK Day | Next business day |

---

## Quick Reference

### Critical Dates at a Glance

| Date | What is Due |
|------|-----------|
| Jan 15 | Q4 estimated payment |
| Jan 31 | W-2s and 1099-NECs |
| Mar 15 | S-corp and partnership returns (or extension) |
| Apr 15 | Individual return (or extension), Q1 estimated payment, IRA/HSA funding deadline |
| Jun 15 | Q2 estimated payment |
| Sep 15 | Q3 estimated payment, extended S-corp/partnership returns |
| Oct 15 | Extended individual returns |
| Dec 31 | 401(k) employee contributions, Roth conversions, charitable donations, RMDs |

### If You Miss a Deadline

| Missed | Immediate Action |
|--------|-----------------|
| Estimated payment | Pay immediately -- interest accrues daily, pay ASAP to minimize |
| Filing deadline | File as soon as possible -- penalty is per-month, partial months count |
| Extension deadline | File the return immediately -- you are now in late-filing penalty territory |
| 1099 issuance | File immediately -- penalty increases with lateness |
| Retirement contribution | Generally cannot be made up (except employer contributions with extension) |

### Monthly Tax Calendar Maintenance

- [ ] First of each month: review upcoming deadlines in next 30-60 days
- [ ] Verify no deadline adjustments for weekends/holidays
- [ ] Confirm documents needed are on track
- [ ] Check estimated payment tracking sheet is current
- [ ] Note any income changes that affect estimated payment calculations

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Approach |
|-------------|-------------|-----------------|
| Relying on memory for tax deadlines | One forgotten date = penalties that exceed the cost of any calendar system | Set up systematic reminders at 30/14/7/3 days |
| Filing extension without paying estimated tax | Extension avoids filing penalty but not payment penalty | Always estimate and pay with extension |
| Waiting for K-1 forms and missing the deadline | K-1s are frequently late; meanwhile your filing deadline passes | File extension proactively if K-1 dependent |
| Not adjusting for weekends and holidays | Submitting on the "standard" date that is actually past the shifted deadline | Verify actual due dates each year |
| Making estimated payments on the due date | Payment processing takes time; electronic may be same-day but check can take days | Submit 3-5 days before due date |
| Ignoring state deadlines | State penalties are separate from and additional to federal | Track state deadlines alongside federal |
| Not keeping payment confirmations | Cannot prove timely payment if records are lost | Save confirmation numbers and screenshots |
| Treating the extension deadline as optional | After the extension deadline, penalties compound rapidly | The extended deadline is a hard deadline, not a suggestion |
| Planning to "catch up" in Q4 | Estimated payment penalties are calculated per quarter, not annually | Pay each quarter's obligation on time |


## Quality Tests

### Accuracy Test
- All calculations are correct and assumptions are stated
- **PASS:** Numbers are verifiable and assumptions clearly documented
- **FAIL:** Rough estimates presented as precise figures

### Completeness Test
- Analysis considers tax implications and opportunity costs
- **PASS:** Tax impact calculated for each recommendation
- **FAIL:** Pre-tax returns presented without noting tax drag

