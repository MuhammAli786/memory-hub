# Security Boundary

This repository is deliberately non-operational. It contains no personal records, source transcripts, model outputs, service addresses, host names, user or team identifiers, repository references, credentials, authentication material, or deployment protocol details.

## Excluded by design

- Any secret value, credential, password, access token, signing material, or webhook verification value.
- Any production, home-directory, or machine-specific path.
- Any service binding, address, network overlay, port, or transport endpoint.
- Any configuration loading from the process environment.
- Any executable client that can connect to a live service.

## Before publishing

Run the release audit, inspect the complete tracked-file list, and use a secret scanner. Confirm that generated artifacts, test fixtures, command history, local configuration, and Git history are absent. Use a new repository with a new root commit; do not copy history from a private vault.

## Deployment guidance

Keep runtime configuration and authorization outside this repository. A deployment-specific adapter should accept configuration only from the operator's protected secret-management system. Review that adapter independently before use. Do not commit it back into this reference project.
