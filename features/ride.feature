Feature: Ride

  Scenario: Alice wants a ride
    Given users Alice
    When Alice writes: lat 0.0 lon 0.0
    Then Alice reads: do you want to ride or drive?
    When Alice writes: ride
    Then Alice reads: please share your target location
    When Alice writes: lat 1.0 lon 1.0
    Then Alice reads: looking for a driver

  Scenario: No nearby driver
    Given users Alice
    And Alice wants a ride
    And there are no nearby drivers
    Then Alice reads: no available drivers found

  Scenario: Alice accepts a driver
    Given users Alice,Bob
    And Bob is available to drive
    And Alice wants a ride
    Then Bob reads: request for a ride from:
    And Bob receives location
    And Bob reads: to:
    And Bob receives location
    And Bob reads: how much do you charge for it? (example answer: 25)
    When Bob writes: 10
    Then Alice reads: Bob will take you there for 10
    When Alice writes: accept
    Then Bob reads: Alice accepted your ride and is waiting for you. text her if needed

    Scenario: Alice rejects a driver
      Given users Alice,Bob
      And Bob is available to drive
      And Alice wants a ride
      Then Bob reads: request for a ride from:
      And Bob receives location
      And Bob reads: to:
      And Bob receives location
      And Bob reads: how much do you charge for it? (example answer: 25)
      When Bob writes: 10
      Then Alice reads: Bob will take you there for 10
      When Alice writes: reject
      Then nothing happens

    Scenario: Alice gets offered the lowest bid
      Given users Alice,Bob,Charlie
      And Bob is available to drive
      And Charlie is available to drive
      And Alice wants a ride
      When Bob bids: 10
      And Charlie bids: 5
      Then Alice reads: Charlie will take you there for 5
      When Alice writes: accept
      Then Charlie reads: Alice accepted your ride and is waiting for you. text her if needed

    Scenario: Alice gets offered the nearby driver
      Given users Alice,Bob,Charlie
      And Bob is available to drive at lat 0.0 lon 0.0
      And Charlie is available to drive at lat 45.0 lon 100.0
      And Alice wants a ride from lat 0.0 lon 0.0
      When Bob bids: 10
      Then Alice reads: Bob will take you there for 10
      When Alice writes: accept
      Then Bob reads: Alice accepted your ride and is waiting for you. text her if needed
