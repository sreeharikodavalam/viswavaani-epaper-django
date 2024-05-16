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
    $(".cropme").click(function () {
        initJcrop();
    });
    $(document).on("click", ".subscribe", function (event) {
        $('#subscribe-modal').modal('show');
    });
    
    ///- -----------------------------------
    ///- -----------------------------------
    ///- -----------------------------------
    $(document).on("click", ".crop-button", function (event) {
        // event.preventDefault();
        cropImage()
    });
    $(document).on("touchstart", ".crop-button", function (event) {
        // event.preventDefault(); // Prevent default touchstart behavior
        cropImage();
    });
    // Add touch event handlers for document
    window.addEventListener("touchstart", function (e) {
        console.log(e)
    }, {passive: true});
    $(document).on("click touchstart", ".crop-button", function (event) {
        console.log(e)
        console.log('click touchstart')
        event.preventDefault();
        cropImage()
    }, {passive: true});
});

function destroyJcrop() {
    if (jCropInitButton === true) {
        jCropInitButton = false;
        jcropAPI.destroy()
    }
}

function initJcrop() {
    if (jCropInitButton === false) {
        jCropInitButton = true;
        containerActiveImage.Jcrop({
                onSelect: updateCoords
            },
            function () {
                jcropAPI = this;
                jcropAPI.setSelect([100, 100, 400, 300]);
                $('<button class="red-button btn btn-danger btn-sm crop-button" style="z-index: -9999">CROP</button>').appendTo('.jcrop-tracker:first');
                $('<button class="red-button btn btn-danger btn-sm crop-button">CROP</button>').appendTo('.jcrop-tracker:last');
            });
    }
}

function updateCoords(c) {
    updateCropPositions(c.x, c.y, c.w, c.h)
}

function updateCropPositions(x, y, w, h) {
    lastCropPositions = {
        x: Math.round(x * originalImageWidth / containerActiveImage.width()),
        y: Math.round(y * originalImageHeight / containerActiveImage.height()),
        w: Math.round(w * originalImageWidth / containerActiveImage.width()),
        h: Math.round(h * originalImageHeight / containerActiveImage.height())
    };
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
    const url = `/share/api/${pageData.page_id}/${pos.x}/${pos.y}/${pos.w}/${pos.h}`;
    postJsonData(url, {}, function (result, response) {
        if (result && response.data) {
            const shareData = response.data;
            containerImagePreview.attr('src', shareData.image_url);
            updateShareLinks(shareData)
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
const containerProgressBar = $('.progress-bar')
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
    destroyJcrop()
    showImageLoadingIndicator()
    containerActiveImage.attr('src', '')
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

containerActiveImage.on("load", function () {
    completeImageLoadingIndicator()
}).on("error", function () {
    hideImageLoadingIndicator()
});
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
    downloadFromUrl(`${baseUrl}download/${data.page_id}/pdf`)
});
$(document).on("click", ".download-active-gif", function (event) {
    const data = activePageData()
    downloadFromUrl(`${baseUrl}download/${data.page_id}/gif`)
});

function downloadFromUrl(url) {
    showFullLoader()
    setTimeout(function () {
        hideFullLoader()
    }, 300)
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

function updateShareLinks(shareData) {
    const url = shareData.image_url;
    const shareUrl = shareData.share_url;
    // WhatsApp Share Icon
    $(".whatsapp").attr("href", `https://wa.me/?text=Vishwavani ePaper : ${encodeURIComponent(shareUrl)}`);
    // Facebook Share Icon
    $(".facebook").attr("href", "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(url));
    // Twitter Share Icon
    $(".twitter").attr("href", "https://twitter.com/intent/tweet?url=" + encodeURIComponent(shareData.share_url) + "&text=Vishwavani ePaper");
    // Download Icon
    $(".download-button").attr("href", `${baseUrl}direct?to=${url}`);
}

/// -------------------------------
/// -------------------------------
function showImageLoadingIndicator() {
    containerProgressBar.width('100%').attr('aria-valuenow', 0).text('0%');
    containerProgressBar.removeClass('bg-primary').addClass('bg-success').text('Loading...');
    simulateLoading()
    containerProgressBar.fadeIn()
}

function hideImageLoadingIndicator() {
    containerProgressBar.fadeOut();
    containerProgressBar.width('100%').attr('aria-valuenow', 0).text('0%');
}

function completeImageLoadingIndicator() {
    percentage = 100;
    updateProgress(percentage);
    containerProgressBar.fadeOut();
}

function updateProgress(percentage) {
    containerProgressBar.width(percentage + '%').attr('aria-valuenow', percentage).text(percentage + '%');
}

let percentage = 0;

function simulateLoading() {
    percentage = 0
    const interval = setInterval(function () {
        if (percentage >= 95) {
            clearInterval(interval);
        } else {
            percentage += 2;
            updateProgress(percentage);
        }
    }, 100);
}