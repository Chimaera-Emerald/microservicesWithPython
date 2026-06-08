# Module 4 — Reflection

**Team name**: Chimaera-Emerald
**Branch**: `module-04/chimaera-emerald`
**Submitted**: before Module 5 lesson

---

Answer the three questions below. There are no right or wrong answers — we are looking for your reasoning, not a textbook definition. A few honest sentences are worth more than a long generic paragraph.

---

## 1. The "why"

In Module 3, services called each other directly over HTTP. Now activity-service drops a message into a broker and moves on — it never waits for a reply.

**What does the activity-service gain by not waiting? And what does the notification-service gain by consuming at its own pace?**

Think about what happens under load, or when notification-service is temporarily down.

> *Your answer:*
> activity-service can save the activity fast and move on, so the user isn't stuck waiting for notifications. if notification-service is down or slow, the message sits in rabbitmq and gets handled later. that means the main flow stays working even if notifications are temporarily offline.

---

## 2. Your choice

In Module 3 you already knew how to call another service directly over HTTP — you did it for user validation and game enrichment.

**Why not use the same approach for notifications? What does introducing a broker give you that a direct HTTP call doesn't?**

Think about what happens if notification-service is slow, or crashes mid-message.

> *Your answer:*
> if we did HTTP, activity creation would hang or fail whenever notification-service was slow or down. with rabbitmq the activity-service just drops a message and keeps going, so the main request stays fast and reliable. the broker decouples them — notifications can be processed later without holding up the user.

---

## 3. The tradeoff

With synchronous REST, you get an immediate answer: success or failure. With async messaging, the activity is saved and the message is sent — but you have no idea if the notification was ever delivered.

**How would a user know if their notification was never sent? How would you know as a developer?**

What visibility do you lose when you go async?

> *Your answer:*
> the user probably wouldn't know right away — they just see the activity succeed and may never see the notification. as a dev you'd need logs, queue metrics, or dead-letter handling to know if the message got stuck. going async means you lose immediate delivery confirmation: the request is done before the notification is actually processed.

---

*Keep this file. You will refer back to it during the oral presentation.*
