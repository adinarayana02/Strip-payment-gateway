import streamlit as st
import stripe
import secrets

# Set up Stripe API key
stripe.api_key = 'sk_test_51P2EfNIS4MdDIAjNyeWsQlbLNZ3u1WoeyOvfCuXFtDLPvrxfzwYJe3kevMBZ7YwX6oHThHSjit8TEO7kR0o9GiBW000SFKKFfO'  # Replace with your Stripe secret key

# Streamlit app code
st.title("Stripe Payment Integration")

st.write("Enter your email and the amount to pay:")

# Collect email and amount input from the user
email = st.text_input("Email", "")
amount = st.number_input("Amount (USD)", min_value=0.0, step=0.01)

# When the "Pay" button is clicked
if st.button("Pay"):
    if email and amount > 0:
        try:
            # Create a new Stripe Checkout Session
            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Your Product Name',
                        },
                        'unit_amount': int(amount * 100),  # Convert amount to cents
                    },
                    'quantity': 1,
                }],
                mode='payment',
                 success_url=url_for('payment_success', _external=True),
            cancel_url=url_for('payment_failure', _external=True),
            customer_email=email
            )
            # Display success message and provide a link to the Stripe Checkout page
            st.success("Session created successfully! Redirecting to payment...")
            st.write(f"Session ID: {session.id}")
            st.markdown(f"[Proceed to Payment](https://checkout.stripe.com/pay/{session.id})", unsafe_allow_html=True)
        except Exception as e:
            # Display any error that occurs during the session creation
            st.error(f"Error: {str(e)}")
    else:
        # Prompt the user to enter valid details if they haven't
        st.warning("Please enter a valid email and amount.")
