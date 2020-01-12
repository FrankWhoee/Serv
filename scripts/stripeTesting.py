import stripe

# Set your secret key: remember to change this to your live secret key in production
# See your keys here: https://dashboard.stripe.com/account/apikeys
stripe.api_key = 'sk_test_kzn7NBgGPNNyYq3FUMafE2f300hzdblNYt'

customer = stripe.Customer.create(
  name='jenny rosen',
  email='jenny.rosen@example.com',
  description='My First Test Customer (created for API docs)',
)

print(customer)