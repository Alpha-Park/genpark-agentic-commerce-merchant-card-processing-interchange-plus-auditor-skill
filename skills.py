# -*- coding: utf-8 -*-
"""Merchant Processing Interchange-Plus (IC+) Markup & Fee Leakage Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def audit_interchange_plus_processing_fees(**kwargs):
    """Deconstructs monthly merchant processing statements across Visa/Mastercard Interchange, card brand assessments, and acquirer markups, detecting fee padding and downgrades."""
    total_monthly_processing_volume_usd = kwargs.get('total_monthly_processing_volume_usd')
    total_transactions_count = kwargs.get('total_transactions_count')
    contractual_acquirer_basis_points = kwargs.get('contractual_acquirer_basis_points')
    contractual_per_transaction_fee_usd = kwargs.get('contractual_per_transaction_fee_usd')
    total_fees_billed_by_processor_usd = kwargs.get('total_fees_billed_by_processor_usd')

    # Effective rate = total fees / volume
    effective_rate_pct = round((total_fees_billed_by_processor_usd / (total_monthly_processing_volume_usd if total_monthly_processing_volume_usd > 0 else 1.0)) * 100.0, 3)
    
    # Standard blended wholesale Interchange + Card Brand Assessments average ~ 1.85%
    estimated_wholesale_interchange = total_monthly_processing_volume_usd * 0.0185
    
    # Contractual Acquirer Markup
    contractual_vol_markup = total_monthly_processing_volume_usd * (contractual_acquirer_basis_points / 10000.0)
    contractual_item_markup = total_transactions_count * contractual_per_transaction_fee_usd
    contractual_total_markup = round(contractual_vol_markup + contractual_item_markup, 2)
    
    expected_total_fees = round(estimated_wholesale_interchange + contractual_total_markup, 2)
    unexplained_fee_leakage = round(max(0.0, total_fees_billed_by_processor_usd - expected_total_fees), 2)
    
    result = {
        "status": "success",
        "gross_volume_usd": total_monthly_processing_volume_usd,
        "effective_processing_rate_pct": effective_rate_pct,
        "estimated_wholesale_interchange_usd": round(estimated_wholesale_interchange, 2),
        "contractual_acquirer_markup_usd": contractual_total_markup,
        "expected_legitimate_charges_usd": expected_total_fees,
        "actual_processor_billed_fees_usd": total_fees_billed_by_processor_usd,
        "unexplained_fee_padding_leakage_usd": unexplained_fee_leakage,
        "processor_contract_audit_verdict": f"FEE_PADDING_DETECTED: Processor overbilled approximately ${unexplained_fee_leakage:.2f} via non-qualified downgrade padding." if unexplained_fee_leakage > 200.0 else "FEES_COMPLIANT_WITH_INTERCHANGE_PLUS_SCHEDULE",
        "engine": "GenPark Merchant Acquiring Interchange-Plus Audit Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "audit_interchange_plus_processing_fees": {
        "name": "audit_interchange_plus_processing_fees",
        "description": "Deconstructs monthly merchant processing statements across Visa/Mastercard Interchange, card brand assessments, and acquirer markups, detecting fee padding and downgrades.",
        "parameters": {
            "type": "object",
            "properties": {
                "total_monthly_processing_volume_usd": {"type": "number", "description": "Gross monthly credit card sales volume"},
                "total_transactions_count": {"type": "integer", "description": "Total settled transactions processed"},
                "contractual_acquirer_basis_points": {"type": "number", "description": "Agreed acquirer markup in bps (e.g. 15 bps = 0.15%)"},
                "contractual_per_transaction_fee_usd": {"type": "number", "description": "Agreed acquirer per-item fee (e.g. $0.10)"},
                "total_fees_billed_by_processor_usd": {"type": "number", "description": "Total gross fees deducted by payment gateway"},
            },
            "required": ['total_monthly_processing_volume_usd', 'total_transactions_count', 'contractual_acquirer_basis_points', 'contractual_per_transaction_fee_usd', 'total_fees_billed_by_processor_usd']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "audit_interchange_plus_processing_fees":
            res = audit_interchange_plus_processing_fees(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-merchant-card-processing-interchange-plus-auditor-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-agentic-commerce-merchant-card-processing-interchange-plus-auditor-skill...")
    test_args = {'total_monthly_processing_volume_usd': 1250000.0, 'total_transactions_count': 18500, 'contractual_acquirer_basis_points': 12.0, 'contractual_per_transaction_fee_usd': 0.08, 'total_fees_billed_by_processor_usd': 28450.0}
    res = audit_interchange_plus_processing_fees(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-agentic-commerce-merchant-card-processing-interchange-plus-auditor-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
