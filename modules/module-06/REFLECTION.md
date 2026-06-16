# Module 6 — Reflection

**Team name**: _______________
**Branch**: `module-06/<team-name>`
**Submitted**: before Module 7 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

The gateway now validates every JWT before forwarding a request. Individual services no longer need to check identity themselves.

**What does centralising authentication at the gateway buy you?** What would the alternative look like — if every service validated tokens on its own?

Think about what happens when you need to rotate the secret key, or add a new service to the system.

> Centralising it at the gateway means there is one place to update when you rotate the secret key — you change it in the gateway config and you're done. If every service validated tokens on its own, rotating the key would mean updating and redeploying every service simultaneously, which is error-prone and creates a window where some services accept old tokens and others don't. Adding a new service would also mean remembering to add auth logic to it. The gateway makes auth a solved problem that new services inherit for free.

---

## 2. Your choice

When activity-service calls user-service internally, it uses a Machine-to-Machine (M2M) token — not a user's token.

**Why can't it just reuse the user's token that arrived in the original request?**

What would break, or what door would you accidentally leave open, if services passed user tokens between themselves?

> If activity-service forwarded the user's token to user-service, then user-service would think it's talking directly to the user, not to another service. This breaks accountability — you can no longer tell whether a request came from the user or from an internal service acting on their behalf. Worse, it means any service could impersonate the user and call any other service with their full permissions. The M2M token has role "service", which can be granted only the specific permissions it needs, keeping internal traffic separate from user traffic.

---

## 3. The tradeoff

The gateway and the auth-service share the same `SECRET_KEY` to verify tokens without making a network call on every request.

**What is the security risk of sharing this key?** What happens if it leaks?

And what would the alternative look like — verifying tokens by calling auth-service on every request instead? What does that cost you?

> If the SECRET_KEY leaks, anyone who has it can forge valid tokens for any user with any role — including admin. There's no way to detect forged tokens because they're cryptographically indistinguishable from real ones. The only fix is to rotate the key immediately and invalidate all existing tokens. The alternative — calling auth-service on every request to verify tokens — eliminates that risk since the key never leaves auth-service. But the cost is latency on every single request and a single point of failure: if auth-service goes down, the entire system stops working. The shared key approach trades some security risk for performance and resilience.

---

*Keep this file. You will refer back to it during the oral presentation.*
