# Data for demo

Only customers for whom at hits are predicted for coupons from at least 3 categories are taken into account.

`customers_categories.csv` - mapping of customers to their 'hit' categories, ordered by total number of hit coupons for a customer, descending

`customers_coupons_categories.csv` - mapping of customers to 'hit' coupons and 'hit' categories, ordered as above

`cust_coup_cat_details.csv` - the same item set as `customers_coupon_categories.csv`, but with all details necessary to generate json payload
