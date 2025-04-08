// Function to load and render the Altair visualization
function loadVisualization() {
  // Fetch the visualization spec from a JSON file
  fetch("Final/DS4200-Bike-Project/app/viz1_spec.json") // Changed path to look in the current directory
    .then((response) => {
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`)
      }
      return response.json()
    })
    .then((spec) => {
      // Embed the visualization in the container
      try {
        vegaEmbed("#viz1-container", spec, {
          actions: true,
          theme: "light",
        }).catch(console.error)
      } catch (error) {
        console.error("Vega Embed is not properly loaded:", error)
        document.getElementById("viz1-container").innerHTML =
          '<p class="error">Vega Embed is not properly loaded. Please ensure vega-embed is included.</p>'
      }
    })
    .catch((error) => {
      console.error("Error loading visualization:", error)
      document.getElementById("viz1-container").innerHTML =
        '<p class="error">Error loading visualization. Please try again later.</p>'
    })
}

// Load visualization when the page is ready
document.addEventListener("DOMContentLoaded", () => {
  loadVisualization()
})

// Function to create linechart using d3
const svg = d3.select("#chart");
const margin = { top: 40, right: 100, bottom: 50, left: 60 };
const width = +svg.attr("width") - margin.left - margin.right;
const height = +svg.attr("height") - margin.top - margin.bottom;

const g = svg.append("g").attr("transform", `translate(${margin.left},${margin.top})`);
const colors = d3.schemeCategory10;

// Load each file into its own variable
Promise.all([
  d3.csv("hourly_data_4.csv", d => ({ hour: +d.hour, count: +d.count })),
  d3.csv("hourly_data_9.csv", d => ({ hour: +d.hour, count: +d.count })),
  d3.csv("hourly_data_12.csv", d => ({ hour: +d.hour, count: +d.count }))
]).then(([data1, data2, data3]) => {
  const allData = [...data1, ...data2, ...data3];

  const x = d3.scaleLinear()
              .domain([0, 23])
              .range([0, width]);

  const y = d3.scaleLinear()
              .domain([0, d3.max(allData, d => d.count)])
              .nice()
              .range([height, 0]);

  // Axes
  g.append("g")
    .attr("transform", `translate(0, ${height})`)
    .call(d3.axisBottom(x).ticks(24).tickFormat(d3.format("02")));

  g.append("g")
    .call(d3.axisLeft(y));

  // Line generator
  const line = d3.line()
                 .x(d => x(d.hour))
                 .y(d => y(d.count));

  const datasets = [data1, data2, data3];
  datasets.forEach((data, i) => {
    g.append("path")
     .datum(data)
     .attr("fill", "none")
     .attr("stroke", colors[i])
     .attr("stroke-width", 2)
     .attr("d", line);

    // Legend
    g.append("text")
     .attr("x", width - 60)
     .attr("y", 20 + i * 20)
     .attr("fill", colors[i])
     .text(`Dataset ${i + 1}`);
  });

  // Labels
  g.append("text")
    .attr("x", width / 2)
    .attr("y", height + 40)
    .attr("text-anchor", "middle")
    .text("Hour of Day");

  g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("x", -height / 2)
    .attr("y", -40)
    .attr("text-anchor", "middle")
    .text("Count");
});