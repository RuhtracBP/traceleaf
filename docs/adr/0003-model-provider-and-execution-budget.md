# Do not enable remote AI before an evaluated provider integration

M0 has no model adapter and makes no inference or embedding requests. All AI capabilities are unavailable, even if a key is present. An absent key is reported explicitly; a configured key is never returned to the client. No provider, model quality, price or token usage is claimed to have been validated.

The final model/provider selection is **pending M2**, when an official SDK can be evaluated on the development corpus. Compare structured output, tool calling, embeddings, latency, measured quality and dated pricing. Record exact generation/embedding model identifiers, embedding dimensions and a second generation model for M5; do not use a moving `latest` alias. The internal ModelGateway must keep authorization and budgets outside model output.

Initial policy for the future implementation: remote AI disabled by default; per-run limits of 8 tool calls, 2 repair attempts, 3 total attempts for a transient provider request, 60 seconds per request and 180 seconds per run. Start with at most 8,000 input tokens and 2,000 generated tokens per request; token counting and context truncation must be validated against the selected model. These limits are design decisions, **not enforced AI functionality in M0**.

External spending defaults to zero until the operator explicitly configures a provider, consent, a positive per-run monetary cap and a daily cap. Reject requests when price metadata or required accounting is unavailable. The estimate must include embeddings, generation, retries and evaluation. Do not charge or provision cloud resources during foundation setup. M2/M4 will implement and test budget enforcement before enabling calls; M6 requires separate cloud credentials and budget authorization.
