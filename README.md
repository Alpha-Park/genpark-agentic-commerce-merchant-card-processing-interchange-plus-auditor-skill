# Merchant Processing Interchange-Plus (IC+) Markup & Fee Leakage Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `audit_interchange_plus_processing_fees`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Deconstructs monthly merchant processing statements across Visa/Mastercard Interchange, card brand assessments, and acquirer markups, detecting fee padding and downgrades.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Agentic Commerce (Merchant FinTech & Acquiring)`

## MCP Tool Specification
### `audit_interchange_plus_processing_fees`
Parameters:
- `total_monthly_processing_volume_usd` (float): Gross monthly credit card sales volume
- `total_transactions_count` (int): Total settled transactions processed
- `contractual_acquirer_basis_points` (float): Agreed acquirer markup in bps (e.g. 15 bps = 0.15%)
- `contractual_per_transaction_fee_usd` (float): Agreed acquirer per-item fee (e.g. $0.10)
- `total_fees_billed_by_processor_usd` (float): Total gross fees deducted by payment gateway

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-agentic-commerce-merchant-card-processing-interchange-plus-auditor-skill": {
      "command": "python",
      "args": ["/path/to/genpark-agentic-commerce-merchant-card-processing-interchange-plus-auditor-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
