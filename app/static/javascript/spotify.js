var accessToken;



$.ajax({
	        url: "https://spotify-token-authenticator.frinzelapuz.now.sh/api/token",
	        type: 'GET',
	        dataType: 'json', // added data type
	        success: function(data) {
	            console.log(data.accessToken);
	            accessToken = data.accessToken;
	        }
	    });



var id;
window.onload=function(){
var el = document.getElementById('submit');
if (el){
document.querySelector("#submit").addEventListener("click", function(event) {
	document.getElementById('artists').innerHTML=('')
	event.preventDefault();
	$.ajax({
          url: "https://api.spotify.com/v1/search?q=" + $('#tracks').val() + '&type=artist',
          type: 'GET',
          contentType: 'application/json',
          headers: {
                    "Authorization": "Bearer " + accessToken
                 },
          success: function(data) {
	            console.log(data);
	            for (i=0;i<data.artists.items.length;i++) {
	            	document.getElementById('artists').innerHTML+=("<li><button class='artistname' type='button'>"+(data.artists.items[i].name)+"</button></li>");
	            }
	            $('.artistname').click(function(event) {
	            	document.getElementById('artists').innerHTML=('')
	            	var target = event.target || event.srcElement;
	            	var name = target.innerHTML;
	            	
  					for (i=0;i<data.artists.items.length;i++) {

  						if (name == data.artists.items[i].name) {
  							console.log(data.artists.items[i].id);
  							id = data.artists.items[i].id;
  							$.ajax({
  							url: "https://api.spotify.com/v1/artists/" + id + "/top-tracks?country=AU",
  							type: "GET",
  							contentType: "application/json",
  							headers: {
                    		"Authorization": "Bearer " + accessToken
                 				},
                 			success: function(data) {
                 				for (i=0;i<data.tracks.length;i++) {
	            					document.getElementById('artists').innerHTML+=("<li><input class='tracks' type='submit' value='"+(data.tracks[i].name)+"'></li>");
	            				}
	            				$('.tracks').click(function(event) {
	            					document.getElementById('tracks').innerHTML=('')
					            	var target = event.target || event.srcElement;
					            	var name = target.value;
					            	console.log(name)
					            	for (i=0;i<data.tracks.length;i++) {

  										if (name == data.tracks[i].name) {
  											console.log(data.tracks[i].id)
  											$.ajax({
					  							url: "https://api.spotify.com/v1/tracks/" + data.tracks[i].id + "?market=au",
					  							type: "GET",
					  							contentType: "application/json",
					  							headers: {
					                    		"Authorization": "Bearer " + accessToken
					                 				},
					                 			success: function(data) {
					                 				$.ajax({
							  							url: "/process",
							  							type: "POST",
							  							contentType: "application/json",
							  							dataType: 'json',
							  							data: JSON.stringify({
							  								songName: data.name,
							  								songID: data.id,
							  								prevURL: data.preview_url,
							  							})

					                 					});
					                 			}
				                 			});
  										}
  									}
	            				});
	            	
                 				console.log(data);

                 			}
                 			});

  						}
  						
  					}
				});

	        }
          
            });
        });
}
}
