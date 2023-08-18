function registerSearch(searchElementId, resultsElementId,doconly=false) {
    function redirect(item) {

        $("<div>").text(item).prependTo(`#${resultsElementId}`);
        $(`#${resultsElementId}`).scrollTop(0);
    }

    let patched = $(`#${searchElementId}`).autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.origin + "/api/search/",
                dataType: "json",
                data: {
                    q: request.term
                },
                headers: {
                    'Accept-Language': 'sr'
                },
                success: function (data) {
                    response(data);
                }
            });
        },
        minLength: 5,
        select: function (event, ui) {
          if(!doconly){
            redirect(ui.item);
          }else{
            // console.log(ui.item.full_name);
            // console.log($(this));
            $('#searchDoctorResults').hide();
            redirect(ui.item);
            // $(this).val(ui.item.full_name);
            // return false;
            //$(this).removeClass("ui-corner-all").addClass("ui-corner-top");
          }
        },
        open: function () {
            $(this).removeClass("ui-corner-all").addClass("ui-corner-top");
        },
        close: function () {
            $(this).removeClass("ui-corner-top").addClass("ui-corner-all");
        }
    });

    patched.data("ui-autocomplete")._renderMenu = function (ul, items) {
        //console.log("SVE", items);
        var extraWidth = $(`#${searchElementId}`).width() + 80;
        ul.css('maxWidth', extraWidth);

        //console.log(typeof items["0"]);
      if(doconly){
        const doctors = Object.values(items["1"]);
        if (doctors.length > 0) {
          //  ul.append("<li class='ui-autocomplete-category'>Lekari</li>");
            $.each(items[1], function (index, item) {
                //console.log("REND DOC", item);
                return $(`<li onclick="(function(){
                            location.href = '/lekari/${item.slug}';
                            return false;
                        })();return false;">`)
                .data( "ui-autocomplete-item", item )
                .append(item.full_name)
                //.append(`<a href="/lekari/${item.slug}">` + item.full_name + "</a>")
                .appendTo( ul );
            });
        }
      }else{
        const services = Object.values(items["0"]);
        if (services.length > 0) {
            ul.append("<li class='ui-autocomplete-category'>Usluge</li>");
            $.each(items[0], function (index, item) {
              if (index < 5) {
              //  console.log("REND", item);
                $("<li></li>").data("item.autocomplete", item)
                    .append(`<a href="/usluga/${item.slug}">` + item.name + "</a>")
                    .appendTo(ul);
              }
            });
        }

        /*const doctors = Object.values(items["1"]);
        if (doctors.length > 0) {
            ul.append("<li class='ui-autocomplete-category'>Lekari</li>");
            $.each(items[1], function (index, item) {
                //console.log("REND DOC", item);
                $("<li></li>").data("item.autocomplete", item)
                    .append(`<a href="/lekari/${item.slug}">` + item.full_name + "</a>")
                    .appendTo(ul);
            });
        }*/
      }
    }
}
