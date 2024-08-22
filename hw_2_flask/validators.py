from webargs import fields, validate


password_length_config = {
  'length': fields.Int(
    missing=10, 
    validate=validate.Range(min=8, max=100, max_inclusive=True)
  ),
}
