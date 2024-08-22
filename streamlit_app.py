import streamlit as st
import requests

# Flask server URL
FLASK_SERVER_URL = "http://localhost:5000"  # Update to your Flask server URL

def create_checkout_session(amount, email):
    response = requests.post(
        f"{FLASK_SERVER_URL}/create-checkout-session",
        json={"amount": amount, "email": email}
    )
    if response.status_code == 200:
        session_id = response.json().get('sessionId')
        return session_id
    else:
        st.error("Failed to create checkout session")
        return None

def main():
    st.title("Checkout Page")

    with st.form(key='checkout_form'):
        email = st.text_input("Email")
        amount = st.number_input("Amount (USD)", min_value=1)
        submit_button = st.form_submit_button("Pay")

        if submit_button:
            session_id = create_checkout_session(amount, email)
            if session_id:
                checkout_url = f"https://checkout.stripe.com/c/pay/{session_id}"
                st.write("Redirecting to checkout...")
                st.markdown(f'<a href="{checkout_url}" target="_blank">Click here if you are not redirected automatically.</a>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
