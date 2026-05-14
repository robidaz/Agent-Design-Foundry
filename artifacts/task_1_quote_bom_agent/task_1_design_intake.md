# Task 1 — Quote / BOM Generation Agent

## Context

Dynamix sources from 200+ vendors and distributors — Arrow, TD Synnex, Ingram Micro, and others. Sales engineers spend significant time manually building Bills of Materials for customer requirements: pulling SKUs across catalogs, validating availability and lead times, calculating margin against vendor cost, and assembling alternatives at different price/performance tiers. Quote turnaround time is one of the levers we use to compete; today, it is slower than it should be.

## Assumptions
- PoC leverages only 3-4 representative product categories, but solution should support additional product categories to be added in the future
- Catalog data is created using a python script created by Claude for repeatable data output specific to the task
- PoC will have a specific data source referenced in the form of JSON or YAML and consists of 50 Vendors/Distributors each with multiple product SKUs varied across the defined product categories
- A boilerplate BOM template is be used for PoC
- Sales engineer is responsible for producing a curated list of customer requirements
- Sales engineer has basic knowledge of the product suite such that provided requirements can feasibly be used to produce comparable results
- Agent is not responsible for updating/ managing data source
- Data source returns key date fields indicating last updated overall source data, as well as effective date of each vendor's catalog
  - Effective data is not tracked at the SKU level
- Data source provides
- Customer requirements can be satisfied by leveraging SKUs across different vendors, but vendors should not vary across a specific category
- Sales engineer provides an initial source of definitions and rules solicited by the AI Architect
  - Sales engineer provides fallback rulesets that drive agent evaluation logic if not called out (i.e. acceptable lead times, time since last update)
  - Sales engineer provides initial descriptions of product classes represented in catalogs to be used to translate initial prompt. Sales engineer maintains this list manually or via prompt
- Sales engineer is referred to as 'user' throughout document


## Requirements
- Agent that converts a customer technical requirement into a multi-vendor BOM
  - Needs to support
- Product categories, Vendors, and individual SKUs are subject to change and thus the agent must be able to support a variable data model
- Agent references a "rulesets & guidelines" source initially provided by user that serves as the translation basis
  - Agent reads this document before performing any evaluations
  - Agent has the ability to modify this source when given explicit access to do so by the user (Sales Engineer)
- Agent evaluates product data based on availability, lead times, margin.
- Agent must be able to support specific Vendor or SKU requests from user and validate availability and lead time as a constraint. If initial user request can not be met agent must provide alternative or state that request can not be met and provide reasoning.
- Agent must prioritize information accuracy over results returned, meaning the output may be that no data is available based on the users request.

## Scope Exclusions
- Full Pricing Engine
- Contract Pricing
- Customer Portal UI

## Proposed Deliverables

- BoM with 3 tiers of price/performance
- Relevant data points from the Vendor/SKU selected
- Justification of choices and soft recommendation
