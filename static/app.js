/* DYNAMIC FORM OPTIONS */
var dynamicform = function(e) {
	let option = $("#type option:selected").text()

	if (option === 'On Ear') {
		$('#portability-wrapper').hide()
		$('#fit-wrapper').hide()
		$('#soundstage-wrapper').show()
		$('#onearhelp').show()
		$('#overearhelp').hide()
		$('#iemhelp').hide()

	} else if (option === 'In Ear Monitor') {
		$('#fit-wrapper').show()
		$('#portability-wrapper').hide()
		$('#soundstage-wrapper').hide()
		$('#onearhelp').hide()
		$('#overearhelp').hide()
		$('#iemhelp').show()

	} else { //over ear
		$('#fit-wrapper').hide()
		$('#portability-wrapper').show()
		if ($("#portability option:selected").text() === 'Not Portable') {
			$('#soundstage-wrapper').show()
		}
		else {
			$('#soundstage-wrapper').hide()
		}
		$('#onearhelp').hide()
		$('#overearhelp').show()
		$('#iemhelp').hide()
	}
}

$('#type').on('input', dynamicform)
$('#portability').on('input', dynamicform)

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
	data.append('backing', $("#soundstage option:selected").text())
	data.append('file', mp3)

	var SERVER = ""
	var PROD = false
	if (PROD) {
	    SERVER = '/upload'
	}
	else {
	    SERVER = 'http://127.0.0.1:5000/upload'
	}

	console.log(data)

	$.makeTable = function (mydata) {
	    var table = $('<table border=1>')
	    var tblHeader = "<tr>"
		tblHeader += "<th>" + "PRICE" + "</th>"
		tblHeader += "<th>" + "HEADPHONE" + "</th>"
	    tblHeader += "</tr>"
	    $(tblHeader).appendTo(table)

	    $.each(mydata, function (price, name) {
	        var TableRow = "<tr>"
            TableRow += "<td>" + "$" + price + "</td>"
            TableRow += "<td>" + name + "</td>"
	        TableRow += "</tr>"
	        $(table).append(TableRow)
	    });
	    return ($(table))
	};


	axios.post(SERVER, data)
		.then(function (response) {
			$('#response').text(response.data.signature)
			$('#response-modal').addClass('active')
			$('#submit').removeClass('loading')

			var table = $.makeTable(response.data.headphones);
			$(table).appendTo("#headphonetable");

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
	$('#headphonetable').empty()
})

$('#error-close').on('click', function(e) {
	$('#error-toast').hide()
})

$('.help-close').on('click', function(e) {
	$('#onearhelp').hide()
	$('#overearhelp').hide()
	$('#iemhelp').hide()
})