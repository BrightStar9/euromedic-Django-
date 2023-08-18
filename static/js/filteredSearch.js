function filteredSearch(term, category, hospital, classIdentifier, parentElementId) {
    term = term.trimStart()



    let query = {};
    
    if (term) {
        query["search"] = "name:" + term;
    }
    if (category) {
        query["n_category"] = category;
    }
    if (hospital) {
        query["n_hospital"] = hospital;
    }

    $.ajax({
        url: window.location.origin + "/api/search-services/",
        dataType: "json",
        data: query,
        headers: {
            'Accept-Language': 'sr'
        },
        success: function (data) {
            let processedData = groupByCategory(data.results);
            displayResults(processedData, classIdentifier, parentElementId);
        }
    });
}

function groupByCategory(data) {
    let result = {};
    data.forEach(el => {
        if (!result[el.category.name]) {
            result[el.category.name] = [el];
        } else {
            result[el.category.name].push(el);
        }
    });
    return result;
}

function groupDoctorsByCategory(data) {
    let result = {};
    data.forEach(el => {
        if(!el.category) return;
        if (!result[el.category.display_title]) {
            result[el.category.display_title] = [el];
        } else {
            result[el.category.display_title].push(el);
        }
    });
    return result;
}

function groupedDoctorDataToUngroup(data){
  let result={};
  let inx = 0;
  Object.keys(data).forEach(key => {
    if(data[key].length > 1){
      data[key].forEach(el => {
        result[inx] = [el];
        inx = inx+1;
      });
    }else{
      result[inx] = data[key];
      inx = inx+1;
    }
  });

  return result;
}

function displayResults(data, classIdentifier, parentElementId) {
    $(classIdentifier).remove();

    if (!Object.keys(data).length) {
        return;
    }

    Object.keys(data).forEach(key => {
        let tplCategory = document.querySelector('#tpl-category');
        tplCategory.content.querySelector('.tpl-category-name').textContent = key;
        tplCategory.content.querySelector('.tpl-category-services').innerHTML = "";

        data[key].forEach(el => {
            let tplService = document.querySelector('#tpl-single-service');
            let link = document.createElement("a");
            let price = document.createElement("span");

            link.href = "/usluga/" + el.slug;
            link.text = el.name;
            link.classList.add("category-name");

            price.innerText = el.price + " ";
            price.classList.add("float-right", "category-price");
            price.insertAdjacentHTML("beforeend", "<span class=\"fw-normal\">RSD</span>");

            tplService.content.querySelector('.tpl-single-body').innerHTML = "";
            tplService.content.querySelector('.tpl-single-body').append(link, price);

            let srvClone = document.importNode(tplService.content, true);
            tplCategory.content.querySelector('.tpl-category-services').append(srvClone);
        });

        let clone = document.importNode(tplCategory.content, true);
        $(parentElementId).append(clone);
    });
}


function filteredSearchDoctorsSectionWise(term, category, hospital, classIdentifier, parentElementId) {
    term = term.trimStart();
    // var no_per_page = 5;
    let query = {};
    let page = parseInt($("#main-flux").attr("data-page"));
    var searchflag = false;

    if (category) {
        query["n_category"] = category;
        query["ordering"] = "ordering_id";
    }

    $.ajax({
        url: window.location.origin + "/api/search-doctors/",
        dataType: "json",
        data: query,
        headers: {
            'Accept-Language': 'sr'
        },
        success: function (data) {
            let processedData = groupDoctorsByCategory(data.results);
            processedData = groupedDoctorDataToUngroup(processedData);
            displayResultsDoctorsPerSections(processedData, classIdentifier, parentElementId, page);
            $("#svg-two").css("display", "none");
        }
    });
}

function displayResultsDoctorsPerSections(data, classIdentifier, parentElementId, page) {
  //  $(classIdentifier).remove();

    if (!Object.keys(data).length) {
        return;
    }
    parentElementId = '#pricing-content';

    //scroll to response part.
    // var elmnt = document.getElementById("pricing-content");
    // elmnt.scrollIntoView();

    var drMainContainerSect = document.createElement("section");
    drMainContainerSect.classList.add('vc_row', 'pt-50', 'pb-80', 'd-flex', 'category-section', 'bg-image');

    var drMainContainerPadd = document.createElement("div");
    drMainContainerPadd.classList.add('container', 'align-self-center');

    var drMainContainerCenter = document.createElement("div");
    drMainContainerCenter.classList.add('row', 'justify-content-center');
    let drSubTitName = document.createElement("h4");
    drSubTitName.classList.add('text-uppercase', 'mb-1', 'tpl-category-name');
    drSubTitName.innerText = data[Object.keys(data)[0]][0].category.display_title;
    let drContainerSubTit = document.createElement("div");
    drContainerSubTit.classList.add('col-12', 'col-md-8', 'text-center', 'mb-4');
    drContainerSubTit.appendChild(drSubTitName);
    let svgIcon = '<svg class="red-cross" width="36px" height="36px" viewBox="0 0 36 36" version="1.1" xmlns="http://www.w3.org/2000/svg"><title>Combined Shape</title><desc>Created with Sketch.</desc><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><g transform="translate(-942.000000, -1096.000000)" fill="#DA1D25"><g transform="translate(0.000000, 1020.000000)"><g transform="translate(228.000000, 0.000000)"><path d="M732.064516,76 C741.935484,76 750,84.0645161 750,94 C750,103.935484 741.935484,112 732,112 C722.064516,112 714,103.935484 714,94 C714.064516,84.0645161 722.129032,76 732.064516,76 Z M732.064516,77.4193548 C722.903226,77.4193548 715.483871,84.8387097 715.483871,94 C715.483871,103.16129 722.903226,110.580645 732.064516,110.580645 C741.225806,110.580645 748.645161,103.16129 748.645161,94 C748.645161,84.8387097 741.225806,77.4193548 732.064516,77.4193548 Z M734,82.8387097 C734.645161,82.8387097 735.16129,83.3548387 735.16129,84 L735.161,90.967 L742,90.9677419 C742.645161,90.9677419 743.16129,91.483871 743.16129,92.1290323 L743.16129,95.9354839 C743.16129,96.5806452 742.645161,97.0967742 742,97.0967742 L735.161,97.096 L735.16129,103.935484 C735.16129,104.580645 734.645161,105.096774 734,105.096774 L730.193548,105.096774 C729.548387,105.096774 729.032258,104.580645 729.032258,103.935484 L729.032,97.096 L722.064516,97.0967742 C721.419355,97.0967742 720.903226,96.5806452 720.903226,95.9354839 L720.903226,92.1290323 C720.967742,91.483871 721.419355,90.9677419 722.064516,90.9677419 L729.032,90.967 L729.032258,84 C729.032258,83.3548387 729.548387,82.8387097 730.193548,82.8387097 L734,82.8387097 Z"></path></g></g></g></g></svg>';
    drContainerSubTit.innerHTML += svgIcon;
    drMainContainerCenter.append(drContainerSubTit);


    var drMainContainer = document.createElement("div");
    drMainContainer.setAttribute("id", "tpl-main-category-doctors-"+page);
    drMainContainer.classList.add('col-12', 'row', 'doctors-row', 'tpl-category-doctors');

    // if(searchflag){
    //   var dataArray = Object.values(data);
    //   dataArray = dataArray.slice(0, 3);
    //   data = arrayToObject(dataArray);
    // }

    Object.keys(data).forEach(key => {
        let tplCategory = document.querySelector('#tpl-category');
        tplCategory.content.querySelector('.tpl-category-name').textContent = key;
        tplCategory.content.querySelector('.tpl-category-doctors').innerHTML = "";
        data[key].forEach(el => {
            let tplService = document.querySelector('#tpl-single-doctor');
            let link = document.createElement("a");

            link.href = "/lekari/" + el.slug;

            let drContainer = document.createElement("div");
            drContainer.classList.add("doctor-single");

            let drImageContainer = document.createElement("div");
            let drImage = document.createElement("img");
            drImage.src = el.image_url;
            drImageContainer.classList.add("doctor-image");
            drImageContainer.appendChild(drImage);
            drContainer.appendChild(drImageContainer);

            let drInfoContainer = document.createElement("div");
            let drInfo = document.createElement("div");
            let drName = document.createElement("h4");
            drName.innerText = el.full_name;
            let drSpec = document.createElement("span");
            drSpec.innerText = el.specialization;
            drInfo.appendChild(drName);
            drInfo.appendChild(drSpec);
            if(el.specialization_details){
                let brEl = document.createElement("br");
                drInfo.appendChild(brEl);
                let subSpec = document.createElement("span");
                subSpec.innerText = el.specialization_details;
                drInfo.appendChild(subSpec);
            }
            drInfoContainer.classList.add("doctor-info");
            drInfoContainer.appendChild(drInfo);
            drContainer.appendChild(drInfoContainer);
            link.appendChild(drContainer);

            tplService.content.querySelector('.tpl-single-body').innerHTML = "";
            tplService.content.querySelector('.tpl-single-body').append(link);
            tplService.classList.add("doctor-single");

            let srvClone = document.importNode(tplService.content, true);
            drMainContainer.append(srvClone);
            // $(parentElementId).append(srvClone);
            // tplCategory.content.querySelector('.tpl-category-doctors').append(srvClone);
        });
        // let clone = document.importNode(tplCategory.content, true);
        // $(parentElementId).append(clone);
    });
    drMainContainerCenter.append(drMainContainer);
    drMainContainerPadd.append(drMainContainerCenter);
    drMainContainerSect.append(drMainContainerPadd);

    $(parentElementId).append(drMainContainerSect);

    document.querySelector('#tpl-main-category-doctors-'+page).scrollIntoView({behavior: 'smooth'});

    page = (page+1);
    //if(!searchflag){
      $("#main-flux").attr("data-fetch", "false");
    //}
    $("#main-flux").attr("data-page", page.toString());

}


function filteredSearchDoctors(term, category, hospital, classIdentifier, parentElementId, loadmore) {
    term = term.trimStart();
    var no_per_page = 5;
    let query = {};
    let page = $("#flux").attr("data-page");
    var searchflag = false;
    if (term) {
        query["search"] = "full_name:" + term;
        searchflag = true;
    }
    if (category) {
        query["n_category"] = category;
    }
    if (hospital) {
        query["n_hospital"] = hospital;
    }

    page = parseInt(page);
    query["offset"] = (page-1)*no_per_page;
    if(page){
      query["limit"] = no_per_page;
    }


    $.ajax({
        url: window.location.origin + "/api/search-doctors/",
        dataType: "json",
        data: query,
        headers: {
            'Accept-Language': 'sr'
        },
        success: function (data) {
            let processedData = groupDoctorsByCategory(data.results);
            processedData = groupedDoctorDataToUngroup(processedData);
            if(loadmore){
               displayResultsDoctorsLoadMore(processedData, classIdentifier, parentElementId, page, searchflag);
            }else{
               displayResultsDoctors(processedData, classIdentifier, parentElementId, page, searchflag);
            }
            $("#svg-one").css("display", "none");
        }
    });
}

function displayResultsDoctorsLoadMore(data, classIdentifier, parentElementId, page, searchflag) {
  if (!Object.keys(data).length) {
      return;
  }
  parentElementId = '#pricing-content';

  var drMainContainer = document.getElementById("tpl-main-category-doctors");

  if(searchflag){
    var dataArray = Object.values(data);
    dataArray = dataArray.slice(0, 3);
    data = arrayToObject(dataArray);
  }

  Object.keys(data).forEach(key => {
      let tplCategory = document.querySelector('#tpl-category');

      data[key].forEach(el => {
          let tplService = document.querySelector('#tpl-single-doctor');
          let link = document.createElement("a");

          link.href = "/lekari/" + el.slug;

          let drContainer = document.createElement("div");
          drContainer.classList.add("doctor-single");

          let drImageContainer = document.createElement("div");
          let drImage = document.createElement("img");
          drImage.src = el.image_url;
          drImageContainer.classList.add("doctor-image");
          drImageContainer.appendChild(drImage);
          drContainer.appendChild(drImageContainer);

          let drInfoContainer = document.createElement("div");
          let drInfo = document.createElement("div");
          let drName = document.createElement("h4");
          drName.innerText = el.full_name;
          let drSpec = document.createElement("span");
          drSpec.innerText = el.specialization;
          drInfo.appendChild(drName);
          drInfo.appendChild(drSpec);
          if(el.specialization_details){
              let brEl = document.createElement("br");
              drInfo.appendChild(brEl);
              let subSpec = document.createElement("span");
              subSpec.innerText = el.specialization_details;
              drInfo.appendChild(subSpec);
          }
          drInfoContainer.classList.add("doctor-info");
          drInfoContainer.appendChild(drInfo);
          drContainer.appendChild(drInfoContainer);
          link.appendChild(drContainer);

          tplService.content.querySelector('.tpl-single-body').innerHTML = "";
          tplService.content.querySelector('.tpl-single-body').append(link);
          tplService.classList.add("doctor-single");

          let srvClone = document.importNode(tplService.content, true);
          drMainContainer.append(srvClone);
      });

  });
  page = (page+1);
  if(!searchflag){
    $("#flux").attr("data-fetch", "false");
  }
  $("#flux").attr("data-page", page.toString());

}

function arrayToObject(arr) {
            var rv = {};
            for (var i = 0; i < arr.length; ++i)
                rv[i] = arr[i];
            return rv;
}

function displayResultsDoctors(data, classIdentifier, parentElementId, page, searchflag) {
    $(classIdentifier).remove();

    if (!Object.keys(data).length) {
        return;
    }
    parentElementId = '#pricing-content';

    //scroll to response part.
    document.querySelector('#pricing-content').scrollIntoView({behavior: 'smooth'});
    // var elmnt = document.getElementById("pricing-content");
    // elmnt.scrollIntoView();

    var drMainContainerSect = document.createElement("section");
    drMainContainerSect.classList.add('vc_row', 'pt-50', 'pb-80', 'd-flex', 'category-section', 'bg-image');

    var drMainContainerPadd = document.createElement("div");
    drMainContainerPadd.classList.add('container', 'align-self-center');

    var drMainContainerCenter = document.createElement("div");
    drMainContainerCenter.classList.add('row', 'justify-content-center');
    let drSubTitName = document.createElement("h4");
    drSubTitName.classList.add('text-uppercase', 'mb-1', 'tpl-category-name');
    drSubTitName.innerText = 'Rezultati pretrage';
    let drContainerSubTit = document.createElement("div");
    drContainerSubTit.classList.add('col-12', 'col-md-8', 'text-center', 'mb-4');
    drContainerSubTit.appendChild(drSubTitName);
    let svgIcon = '<svg class="red-cross" width="36px" height="36px" viewBox="0 0 36 36" version="1.1" xmlns="http://www.w3.org/2000/svg"><title>Combined Shape</title><desc>Created with Sketch.</desc><g stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><g transform="translate(-942.000000, -1096.000000)" fill="#DA1D25"><g transform="translate(0.000000, 1020.000000)"><g transform="translate(228.000000, 0.000000)"><path d="M732.064516,76 C741.935484,76 750,84.0645161 750,94 C750,103.935484 741.935484,112 732,112 C722.064516,112 714,103.935484 714,94 C714.064516,84.0645161 722.129032,76 732.064516,76 Z M732.064516,77.4193548 C722.903226,77.4193548 715.483871,84.8387097 715.483871,94 C715.483871,103.16129 722.903226,110.580645 732.064516,110.580645 C741.225806,110.580645 748.645161,103.16129 748.645161,94 C748.645161,84.8387097 741.225806,77.4193548 732.064516,77.4193548 Z M734,82.8387097 C734.645161,82.8387097 735.16129,83.3548387 735.16129,84 L735.161,90.967 L742,90.9677419 C742.645161,90.9677419 743.16129,91.483871 743.16129,92.1290323 L743.16129,95.9354839 C743.16129,96.5806452 742.645161,97.0967742 742,97.0967742 L735.161,97.096 L735.16129,103.935484 C735.16129,104.580645 734.645161,105.096774 734,105.096774 L730.193548,105.096774 C729.548387,105.096774 729.032258,104.580645 729.032258,103.935484 L729.032,97.096 L722.064516,97.0967742 C721.419355,97.0967742 720.903226,96.5806452 720.903226,95.9354839 L720.903226,92.1290323 C720.967742,91.483871 721.419355,90.9677419 722.064516,90.9677419 L729.032,90.967 L729.032258,84 C729.032258,83.3548387 729.548387,82.8387097 730.193548,82.8387097 L734,82.8387097 Z"></path></g></g></g></g></svg>';
    drContainerSubTit.innerHTML += svgIcon;
    drMainContainerCenter.append(drContainerSubTit);


    var drMainContainer = document.createElement("div");
    drMainContainer.setAttribute("id", "tpl-main-category-doctors");
    drMainContainer.classList.add('col-12', 'row', 'doctors-row', 'tpl-category-doctors');

    if(searchflag){
      var dataArray = Object.values(data);
      dataArray = dataArray.slice(0, 3);
      data = arrayToObject(dataArray);
    }

    Object.keys(data).forEach(key => {
        let tplCategory = document.querySelector('#tpl-category');
        //tplCategory.content.querySelector('.tpl-category-name').textContent = key;
        tplCategory.content.querySelector('.tpl-category-doctors').innerHTML = "";
        data[key].forEach(el => {
            let tplService = document.querySelector('#tpl-single-doctor');
            let link = document.createElement("a");

            link.href = "/lekari/" + el.slug;

            let drContainer = document.createElement("div");
            drContainer.classList.add("doctor-single");

            let drImageContainer = document.createElement("div");
            let drImage = document.createElement("img");
            drImage.src = el.image_url;
            drImageContainer.classList.add("doctor-image");
            drImageContainer.appendChild(drImage);
            drContainer.appendChild(drImageContainer);

            let drInfoContainer = document.createElement("div");
            let drInfo = document.createElement("div");
            let drName = document.createElement("h4");
            drName.innerText = el.full_name;
            let drSpec = document.createElement("span");
            drSpec.innerText = el.specialization;
            drInfo.appendChild(drName);
            drInfo.appendChild(drSpec);
            if(el.specialization_details){
                let brEl = document.createElement("br");
                drInfo.appendChild(brEl);
                let subSpec = document.createElement("span");
                subSpec.innerText = el.specialization_details;
                drInfo.appendChild(subSpec);
            }
            drInfoContainer.classList.add("doctor-info");
            drInfoContainer.appendChild(drInfo);
            drContainer.appendChild(drInfoContainer);
            link.appendChild(drContainer);

            tplService.content.querySelector('.tpl-single-body').innerHTML = "";
            tplService.content.querySelector('.tpl-single-body').append(link);
            tplService.classList.add("doctor-single");

            let srvClone = document.importNode(tplService.content, true);
            drMainContainer.append(srvClone);
            //$(parentElementId).append(srvClone);
            // tplCategory.content.querySelector('.tpl-category-doctors').append(srvClone);
        });
        // let clone = document.importNode(tplCategory.content, true);
        // $(parentElementId).append(clone);
    });
    drMainContainerCenter.append(drMainContainer);
    drMainContainerPadd.append(drMainContainerCenter);
    drMainContainerSect.append(drMainContainerPadd);

    $(parentElementId).append(drMainContainerSect);

    page = (page+1);
    if(!searchflag){
      $("#flux").attr("data-fetch", "false");
    }
    $("#flux").attr("data-page", page.toString());
}
