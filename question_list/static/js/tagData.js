var word_list = [
    {text: "Java", weight: Math.random()*10, html: {title: "My Title", "class": "custom-class"}, link: {href: "", target: "_blank"}},
    {text: "C++", weight: Math.random()*10, link: "#"},
    {text: "mail.ru", weight: Math.random()*10, link: "#"},
    {text: "revolution 4.0", weight: Math.random()*10, link: "#"},
    {text: "AI", weight: Math.random()*10, link: "#"},
    {text: "augmented reality", weight: Math.random()*10, link: "#"},
    {text: "cats", weight: Math.random()*10, link: "#"},
    {text: "evangelion", weight: Math.random()*10, link: "#"},
    {text: "Kotlin", weight: Math.random()*10, link: "#"},
    {text: "web", weight: Math.random()*10, link: "#"},
    {text: "apple", weight: Math.random()*10, link: "#"},
    {text: "google", weight: Math.random()*10, link: "#"},
    {text: "destiny", weight: 6, link: "tag.html"},
  ];
  $(function() {
    $("#tagCloud").jQCloud(word_list);
  });