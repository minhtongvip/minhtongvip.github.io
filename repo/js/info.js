function iOSVersion(){var match=(navigator.appVersion).split('OS ');if(match.length>1){return match[1].split(' ')[0].split('_').join('.');}return false;}

function isCompatibleIOS(version, compat) {
    if (!version || !compat) return false;

    var current = Math.floor(parseFloat(version));

    var numbers = compat.match(/\d+/g);
    if (!numbers || numbers.length < 2) return false;

    var min = parseInt(numbers[0], 10);
    var max = parseInt(numbers[1], 10);

    return current >= min && current <= max;
}

function loadPackageInfo(){if(navigator.userAgent.search(/Cydia/)==-1){$("#showAddRepo_").show();$("#showAddRepoUrl_").show();}
var urlSelfParts=window.location.href.split('info.html?id=');
var form_url=urlSelfParts[0]+"info/"+urlSelfParts[1];

var logoHtml =
    '<div class="logo">' +
        '<img src="../img/logo/cert.png" alt="Logo">' +
    '</div>';

$("#logo").html(logoHtml);

$.ajax({url:form_url,type:"GET",dataType:"json",cache:false,crossDomain: true,success:function(decodeResp){
$("#tweakStatusInfo").hide();

if(decodeResp.name){document.title=decodeResp.name;$("#name").html(decodeResp.name).show();}

if(decodeResp.desc_long){$("#desc_long").html(decodeResp.desc_long);$("#desc_long_").show();}

if (decodeResp.compatitle) {
    var ios_ver = iOSVersion();

    if (ios_ver) {
        $("#your_ios_").show();

        if (isCompatibleIOS(ios_ver, decodeResp.compatitle)) {
            $("#your_ios").html('<span class="compatible">✅ iOS hiện tại đã tương thích.</span>');
        } else {
            $("#your_ios").html('<span class="not-compatible">❌ iOS hiện tại không tương thích.</span>');
        }
    }
}

if (decodeResp.screenshots && decodeResp.screenshots.length) {

    var html = '<div class="screenshot-viewer">';

    var total = Math.min(decodeResp.screenshots.length, 2);

    for (var i = 0; i < total; i++) {

        var img = decodeResp.screenshots[i];

        html +=
            '<li>' +
                '<a href="' + img + '" target="_blank">' +
                    '<img src="' + img + '" alt="Screenshot">' +
                '</a>' +
            '</li>';
    }

    html += '</div>';

    $("#screenshot").html(html);
    $("#screenshot_").show();
}

},
error:function(){
    $("#errorInfo").html("Mô tả không có sẵn cho "+urlSelfParts[1]).show();
}
});

var supportHtml =
    '<div class="card support-card">' +
        '<div class="section-title">Liên hệ & Hỗ trợ</div>' +

        '<div class="support-row">' +

            '<a href="https://facebook.com/quangminhios" ' +
               'target="_blank" ' +
               'class="support-btn">' +
                '<span>Facebook 👍</span>' +
            '</a>' +

            '<a href="https://zalo.me/0868388373" ' +
               'target="_blank" ' +
               'class="support-btn">' +
                '<span>Zalo 💬</span>' +
            '</a>' +

        '</div>' +

        '<div class="qr-box">' +
            '<img src="../img/logo/QR.png" alt="QR">' +
            '<p class="donate-text">' +
                '❤️ Nếu bạn thấy hữu ích, hãy ủng hộ tôi.' +
            '</p>' +
        '</div>' +
    '</div>' +

        '<footer class="footer">' + '© Bản quyền thuộc về TQM-MOS.' + '</footer>';

$("#support").html(supportHtml);
}