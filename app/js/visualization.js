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
