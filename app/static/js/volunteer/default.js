/* When the user clicks on the button,
toggle between hiding and showing the dropdown content */
function clickDropBtn(id, dropList) {
    
    var dropbtn = document.getElementById(dropList).classList;
    
    dropbtn.toggle("show");
    
    var child_image = document.querySelector('#' + id + ' .dropbtn-image');
    if (dropbtn.contains('show')) {
        closeDropBtnAll();
        dropbtn.toggle("show");
        child_image.innerHTML = 'open';
    } else {
        child_image.innerHTML = 'close';
    }
}

// Close the dropdown menu if the user clicks outside of it
window.onclick = function(event) {
    if (!event.target.matches('.drop-btn-wrapper')) closeDropBtnAll();
}

function closeDropBtnAll() {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    var i;
    for (i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i];
        if (openDropdown.classList.contains('show')) {
            openDropdown.classList.remove('show');
        }
    }
    var children = document.querySelectorAll('.dropbtn-image');
    children.forEach(element => {
        element.innerHTML = 'close';
    });
}

function setDropBtnName(id, name) {
    var child = document.querySelector('#' + id + ' .dropbtn');
    child.innerHTML = name;
    child.style.color = "black";
    
    var dropDownClicked = document.getElementById(id + "_isClicked");
    dropDownClicked.value = "true";
}

var dropBtnIgnore = document.querySelectorAll('.dropbtn');
var dropBtnImageIgnore = document.querySelectorAll('.dropbtn-image');

function ignoreOnClick(selectorAll) {
    var k = [1,2,3,4,6];
    selectorAll.forEach(element => {
        element.addEventListener('click',function (e){
            e.stopPropagation();
        });
    });
}

ignoreOnClick(dropBtnIgnore);
ignoreOnClick(dropBtnImageIgnore);
