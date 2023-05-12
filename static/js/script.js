$(document).ready(function() {
  let destinationCount = 1;

$("#add-destination").on("click", function() {
    if (destinationCount < 4) {  // Increase this number if you want to add more destinations
      const newDestination = $(".destination:first").clone();
      newDestination.find("input").attr("id", `location-${destinationCount + 1}`).attr("name", "locations");
      newDestination.find(".night-selection select").attr("id", `nights-${destinationCount + 1}`).attr("name", "nights");
      newDestination.find("label[for]").each(function() {
        $(this).attr("for", function(i, currentValue) {
          return currentValue.replace(/\d/, destinationCount + 1);
        });
        if (destinationCount > 0) {
          $(this).text(`Destination ${destinationCount + 1}:`);
        }
      });
      $("#destinations").append(newDestination);
      destinationCount++;
    } else {
      alert("You can add up to 4 destinations.");
    }
  });

  let nextButtonState = 0;

  $('#next').on('click', function() {
  switch (nextButtonState) {
    case 0:
      // Switch from destinations input to nights selection
      $('.destination').each(function() {
        const location = $(this).find('input').val();
        $(this).find('.destination-name').text(location);
      });
      $('.destination .form-group:not(.night-selection)').addClass('d-none');
      $('.night-selection').removeClass('d-none');
      $('#add-destination').addClass('d-none');
      nextButtonState++;
      break;
    case 1:
      // Switch from nights selection to travel preferences
      $('#destinations').addClass('d-none');
      $('#travel-preferences').removeClass('d-none');
      $('#generate-itinerary').removeClass('d-none');
      $(this).addClass('d-none'); // Hide the "Next" button
      break;
    default:
      break;
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




  $("#travel-form").on("submit", function(event) {
    event.preventDefault();  // Prevent the form from submitting normally

    if ($("input[name='travel_desires']").length === 0) {
      alert("Please select at least one travel preference.");
      return false;
    }

    // Display the loading message.
    $("#loading-message").removeClass("d-none");
    // Hide the spinner if it's still visible.
    $("#spinner").addClass("d-none");
    // Post the form data using AJAX
    $.ajax({
      type: "POST",
      url: "/",
      data: $(this).serialize(),
      success: function(response) {
  console.log("Form submission response:", response);
  // Start polling the task status
  pollStatus(response.task_id);
}
    });
});

function pollStatus(task_id) {
  $.getJSON("/status/" + task_id, function(data) {
  console.log("Poll status response:", data);
    if (data.state === "PENDING") {
      // The task is still running, poll again after 1 second
      setTimeout(function() {
        pollStatus(task_id);
      }, 10000);
    } else if (data.state === "SUCCESS") {
      // The task has finished, fetch the result
      fetchResult(task_id);
    } else if (data.state === "FAILURE") {
      // The task has failed, display an error message
      $("#loading-message").html("An error occurred while generating your itinerary: " + data.status);
    } else {
      // Something unexpected happened, display an error message
      $("#loading-message").html("An unexpected error occurred while generating your itinerary. Please try again.");
    }
  }).fail(function() {
    // The request itself failed, display an error message
    $("#loading-message").html("An error occurred while checking the task status. Please try again.");
  });
}

function fetchResult(task_id) {
  $.get("/result/" + task_id, function(data) {
    console.log("Fetch result response:", data);
    // Hide the loading message
    $("#loading-message").addClass("d-none");

    // Check if data is a string
    if (typeof data === "string") {
      // Display the result
      $(".result").removeClass("d-none");
      $(".itinerary-result").html(data.replace(/\n/g, "<br>")); // Replace '\n' with '<br>'
    } else {
      // Something unexpected happened, display an error message
      $("#loading-message").html("An unexpected error occurred while fetching the result. Please try again.");
    }
  }).fail(function() {
    // The request itself failed, display an error message
    $("#loading-message").html("An error occurred while fetching the result. Please try again.");
  });
}
});