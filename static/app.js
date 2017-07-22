/* DYNAMIC FORM OPTIONS */
$('#type, #portability').on('input', function() {
	let option = $('#type option:selected').text()

	if (option === 'On Ear') {
		$('#portability-wrapper, #fit-wrapper, #overearhelp, #iemhelp').hide()
		$('#soundstage-wrapper, #onearhelp').show()

	} else if (option === 'In Ear Monitor') {
		$('#fit-wrapper, #iemhelp').show()
		$('#portability-wrapper, #soundstage-wrapper, #onearhelp, #overearhelp').hide()
	} else { //over ear
		if ($('#portability option:selected').text() === 'Not Portable') {
			$('#soundstage-wrapper').show()
		} else {
			$('#soundstage-wrapper').hide()
		}
		$('#onearhelp, #iemhelp, #fit-wrapper').hide()
		$('#overearhelp, #portability-wrapper').show()
	}
})

let makeTable = function (data) {
	let table = '<table class="table table-striped table-hover">'
	table += '<thead><tr><th>Price</th>'
	table += '<th>Headphone</th></tr></thead><tbody>'
	$.each(data, function (name, price) {
		let row = `<tr><td>$${price}</td><td>${name}</td><tr>`
		table += row
	})
	table += '</tbody></table>'
	return table
}

let showErr = function () {
	$('#error-toast').show()
	$('#submit').removeClass('loading')
}

/* FORM SUBMISSION */
$('form').on('submit', function(e) {
	e.preventDefault()

	$('#submit').addClass('loading')
	$('#error-toast').hide() // hide error on resubmit

	// verify if .mp3 file
	let mp3 = $('#input-file')[0].files[0]
	if (!mp3.name.endsWith('.mp3')) {
		$('#error-msg').text('Invalid file, please select an .mp3')
		showErr()
		return
	}

	// verify if .mp3 is under 20MB
	if (mp3.size > 20971520) {
		$('#error-msg').text('File too large, please select a smaller .mp3 under 20MB')
		showErr()
		return
	}

	// create form data
	const data = new FormData()
	data.append('type', $('#type option:selected').text())

	if ($('#portability').is(':visible'))
		data.append('opt1', $('#portability option:selected').text())

	if ($('#fit').is(':visible'))
		data.append('opt1', $('#fit option:selected').text())

	if ($('#soundstage').is(':visible'))
		data.append('opt2', $('#soundstage option:selected').text())

	data.append('price', $('#price option:selected').text())
	data.append('file', mp3)

	axios.post('/upload', data)
		.then(function (response) {
			$('#response').text(response.data.signature)
			$('#response-modal').addClass('active')
			$('#submit').removeClass('loading')

			var table = makeTable(response.data.headphones)
			$(table).appendTo('#headphonetable')

			console.log(response)
		})
		.catch(function (error) {
			showErr()
			console.log(error)
		})
})

/* CLOSING ACTIONS */
$('.modal-overlay').on('click', function() {
	$('#response-modal').removeClass('active')
})

$('#modal-close').on('click', function() {
	$('#response-modal').removeClass('active')
	$('#headphonetable').empty()
})

$('#error-close').on('click', function() {
	$('#error-toast').hide()
})