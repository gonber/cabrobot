Feature: Arrange a drive

  Scenario: Set location and availability to drive
    Given Bob shared current location
     When Bob offers to drive
     Then Bob is flagged as available

   Scenario: Reset availability to drive
     Given Bob is flagged as available
      When Bob withdraws availability
      Then Bob is flagged as unavailable

  Scenario: Availability ping
    Given Bob is flagged as available
     When Bob is inactive for a certain period
     Then Bob is asked to renew availability

  Scenario: Renew availability
    Given Bob is asked to renew availability
     When Bob renews availability
     Then Bob availability does not change

  Scenario: Renew availability with new location
    Given Bob is asked to renew availability
     When Bob shares new location
     Then Bob current location is updated
     And Bob availability does not change

  Scenario: Renew availability timeout
    Given Bob is asked to renew availability
     When Bob does not react for a certain period
     Then Bob is flagged as unavailable

  Scenario: Driver needed notification without destination
    Given Bob is flagged as available
     When a nearby rider asks for a ride without destination
     Then Bob is asked to drive without knowing destination

  Scenario: Accept driving without destination
    Given Bob is asked to drive without knowing destination
     When Bob accepts to drive without knowing destination
     And Alice accepts the proposal
     Then Bob receives the go signal

  Scenario: Driver needed notification with destination
    Given Bob is flagged as available
     When a nearby rider asks for a ride with destination
     Then Bob is asked to bid for the ride

  Scenario: Lowest bidder for a ride
    Given Bob is asked to bid for a ride
     When Bob bids for a ride
     And Bob is lowest bidder
     And Alice accepts the proposal
     Then Bob receives the go signal
