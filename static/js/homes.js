

$(document).ready(function () {
    //initiate Google Maps

    const homeMarkers =[];
    homes();
    //make a hover event
    $('.markers').hover(
        // mouse in
            function () {
                // first we need to know which <div class="marker"></div> we hovered
                let index = $('.markers').index(this);
                homeMarkers[index].setIcon(highlightedIcon());
            },
            // mouse out
            function() {
                // first we need to know which <div class="marker"></div> we hovered
                let index = $('.markers').index(this);
                homeMarkers[index].setIcon(normalIcon());        
            }
    );

    

    function homes() {
    // map showing on homes.html 
    
        //creates map 
        const searchMap = new google.maps.Map(
            document.querySelector("#home-map"),{
                center: new google.maps.LatLng(0,0),
                zoom: 15,
                mapId: 'e54bf19c5f6ff97',
            },
            );     
        // using to center map by markers
        var bounds = new google.maps.LatLngBounds();
        
        //looping over search results, and places marker at each home by lat & long 
        for (const home of data) {

            let latLng = new google.maps.LatLng(home.latitude, home.longitude);

            const homeMarker = new google.maps.Marker({
                position: latLng,
                icon: normalIcon(),
                map: searchMap
            });

            homeMarkers.push(homeMarker);

            const homeContent = (
            "<div id='homeContent'>" +
                `<b1> ${home.rawAddress}</b1><br>` +
                `<b2> <img src='https://maps.googleapis.com/maps/api/streetview?size=600x300&location=${home.latitude},${home.longitude}&heading=151.78&pitch=-0.76&key=AIzaSyCo9kZSGr66VUlUwXP7odZ3fv0XuVBI4q0&'> </b2>` +
            "</div>");

            const homeWindow = new google.maps.InfoWindow({
                content: homeContent,
            });
            //shows home address info window when homemarker clicked
            homeMarker.addListener("click", () => {
                homeWindow.open({
                    anchor: homeMarker,
                    shouldFocus: false,
                })
            });

            //extends map bounderies based on each home marker
            bounds.extend(latLng);

        }
        //impliments map boundries so all markers are in view
        searchMap.fitBounds(bounds);
    }
     
    function normalIcon() {
        return {
        url: '/static/icons/businesses.png'
        };
    }
    function highlightedIcon() {
        return {
        url: '/static/icons/saved.png'
        };
    }
});
