'use strict';
const MANIFEST = 'flutter-app-manifest';
const TEMP = 'flutter-temp-cache';
const CACHE_NAME = 'flutter-app-cache';
const RESOURCES = {
  "assets/AssetManifest.json": "fdc3205388a03ef275c911bd7f034fee",
"assets/FontManifest.json": "80ee7aa8e2a97688adc3a79f4c13a61c",
"assets/fonts/MaterialIcons-Regular.otf": "e7069dfd19b331be16bed984668fe080",
"assets/lib/asserts/app_icon/icon.png": "9274662457e48aad71c41b161f9ede55",
"assets/lib/asserts/app_icon/icon.svg": "80242d5f6c2ac2ea10fc3c28d487fbad",
"assets/lib/asserts/general_asserts/all.svg": "088cfdfefbef2d9b81826af77ce5ff2a",
"assets/lib/asserts/general_asserts/all_stroke.svg": "2310ae41018a4f2a3372267dbc99d283",
"assets/lib/asserts/general_asserts/apple.svg": "00587615733dd4954be85d8bf79f1d6f",
"assets/lib/asserts/general_asserts/arrow_down.svg": "2a5d887501ac129561d04264b1d5f925",
"assets/lib/asserts/general_asserts/arrow_left.svg": "e1f3d7eec3bd93d089eb5d1753747fae",
"assets/lib/asserts/general_asserts/arrow_right.svg": "e23586423214a5509ece1511497a06e5",
"assets/lib/asserts/general_asserts/arrow_up.svg": "fbc4c061008c271648b3def375275449",
"assets/lib/asserts/general_asserts/battery.svg": "07b370947cf1def84f417295c52610ed",
"assets/lib/asserts/general_asserts/capacity.svg": "b4ada0b789ff3dc067fd0af1b23374ef",
"assets/lib/asserts/general_asserts/check_circle.svg": "4f41f4657e8c35da7b2966df1b462dc9",
"assets/lib/asserts/general_asserts/clock.svg": "c72cfb818dbac334ad8a73a08dd46f45",
"assets/lib/asserts/general_asserts/energy.svg": "785600027031a79ee24ef61847aca9a8",
"assets/lib/asserts/general_asserts/eye-off.svg": "57d3c6b91c6284dbed82639f1c0e452d",
"assets/lib/asserts/general_asserts/eye.svg": "67aefd9108f25cdef3dddddd0d9cc579",
"assets/lib/asserts/general_asserts/facebook.svg": "85a95315742b62a7bf782385a0f6a88c",
"assets/lib/asserts/general_asserts/flashlight.svg": "b0deefc95bfaa9c2c4dd32e583688268",
"assets/lib/asserts/general_asserts/google.svg": "ea735e62c31af39012853c932d74375a",
"assets/lib/asserts/general_asserts/heathy.svg": "21e07f41476d7c880c2a2aefccebc5c7",
"assets/lib/asserts/general_asserts/home.svg": "48b0fb518a95cf5505bf7bbb15524457",
"assets/lib/asserts/general_asserts/humidity.svg": "53d4dc408c31275ad07d7771b213d6df",
"assets/lib/asserts/general_asserts/lightbulb_stroke.svg": "128e9400ef7a56c03ed4a0fc06fef4d6",
"assets/lib/asserts/general_asserts/log-out.svg": "b503eab0ab8f6fa231011828af85bf91",
"assets/lib/asserts/general_asserts/minus.svg": "a88d50bf4ebaf9b08d18bc7fe619afd8",
"assets/lib/asserts/general_asserts/more.svg": "4e2f9a4f9d85fc8417118d4c88710a67",
"assets/lib/asserts/general_asserts/notification.svg": "eb2b4fecc0f4f647ed3079bb4c79d5fe",
"assets/lib/asserts/general_asserts/plus.svg": "28bd189259f9962b4c977809dec1a451",
"assets/lib/asserts/general_asserts/plus_thin.svg": "3631b3c914ea00454d8ec246a1704c18",
"assets/lib/asserts/general_asserts/refresh.svg": "5cdd717252710bf85774bedd2caede10",
"assets/lib/asserts/general_asserts/refreshing_1.svg": "ba685b80ed9431be104ff40b8f6e9489",
"assets/lib/asserts/general_asserts/refreshing_2.svg": "ca69332cc64d9c6b210be1aee28225dd",
"assets/lib/asserts/general_asserts/scanner.svg": "b6a571bd6e09a3477f295df633806959",
"assets/lib/asserts/general_asserts/search.svg": "3e246e32f63adf195b18d0970e1d6b7e",
"assets/lib/asserts/general_asserts/settings.svg": "f13b9526542a0bf1c3c3bba78a438272",
"assets/lib/asserts/general_asserts/sort.svg": "1db96d1c497e2bd7a4c09352305d60bf",
"assets/lib/asserts/general_asserts/suggest.svg": "44a39dadbbd8fdb8c21da885a54c30d6",
"assets/lib/asserts/general_asserts/temperature.svg": "3d9192bb5f73b7e1a47537fcbecb35fc",
"assets/lib/asserts/general_asserts/uncheck_circle.svg": "c381e013d2c2729df4c8fb94fe3dceb1",
"assets/lib/asserts/general_asserts/unheathy.svg": "09b4d9d8d9e45667a813684d0909f2ab",
"assets/lib/asserts/images/demo.jpg": "4482e463509755880fdd7c124ed7fcad",
"assets/lib/asserts/images/device.png": "24a7f893e76a074628521005fcd15fc3",
"assets/lib/asserts/images/device_2.png": "35c9072dabc0f7bf7592cef864060f36",
"assets/lib/asserts/images/device_manage.png": "5cf11e3072e2da059a1820c753d78706",
"assets/lib/asserts/images/food.png": "1ddb71cec6687b5438455a3628a8abe7",
"assets/lib/asserts/images/fridge.png": "97b7e9ae8ba656af8106600c56e7be50",
"assets/lib/asserts/images/heelo.jpg": "faead60b1423634ebf9a30bb2b2fcbc6",
"assets/lib/asserts/images/rcm_dish.png": "33d67799417a4d92c78bf194eda08818",
"assets/lib/asserts/images/rcm_meal.png": "06d68e67822c848352cef3b377d25abe",
"assets/lib/asserts/images/take_igd.png": "b720104fabe781b3865a7e691e0c1910",
"assets/lib/fonts/Gilroy/Gilroy-Black.otf": "91508b3f0beef57e1e54b407b0343020",
"assets/lib/fonts/Gilroy/Gilroy-BlackItalic.otf": "59f76af44fc0b60bc5ca1ac226d92462",
"assets/lib/fonts/Gilroy/Gilroy-Bold.otf": "83a4e50a248e2b9da6b2e6802834646d",
"assets/lib/fonts/Gilroy/Gilroy-BoldItalic.otf": "3f40c274ef9c091c68e34d74e4f104e5",
"assets/lib/fonts/Gilroy/Gilroy-ExtraBold.otf": "c37c61167ee0b1b418f983f2f9a180b5",
"assets/lib/fonts/Gilroy/Gilroy-ExtraBoldItalic.otf": "ce2a7b77ebd0d680953e8e1f8963a8e7",
"assets/lib/fonts/Gilroy/Gilroy-ExtraLight.otf": "8bd3fe58633f8bc4b21e081ce4f8cddd",
"assets/lib/fonts/Gilroy/Gilroy-ExtraLightItalic.otf": "4f186c7835190684e3d489ccb59bc220",
"assets/lib/fonts/Gilroy/Gilroy-Light.otf": "500ee3f8d1beb34b515976e9b27e3706",
"assets/lib/fonts/Gilroy/Gilroy-LightItalic.otf": "c5e9ddb27b3a84f9a2a8aa1879794a50",
"assets/lib/fonts/Gilroy/Gilroy-Medium.otf": "1ae06bc5340fe8ecc9689f7435f4d57e",
"assets/lib/fonts/Gilroy/Gilroy-MediumItalic.otf": "ebefcaca02270f061c6a55d57e0e31a7",
"assets/lib/fonts/Gilroy/Gilroy-Regular.otf": "6655e711b71fad445f2fc2e071ea6f5b",
"assets/lib/fonts/Gilroy/Gilroy-RegularItalic.otf": "c3768e33f44d61c676a0247eeb2e5b70",
"assets/lib/fonts/Gilroy/Gilroy-SemiBold.otf": "82e5334b9753f83c1a97ac8419ee3c71",
"assets/lib/fonts/Gilroy/Gilroy-SemiBoldItalic.otf": "7bc3fa7432dbbe53aca7f864d9352845",
"assets/lib/fonts/Gilroy/Gilroy-Thin.otf": "d77450bfee1e54ea478b559bc390d078",
"assets/lib/fonts/Gilroy/Gilroy-ThinItalic.otf": "cfcf7956ff37267687c865cf4c6b0326",
"assets/NOTICES": "c184c3aef738e252de9b54b21d390ee2",
"canvaskit/canvaskit.js": "97937cb4c2c2073c968525a3e08c86a3",
"canvaskit/canvaskit.wasm": "3de12d898ec208a5f31362cc00f09b9e",
"canvaskit/profiling/canvaskit.js": "c21852696bc1cc82e8894d851c01921a",
"canvaskit/profiling/canvaskit.wasm": "371bc4e204443b0d5e774d64a046eb99",
"favicon.png": "5dcef449791fa27946b3d35ad8803796",
"flutter.js": "a85fcf6324d3c4d3ae3be1ae4931e9c5",
"icons/Icon-192.png": "ac9a721a12bbc803b44f645561ecb1e1",
"icons/Icon-512.png": "96e752610906ba2a93c65f8abe1645f1",
"icons/Icon-maskable-192.png": "c457ef57daa1d16f64b27b786ec2ea3c",
"icons/Icon-maskable-512.png": "301a7604d45b3e739efc881eb04896ea",
"index.html": "02896af77c08a5ce1618c7d252f83f8d",
"/": "02896af77c08a5ce1618c7d252f83f8d",
"main.dart.js": "2c846df94f1bf8ae67bd2586364f4045",
"manifest.json": "4b6b5e001327ed513d8e458a14958c13",
"version.json": "70601ec6b406c548fdeed13677fbb0ff"
};

// The application shell files that are downloaded before a service worker can
// start.
const CORE = [
  "main.dart.js",
"index.html",
"assets/AssetManifest.json",
"assets/FontManifest.json"];
// During install, the TEMP cache is populated with the application shell files.
self.addEventListener("install", (event) => {
  self.skipWaiting();
  return event.waitUntil(
    caches.open(TEMP).then((cache) => {
      return cache.addAll(
        CORE.map((value) => new Request(value, {'cache': 'reload'})));
    })
  );
});

// During activate, the cache is populated with the temp files downloaded in
// install. If this service worker is upgrading from one with a saved
// MANIFEST, then use this to retain unchanged resource files.
self.addEventListener("activate", function(event) {
  return event.waitUntil(async function() {
    try {
      var contentCache = await caches.open(CACHE_NAME);
      var tempCache = await caches.open(TEMP);
      var manifestCache = await caches.open(MANIFEST);
      var manifest = await manifestCache.match('manifest');
      // When there is no prior manifest, clear the entire cache.
      if (!manifest) {
        await caches.delete(CACHE_NAME);
        contentCache = await caches.open(CACHE_NAME);
        for (var request of await tempCache.keys()) {
          var response = await tempCache.match(request);
          await contentCache.put(request, response);
        }
        await caches.delete(TEMP);
        // Save the manifest to make future upgrades efficient.
        await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
        return;
      }
      var oldManifest = await manifest.json();
      var origin = self.location.origin;
      for (var request of await contentCache.keys()) {
        var key = request.url.substring(origin.length + 1);
        if (key == "") {
          key = "/";
        }
        // If a resource from the old manifest is not in the new cache, or if
        // the MD5 sum has changed, delete it. Otherwise the resource is left
        // in the cache and can be reused by the new service worker.
        if (!RESOURCES[key] || RESOURCES[key] != oldManifest[key]) {
          await contentCache.delete(request);
        }
      }
      // Populate the cache with the app shell TEMP files, potentially overwriting
      // cache files preserved above.
      for (var request of await tempCache.keys()) {
        var response = await tempCache.match(request);
        await contentCache.put(request, response);
      }
      await caches.delete(TEMP);
      // Save the manifest to make future upgrades efficient.
      await manifestCache.put('manifest', new Response(JSON.stringify(RESOURCES)));
      return;
    } catch (err) {
      // On an unhandled exception the state of the cache cannot be guaranteed.
      console.error('Failed to upgrade service worker: ' + err);
      await caches.delete(CACHE_NAME);
      await caches.delete(TEMP);
      await caches.delete(MANIFEST);
    }
  }());
});

// The fetch handler redirects requests for RESOURCE files to the service
// worker cache.
self.addEventListener("fetch", (event) => {
  if (event.request.method !== 'GET') {
    return;
  }
  var origin = self.location.origin;
  var key = event.request.url.substring(origin.length + 1);
  // Redirect URLs to the index.html
  if (key.indexOf('?v=') != -1) {
    key = key.split('?v=')[0];
  }
  if (event.request.url == origin || event.request.url.startsWith(origin + '/#') || key == '') {
    key = '/';
  }
  // If the URL is not the RESOURCE list then return to signal that the
  // browser should take over.
  if (!RESOURCES[key]) {
    return;
  }
  // If the URL is the index.html, perform an online-first request.
  if (key == '/') {
    return onlineFirst(event);
  }
  event.respondWith(caches.open(CACHE_NAME)
    .then((cache) =>  {
      return cache.match(event.request).then((response) => {
        // Either respond with the cached resource, or perform a fetch and
        // lazily populate the cache only if the resource was successfully fetched.
        return response || fetch(event.request).then((response) => {
          if (response && Boolean(response.ok)) {
            cache.put(event.request, response.clone());
          }
          return response;
        });
      })
    })
  );
});

self.addEventListener('message', (event) => {
  // SkipWaiting can be used to immediately activate a waiting service worker.
  // This will also require a page refresh triggered by the main worker.
  if (event.data === 'skipWaiting') {
    self.skipWaiting();
    return;
  }
  if (event.data === 'downloadOffline') {
    downloadOffline();
    return;
  }
});

// Download offline will check the RESOURCES for all files not in the cache
// and populate them.
async function downloadOffline() {
  var resources = [];
  var contentCache = await caches.open(CACHE_NAME);
  var currentContent = {};
  for (var request of await contentCache.keys()) {
    var key = request.url.substring(origin.length + 1);
    if (key == "") {
      key = "/";
    }
    currentContent[key] = true;
  }
  for (var resourceKey of Object.keys(RESOURCES)) {
    if (!currentContent[resourceKey]) {
      resources.push(resourceKey);
    }
  }
  return contentCache.addAll(resources);
}

// Attempt to download the resource online before falling back to
// the offline cache.
function onlineFirst(event) {
  return event.respondWith(
    fetch(event.request).then((response) => {
      return caches.open(CACHE_NAME).then((cache) => {
        cache.put(event.request, response.clone());
        return response;
      });
    }).catch((error) => {
      return caches.open(CACHE_NAME).then((cache) => {
        return cache.match(event.request).then((response) => {
          if (response != null) {
            return response;
          }
          throw error;
        });
      });
    })
  );
}
