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

@given(u'{user} is available to drive')
def step_impl(context, user):
    context.test_users[user].location(0., 0.) \
                            .writes('drive')

@given(u'{user} wants a ride')
def step_impl(context, user):
    context.test_users[user].location(0., 0.) \
                            .writes('ride') \
                            .location(1., 1.)

@when(u'{user} is inactive')
def step_impl(context, user):
    context.test_users[user].wait_new_message()

@when(u'{user} waits for a response')
def step_impl(context, user):
    context.test_users[user].wait_new_message()

@given(u'there are no nearby drivers')
def step_impl(context):
    pass
