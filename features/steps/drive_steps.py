from behave import given, when, then, step


@given(u'Bob shared current location')
def step_impl(context):
    context.bob.location(0., 0.)

@when(u'Bob offers to drive')
def step_impl(context):
    context.bob.reads('do you want to ride or drive?') \
               .writes('drive')

@then(u'Bob is flagged as available')
def step_impl(context):
    context.bob.reads('you are now available')

@given(u'Bob is flagged as available')
def step_impl(context):
    context.bob.location(0., 0.) \
               .writes('drive') \
               .reads('you are now available')

@when(u'Bob is inactive for a certain period')
def step_impl(context):
    context.bob.wait_new_message()

@then(u'Bob is asked to renew availability')
def step_impl(context):
    context.bob.reads('are you still available to drive?')
