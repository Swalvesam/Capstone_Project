//API calls to enable Google maps on html pages
console.log(homeLongitude)

function initMap() {
    console.log("trying to init map!!")
    //code that works with google maps
    const savedHomeCoords = {
        lat: homeLatitude,
        lng: homeLongitude
    };
    
    console.log(savedHomeCoords)
    const homeMap = new google.maps.Map(
        document.querySelector('#map'),
        {
            center: savedHomeCoords,
            zoom: 15
        }
    );

    const homeMarker = new google.maps.Marker({
        position: savedHomeCoords,
        // label: homeTitle,
        map: homeMap
    });

    homeMarker.addListener('click', () => {
        alert(homeTitle)
    })

    const homeInfo = new google.maps.InfoWindow({
        content: `<p1>${homeTitle}</p1>`,
    });
    
    homeInfo.open(homeMap, homeMarker);




};

