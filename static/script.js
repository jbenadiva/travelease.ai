let destinationCount = 1;

function addDestination() {
  const currentLocation = document.querySelector("input[name='location']").value;
  const currentNights = document.querySelector("select[name='nights[]']").value;
  const currentNeighborhood = document.querySelector("input[name='neighborhood']").value;

  const previousInputText = document.createElement("div");
  previousInputText.classList.add("previous-input");
  previousInputText.innerHTML = `Destination ${destinationCount}: ${currentLocation}<br>${currentNights} nights in ${currentLocation}${currentNeighborhood ? " (" + currentNeighborhood + ")" : ""}`;

  const destination = document.querySelector(".destination");
  destination.parentNode.insertBefore(previousInputText, destination);

  document.querySelector("input[name='location']").value = '';
  document.querySelector("select[name='nights[]']").value = '1';
  document.querySelector("input[name='neighborhood']").value = '';

  destinationCount++;
}

function toggleTravelOption(option) {
  const value = option.dataset.value;
  const hiddenInput = document.getElementById("travel-desires-value");
  const currentValues = hiddenInput.value ? hiddenInput.value.split(",") : [];
  const selectedIndex = currentValues.indexOf(value);

  if (selectedIndex === -1) {
    currentValues.push(value);
    option.classList.remove("btn-outline-primary");
    option.classList.add("btn-primary");
  } else {
    currentValues.splice(selectedIndex, 1);
    option.classList.remove("btn-primary");
    option.classList.add("btn-outline-primary");
  }

  hiddenInput.value = currentValues.join(",");

  const li = document.createElement("li");
  li.textContent = option.textContent.replace("+ ", ""); // Remove the "+" from the displayed text
  li.id = "li-" + value;
  const selectedPreferences = document.getElementById("selected-preferences");

  if (selectedIndex === -1) {
    selectedPreferences.appendChild(li);
  } else {
    const liToRemove = document.getElementById("li-" + value);
    selectedPreferences.removeChild(liToRemove);
  }
}

function showTravelOptions() {
  document.getElementById("step-2").style.display = "block";
  document.querySelectorAll(".travel-option").forEach(option => {
    option.addEventListener("click", () => toggleTravelOption(option));
  });
}

document.getElementById("add-destination").addEventListener("click", addDestination);

document.getElementById("next-step-1").addEventListener("click", showTravelOptions);

document.getElementById("next-step-2").addEventListener("click", () => {
  document.getElementById("step-3").style.display = "block";
});

addNewDestinationInputs();