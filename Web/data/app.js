
function initPageContent() {
    document.getElementById("last-update").innerHTML += last_update;

    document.getElementById("bonjour-post").innerHTML += data.BonjourCosmetics["Post Content"];

    document.getElementById("sasa-post").innerHTML += data.SasaHongKong["Post Content"];

    document.getElementById("JHC-post").innerHTML += data.JHC["Post Content"];

}

function getBonjourUrl() {
    return data.BonjourCosmetics["FB Page Url"]
}

function getSasaUrl() {
    return data.SasaHongKong["FB Page Url"]
}

function getJHCUrl() {
    return data.JHC["FB Page Url"]
}

document.addEventListener("DOMContentLoaded", initPageContent);
