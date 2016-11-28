Feature: Test
  # Create user


  @test_01
  Scenario: Partner creates user. Positive scenario
   When I add request body
   """
    {
      "id": 47,
      "title": "Cultural",
      "createdAt": "",
      "updatedAt": "",
      "icon": "http://redmine.cleveroad.com:3790/images/category-icons/ic_cultural.png",
      "subCategories": [
        {
          "id": "125",
          "title": "Music shows",
          "createdAt": "2016-11-02T15:01:39.000",
          "updatedAt": "2016-11-02T15:01:39.000",
          "categoryId": 47
        },
        {
          "id": "context.member_id_payment",
          "title": "Music shows",
          "createdAt": "2016-11-02T15:01:39.000",
          "updatedAt": "2016-11-02T15:01:39.000",
          "categoryId": 47
        }
      ]
    }
    """






