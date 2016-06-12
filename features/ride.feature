Feature: Ride

  Scenario: Get a driver without target location
    Given Alice shared current location
     When Alice asks for a ride
     And Alice does not share target location
     Then Alice gets Bob contact

  Scenario: Get a driver with target location
    Given Diane shared current location
     When Diane asks for a ride
     And Diane shares target location
     Then Diane gets the contact for the lowest bidding nearby driver

   Scenario: No nearby driver
     Given Alice shared current location
      When Alice asks for a ride
      And there are no nearby drivers
      Then Alice ride is rejected

  Scenario: Accept driver proposal
    Given Alice received Bob's contact
     When Alice accepts the proposal
     Then Bob receives the go signal
     And Alice is asked to wait for Bob

  Scenario: Reject driver proposal
     Given Alice received Bob contact
      When Alice rejects the proposal
      Then Alice gets the contact for the next available driver
