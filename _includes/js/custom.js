var inp = document.getElementsByTagName("input")
for (var i = 0; i < inp.length; i++) {
    if ( inp[i].type == "checkbox" ) {
        inp[i].disabled=false;
    }
}