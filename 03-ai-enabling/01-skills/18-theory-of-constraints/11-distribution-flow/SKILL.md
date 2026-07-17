---
last_updated: 2026-04-02
status: active
name: distribution-flow
description: Optimize distribution and replenishment using TOC pull-based methodology. Use when managing inventory, planning replenishment, sizing buffers for distribution, or optimizing any supply-demand matching process. Triggers on inventory management, replenishment, buffer sizing, supply chain, and demand management.
allowed-tools: Bash(python3:*) Read Write
---

# Distribution Flow: TOC Pull-Based Replenishment

TOC distribution replaces forecast-driven push replenishment with consumption-driven pull replenishment. The core insight: you can never forecast demand perfectly, but you can always measure what was consumed. Replenish what was consumed, when it was consumed, in the quantity consumed. This keeps buffers healthy while minimizing excess inventory.

## Why Forecast-Driven Distribution Fails

Traditional distribution uses demand forecasts to decide how much to stock and when. This creates three systematic problems:

**Local optimization creates global waste.** Each distribution point over-orders to protect against stockouts. The result: excess inventory across the network, while stockouts still occur because the excess is in the wrong places.

**Forecast error compounds upstream.** Small errors at retail compound into massive swings at distribution centers (the Bullwhip Effect). The further upstream you go, the worse the variability — even when end demand is stable.

**Safety stock is static while demand is dynamic.** Fixed reorder points and safety stock levels are calculated once and rarely revisited. Demand patterns change. The static buffer becomes miscalibrated without anyone noticing until a stockout or an excess write-off.

---

## The TOC Solution: Pull-Based Replenishment

**The rule:** Replenish what was consumed. Do not replenish based on what you forecast will be consumed.

**How it works:**
1. Each location holds a buffer — a target stock level sized for variability and lead time.
2. When consumption occurs, a replenishment signal is sent for the quantity consumed.
3. The replenishment arrives and restores the buffer.
4. The buffer size itself is adjusted dynamically based on actual consumption patterns.

The buffer is not a forecast. It is a shock absorber. It handles variability without requiring accurate prediction.

---

## Buffer Zones

Every buffer has three zones based on what fraction remains:

| Zone | Remaining | Signal |
|------|-----------|--------|
| **Green** | >66% | Adequate. No action. |
| **Yellow** | 33-66% | Monitor. Replenishment may be needed soon. |
| **Red** | <33% | Replenish now. Buffer is at risk. |

The zones give operational visibility without requiring anyone to recalculate optimal order quantities. "What zone is this item in?" is answerable at a glance.

---

## Replenishment Signals

Four signal types based on buffer health and consumption rate:

| Signal | Condition | Action |
|--------|-----------|--------|
| **Urgent** | Red zone AND <3 days supply | Expedite replenishment immediately |
| **Replenish** | Yellow zone | Place standard replenishment order |
| **Hold** | Green zone | No action needed |
| **Reduce** | >150% of buffer target | Buffer is oversized; absorb before reordering |

Sorting by urgency (urgent → replenish → hold → reduce) gives a daily action list that prioritizes attention correctly.

---

## Dynamic Buffer Management (DBM)

Buffers are not set-and-forget. DBM adjusts buffer sizes based on actual consumption:

**Increase the buffer when:** Items frequently penetrate deep into red zone before replenishment arrives. Demand is higher than the buffer was sized for.

**Decrease the buffer when:** Items stay in green zone for extended periods. Replenishments arrive faster than consumption; the buffer is over-sized.

**Rule of thumb:** If an item hits red more than 20% of the time in a review period, increase the buffer by one increment. If it stays green more than 80% of the time, decrease it by one increment.

DBM creates a self-calibrating system. Buffers adapt to actual demand without requiring re-forecasting.

---

## Adapted for Digital / SaaS

Distribution flow applies anywhere you have a supply-demand matching problem. In SaaS and digital businesses:

### Feature Delivery Pipeline
- **Buffer:** Features in staging, ready to release
- **Drum:** Release capacity (deploy slots, QA bandwidth)
- **Replenishment signal:** When feature queue drops to yellow, pull more from development backlog
- **Red signal:** Release queue empty — development is the bottleneck

### Content Distribution
- **Buffer:** Published articles, videos, or campaigns ready to schedule
- **Drum:** Publication calendar slots
- **Replenishment signal:** When content calendar has yellow coverage, commission more
- **Dynamic adjustment:** If content performs well (consumed faster), increase buffer target

### Sales Lead Allocation
- **Buffer:** Qualified leads assigned per sales rep
- **Drum:** Sales rep close capacity (deals/month)
- **Replenishment signal:** When a rep's pipeline drops to yellow, assign new leads
- **Urgent signal:** Rep at red with no leads assigned — pipeline at risk

### Customer Success Capacity
- **Buffer:** Onboarding slots available
- **Drum:** CS manager bandwidth
- **Replenishment signal:** When available slots drop to yellow, hire/train
- **Reduce signal:** Excess capacity → slow sales intake or redirect CS to expansion

---

## Central Aggregation Principle

TOC distribution advocates for **central stock aggregation** over distributed inventory. The reasoning is statistical: when N locations each hold safety stock for demand variability σ, total safety stock needed is:

```
Distributed: N × σ  (each location holds independent safety stock)
Centralized: √N × σ  (central stock covers the same variability)
```

For N=10 locations, centralization reduces required safety stock by 68%.

In digital systems, "centralization" means a shared pool — shared content calendar, shared lead pool, shared feature staging queue — rather than siloed per-team or per-region inventories.

---

## Scripts

### `scripts/buffer_sizing.py`

Calculate buffer size given consumption rate and lead time.

```bash
python3 scripts/buffer_sizing.py --file sizing.json
```

Input:
```json
{
  "avg_daily_consumption": 10,
  "replenishment_lead_time_days": 5,
  "variability_factor": 1.5,
  "current_level": 35
}
```

Output: buffer size, zone thresholds, current zone if level provided.

**Use when:** Setting initial buffer sizes, recalibrating after demand changes, or sizing buffers for a new distribution point.

### `scripts/replenishment_signal.py`

Generate replenishment signals for a portfolio of items.

```bash
python3 scripts/replenishment_signal.py --file inventory.json
```

Input:
```json
{
  "items": [
    {
      "name": "Widget A",
      "buffer_target": 100,
      "current_level": 28,
      "avg_daily_consumption": 8
    }
  ]
}
```

Output: per-item signals (urgent/replenish/hold/reduce) sorted by urgency, days of supply, zone.

**Use when:** Running a daily replenishment review, building a purchase order list, or identifying which items need immediate attention.

---

## Common Mistakes

**Mistake:** Using the buffer as a forecast ("we need 30 days of stock because we forecast 10 units/day for 30 days").
**Fix:** Size the buffer for variability and lead time, then replenish by consumption signal. The buffer is not a forecast.

**Mistake:** Replenishing to full buffer every time, regardless of consumption.
**Fix:** Only replenish what was consumed. If you consumed 15 units, replenish 15 units. This prevents the Bullwhip Effect.

**Mistake:** Setting buffer sizes once and never revisiting.
**Fix:** Apply Dynamic Buffer Management — review buffer sizes monthly and adjust based on zone penetration frequency.

**Mistake:** Managing by item count rather than buffer zone.
**Fix:** The zone tells you what action to take. An item at 25% of buffer needs action regardless of whether that's 25 units or 2,500 units.
