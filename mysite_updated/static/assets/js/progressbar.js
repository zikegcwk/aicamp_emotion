$(document).ready(function() {
	$("#uploadedprogress").hide();
	document.getElementById('image_button').addEventListener('click', openDialog);

	function openDialog() {
		document.getElementById('image_input_button').click();
	}

	$('form').on('change', function(event) {
		event.preventDefault();
		$("#uploadedprogress").show();

		var formData = new FormData($('form')[0]);

		$.ajax({
			xhr: function() {
				var xhr = new window.XMLHttpRequest();

				xhr.upload.addEventListener('progress', function(e) {

					if (e.lengthComputable) {
						console.log('Bytes Loaded' + e.loaded);
						console.log('Total Size: ' + e.total);
						console.log('Percentage Uploaded: ' + (e.loaded / e.total))

						var percent = Math.round(e.loaded / e.total * 100);
						var progress = percent + "%";
						$("#progressbar").css("width", progress);
						$("#progressbar").text(progress);
						$("#progresstext").text("Uploaded " + e.loaded + " bytes of " + e.total + " bytes");

					}

				});

				return xhr;
			},
			type: 'POST',
			url: '/',
			data: formData,
			processData: false,
			contentType: false,
			success: function() {
				$("#uploadedprogress").hide();
			}
		});

	});

});
