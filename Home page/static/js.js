document.getElementById('bell').addEventListener("click", function(){

    var box = document.getElementById('box');

    if(box.style.display === "none") {

        box.style.display ="block";
    } else {
        box.style.display ="none";
    }

});

