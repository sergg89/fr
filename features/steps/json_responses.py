import trafaret as t

User = t.Dict({
  t.Key("id"): t.Int,
  t.Key("name"): t.String,
  t.Key("role"): t.Int,
  t.Key("isBlocked"): t.Int,
  t.Key("createdAt"): t.String,
  t.Key("updatedAt"): t.String,
  t.Key("email"): t.Email,
  t.Key("avatar"): t.Dict({
    t.Key("default"): t.URL,
    t.Key("small"): t.URL
  }),
  t.Key("facebookId"): (t.String | t.Null),
  t.Key("twitterId"): (t.String | t.Null),
  t.Key("instagramId"): (t.String | t.Null),
  t.Key("businessName"): (t.String | t.Null),
  t.Key("practice"): (t.String | t.Null),
  t.Key("cover"): t.URL,
  t.Key("additionalInfo"): t.String(allow_blank=True),
  t.Key("stripeAccountId"): t.Null,
  t.Key("stripeFirstName"): t.Null,
  t.Key("stripeLastName"): t.Null,
  t.Key("subscriptionDate"): t.Null,
  t.Key("pushCount"): t.Int,
  t.Key("phone"): t.Null,
  t.Key("token"): t.String,
  t.Key("tokenExpiresAt"): t.String
})




