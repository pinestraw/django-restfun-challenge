# Django Restfun Challenage

An RESTful django development challenge for managing a small coffee shop

## Introduction 
In this challenge I created an API Restful using Django Rest Framework.
With this challenge any interface can be created using JSON return from designed services.

1 - In restfun, the manager can define variety of products via admin panel. 
2 - Customers are able to order and customize their coffee with several options. 
3 - Order can have a status: waiting, preparation, ready, delivered. 
4 - Manager can chagne orders status. After each status change on order, you should notify the customer via email.

For 1st the manager should follow instructions below to manage any product.
- The entity Product contains product description and a base price.
- Attributes like SIZE / KIND ...  can be added to Product by creating relations 
between Options from Attribute and Product - OptionAttributeProduct -> Product
- On any OptionAttributeProduct the manager can define price adjust by percentual.
For example: Price: 10.0 * PriceOption: 1.1 = Price plus 10% = 11.0

Here is sample catalog of products offered by restfun:

Product > Customization Option

- Latte >	Milk: skim, semi, whole
- Cappuccino > Size: small, medium, large
- Espresso > Shots: single, double, triple
- Tea
- Hot chocolate > Size: small, medium, large
- Cookie > Kind: chocolate chip, ginger
- All > Consume location: take away, in shop

The following services are provided by REST APIs:

- View Menu (list of products) (GET /api/v1/product)
- Order at coffee shop with options (POST /api/v1/order)
- View his order (product list, pricing & order status) (GET /api/v1/order)
- Change a waiting order (PUT /api/v1/order)
- Cancel a waiting order ( Delete order on Waiting status ) (DELETE /api/v1/order)

On any endpoint a token should be provided for authentication

## Tests

- Unit tests were created to cover API endpoints defined on product description.
- To run: python manage.py test --keepdb

## Code version

Python: 3.6
Django: 2.2.17
Django Rest Framework: 3.12.2