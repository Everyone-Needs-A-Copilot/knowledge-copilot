# <Product Name> — overview

> Copy `_dossier-template/` to `02-products/<layer>/<product-name>/` and fill this in.
> Machine-readable header so tools can parse the essentials:

```yaml
product: <product-name>
layer: <foundational | work | applications>
status: <idea | active | archived>
repo: <git url or "n/a">
local_path: <path on this machine or "n/a">
one_liner: <what it is, in one sentence>
```

## What it is

<Two or three sentences: the problem it solves and for whom.>

## How it works

<Architecture / key components at a high level.>

## Interfaces & integrations

<APIs, services, or other products it connects to. Reference any credentials as
`requires_secret: <NAME>` — never paste values.>

## Suggested companion docs

`01-architecture.md`, `02-usage.md`, `03-api.md`, `04-decisions.md` — add as needed.
