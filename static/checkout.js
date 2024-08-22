document.addEventListener('DOMContentLoaded', function () {
    var stripe = Stripe('pk_test_51P2EfNIS4MdDIAjNEABa0PlwvzI7GgHdEGtCzCNPG0hDODhI8qz46TqRbUvFYSTvAsnneCnW0UNlWLubpZ0TQqxo00VUTUTc3n'); // Your Stripe public key
    var elements = stripe.elements();

    // Create an instance of the card Element
    var card = elements.create('card');
    card.mount('#card-element');

    // Handle form submission
    var form = document.getElementById('payment-form');
    form.addEventListener('submit', function (event) {
        event.preventDefault();

        var amount = document.getElementById('amount').value;
        var email = document.getElementById('email').value;

        // Create a payment intent
        fetch('/create-payment-intent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ amount: amount, email: email }),
        })
        .then(function (response) {
            return response.json();
        })
        .then(function (paymentIntentResponse) {
            var clientSecret = paymentIntentResponse.clientSecret;

            stripe.confirmCardPayment(clientSecret, {
                payment_method: {
                    card: card,
                    billing_details: {
                        email: email,
                    },
                }
            })
            .then(function (result) {
                if (result.error) {
                    var errorElement = document.getElementById('card-errors');
                    errorElement.textContent = result.error.message;
                } else {
                    if (result.paymentIntent.status === 'succeeded') {
                        window.location.href = '/payment-success';
                    }
                }
            });
        });
    });
});
