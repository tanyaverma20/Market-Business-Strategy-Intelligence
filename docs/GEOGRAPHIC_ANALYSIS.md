# Geographic Analysis

## Scope

The GAI framework is implemented as a reusable scoring template. It allows normalization and weighting for indicators such as market size, EV penetration, growth, purchasing power, charging infrastructure, and policy score.

## Status

The current state indicator dataset is not verified and is therefore not used for factual rankings. The output in [data/processed/geographic_scoring_template.csv](data/processed/geographic_scoring_template.csv) remains a data structure for future verified inputs, not a real state ranking.

## Methodology

- Normalization is min-max scaling over the available values.
- Default weights are analytical assumptions, not industry-standard truths.
- Weighted score is computed as a sum of normalized metrics multiplied by weights.
- The score is reported on a 0-100 scale.

## Interpretation

This framework is production-ready for future state-level analytics once verified state data becomes available. Until then, the project correctly labels the output as PENDING VERIFIED DATA.
