<div align="center">

# MLB Home Runs (1871–2025)
## Individual Leaders Also Shown Per Year (hover over line)

</div>

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
  .range([m + 10, w - m - 50]);

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
  .transition().duration(8000)
  .ease(d3.easeLinear)
    .attr("stroke-dashoffset", 0); // dash offset from fully hidden to fully revealed
               

svg.append("g")
  .attr("class", "x-axis")
  .attr("transform", `translate(0,${h - m})`)   
  .call(d3.axisBottom(x));   

svg.select(".x-axis")
  .selectAll("text")
  .style("font-size", "12px")
  .style("fill", "#f1faee");

svg.append("g")
  .attr("transform", `translate(${m},0)`)
  .call(d3.axisLeft(y));
svg.selectAll(".y-axis text, .tick text")
  .style("font-size", "12px")
  .style("fill", "#f1faee");


// tooltip for each year
const tooltip = d3.select("body").append("div")
  .style("position", "absolute")
  .style("background", "white")
  .style("padding", "8px")                             
  .style("border-radius", "6px")                        // rounded edges
  .style("box-shadow", "0 2px 6px rgba(0,0,0,0.2)")     // shadow to help box display better
  .style("pointer-events", "none")                    
  .style("opacity", 0)
  .style("color", "#222") 
  .style("line-height", "1.2"); 

let locked = false; // pinned by click

// circles and tooltip
const circles = svg.selectAll("circle")
  .data(mlb)
  .join("circle")
  .attr("cx", d => x(d.Year))
  .attr("cy", d => y(d.TotalHR))
  .attr("r", 10)
  .attr("fill", "transparent")
  .style("cursor", "pointer")
  .style("opacity", 1)
  .on("mouseover", (event, d) => {
  if (locked) return; // doesnt show hover tooltip when locked

  const list = leaderLists.get(d.Year);
  const htmlList = list
    ? list.map(p => `${p.Rank}. ${p.Player} (${p.HomeRuns})`).join("<br>")
    : "No data available";

  tooltip.transition().duration(150).style("opacity", 1);
  tooltip.html(`<b>${d.Year}</b><br>Total HR: ${d.TotalHR}<br><b>Top 10 HR Leaders</b><br>${htmlList}`)
    .style("left", `${event.pageX + 12}px`)
    .style("top", `${event.pageY - 28}px`);
  })
.on("mousemove", event => {
  if (!locked) {
    tooltip.style("left", `${event.pageX + 12}px`)
           .style("top", `${event.pageY - 28}px`);
  }
})
.on("mouseout", () => {
  if (!locked) tooltip.transition().duration(200).style("opacity", 0);
})
// click locks the tooltip
.on("click", (event, d) => {
  event.stopPropagation(); // prevent global click from closing it
  locked = true;

  const list = leaderLists.get(d.Year);
  const htmlList = list
    ? list.map(p => `${p.Rank}. ${p.Player} (${p.HomeRuns})`).join("<br>")
    : "No data available";

  tooltip.transition().duration(150).style("opacity", 1);
  tooltip.html(`<b>${d.Year}</b><br>Total HR: ${d.TotalHR}<br><b>Top 10 HR Leaders</b><br>${htmlList}`)
    .style("left", `${event.pageX + 12}px`)
    .style("top", `${event.pageY - 28}px`);
});

circles.transition()
  .delay((d, i) => (i / mlb.length) * 8000)  
  .duration(0)
  .style("opacity", 1);

svg.append("g")
  .attr("class", "grid")
  .attr("transform", `translate(${m},0)`)
  .call(d3.axisLeft(y).tickSize(-w + 2*m).tickFormat(""))
  .selectAll("line")
  .attr("stroke", "#ffffff15")
  .attr("stroke-width", 0.5)
  .attr("shape-rendering", "crispEdges");
svg.selectAll(".grid .domain").remove();

// zoom function
function zoomToYears(startYear, endYear, facts, drawLines = true) {
  const zoomDuration = 2000; 
  const factFade = 800;

  svg.selectAll(".main-label")
  .transition()
  .duration(500)
  .style("opacity", 0);

  x.domain([startYear, endYear]);

  svg.select(".x-axis")
  .transition()
  .duration(zoomDuration)
  .ease(d3.easeCubicInOut)
  .call(d3.axisBottom(x).tickFormat(d3.format("d")))
  .selection()
  .selectAll("text")
  .style("font-size", "12px")
  .style("fill", "#f1faee");

  svg.select("path")
    .transition()
    .duration(zoomDuration)
    .ease(d3.easeCubicInOut)
    .attr("d", line(mlb.filter(d => d.Year >= startYear && d.Year <= endYear)));

  svg.selectAll("circle")
  .transition()
  .duration(zoomDuration)
  .ease(d3.easeCubicInOut)
  .attr("cx", d => x(d.Year))
  .attr("cy", d => y(d.TotalHR))
  .style("opacity", d => (d.Year >= startYear && d.Year <= endYear ? 1 : 0));

  svg.selectAll(".fact-text").remove();

  svg.transition()
  .delay(zoomDuration)
  .on("end", () => {
    facts.forEach((f, i) => {
      const factGroup = svg.append("text")
        .attr("class", "fact-text")
        .attr("x", x(f.xPos ?? f.year))
        .attr("y", y(f.yVal))
        .attr("text-anchor", "middle")
        .style("fill", "#f1faee")
        .style("font-size", "14px")
        .style("font-style", "italic")
        .style("opacity", 0);

      // so i can use \n
      const lines = `${f.year}: ${f.text}`.split("\n");

      lines.forEach((line, j) => {
        factGroup.append("tspan")
          .attr("x", x(f.xPos ?? f.year))
          .attr("dy", j === 0 ? 0 : "1.2em") 
          .text(line.trim());
      });

      factGroup.transition()
        .delay(i * 400)
        .duration(factFade)
        .style("opacity", 1);
    });
  svg.selectAll(".fact-line").remove();

  if (drawLines) {
    facts.forEach((f, i) => {
      svg.append("line")
        .attr("class", "fact-line")
        .attr("x1", x(f.year))
        .attr("x2", x(f.year))
        .attr("y1", y(0))          // bottom of chart
        .attr("y2", y(f.yVal) - 20) 
        .attr("stroke", "#f1faee")
        .attr("stroke-width", 1)
        .attr("stroke-dasharray", "4,4")
        .style("opacity", 0)
        .transition()
        .delay(i * 400)
        .duration(factFade)
        .style("opacity", 0.5);
    });
  }
  });

}

//zoom buttons
const zoomSections = [
  {
    label: "Deadball Era (1900–1919)",
    range: [1876, 1919],
    facts: [
      { year: 1919, xPos: 1916, text: "Babe Ruth hits record 29 HRs", yVal: 1100 },
      { year: 1884, xPos: 1887, text: "Ned Williamson hits 27 HR (19th century record)", yVal: 1000 }
    ]
  },
  {
    label: "Live-Ball Era (1920–1941)",
    range: [1920, 1941],
    facts: [
      { year: 1920, xPos: 1925, text: "Babe Ruth hits 54 HRs, more than a lot of other teams!", yVal: 2000 },
      { year: 1927, xPos: 1930, text: "Ruth hits 60 HR, a record for the next 34 years", yVal: 1000 }
    ]
  },
  {
    label: "WWII Era (1942–1945)",
    range: [1940, 1947],
    facts: [
      { year: 1941, xPos: 1943, text: "Ted Williams hits 37 HR while batting .406 before serving in WWII", yVal: 1700 }
    ]
  },
  {
    label: "Post-War Era (1946–1962)",
    range: [1942, 1966],
    facts: [
      { year: 1947, xPos: 1950, text: "Jackie Robinson debuts, paving way for \nHank Aaron, Willie Mays, and other power hitters of color", yVal: 2600 },
      { year: 1956, xPos: 1958.5, text: "Mickey Mantle wins \nTriple Crown with 52 HR", yVal: 1800 },
      { year: 1961, text: "Roger Maris breaks Ruth’s record with 61 HR,\n amid huge media scrutiny", yVal: 3500 }
    ]
  },
  {
    label: "Pitcher's Era (1963–1976)",
    range: [1963, 1976],
    facts: [
      { year: 1968, text: "Year of the Pitcher, HRs way down", yVal: 1600 },
      { year: 1974, text: "Hank Aaron hits HR #715, breaking Babe Ruth’s career record (714)", yVal: 4000 }
    ]
  },
  {
    label: "Steroid Era (1995–2005)",
    range: [1995, 2005],
    facts: [
      { year: 1998, xPos: 2000, text: "Mark McGwire (70 HR) & Sosa (66 HR) home-run race", yVal: 4600 },
      { year: 2001, text: "Barry Bonds hits 73 HRs, the all-time record", yVal: 5900 },
      { year: 2005, xPos: 2004, text: "Congressional steroid hearings", yVal: 4600 }
    ]
  },
  {
    label: "Post-Steroid Era (2006-2014)",
    range: [2006, 2014],
    facts: [
      { year: 2009, text: "Albert Pujols hits 47 HR, \nbecomes model of consistent power", yVal: 5500 },
      { year: 2012, text: "Miguel Cabrera Wins MLB’s first \nTriple Crown since 1967", yVal: 5500 }
    ]
  },  
  {
    label: "Modern Power Era- Statcast (2015–2025)",
    range: [2015, 2025],
    facts: [
      { year: 2019, text: 'Record-breaking 6,776 HRs- "Juiced Ball controversy"', yVal: 6900 },
      { year: 2022, text: "Aaron Judge (62 HR) breaks AL record", yVal: 4800 },
      { year: 2023, text: "Shohei Ohtani redefines power \nhitting as a two-way superstar", yVal: 6400 }
    ]
  }
];

const chartContainer = d3.create("div")
  .style("display", "flex")
  .style("flex-direction", "column")
  .style("align-items", "center");

chartContainer.node().appendChild(svg.node());

d3.select("#button-container").remove();
const btnContainer = chartContainer
  .append("div")
  .attr("id", "button-container")
  .style("margin-top", "20px")
  .style("text-align", "center");

let activeButton = null;

zoomSections.forEach(section => {
  const btn = btnContainer.append("button")
    .text(section.label)
    .style("margin", "0 6px")
    .style("padding", "8px 14px")
    .style("background", "#0a356b")
    .style("color", "#f1faee")
    .style("border", "none")
    .style("border-radius", "6px")
    .style("cursor", "pointer")
    .style("transition", "all 0.2s ease")
    .on("click", () => {
      if (activeButton && activeButton !== btn) {
        activeButton
          .style("background", "#0a356b")
          .style("color", "#f1faee")
          .style("transform", "none");
      }
      btn
        .style("background", "#42c2f5")
        .style("color", "#0a356b")
        .style("transform", "scale(1.05)");
      activeButton = btn;
      zoomToYears(section.range[0], section.range[1], section.facts);
    });
});

// back button
btnContainer.append("button")
  .text("⟵ Back to Full View")
  .style("margin-left", "10px")
  .style("padding", "8px 14px")
  .style("background", "#42c2f5")
  .style("color", "#0a356b")
  .style("border", "none")
  .style("border-radius", "6px")
  .style("cursor", "pointer")
  .on("click", () => {
    zoomToYears(1871, 2025, []);
    if (activeButton) {
      activeButton
        .style("background", "#0a356b")
        .style("color", "#f1faee")
        .style("transform", "none");
      activeButton = null;
    }
  });


display(chartContainer.node()); // close when clicked outside of svg
document.addEventListener("click", () => {
  if (locked) {
    tooltip.transition().duration(150).style("opacity", 0);
    locked = false;
  }
});
