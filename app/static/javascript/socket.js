//https://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
const getParameterByName = (name, url = window.location.href) => {
	name = name.replace(/[\[\]]/g, '\\$&');
	var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
		results = regex.exec(url);
	if (!results) return null;
	if (!results[2]) return '';
	return decodeURIComponent(results[2].replace(/\+/g, ' '));
};

const notifyUserJoin = (username) => {
	const toasts = document.querySelector('#toasts');
	toasts.outerHTML = `<div class="toast" role="alert" aria-live="assertive" aria-atomic="true" id="toasts" style="position: absolute; top: 100px; right: 100px;">
  <div class="toast-header">
    <strong class="mr-auto">A User Has Joined!</strong>
    <button type="button" class="ml-2 mb-1 close" data-dismiss="toast" aria-label="Close">
      <span aria-hidden="true">&times;</span>
    </button>
  </div>
  <div class="toast-body">
	${username} has joined !
  </div>
</div>`;
	$('.toast').toast({ delay: 3000 });
	$('#toasts').toast('show');
};

$(document).ready(function () {
	//SOCKET CONNECTION
	const socket = io.connect('http://' + document.domain + ':' + location.port + '/sockets');

	socket.on('connect', () => {
		// REGISTER ON THE SERVER SESSION
		const userId = sessionStorage.getItem('userId');
		const username = sessionStorage.getItem('username');
		const playlistId = sessionStorage.getItem('playlistId');
		const room = getParameterByName('room') || `${userId}${username}${playlistId}`;
		console.log(room);
		socket.emit('connectFirstTime', { message: "I'm connected! ", userId, username, playlistId, room });
	});

	socket.on('onUserJoin', (data) => {
		//NEED TO DISPLAY SOMETHING
		console.log(data);
		notifyUserJoin(data.username);
	});

	socket.on('receiveData', (data) => {
		//NEED TO DISPLAY SOMETHING
		console.log('Data Received');
	});
});
