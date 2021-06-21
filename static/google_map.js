//API calls to enable Google maps on html pages


function initMap() {

    //code that works with google maps
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

