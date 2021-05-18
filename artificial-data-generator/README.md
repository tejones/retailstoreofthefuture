# Data generator

This generator can generate transaction data for predicting the probability of coupon usage by the given customer.

It makes a few assumptions for that purpose:
1. Men use coupons with the probability of p=0.8 and women with p=0.9
1. Women buy products from the end of the products list* more often
1. Men buy products from the beginning of the product list* more often
1. People in the age up to 35 buys products from the beginning to 1/3 of the list* more often,
1. People in the age 36-60 buys products from 1/3 to 2/3 of the list* more often,
1. People in the age 61 and above buys products from the 2/3 to the end of the list* more often,
1. The customer has personal preferences which can change the probability of buying products by up to 40% (20% on average) in 20% of cases.


> *There are actually 3 lists - vendors, departments, and categories. The order in all lists is random but always the same for all generated customers. Every customer has his/her  own list of preferences for all 3 types. All lists are generated the same way and using the same assumptions described above.

All numbers and functions described above can be changed using the config.py file.

## The algorithm

Here's an approximate algorithm of the generator. For more details please check the code.

1. Generate customers
1. Generate products
1. Generate inventory (number of items)
1. Generate customer preferences. For each list: departments, vendors, categories create a preferences list:
   1. create a list of random numbers (length = number of products). ~80% of them will be equal to 0.8. The rest should be random with the even distribution of numbers from 0.6 to 1.0 (personal preferences),
   1. map elements: multiply every element by the gender function result for the element's position in the list. If X is the number on the list and I is its index on the list, then the final number is X*gender_function(I)
   1. map new elements: multiply each number by age function: X*age_function(I)
   1. normalize the list - scale the list so the sum of all elements is 1, and the proportions between numbers are the same. In other words, divide all elements by the sum.
   1. the new list describes the client's probability of buying a product from a particular department/vendor/category
1. Generate coupons
   * The algorithm makes sure that there are 3 (configurable) coupons/day for each of the departments
1. Generate orders
   1. For dates in a given range, for every hour when the shop is opened, for each customer get the probability of her/him entering the shop,
   1. Pick a number <0.0, 1.0> - if this number is < then the probability, the customers enters the store,
   1. Create a transaction: get X products (where X is random) but consider customer's preferences. Select a vendor, then the department, and then the category.
   1. If there's a coupon for the product, there's a high chance of using it (95%).
   1. If there's no coupon, the customer checks if there's a similar product with the coupon. If there is, it buys a similar product.

## Usage

```
python3 generate.py 
```

optional arguments:

```
-h,             --help
                      show this help message and exit
-c CUSTOMERS,   --customers CUSTOMERS
                      number of customers
-d DEPARTMENTS, --departments DEPARTMENTS
                      number of departments
-p PRODUCTS,    --products PRODUCTS
                      number of products
-C COUPONS,     --coupons COUPONS
                      number of coupons
-S START,       --start START
                      start date
-E END,         --end END
                      end date
-D DAYS,        --days DAYS 
                      number of days if end not set
-P PATH,        --path PATH
                      path where to generate a files
-v,             --verbose    
                      verbose
```
