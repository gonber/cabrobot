Feature: Drive

  Scenario: Bob wants to drive
    Given users Bob
    When Bob writes: lat 0.0 lon 0.0
    Then Bob reads: do you want to ride or drive?
    When Bob writes: drive
    Then Bob reads: you are now available

  Scenario: Renew after availability ping
    Given users Bob
    And Bob is available to drive
    When Bob is inactive
    Then Bob reads: are you still available to drive?
    When Bob writes: yes
    Then Bob reads: ok

  Scenario: Timeout after availability ping
    Given users Bob
    And Bob is available to drive
    When Bob is inactive
    Then Bob reads: are you still available to drive?
    When Bob writes: no
    Then nothing happens
