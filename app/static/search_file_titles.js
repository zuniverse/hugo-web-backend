console.log("search_file_titles.js loaded");

let allFilesObj = [];
let searchInput = null;
let searchResultsDiv = null;

document.addEventListener("DOMContentLoaded", () => {
  searchInput = document.querySelector("input#search-input");
  if (!searchInput) return;

  console.log("this is a search page");
  clearSearchText();

  // Build a list of all file titles from html elements
  allFilesObj = Array.from(document.querySelectorAll(".list-content a"));
  console.log("allFilesObj length:", allFilesObj.length);
  // searchInput = document.querySelector("input#search-input");
  // searchInput.addEventListener("change", findMatch);
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

  // debug
  // console.log("searching for ", q);
  // return

  // if empty search input box, we erase the search results
  if (q === "") {
    searchResultsDiv.innerHTML = "";
    return;
  }

  // find matches
  let matchesFound = [];
  const needle = q.trim().toLowerCase();
  for (var i = 0; i < allFilesObj.length; i++) {
    const hay = allFilesObj[i].textContent.toLowerCase();
    //if (allFilesObj[i].textContent.toLowerCase().includes(q.toLowerCase())) {
    if (matchesOrderedSubsequence(hay, needle)) {
      matchesFound.push({
        href: allFilesObj[i].href,
        text: allFilesObj[i].textContent,
      });
    }
  }

  // display matches found in html (TODO: separate this into a different function)
  let contents = "";
  if (matchesFound.length > 0) {
    matchesFound.forEach((elem) => {
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
function matchesOrderedSubsequence(hay, needle) {
  hay = hay.toLowerCase();
  needle = needle.toLowerCase();

  let i = 0;
  for (const c of hay) {
    if (c === needle[i]) {
      i++;
      if (i === needle.length) return true;
    }
  }
  return false;
}
