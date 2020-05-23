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
		deleteSongDom(e.id);
		console.log('Successfully Deleted');
	} catch (err) {
		console.log(err);
	}
};

const deleteSongDom = (songId) => {
	$(`#${songId}`).remove();
};

const searchSong = async (e) => {
	document.getElementById('results').innerHTML = '';
	document.getElementById('RSDescription').innerHTML = 'Loading...';

	let searchOption = $('#artistOption').val();
	if ($('#trackOption').prop('checked')) {
		searchOption = $('#trackOption').val();
	}
	console.log(searchOption);

	const searchInput = $('#searchInput').val();

	const responseData = await (await spotifyFetchAPI(`search?q=${searchInput}&type=${searchOption}`)).json();
	console.log(responseData);
	if (searchOption === 'artist') {
		responseData.artists.items.forEach((artist) => {
			document.getElementById('RSDescription').innerHTML = 'Click on Artist to Show their Top Songs...';
			if (artist.images.length == 0) {
				document.getElementById('results').innerHTML += 
				`<li class="searchResultList">
					<button type="button" class="inputSubmit" onclick="onClickNavigateArtist('${artist.id}')" style="font-size: 20px;">
						${artist.name}
					</button>
				</li>`;
			}
			else {
				document.getElementById('results').innerHTML += 
				`<li class="searchResultList">
					<button type="button" class="inputSubmit" onclick="onClickNavigateArtist('${artist.id}')" style="font-size: 20px;">
						<img src="${artist.images[0].url}" class="artistArt">
						${artist.name}
					</button>
				</li>`;
			}
		});
	} else if (searchOption === 'track') {
		responseData.tracks.items.forEach((track) => {
			document.getElementById('RSDescription').innerHTML = 'Click on Song to Add to Playlist...';
			document.getElementById('results').innerHTML += 
			`<li class="searchResultList">
				<button class='inputSubmit' id='${track.id}' onclick="onClickTrack('${track.id}')">
				${track.name}
				</button>
			</li>`;
		});
	}
};

const onClickNavigateArtist = async (id) => {
	document.getElementById('results').innerHTML = '';
	document.getElementById('RSDescription').innerHTML = 'Loading...';
	const responseData = await (await spotifyFetchAPI(`artists/${id}/top-tracks?country=AU`)).json();
	console.log(responseData);
	responseData.tracks.forEach((track) => {
		document.getElementById('RSDescription').innerHTML = 'Click on Song to Add to Playlist...';
		document.getElementById('results').innerHTML += 
		`<li class="searchResultList">
			<button class='inputSubmit' id='${track.id}' onclick="onClickTrack('${track.id}');">
				${track.name}
			</button>
		</li>`;
	});
};

const onClickTrack = async (id) => {
	const data = await (await spotifyFetchAPI(`tracks/${id}?market=au`)).json();
	console.log(data);
	var songElement = document.getElementById(`${id}`);
	songElement.style.display = 'none';
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
		addSongDom(payload);
		console.log('SUCCESS');
	} catch (err) {
		console.log(err);
	}
};

const addSongDom = ({ spotifySongID, prevURL, prevIMG, songName, artist, album }) => {
	const playlistId = sessionStorage.getItem('playlistId');
	const container = document.querySelector('#forloop');
	container.innerHTML += `				<div id="${spotifySongID}">
					<div class="avatar-root">
						<img class="avatar" src="${prevIMG}" alt="" />
					</div>
					<p>${songName}</p>
					<p>${artist}</p>
					<audio controls>
						<source src="${prevURL}" />
						Your browser does not support the audio element.
					</audio>
					<a id="${spotifySongID}" onclick="deleteSong(this,'${playlistId}')"><i class="fa fa-trash" aria-hidden="true"></i></a>
				</div>
				`;
};
