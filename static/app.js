/* DYNAMIC FORM OPTIONS */
$('#type').on('input', function(e) {
	let option = $("#type option:selected").text()

	if (option === 'On Ear') {
		$('#portability-wrapper').hide()
		$('#fit-wrapper').hide()
	} else if (option === 'In Ear Monitor') {
		$('#fit-wrapper').show()
		$('#portability-wrapper').hide()
	} else {
		$('#fit-wrapper').hide()
		$('#portability-wrapper').show()
	}
})

/* FORM SUBMISSION */
$('form').on('submit', function(e) {
	e.preventDefault()

	$('#submit').addClass('loading')
	$('#error-toast').hide() // hide error on resubmit

	// verify if .mp3 file
	let mp3 = $('#input-file')[0].files[0]
	if (!mp3.name.endsWith('.mp3')) {
		$('#error-msg').text('Invalid file, please select an .mp3')
		$('#error-toast').show()
		$('#submit').removeClass('loading')
		return
	} else if (mp3.size > 20971520) {
		$('#error-msg').text('File too large, please select a smaller .mp3 under 20MB')
		$('#error-toast').show()
		$('#submit').removeClass('loading')
		return
	}

	const data = new FormData()
	data.append('type', $("#type option:selected").text())
	data.append('portability', $("#portability option:selected").text())
	data.append('fit', $("#fit option:selected").text())
	data.append('price', $("#price option:selected").text())
	data.append('file', mp3)

	axios.post('/upload', data)
		.then(function (response) {
			$('#response').text(response.data)
			$('#response-modal').addClass('active')
			$('#submit').removeClass('loading')
			console.log(response);
		})
		.catch(function (error) {
			$('#error-toast').show()
			$('#submit').removeClass('loading')
			console.log(error);
		});
})

/* CLOSING ACTIONS */
$('#modal-close').on('click', function(e) {
	$('#response-modal').removeClass('active')
})

$('#error-close').on('click', function(e) {
	$('#error-toast').hide()
})