# Report findings
Hayden Coffing, h@ydencoffing.com, 702-339-0544

## Cleaning steps:
The data was encoded into a pdf. It seemed like the data was in some sort of scrollable window but I could not scroll 
through all of it. I thought there was something hidden, that I just couldnt see.
After some investigation into the pdf standard, I exported the given file as a raw text file and,
to my dismay, discovered the data is indeed truncated. Assured I was indeed seeing all the data I could, I began cleaning.

I immediately noticed a few things. For one, there were not a column name for all of the data points in each line of the csv.

For example:
>"Masala Chai Mix (12oz)",9.99,beverages,18,15,2024-11-18,Spice W

Has two extra elements, `2024-11-18` and `Spice W`
I made the assumption that the date is the date of last restock, and the text is the name of the company who makes the product.
So, with that assumption I added in column names `last_restock` and `product_brand`. 

I then did some general sanitzations, like filling empty cells with 0, or n/a where appropriate. I then stripped numbers
like prices of extraneous dollar signs. I replaced the string `out of stock` with 0 to enforce numerical values in the
`current_stock` column. I then changed all the text in the `category` column to be lowercase, to avoid unwanted separation of values
like `Beverages` and `beverages`. It is assumed that they both belong to the same category. 
Lastly, I changed all dates to be formatted YYYY-MM-DD format according to ISO 8601

## Note on quality of data:
It should be noted that the quality of the data is rather low. For an example, there is a category of product stored in the table 
that is titled `category` with elements in that category being: `beverages, coffee, tea`. Not to get engrossed in the semantics 
of what exactly constitues the differences between the categories, but I would prefer to see more specific descriptors, for example:
`Roobios Tea` is listed as a `beverage` when it could easily exist in the `tea` category. 







