// console.log('img_file_hover.js loaded')
let img_list = document.querySelectorAll(".img-file");
console.log(img_list)

function build_img_thumbnail(elem_href) {
  let img_element = '<img alt="" src="' + elem_href + '" id="img" />';
  let div_element = '<div class="img_element_hover">' + img_element + '</div>';
  return div_element;
}

function display_img_thumbnail(elem_href) {
  let img_thumbnail = build_img_thumbnail(elem_href);
  let img_placement = document.querySelector("#img-placement");
  img_placement.innerHTML = img_thumbnail;
}

img_list.forEach(e => {
  return // retirer ça quand on peut servir les img localement
  e.addEventListener("mouseover", function (event) {
    let elem_href = e.getElementsByTagName('a')[0].getAttribute('href')
    // console.log(elem_href);
    display_img_thumbnail(elem_href)
  });
})

