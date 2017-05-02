User and authentication service

# Flow

Create user by posting to `/user`:

```
POST /user -d '
{
    "username": "Jim",
    "password": "123",
    "email": "jim@example.com"
}'
```

Get an access token from `/auth`:

```
POST /auth -d '
{
    "username": "Jim",
    "password": "123"
}
Response:
{
    "access_token": "blahblah.foo.bar"
}
```

Confirm authentication:

```
GET -H "Authorization: JWT blahblah.foo.bar" /auth/status
Response:
{
  "version": "1.0",
  "status": 200,
  "username": "Jim"
}
```

Done!
