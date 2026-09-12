# Unit Economics

## Scope

The unit-economics module provides a reusable structure for gross margin, contribution margin, break-even, and TCO calculations. It is intentionally fail-closed. No factual business result is produced without verified cost/BOM inputs.

## Available framework elements

- COGS input placeholder
- gross margin calculation
- gross margin %
- variable cost handling
- contribution margin and contribution margin %
- break-even units and break-even revenue
- TCO template

The methods are in [src/analytics/unit_economics.py](src/analytics/unit_economics.py). The project exports templates in [data/processed/unit_economics_input_template.csv](data/processed/unit_economics_input_template.csv) and [data/processed/unit_economics_results.csv](data/processed/unit_economics_results.csv).

## Verified vs pending status

- VERIFIED: only the mathematical formulas are implemented.
- PENDING VERIFIED COST DATA: the actual cost fields are not populated and no business result is claimed.
- PROXY / NOT ALLOWED: no invented or estimated cost assumptions are used.

## Interpretation

This framework is useful when a verified cost model is later supplied, because it can test pricing sensitivity and profitability assumptions. Until then, it is a safe template and calculation library, not a business claim.
