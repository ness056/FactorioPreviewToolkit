const viewerConfig = {
  planetPreviewSources: {
    nauvis: "https://dl.dropboxusercontent.com/scl/fi/1nrx5ovnnywacduf6zqxi/nauvis.png?rlkey=xqwa3xs31e4bm09n23xbawo9x",
    vulcanus: "https://dl.dropboxusercontent.com/scl/fi/8amgdmea6ngowkuf3ar9d/vulcanus.png?rlkey=54t749jwvckzmh4d6mugjr5wb",
    gleba: "https://dl.dropboxusercontent.com/scl/fi/q8tokblpjo8nqbxmyyhcl/gleba.png?rlkey=lv4bqvznhykc8o5psoyp078za",
    fulgora: "https://dl.dropboxusercontent.com/scl/fi/y9sjsy08kipoq985bpqc0/fulgora.png?rlkey=jphe3e7e2m4u8wl05j5r6e6z3",
    aquilo: "https://dl.dropboxusercontent.com/scl/fi/dnt8n2f63xq2z1xtonhuz/aquilo.png?rlkey=gqaxchtp320u90yfjiwt4yjhr",
  },
  planetNamesSource: "https://dl.dropboxusercontent.com/scl/fi/2yarwux3apgfdwqe50uys/remote_planet_names.json?rlkey=s54eg4dw8cbawwr95a24bhpnb",

  // Composite "Overview" tab: one large planet on the left (~2/3 width),
  // the rest stacked top-to-bottom on the right (~1/3 width). The Overview
  // tab is shown only when at least one of these side planets is available
  // (i.e. it is skipped for vanilla / non-Space-Age maps).
  overview: {
    main: "nauvis",
    side: ["gleba", "aquilo"]
  },

  // Tab selected on load: "overview", a planet name (e.g. "nauvis"), or
  // "auto" (overview when available, otherwise the first planet). Falls back
  // gracefully when the requested tab isn't available.
  defaultTab: "overview",

  // Zoom for the overview's side cells, as a multiple of the "fill the cell"
  // baseline (1 = just fill, higher = zoom in). `default` applies to any side
  // planet not listed here. Planet tabs and the overview's main planet
  // (Nauvis) stay at the upstream default and are not affected by this.
  defaultZoom: {
    default: 3.5,
    aquilo: 7
  }
};
