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

## 📊 Exploratory Data Analysis

### Chart 1: Price Distribution of Amazon Electronics

![Price Distribution](outputs/charts/price_distribution.png)

**Plot Details:**
- Chart Type: Histogram (bins=50)
- Column: current/discounted_price
- Reference Lines: Mean ($168.52) and Median ($77.00)

**Distribution Type:**
Heavily Right Skewed (Positive Skew)

**Analysis:**
Majority of products concentrated in $0-$200 range 
with 28,000+ products in lowest price bin. Mean ($168.52) 
is significantly higher than Median ($77.00) with a gap 
of $91.52 caused by luxury products ($2,000-$4,500) 
pulling mean artificially rightward. Median better 
represents true center of data confirming correct 
decision to use median strategy for missing value imputation.

**Business Insights:**
- Amazon electronics catalog dominated by budget 
  to mid-range products ($0-$200)
- Three natural price clusters identified:
  Mass market ($0-$200) | Mid-premium ($200-$500) | Luxury ($500+)
- Premium segment ($1,000+) significantly underserved
  representing potential business opportunity
- Mean price ($168.52) is misleading — Median ($77.00) 
  better represents typical Amazon electronics price             

### Chart 1: Price Distribution of Amazon Electronics

![Price Distribution](outputs/charts/rating_distribution.png)

**Plot Details:**
- Chart Type: Histogram (bins=20)
- Column: rating
- Reference Lines: Mean (4.40) and Median (4.50)

**Distribution Type:**
Left Skewed

**Analysis:**
1.90% of the products are rated above 4.0 indicating that high customer satisfaction
2.14000+ reviews are positive(peak at 4.7)

**Business Insights:**
Implication for pricing:
 → Rating alone NOT enough differentiator
 → Need review_credibility score
   to distinguish truly trustworthy products!"

