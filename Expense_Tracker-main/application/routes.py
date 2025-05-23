from application import app, db
from flask import render_template, url_for, redirect, flash, request, jsonify
from application.form import UserDataForm
from application.models import IncomeExpenses
import json
import ollama  # Import Ollama for Llama 3


@app.route('/')
def index():
    entries = IncomeExpenses.query.order_by(IncomeExpenses.date.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/add', methods=["POST", "GET"])
def add_expense():
    form = UserDataForm()
    if form.validate_on_submit():
        entry = IncomeExpenses(type=form.type.data, category=form.category.data, amount=form.amount.data)
        db.session.add(entry)
        db.session.commit()
        flash(f"{form.type.data} has been added to {form.type.data}s", "success")
        return redirect(url_for('index'))
    return render_template('add.html', title="Add expenses", form=form)

@app.route('/delete-post/<int:entry_id>')
def delete(entry_id):
    entry = IncomeExpenses.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for("index"))

@app.route('/dashboard')
def dashboard():
    income_vs_expense = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.type).group_by(IncomeExpenses.type).order_by(IncomeExpenses.type).all()
    category_comparison = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.category).group_by(IncomeExpenses.category).order_by(IncomeExpenses.category).all()
    dates = db.session.query(db.func.sum(IncomeExpenses.amount), IncomeExpenses.date).group_by(IncomeExpenses.date).order_by(IncomeExpenses.date).all()

    income_category = [amounts for amounts, _ in category_comparison]
    income_expense = [total_amount for total_amount, _ in income_vs_expense]
    over_time_expenditure = [amount for amount, _ in dates]
    dates_label = [date.strftime("%m-%d-%y") for _, date in dates]

    return render_template('dashboard.html',
                            income_vs_expense=json.dumps(income_expense),
                            income_category=json.dumps(income_category),
                            over_time_expenditure=json.dumps(over_time_expenditure),
                            dates_label=json.dumps(dates_label)
                        )

@app.route('/llama_insights', methods=['POST'])
def llama_insights():
    try:
        data = IncomeExpenses.query.all()
        if not data:
            return jsonify({"insights": "No expense data available."}), 400

        expenses = [f"{entry.category}: {entry.amount}" for entry in data]
        prompt = f"Analyze these expenses and provide savings tips: {', '.join(expenses)}"
        
        response = ollama.chat(model='llama3', messages=[{"role": "user", "content": prompt}])

        if 'message' in response and 'content' in response['message']:
            insights = response['message']['content']
            return jsonify({"insights": insights})
        else:
            return jsonify({"insights": "Error: No response from AI"}), 500

    except Exception as e:
        print("Error fetching AI insights:", str(e))
        return jsonify({"insights": "Error fetching insights"}), 500


