(function () {
  const isLocal = location.protocol === "file:";

  if (isLocal) {
    // Local: define config from JS file
    const script = document.createElement("script");
    script.src = "./local_viewer_config.js";
    script.onload = () => {
      if (typeof localViewerConfig !== "undefined") {
        window.viewerConfig = localViewerConfig;
      } else {
        console.error("❌ localViewerConfig not found in local_viewer_config.js");
      }
    };
    script.onerror = () => {
      console.error("❌ Failed to load local_viewer_config.js");
    };
    document.head.appendChild(script);
  } else {
    // Remote: fetch JSON config
    fetch("./remote_viewer_config.json")
      .then(res => res.json())
      .then(remoteConfig => {
        window.viewerConfig = remoteConfig;
      })
      .catch(err => {
        console.error("❌ Failed to load remote_viewer_config.json:", err);
      });
  }
})();
