var search = document.getElementById('search');
var list = false;

function toggSearch() {
    if(list){
        search.style.height = '0px'
        search.style.opacity = '0'
        list=false
    }else {
        search.style.height = '510px'
        search.style.opacity = '1'
        list=true;
        
    }
}