# Design Analysis 
## Design Rationale

My primary goal of the visualization was to show how home runs in Major League Baseball have evolved over time. I wanted to highlight specific trends and key moments of different eras. I created a line chart for the entire history of the MLB (1871-2025) because I felt like a line chart would best show changes over time and allow me to focus on dips and peaks in the total home run count.  For the color choice, I used blue on the dark background of my webpage (dark mode) and white text.  For the interactive portion, I did tooltips with hover areas for each year, so hovering or clicking on these points shows the top 10 home run leaders for that year. This allows the user to explore each year individually. Next, users can zoom into each significant MLB era using buttons, which changes the x-axis range and adds facts to each era. Moreover, I chose not to include the years 1977-1994, as this time period didn’t feature any major developments or milestones related to home run trends in MLB.

## References
Datasets: 
https://www.baseball-reference.com/leaders/HR_top_ten.shtml
https://www.baseball-reference.com/leagues/majors/bat.shtml
Inspiration: 
https://baseballsavant.mlb.com/visuals
https://www.espn.com/mlb/

- Used D3.js and Observable Plot
- Used AI to help generate some of the functions
Asked questions like “how to build a zoom function,” and “what are the different attributes I can add to the lines, circles, axes” and “how to increase axis size”

## Development Process
This project was the largest so far, it took a good amount of hours (15-20 hours) and was significantly larger than the static visualizations. It was challenging to use D3 and implementing the interactive components took a while.  Resting the features required a lot of time to get working and also a lot of testing to see what looked best. The refinements and experimenting with different things, such as layout and readability, also took a good amount of hours to finalize the visualization. 
