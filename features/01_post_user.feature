Feature: Create user
  # Create user


  @test_01
  Scenario: Create user. Positive scenario
   Given I run sql script
    """
    DELETE FROM users WHERE name = 'Petushara222';
    """
   And I set "Content-type" header to "application/json"
    And I add request body
    """
    {
      "email": "qqqqqq@aaa.zzz",
      "password": "qwerty11",
      "confirmPassword": "qwerty11",
      "name": "Petushara222"
    }
    """
   When I make a POST request to "/signup/basic"
   Then the response status code should equal 200
   And the response structure should equal "User"
   And JSON at path ".name" should equal "Petushara222"
   And JSON at path ".role" should equal 1
   And JSON at path ".email" should equal "qqqqqq@aaa.zzz"
   And JSON at path ".avatar.default" should equal "http://redmine.cleveroad.com:7777/resources/img/default.png"
   And JSON at path ".facebookId" should equal null
   And JSON value at path ".token" I save as "context.token"
    
  Scenario: Get professionals
    Given I set "Authorization" header to "context.token"
    And I set "Accept" header to "application/json"
    When I make a GET request to "/professionals"
    | PARAMETER_NAME | VALUE         |
    | distance       | 5             |





