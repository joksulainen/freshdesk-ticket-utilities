document.getElementById("refreshlist_button").addEventListener("click", function() {
    var x = parseInt(document.getElementById("companyid_input").value)
    switch(x) {
        case 69:
        case 420:
        case 666:
        case 1337:
            alert("Ja!")
            break
        default:
            alert("Nein!")
            break
    }
});