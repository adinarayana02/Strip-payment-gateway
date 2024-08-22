from flask import Flask, render_template, request, jsonify, redirect, url_for
import stripe
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)

stripe.api_key = 'sk_test_51P2EfNIS4MdDIAjNyeWsQlbLNZ3u1WoeyOvfCuXFtDLPvrxfzwYJe3kevMBZ7YwX6oHThHSjit8TEO7kR0o9GiBW000SFKKFfO'  # Replace with your Stripe secret key

@app.route('/')
def index():
    return render_template('checkout.html')

@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    data = request.json
    amount = int(data['amount']) * 100  # Convert amount to cents
    email = data['email']

    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Your Product Name',
                    },
                    'unit_amount': amount,
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=url_for('payment_success', _external=True),
            cancel_url=url_for('payment_failure', _external=True),
            customer_email=email
        )
        return jsonify({'sessionId': session.id})
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/payment-success')
def payment_success():
    return render_template('success.html')

@app.route('/payment-failure')
def payment_failure():
    return render_template('failure.html')

if __name__ == '__main__':
    app.run(port=3000, debug=True)
