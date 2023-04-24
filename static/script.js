let destinationCount = 1;

function addDestination() {
  // Get the values from the current inputs
  const currentLocation = document.querySelector("input[name='location']").value;
  const currentNights = document.querySelector("select[name='nights[]']").value;
  const currentNeighborhood = document.querySelector("input[name='neighborhood']").value;

  // Replace the current inputs with static text
  const destination = document.querySelector(".destination");
  destination.innerHTML = `Location: ${currentLocation}<br>Nights: ${currentNights}<br>Neighborhood: ${currentNeighborhood || "N/A"}<br><br>`;

  // Add a new set of inputs
  addNewDestinationInputs();
}

function addNewDestinationInputs() {
  destinationCount++;
  const destinationGroup = document.createElement("div");
  destinationGroup.className = "destination-group";

  const locationLabel = document.createElement("label");
  locationLabel.textContent = "Location:";
  destinationGroup.appendChild(locationLabel);

  const locationInput = document.createElement("input");
  locationInput.type = "text";
  locationInput.name = "location";
  destinationGroup.appendChild(locationInput);

  const nightsLabel = document.createElement("label");
  nightsLabel.textContent = "How many nights?";
  destinationGroup.appendChild(nightsLabel);

  const nightsInput = document.createElement("select");
  nightsInput.name = "nights[]";
  for (let i = 1; i <= 6; i++) {
    const option = document.createElement("option");
    option.value = i;
    option.textContent = i;
    nightsInput.appendChild(option);
  }
  nightsInput.required = true;
  destinationGroup.appendChild(nightsInput);

  const neighborhoodLabel = document.createElement("label");
  neighborhoodLabel.textContent = "Neighborhood (optional):";
  destinationGroup.appendChild(neighborhoodLabel);

  const neighborhoodInput = document.createElement("input");
  neighborhoodInput.type = "text";
  neighborhoodInput.name = "neighborhood";
  destinationGroup.appendChild(neighborhoodInput);

  const destinationsContainer = document.getElementById("destinations-container");
  destinationsContainer.appendChild(destinationGroup);
}

document.getElementById("add-destination").addEventListener("click", addDestination);

document.getElementById("next-step-1").addEventListener("click", () => {
  document.getElementById("step-2").style.display = "block";
});

document.getElementById("next-step-2").addEventListener("click", () => {
  document.getElementById("step-3").style.display = "block";
});

document.getElementById("travel_desires").addEventListener("change", (event) => {
  const selectedDesires = Array.from(event.target.selectedOptions).map(option => option.value);
  document.getElementById("selected-desires").textContent = selectedDesires.join(", ");
});

addNewDestinationInputs();