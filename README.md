# SustainStyle: Eco-App in Action

**Scan a clothing tag, see its environmental impact, swap to something cheaper and greener, and earn GreenPoints.**

Live app: **add your Streamlit link here** · Design document: [FA-1 submission](docs/FA1_Submission.docx)
Course: Critical and Creative Thinking (CRS), Formative Assessment 2



## What the app does
SustainStyle is a mobile-first web app for shoppers who want to buy better clothes without paying more. The shopper scans a tag (barcode, typed code, search or camera) and gets a 0 to 100 eco-score with an A to E grade, a traffic-light verdict and a breakdown by materials, carbon, water and labour. If the item scores badly, the app lists second-hand, repair or organic options that score higher and fit the shopper's size, style and budget, and shows the money, water and CO₂ each swap saves. Scans, swaps and skipped purchases earn GreenPoints, which build streaks, levels and badges and can be redeemed for rewards. Two items can be compared side by side. The interface is available in English and Hindi.

## How this connects to FA-1
This app is the working prototype of the concept in [FA-1](docs/FA1_Submission.docx) (research report, SCAMPER ideation, six-screen storyboard). FA-1 found that price, not being able to identify sustainable items, and doubts about green claims get in the way of sustainable shopping. The goal: *an app that gives an instant item-level eco-score and a cheaper, greener alternative at the moment of buying, and rewards better choices with GreenPoints.*

| FA-1 insight | Design decision | Where in the app |
|---|---|---|
| **I1** Price is the top barrier | Cheaper, second-hand and repair options first; filters and a budget setting | Alternatives |
| **I2** Hard to tell which items are sustainable | Score the exact item; barcode, search and camera input; guest mode | Home, Scan |
| **I3** Intentions do not turn into action | Instant result, GreenPoints, streaks, 30-wear challenge, rewards | Reward, Impact |
| **I4** Trust in green claims is shaky | Visible weights, per-factor reasons, data-confidence label, "How is this calculated?" | Result |

| FA-1 storyboard screen | Built as |
|---|---|
| 1 Home | Home: points hero, scan, guest mode, impact tiles, quick scan |
| 2 Scan | Scan: viewfinder, sample items, barcode, search, camera |
| 3 Eco-Score | Result: gauge, grade, traffic light, factor bars, cost per wear |
| 4 Swaps | Alternatives with filters, size/style/budget matching, Compare |
| 5 Reward | Great choice: points, savings, level-up, share text |
| 6 My Impact | Impact: weekly chart, streak, challenge, badges, rewards, community |
| Customize | Profile: name, language, size, shoe size, style, budget, larger text, reduce motion |


## Eco-score
`score = 0.35 × materials + 0.25 × carbon + 0.25 × water + 0.15 × labour`
carbon factor = 100 − 4 × kg CO₂e (25 kg or more = 0); water factor = 100 − litres ÷ 40 (4,000 L or more = 0).
Grades: A 85+, B 70+, C 55+, D 30+, E below. Green for A and B, amber for C, red for D and E.
Levels and badges use lifetime points, so redeeming rewards never lowers your level.



## References
- Zalando (2025). Attitude-Behaviour Gap Report 2025. https://corporate.zalando.com/en/node/10765
- Sheffield Hallam University (2022). Fast fashion survey of 60 students. https://www.shu.ac.uk/news/all-articles/latest-news/fast-fashion
- FashionUnited (2019). Redress shares resources on fashion's impact on the environment and economy. https://fashionunited.com/news/fashion/redress-shares-resources-on-fashion-s-impact-on-the-environment-and-economy/2019092530105
- Dazed Digital. Good On You app ranks fashion brands on how ethical and sustainable they are. https://dazeddigital.com/fashion/article/40643/1/good-on-you-app-ranks-fashion-brands-how-ethical-sustainable-they-are
