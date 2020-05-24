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
	$(`.card#${songId}`).remove();
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
				document.getElementById('results').innerHTML += `<li class="searchResultList">
					<div class="card text-center text-white bg-dark" style="border-radius: 25px; width: 100%;">
						<div class="card-header">
							<h1 class="card-title inputLabel">${artist.name}</h1>
							<h2 class="card-subtitle text-muted inputLabel"><small>Artist</small></h2>
						</div>
						<div class="card-footer">
							<button type="button" onclick="onClickNavigateArtist('${artist.id}')" class="inputSubmit" style="font-size: 15px;">Get Top Songs</button>
						</div>
					</div>
				</li>`;
			} else {
				document.getElementById('results').innerHTML += `<li class="searchResultList">
					<div class="card text-center text-white bg-dark" style="border-radius: 25px; width: 100%;">
						<div class="card-header">
							<h1 class="card-title inputLabel">${artist.name}</h1>
							<h2 class="card-subtitle text-muted inputLabel"><small>Artist</small></h2>
						</div>
						<div class="card-body">
							<img class="card-img-top artistArt" src="${artist.images[0].url}">
						</div>
						<div class="card-footer">
							<button type="button" onclick="onClickNavigateArtist('${artist.id}')" class="inputSubmit" style="font-size: 15px;">Get Top Songs</button>
						</div>
					</div>
				</li>`;
			}
		});
	} else if (searchOption === 'track') {
		responseData.tracks.items.forEach((track) => {
			document.getElementById('RSDescription').innerHTML = 'Click on Song to Add to Playlist...';
			if (`${track.preview_url}` !== 'null') {
				document.getElementById('results').innerHTML += `<li class="searchResultList">
				<button class='inputSubmit' id='${track.id}' onclick="onClickTrack('${track.id}')">
				${track.name}
				</button>
			</li>`;
			}
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
		if (`${track.preview_url}` !== 'null') {
			document.getElementById('results').innerHTML += `<li class="searchResultList">
			<button class='inputSubmit' id='${track.id}' onclick="onClickTrack('${track.id}');">
				${track.name}
			</button>
		</li>`;
		}
	});
};

const onClickTrack = async (id) => {
	const data = await (await spotifyFetchAPI(`tracks/${id}?market=au`)).json();
	console.log(data);
	var songElement = document.getElementById(`${id}`);
	$(`.inputSubmit#${id}`).remove();
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
	const element = document.querySelector('#forloop');
	const temp = element.innerHTML;
	const toBeAdded = `<div id="${spotifySongID}" class="card text-center text-white bg-dark" style="border-radius: 25px; margin: 10px 0;">
		<div class="card-header">
			<label class="inputLabel" style="font-weight: bold;">${songName}</label>
		</div>
		<div class="card-body">
			<img class="card-img-top artistArt" src="${prevIMG}" style="width: 80%;">
			<br>
			<h4 class="card-title inputLabel" style="font-size: 15px;">by ${artist}</h4>
			<br>
			<a id="${spotifySongID}" onclick=" deleteSong(this,'${playlistId}')" style="font-size: 25px;" class="btn text-muted">
				<i class="fa fa-trash" aria-hidden="true"></i>
			</a>
		</div>
		<div class="card-footer text-muted">
			<audio controls>
				<source src="${prevURL}">
				Your browser does not support the audio element.
			</audio>
		</div>
	</div>`;

	element.innerHTML = toBeAdded + temp;
	element.scrollIntoView();
};
