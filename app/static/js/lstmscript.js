//global baseUrl
//const baseUrl = window.location.origin;

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

    // Fetch and display the data
    fetch(`${baseUrl}/lstmmodel`, {
      // Use baseUrl dynamically
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

        // Update only the #lstm-results div without affecting Sklearn results
        const lstmResultsDiv = document.getElementById("lstm-results");
        lstmResultsDiv.innerHTML = `Predicted Stock Price: $${data.predicted_stock_price.toFixed(
          2
        )}`;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });
});
