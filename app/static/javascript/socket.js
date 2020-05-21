// TIMERS
const setTimer = () => {
	let timeleft = 60;
	const songTimer = setInterval(() => {
		if (timeleft <= 0) {
			clearInterval(songTimer);
			const isSubmitted = sessionStorage.getItem('isSubmitted');
			document.getElementById('countdown').innerHTML = 'Times Up!!!';
			// EMIT SOMETHING IF NOT YET SUBMITTED
			if (!isSubmitted) {
			}
		} else {
			document.getElementById('countdown').innerHTML = timeleft + ' seconds remaining';
		}
		timeleft -= 1;
	}, 1000);
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
	hiddenCopyElement.value = `${window.location.href}?room=${userId}${username}${playlistId}`;

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
	$('.toast').toast({ delay: 3000 });
	$('#toasts').toast('show');
};

const notifyUserJoin = (username) => {
	showToast(`A User Has Joined!`, `${username} has joined !`);
};

$(document).ready(function () {
	// SHOW STARTING MODAL
	$('#joinModal').modal('show');

	//SOCKET CONNECTION
	socket = io.connect('http://' + document.domain + ':' + location.port + '/sockets');

	socket.on('connect', () => {
		// REGISTER ON THE SERVER SESSION
		const userId = sessionStorage.getItem('userId');
		const username = sessionStorage.getItem('username');
		const playlistId = sessionStorage.getItem('playlistId');
		const room = getParameterByName('room') || `${userId}${username}${playlistId}`;
		sessionStorage.setItem('room', room);
		console.log(room);
		socket.emit('connectFirstTime', { message: "I'm connected! ", userId, username, playlistId, room });
	});

	socket.on('onUserJoin', (data) => {
		notifyUserJoin(data.username);
	});

	socket.on('receivesSongData', (data) => {
		//NEED TO DISPLAY SOMETHING
		console.log('Data Received');
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
	});
});

const startTheGame = () => {
	const room = sessionStorage.getItem('room');
	console.log(room);
	socket.emit('startGame', { room });
};

const submitSong = () => {

}

const changeSong = (prevURL) => {
	const audioPlayer = document.querySelector('#quizAudioPlayer');
	const songPlayer = document.querySelector('#quizSong');
	songPlayer.src = prevURL;

	audioPlayer.volume = 0.5;
	audioPlayer.load();
	audioPlayer.play();

	setTimer();
};

const showImageHint = () => {
	const imageLink = sessionStorage.getItem('prevIMG');
	const image = document.querySelector('#quizImage');
	image.src = imageLink;
};

// SET DEFAULT VOLUME OF AUDIO
const audioPlayer = document.querySelector('#quizAudioPlayer');
audioPlayer.volume = 0.5;
