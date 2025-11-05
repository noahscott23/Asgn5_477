# MLB 

## Total Homeruns by Year

```js
import * as d3 from "npm:d3";
import * as Plot from "npm:@observablehq/plot";

const mlb = await FileAttachment("mlb.csv").csv({ typed: true });
const leaders = await FileAttachment("leaders.csv").csv({ typed: true });

// Convert fields
mlb.forEach(d => {
  d.Year = +d.Year;
  d.TotalHR = +d.HR;   
});

leaders.forEach(d => {
  d.Year = +d.Year;
  d.Rank = +d.Rank;
  d.HomeRuns = +d.HomeRuns;
});

// sort mlb data
mlb.sort((a, b) => d3.ascending(a.Year, b.Year));

const leaderLists = d3.group(leaders, d => d.Year);

// create chart
const w = 1000, h = 500, m = 50;
const svg = d3.create("svg").attr("width", w).attr("height", h);

// scales
const x = d3.scaleLinear()
  .domain(d3.extent(mlb, d => d.Year))
  .range([m, w - m]);

const y = d3.scaleLinear()
  .domain([0, d3.max(mlb, d => d.TotalHR)])
  .nice()
  .range([h - m, m]);

// creates the line
const line = d3.line()
  .x(d => x(d.Year))
  .y(d => y(d.TotalHR));

const path = svg.append("path")
  .datum(mlb)
  .attr("fill", "none")
  .attr("stroke", "#42c2f5")
  .attr("stroke-width", 2)
  .attr("d", line);

// making the line animated
const totalLength = path.node().getTotalLength();   // gets exact len of path
path.attr("stroke-dasharray", totalLength)    // means no dashes, needed to animate the line
    .attr("stroke-dashoffset", totalLength)
  .transition().duration(10000)
    .attr("stroke-dashoffset", 0); // dash offset from fully hidden to fully revealed

// 2020 static text
svg.append("text")
  .attr("x", x(2020))
  .attr("y", y(1800)) 
  .attr("text-anchor", "middle")
  .style("fill", "#f1faee")
  .style("font-size", "14px")
  .style("font-style", "italic")
  .call(text => {
    text.append("tspan")
      .attr("x", x(2020))
      .attr("dy", 0) 
      .text("COVID-19 shortened");
    text.append("tspan")
      .attr("x", x(2020))
      .attr("dy", "1.2em") // move down for the second line
      .text("season (60 games)");
  });


// Axes
svg.append("g")
  .attr("transform", `translate(0,${h - m})`)   // makes x-axis start at bottom
  .call(d3.axisBottom(x));   // creating a bottom-oriented axis with ticks and labels

svg.append("g")
  .attr("transform", `translate(${m},0)`)
  .call(d3.axisLeft(y));

// tooltip for each year
const tooltip = d3.select("body").append("div")
  .style("position", "absolute")
  .style("background", "white")
  .style("padding", "8px")                              // text and edges padding
  .style("border-radius", "6px")                        // rounded edges
  .style("box-shadow", "0 2px 6px rgba(0,0,0,0.2)")     // shadow to help box display better
  .style("pointer-events", "none")                      // needed for smooth hover
  .style("opacity", 0);

// Points + tooltip
svg.selectAll("circle")
  .data(mlb)
  .join("circle")
  .attr("cx", d => x(d.Year))
  .attr("cy", d => y(d.TotalHR))
  .attr("r", 4)
  .attr("fill", "#0a356b")
  .on("mouseover", (event, d) => {
  const list = leaderLists.get(d.Year);
  const htmlList = list
    ? list.map(p => `${p.Rank}. ${p.Player} (${p.HomeRuns})`).join("<br>")
    : "No data available";

  tooltip.transition().duration(150).style("opacity", 1);
  tooltip.html(`<b>${d.Year}</b><br>Total HR: ${d.TotalHR}<br><br><b>Top 10 HR Leaders</b><br>${htmlList}`)
    .style("left", `${event.pageX + 12}px`)
    .style("top", `${event.pageY - 28}px`);
})

  .on("mousemove", event => {
    tooltip.style("left", `${event.pageX + 12}px`)
           .style("top", `${event.pageY - 28}px`);
  })
  .on("mouseout", () => {
    tooltip.transition().duration(200).style("opacity", 0);
  });

display(svg.node());