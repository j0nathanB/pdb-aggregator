// Privacy-friendly analytics by Plausible.
//
// Mintlify auto-injects any .js file in this directory as a <script> tag
// on every page. We can't drop the original HTML <script> tags directly,
// so we replicate them in JS: set up the Plausible queue shim, call init,
// and dynamically inject the async script tag that loads the library.
//
// The queue pattern (`plausible.q.push(arguments)`) defers any tracking
// calls made before the library loads — order between this file and the
// async script is irrelevant.
(function () {
  window.plausible =
    window.plausible ||
    function () {
      (plausible.q = plausible.q || []).push(arguments);
    };
  plausible.init =
    plausible.init ||
    function (i) {
      plausible.o = i || {};
    };
  plausible.init();

  var script = document.createElement("script");
  script.async = true;
  script.src = "https://plausible.io/js/pa-FJgpRwa8C04_9sJEB6MuY.js";
  document.head.appendChild(script);
})();
