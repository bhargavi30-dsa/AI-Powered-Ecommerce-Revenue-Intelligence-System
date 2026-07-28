# Ecommerce-Revenue-Intelligence
AI-Powered dynamic pricing intelligence system for ecommerce
# Findings after feature construction
"Revenue Leakage Analysis:
→ 50% of products have zero revenue leakage
→ 25% of products lose more than 21% revenue
→ Maximum leakage of 93.7% detected
   (product selling at nearly zero profit!)
→ Average revenue leakage: 14.28%
→ High std (22.57%) suggests inconsistent
  discounting strategy across catalog"

  "Premium Pricing Analysis:
→ 56.7% products flagged as premium priced
→ CAUTION: listed_price had 72% missing values
  filled with median → may inflate premium flag
→ Reliable premium detection only possible
  with complete listed_price data
→ Recommend collecting actual listed prices
  for accurate premium detection"

 #Business interpretation scale for price_vs_avg extra added feature:
 price_vs_avg < 0.5  → Deep budget
                       (less than half of average!)

price_vs_avg 0.5-0.8 → Budget
                        (below average)

price_vs_avg 0.8-1.2 → Mid market
                        (around average ±20%)

price_vs_avg 1.2-2.0 → Premium
                        (above average)

price_vs_avg > 2.0   → Luxury/Ultra premium
                        (more than 2x average!)

#Why price_vs_avg is more powerful than price_category:
price_category:
Product A ($15) → "Budget"
Product B ($24) → "Budget"
→ Both look same! No differentiation!

price_vs_avg:
Product A ($15) → 0.19 (very budget!)
Product B ($24) → 0.31 (less budget!)
→ Shows HOW budget each product is!
→ More precise for ML model!
Example from dataset:
- USB Cable ($9.99): 0.13 → Deep budget
- Wireless Mic ($89.68): 1.16 → Upper mid
- DJI Mic ($314): 4.07 → Luxury tier  

Added Review Credibility Score feature through logarithmic scaling:
Formula: rating × log(number_of_reviews + 1)

Why log?
→ Prevents large review counts from
  dominating the score unfairly
→ 100K reviews is not 10,000x better
  than 10 reviews in terms of credibility!
→ Logarithmic scaling = fair comparison!

Why +1?
→ Prevents log(0) error
→ Products with 0 reviews get score of 0

Interpretation:
Low score  → either low rating OR few reviews
High score → high rating AND many reviews
             = most trustworthy product!

