# /* -------------- *\
#       api.user
# \* -------------- */

api_login = '/api-login'
"""
:var username
:var password
find user then match password
:return jwt({username: username}), user, roles
"""
get_user = '/get-user'
"""
:var token
if token == user.username:
:return user
"""
login = '/login'
"""
:var ...
:return user, ...
"""
logout = '/logout'
"""
:var token
if token == user.username:
del redis[token]
"""
global_get = '/user-details/{id}'
global_update = '/{id}/update-user'


# /* -------------- *\
#       api.biker
# \* -------------- */


save_location = '/save-location'
"""
:var lat
:var longt

"""
trips = '/trips'
"""
:var status
:var allTrips
:var currentPage
:return trips
"""
update_status = '/update-status'
"""
:var tripId
:var status
"""
update_user_status = '/update-user-status'
"""
:var bikerId
:var status
"""
has_problem = '/has-problem'
"""
:go to update_user_status
"""

""" *** """


# /* --------------- *\
#  api.trip_suggestion
# \* --------------- */


trip_suggestions = '/trip-suggestion/{id}?'


# /* --------------- *\
#      api.device
# \* --------------- */


register = '/register'
"""
:var client
:var UDID
:var ...
"""

push_zoodfood_vendors = '/pushZoodfoodVendor'
"""
:var ...
"""


# /* --------------- *\
#     api.loginext
# \* --------------- */


_order_action = ['/accept', '/reject', '/picked-up', '/delivered']
"""
:var clientShipmentId
:var deliveryMediumName
"""

# /* --------------- *\
#     biker.biker
# \* --------------- */

"""
    /all-bikers,
    /deleteUserBikerNotification,
    /biker-log,
    /biker-history,
    /details,
    /activated-bikers,
    /deactivated-bikers,
    /bikers-to-assign,
    /result,
    /result1,
    /pot-disconnected-bikers,
    /food-not-picked-bikers,
    /show-bikers-list,
    /show-bikers,
    /new-show-bikers,
"""