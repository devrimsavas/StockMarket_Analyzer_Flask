//global baseUrl
//let baseUrl = window.location.origin;

document.getElementById("skilearnbutton").addEventListener("click", (e) => {
  e.preventDefault();
  console.log("skilearn button intercepted");

  // Get input values from the form
  let tickinput = document.getElementById("tickinput").value;
  let periodinput = document.getElementById("periodinput").value;
  let predictioninput = document.getElementById("predictioninput").value;

  // Validation
  if (!tickinput || !periodinput || !predictioninput) {
    alert(
      "You need to enter valid values for Ticker, Time period, and Prediction days"
    );
    return;
  }

  // Disable button and show loading message
  const skilearnButton = document.getElementById("skilearnbutton");
  skilearnButton.disabled = true;
  const sklearnResultsDiv = document.getElementById("sklearn-results");
  sklearnResultsDiv.innerHTML = `<p>Processing, please wait...</p>`;

  // Fetch and display the data
  fetch(`${baseUrl}/skilearn`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tickinput, predictioninput, periodinput }),
  })
    .then((response) => {
      if (!response.ok) {
        alert("Error fetching data from server");
        return;
      }
      return response.json(); // Parse the response as JSON
    })
    .then((data) => {
      console.log("Prediction Data:", data);

      // Update the #sklearn-results div with prediction data
      sklearnResultsDiv.innerHTML = `
        <h5>Prediction Results:</h5>
        <ul class="list-group">
          <li class="list-group-item">Predicted Stock Price for ${
            data.predictioninput
          } days ahead: $${data.prediction.toFixed(2)}</li>
          <li class="list-group-item">R² Value: ${data.r2.toFixed(
            4
          )} (Explains ${Math.round(data.r2 * 100)}% of the variance)</li>
          <li class="list-group-item">F-statistic: ${data.f_stat.toFixed(
            4
          )}</li>
        </ul>
      `;
    })
    .catch((error) => {
      console.error("Error:", error);
      sklearnResultsDiv.innerHTML = `<p>Error occurred while processing the request.</p>`;
    })
    .finally(() => {
      // Re-enable the button after the request is complete
      skilearnButton.disabled = false;
    });
});
