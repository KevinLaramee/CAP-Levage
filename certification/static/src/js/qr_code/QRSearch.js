var video = document.createElement("video");
var canvasElement = document.getElementById("canvas");
var canvas = canvasElement.getContext("2d");
var loadingMessage = document.getElementById("loadingMessage");

var $scanProgress = false;
//var outputContainer = document.getElementById("output");
//var outputMessage = document.getElementById("outputMessage");
//var outputData = document.getElementById("outputData");

function drawLine(begin, end, color) {
    console.log(1);
    canvas.beginPath();
    canvas.moveTo(begin.x, begin.y);
    canvas.lineTo(end.x, end.y);
    canvas.lineWidth = 4;
    canvas.strokeStyle = color;
    canvas.stroke();
    console.log(2);
}

navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
  .then(function(stream) {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function(stream) {
            video.srcObject = stream;
            video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
            video.play();
            requestAnimationFrame(tick);

        });

        $( document ).ready(function() {
            $(video).css('display', 'none');
            document.getElementById("qrCodeModal").appendChild(video);
        });
  })
  .catch(function(error) {
    console.log('error camera');
    $('#qr_error').html('Aucune caméra détectée !');
  });
  /*
if(window.location.toString().indexOf('http://localhost:8069') != -1) {//pour le localhost
    navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } })
  .then(function(stream) {
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function(stream) {
            video.srcObject = stream;
            video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
            video.play();
            requestAnimationFrame(tick);

        });

        $( document ).ready(function() {
            $(video).css('display', 'none');
            document.getElementById("qrCodeModal").appendChild(video);
        });
  })
  .catch(function(error) {
    console.log('error camera');
    $('#qr_error').html('Aucune caméra détectée !');
  });
}else { //pour le serveur
    if(navigator.mediaDevices){
         navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function(stream) {
            video.srcObject = stream;
            video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
            video.play();
            requestAnimationFrame(tick);

        });

        $( document ).ready(function() {
            $(video).css('display', 'none');
            document.getElementById("qrCodeModal").appendChild(video);
        });
    }else{
		setTimeout(function(){
			console.log('error camera');

			$('#qr_error').html('Aucune caméra détectée !');
		}, 500);

    }
}*/







/*
if(navigator.mediaDevices){
    if(navigator.mediaDevices.getUserMedia){
        // Use facingMode: environment to attemt to get the front camera on phones
        console.log(3);
        navigator.mediaDevices.getUserMedia({ video: { facingMode: "environment" } }).then(function(stream) {
            video.srcObject = stream;
            video.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
            video.play();
            requestAnimationFrame(tick);

        });

        $( document ).ready(function() {
            $(video).css('display', 'none');
            document.getElementById("qrCodeModal").appendChild(video);
        });
    }
}
*/




function stopStreamedVideo(video){
    if(!video) return false;
    let stream = video.srcObject;
    if(!stream) return false;
    let tracks = stream.getTracks();
    if(!tracks) return false;
    tracks.forEach(function(track){
        track.stop();
    });

    video.srcObject = null;
}

function tick() {
    loadingMessage.innerText = "⌛ Loading video...";
    var video = $('#qrCodeModal').find('video')[0];
    if(!video) return false;
    if (video.readyState === video.HAVE_ENOUGH_DATA) {
        loadingMessage.hidden = true;
        canvasElement.hidden = false;
        //outputContainer.hidden = false;

        canvasElement.height = video.videoHeight;
        canvasElement.width = video.videoWidth;
        canvas.drawImage(video, 0, 0, canvasElement.width, canvasElement.height);
        var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
        var code = jsQR(imageData.data, imageData.width, imageData.height, {
          inversionAttempts: "dontInvert",
        });

        if (code) {

            drawLine(code.location.topLeftCorner, code.location.topRightCorner, "#FF3B58");
            drawLine(code.location.topRightCorner, code.location.bottomRightCorner, "#FF3B58");
            drawLine(code.location.bottomRightCorner, code.location.bottomLeftCorner, "#FF3B58");
            drawLine(code.location.bottomLeftCorner, code.location.topLeftCorner, "#FF3B58");
            //outputMessage.hidden = true;
            //outputData.parentElement.hidden = false;
            //outputData.innerText = code.data;
            if(!$scanProgress){

                var origin = $('#qrCodeOrigin').val();
                if(origin == 'bo'){
                    var url = '/cap_levage_portal/materiels?search_in=allid&';
                    url+= 'search=' + code.data;
                    $scanProgress = true;
                    window.location = url;
                }else{
                    var location = window.location.toString();
                    console.log('location: ' + location);


                    //Front office, recherche sur les matériels
                    if (location.indexOf('/my/equipments') != -1){
                        var url = '/my/equipments?';
                        url+= 'search_qr_code=' + code.data;
                        $scanProgress = true;
                        window.location = url;
                    }
                    //Back office, affectation du qr code sur le formulaire d'édition ou de création d'un matériel
                    if(location.indexOf('model=critt.equipment') != -1 && location.indexOf('view_type=form') != -1){
                        $("input[name*='qr_code']").val(code.data);
                        $("input[name*='qr_code']").change();
                        $('#qrCodeModal').modal('hide');
                        var video = $('#qrCodeModal').find('video')[0];
                        stopStreamedVideo(video);
                    }
                    //Front office, affectation du qr code sur le formulaire d'édition ou de création d'un matériel
                    if (location.indexOf('/equipment?id=') != -1 || location.indexOf('/my/equipment') != -1 ){
                        $('#qr_code').val(code.data);
                        $('#qrCodeModal').modal('hide');
                        var video = $('#qrCodeModal').find('video')[0];
                        stopStreamedVideo(video);
                    }
                }

            }


        }
        else {
            //outputMessage.hidden = false;
            //outputData.parentElement.hidden = true;
        }
    }
    requestAnimationFrame(tick);
}
