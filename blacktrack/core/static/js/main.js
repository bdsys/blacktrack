function ToggleHideByIdDisplay() {
  var HiddenIdObject = document.getElementById("default_no_display_form");
  if (HiddenIdObject.style.display === "none") {
    HiddenIdObject.style.display = "block";
  } else {
    HiddenIdObject.style.display = "none";
  }
}

function ToggleHideByIdVisbility() {
  function Toggle(elementObject) {
    if (elementObject.style.display === "none") 
    {
      elementObject.style.display = "";
    } 
    else 
    {
      elementObject.style.display = "none";
    }
  }
  
  var HiddenIdObjects = document.querySelectorAll('[id=default_no_display_form]');
  
  HiddenIdObjects.forEach(Toggle);
  
}