import constants
from flask import g, jsonify, request, session
from gaelib.auth import auth
from gaelib.auth.models import User, UserRole
from gaelib.env import dashboard_login_page



def auth_required(view_function):
  """
      Function to be used with as_view().
      Returns a decorator function which authenticates a request
      before the target view's dispatch_request() is invoked.
  """
  def decorator(*args, **kwargs):
    """
        Authenticates request before invoking dispatch_request
        of target view.
    """
    response_dict = {"success": 0}

    user_id, id_token, auth_type, is_dashboard_url = auth.get_user_id_and_token()

    if is_dashboard_url and not (user_id and id_token):
      return dashboard_login_page()

    if not user_id:
      response_dict["error_message"] = "UNAUTHORIZED USER"
      return jsonify(response_dict), 401

    if not id_token:
      response_dict["error_message"] = "UNAUTHORIZED TOKEN"
      return jsonify(response_dict), 401

    auth_ob = auth.Auth(id_token, user_id)
    error = ''
    # pragma pylint: disable=broad-except
    try:
      auth_result = auth_ob.authorize_request(auth_type=auth_type)
    except Exception as e:
      error = e
      auth_result = None

    if not auth_result:
      error = "Unauthorised login for web request found"
      if is_dashboard_url:
        g.app.logger.warning(error)
        session.pop("gae_uid", None)
        return dashboard_login_page()

      response_dict["error_message"] = str(error)
      return jsonify(response_dict), 401

    uid_filter = ('uid', '=', user_id)
    user = User.retrieve(filters=[uid_filter])[0]
    g.user_key = user.key().id
    return view_function(*args, **kwargs)

  # The following if block is required to avoid different
  # view functions getting mapped to the same endpoint name
  # when the view_function is a LazyView object.
  # We explicitly change the decorator name to the LazyView object's
  # view_function name.
  # This ensures there's no conflicting view function to end point mapping.
  # Note that if this is not done, then registering more than 1 url rules
  # to the same blueprint (say solo) will get the same endpoint name (solo.decorator)
  # which raises an exception.
  # Refer to
  # https://stackoverflow.com/questions/17256602/assertionerror-view-function-mapping-is-overwriting-an-existing-endpoint-functi
  # for further details
  if view_function.__class__.__name__ == "LazyView":
    decorator.__name__ = view_function.view_function
  return decorator


def access_control(role):
  def decorator_without_arg(view_func):
    def access_control_decorator(*args, **kwargs):
      response_dict = {"success": 0}
      user_id, _, _, _ = auth.get_user_id_and_token()

      uid_filter = ('uid', '=', user_id)

      try:
        user = User.retrieve(filters=[uid_filter])[0]
      except IndexError:
        user = None

      if user:
        if UserRole(user.role) is role:
          return view_func(*args, **kwargs)
        else:
          g.app.logger.error(
              "User %s does not have access to staff only ", str(user.__dict__))
      else:
        g.app.logger.error("Unauthorised access, user doesn't exist")

      response_dict["error_message"] = "UNAUTHORIZED ACCESS"
      return jsonify(response_dict), 200
    return access_control_decorator

  return decorator_without_arg
