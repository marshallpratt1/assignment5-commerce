document.addEventListener('DOMContentLoaded', function() {
    //update_stats();
    //setInterval(update_stats, 2000);
    });
    

function watchlist() {
    if (document.querySelector('#watch').src == "https://cdn-icons-png.flaticon.com/512/1077/1077035.png"){
    document.querySelector('#watch').src = "https://cdn-icons-png.flaticon.com/512/2077/2077502.png";
}
else {
    document.querySelector('#watch').src = "https://cdn-icons-png.flaticon.com/512/1077/1077035.png";
}
};


function update_stats() {  
        fetch("/api/status")
        .then(response => response.json())
        .then(data => {
            document.querySelector('#al').innerHTML = data['active_listings']
        });
    }