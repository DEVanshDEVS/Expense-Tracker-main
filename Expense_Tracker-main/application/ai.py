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


def build_financial_summary(entries):
    income_total = sum(
        entry.amount for entry in entries
        if (entry.type or "").strip().lower() == "income"
    )
    expense_total = sum(
        entry.amount for entry in entries
        if (entry.type or "").strip().lower() == "expense"
    )

    net_cash_flow = income_total - expense_total
    expense_ratio = (
        (expense_total / income_total) * 100
        if income_total
        else None
    )

    expenses_by_category = {}
    for entry in entries:
        if (entry.type or "").strip().lower() != "expense":
            continue
        category = entry.category or "uncategorized"
        expenses_by_category[category] = (
            expenses_by_category.get(category, 0) + entry.amount
        )

    largest_expense_category = None
    largest_expense_amount = None
    if expenses_by_category:
        largest_expense_category, largest_expense_amount = max(
            expenses_by_category.items(),
            key=lambda item: item[1]
        )

    lines = [
        f"- Verified total income: {income_total}",
        f"- Verified total expenses: {expense_total}",
        f"- Verified net cash flow: {net_cash_flow}",
    ]

    if expense_ratio is not None:
        lines.append(f"- Verified expense-to-income ratio: {expense_ratio:.1f}%")

    if largest_expense_category is not None:
        lines.append(
            f"- Verified largest expense category: "
            f"{largest_expense_category} ({largest_expense_amount})"
        )

    return "\n".join(lines)


def build_ai_prompt(context, summary):
    return f"""
You are a financial analysis assistant.

Analyze the user's transaction data below and follow these rules strictly:
- Keep income and expenses completely separate.
- Use the verified calculations below for totals and metrics. Do not recalculate them yourself.
- Never contradict a verified calculation.
- Never add a currency symbol or currency name unless it appears in the input.
- Never describe an amount as monthly, yearly, weekly, or any other period unless the input specifies that period.
- Never introduce external statistics, sources, averages, comparisons, or facts that are not in the input.
- Do not infer missing financial details.
- Base every claim only on the supplied transaction records and verified calculations.
- Refer to amounts exactly as supplied when discussing them.

Transaction data:
{context}

Verified calculations:
{summary}

Provide concise, practical analysis based only on the supplied records.
Use clear sections for Income, Expenses, and Insights.

For the Income and Expenses sections, list the relevant transactions and use the verified totals exactly.
In the Insights section, do not merely repeat the totals. Identify 2-4 useful patterns or observations using the verified calculations, such as net cash flow, expense-to-income ratio, largest expense, or concentration of spending. Do not perform new arithmetic that could contradict the verified calculations.
With limited data, state the limitation rather than inventing a conclusion.
""".strip()
