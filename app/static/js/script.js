function getLocation() {
  navigator.geolocation.getCurrentPosition(function(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    window.location.href = `/?lat=${lat}&lon=${lon}`;
  });
}

function toggleUnits() {
  const currentUrl = new URL(window.location.href);
  const currentUnits = currentUrl.searchParams.get("units") || "metric";
  const newUnits = currentUnits === "metric" ? "imperial" : "metric";
  currentUrl.searchParams.set("units", newUnits);
  window.location.href = currentUrl.toString();
}

