//API calls to enable Google maps on html pages


function initMap() {

    //map that works on home_info.html
    const savedHomeCoords = {
        lat: homeLatitude,
        lng: homeLongitude
    };
    

    const homeMap = new google.maps.Map(
        document.querySelector('#map'),
        {
            center: savedHomeCoords,
            zoom: 15
        }
    );

    const homeMarker = new google.maps.Marker({
        position: savedHomeCoords,
        icon: "/static/icons/home.png",
        map: homeMap
    });

    
    for (const bus of businesses) {
        const busMarker = new google.maps.Marker({
            position: {lat: bus[5].latitude, lng: bus[5].longitude},
            icon: "/static/icons/businesses.png",
            map: homeMap

        });

        const busContent = 
        '<div id="busContent">' +
            `<b1> ${bus[0]} </b1><br>` +
            `<a href= ${bus[2]}>View on Yelp</a>` +
        '</div>';

        const busWindow = new google.maps.InfoWindow({
            content: busContent,
        });

        busMarker.addListener("click", () => {
            busWindow.open({
                anchor: busMarker,
                map,
                shouldFocus: false,
            });

        });

    }
    
    const homeView = new google.maps.StreetViewPanorama (
        document.getElementById("pano"),
        {
            position: savedHomeCoords,
            pov: {
                heading: 34,
                pitch: 10,
            },
        }
    );
    homeMap.setStreetView(homeView);

};


function homes() {
    // map showing on homes.html 
    
    //creates map 
    const searchMap = new google.maps.Map(
        document.querySelector("#home-map"),{
            center: new google.maps.LatLng(0,0),
            zoom: 15,
        },
        );     
    // using to center map by markers
    var bounds = new google.maps.LatLngBounds();
    
    //looping over search results, and places marker at each home by lat & long 
    for (const home of data) {

        let latLng = new google.maps.LatLng(home.latitude, home.longitude);

        const homeMarker = new google.maps.Marker({
            position: latLng,
            icon: "/static/icons/home.png",
            map: searchMap
        });


        const homeContent = 
        '<div id="homeContent">' +
            `<b1> ${home.rawAddress} </b1><br>` +
        '</div>';

        const homeWindow = new google.maps.InfoWindow({
            content: homeContent,
        });

        homeMarker.addListener("click", () => {
            homeWindow.open({
                anchor: homeMarker,
                shouldFocus: false,
            })
        });
        //extends map view based on each home marker
        bounds.extend(latLng);
    }
    //enables map size to view all markers
    searchMap.fitBounds(bounds);

};
// function directions() {
//     // map showing on users.html 
//     // get directions from user current location to saved business

// try this code for get directions
// if (navigator.geolocation) {
//     navigator.geolocation.getCurrentPosition(function (position) {
//         initialLocation = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
//         map.setCenter(initialLocation);
//     });
// }

// };