var locations = [
    [`EUROMEDIK Bolnica - Pariske komune 22`, 44.8296676, 20.4011574, 4, `https://www.google.com/maps/dir/?api=1&destination=44.8296676,20.4011574`],
    [`EUROMEDIK Bolnica - Višegradska 20`, 44.8007873, 20.4553052, 4, `https://www.google.com/maps/dir/?api=1&destination=44.8007873,20.4553052`],
    [`EUROMEDIK Bolnica i stacionar - Bulevar Umetnosti 29`, 44.8148118, 20.4114995, 4, `https://www.google.com/maps/dir/?api=1&destination=44.8148118,20.4114995`],
    [`Dom zdravlja EUROMEDIK - Kosovska 12`, 44.8432452, 20.4141855, 5, `https://www.google.com/maps/dir/?api=1&destination=44.8432452,20.4141855`],
    [`Dom zdravlja EUROMEDIK - Gandijeva 122G`, 44.8044156, 20.3850326, 5, `https://www.google.com/maps/dir/?api=1&destination=44.8044156,20.3850326`],
    [`Dom zdravlja EUROMEDIK - Zrmanjska 8a, Banovo Brdo`, 44.7847704, 20.4192865, 3, `https://www.google.com/maps/dir/?api=1&destination=44.7847704,20.4192865`],
    [`Dom zdravlja EUROMEDIK - Alekse Nenadovića 7`, 44.8023888, 20.4688402, 3, `https://www.google.com/maps/dir/?api=1&destination=44.8023888,20.4688402`],
    [`Dom zdravlja EUROMEDIK - Alekse Nenadovića 8`, 44.8023861, 20.4689874, 3, `https://www.google.com/maps/dir/?api=1&destination=44.8023861,20.4689874`],
    [`Dom zdravlja EUROMEDIK - Stefana Prvovenčanog 32`, 44.7856183, 20.4772976, 3, `https://www.google.com/maps/dir/?api=1&destination=44.7856183,20.4772976`],
    [`Dom zdravlja EUROMEDIK - Cvijićeva 32`, 44.8156388, 20.4770645, 3, `https://www.google.com/maps/dir/?api=1&destination=44.8156388,20.47706455`],
];

var map = new google.maps.Map(document.getElementById(`map`), {
    zoom: 12,
    center: new google.maps.LatLng(44.8091957, 20.4309735),
    mapTypeId: google.maps.MapTypeId.ROADMAP
});

var infowindow = new google.maps.InfoWindow();

var marker, i;

for (i = 0; i < locations.length; i++) {
    marker = new google.maps.Marker({
        position: new google.maps.LatLng(locations[i][1], locations[i][2]),
        map: map,
        url: locations[i][4]
    });

    google.maps.event.addListener(marker, `click`, (function (marker, i) {
        return function () {    
            infowindow.setContent('<a target="_blank" href="' + locations[i][4] + '">' + locations[i][0] + '</a>');
            infowindow.open(map, marker);
        };
    })(marker, i));
}