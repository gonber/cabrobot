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
    When Alice waits for a response
    Then Alice reads: no available drivers found
