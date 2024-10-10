document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("lsmmodelbutton").addEventListener("click", (e) => {
    e.preventDefault();
    console.log("LSTM button clicked");

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

    // Display loading message while waiting for the analysis
    const lstmResultsDiv = document.getElementById("lstm-results");
    lstmResultsDiv.innerHTML = `<p>Analyzing... Please wait.</p>`;

    // Fetch and display the data
    fetch(`${baseUrl}/lstmmodel`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ tickinput, periodinput, predictioninput }),
    })
      .then((response) => {
        if (!response.ok) {
          alert("Error: an error occurred");
          return;
        }
        return response.json();
      })
      .then((data) => {
        console.log("LSTM Data:", data);

        // Check if epoch data is available and display it
        if (data.epochs) {
          const epochsHtml = data.epochs
            .map(
              (epoch, index) =>
                `<p>Epoch ${index + 1}: Loss - ${epoch.loss}</p>`
            )
            .join("");

          lstmResultsDiv.innerHTML = `<h5>Epoch Data:</h5>${epochsHtml}`;
        }

        // Display the final predicted stock price
        lstmResultsDiv.innerHTML += `Predicted Stock Price: $${data.predicted_stock_price.toFixed(
          2
        )}`;
      })
      .catch((error) => {
        console.error("Error:", error);
        lstmResultsDiv.innerHTML = `<p>Error occurred during the analysis.</p>`;
      });
  });
});
