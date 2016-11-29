#@test2
#  Scenario: Test scenario verify account
#    Given I run sql script
#   """
#   context.token = SELECT token FROM confirms WHERE user_id = (SELECT id FROM users WHERE email = 'test@email.com');
#  """
#    When I make a GET request to "/v1/auth/confirm"
#    | PARAMETER_NAME | VALUE         |
#    | token          | context.token |
#    Then the response status code should equal 200

#  @test3
#  Scenario: Test scenario login
#    Given I add request body
#     """
#     {
#        "email": "test@email.com",
#        "password": "string"
#     }
#     """
#    When I make a POST request to "/v1/auth/local"
#    Then the response status code should equal 200
#    And the response structure should equal "SessionStartBodyResponse"
#    And JSON at path "payload.email" should equal "test@email.com"
#    And JSON at path "payload.status" should equal 1
#   And JSON value at path "payload.token" I save as "context.token"
#
#  | PARAMETER_NAME | VALUE |
#  | limit          | 10    |
#  | offset         | 20    |
# Scenario: Partner creates user. Positive scenario
#    Given I run sql script
#    """
#      DELETE FROM zc_user WHERE email = 'partner_user222@ukr.net';
#    """
#     And I add request body
#    """
#        {
#        "email": "partner_user222@ukr.net",
#        "partner_user_id": "user_id_3",
#        "phone": "0631231258",
#        "firstName": "Partner_autotest_user",
#        "nickname": "carnaval",
#        "lastName": "Ososososs",
#        "location": "Ukraine",
#        "bday_day": 26,
#        "bday_month": 1,
#        "bday_year": 1989,
#        "gender": 1,
#        "address_1": "Mira av, Dnipro",
#        "state": "NY",
#        "city": "NY",
#        "zip_code": "10008"
#        }
#    """
#    And I set "x-api-key" header to "test_qa"
#    And I set "x-api-version" header to "2"
#    And I set "Content-Type" header to "application/json"
#    When I make a POST request to "/users"
#    Then the response status code should equal 200
#    And the response structure should equal "User"
#    And JSON at path ".email" should equal "partner_user222@ukr.net"
#    And JSON at path ".partner_user_id" should equal "user_id_3"
#    And JSON at path ".phone" should equal "0631231258"
#    And JSON at path ".firstName" should equal "Partner_autotest_user"
#    And JSON at path ".nickname" should equal "carnaval"
#    And JSON at path ".lastName" should equal "Ososososs"
#    And JSON at path ".active" should equal "1"
#    And JSON at path ".location" should equal "Ukraine"
#    And JSON at path ".bday_day" should equal "26"
#    And JSON at path ".bday_month" should equal "1"
#    And JSON at path ".bday_year" should equal "1989"
#    And JSON at path ".address_1" should equal "Mira av, Dnipro"
#    And JSON at path ".state" should equal "NY"
#    And JSON at path ".city" should equal "NY"
#    And JSON at path ".zip_code" should equal "10008"
#    When I make a POST request to "/signup/basic/context.id/company/context.id"