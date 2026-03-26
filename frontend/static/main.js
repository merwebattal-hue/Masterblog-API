window.onload = function () {
    const savedBaseUrl = localStorage.getItem("apiBaseUrl");

    if (savedBaseUrl) {
        document.getElementById("api-base-url").value = savedBaseUrl;
        loadPosts();
    }
};

function loadPosts() {
    const baseUrl = document.getElementById("api-base-url").value.trim();

    if (!baseUrl) {
        console.error("API base URL is missing.");
        return;
    }

    localStorage.setItem("apiBaseUrl", baseUrl);

    fetch(baseUrl + "/posts")
        .then(response => response.json())
        .then(data => {
            const postContainer = document.getElementById("post-container");
            postContainer.innerHTML = "";

            data.forEach(post => {
                const postDiv = document.createElement("div");
                postDiv.className = "post";

                postDiv.innerHTML = `
                    <h2>${post.title}</h2>
                    <p>${post.content}</p>
                    <p><strong>Author:</strong> ${post.author ?? "Unknown"}</p>
                    <p><strong>Date:</strong> ${post.date ?? "No date"}</p>
                    <button onclick="deletePost(${post.id})">Delete</button>
                `;

                postContainer.appendChild(postDiv);
            });
        })
        .catch(error => console.error("Error:", error));
}

function addPost() {
    const baseUrl = document.getElementById("api-base-url").value.trim();
    const postTitle = document.getElementById("post-title").value.trim();
    const postContent = document.getElementById("post-content").value.trim();

    const authorInput = document.getElementById("post-author");
    const dateInput = document.getElementById("post-date");

    const postAuthor = authorInput ? authorInput.value.trim() : "Unknown";
    const postDate = dateInput ? dateInput.value.trim() : new Date().toISOString().split("T")[0];

    if (!baseUrl) {
        console.error("API base URL is missing.");
        return;
    }

    if (!postTitle || !postContent) {
        console.error("Title and content are required.");
        return;
    }

    fetch(baseUrl + "/posts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            title: postTitle,
            content: postContent,
            author: postAuthor,
            date: postDate
        })
    })
        .then(response => response.json())
        .then(post => {
            console.log("Post added:", post);

            document.getElementById("post-title").value = "";
            document.getElementById("post-content").value = "";

            if (authorInput) authorInput.value = "";
            if (dateInput) dateInput.value = "";

            loadPosts();
        })
        .catch(error => console.error("Error:", error));
}

function deletePost(postId) {
    const baseUrl = document.getElementById("api-base-url").value.trim();

    if (!baseUrl) {
        console.error("API base URL is missing.");
        return;
    }

    fetch(baseUrl + "/posts/" + postId, {
        method: "DELETE"
    })
        .then(response => response.json())
        .then(data => {
            console.log("Post deleted:", data);
            loadPosts();
        })
        .catch(error => console.error("Error:", error));
}