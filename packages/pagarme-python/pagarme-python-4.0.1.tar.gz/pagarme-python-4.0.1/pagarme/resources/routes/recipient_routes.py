from pagarme.resources.routes import company_routes

BASE_URL = 'https://api.pagar.me/1/recipients'

GET_ALL_RECIPIENTS = BASE_URL

GET_DEFAULT_RECIPIENT = company_routes.BASE_URL

GET_RECIPIENT_BALANCE = BASE_URL + '/{0}/balance'

GET_RECIPIENT_BALANCE_OPERATIONS = BASE_URL + '/{0}/balance/operations'

GET_RECIPIENT_BALANCE_OPERATION_BY_ID = BASE_URL + '/{0}/balance/operations/{1}'

GET_RECIPIENT_BY = BASE_URL

UPDATE_RECIPIENT = BASE_URL + '/{0}'
