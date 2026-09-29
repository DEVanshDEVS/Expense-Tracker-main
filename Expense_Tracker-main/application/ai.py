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

Analyze the user's transaction data below and follow these rules strictly:
- Keep income and expenses completely separate.
- Never add a currency symbol or currency name unless it appears in the input.
- Never describe an amount as monthly, yearly, weekly, or any other period unless the input specifies that period.
- Never introduce external statistics, sources, averages, comparisons, or facts that are not in the input.
- Do not infer missing financial details.
- Base every claim only on the supplied transaction records.
- Refer to amounts exactly as supplied when discussing them.

Transaction data:
{context}

Provide concise, practical insights based only on the supplied records.
Use clear sections for Income, Expenses, and Insights.
""".strip()
