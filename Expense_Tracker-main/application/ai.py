def build_financial_context(entries):
    lines = []

    for entry in entries:
        transaction_type = (entry.type or "").strip().lower()
        category = entry.category or "uncategorized"
        amount = entry.amount

        lines.append(
            f"- Type: {transaction_type}; Category: {category}; Amount: {amount}"
        )

    return "\n".join(lines)


def build_ai_prompt(context):
    return f"""
You are a financial analysis assistant.

Analyze the user's transaction data below. Keep income and expenses
semantically distinct and do not invent currency, time period, or other
financial details that are not present in the data.

Transaction data:
{context}

Provide concise, practical insights based only on the supplied records.
If a currency or time period is not provided, refer to amounts without
assuming one.
""".strip()
