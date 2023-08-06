# Flask-URLSigning

A flask extension to sign and verify signed urls.

Flask-URLSigning leverages `bcrypt` package and an API equivalent to Flask's
`url_for` utility function for generating cryptographically signed urls for
your application.

This is specially useful for off-the-record email verification, for example:

    * Password recovery
    * User registration

Or otherwise any situation where you need to ensure integrity of a given url.

## Usage

In the example bellow, `/target` is only accessible via a redirect from
`/signed-redirect`. Attempting to access `/target` directly, or otherwise tamper
with the redirect url will result in a `403`.

```python
from flask import Flask, redirect
from flask_urlsigning import signed_url_for, verify_signed_url

app = Flask(__name__)
app.debug = True
app.secret_key = 'test-key'

@app.route('/target')
def target():
    if verify_signed_url():
        return '', 200
    return '', 403

@app.route('/signed-redirect')
def signed_redirect():
    return redirect(signed_url_for('target'))
```

### Sign Up flow

The snippet bellow should help you setup a verification link to be sent via
email.

```python
from flask import Flask, redirect, render_template
from flask_urlsigning import signed_url_for, verify_signed_url

app = Flask(__name__)
app.debug = True
app.secret_key = 'test-key'

@app.route('/sign-up')
def sign_up():
    if not verify_signed_url():
        form = SignUpEmailForm()
        if not form.validate_on_submit():
            ## Step 1. Provide an email
            return render_template('sign-up-enter-email.html', form=form)

        ## Step 2. Send continuation link
        continue_url = signed_url_for('sign_up', email=form.email.data)
        # @TODO: send an email message with the continue_url
        return render_template('sign-up-check-inbox.html')

    form = SignUpPasswordForm()
    email = request.args['email']
    if not form.validate_on_submit():
        ## Step 3. Provide a password
        return render_template('auth/sign-up-password.html', form=form)

    ## Step 4. Registration complete
    # @TODO: set user session, save user, etc..
    return 'Congrats'
```
