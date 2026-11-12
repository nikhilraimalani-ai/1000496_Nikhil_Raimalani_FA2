# SustainStyle: Eco-App in Action

**Scan a clothing tag, see its real environmental impact, swap to something cheaper and greener, and earn GreenPoints.**

Live app: **add your Streamlit link here** · Design document: [FA-1 submission](docs/FA1_Submission.docx)
· Course: Critical and Creative Thinking (CRS), Formative Assessment 2



## What the app does
SustainStyle is a mobile-first web app for shoppers who want to buy better clothes without paying more. The shopper scans a barcode or care label and gets an instant 0 to 100 eco-score with an A to E grade, a traffic-light verdict and a breakdown by materials, carbon, water and labour. If the item scores badly, the app suggests second-hand, repair or organic options that score higher, and shows how much money, water and CO₂ each swap saves. Every scan, swap and skipped purchase earns GreenPoints, which build streaks, levels and badges and can be spent on vouchers.

## How this connects to FA-1
This app is the working prototype of the concept designed in [FA-1](docs/FA1_Submission.docx) (research report, SCAMPER ideation, six-screen storyboard). FA-1 found that people say they want to shop sustainably, but price, not being able to identify sustainable items, and doubts about green claims get in the way. The app goal from FA-1: *a user-friendly mobile app that gives an instant item-level eco-score and a cheaper, greener alternative at the moment of buying, and rewards better choices with GreenPoints.*

| FA-1 insight | Design decision | Where in the app |
|---|---|---|
| **I1** Price is the top barrier (41%) | Cheaper and greener options first: second-hand and repair; "Cheaper", "In budget" filters and a budget setting | Greener alternatives screen |
| **I2** 27% cannot tell which items are sustainable | Score the exact item, not the brand. Barcode, manual entry and camera input. Guest mode, no sign-up | Home, Scan |
| **I3** Good intentions do not turn into action | Instant result, GreenPoints, streaks, a 30-wear challenge, vouchers (including a repair voucher) | Reward and Impact screens |
| **I4** Trust in green claims is shaky | Visible weights, per-factor reasons, a data-confidence label and "How is this calculated?" | Eco-Score result |

### FA-1 storyboard to the built screens
| FA-1 screen | Built as | Status |
|---|---|---|
| 1 Home | Home: points hero, scan button, guest mode, impact tiles | Built |
| 2 Scan | Scan: barcode, type-it and camera input | Built, recognition simulated |
| 3 Eco-Score | Result: score ring, grade, traffic light, factor bars, data confidence | Built |
| 4 Swaps | Greener alternatives with filters and Pause and Skip | Built |
| 5 Reward | Great choice: points, savings, level-up, streak, share text | Built |
| 6 My Impact | Impact: levels, weekly chart, streak, challenge, badges, rewards, community | Built |
| Customize | Profile → Settings: name, budget, larger text | Partly built (see below) |

### What the prototype does not do (limits)
- **Scanning is simulated.** The sample items are matched by barcode from a built-in catalogue. The camera photo is not analysed; it uses the selected sample item.
- **Data is illustrative.** The 22 products and their carbon, water and labour figures are made up for the demo. A live version would use brand disclosures and certification databases.
- **"AI recommendations" are rule-based.** Alternatives are the items in the same category with a higher score, ranked by price and score. There is no machine-learning model.
- **Language, size and style personalisation from FA-1 are not built.** Budget and accessibility (larger text) are.
- **No accounts or storage.** Progress lives in the browser session and resets on refresh.
- **Sample starting data.** The app opens with sample points, history, closet and friends so every screen can be seen. *Profile → Settings → Clear sample data and start fresh* resets it to zero.

## Features
- **Scan:** animated viewfinder, six sample items, manual barcode entry, optional camera
- **Eco-score engine:** `score = 0.35 × materials + 0.25 × carbon + 0.25 × water + 0.15 × labour`
  - carbon score = 100 − 4 × kg CO₂e (25 kg or more scores 0)
  - water score = 100 − litres ÷ 40 (4,000 L or more scores 0)
  - grades: A 85+, B 70+, C 55+, D 30+, E below 30. Red for D and E, amber for C, green for A and B
- **Everyday units:** carbon as km of driving, water as years of drinking water
- **Swaps:** 22-item catalogue across tops, jeans, jackets, dresses, shoes and shirts. Savings in rupees, litres and CO₂. Pause and Skip earns points for not buying
- **GreenPoints:** levels (Seedling to Planet Hero, based on lifetime points), streak tracker, weekly chart, six badges, 30-wear challenge, rewards store, sample leaderboard
- **Profile:** Eco Impact Score share card, outfit ideas, closet, settings


## Tools
Python and Streamlit. Built with assistance from Claude (Anthropic's AI assistant) for code.

## References
- Zalando (2025). Attitude-Behaviour Gap Report 2025. https://corporate.zalando.com/en/node/10765
- Sheffield Hallam University (2022). Fast fashion survey of 60 students. https://www.shu.ac.uk/news/all-articles/latest-news/fast-fashion
- FashionUnited (2019). Redress shares resources on fashion's impact on the environment and economy. https://fashionunited.com/news/fashion/redress-shares-resources-on-fashion-s-impact-on-the-environment-and-economy/2019092530105
- Dazed Digital. Good On You app ranks fashion brands on how ethical and sustainable they are. https://dazeddigital.com/fashion/article/40643/1/good-on-you-app-ranks-fashion-brands-how-ethical-sustainable-they-are
