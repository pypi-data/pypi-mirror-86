from datetime import datetime, timedelta
from functools import wraps
from uuid import uuid4
from biscuits import parse, Cookie
from itsdangerous import TimestampSigner
import itsdangerous.exc

from .prototypes import Session


class SignedCookieManager:

    session = Session

    def __init__(self, secret, store, cookie='sid'):
        self.store = store
        self.delta = store.delta  # lifespan delta in seconds.
        self.cookie_name = cookie
        self.signer = TimestampSigner(secret)

    def generate_id(self):
        return str(uuid4())

    def refresh_id(self, sid):
        return str(self.signer.sign(sid), 'utf-8')

    def verify_id(self, ssid):
        return self.signer.unsign(ssid, max_age=self.delta)

    def get_session(self, cookie):
        new, sid = self.get_id(cookie)
        return self.session(sid, self.store, new=new)

    def get_id(self, cookie):
        if cookie is not None:
            morsels = parse(cookie)
            signed_sid = morsels.get(self.cookie_name)
            if signed_sid is not None:
                try:
                    sid = self.verify_id(signed_sid)
                    return False, str(sid, 'utf-8')
                except itsdangerous.exc.SignatureExpired:
                    # Session expired. We generate a new one.
                    pass
        return True, self.generate_id()

    def cookie(self, sid, path="/", domain="localhost"):
        """We enforce the expiration.
        """
        # Refresh the signature on the sid.
        ssid = self.refresh_id(sid)

        # Generate the expiration date using the delta
        expires = datetime.now() + timedelta(seconds=self.delta)

        # Create the cookie containing the ssid.
        cookie = Cookie(
            name=self.cookie_name, value=ssid, path=path,
            domain=domain, expires=expires)

        value = str(cookie)

        # Check value
        if len(value) > 4093:  # 4096 - 3 bytes of overhead
            raise ValueError('The Cookie is over 4093 bytes.')

        return value


class WSGISessionManager:

    def __init__(self, manager, environ_key='session'):
        self.environ_key = environ_key
        self.manager = manager

    def __call__(self, app):

        @wraps(app)
        def session_wrapper(environ, start_response):

            def session_start_response(status, headers, exc_info=None):
                # Write down the session
                # This relies on the good use of the `save` method.
                session = environ[self.environ_key]
                session.persist()

                # Prepare the cookie
                path = environ['SCRIPT_NAME'] or '/'
                domain = environ['HTTP_HOST'].split(':', 1)[0]
                cookie = self.manager.cookie(session.sid, path, domain)

                # Write the cookie header
                headers.append(('Set-Cookie', cookie))

                # Return normally
                return start_response(status, headers, exc_info)

            session = self.manager.get_session(environ.get('HTTP_COOKIE'))
            environ[self.environ_key] = session
            return app(environ, session_start_response)

        return session_wrapper
