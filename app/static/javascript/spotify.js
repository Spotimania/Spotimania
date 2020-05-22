var accessToken;

//Gets the spotify access token
$.ajax({
	url: 'https://spotify-token-authenticator.frinzelapuz.now.sh/api/token',
	type: 'GET',
	dataType: 'json', // added data type
	success: function (data) {
		console.log(data.accessToken);
		accessToken = data.accessToken;
	},
});

const sameOriginAPI = (
	endpoint = '',
	body = {},
	method = 'POST',
	headers = {
		'Content-Type': 'application/json',
	}
) => {
	return fetch(`/api/${endpoint}`, { headers, method, body: JSON.stringify(body) });
};

const spotifyFetchAPI = (
	query = '',
	method = 'GET',
	headers = {
		Accept: 'application/json',
		'Content-Type': 'application/json',
		Authorization: 'Bearer ' + accessToken,
	}
) => {
	return fetch(`https://api.spotify.com/v1/${query}`, { headers, method });
};

const deleteSong = async (e, playlistId) => {
	try {
		sameOriginAPI(`playlist/${playlistId}/${e.id}`, (body = {}), (method = 'DELETE'));
		console.log('Successfully Deleted');
	} catch (err) {
		console.log(err);
	}
};

const searchSong = async (e) => {
	document.getElementById('results').innerHTML = '';
	const searchOption = $('#searchOption').val();
	const searchInput = $('#searchInput').val();

	const responseData = await (await spotifyFetchAPI(`search?q=${searchInput}&type=${searchOption}`)).json();
	console.log(responseData);
	if (searchOption === 'artist') {
		responseData.artists.items.forEach((item) => {
			document.getElementById(
				'results'
			).innerHTML += `<li><button class='inputSubmit' type='button' onclick="onClickNavigateArtist('${item.id}')">${item.name}</button></li>`;
		});
	} else if (searchOption === 'track') {
		responseData.tracks.items.forEach((track) => {
			document.getElementById(
				'results'
			).innerHTML += `<li><button class='inputSubmit' id='${id}' onclick="onClickTrack('${track.id}')">${track.name}</button></li>`;
		});
	}
};

const onClickNavigateArtist = async (id) => {
	document.getElementById('results').innerHTML = '';
	const responseData = await (await spotifyFetchAPI(`artists/${id}/top-tracks?country=AU`)).json();
	console.log(responseData);
	responseData.tracks.forEach((track) => {
		document.getElementById(
			'results'
		).innerHTML += `<li><button class='inputSubmit' id='${track.id}' onclick="updateDiv(); onClickTrack('${track.id}');">${track.name}</button></li>`;
	});
};

const onClickTrack = async (id) => {
	const data = await (await spotifyFetchAPI(`tracks/${id}?market=au`)).json();
	console.log(data);
	var x = document.getElementById(`${id}`)
	x.style.display = 'none';
	const playlistId = sessionStorage.getItem('playlistId');
	const payload = {
		spotifySongID: data.id,
		prevURL: data.preview_url,
		prevIMG: data.album.images[0].url,
		songName: data.name,
		artist: data.album.artists[0].name,
		album: data.album.name,
	};
	try {
		sameOriginAPI(`playlist/${playlistId}`, payload);
		console.log('SUCCESS');
	} catch (err) {
		console.log(err);
	}
};




