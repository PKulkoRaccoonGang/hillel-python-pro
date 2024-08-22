from webargs import fields, validate

from settings import MIN_NUMBER_OF_USERS, MAX_NUMBER_OF_USERS


number_of_users_config = {
  'number_of_users': fields.Int(
    missing=MIN_NUMBER_OF_USERS,
    validate=validate.Range(min=MIN_NUMBER_OF_USERS, max=MAX_NUMBER_OF_USERS, max_inclusive=True)
  )
}


bitcoin_search_config = {
  'currency': fields.Str(load_default='USD'),
  'amount_of_currency': fields.Int(load_default=1, validate=validate.Range(min=1))
}
