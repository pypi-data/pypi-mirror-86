from gaelib.view.base_view import BaseHttpHandler
from gaelib.auth.models import User, UserRole
from gaelib.auth import auth
from gaelib.env import get_app_or_default_prop
from flask import g, request, session



# pragma pylint: disable=too-few-public-methods


class Login(BaseHttpHandler):
  """
      The Login view function to sign in a user based on id_token.
      Creates a new User in datastore if user doesn't exist already.
  """

  def dispatch_request(self):
    """
        Process and dispatch response for request to Base-URL/login/
    """
    g.app.logger.debug("In Login View dispatch_request")
    user_id, id_token, auth_type, _ = auth.get_user_id_and_token()

    if not user_id:
      return self.json_error("NO USER_ID", 400)

    if not id_token:
      return self.json_error("NO_ID_TOKEN", 400)

    # Make auth object
    auth_ob = auth.Auth(id_token=id_token)

    # pragma pylint: disable=broad-except
    # Verify the id_token with Firebase
    try:
      claims = auth_ob.authorize_login_request(auth_type=auth_type)
    except Exception as e:
      return self.json_error(
          "UNAUTHORIZED_TOKEN" + str(e), 401, "Unauthorised login attempt:")

    # Check if id_token has been authorised
    # if claims is None, Unauthorised
    if not claims:
      return self.json_error("EMPTY_CLAIM", 401, "Unauthorised login attempt:")

    g.app.logger.info("Signing in with claims %s" % str(claims))

    if request.json:
      device_token_data = request.json.get('device_token', {})
    else:
      device_token_data = {}

    user = check_for_new_user(auth_ob.user_id, claims, auth_type, device_token_data, g.app.logger)

    session["gae_uid"] = user_id
    session["gae_token"] = id_token
    
    auth.login_callback(user)
    if auth_type == 'firebase':
      provider = claims.get('firebase').get('sign_in_provider')
    elif auth_type == 'auth0':
      provider = 'apple' if 'apple' in user.uid else 'google'


    response_dict = {"id": user.key().id,
                     "uId": user.uid,
                     "email": user.email,
                     "name": user.name,
                     "picture": user.picture,
                     "provider": provider,
                     }
    return self.json_success(response_dict, 202)



def check_for_new_user(user_id, claims, auth_type, device_token_data, logger):
  """
      checks if user with email exists in datastore.
      If exists, return games_played, games_won,
      Else, add to datastore
      with attributes
      user_id, email, games_played, games_won, join_date
  """

  logger.info("Checking if " + user_id + " is a new user")

  uid_filter = ('uid', '=', user_id)

  try:
    user = User.retrieve(filters=[uid_filter])[0]
  except IndexError:
    user = None
  except Exception as e:
    logger.info("Error trying to retrieve User %s", e)

  if not user:
    # Checking for user being an old cryptic cup member
    # from migration. This is not code that should be in
    # the library long term
    email_filter = ('email', '=', claims['email'])
    filters = [email_filter]

    ######
    #TODO: Handle multiple users
    ####
    try:
      user = User.retrieve(filters=filters)[0]
    except IndexError:
      user = None

  name = claims.get('name', '')
  if not name:
    email = claims['email']
    name = email[:email.find('@')]

  picture = claims.get('picture', get_app_or_default_prop('DEFAULT_PROFILE_IMAGE'))
  if user:
    user.update(
        uid=user_id,
        picture=picture,
        name=name,
        role=UserRole.DEFAULT.value
    )
  else:
    logger.info("Creating new user")
    logger.debug("\tUser ID: " + user_id)
    user = User(
        uid=user_id,
        email=claims['email'],
        picture=picture,
        name=name,
        role=UserRole.DEFAULT.value
    )
  if device_token_data:
    user.update(
      os=device_token_data.get('os'),
      device_token=device_token_data.get('token')
      )

  user.put()
  return user

