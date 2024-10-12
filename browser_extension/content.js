function hidePosts() {
    const bannedTitles = ["Kamala", "IDF", "Trump", "Democrat", "Republican", "Donald"];
    const posts = document.querySelectorAll('article[class="w-full m-0"]');
    posts.forEach(post => {
        foo = post.getAttribute("aria-label");
        const title = foo;
          if (bannedTitles.some(bannedTitle => title.includes(bannedTitle.toLowerCase()))) {
            post.remove()
            console.log("removed: " + foo);
          }
    });
  }
  console.log("Started");
  hidePosts()
  setInterval(hidePosts, 2000);