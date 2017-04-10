document.getElementById("symbol").addEventListener("change", updatePreview);

function updatePreview() {
    console.log("Running");
    var ele = document.getElementById("symbol");
    var preview = document.getElementById("preview");
    preview.className = ele.value;
}
