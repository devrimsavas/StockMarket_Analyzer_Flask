//global baseUrl
//let baseUrl = window.location.origin;

// Add event listener to all elements with the class 'company-tick'
document.querySelectorAll(".company-tick").forEach(function (tickerElement) {
  tickerElement.addEventListener("click", function () {
    let ticker = tickerElement.getAttribute("data-ticker");
    console.log("Company ticker clicked: " + ticker);

    // You can now send this ticker to the backend or trigger any action
    // Example: autofill the search form with the clicked ticker
    document.getElementById("tickinput").value = ticker;
  });
});

document.getElementById("companyinfobutton").addEventListener("click", (e) => {
  e.preventDefault();
  console.log("Company info button clicked");
  let tickinput = document.getElementById("tickinput").value;
  let periodinput = document.getElementById("periodinput").value;

  if (!tickinput || !periodinput) {
    alert("You need to enter valid values for Ticker and Time period");
    return;
  }

  console.log(`Ticker: ${tickinput}, Time period: ${periodinput}`);

  // Post values to back-end
  try {
    fetch(`${baseUrl}/getcompanyinfo`, {
      // Use baseUrl dynamically
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ tickinput: tickinput, periodinput: periodinput }),
    })
      .then((response) => {
        if (!response.ok) {
          alert(
            "Error: It seems Company Ticker does not exist. Please update your list or try another company."
          );
          return;
        }
        return response.json();
      })
      .then((data) => {
        let companyAddress = {
          street: data.company_info.address1,
          city: data.company_info.city,
          country: data.company_info.country,
        };
        document.getElementById("company address").innerHTML = JSON.stringify(
          companyAddress,
          null,
          7
        );

        document.getElementById("hiprcell").innerHTML =
          data.highest_price.toFixed(3);
        document.getElementById("hiprdate").innerHTML = data.highest_price_date;
        document.getElementById("loprcell").innerHTML =
          data.lowest_price.toFixed(3);
        document.getElementById("loprdate").innerHTML = data.lowest_price_date;

        // Update the company logo
        let companyLogoElement = document.querySelector(
          'img[alt="Company Logo"]'
        );
        companyLogoElement.src = data.company_logo_url;

        // Clear the table before adding new rows
        const tableBody = document.getElementById("table-body");
        tableBody.innerHTML = "";

        // Dynamically add rows to the table
        data.dates.forEach((date, index) => {
          let newRow = `
                            <tr>
                                <td>${date}</td>
                                <td>${data.closing_prices[index]}</td>
                            </tr>
                        `;
          tableBody.insertAdjacentHTML("beforeend", newRow);
        });

        // Update the graph inside the same promise
        const imgElement = document.getElementById("graph-image");
        imgElement.src = `data:image/png;base64,${data.image_data}`;
      });
  } catch (error) {
    console.error("Error ", error);
  }
});
