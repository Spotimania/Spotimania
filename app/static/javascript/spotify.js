var accessToken;


//Gets the spotify access token
$.ajax({
	url: "https://spotify-token-authenticator.frinzelapuz.now.sh/api/token",
	type: 'GET',
	        dataType: 'json', // added data type
	        success: function(data) {
	        	console.log(data.accessToken);
	        	accessToken = data.accessToken;
	        }
	    });



//search by artist name
window.onload=function(){
	var el = document.getElementById('submitArtist');
	if (el){
		document.querySelector("#submitArtist").addEventListener("click", function(event) {
			document.getElementById('results').innerHTML=('')
			event.preventDefault();
	//ajax call to get data for artist
	$.ajax({
		url: "https://api.spotify.com/v1/search?q=" + $('#artist').val() + '&type=artist',
		type: 'GET',
		contentType: 'application/json',
		headers: {
			"Authorization": "Bearer " + accessToken
		},
		success: function(data) {

			for (i=0;i<data.artists.items.length;i++) {
				document.getElementById('results').innerHTML+=("<li><button class='artistname' type='button'>"+(data.artists.items[i].name)+"</button></li>");
			}
			$('.artistname').click(function(event) {
				document.getElementById('results').innerHTML=('')
				var target = event.target || event.srcElement;
				var name = target.innerHTML;

				for (i=0;i<data.artists.items.length;i++) {

					if (name == data.artists.items[i].name) {
						console.log(data.artists.items[i].id);
						id = data.artists.items[i].id;
  							//ajax call to get top 10 tracks for artist
  							$.ajax({
  								url: "https://api.spotify.com/v1/artists/" + id + "/top-tracks?country=AU",
  								type: "GET",
  								contentType: "application/json",
  								headers: {
  									"Authorization": "Bearer " + accessToken
  								},
  								success: function(data) {
  									for (i=0;i<data.tracks.length;i++) {
  										document.getElementById('results').innerHTML+=("<li><input class='tracks' type='submit' value='"+(data.tracks[i].name)+"'></li>");
  									}
  									$('.tracks').click(function(event) {
  										var target = event.target || event.srcElement;
  										var name = target.value;
  										target.style.display='none';
  										for (i=0;i<data.tracks.length;i++) {

  											if (name == data.tracks[i].name) {
  											//ajax call to get data for specific track
  											$.ajax({
  												url: "https://api.spotify.com/v1/tracks/" + data.tracks[i].id + "?market=au",
  												type: "GET",
  												contentType: "application/json",
  												headers: {
  													"Authorization": "Bearer " + accessToken
  												},
  												success: function(data) {
  													console.log(data);
					                 				//ajax call to post track data
					                 				$.ajax({
					                 					url: "/playlist",
					                 					type: "POST",
					                 					contentType: "application/json",
					                 					dataType: 'json',
					                 					data: JSON.stringify({
					                 						spotifySongID: data.id,
					                 						prevURL: data.preview_url,
					                 						prevIMG: data.album.images[0].url,
					                 						songName: data.name,
					                 						artist: data.album.artists[0].name,
					                 						album: data.album.name,
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

//search by track name
	var el = document.getElementById('submitTrack');
	if (el){
		document.querySelector("#submitTrack").addEventListener("click", function(event) {
			document.getElementById('results').innerHTML=('')
			event.preventDefault();
		
		$.ajax({
			url: "https://api.spotify.com/v1/search?q=" + $('#track').val() + '&type=track',
			type: 'GET',
			contentType: 'application/json',
			headers: {
				"Authorization": "Bearer " + accessToken
			},
			success: function(data) {
				console.log(data)
				for (i=0;i<data.tracks.items.length;i++) {
					document.getElementById('results').innerHTML+=("<li><button class='songname' type='button'>"+(data.tracks.items[i].name)+"</button></li>");
				}
				$('.songname').click(function(event) {
					var target = event.target || event.srcElement;
					var name = target.innerHTML;
					target.style.display='none';
					console.log(name);
					for (i=0;i<data.tracks.items.length;i++){
  						//ajax call to get data for specific track
  						if (name == data.tracks.items[i].name) {
  							$.ajax({
  								url: "/playlist",
  								type: "POST",
  								contentType: "application/json",
  								dataType: 'json',
  								data: JSON.stringify({
  									songID: data.tracks.items[i].id,
  									artist: data.tracks.items[i].album.artists[0].name,
  									songName: data.tracks.items[i].name,
  									prevIMG: data.tracks.items[i].album.images[0].url,
  									prevURL: data.tracks.items[i].preview_url,
  									album: data.tracks.items[i].album.name,
  										})

  									});
  							}
  						}
  					});
				}
			});
		})
	}
}


