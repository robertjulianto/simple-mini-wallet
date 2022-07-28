Feature: Transaction

  Background:
    Given I have customer id

  Scenario: Deposit money
    Given I have enabled wallet
    And Deposit amount is 1.000.000
    And Reference id is DUMMY_DEPOSIT_REF_ID
    And Deposit time is now

    When I deposit money

    Then Transaction is created
    And Transaction type is deposit
    And Transaction status is success
    And Deposit by me
    And Amount is 1.000.000
    And Reference id is DUMMY_DEPOSIT_REF_ID
    And Deposit money is success

  Scenario Outline: Withdraw money
    Given I have enabled wallet
    And I have balance <balance_amount>
    And Withdraw amount is <withdraw_amount>
    And Reference id is DUMMY_WITHDRAW_REF_ID
    And Withdraw time is now

    When I withdraw money

    Then Transaction is created
    And Transaction type is withdraw
    And Transaction status is <transaction_status>
    And Withdraw by me
    And Amount is <withdraw_amount>
    And Reference id is DUMMY_WITHDRAW_REF_ID
    And Withdraw money is success

    Examples:
      | balance_amount | withdraw_amount | transaction_status |
      | 2.000.000      | 1.000.000       | success            |
      | 1.000.000      | 1.000.000       | success            |
      | 500.000        | 1.000.000       | fail               |

  Scenario: Deposit money into disabled wallet
    Given I have enabled wallet
    And Deposit amount is 1.000.000
    And Reference id is DUMMY_DEPOSIT_REF_ID
    And Deposit time is now
    And My wallet is disabled

    When I deposit money into disabled wallet

    Then I get error that wallet is already disabled

  Scenario Outline: Withdraw money into disabled wallet
    Given I have enabled wallet
    And I have balance <balance_amount>
    And Withdraw amount is <withdraw_amount>
    And Reference id is DUMMY_WITHDRAW_REF_ID
    And Withdraw time is now
    And My wallet is disabled

    When I withdraw money into disabled wallet

    Then I get error that wallet is already disabled

    Examples:
      | balance_amount | withdraw_amount |
      | 2.000.000      | 1.000.000       |
      | 1.000.000      | 1.000.000       |
      | 500.000        | 1.000.000       |
