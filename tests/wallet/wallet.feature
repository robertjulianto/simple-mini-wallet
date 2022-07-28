Feature: Wallet

  Background:
    Given I have customer id

  Scenario: Create Wallet
    When I create wallet

    Then Wallet is created
    And Initial wallet status is disabled
    And I get token
    And Creating wallet is success

  Scenario: Enable Wallet
    Given I have disabled wallet

    When I enable wallet

    Then Wallet status is enabled
    And Owner is me
    And Enabling wallet is success

  Scenario: Enable Enabled Wallet
    Given I have enabled wallet

    When I enable enabled wallet

    Then I get error that wallet is already enabled

  Scenario: View Wallet
    Given I have enabled wallet

    When I view wallet

    Then Wallet is returned
    And Owner is me
    And Viewing wallet is success

  Scenario: Disable Wallet
    Given I have enabled wallet
    And I have balance 0

    When I disable wallet

    Then Wallet status is disabled
    And Owner is me
    And Balance is 0
    And Disabling wallet is success

  Scenario: Disable Disabled Wallet
    Given I have disabled wallet

    When I disable disabled wallet

    Then I get error that wallet is already disabled

  Scenario: View Disabled Wallet
    Given I have disabled wallet

    When I view disabled wallet

    Then I get error that wallet is already disabled

