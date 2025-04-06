# hollandsenieuwe-verbruik

Using python I created a (messy) script that based on your hollandsenieuwe receipts will generate graphs (currently including per weekday and per month). 

## How to Use:

Place Hollandse Nieuwe or mayby even other receipts from providers in the source\_files folder. Hollandse Nieuwe named my files \_blob\_hollandsnieuwe-factuur-\*\*\*customernumber\*\*\*250106.pdf

The file does not need to follow the whole format. As long as it ends with the year in 2 decimals followed by the month and date. 

## Example of output:

![example images](https://github.com/101br03k/hollandsenieuwe-verbruik/blob/main/images/example_image.png)

## To Do:

*   Integrate sms (waiting for the 7th day of month 4 to get my new receipt with 1 sms to see what regex I should use). 
*   Report over multiple years
*   Stacked bar report \*everything\*?