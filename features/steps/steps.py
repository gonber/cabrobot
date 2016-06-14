from behave import given, when, then, step
from time import sleep
from environment import TestUser


@given(u'users {users}')
def step_impl(context, users):
    users = users.split(',')
    user_id = 101
    for user in users:
        context.test_users[user] = TestUser(context, user, user_id)
        user_id = user_id + 1

@when(u'{user} writes: lat {lat:f} lon {lon:f}')
def step_impl(context, user, lat, lon):
    context.test_users[user].location(lat, lon)

@when(u'{user} writes: {text}')
def step_impl(context, user, text):
    context.test_users[user].writes(text)

@then(u'{user} reads: {text}')
def step_impl(context, user, text):
    context.test_users[user].reads(text)

@then(u'{user} receives location')
def step_impl(context, user):
    context.test_users[user].receives_location()

@given(u'{user} is available to drive')
def step_impl(context, user):
    context.test_users[user].location(0., 0.) \
                            .reads('do you want to ride or drive?') \
                            .writes('drive') \
                            .reads('you are now available')

@when(u'{user} bids: {ammount:d}')
def step_impl(context, user, ammount):
    context.test_users[user].reads('request for a ride from:') \
                            .receives_location() \
                            .reads('to:') \
                            .receives_location() \
                            .reads('how much do you charge for it? (example answer: 25)') \
                            .writes(ammount)

@given(u'{user} wants a ride')
def step_impl(context, user):
    context.test_users[user].location(0., 0.) \
                            .reads('do you want to ride or drive?') \
                            .writes('ride') \
                            .reads('please share your target location') \
                            .location(1., 1.) \
                            .reads('looking for a driver')

@when(u'{user} is inactive')
def step_impl(context, user):
    pass

@given(u'there are no nearby drivers')
def step_impl(context):
    pass

@then(u'nothing happens')
def step_impl(context):
    pass
