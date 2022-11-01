document.addEventListener('DOMContentLoaded', function() {
    //update_stats();
    //setInterval(update_stats, 2000);
    //document.querySelector('#watchlist_form').onclick = watchlist
    });
    

const watch = document.getElementById('watch')
watch.addEventListener(click, (click)=>{
        
        //console.log(listing_id)
        alert("This alert box was called!!!");
       
        //fetch("/api/watchlist")

        return false;
    });

function watchlist() {
    if (document.querySelector('#watch').src == "https://cdn-icons-png.flaticon.com/512/1077/1077035.png"){
    document.querySelector('#watch').src = "https://cdn-icons-png.flaticon.com/512/2077/2077502.png";
}
else {
    document.querySelector('#watch').src = "https://cdn-icons-png.flaticon.com/512/1077/1077035.png";
}
    /*
    if (document.querySelector('#watch').style.backgroundColor == "black"){
        document.querySelector('#watch').style.backgroundColor = "transparent";
    }
    else {
        document.querySelector('#watch').style.backgroundColor = "black";
    }
    */
}

    function update_stats() {  
        fetch("/api/status")
        .then(response => response.json())
        .then(data => {
            document.querySelector('#al').innerHTML = data['active_listings']
        });
    }