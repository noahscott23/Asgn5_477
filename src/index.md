# Assignment 5: Design Brief
Noah Scott  

---

## Dataset Choice
I chose the **Baseball-Reference MLB Batting Year-by-Year Totals** dataset:  
https://www.baseball-reference.com/leagues/majors/bat.shtml

This dataset contains annual batting statistics and totals such as batting average, on-base percentage, and total hits, and total homeruns for Major League Baseball from 1871-2025

---

## Analysis Question
How has offensive performance in Major League Baseball evolved over time, and what time periods show the greatest changes in homeruns?

---

## Visual Concept
A **line chart** showing the trend in batting average over time.  
- **X-axis:** Year  
- **Y-axis:** Homerun Totals 
- **Color:** Indicates different offensive eras

---

## Interaction Concept
- **Hover:** view the year and number of homeruns, as well as the homerun leader for that year

---

## Inspiration
- [MLB Visuals](https://baseballsavant.mlb.com/visuals)
- [ESPN Visuals](https://www.espn.com/mlb/)

---

## Data Loading

```js
import * as d3 from "npm:d3";
import * as Plot from "npm:@observablehq/plot";
const data = await FileAttachment("mlb.csv").csv({typed: true});

// data loading
display(data);
