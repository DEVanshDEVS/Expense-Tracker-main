from flask import render_template, url_for, redirect, flash, jsonify
from application import app, db
from application.form import UserDataForm
from application.models import IncomeExpenses
from application.ai import build_financial_context, build_financial_summary, build_ai_prompt
import ollama


@app.route('/')
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template('index.html', entries=entries)


@app.route('/add', methods=["POST", "GET"])
def add_expense():
    form = UserDataForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(
            type=form.type.data,
            category=form.category.data,
            amount=form.amount.data
        )
        db.session.add(entry)
        db.session.commit()
        flash(f"{form.type.data} has been added to {form.type.data}s", "success")
        return redirect(url_for('index'))
    return render_template('add.html', title="Add expenses", form=form)


@app.route('/delete-post/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(entry_id)
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for("index"))


@app.route('/dashboard')
def dashboard():
    income_vs_expense = db.session.query(
        db.func.sum(IncomeExpenses.amount),
        IncomeExpenses.type
    ).group_by(
        IncomeExpenses.type
    ).order_by(
        IncomeExpenses.type
    ).all()

    expense_categories = db.session.query(
        db.func.sum(IncomeExpenses.amount),
        IncomeExpenses.category
    ).filter(
        IncomeExpenses.type == 'expense'
    ).group_by(
        IncomeExpenses.category
    ).order_by(
        IncomeExpenses.category
    ).all()

    expense_dates = db.session.query(
        db.func.date(IncomeExpenses.date),
        db.func.sum(IncomeExpenses.amount)
    ).filter(
        IncomeExpenses.type == 'expense'
    ).group_by(
        db.func.date(IncomeExpenses.date)
    ).order_by(
        db.func.date(IncomeExpenses.date)
    ).all()

    income_expense = [total_amount for total_amount, _ in income_vs_expense]
    expense_category_values = [amount for amount, _ in expense_categories]
    expense_category_labels = [category for _, category in expense_categories]
    over_time_expenditure = [amount for _, amount in expense_dates]
    dates_label = [date for date, _ in expense_dates]

    return render_template(
        'dashboard.html',
        income_vs_expense=income_expense,
        expense_category_values=expense_category_values,
        expense_category_labels=expense_category_labels,
        over_time_expenditure=over_time_expenditure,
        dates_label=dates_label
    )


@app.route('/llama_insights', methods=['POST'])
def llama_insights():
    try:
        data = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()

        if not data:
            return jsonify({"insights": "No financial data available."}), 400

        context = build_financial_context(data)
        summary = build_financial_summary(data)\n        prompt = build_ai_prompt(context, summary)

        response = ollama.chat(
            model='llama3',
            messages=[{"role": "user", "content": prompt}],
            options={
                "num_predict": 300,
                "temperature": 0.2
            },
            keep_alive="10m"
        )

        message = response.get('message', {}) if isinstance(response, dict) else getattr(response, 'message', None)
        insights = (
            message.get('content')
            if isinstance(message, dict)
            else getattr(message, 'content', None)
        )

        if insights:
            return jsonify({"insights": insights})

        return jsonify({"insights": "Error: No response from AI"}), 500

    except Exception as e:
        app.logger.exception("Error fetching AI insights: %s", e)
        return jsonify({"insights": "Error fetching insights"}), 500
