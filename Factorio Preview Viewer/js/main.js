const tabButtonsContainer = document.querySelector(".tab-buttons");
const mapImage = document.getElementById("mapImage");
const mapContainer = document.getElementById("mapContainer");
const zoomDisplay = document.getElementById("zoomDisplay");
const resetBtn = document.getElementById("resetView");

setupTabs(planetConfig, tabButtonsContainer, mapImage);
setInitialPlanet(mapImage);
initKeyboardControls(mapImage, mapContainer, zoomDisplay);

resetBtn.addEventListener("click", () => {
  resetMapView(mapImage, mapContainer, zoomDisplay);
});
