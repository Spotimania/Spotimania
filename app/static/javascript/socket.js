// TIMERS
const setTimer = () => {
	let timeleft = 60;
	const songTimer = setInterval(() => {
		if (timeleft <= 0) {
			clearInterval(songTimer);
			const isSubmitted = sessionStorage.getItem('isSubmitted');
			document.getElementById('countdown').innerHTML = 'Times Up!!!';
			// EMIT SOMETHING IF NOT YET SUBMITTED

			// SESSION STORAGE ONLY STORES STRING
			if (isSubmitted === 'false') {
				submitAnswer();
			}
		} else {
			document.getElementById('countdown').innerHTML = timeleft + ' seconds remaining';
		}
		timeleft -= 1;
	}, 1000);
	window.Timer = songTimer;
};

// WITH MODIFCATION FROM
//https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
const getParameterByName = (name, url = window.location.href) => {
	name = name.replace(/[\[\]]/g, '\\$&');
	var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
		results = regex.exec(url);
	if (!results) return null;
	if (!results[2]) return '';
	return decodeURIComponent(results[2].replace(/\+/g, ' '));
};

// WITH MODIFICATION FROM
//https://www.30secondsofcode.org/blog/s/copy-text-to-clipboard-with-javascript
const getJoinLink = () => {
	//GET RELATED VARIABLES TO GET ROOM
	const userId = sessionStorage.getItem('userId');
	const username = sessionStorage.getItem('username');
	const playlistId = sessionStorage.getItem('playlistId');

	const hiddenCopyElement = document.createElement('textarea');
	hiddenCopyElement.value = `${window.location.href}?room=${userId}Xr00mZ${username}${playlistId}`;

	// HIDE APPENDED ELEMENT
	hiddenCopyElement.setAttribute('readonly', '');
	hiddenCopyElement.style.position = 'absolute';
	hiddenCopyElement.style.left = '-9999px';

	const modal = document.querySelector('#joinModalContent');
	modal.appendChild(hiddenCopyElement);
	hiddenCopyElement.select();

	// COPY TO CLIPBOARD
	document.execCommand('copy');
	modal.removeChild(hiddenCopyElement);

	showToast('Sharing is Caring!!', `Link Has Been Copied To Your Clipboard`);
};

const showToast = (title, message) => {
	// CREEPY ROBOT VOICE RIGHT HERE!!
	// const say = (text) => speechSynthesis.speak(new SpeechSynthesisUtterance(text));
	// say(message);
	const toasts = document.querySelector('#toasts');
	toasts.outerHTML = `<div class="toast" role="alert" aria-live="assertive" aria-atomic="true" id="toasts" style="position: absolute; top: 100px; right: 100px;">
  <div class="toast-header">
    <strong class="mr-auto">${title}</strong>
    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
  <div class="toast-body">
	${message}
  </div>
</div>`;
	$('.toast').toast({ delay: 5000 });
	$('#toasts').toast('show');
};

const notifyUserJoin = (username) => {
	showToast(`A User Has Joined!`, `${username} has joined !`);
};
const notifyScore = (username, newScore, scoreReceived) => {
	showToast('Player Scored', `${username} received ${scoreReceived} points. New score is ${newScore}`);
};

$(document).ready(function () {
	// SHOW STARTING MODAL
	$('#joinModal').modal('show');

	// SET DEFAULT VOLUME OF AUDIO
	const audioPlayer = document.querySelector('#quizAudioPlayer');
	audioPlayer.volume = 0.5;

	//SOCKET CONNECTION
	socket = io.connect('http://' + document.domain + ':' + location.port + '/sockets');

	socket.on('connect', () => {
		// REGISTER ON THE SERVER SESSION
		const userId = sessionStorage.getItem('userId');
		const username = sessionStorage.getItem('username');
		const playlistId = sessionStorage.getItem('playlistId');
		const room = getParameterByName('room') || `${userId}Xr00mZ${username}${playlistId}`;
		sessionStorage.setItem('room', room);
		console.log(room);
		socket.emit('connectFirstTime', { message: "I'm connected! ", userId, username, playlistId, room });
		hideButtonsForNonHost();
	});

	socket.on('onUserJoin', (data) => {
		notifyUserJoin(data.username);
	});
	socket.on('syncUsers', (data) => {
		const users = data.map((user) => ({ ...user, score: 0 }));
		console.log(users);
		sessionStorage.setItem('users', JSON.stringify(users));
		updateScoreBoard();
	});

	socket.on('receivesSongData', (data) => {
		//MODAL INTERACTION
		$('#joinModal').modal('hide');

		//NEED TO DISPLAY SOMETHING
		console.log(data);
		const { prevIMG, prevURL, id, album } = data;
		sessionStorage.setItem('prevIMG', prevIMG);
		sessionStorage.setItem('prevURL', prevURL);
		sessionStorage.setItem('songId', id);
		sessionStorage.setItem('album', album);
		sessionStorage.setItem('isSubmitted', false);

		changeSong(prevURL);
	});
	socket.on('receivesScoreData', (data) => {
		//NEED TO DISPLAY SOMETHING
		console.log('Data Received');
		console.log(data);
		const { scoreReceived, newScore, username, userId } = data;
		notifyScore(username, newScore, scoreReceived);

		// UPDATE SESSION STORAGE
		const users = JSON.parse(sessionStorage.getItem('users'));
		const userToUpdate = users.find((user) => user.userId === userId);
		userToUpdate.score = newScore;

		// CAN ONLY STORE STRING
		sessionStorage.setItem('users', JSON.stringify(users));

		updateScoreBoard();
	});
	socket.on('gameOver', (data) => {
		console.log('GAME OVER');
		gameOver();
	});
	socket.on('ready', () => {
		console.log('All Players Ready');

		//CHANGE TEXT
		const modalTextContent = document.querySelector('#modalTextContent');
		if (isHost()) {
			modalTextContent.textContent = `Press "Next" for Next round`;
		} else {
			modalTextContent.textContent = `Waiting For Host To Press Next`;
		}
		//ENABLE BUTTON
		const primaryButton = document.querySelector('#modalPrimary');
		primaryButton.disabled = false;
	});
});

const startTheGame = () => {
	const room = sessionStorage.getItem('room');
	console.log(room);
	socket.emit('startGame', { room });

	//MODAL INTERACTION
	$('#joinModal').modal('hide');

	// SET THE NEW MODAL
	const modalTitle = document.querySelector('#modalTitle');
	modalTitle.textContent = 'Scoreboard';
	const secondaryButton = document.querySelector('#modalSecondary');
	document.querySelector('#buttonContainer').removeChild(secondaryButton);
	const primaryButton = document.querySelector('#modalPrimary');
	primaryButton.textContent = 'Next';
	primaryButton.onclick = nextSong;
};

const gameOver = () => {
	const userId = sessionStorage.getItem('userId');
	const users = JSON.parse(sessionStorage.getItem('users'));
	const score = users.find((user) => user.userId === userId).score;
	//SCORE
	const modalTextContent = document.querySelector('#modalTextContent');
	modalTextContent.textContent = `The game is finished. You have Scored ${score} points. Thank you for playing the game`;

	//CHANGE BUTTON FUNCTION
	const primaryButton = document.querySelector('#modalPrimary');
	primaryButton.textContent = 'Play Other Playlists';
	primaryButton.onclick = () => (window.location.href = '../');

	//MODAL INTERACTION
	// WORK AROUND - FORCE SHOW
	setTimeout(() => {
		$('#joinModal').modal('show');
	}, 300);

	$('#joinlink').hide();
};

const nextSong = () => {
	const room = sessionStorage.getItem('room');
	console.log('ABCDE');
	socket.emit('nextSong', { room });
};

const changeSong = (prevURL) => {
	const audioPlayer = document.querySelector('#quizAudioPlayer');
	const songPlayer = document.querySelector('#quizSong');
	songPlayer.src = prevURL;

	audioPlayer.volume = 0.5;
	audioPlayer.load();
	audioPlayer.play();

	setTimer();
};

const submitAnswer = () => {
	sessionStorage.setItem('isSubmitted', true);
	const userId = sessionStorage.getItem('userId');
	const room = sessionStorage.getItem('room');
	const songId = sessionStorage.getItem('songId');
	const artistSelectors = document.querySelector('#artistName');
	const artist = document.querySelector('#artistName').value;
	const songSelectors = document.querySelector('#songName');
	const song = document.querySelector('#songName').value;
	console.log({ artist, song, userId, room, songId });
	socket.emit('submitAnswer', { artist, song, userId, room, songId });

	// STOP SONG
	const audioPlayer = document.querySelector('#quizAudioPlayer');
	audioPlayer.pause();

	// CLEAR ANSWER
	artistSelectors.value = '';
	songSelectors.value = '';

	// SHOW MODAL
	$('#joinModal').modal('show');

	// CLEAR TIMER
	clearTimeout(window.Timer);

	// WAITING FOR OTHER PLAYERS
	//SCORE
	const modalTextContent = document.querySelector('#modalTextContent');
	modalTextContent.textContent = `Waiting For Other Players To Guess The Song`;
	const primaryButton = document.querySelector('#modalPrimary');
	primaryButton.disabled = true;
};

const showImageHint = () => {
	const imageLink = sessionStorage.getItem('prevIMG');
	const image = document.querySelector('#quizImage');
	image.src = imageLink;
};

const updateScoreBoard = () => {
	const scoreboard = document.querySelector('#scoreboard');
	const header = `<tr>
						<th>Username</th>
						<th>Scores</th>
					</tr>`;
	const users = JSON.parse(sessionStorage.getItem('users'));
	console.log(users);
	let userString = users
		.map(
			(user) => `<tr>
						<td>${user.username}</td>
						<td>${user.score}</td>
					</tr>`
		)
		.toString();
	scoreboard.innerHTML = `${header}${userString}`;
};

const isHost = () => {
	const userId = sessionStorage.getItem('userId');
	const hostUserId = sessionStorage.getItem('room').split('Xr00mZ')[0];
	return userId == hostUserId;
};

const hideButtonsForNonHost = () => {
	if (!isHost()) {
		// SET THE NEW MODAL
		const modalTitle = document.querySelector('#modalTitle');
		modalTitle.textContent = 'Scoreboard';
		$('#modalSecondary').hide();
		$('#modalPrimary').hide();
	}
};
