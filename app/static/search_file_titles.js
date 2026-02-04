console.log("search_file_titles.js loaded");

let allFilesObj = [];
let searchInput = null;
let searchResultsDiv = null;

document.addEventListener("DOMContentLoaded", () => {
  searchInput = document.querySelector("input#search-input");
  if (!searchInput) return;

  console.log("this is a search page");
  clearSearchText();

  //get all html elements
  allFilesObj = Array.from(document.querySelectorAll(".list-content a"));
  console.log("allFilesObj length:", allFilesObj.length);
  // searchInput = document.querySelector("input#search-input");
  //searchInput.addEventListener("change", findMatch);
  searchResultsDiv = document.getElementById("search-result");
  if (!searchResultsDiv) {
    console.warn("Missing element: #search-result");
  }

  searchInput.addEventListener("input", findMatch);
});

// build array of objects : text & elem
// analyse input & pour chaque input in text, retourner la liste des elem et l'afficher
function findMatch(e) {
  const q = e.target.value.trim();
  console.log("searching for ", q);
  // return

  // si vide, on efface
  if (q === "") {
    searchResultsDiv.innerHTML = "";
    return;
  }

  let found = [];
  const needle = q.trim().toLowerCase();
  for (var i = 0; i < allFilesObj.length; i++) {
    const hay = allFilesObj[i].textContent.toLowerCase();
    //if (allFilesObj[i].textContent.toLowerCase().includes(q.toLowerCase())) {
    if (matchesOrderedSubsequence(hay, needle)) {
      found.push({
        href: allFilesObj[i].href,
        text: allFilesObj[i].textContent,
      });
    }
  }

  // à separer
  let contents = "";
  if (found.length > 0) {
    found.forEach((elem) => {
      const div =
        '<p class="list-content"><a href="' +
        elem.href +
        '">' +
        elem.text +
        "</a></p>";
      contents += div;
    });
    searchResultsDiv.innerHTML = contents;
  }
  //clearSearchText();
}

function clearSearchText() {
  console.log("clearing search text input");
  //return
  if (searchInput) {
    searchInput.value = "";
  }
}

// TODO chercher un match par sous-sequence ordonnée de texte plutot que query length,
// pour obtenir une série de lettre séquentielles qui matchent le haystack
// pour ne pas que comme actuellement, "rdme" match "ReadMe.txt"
function matchesOrderedSubsequence(text, query) {
  text = text.toLowerCase();
  query = query.toLowerCase();

  let i = 0;
  for (const c of text) {
    if (c === query[i]) {
      i++;
      if (i === query.length) return true;
    }
  }
  return false;
}
