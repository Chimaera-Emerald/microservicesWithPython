# Module 3 — Reflection

**Team name**: Chimaera-Emerald
**Branch**: `module-03/chimaera-emerald`
**Submitted**: Module 3 implementation complete

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

All client requests now go through the gateway. No client ever calls a service directly.

**Why does that single entry point exist? What would the client's life look like without it?**

Think about what the client would need to know and manage if it talked to each service on its own port.

> *Your answer:*
> without the gateway the client gotta know where every service is. like remember which port is 8001, 8002, 8003? pain. if we move stuff around or scale, client code breaks. gateway solves that — client just talks to one address and the gateway figures out where to send it. also means we can add auth or rate limiting in one place instead of everywhere.

---

## 2. Your choice

The activity-service makes two outbound calls: one to validate the user (with retry logic), one to fetch game data (with a null fallback if it fails).

**Why are these two calls treated differently? Why does one retry and the other just give up gracefully?**

What is the consequence for the user in each case if the downstream service is unavailable?

> *Your answer:*
> user validation is a must-have. u can't save an activity without knowing the user exists or u get junk data. so we retry and fail hard if it doesn't work. game data is just extra — the activity is still good even if we don't have the game name. so if game-service dies we're like "ok whatever here's null" instead of blowing up everything.

---

## 3. The tradeoff

Every time a client creates an activity, three services are involved synchronously. They all have to be running, healthy, and fast.

**What is the systemic risk of chaining synchronous calls like this?**

What happens to the user experience if the slowest service in the chain takes 3 seconds to respond?

> *Your answer:*
> ur system is only as fast as the slowest service. if one takes 3 seconds everything waits. plus if anything dies the whole chain breaks. that's why big systems use queues and stuff — so one slow/dead service doesn't tank everything else.

---

*Keep this file. You will refer back to it during the oral presentation.*
