$( document ).ready(function() {


	//$('.navbar-listequipment').find('input').attr('class', 'col-xs-6');

	var table = $('#myTable').DataTable({
		"pageLength": 10,
		searching: false,
		"bLengthChange" : false,
		"language": {
            "url": "/certification/static/src/js/datatables/French.json"
        }
	});
	table.on( 'draw', function () {
		$('#myTable').parent().parent().addClass('col-xs-12');
        var $div = $('<div class="col-xs-12"></div>');
        $('#myTable_wrapper').append($div);

        var $divInfo = $('<div class="col-sm-5"></div>');
        $divInfo.append($('#myTable_info'));
        var $divPaginate = $('<div class="col-sm-7"></div>');
        $divPaginate.append($('#myTable_paginate'));
        $div.append($divInfo);
        $div.append($divPaginate);

        $("#loader").hide();
	} );
	table.on( 'order.dt', function () {
        var order = table.order();
        console.log(table);
        console.log(order);

        var data = table
        .rows()
        .data();
        console.log(data);

        console.log( 'Ordering on column '+order[0][0]+' ('+order[0][1]+')' );
    } );

    $('#btn_request_audits').click(function(){
        $('#form_request_audits').submit();
    });



	/*$.each($('.equipment_image_src'), function(key, value){
		var src = $(this).html();
		if(src){
			if(src.length > 0){
				$(this).parent().find('.equipment_image_img').attr('src', src.replace(/amp;/g, ''));
				$(this).parent().find('.equipment_image_img').show();
			}
		}
	});*/

	$('#clear_filter').click(function(){
        //$('#exportTable').DataTable().destroy();
        window.location = '/my/equipments';
    });

	$('#btnSearch').click(function(){
        var search = $('#search').val();
        window.location = '/my/equipments?search=' + search;
    });

	$('#search').keypress(function(event){
        var keycode = (event.keyCode ? event.keyCode : event.which);
        if(keycode == '13'){
             $('#btnSearch').click();
        }
    });

    $("#exportButton").click(function () {
        //$('.buttons-pdf').click();
            exportButtonPdfClick();
    });

    /* $("#pdferror").find(".close_pdf_error").click(function(){
        alert("close error");
        $("#pdferror").hide();
    });*/


    function showModalMultiDocs(nbMaxParDoc) {
        var $msg = $("<div></div>");
        $msg.addClass("liste_fichiers");
        var $msg_infos = $("<span></span>");
        $msg_infos.append("En raison d'un nombre trop important de matériels, la liste à été divisée en plusieurs fichiers.");
        $msg.append($msg_infos);

        var data = table.rows().data().toArray();
        var nbDeFichier = Math.ceil(data.length / nbMaxParDoc);
        //console.log("nb de page: " + nbDeFichier);
        var nbMaterielFichier = 0;
        for(var i = 1 ; i <= nbDeFichier ; i++){
            if(i < nbDeFichier){ //
                nbMaterielFichier = nbMaxParDoc;
            }else{
                //nb de matériels dans le dernier document
                nbMaterielFichier = nbMaxParDoc - ((nbMaxParDoc * nbDeFichier) - data.length);
            }

             var $msg_file = $("<span data-file='"+ i + "' data-nbmateriel='" + nbMaterielFichier + "'></span>");
             $msg_file.addClass("link_dl_file");
             $msg_file.append("Fichier " + i + " <img src='/certification/static/src/img/pdf.png' height='18'>");
             $msg_file.click(function(){
                var file = $(this).data("file");
                var nbmateriel = $(this).data("nbmateriel");
                //console.log("file : " + file + " nbmateriel: " + nbmateriel);
                var start = file == 1 ? 0 : (((file - 1) * nbMaxParDoc));
                generateHtml(start, nbmateriel);

                setTimeout(function(){
                    var nomFichier = "liste_materiels_" + file + ".pdf";
                    createPdf(nomFichier);
                }, 300);

             });
             $msg.append($msg_file);
        }

        var $msg_infos2 = $("<span></span>");
        $msg_infos2.append("Cliquez sur un des fichiers pour le télécharger");
        $msg.append($msg_infos2);



        $('#message_modal').find('.modal-title').html('Téléchargement de la liste des matériels');
        //$('#message_modal').find('.modal-body').html(msg);
        $('#message_modal').find('.modal-body').empty();
        $('#message_modal').find('.modal-body').append($msg);
        $('#message_modal').modal();
    }


    function generateHtml(start, nb){
        $("#loader").show();

        $(".tablepdf").find(".rowpdf").remove();

        var data = table.rows().data().toArray();
        var firstPage = true;
        var row_number = 1;
        var nbMateriel = 0;
        var end = start + (nb - 1);
        //console.log("generate html, start: " + start + " nb: " + nb + " end: " + end);
        for(var i = start ; i <= end ; i++){
            var item = data[i];

            var num_materiel_bg = $(item[0]).css("background-color");
            var num_materiel_color = $(item[0]).css("color");
            var num_materiel = $(item[0]).html();
            var type = item[1];
            var etat_bg = $(item[2]).css("background");
            var etat_color = $(item[2]).css("color");
            var etat = $(item[2]).html();
            var photo = $(item[3]).html();
            var agence = item[4];
            var equipe = item[5];

            //console.log(num_materiel + " " + type + " " + etat + " " + photo + " " + agence + " " + equipe);

            $row = $("<div class='rowpdf'></div>");
            $row.addClass("row_" + row_number);

            $num_materiel = $("<span class='cell_num_materiel'></span>");
            $num_materiel.addClass("equipment_cell");
            $num_materiel.css("background-color", num_materiel_bg);
            $num_materiel.css("color", num_materiel_color);
            $num_materiel.append(num_materiel);
            $row.append($num_materiel);

            $type = $("<span class='equipment_category_rows'></span>");
            $type.append(type);
            $row.append($type);
            $etat = $("<span></span>");
            $etat.css("background", etat_bg);
            $etat.css("color", etat_color);
            $etat.append(etat);
            $row.append($etat);
            $photo = $("<span></span>");
            $photo.append(photo);
            $row.append($photo);
            $agence = $("<span></span>");
            $agence.addClass("equipment_cell");
            $agence.append(agence);
            $row.append($agence);
            $equipe = $("<span></span>");
            $equipe.addClass("equipment_cell");
            $equipe.append(equipe);
            $row.append($equipe);

            $(".tablepdf").append($row);

            //console.log("num materiel: " + num_materiel + " row_number: " + row_number + " firstpage: " + firstPage);
            if(firstPage){
                //gestion de la première page
                if(row_number == 9){
                    $row.addClass("after");
                    $row.addClass("lastRowPage");
                    $row.removeClass("row_"+ row_number);
                    row_number = 1;
                    firstPage = false;
                }else{
                    row_number++;
                }
            }else{ //gestion du nombre de matériels sur les pages suivantes
                if(row_number == 10){
                    $row.addClass("after");
                    $row.addClass("lastRowPage");
                    $row.removeClass("row_"+ row_number);
                    row_number = 1;
                }else{
                    row_number++;
                }
            }

        }


    }

    function exportButtonPdfClick() {
        //$("#loader").show();

        //generation tableau pdf
          var data = table.rows().data().toArray(); // table.data();



        $(".tablepdf").find(".rowpdf").remove();
        var firstPage = true;
        var row_number = 1;
        var nbMateriel = 0;

        var nbMaxParDoc = 99; //150;

        //console.log(data);

        if(data.length > nbMaxParDoc){
            showModalMultiDocs(nbMaxParDoc);
        }else{
            generateHtml(0, data.length);
            setTimeout(function(){
                var nomFichier = "liste_materiels.pdf";
                createPdf(nomFichier);
            }, 300);
        }

    }

    function createPdf(nomFichier){
        // Get the element.
            var element = document.getElementById('templatePdfContent');
            //$(element).show();
            // Choose pagebreak options based on mode.
            var mode = 'css';
            var pagebreak = (mode === 'specify') ?
                { mode: '', before: '.before', after: '.after', avoid: '.avoid' } :
                { mode: mode };

            // Generate the PDF.
            html2pdf().from(element).set({
              filename: nomFichier,
              pagebreak: pagebreak,
              image:        { type: 'jpeg', quality: 0.98 },
              html2canvas:  { scale: 2 },
              jsPDF: {orientation: 'landscape', unit: 'in', format: 'letter', compressPDF: false}
            })
            .save()
            .catch(function(e){
                console.log("error pdf");
                $("#pdferror").find(".pdferrormessage").html("Une erreur est survenue lors de la génération du pdf !");
                $("#loader").hide();
                $("#pdferror").show();
            })
            .then(function(e){
                $("#loader").hide();
            });
    }



});
