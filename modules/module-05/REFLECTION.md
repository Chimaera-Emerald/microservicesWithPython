# Module 5 — Reflection

**Team name**: _______________
**Branch**: `module-05/<team-name>`
**Submitted**: before Module 6 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The game-service now has two models for the same data: SQLite for writes, Redis for reads. They store the same games in two different shapes.

**Why go through the trouble of maintaining two representations of the same data?**

Think about what kind of queries each model is optimised for, and what would happen if you tried to use the write model for high-traffic read operations.

> SQLite is optimised for accurate, transactional writes — it handles one game being added or updated reliably. But if thousands of users were hitting GET /v1/games/{id}/summary at the same time, hammering SQLite with reads would slow it down and compete with writes. Redis keeps a pre-computed, denormalised version in memory so reads are nearly instant and don't touch the database at all. The cost is maintaining two copies, but the benefit is that reads and writes can scale independently without blocking each other.

---

## 2. Your choice

The logging-service checks GDPR consent before recording any activity. If a user has not opted in, the log is silently dropped.

**What does this consent check force you to accept about your data?** It is incomplete by design — some activities will never be recorded.

From a system design perspective: where is the right place to enforce this rule — in the logging-service, in the activity-service, or at the gateway? Why?

> It forces you to accept that your logs will have gaps — they are not a complete record of what happened, only a record of what consenting users did. That's intentional and legally required under GDPR. The right place to enforce it is in the logging-service, because that's the service responsible for storing the data. If you put it in the gateway or activity-service, you're leaking a data storage concern into layers that shouldn't care about it. The logging-service owns the decision of what it stores, so it owns the consent check.

---

## 3. The tradeoff

With CQRS, your write model and read model can drift out of sync — a game is updated in SQLite but the Redis projection still shows the old data.

**In what scenario does this inconsistency matter to the user? In what scenario is it completely acceptable?**

Is there a class of applications where eventual consistency is never acceptable? What are they?

> It matters when the user is acting on the data — for example, if a game's platform was corrected and a user reads the stale summary to decide whether to buy it, they could make the wrong decision based on old information. It's completely acceptable for a browse page or leaderboard where being a few seconds behind doesn't affect anything important. Applications where eventual consistency is never acceptable are financial systems (bank balances, payment processing) and medical systems (drug dosages, patient records) — anywhere where stale data could cause real harm or financial loss.

---

*Keep this file. You will refer back to it during the oral presentation.*
