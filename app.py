import streamlit as st
import stripe
import secrets
import requests

# Initialize Stripe
stripe.api_key = 'sk_test_51P2EfNIS4MdDIAjNyeWsQlbLNZ3u1WoeyOvfCuXFtDLPvrxfzwYJe3kevMBZ7YwX6oHThHSjit8TEO7kR0o9GiBW000SFKKFfO'  # Replace with your Stripe secret key
st.set_page_config(page_title="Checkout", page_icon="💳")

# Session state for storing transaction status
if 'payment_status' not in st.session_state:
    st.session_state['payment_status'] = None

def create_checkout_session(amount, email):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Your Product Name',
                    },
                    'unit_amount': int(amount) * 100,  # Convert to cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='https://streamlit.io/success',  # You can adjust this
            cancel_url='https://streamlit.io/failure',  # You can adjust this
            customer_email=email
        )
        return session.id
    except Exception as e:
        st.error(f"Error creating checkout session: {str(e)}")
        return None

def checkout_page():
    st.title("Checkout")

    with st.form("checkout_form"):
        amount = st.number_input("Amount (in USD):", min_value=0)
        email = st.text_input("Email:")
        submit = st.form_submit_button("Checkout")

        if submit:
            session_id = create_checkout_session(amount, email)
            if session_id:
                st.success(f"Checkout session created! Session ID: {session_id}")
                st.write(f"[Proceed to Payment](https://checkout.stripe.com/pay/{session_id})")
            else:
                st.error("Failed to create checkout session.")

def payment_status_page():
    if st.session_state['payment_status'] == 'success':
        st.title("Payment Successful")
        st.write("Thank you for your payment!")
    elif st.session_state['payment_status'] == 'failure':
        st.title("Payment Failed")
        st.write("Sorry, your payment was not successful.")

def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Checkout", "Payment Status"])

    if page == "Checkout":
        checkout_page()
    elif page == "Payment Status":
        payment_status_page()

if __name__ == '__main__':
    main()
