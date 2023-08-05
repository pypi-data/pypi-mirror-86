var converter = new showdown.Converter({
  tables: true,
  strikethrough: true,
  simplifiedAutoLink: true,
});

window.onload = function () {

  var blogpost = document.getElementsByClassName("blogstrap");
  for (div of blogpost) {
    text = div.textContent.trim().split('/\n */').join('\n');
    var html = converter.makeHtml(text);
    div.innerHTML = html;
  }


  /* Bootstrap Classes */
  tables = blogpost[0].getElementsByTagName("table");
  for (table of tables) {
    table.classList.add("table");
  }

  quotes = blogpost[0].getElementsByTagName("blockquote");
  for (quote of quotes) {
    quote.classList.add("blockquote");
  }


  // the page starts hidden and is only shown visible after the whole
  // conversion is done, to avoid the flickering animation at the
  // start.
  document.body.style.visibility = "visible";

};
