// Initialize Flatpickr
const today = new Date().toISOString().split('T')[0];
let lastCropPositions = {}
let jcropAPI;
let jCropInitButton = false;
$(document).ready(function () {
    /** Date Picker **/
    flatpickr("#datepicker", {defaultDate: today});
    /** Nice select **/
    $('select').niceSelect();
    /** jCrop**/
    $(document).on("click", ".crop-button", function (event) {
        event.preventDefault(); // Prevent default action for the click event
        cropImage()
    });
    $(".cropme").click(function () {
        initJcrop();
    });
    $(document).on("click", ".subscribe", function (event) {
        $('#subscribe-modal').modal('show');
    });
});

function initJcrop() {
    if (jCropInitButton === false) {
        containerActiveImage.Jcrop({
                onSelect: updateCoords
            },
            function () {
                jcropAPI = this;
                jcropAPI.setSelect([100, 100, 400, 300]);
            });
    }
}

function updateCoords(c) {
    updateCropPositions(c.x, c.y, c.w, c.h)
    if (!jCropInitButton) {
        $('<button class="red-button btn btn-danger btn-sm crop-button" type="button">CROP</button>').appendTo('.jcrop-tracker:first');
        $('.red-button').css({
            'position': 'absolute',
            'bottom': '10px',
            'right': '10px',
            'font-weight': 'bold',
            'border': '2px solid #FFFFFF',
            'z-index': '9999'
        });
        jCropInitButton = true;
    }
    console.log('Selected area: x=' + c.x + ', y=' + c.y + ', w=' + c.w + ', h=' + c.h);
}

function updateCropPositions(x, y, w, h) {
    lastCropPositions = {
        x: Math.round(x * originalImageWidth / containerActiveImage.width()),
        y: Math.round(y * originalImageHeight / containerActiveImage.height()),
        w: Math.round(w * originalImageWidth / containerActiveImage.width()),
        h: Math.round(h * originalImageHeight / containerActiveImage.height())
    };
    console.log(lastCropPositions)
}

let originalImageWidth = 0;
let originalImageHeight = 0;

function updateImageDimensions() {
    originalImageWidth = containerActiveImage.prop('naturalWidth');
    originalImageHeight = containerActiveImage.prop('naturalHeight');
}

function cropImage() {
    const pos = lastCropPositions;
    const pageData = activePageData();
    const url = `/share/${pageData.page_id}/${pos.x}/${pos.y}/${pos.w}/${pos.h}`;
    postJsonData(url, {}, function (result, response) {
        if (result && response.data) {
            var shareImageUrl = response.data;
            containerImagePreview.attr('src', shareImageUrl);
            updateShareLinks(shareImageUrl)
            $('#share-image-modal').modal('show');
        }
    }, true, false)
}

/* *************************************************** */
/* *************************************************** */
/* *************************************************** */
let selectOptionEdition, selectOptionSubEdition
$(document).ready(function () {
    selectOptionEdition = $('#select-main-edition');
    selectOptionSubEdition = $('#select-sub-edition');
    selectOptionEdition.change(function () {
        showFullLoader()
        postJsonDataAsFormData(urlApiSubEditions, {edition_id: $(this).val()}, function (status, data) {
            if (status) {
                selectOptionSubEdition.html('')
                data.editions.forEach(function (item) {
                    selectOptionSubEdition.append($('<option>', {value: item.id, text: item.name}));
                })
                selectOptionSubEdition.niceSelect('update');
                apiFetchPapers()
            }
        }, false, false)
    });
    selectOptionSubEdition.change(function () {
        console.log("Sub Editions updated")
        apiFetchPapers()
    });
    containerDatePicker.change(function () {
        apiFetchPapers()
    })
    selectOptionEdition.niceSelect('update');
    selectOptionSubEdition.niceSelect('update');
    apiFetchPapers()
})

function parsePageId(input) {
    const parsedInt = parseInt(input);
    return isNaN(parsedInt) ? 1 : parsedInt;
}

function apiFetchPapers() {
    const jsonData = serializeFormData("#form-epapers")
    console.log("Form data")
    console.log(jsonData)
    postJsonDataAsFormData(urlApiEPapers, jsonData, function (status, data) {
        updatePaperPageResult(data)
    }, true, false);
}

let activePageId = 1;
const isActive = (id) => activePageId.toString() === id.toString();
const hasNext = () => activePageId < pages.length;
const hasPrevious = () => activePageId > 1;
let pages = [];
const activePageData = () => pages[activePageId - 1];
const containerPageThumbnails = $('#container-thumbnail-previews')
const containerPageNumbers = $('#container-page-numbers')
const containerActiveImage = $('#crop-target')
const containerActivePageNumber = $('.active-page-number')
const containerImagePreview = $('#image-preview')
const containerDatePicker = $('#datepicker')
const containerNotFoundMessage = $('#not-found-message')
const containerPreviewItems = $('.preview-items')
containerActiveImage.on('load', function () {
    updateImageDimensions();
});

function updatePaperPageResult(data) {
    containerNotFoundMessage.hide()
    containerPageThumbnails.empty()
    containerPageNumbers.empty()
    containerActiveImage.attr('src', '#')
    containerActivePageNumber.html('0')
    if (data.result && data.pages) {
        containerNotFoundMessage.hide()
        containerPreviewItems.show()
        pages = data.pages;
        pages.forEach((paper) => {
            containerPageThumbnails.append(buildThumbnailImage(paper))
            containerPageNumbers.append(buildPageNumbers(paper))
            updateActivePage(1)
        });
    } else {
        containerNotFoundMessage.show()
        containerPreviewItems.hide()
    }
}

function updateActivePage(id) {
    activePageId = parsePageId(id);
    $(".active-page-number").html(activePageId)
    $('.page-thumbnail').each(function () {
        const id = $(this).data('id');
        $(this).find('.thumb').toggleClass('thumbactive', isActive(id));
    });
    $('.page-numbers').each(function () {
        const id = $(this).data('id');
        $(this).toggleClass('active', isActive(id));
    });
    const data = activePageData()
    containerActiveImage.attr('src', data.gif_url)
    containerActivePageNumber.html(activePageId)
}

$(document).on("click", ".page-thumbnail,  .page-numbers", function (event) {
    const pageId = $(this).data('id');
    updateActivePage(pageId);
});
$(document).on("click", ".go-next-page", function (event) {
    if (hasNext()) {
        updateActivePage(activePageId + 1)
    }
});
$(document).on("click", ".go-previous-page", function (event) {
    if (hasPrevious()) {
        updateActivePage(activePageId - 1)
    }
});
$(document).on("click", ".download-active-pdf", function (event) {
    const data = activePageData()
    downloadFromUrl(data.pdf_url)
});
$(document).on("click", ".download-active-gif", function (event) {
    const data = activePageData()
    downloadFromUrl(data.gif_url)
});

function downloadFromUrl(url) {
    const link = document.createElement('a');
    link.href = url;
    link.target = "_blank";
    link.download = url.substring(url.lastIndexOf('/') + 1);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

function buildThumbnailImage(page) {
    return `<a class="page-thumbnail" data-id="${page.id}" onclick="updateActivePage('${page.id}')">
                <div class="thumb ${isActive(page.id) ? 'thumbactive' : ''} ">
                    <img src="${page.thumbnail_url}" class="img-fluid" alt="Thumbnail">
                    <div class="red-box mx-auto">
                        <p class="text-white m-0">Page ${page.id}</p>
                    </div>
                </div>
            </a>`;
}

function buildPageNumbers(page) {
    return `<a class="list-group-item list-group-item-action page-numbers ${isActive(page.id) ? 'active' : ''}"  data-id="${page.id}">${page.id}</a>`
}

function updateShareLinks(url) {
    // WhatsApp Share Icon
    $(".whatsapp").attr("href", "whatsapp://send?text=Check%20out%20this%20awesome%20content!%20" + encodeURIComponent(url));
    // Facebook Share Icon
    $(".facebook").attr("href", "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(url));
    // Twitter Share Icon
    $(".twitter").attr("href", "https://twitter.com/intent/tweet?url=" + encodeURIComponent(url) + "&text=Check%20out%20this%20awesome%20content!");
    // Download Icon
    $(".download-button").attr("href", url);
}