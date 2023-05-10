$(document).ready(function() {
  let destinationCount = 1;

  $("#add-destination").on("click", function() {
    if (destinationCount < 4) {
      const newDestination = $(".destination:first").clone();
      newDestination.find("input").attr("id", `location-${destinationCount + 1}`);
      newDestination.find("select").attr("id", `nights-${destinationCount + 1}`);
      newDestination.find("label[for]").each(function() {
         $(this).attr("for", function(i, currentValue) {
          return currentValue.replace(/\d/, destinationCount + 1);
        });
      });
      $("#destinations").append(newDestination);
      destinationCount++;
    } else {
      alert("You can add up to 4 destinations.");
    }
  });

  $(".preference-button").on("click", function() {
    const preference = $(this).text();
    const preferenceItem = $("<li></li>").text(preference);
    $("#selected-preferences ul").append(preferenceItem);
    $("<input>").attr({
      type: "hidden",
      name: "travel_desires",
      value: preference
    }).appendTo("#travel-form");
  });

  $("#travel-form").on("submit", function() {
    if ($("input[name='travel_desires']").length === 0) {
      alert("Please select at least one travel preference.");
      return false;
    }
    // Display the loading message.
    $("#loading-message").removeClass("d-none");
    // Hide the spinner if it's still visible.
    $("#spinner").addClass("d-none");
  });
});