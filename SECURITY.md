# Security

- Scripts make outbound HTTP requests only to the target site and, when keys are present, to the OpenAI, Perplexity, Google and Anthropic APIs.
- Keys are read from environment variables and never written to disk by this project.
- The audit fetches pages with crawler user-agent strings for diagnosis; it does not bypass authentication, rate limits or bot protection. Respect the target's terms and keep fetch volumes small.
- Report vulnerabilities by opening a GitHub issue marked "security" or contacting the maintainer directly.
