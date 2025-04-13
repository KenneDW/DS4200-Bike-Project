// Define the dimensions and margins for the SVG
const width = 800, height = 600;
const margin = {top: 100, bottom: 60, left: 50, right: 50};


const hours = [...Array(24).keys()];
const month_4 = [108, 78, 38, 8, 9, 15, 84, 182, 276, 370, 279, 316, 296, 313, 413, 418, 539, 557, 518, 411, 315, 210, 187, 121];
const month_9 = [127, 93, 67, 14, 14, 27, 133, 582, 687, 505, 306, 483, 338, 526, 525, 640, 764, 980, 707, 589, 462, 318, 240, 154];
const month_12 = [28, 31, 18, 4, 5, 13, 38, 123, 221, 168, 109, 115, 141, 158, 152, 171, 189, 274, 142, 127, 83, 56, 55, 49]

// Create the SVG container
const svg = d3.select("#lineplot")
    .attr("width", width)
    .attr("height", height)
    .style("background", "#ffffff");

const yScale = d3.scaleLinear()
    .domain([0, d3.max(month_9)])
    .range([height - margin.bottom, margin.top]);

const xScale = d3.scaleLinear()
    .domain([0, d3.max(hours)])
    .range([margin.left, width - margin.right]);

let xAxis = svg
    .append('g')
    .attr('transform', `translate(0,${height - margin.bottom})`)
    .call(d3.axisBottom(xScale));

let yAxis = svg
    .append('g')
    .attr('transform', `translate(${margin.left},0)`)
    .call(d3.axisLeft(yScale));

// Add titles
xAxis.append("text")
    .attr("x", width/2)
    .attr("y", 30)
    .style("stroke", "black")
    .text("Hour of the Day")


yAxis.append("text")
    .attr("x", -height/2)
    .attr("y", -40)
    .attr("transform", "rotate(-90)")
    .style("stroke", "black")
    .text("Number of Rides")

svg.append("text")
    .attr("x", 250)
    .attr("y", margin.top / 2)
    .style("font-weight", "bold")
    .text("Quantity of Bike Rides by Hour of the Day");


// map hours of th day to our data
const month_4_data = hours.map((x, i) => ({ x: x, y: month_4[i] }));
const month_9_data = hours.map((x, i) => ({ x: x, y: month_9[i] }));
const month_12_data = hours.map((x, i) => ({ x: x, y: month_12[i] }));

// Add the lines
let line = d3.line()
    .x(d => xScale(d.x))
    .y(d => yScale(d.y))
    .curve(d3.curveNatural)

svg.append("path")
    .datum(month_4_data)
    .attr("fill", "none")
    .attr("stroke", "rgb(157, 229, 230)")
    .attr("stroke-width", 2)
    .attr("d", line);

svg.append("path")
    .datum(month_9_data)
    .attr("fill", "none")
    .attr("stroke", "rgb(242, 140, 237)")
    .attr("stroke-width", 2)
    .attr("d", line);

svg.append("path")
    .datum(month_12_data)
    .attr("fill", "none")
    .attr("stroke", "rgb(72, 182, 81)")
    .attr("stroke-width", 2)
    .attr("d", line);

// Create Legend
const legend = svg.append("g")
    .attr("transform", `translate(${width - 150}, ${margin.top})`);

legend.append("rect")
    .attr("x", 0)
    .attr("y", 0)
    .attr("width", 30)
    .attr("height", 10)
    .attr("fill", "rgb(157, 229, 230)");
legend.append("text")
    .attr("x", 40)
    .attr("y", 5)
    .text("April")
    .style("font-size", "12px")
    .attr("alignment-baseline", "middle");

legend.append("rect")
    .attr("x", 0)
    .attr("y", 15)
    .attr("width", 30)
    .attr("height", 10)
    .attr("fill", "rgb(242, 140, 237)");
legend.append("text")
    .attr("x", 40)
    .attr("y", 20)
    .text("September")
    .style("font-size", "12px")
    .attr("alignment-baseline", "middle");

legend.append("rect")
    .attr("x", 0)
    .attr("y", 30)
    .attr("width", 30)
    .attr("height", 10)
    .attr("fill", "rgb(72, 182, 81)");
legend.append("text")
    .attr("x", 40)
    .attr("y", 35)
    .text("December")
    .style("font-size", "12px")
    .attr("alignment-baseline", "middle");