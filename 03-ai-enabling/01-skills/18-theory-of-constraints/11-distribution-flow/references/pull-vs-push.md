---
last_updated: 2026-04-02
status: active
---

# Pull vs. Push Replenishment

## The Core Distinction

**Push replenishment:** Decide in advance how much to stock based on forecast. Send product downstream based on what you think will be consumed. The system is driven by predictions.

**Pull replenishment:** Replenish what was actually consumed, when it was consumed, in the quantity consumed. The system is driven by actual demand signals.

---

## Why Push Fails

### 1. Forecast Error Is Inevitable

No forecast is accurate at the SKU-location level. Aggregated demand forecasts (total units sold) can be reasonably accurate. But distributing that forecast across hundreds of locations and thousands of SKUs multiplies the error at every level.

A forecast that's 90% accurate at the aggregate level might be 40-60% accurate at the local level. Push systems stock based on local forecasts — they inherit local forecast error directly.

### 2. The Bullwhip Effect

Small demand variations at retail become large swings at distribution. The mechanism:

1. Retail sees a 10% demand spike one week (noise, not a real trend).
2. Retailer orders 20% more to cover the spike and rebuild safety stock.
3. Distributor sees a 20% increase in orders, interprets it as a trend, orders 30% from the manufacturer.
4. Manufacturer sees 30% demand increase, ramps production, over-produces.
5. The spike was noise. The result is a system-wide overstock followed by a shortage as the excess is worked down.

Pull systems don't amplify signals. Each replenishment is sized to what was consumed, not what someone predicted would be consumed. The signal stays proportional to actual demand.

### 3. Stock in the Wrong Place

Push systems distribute stock based on forecast allocation. When forecasts are wrong (which they always are), stock ends up in wrong locations:

- Location A over-forecast → excess inventory that may be written off
- Location B under-forecast → stockout that loses sales and customers

The stock doesn't move between locations without cost and delay. The forecast error becomes permanent until the next planning cycle.

Pull systems let actual demand pull stock from a central buffer. The stock goes where demand actually is, not where it was predicted to be.

---

## How Pull Replenishment Works

**The basic cycle:**
1. A unit is consumed at a distribution point.
2. A replenishment signal is immediately sent for that unit.
3. The signal travels upstream until it reaches the stocking point with inventory.
4. The unit is shipped to replenish the consumed unit.
5. The cycle repeats.

**The buffer:** Each distribution point holds a buffer — not a forecast-based inventory level, but a variability absorber. The buffer is sized for lead time variability, not for demand prediction.

**The signal:** The replenishment signal is triggered by zone penetration (yellow or red), not by calendar (weekly purchase orders) or forecast (reorder point based on predicted demand).

---

## Advantages of Pull

| Dimension | Push | Pull |
|-----------|------|------|
| Stock location | Based on forecast allocation | Based on actual consumption |
| Stockout cause | Forecast error | Buffer undersizing |
| Excess inventory | Forecast over-prediction | Buffer oversizing |
| Reaction to demand change | Next planning cycle | Next replenishment cycle |
| Bullwhip amplification | Yes | Minimal |
| Management attention | Weekly order calculation | Daily zone monitoring |
| System complexity | High (multi-level forecasting) | Low (compare level to zone threshold) |

---

## The Central Buffer Advantage

Pull replenishment works best with centralized inventory. Instead of allocating fixed stock to each location based on forecast, hold a central buffer and replenish as consumption signals arrive from each location.

**Why centralization works:**
- Central buffer aggregates variability across all locations. Statistical pooling means the central buffer can be smaller than the sum of all distributed buffers.
- No stock gets "trapped" at a location with low demand — it stays central until a location with high demand signals for it.
- Replenishment signal latency determines how quickly central stock responds. With modern systems, this can be same-day or next-day.

**In digital systems:** The "central buffer" is a shared pool. A pool of qualified leads, a shared content calendar, a shared onboarding queue. Each team/region/channel pulls from the pool as their local supply depletes.

---

## Objections and Responses

**"We need to predict demand to plan production capacity."**
True — production planning requires some forecast. But distribution replenishment doesn't. Separate the two: use rough aggregate forecasts for capacity planning (where forecast accuracy is reasonable), use pull signals for distribution (where local forecast error is high).

**"Frequent small replenishments cost more in shipping."**
Pull replenishment enables smaller, more frequent replenishments. Shipping cost is a real concern. The trade-off: compare shipping cost increase against inventory carrying costs, write-offs from excess, and lost sales from stockouts. In most supply chains, the latter exceed the former substantially.

**"Our lead times are too long for pull to work."**
Long lead times require larger buffers, but don't invalidate pull. The buffer absorbs variability during the lead time. If lead times are very long (months), the buffer may be large — but it's still sized for variability, not for forecast. The alternative (forecast-driven push with long lead times) is worse: you're forecasting further out, with more error, resulting in even larger excess inventory.

**"We already have an MRP/ERP system."**
Most ERP systems support pull replenishment alongside MRP. Pull replenishment doesn't require replacing ERP — it requires changing the trigger (consumption signal instead of reorder point) and the sizing logic (variability-based buffer instead of safety stock formula).
