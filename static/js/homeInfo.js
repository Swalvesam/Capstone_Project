


$(document).ready(function () {
    // Quill editor for home notes
    const quill = new Quill('#editor-container', {
        modules: {
          toolbar: [
            ['bold', 'italic'],
            ['link', 'blockquote', 'code-block', 'image'],
            [{ list: 'ordered' }, { list: 'bullet' }]
          ]
        },
        placeholder: 'Love the Kitchen! Close to Restaurants...',
        theme: 'snow'
      });
    //pulls note body to then return in server.py to add note to database
    const form = document.querySelector('#add_home_note');
    console.log(form)
      form.onsubmit = function() {
        // Populate hidden form on submit
        const note = document.querySelector('input[name=note]');
        note.value = quill.root.innerHTML;
      };
    


    const busMarkers = [];
    const busDict = [];
    //creating a busDictionary 
    for(const bus of businesses) {
        busDict.push( {
        title: bus[0],
        url: bus[2],
        lat: bus[5].latitude,
        lng: bus[5].longitude,
        })
    }

    //initiate Google Maps
    initMap();

    //make a hover event
    $('.markers').hover(
    // mouse in
        function () {
            // first we need to know which <div class="marker"></div> we hovered
            let index = $('.markers').index(this);
            busMarkers[index].setIcon(highlightedIcon());
        },
        // mouse out
        function() {
            // first we need to know which <div class="marker"></div> we hovered
            let index = $('.markers').index(this);
            busMarkers[index].setIcon(normalIcon());        
        }
    );


    //create variable to access outside of function
    let homeMap;

    function initMap() {
        //map that works on home_info.html
        const savedHomeCoords = {
            lat: homeLatitude,
            lng: homeLongitude
        };
        
        let mapOptions = {        
            center: savedHomeCoords,
            zoom: 13,
            mapId: 'e54bf19c5f6ff97',
        };

        const homeMap = new google.maps.Map(document.querySelector('#map'), mapOptions)
        


        for (const bus of busDict) {
            const newMarker = new google.maps.Marker({
                position: new google.maps.LatLng(bus.lat, bus.lng),
                title: bus.title,
                icon: normalIcon(),
                map: homeMap
                })
            busMarkers.push (newMarker);
            
            const busContent = 
            '<div id="busContent">' +
                `<b1> ${bus.title} </b1><br>` +
                `<a href= ${bus.url}>View on Yelp</a>` +
            '</div>';
        
            let busWindow = new google.maps.InfoWindow({
                content: busContent,
            });

            //open info window when bus is clicked on
            newMarker.addListener("click", () => {
                    busWindow.open({
                        anchor: newMarker,
                        map,
                        shouldFocus: false,
                    });
            });
        };

            
        const homeMarker = new google.maps.Marker({
            position: savedHomeCoords,
            icon: "/static/icons/home.png",
            map: homeMap
        });
        
        const homeView = new google.maps.StreetViewPanorama (
            document.getElementById("pano"),
            {
                position: savedHomeCoords,
                pov: {
                    heading: 0,
                    pitch: 0,
                },
            }
        );
        homeMap.setStreetView(homeView);

    };

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


