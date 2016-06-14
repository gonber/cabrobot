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

  @wip
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
