# Circularity Score Calculation

## Where the calculation lives

- [`modules/circularity/methodology.py`](./modules/circularity/methodology.py)
  defines `ScoringMethodology`, which holds the version and scoring rules.
- [`modules/circularity/scoring.py`](./modules/circularity/scoring.py)
  contains `CircularityScorer`, which normalizes indicator values and
  calculates dimension and overall scores.
- [`modules/product_data/product_repository.py`](./modules/product_data/product_repository.py)
  retrieves products and indicator values from SQLite. Scores are calculated
  from those indicators; they are not read from the database.
- [`app/routes.py`](./app/routes.py) asks the scorer to assess a product and
  passes the result to the page.
- [`app/templates/product.html`](./app/templates/product.html) displays the
  assessment and its coverage.

The default rules are held in `DEFAULT_METHODOLOGY`. A scorer can also be
created with a different `ScoringMethodology` object.

## Dimensions

The methodology defines three dimensions:

1. **Material Inputs**
2. **Design & Durability**
3. **End-of-Life Recovery**

Each indicator is stored with its dimension. The scorer processes indicators
separately for each dimension.

## Converting indicator values to a common scale

The scorer needs values on a 0–100 scale before it can average them. This
conversion is called **normalization**.

| Input format | Supported indicators or rule | Normalized result |
|---|---|---|
| Percentage such as `75%` | Any indicator name | `75` |
| Rating such as `8.8 / 10` | `Repairability index` | Rating multiplied by 10; `8.8 / 10` becomes `88` |
| Years such as `6 years` | `Spare-parts availability` or `Software support` | Years divided by 7 and multiplied by 100, capped at 100 |
| `Yes`, `Available`, or `No` | `Standard fasteners`, `Replaceable battery`, or `Take-back program` | `Yes` and `Available` become `100`; `No` becomes `0` |

Values outside the valid range are not scored. For example, `101%` and
`10.1 / 10` are unsupported. The binary conversion applies only to the listed
indicator names; an unrelated indicator with value `Yes` is not automatically
given a score.

The seven-year cap means that both `7 years` and any value above seven years
normalize to `100`. This is a prototype assumption, not a conclusion that
seven years is the correct real-world sustainability threshold.

## Calculating each dimension

After normalization, the scorer calculates the **arithmetic mean** of the
usable indicators in that dimension:

```text
dimension score = sum of usable normalized indicator scores
                  / number of usable normalized indicator scores
```

Every usable indicator currently has equal weight within its dimension. No
dimension-specific indicator weights are configured.

If a dimension has no usable indicators, its score is `N/A` (`None` in Python).
Missing information is not treated as a score of zero.

## Calculating the overall score

The scorer takes the arithmetic mean of the dimension scores that are
available:

```text
overall score = sum of available dimension scores
                / number of available dimension scores
```

Each available dimension has equal weight in the overall score. A dimension
with no usable indicators is excluded. If all three dimensions have no usable
indicators, the overall score is also unavailable.

Carbon footprint is shown separately and is not included in the Circularity
Score.

## Coverage

The assessment reports two kinds of coverage:

- **Indicator coverage for a dimension** is the number of usable indicators
  divided by the total number of indicators listed in that dimension. The
  product page displays this as a count, for example `2 / 3 indicators`.
- **Overall dimension coverage** is the number of dimensions with a score
  divided by the three defined dimensions. The product page displays this as a
  percentage, for example `100% of dimensions`.

Coverage describes how much of the available data contributed; it is not a
measure of score quality or product sustainability. For example, `100% of
dimensions` can still mean that some indicators within those dimensions were
unavailable.
